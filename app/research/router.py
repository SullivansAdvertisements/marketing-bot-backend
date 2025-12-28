from .google_trends import get_google_trends
from .youtube_trends import get_youtube_trends
from .meta_ad_library import search_meta_ad_library

def run_research(
    platform: str,
    keyword: str,
    geo: str = "US",
    timeframe: str = "today 12-m",
    access_token: str = None,
):
    if platform == "google_trends":
        return get_google_trends(keyword, geo, timeframe)

    if platform == "youtube":
        return get_youtube_trends(region_code=geo)

    if platform == "meta_ads":
        return search_meta_ad_library(keyword, geo, access_token)

    raise ValueError("Unsupported research platform")
