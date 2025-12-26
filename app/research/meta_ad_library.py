import requests
import os

def search_meta_ads(query, country):
    url = "https://graph.facebook.com/v19.0/ads_archive"
    params = {
        "search_terms": query,
        "ad_type": "ALL",
        "ad_reached_countries": country,
        "access_token": os.getenv("META_ACCESS_TOKEN")
    }
    return requests.get(url, params=params).json()