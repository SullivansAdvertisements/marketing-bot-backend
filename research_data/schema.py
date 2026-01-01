KEYWORD_SCHEMA = {
    "keyword": str,
    "avg_monthly_searches": int,
    "competition": str,          # LOW / MEDIUM / HIGH
    "competition_index": int,    # 0–100
    "top_of_page_cpc_low": float,
    "top_of_page_cpc_high": float,
    "source": str                # google_ads
}

AUDIENCE_SCHEMA = {
    "age_ranges": list,
    "genders": list,
    "locations": list,
    "interests": list,
    "platform": str,
    "source": str
}