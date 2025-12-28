def fetch_campaign_insights(
    access_token: str,
    campaign_id: str,
) -> dict:
    url = f"{GRAPH_BASE}/{campaign_id}/insights"

    params = {
        "fields": "impressions,clicks,spend,ctr,cpm",
        "access_token": access_token,
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(f"Insights fetch failed: {data}")

    return data