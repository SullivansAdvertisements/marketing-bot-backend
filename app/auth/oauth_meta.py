import os
import urllib.parse
import requests

META_AUTH_URL = "https://www.facebook.com/v19.0/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"

def meta_login_url():
    redirect_uri = os.getenv("META_REDIRECT_URI")

    params = {
        "client_id": os.getenv("META_APP_ID"),
        "redirect_uri": redirect_uri,
        "scope": "ads_read,ads_management",
        "response_type": "code",
    }

    return f"{META_AUTH_URL}?{urllib.parse.urlencode(params)}"


def exchange_code_for_token(code: str):
    redirect_uri = os.getenv("META_REDIRECT_URI")

    payload = {
        "client_id": os.getenv("META_APP_ID"),
        "client_secret": os.getenv("META_APP_SECRET"),
        "redirect_uri": redirect_uri,
        "code": code,
    }

    r = requests.get(META_TOKEN_URL, params=payload, timeout=10)
    r.raise_for_status()
    return r.json()