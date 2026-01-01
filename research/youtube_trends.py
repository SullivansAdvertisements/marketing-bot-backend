from googleapiclient.discovery import build
import os

YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")

def fetch_youtube_trends(keyword, max_results=25):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_KEY)

    request = youtube.search().list(
        q=keyword,
        part="snippet",
        type="video",
        order="viewCount",
        maxResults=max_results,
    )
    response = request.execute()

    results = []
    for item in response["items"]:
        results.append({
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "published_at": item["snippet"]["publishedAt"],
        })

    return results