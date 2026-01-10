"""
research_data/contracts.py

Strict schema enforced across all research sources.
NO mock data. NO synthetic fields.
"""

KEYWORD_CONTRACT = {
    "keyword": str,
    "avg_monthly_searches": int,
    "competition": str,              # LOW / MEDIUM / HIGH
    "competition_index": int,         # 0–100
    "top_of_page_cpc_low": float,
    "top_of_page_cpc_high": float,
    "source": str                     # google_ads
}

SEARCH_TREND_CONTRACT = {
    "term": str,
    "interest_score": int,            # 0–100
    "timeframe": str,
    "platform": str,                  # google
    "source": str                     # google_trends
}

CONTENT_TREND_CONTRACT = {
    "title": str,
    "channel": str,
    "published_at": str,
    "platform": str,                  # youtube / tiktok
    "source": str                     # youtube_api / tiktok_api
}

AD_LIBRARY_CONTRACT = {
    "platform": str,                  # facebook / instagram
    "page_name": str,
    "ad_creative": str,
    "ad_copy": str,
    "cta": str,
    "active": bool,
    "source": str                     # meta_ad_library
}

AUDIENCE_CONTRACT = {
    "platform": str,
    "age_ranges": list,
    "genders": list,
    "locations": list,
    "interests": list,
    "source": str
}

RESEARCH_DATA_CONTRACT = {
    "niche": str,
    "platforms": list,
    "keywords": list,                 # KEYWORD_CONTRACT
    "search_trends": list,            # SEARCH_TREND_CONTRACT
    "content_trends": list,           # CONTENT_TREND_CONTRACT
    "ad_intel": list,                 # AD_LIBRARY_CONTRACT
    "audiences": dict,                # platform → AUDIENCE_CONTRACT
    "funnels": dict,
    "angles": dict,
    "budget_guidance": dict,
    "sources": dict                   # platform → api name
}
LOCATION_CONTRACT = {
    "platform": str,
    "location": str,          # country or region code/name
    "metric": str,            # searches / interest / ads / videos
    "value": int | float,
    "source": str,
}