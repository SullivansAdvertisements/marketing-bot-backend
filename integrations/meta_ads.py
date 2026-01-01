import os
import requests

BASE_URL = "https://graph.facebook.com/v19.0"

def build_meta_targeting(
    countries=["US"],
    age_min=18,
    age_max=44,
    genders=[1, 2],  # 1=male, 2=female
    interests=None,
    placements="automatic"
):
    targeting = {
        "geo_locations": {"countries": countries},
        "age_min": age_min,
        "age_max": age_max,
        "genders": genders
    }

    if interests:
        targeting["interests"] = [{"name": i} for i in interests]

    if placements == "automatic":
        targeting.update({
            "publisher_platforms": ["facebook", "instagram", "audience_network"],
            "facebook_positions": ["feed", "story", "reels"],
            "instagram_positions": ["stream", "story", "reels"]
        })

    return targeting


def fetch_meta_audience_insights(targeting):
    """
    REAL Meta audience insights via delivery estimates.
    """
    token = os.getenv("META_ACCESS_TOKEN")
    ad_account = os.getenv("META_AD_ACCOUNT_ID")

    url = f"{BASE_URL}/act_{ad_account}/delivery_estimate"

    payload = {
        "optimization_goal": "REACH",
        "targeting_spec": targeting,
        "access_token": token
    }

    r = requests.post(url, json=payload)
    r.raise_for_status()

    data = r.json()

    # Normalize into usable "insights"
    return {
        "audience_size_lower": data.get("estimate_dau_lower_bound"),
        "audience_size_upper": data.get("estimate_dau_upper_bound"),
        "daily_impressions_lower": data.get("estimate_impressions_lower_bound"),
        "daily_impressions_upper": data.get("estimate_impressions_upper_bound"),
        "placement_coverage": targeting.get("publisher_platforms"),
        "geo": targeting["geo_locations"],
        "age_range": f'{targeting["age_min"]}-{targeting["age_max"]}',
        "genders": targeting["genders"],
        "interests": [i["name"] for i in targeting.get("interests", [])],
        "source": "meta_delivery_estimate_api"
    }