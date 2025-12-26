import os
import requests

META_AUTH_URL = "https://www.facebook.com/v19.0/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"
META_ACCOUNTS_URL = "https://graph.facebook.com/v19.0/me/adaccounts"


def meta_login_url():
    return (
        f"{META_AUTH_URL}"
        f"?client_id={os.getenv('META_APP_ID')}"
        f"&redirect_uri={os.getenv('META_REDIRECT_URI')}"
        f"&scope=ads_read,ads_management,business_management"
    )


def exchange_code_for_token(code: str):
    r = requests.get(
        META_TOKEN_URL,
        params={
            "client_id": os.getenv("META_APP_ID"),
            "client_secret": os.getenv("META_APP_SECRET"),
            "redirect_uri": os.getenv("META_REDIRECT_URI"),
            "code": code,
        },
    )
    return r.json()


def fetch_meta_ad_accounts(access_token: str):
    r = requests.get(
        META_ACCOUNTS_URL,
        params={"access_token": access_token}
    )
    return r.json().get("data", [])