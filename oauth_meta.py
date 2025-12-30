import os
import requests
from urllib.parse import urlencode

# =================================================
# ENV VARS (STREAMLIT SECRETS)
# =================================================
META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")
META_REDIRECT_URI = os.getenv(
    "META_REDIRECT_URI",
    "https://sullys-beginning-v1.streamlit.app/",
)

GRAPH_BASE = "https://graph.facebook.com/v18.0"

# =================================================
# LOGIN URL
# =================================================
def meta_login_url():
    params = {
        "client_id": META_APP_ID,
        "redirect_uri": META_REDIRECT_URI,
        "state": "meta",
        "response_type": "code",
        "scope": "ads_read,ads_management",
    }
    return f"https://www.facebook.com/v18.0/dialog/oauth?{urlencode(params)}"

# =================================================
# TOKEN EXCHANGE
# =================================================
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

# =================================================
# FETCH AD ACCOUNTS
# =================================================
def fetch_ad_accounts(access_token: str) -> dict:
    url = f"{GRAPH_BASE}/me/adaccounts"
    params = {
        "access_token": access_token,
        "fields": "id,name",
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(data)

    return data