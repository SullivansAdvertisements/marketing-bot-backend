def create_meta_adset(
    access_token: str,
    ad_account_id: str,
    campaign_id: str,
    name: str,
    daily_budget: int,
    start_time: str,
    end_time: str,
    geo_countries: list,
    age_min: int,
    age_max: int,
) -> dict:
    account_id = ad_account_id.replace("act_", "")
    url = f"{GRAPH_BASE}/act_{account_id}/adsets"

    payload = {
        "name": name,
        "campaign_id": campaign_id,
        "daily_budget": daily_budget,
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "LINK_CLICKS",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "targeting": {
            "geo_locations": {"countries": geo_countries},
            "age_min": age_min,
            "age_max": age_max,
        },
        "start_time": start_time,
        "end_time": end_time,
        "status": "PAUSED",
        "access_token": access_token,
    }

    r = requests.post(url, data=payload, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(f"Ad set creation failed: {data}")

    return data
