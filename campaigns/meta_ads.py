def create_meta_campaign(
    access_token: str,
    ad_account_id: str,
    name: str,
    objective: str,
    daily_budget: int,
) -> dict:
    account_id = ad_account_id.replace("act_", "")
    url = f"{GRAPH_BASE}/act_{account_id}/campaigns"

    payload = {
        "name": name,
        "objective": objective,
        "status": "PAUSED",
        "daily_budget": daily_budget,
        "special_ad_categories": [],
        "access_token": access_token,
    }

    r = requests.post(url, data=payload, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(f"Campaign creation failed: {data}")

    return data
