import os
import requests
from urllib.parse import urlencode

META_CLIENT_ID = os.getenv("META_CLIENT_ID")
META_CLIENT_SECRET = os.getenv("META_CLIENT_SECRET")
META_REDIRECT_URI = os.getenv("META_REDIRECT_URI")

META_AUTH_URL = "https://www.facebook.com/v18.0/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
META_ACCOUNTS_URL = "https://graph.facebook.com/v18.0/me/adaccounts"

SCOPES = [
    "ads_read",
    "ads_management",
    "business_management",
]

def meta_login_url():
    params = {
        "client_id": META_CLIENT_ID,
        "redirect_uri": META_REDIRECT_URI,
        "scope": ",".join(SCOPES),
        "response_type": "code",
        "state": "meta",
    }
    return f"{META_AUTH_URL}?{urlencode(params)}"


def exchange_code_for_token(code: str) -> dict:
    params = {
        "client_id": META_CLIENT_ID,
        "client_secret": META_CLIENT_SECRET,
        "redirect_uri": META_REDIRECT_URI,
        "code": code,
    }

    r = requests.get(META_TOKEN_URL, params=params, timeout=10)
    data = r.json()

    if "access_token" not in data:
        raise Exception(data)

    return data["access_token"]


def fetch_ad_accounts(access_token: str) -> dict:
    params = {
        "access_token": access_token,
        "fields": "id,name",
    }
    r = requests.get(META_ACCOUNTS_URL, params=params, timeout=10)
    return r.json()