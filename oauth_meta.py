import os
import requests

META_APP_ID = os.environ.get("META_APP_ID")
META_APP_SECRET = os.environ.get("META_APP_SECRET")
META_REDIRECT_URI = os.environ.get("META_REDIRECT_URI")


def meta_login_url():
    return (
        "https://www.facebook.com/v19.0/dialog/oauth"
        f"?client_id={META_APP_ID}"
        f"&redirect_uri={META_REDIRECT_URI}"
        "&scope=ads_read,ads_management,business_management"
    )


def exchange_code_for_token(code):
    url = "https://graph.facebook.com/v19.0/oauth/access_token"
    params = {
        "client_id": META_APP_ID,
        "client_secret": META_APP_SECRET,
        "redirect_uri": META_REDIRECT_URI,
        "code": code,
    }

    r = requests.get(url, params=params)
    data = r.json()

    if "error" in data:
        raise Exception(f"Meta OAuth error: {data}")

    return data


def fetch_ad_accounts(access_token):
    url = "https://graph.facebook.com/v19.0/me/adaccounts"
    params = {"access_token": access_token}
    r = requests.get(url, params=params)
    return r.json()