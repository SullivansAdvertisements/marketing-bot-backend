import requests
import os

GOOGLE_ADS_API_KEY = os.getenv("GOOGLE_ADS_API_KEY")

def get_google_keywords(keyword: str):
    if not GOOGLE_ADS_API_KEY:
        raise Exception("GOOGLE_ADS_API_KEY missing")

    url = "https://googleads.googleapis.com/v13/customers:search"

    query = f"""
    SELECT
      keyword_view.resource_name,
      metrics.avg_monthly_searches,
      metrics.competition,
      metrics.high_top_of_page_bid_micros
    FROM keyword_view
    WHERE segments.keyword.info.text LIKE '%{keyword}%'
    """

    headers = {
        "Authorization": f"Bearer {GOOGLE_ADS_API_KEY}",
        "Content-Type": "application/json",
    }

    r = requests.post(url, json={"query": query}, headers=headers)
    data = r.json()

    return data.get("results", [])