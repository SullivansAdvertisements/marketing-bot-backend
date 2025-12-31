import os
import requests

META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")
META_REDIRECT_URI = os.getenv("META_REDIRECT_URI")

def meta_login_url():
    return (
        "https://www.facebook.com/v18.0/dialog/oauth"
        f"?client_id={META_APP_ID}"
        f"&redirect_uri={META_REDIRECT_URI}"
        f"&scope=ads_read,ads_management"
        f"&state=meta"
    )

def exchange_meta_code_for_token(code: str) -> str:
    r = requests.get(
        "https://graph.facebook.com/v18.0/oauth/access_token",
        params={
            "client_id": META_APP_ID,
            "client_secret": META_APP_SECRET,
            "redirect_uri": META_REDIRECT_URI,
            "code": code,
        },
        timeout=10,
    )
    data = r.json()
    if "access_token" not in data:
        raise Exception(data)
    return data["access_token"]

def fetch_ad_accounts(token: str):
    r = requests.get(
        "https://graph.facebook.com/v18.0/me/adaccounts",
        params={"access_token": token},
        timeout=10,
    )
    return r.json()