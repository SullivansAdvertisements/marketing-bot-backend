import os

def fetch_youtube_trends(keyword, max_results=25):
    try:
        from googleapiclient.discovery import build
    except ImportError:
        raise RuntimeError(
            "google-api-python-client is not installed. "
            "Add it to requirements.txt to enable YouTube Trends."
        )

    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("YOUTUBE_API_KEY is missing")

    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        q=keyword,
        part="snippet",
        type="video",
        order="viewCount",
        maxResults=max_results,
    )

    response = request.execute()

    results = []
    for item in response.get("items", []):
        snippet = item["snippet"]
        results.append({
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "published_at": snippet["publishedAt"],
        })

    return results
    
    results.append({
    "title": snippet["title"],
    "channel": snippet["channelTitle"],
    "published_at": snippet["publishedAt"],
    "location": snippet.get("country", "unknown"),
})