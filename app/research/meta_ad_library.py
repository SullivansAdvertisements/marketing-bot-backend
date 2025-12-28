import requests
import os

META_AD_LIBRARY_TOKEN = os.getenv("META_AD_LIBRARY_TOKEN")

def get_meta_ads(keyword: str, country: str = "US"):
    url = "https://graph.facebook.com/v19.0/ads_archive"

    params = {
        "search_terms": keyword,
        "ad_active_status": "ALL",
        "ad_type": "ALL",
        "ad_reached_countries": country,
        "access_token": META_AD_LIBRARY_TOKEN,
        "fields": "ad_creative_bodies,ad_creative_link_titles,page_name,ad_delivery_start_time",
    }

    r = requests.get(url, params=params)
    data = r.json()

    return data.get("data", [])