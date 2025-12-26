import os
import urllib.parse
import requests

META_AUTH_URL = "https://www.facebook.com/v19.0/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"


def meta_login_url():
    params = {
        "client_id": META_APP_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "ads_management,ads_read",
        "response_type": "code",
    }
    return f"https://www.facebook.com/v19.0/dialog/oauth?{urlencode(params)}"


def exchange_code_for_token(code):
    data = {
        "client_id": META_APP_ID,
        "client_secret": META_APP_SECRET,
        "redirect_uri": REDIRECT_URI,  # MUST MATCH
        "code": code,
    }

    r = requests.get("https://graph.facebook.com/v19.0/oauth/access_token", params=data)
    return r.json()
    try:
        data = r.json()
    except Exception:
        raise Exception(f"Non-JSON response from Meta: {r.text}")

    if r.status_code != 200:
        raise Exception(f"Meta OAuth error: {data}")

    return data