import os
import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_trends(region_code="US", max_results=10):
    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if "items" not in data:
        return []

    return data["items"]