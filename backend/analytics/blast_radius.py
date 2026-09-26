import math
from typing import Dict, Any, List

class BlastRadiusPredictor:
    """
    Computes enterprise blast-radius metrics before executing resource reallocations:
    1. Account Attrition Blast Radius (cost of neglect, high churn accounts left behind)
    2. Sales Rep Capacity Skew (per-rep load variance, bottleneck detection)
    3. Quota & Commitment Slippage (quarter-end commits deferred)
    """

    def __init__(self, default_rep_daily_capacity_mins: int = 180):
        self.default_rep_daily_capacity_mins = default_rep_daily_capacity_mins

    def predict(
        self,
        all_leads: List[Dict[str, Any]],
        recommended_leads: List[Dict[str, Any]],
        time_budget_hours: float = None
    ) -> Dict[str, Any]:
        rec_ids = {r.get("lead_id") for r in recommended_leads}
        excluded_leads = [l for l in all_leads if l.get("lead_id") not in rec_ids]

        # 1. Account Attrition Blast Radius
        total_excluded_value = sum(float(l.get("deal_size", 0)) for l in excluded_leads)
        high_churn_excluded = [
            l for l in excluded_leads 
            if str(l.get("churn_risk", "")).lower() == "high"
        ]
        med_churn_excluded = [
            l for l in excluded_leads 
            if str(l.get("churn_risk", "")).lower() == "medium"
        ]
        
        at_risk_excluded_value = sum(float(l.get("deal_size", 0)) for l in high_churn_excluded)
        
        # Estimate churn probability delta per deferred day (~3.5% daily compounding attrition on high-risk accounts)
        daily_attrition_cost = sum(float(l.get("deal_size", 0)) * 0.035 for l in high_churn_excluded) + \
                               sum(float(l.get("deal_size", 0)) * 0.012 for l in med_churn_excluded)

        # 2. Sales Rep Capacity Skew & Bottlenecks
        all_reps = sorted(list(set(l.get("assigned_rep", "Unassigned") for l in all_leads if l.get("assigned_rep"))))
        if not all_reps:
            all_reps = ["Alex Rivera", "Devon Miller", "Sarah Chen"]

        rep_allocations: Dict[str, Dict[str, Any]] = {
            rep: {
                "rep_name": rep,
                "deals_count": 0,
                "total_effort_mins": 0,
                "deal_value_allocated": 0.0,
                "bottleneck_risk": False,
                "utilization_pct": 0.0
            } for rep in all_reps
        }

        total_rec_mins = sum(int(r.get("est_effort_mins", 30)) for r in recommended_leads)

        for r in recommended_leads:
            rep = r.get("assigned_rep", "Alex Rivera")
            if rep not in rep_allocations:
                rep_allocations[rep] = {
                    "rep_name": rep,
                    "deals_count": 0,
                    "total_effort_mins": 0,
                    "deal_value_allocated": 0.0,
                    "bottleneck_risk": False,
                    "utilization_pct": 0.0
                }
            rep_allocations[rep]["deals_count"] += 1
            effort = int(r.get("est_effort_mins", 30))
            rep_allocations[rep]["total_effort_mins"] += effort
            rep_allocations[rep]["deal_value_allocated"] += float(r.get("deal_size", 0))

        # Calculate utilization and per-rep bottleneck risk
        rep_effort_list = []
        warnings = []

        rep_cap_mins = self.default_rep_daily_capacity_mins
        if time_budget_hours:
            # Shared fraction
            rep_cap_mins = max(45, int((time_budget_hours * 60) / max(1, len(all_reps))))

        for rep, stats in rep_allocations.items():
            mins = stats["total_effort_mins"]
            rep_effort_list.append(mins)
            utilization = round((mins / rep_cap_mins) * 100, 1)
            stats["utilization_pct"] = utilization

            # Flag bottleneck if a single rep has >180 mins or >70% of total team hours
            if mins > 180 or (total_rec_mins > 0 and mins / total_rec_mins > 0.65 and len(all_reps) > 1):
                stats["bottleneck_risk"] = True
                warnings.append(
                    f"Rep Bottleneck: {rep} assigned {mins} mins ({stats['deals_count']} deals), exceeding sustainable daily allocation."
                )
            elif mins == 0 and len(recommended_leads) >= len(all_reps):
                warnings.append(
                    f"Rep Starvation: {rep} allocated 0 minutes while team has active priority volume."
                )

        # Variance calculation for capacity skew
        if rep_effort_list:
            mean_effort = sum(rep_effort_list) / len(rep_effort_list)
            variance = sum((x - mean_effort) ** 2 for x in rep_effort_list) / len(rep_effort_list)
            std_dev = math.sqrt(variance)
        else:
            std_dev = 0.0

        # 3. Quota & Commitment Slippage
        # Deals in Negotiation or Proposal that were excluded
        late_stage_excluded = [
            l for l in excluded_leads
            if str(l.get("stage", "")).lower() in ["negotiation", "proposal", "contract"]
        ]
        late_stage_slippage_val = sum(float(l.get("deal_size", 0)) for l in late_stage_excluded)
        if late_stage_slippage_val > 100000:
            warnings.append(
                f"Commitment Slippage Risk: ${late_stage_slippage_val:,.0f} across {len(late_stage_excluded)} late-stage deals deferred outside current batch."
            )

        if high_churn_excluded:
            top_churn_names = ", ".join([l.get("name_y") or l.get("lead_name") or l.get("lead_id") for l in high_churn_excluded[:2]])
            warnings.append(
                f"Attrition Risk: {len(high_churn_excluded)} high-churn accounts omitted ({top_churn_names}) with ${at_risk_excluded_value:,.0f} pipeline exposure."
            )

        # Composite Collateral Risk Score (0 = Low Risk, 100 = Catastrophic Blast Radius)
        risk_components = 0
        if at_risk_excluded_value > 150000:
            risk_components += 30
        elif at_risk_excluded_value > 50000:
            risk_components += 15

        if any(stats["bottleneck_risk"] for stats in rep_allocations.values()):
            risk_components += 25

        if std_dev > 45:
            risk_components += 20
        elif std_dev > 25:
            risk_components += 10

        if late_stage_slippage_val > 150000:
            risk_components += 25
        elif late_stage_slippage_val > 50000:
            risk_components += 15

        collateral_score = min(100, risk_components)

        return {
            "collateral_damage_score": collateral_score,
            "risk_level": "CRITICAL" if collateral_score >= 60 else "ELEVATED" if collateral_score >= 35 else "LOW",
            "excluded_accounts_count": len(excluded_leads),
            "excluded_pipeline_value": total_excluded_value,
            "at_risk_excluded_value": at_risk_excluded_value,
            "estimated_daily_attrition_cost": round(daily_attrition_cost, 2),
            "late_stage_slippage_value": late_stage_slippage_val,
            "late_stage_deferred_count": len(late_stage_excluded),
            "rep_skew_std_dev_mins": round(std_dev, 1),
            "rep_utilizations": list(rep_allocations.values()),
            "warnings": warnings,
            "high_churn_omitted_leads": [
                {
                    "lead_id": l.get("lead_id"),
                    "name": l.get("lead_name") or l.get("name"),
                    "company": l.get("company_name") or l.get("name_y") or l.get("company_id"),
                    "deal_size": float(l.get("deal_size", 0)),
                    "churn_risk": l.get("churn_risk", "High"),
                    "stage": l.get("stage")
                } for l in high_churn_excluded[:5]
            ]
        }
