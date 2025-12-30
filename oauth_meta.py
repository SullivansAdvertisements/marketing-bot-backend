import os
import requests
from urllib.parse import urlencode

META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")

META_REDIRECT_URI = "https://sullys-beginning-v1.streamlit.app/"
GRAPH_API_VERSION = "v19.0"
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

def meta_login_url() -> str:
    params = {
        "client_id": META_APP_ID,
        "redirect_uri": META_REDIRECT_URI,
        "response_type": "code",
        "scope": ",".join([
            "ads_management",
            "ads_read",
            "business_management",
            "public_profile",
        ]),
        "state": "meta",
    }
    return f"https://www.facebook.com/{GRAPH_API_VERSION}/dialog/oauth?{urlencode(params)}"


def exchange_code_for_token(code: str) -> str:
    url = f"{GRAPH_BASE}/oauth/access_token"
    params = {
        "client_id": META_APP_ID,
        "client_secret": META_APP_SECRET,
        "redirect_uri": META_REDIRECT_URI,
        "code": code,
    }
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    if "access_token" not in data:
        raise Exception(data)
    return data["access_token"]


def fetch_ad_accounts(access_token: str) -> dict:
    url = f"{GRAPH_BASE}/me/adaccounts"
    params = {
        "fields": "id,name,account_status,currency",
        "access_token": access_token,
    }
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    if "error" in data:
        raise Exception(data)
    return data