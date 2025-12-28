"""
Performance Estimator
---------------------
Returns realistic outcome ranges using public benchmark data.
"""

from typing import Dict


BENCHMARKS = {
    "meta": {
        "cpm": (8, 18),
        "ctr": (0.8, 1.5),
        "conversion_rate": (0.8, 2.5),
    },
    "google_search": {
        "cpc": (1.2, 4.5),
        "conversion_rate": (2.0, 6.0),
    },
    "tiktok": {
        "cpm": (6, 14),
        "ctr": (0.6, 1.2),
        "conversion_rate": (0.6, 1.8),
    },
}


def estimate_results(
    platform: str,
    budget: float,
    average_order_value: float = 50.0,
) -> Dict[str, float]:

    if platform not in BENCHMARKS:
        raise ValueError("Unsupported platform")

    metrics = BENCHMARKS[platform]

    # -------------------------------------------------
    # CPM based platforms
    # -------------------------------------------------
    if "cpm" in metrics:
        avg_cpm = sum(metrics["cpm"]) / 2
        impressions = (budget / avg_cpm) * 1000

        avg_ctr = sum(metrics["ctr"]) / 2 / 100
        clicks = impressions * avg_ctr

        avg_cr = sum(metrics["conversion_rate"]) / 2 / 100
        conversions = clicks * avg_cr

    # -------------------------------------------------
    # CPC based platforms
    # -------------------------------------------------
    else:
        avg_cpc = sum(metrics["cpc"]) / 2
        clicks = budget / avg_cpc

        avg_cr = sum(metrics["conversion_rate"]) / 2 / 100
        conversions = clicks * avg_cr

    revenue = conversions * average_order_value

    return {
        "estimated_clicks": round(clicks),
        "estimated_conversions": round(conversions, 1),
        "estimated_revenue": round(revenue, 2),
    }