import requests
import os

TIKTOK_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN")

def fetch_tiktok_trends(keyword, region="US"):
    url = "https://open.tiktokapis.com/v2/research/hashtag/search/"

    headers = {
        "Authorization": f"Bearer {TIKTOK_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "query": keyword,
        "region_code": region,
        "max_count": 20,
    }

    r = requests.post(url, json=payload, headers=headers, timeout=10)
    return r.json()