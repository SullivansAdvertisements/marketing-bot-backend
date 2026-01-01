import os
import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_trends(keyword: str, max_results: int = 10):
    if not YOUTUBE_API_KEY:
        raise Exception("YOUTUBE_API_KEY missing")

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": keyword,
        "type": "video",
        "order": "viewCount",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
    }

    r = requests.get(url, params=params)
    data = r.json()

    return [
        {
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "published": item["snippet"]["publishedAt"],
        }
        for item in data.get("items", [])
    ]
