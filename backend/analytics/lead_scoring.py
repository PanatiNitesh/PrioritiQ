import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
from ..database.db import get_all_leads_with_companies, get_max_dataset_timestamp
from .rules import get_active_scoring_rules

def load_data():
    """
    Direct in-memory/database retrieval without repeated disk CSV reads (Weakness 4).
    """
    leads = get_all_leads_with_companies()
    df = pd.DataFrame(leads)
    return df

def compute_deterministic_scores(priority_weight: str = "balanced") -> pd.DataFrame:
    """
    Computes grounded, deterministic lead scores:
    - Eliminates static hardcoded reference dates via dynamic dataset epoch (Weakness 10).
    - Uses customizable developer scoring policies (Weakness 14).
    - Database backed without CSV disk thrashing (Weakness 4).
    """
    df = load_data()
    if df.empty:
        return df

    rules = get_active_scoring_rules()
    stage_weights = rules.get("stage_weights", {})
    strategy_map = rules.get("strategy_weights", {})
    weights = strategy_map.get(priority_weight, strategy_map.get("balanced", {}))
    churn_penalties = rules.get("churn_penalties", {})
    half_life_days = rules.get("recency_decay_half_life_days", 4.0)

    # Dynamic reference epoch: Max timestamp in dataset or current time (Weakness 10)
    now_ref = get_max_dataset_timestamp()

    # Recency factor
    df['last_act_dt'] = pd.to_datetime(df['last_activity_date'], errors='coerce').fillna(now_ref)
    df['days_since_act'] = (now_ref - df['last_act_dt']).dt.total_seconds() / 86400.0
    df['days_since_act'] = df['days_since_act'].clip(lower=0.0)
    df['recency_multiplier'] = np.exp(-df['days_since_act'] / half_life_days)

    # Stage factor
    df['stage_score'] = df['stage'].map(stage_weights).fillna(0.35)

    # Deal size log normalization ($50k to $500k range)
    min_deal, max_deal = 50000.0, 500000.0
    df['deal_normalized'] = np.clip(
        (np.log(df['deal_size'].clip(lower=min_deal)) - np.log(min_deal)) / (np.log(max_deal) - np.log(min_deal)),
        0.0, 1.0
    )

    # ICP and Intent normalization
    df['icp_normalized'] = df['icp_fit'].fillna(80) / 100.0
    df['intent_normalized'] = df['intent_score'].fillna(50) / 100.0

    # Multi-signal composite score
    w_deal = weights.get("w_deal", 0.25)
    w_intent = weights.get("w_intent", 0.25)
    w_stage = weights.get("w_stage", 0.20)
    w_icp = weights.get("w_icp", 0.15)
    w_recency = weights.get("w_recency", 0.15)

    df['raw_score'] = (
        (df['deal_normalized'] * w_deal) +
        (df['intent_normalized'] * w_intent) +
        (df['stage_score'] * w_stage) +
        (df['icp_normalized'] * w_icp) +
        (df['recency_multiplier'] * w_recency)
    )

    # Churn risk penalty
    df['churn_factor'] = df['churn_risk'].map(churn_penalties).fillna(1.0)
    df['final_score'] = (df['raw_score'] * df['churn_factor'] * 100.0).round(1)

    # Sort descending
    df = df.sort_values(by="final_score", ascending=False).reset_index(drop=True)
    return df
