import os
from urllib.parse import urlencode

# ===== META OAUTH CONSTANTS (REQUIRED) =====
META_AUTH_URL = "https://www.facebook.com/v18.0/dialog/oauth"

META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")
META_REDIRECT_URI = os.getenv("META_REDIRECT_URI")

META_SCOPES = [
    "ads_read",
    "ads_management",
    "business_management",
]
def meta_login_url(state: str = "meta"):
    params = {
        "client_id": META_APP_ID,
        "redirect_uri": META_REDIRECT_URI,
        "scope": ",".join(META_SCOPES),
        "response_type": "code",
        "state": state,   # ✅ REQUIRED
    }
    return f"{META_AUTH_URL}?{urlencode(params)}"

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