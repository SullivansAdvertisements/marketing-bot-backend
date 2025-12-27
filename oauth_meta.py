import os
import requests
from urllib.parse import urlencode

META_AUTH_URL = "https://www.facebook.com/v19.0/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"


def meta_login_url():
    return (
        "https://www.facebook.com/v19.0/dialog/oauth"
        "?client_id=" + META_APP_ID +
        "&redirect_uri=" + META_REDIRECT_URI +
        "&scope=ads_read,ads_management"
        "&response_type=code"
    )

    if not meta_app_id or not redirect_uri:
        # Do NOT crash at import time
        return "#"

    params = {
        "client_id": meta_app_id,
        "redirect_uri": redirect_uri,
        "scope": "ads_read,ads_management",
        "response_type": "code",
    }

    return f"{META_AUTH_URL}?{urlencode(params)}"


def exchange_code_for_token(code):
    payload = {
        "client_id": META_APP_ID,
        "client_secret": META_APP_SECRET,
        "redirect_uri": META_REDIRECT_URI,
        "code": code,
    }
    if not meta_app_id or not meta_app_secret or not redirect_uri:
        raise Exception("Meta OAuth env vars missing")

    payload = {
        "client_id": meta_app_id,
        "client_secret": meta_app_secret,
        "redirect_uri": redirect_uri,
        "code": code,
    }

    r = requests.get(META_TOKEN_URL, params=payload, timeout=10)

    try:
        data = r.json()
    except Exception:
        raise Exception(f"Non-JSON response from Meta: {r.text}")

    if r.status_code != 200:
        raise Exception(f"Meta OAuth error: {data}")

    return data
def fetch_ad_accounts(access_token: str):
    url = "https://graph.facebook.com/v19.0/me/adaccounts"
    params = {
        "access_token": access_token,
        "fields": "id,name,account_status,currency,timezone_name"
    }

    r = requests.get(url, params=params)
    data = r.json()

    if r.status_code != 200:
        raise Exception(f"Failed to fetch ad accounts: {data}")

    return data["data"]