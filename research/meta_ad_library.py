import requests
import os

META_TOKEN = os.getenv("META_ACCESS_TOKEN")

def fetch_meta_ads(keyword, country="US", limit=50):
    url = "https://graph.facebook.com/v19.0/ads_archive"

    params = {
        "search_terms": keyword,
        "ad_active_status": "ACTIVE",
        "ad_type": "ALL",
        "countries": country,
        "fields": "ad_creative_body,ad_creative_link_caption,ad_creative_link_title,cta_type,page_name",
        "access_token": META_TOKEN,
        "limit": limit,
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    return data.get("data", [])