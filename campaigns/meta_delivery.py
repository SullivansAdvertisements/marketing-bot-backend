def fetch_meta_delivery_estimate(
    access_token: str,
    ad_account_id: str,
    budget: float,
    countries: list[str],
    age_min: int,
    age_max: int,
):
    url = f"https://graph.facebook.com/v18.0/{ad_account_id}/delivery_estimate"

    payload = {
        "access_token": access_token,
        "optimization_goal": "LINK_CLICKS",
        "daily_budget": int(budget * 100),
        "targeting_spec": {
            "geo_locations": {"countries": countries},
            "age_min": age_min,
            "age_max": age_max,
            "publisher_platforms": ["facebook", "instagram"],
            "device_platforms": ["mobile", "desktop"],
        },
    }

    response = requests.post(url, json=payload).json()

    if "data" not in response:
        return None, response.get("error", "Meta API error")

    est = response["data"][0]

    return {
        "Daily Budget ($)": budget,
        "Estimated Reach": est.get("users"),
        "Estimated Impressions": est.get("impressions"),
        "Platform": "Facebook / Instagram",
    }, None