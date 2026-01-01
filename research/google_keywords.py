import os
import pandas as pd
import requests

# Read from Streamlit secrets or env
GOOGLE_ADS_API_KEY = os.getenv("GOOGLE_ADS_API_KEY")


def fetch_google_keywords(keyword: str, country: str = "US"):
    """
    Fetch keyword metrics from Google Ads API.
    SAFE for Streamlit: never crashes the app.

    Returns:
        pd.DataFrame
    """

    # -----------------------------
    # FAIL SAFE (NO HARD CRASH)
    # -----------------------------
    if not GOOGLE_ADS_API_KEY:
        return pd.DataFrame([
            {
                "keyword": keyword,
                "avg_monthly_searches": "N/A",
                "competition": "N/A",
                "top_of_page_cpc": "N/A",
                "note": "GOOGLE_ADS_API_KEY missing"
            }
        ])

    # -----------------------------
    # API CONFIG (PLACEHOLDER)
    # -----------------------------
    url = "https://googleads.googleapis.com/v13/customers:search"

    headers = {
        "Authorization": f"Bearer {GOOGLE_ADS_API_KEY}",
        "Content-Type": "application/json",
        "developer-token": GOOGLE_ADS_API_KEY,  # placeholder
    }

    query = f"""
        SELECT
            keyword_view.resource_name,
            metrics.avg_monthly_searches,
            metrics.competition,
            metrics.high_top_of_page_bid_micros
        FROM keyword_view
        WHERE segments.keyword.info.text LIKE '%{keyword}%'
    """

    payload = {
        "query": query
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        rows = []

        for row in data.get("results", []):
            metrics = row.get("metrics", {})
            rows.append({
                "keyword": keyword,
                "avg_monthly_searches": metrics.get("avg_monthly_searches"),
                "competition": metrics.get("competition"),
                "top_of_page_cpc": (
                    metrics.get("high_top_of_page_bid_micros", 0) / 1_000_000
                    if metrics.get("high_top_of_page_bid_micros")
                    else None
                ),
            })

        if not rows:
            return pd.DataFrame([{
                "keyword": keyword,
                "avg_monthly_searches": 0,
                "competition": "Low",
                "top_of_page_cpc": 0.0,
            }])

        return pd.DataFrame(rows)

    except Exception as e:
        # NEVER crash Streamlit
        return pd.DataFrame([{
            "keyword": keyword,
            "avg_monthly_searches": "Error",
            "competition": "Error",
            "top_of_page_cpc": "Error",
            "error": str(e),
        }])