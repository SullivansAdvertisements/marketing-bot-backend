import os
import requests
import pandas as pd


META_AD_LIBRARY_TOKEN = os.getenv("META_AD_LIBRARY_TOKEN")


def fetch_meta_ads(keyword: str):
    if not keyword or not META_AD_LIBRARY_TOKEN:
        return pd.DataFrame()

    url = "https://graph.facebook.com/v18.0/ads_archive"

    params = {
        "access_token": META_AD_LIBRARY_TOKEN,
        "search_terms": keyword,
        "ad_type": "ALL",
        "fields": "page_name,ad_creative_body,ad_delivery_start_time",
        "limit": 10,
    }

    r = requests.get(url, params=params, timeout=10)

    if r.status_code != 200:
        return pd.DataFrame()

    data = r.json().get("data", [])

    rows = []
    for ad in data:
        rows.append({
            "page": ad.get("page_name"),
            "text": ad.get("ad_creative_body"),
            "start_date": ad.get("ad_delivery_start_time"),
        })

    return pd.DataFrame(rows)