import numpy as np
from typing import Dict, Any, List, Optional

class MonteCarloPipelineSimulator:
    """
    Stochastic Monte Carlo Pipeline Risk & Revenue Simulator.
    Simulates 1,000 quarterly market execution trials comparing:
    - PrioritiQ Optimized Capacity Schedule
    - Unprioritized Legacy CRM FIFO Ordering
    Provides P10 (Pessimistic), P50 (Median), P90 (Optimistic), expected revenue lift,
    and probability density distributions.
    """

    def __init__(self, random_seed: int = 42):
        self.seed = random_seed

    def simulate(
        self,
        all_leads: List[Dict[str, Any]],
        recommended_leads: List[Dict[str, Any]],
        trials: int = 1000,
        market_volatility: float = 0.12,
        execution_efficiency: float = 1.0
    ) -> Dict[str, Any]:
        rng = np.random.RandomState(self.seed)
        rec_ids = set(l.get("lead_id") for l in recommended_leads)

        # Baseline stage win probabilities
        stage_base_probs = {
            "closing": 0.82,
            "negotiation": 0.64,
            "proposal": 0.45,
            "demo": 0.28,
            "discovery": 0.18
        }

        # Churn risk multipliers
        churn_multipliers = {
            "high": 0.70,
            "medium": 0.88,
            "low": 1.00
        }

        opt_trial_revenues = np.zeros(trials)
        base_trial_revenues = np.zeros(trials)
        opt_wins_count = np.zeros(trials)
        base_wins_count = np.zeros(trials)

        for trial in range(trials):
            trial_opt_rev = 0.0
            trial_base_rev = 0.0
            trial_opt_wins = 0
            trial_base_wins = 0

            for lead in all_leads:
                lid = lead.get("lead_id")
                stage = (lead.get("stage") or "proposal").lower()
                deal_size = float(lead.get("deal_size") or lead.get("deal_value") or 50000)
                churn = (lead.get("churn_risk") or "low").lower()
                intent = float(lead.get("intent_score") or 50.0)
                icp = float(lead.get("icp_fit") or 80.0)

                base_prob = stage_base_probs.get(stage, 0.35) * churn_multipliers.get(churn, 0.9)

                # PrioritiQ Optimized Touchpoint boost if scheduled
                if lid in rec_ids:
                    # Focused engagement boosts conversion probability
                    touch_boost = (1.0 + (0.28 * (intent / 100.0) + 0.15 * (icp / 100.0))) * execution_efficiency
                    opt_prob = min(0.96, base_prob * touch_boost)
                else:
                    # Deferral / neglect penalty for omitted accounts
                    omission_decay = 0.88 if churn == "high" else 0.95
                    opt_prob = max(0.05, base_prob * omission_decay)

                # Stochastic deal value with market variance noise
                noise = rng.normal(1.0, market_volatility)
                realized_value = max(0.0, deal_size * noise)

                # Simulation roll for Optimized
                if rng.rand() < opt_prob:
                    trial_opt_rev += realized_value
                    trial_opt_wins += 1

                # Simulation roll for Baseline
                if rng.rand() < base_prob:
                    trial_base_rev += realized_value
                    trial_base_wins += 1

            opt_trial_revenues[trial] = trial_opt_rev
            base_trial_revenues[trial] = trial_base_rev
            opt_wins_count[trial] = trial_opt_wins
            base_wins_count[trial] = trial_base_wins

        # Summary Statistics
        ev_opt = float(np.mean(opt_trial_revenues))
        ev_base = float(np.mean(base_trial_revenues))
        lift_dollars = ev_opt - ev_base
        lift_pct = round((lift_dollars / max(1.0, ev_base)) * 100.0, 1)

        # Percentiles
        p10_opt = float(np.percentile(opt_trial_revenues, 10))
        p50_opt = float(np.percentile(opt_trial_revenues, 50))
        p90_opt = float(np.percentile(opt_trial_revenues, 90))

        p10_base = float(np.percentile(base_trial_revenues, 10))
        p50_base = float(np.percentile(base_trial_revenues, 50))
        p90_base = float(np.percentile(base_trial_revenues, 90))

        win_prob_better = round(float(np.mean(opt_trial_revenues > base_trial_revenues)) * 100.0, 1)

        # Generate Histogram Distribution Buckets for Visual UI Chart
        min_rev = min(float(np.min(base_trial_revenues)), float(np.min(opt_trial_revenues)))
        max_rev = max(float(np.max(base_trial_revenues)), float(np.max(opt_trial_revenues)))
        bins = np.linspace(min_rev, max_rev, 11)

        opt_hist, _ = np.histogram(opt_trial_revenues, bins=bins)
        base_hist, _ = np.histogram(base_trial_revenues, bins=bins)

        distribution_buckets = []
        for i in range(len(opt_hist)):
            distribution_buckets.append({
                "range_min": round(float(bins[i])),
                "range_max": round(float(bins[i+1])),
                "label": f"${bins[i]/1000:,.0f}k - ${bins[i+1]/1000:,.0f}k",
                "prioritiq_density": int(opt_hist[i]),
                "baseline_density": int(base_hist[i])
            })

        return {
            "simulation_trials": trials,
            "market_volatility": market_volatility,
            "expected_revenue_optimized": round(ev_opt, 2),
            "expected_revenue_baseline": round(ev_base, 2),
            "projected_revenue_lift": round(lift_dollars, 2),
            "lift_percentage": lift_pct,
            "probability_outperforming_baseline_pct": win_prob_better,
            "prioritiq_schedule": {
                "p10_conservative": round(p10_opt, 2),
                "p50_median": round(p50_opt, 2),
                "p90_optimistic": round(p90_opt, 2),
                "avg_deals_won": round(float(np.mean(opt_wins_count)), 1)
            },
            "legacy_crm_baseline": {
                "p10_conservative": round(p10_base, 2),
                "p50_median": round(p50_base, 2),
                "p90_optimistic": round(p90_base, 2),
                "avg_deals_won": round(float(np.mean(base_wins_count)), 1)
            },
            "distribution_buckets": distribution_buckets,
            "executive_summary": (
                f"Monte Carlo simulation over {trials:,} stochastic market trials projects "
                f"an expected quarterly revenue of ${ev_opt:,.0f} under PrioritiQ schedule vs "
                f"${ev_base:,.0f} under unprioritized legacy baseline—generating an estimated "
                f"+${lift_dollars:,.0f} (+{lift_pct}%) commercial lift with {win_prob_better}% confidence."
            )
        }
