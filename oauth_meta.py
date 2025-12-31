# oauth_meta.py
import os
import requests  # ✅ THIS WAS MISSING
from urllib.parse import urlencode

# ============================================================
# META OAUTH CONSTANTS
# ============================================================

META_AUTH_URL = "https://www.facebook.com/v18.0/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
META_ACCOUNTS_URL = "https://graph.facebook.com/v18.0/me/adaccounts"

META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")
META_REDIRECT_URI = os.getenv("META_REDIRECT_URI")

META_SCOPES = [
    "ads_read",
    "ads_management",
    "business_management",
]

# ============================================================
# LOGIN URL
# ============================================================

def meta_login_url(state="meta"):
    params = {
        "client_id": META_APP_ID,
        "redirect_uri": META_REDIRECT_URI,
        "response_type": "code",
        "scope": ",".join(META_SCOPES),
        "state": state,
    }
    return f"{META_AUTH_URL}?{urlencode(params)}"

# ============================================================
# EXCHANGE CODE FOR TOKEN
# ============================================================

def exchange_meta_code_for_token(code):
    params = {
        "client_id": META_APP_ID,
        "client_secret": META_APP_SECRET,
        "redirect_uri": META_REDIRECT_URI,
        "code": code,
    }

    r = requests.get(META_TOKEN_URL, params=params)
    data = r.json()

    if "error" in data:
        raise Exception(data)

    return data

# ============================================================
# FETCH AD ACCOUNTS (OPTIONAL BUT SAFE)
# ============================================================

def fetch_ad_accounts(access_token):
    r = requests.get(
        META_ACCOUNTS_URL,
        params={"access_token": access_token},
    )
    data = r.json()

    if "error" in data:
        raise Exception(data)

    return data.get("data", [])