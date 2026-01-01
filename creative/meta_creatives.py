def create_meta_ad_creative(
    access_token: str,
    ad_account_id: str,
    page_id: str,
    headline: str,
    primary_text: str,
    destination_url: str,
) -> dict:
    account_id = ad_account_id.replace("act_", "")
    url = f"{GRAPH_BASE}/act_{account_id}/adcreatives"

    payload = {
        "name": "Streamlit Creative",
        "object_story_spec": {
            "page_id": page_id,
            "link_data": {
                "message": primary_text,
                "link": destination_url,
                "name": headline,
            },
        },
        "access_token": access_token,
    }

    r = requests.post(url, json=payload, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(f"Creative creation failed: {data}")

    return data
