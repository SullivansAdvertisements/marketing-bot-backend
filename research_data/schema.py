"""
research_data/schema.py

Canonical schema definitions for all research data.
"""

KEYWORD_SCHEMA = {
    "keyword": str,
    "avg_monthly_searches": int,
    "competition": str,
    "competition_index": int,
    "top_of_page_cpc_low": float,
    "top_of_page_cpc_high": float,
    "source": str,
}

SEARCH_TREND_SCHEMA = {
    "term": str,
    "interest_score": int,
    "timeframe": str,
    "platform": str,
    "source": str,
}

CONTENT_TREND_SCHEMA = {
    "title": str,
    "channel": str,
    "published_at": str,
    "platform": str,
    "source": str,
}

AD_LIBRARY_SCHEMA = {
    "platform": str,
    "page_name": str,
    "ad_creative": str,
    "ad_copy": str,
    "cta": str,
    "active": bool,
    "source": str,
}

AUDIENCE_SCHEMA = {
    "platform": str,
    "age_ranges": list,
    "genders": list,
    "locations": list,
    "interests": list,
    "source": str,
}

RESEARCH_SCHEMA = {
    "niche": str,
    "platforms": list,
    "keywords": list,
    "search_trends": list,
    "content_trends": list,
    "ad_intel": list,
    "audiences": dict,
    "funnels": dict,
    "angles": dict,
    "budget_guidance": dict,
    "sources": dict,
}