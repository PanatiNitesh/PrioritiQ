import json
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from ..database.db import get_connection

class ScoringRulesConfig(BaseModel):
    stage_weights: Dict[str, float] = Field(default_factory=lambda: {
        "Closing": 1.0,
        "Negotiation": 0.88,
        "Proposal": 0.72,
        "Demo": 0.55,
        "Discovery": 0.35
    })
    strategy_weights: Dict[str, Dict[str, float]] = Field(default_factory=lambda: {
        "balanced": {"w_deal": 0.25, "w_intent": 0.25, "w_stage": 0.20, "w_icp": 0.15, "w_recency": 0.15},
        "deal_value": {"w_deal": 0.65, "w_intent": 0.15, "w_stage": 0.10, "w_icp": 0.05, "w_recency": 0.05},
        "velocity": {"w_deal": 0.05, "w_intent": 0.35, "w_stage": 0.35, "w_icp": 0.10, "w_recency": 0.15},
        "win_rate": {"w_deal": 0.05, "w_intent": 0.35, "w_stage": 0.35, "w_icp": 0.10, "w_recency": 0.15}
    })
    churn_penalties: Dict[str, float] = Field(default_factory=lambda: {
        "Low": 1.0,
        "Medium": 0.85,
        "High": 0.55
    })
    recency_decay_half_life_days: float = 4.0

DEFAULT_SCORING_RULES = ScoringRulesConfig().model_dump()

def get_active_scoring_rules() -> Dict[str, Any]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT rules_json FROM scoring_rules WHERE id = 'active'")
    row = cur.fetchone()
    conn.close()
    if row and row[0]:
        try:
            return json.loads(row[0])
        except Exception:
            pass
    return DEFAULT_SCORING_RULES

def load_scoring_rules() -> ScoringRulesConfig:
    d = get_active_scoring_rules()
    return ScoringRulesConfig(**d)

def update_scoring_rules(new_rules: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_connection()
    cur = conn.cursor()
    merged = {**DEFAULT_SCORING_RULES, **new_rules}
    cur.execute("INSERT OR REPLACE INTO scoring_rules (id, rules_json) VALUES ('active', ?)", (json.dumps(merged),))
    conn.commit()
    conn.close()
    return merged

def save_scoring_rules(config: ScoringRulesConfig) -> Dict[str, Any]:
    return update_scoring_rules(config.model_dump())
