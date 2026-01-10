"""
research_data/normalizers.py

Normalizes raw API responses into strict contracts.
"""

# ---------------------------
# GOOGLE KEYWORDS
# ---------------------------

def normalize_google_keyword(row: dict) -> dict:
    return {
        "keyword": row["keyword"],
        "avg_monthly_searches": int(row["avg_monthly_searches"]),
        "competition": row["competition"],
        "competition_index": int(row.get("competition_index", 0)),
        "top_of_page_cpc_low": float(row.get("top_of_page_cpc_low", 0.0)),
        "top_of_page_cpc_high": float(row.get("top_of_page_cpc_high", 0.0)),
        "source": "google_ads"
    }


# ---------------------------
# GOOGLE TRENDS
# ---------------------------

def normalize_google_trend(term: str, interest: int, timeframe: str) -> dict:
    return {
        "term": term,
        "interest_score": int(interest),
        "timeframe": timeframe,
        "platform": "google",
        "source": "google_trends"
    }


# ---------------------------
# YOUTUBE TRENDS
# ---------------------------

def normalize_youtube_trend(item: dict) -> dict:
    return {
        "title": item["title"],
        "channel": item["channel"],
        "published_at": item["published_at"],
        "platform": "youtube",
        "source": "youtube_api"
    }


# ---------------------------
# TIKTOK TRENDS
# ---------------------------

def normalize_tiktok_trend(item: dict) -> dict:
    return {
        "title": item["title"],
        "channel": item.get("author", "unknown"),
        "published_at": item.get("created_at", ""),
        "platform": "tiktok",
        "source": "tiktok_api"
    }


# ---------------------------
# META AD LIBRARY
# ---------------------------

def normalize_meta_ad(ad: dict) -> dict:
    return {
        "platform": ad.get("platform", "facebook"),
        "page_name": ad.get("page_name"),
        "ad_creative": ad.get("creative_text", ""),
        "ad_copy": ad.get("ad_copy", ""),
        "cta": ad.get("cta", ""),
        "active": bool(ad.get("is_active", False)),
        "source": "meta_ad_library"
    }
    
# -------------------------
# LOCATION DATA
# -------------------------

def normalize_location(
    platform: str,
    location: str,
    metric: str,
    value,
    source: str
) -> dict:
    return {
        "platform": platform,
        "location": location,
        "metric": metric,
        "value": value,
        "source": source,
    }