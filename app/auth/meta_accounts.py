def fetch_ad_accounts(access_token: str) -> dict:
    url = f"{GRAPH_BASE}/me/adaccounts"

    params = {
        "fields": "id,name,account_status,currency",
        "access_token": access_token,
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(f"Fetch ad accounts failed: {data}")

    return data