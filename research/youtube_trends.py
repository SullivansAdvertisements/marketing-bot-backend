import os
import pandas as pd
from googleapiclient.discovery import build


YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def fetch_youtube_trends(keyword: str):
    if not keyword or not YOUTUBE_API_KEY:
        return pd.DataFrame()

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    request = youtube.search().list(
        q=keyword,
        part="snippet",
        type="video",
        maxResults=10,
        order="viewCount",
    )

    response = request.execute()

    rows = []
    for item in response.get("items", []):
        snippet = item["snippet"]
        rows.append({
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "published_at": snippet["publishedAt"],
        })

    return pd.DataFrame(rows)