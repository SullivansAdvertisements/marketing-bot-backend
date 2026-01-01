"""
Budget Allocation Engine
------------------------
Splits budget across platforms using proven media buying heuristics.
"""

from typing import Dict


def allocate_budget(
    total_budget: float,
    objective: str,
    risk_level: str = "balanced",  # conservative | balanced | aggressive
) -> Dict[str, float]:

    if total_budget <= 0:
        raise ValueError("Budget must be greater than 0")

    # -------------------------------------------------
    # Base allocation by objective
    # -------------------------------------------------
    if objective == "awareness":
        weights = {
            "meta": 0.45,
            "youtube": 0.35,
            "tiktok": 0.20,
        }
    elif objective == "traffic":
        weights = {
            "meta": 0.55,
            "google_search": 0.30,
            "tiktok": 0.15,
        }
    elif objective == "sales":
        weights = {
            "meta": 0.60,
            "google_search": 0.30,
            "retargeting": 0.10,
        }
    else:
        weights = {
            "meta": 0.50,
            "google_search": 0.25,
            "youtube": 0.25,
        }

    # -------------------------------------------------
    # Risk adjustments
    # -------------------------------------------------
    if risk_level == "conservative":
        weights["meta"] += 0.05
        weights = _normalize(weights)
    elif risk_level == "aggressive":
        weights["tiktok"] = weights.get("tiktok", 0) + 0.10
        weights = _normalize(weights)

    # -------------------------------------------------
    # Convert to dollar values
    # -------------------------------------------------
    return {
        platform: round(total_budget * pct, 2)
        for platform, pct in weights.items()
    }


def _normalize(weights: Dict[str, float]) -> Dict[str, float]:
    total = sum(weights.values())
    return {k: v / total for k, v in weights.items()}
