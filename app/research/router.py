from .google_trends import get_google_trends
from .google_keywords import get_google_keywords
from .youtube_trends import get_youtube_trends
from .tiktok_trends import get_tiktok_trends
from .meta_ad_library import get_meta_ads

def run_research(
    platform: str,
    keyword: str,
    geo: str = "US",
    timeframe: str = "today 12-m",
    access_token: str | None = None,
):
    if platform == "google_trends":
        return get_google_trends(keyword, geo, timeframe)

    if platform == "google_keywords":
        return get_google_keywords(keyword)

    if platform == "youtube":
        return get_youtube_trends(keyword)

    if platform == "tiktok":
        return get_tiktok_trends(keyword)

    if platform == "meta_ads":
        return get_meta_ads(keyword, geo)

    raise ValueError("Unsupported research platform")