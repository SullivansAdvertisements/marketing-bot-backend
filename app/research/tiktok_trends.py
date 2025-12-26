import requests
import os

def fetch_tiktok_trends(country):
    url = "https://business-api.tiktok.com/open_api/v1.3/trending/hashtags/"
    headers = {"Access-Token": os.getenv("TIKTOK_ACCESS_TOKEN")}
    return requests.get(url, headers=headers).json()