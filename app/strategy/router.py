"""
Strategy Router
---------------
Thin interface for Streamlit.
"""

from typing import Dict

from .budget_allocator import allocate_budget
from .performance_estimator import estimate_results


def generate_strategy(
    total_budget: float,
    objective: str,
    risk_level: str,
    average_order_value: float,
) -> Dict:

    allocation = allocate_budget(
        total_budget=total_budget,
        objective=objective,
        risk_level=risk_level,
    )

    projections = {}

    for platform, budget in allocation.items():
        try:
            projections[platform] = estimate_results(
                platform=platform,
                budget=budget,
                average_order_value=average_order_value,
            )
        except Exception:
            projections[platform] = {"note": "No benchmark available"}

    return {
        "allocation": allocation,
        "projections": projections,
        "assumptions": {
            "objective": objective,
            "risk_level": risk_level,
            "aov": average_order_value,
        },
    }