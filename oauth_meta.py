import os
import requests
from urllib.parse import urlencode

META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")
META_REDIRECT_URI = os.getenv("META_REDIRECT_URI")

META_AUTH_URL = "https://www.facebook.com/v18.0/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"

SCOPES = [
    "ads_read",
    "ads_management",
    "business_management",
]

def meta_login_url():
    if not META_APP_ID or not META_REDIRECT_URI:
        raise Exception("Meta OAuth not configured")

    params = {
        "client_id": META_APP_ID,          # ✅ Meta App ID
        "redirect_uri": META_REDIRECT_URI,
        "scope": ",".join(SCOPES),
        "response_type": "code",
    }

    return f"{META_AUTH_URL}?{urlencode(params)}"


def exchange_code_for_token(code: str) -> dict:
    params = {
        "client_id": META_APP_ID,          # ✅ App ID
        "client_secret": META_APP_SECRET,  # ✅ App Secret
        "redirect_uri": META_REDIRECT_URI,
        "code": code,
    }

    r = requests.get(META_TOKEN_URL, params=params, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(data)

    return data


def fetch_ad_accounts(access_token: str) -> dict:
    url = "https://graph.facebook.com/v18.0/me/adaccounts"
    params = {"access_token": access_token}
    return requests.get(url, params=params, timeout=10).json()