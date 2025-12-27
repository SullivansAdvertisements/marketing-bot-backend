import os
import requests
from urllib.parse import urlencode

META_AUTH_URL = "https://www.facebook.com/v19.0/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"


def get_meta_config():
    meta_app_id = os.getenv("META_APP_ID")
    meta_app_secret = os.getenv("META_APP_SECRET")
    redirect_uri = os.getenv("META_REDIRECT_URI")

    if not meta_app_id or not meta_app_secret or not redirect_uri:
        raise Exception(
            "Missing Meta OAuth environment variables. "
            "Check META_APP_ID, META_APP_SECRET, META_REDIRECT_URI"
        )

    return meta_app_id, meta_app_secret, redirect_uri


def meta_login_url():
    meta_app_id, _, redirect_uri = get_meta_config()

    params = {
        "client_id": meta_app_id,
        "redirect_uri": redirect_uri,
        "scope": "ads_read,ads_management",
        "response_type": "code",
    }

    return f"{META_AUTH_URL}?{urlencode(params)}"


def exchange_code_for_token(code: str):
    meta_app_id, meta_app_secret, redirect_uri = get_meta_config()

    payload = {
        "client_id": meta_app_id,
        "client_secret": meta_app_secret,
        "redirect_uri": redirect_uri,
        "code": code,
    }

    r = requests.get(META_TOKEN_URL, params=payload, timeout=10)
    data = r.json()

    if r.status_code != 200:
        raise Exception(f"Meta OAuth error: {data}")

    return data
    
    
def fetch_ad_accounts(access_token: