import os
import requests

print("oauth_meta.py loaded")

META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")

REDIRECT_URI = "https://sullys-beginning-v1.streamlit.app/"

def exchange_code_for_token(code: str) -> str:
    if not META_APP_ID or not META_APP_SECRET:
        raise Exception("META_APP_ID or META_APP_SECRET not set")

    params = {
        "client_id": META_APP_ID,
        "client_secret": META_APP_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }

    r = requests.get(
        "https://graph.facebook.com/v19.0/oauth/access_token",
        params=params,
        timeout=10,
    )

    data = r.json()
    print("META TOKEN RESPONSE:", data)

    if "access_token" not in data:
        raise Exception(f"Meta OAuth error: {data}")

    return data["access_token"]


def fetch_ad_accounts(access_token: str) -> dict:
    url = "https://graph.facebook.com/v19.0/me/adaccounts"
    params = {
        "access_token": access_token,
        "fields": "id,name,account_status,currency",
        "limit": 50,
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if r.status_code != 200:
        raise Exception(f"Failed to fetch ad accounts: {data}")

    return data


def create_meta_campaign(
    access_token: str,
    ad_account_id: str,
    name: str,
    objective: str,
    daily_budget: int,
) -> dict:

    clean_id = ad_account_id.replace("act_", "")
    url = f"https://graph.facebook.com/v19.0/act_{clean_id}/campaigns"

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

    if r.status_code != 200:
        raise Exception(f"Campaign creation failed: {data}")

    return data