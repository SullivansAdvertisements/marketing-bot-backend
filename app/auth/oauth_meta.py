import os, requests
from fastapi.responses import RedirectResponse

META_AUTH_URL = "https://www.facebook.com/v19.0/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"

def meta_login():
    url = (
        f"{META_AUTH_URL}"
        f"?client_id={os.getenv('META_APP_ID')}"
        f"&redirect_uri={os.getenv('META_REDIRECT_URI')}"
        f"&scope=ads_read,ads_management,business_management"
    )
    return RedirectResponse(url)

def meta_callback(code: str):
    params = {
        "client_id": os.getenv("META_APP_ID"),
        "client_secret": os.getenv("META_APP_SECRET"),
        "redirect_uri": os.getenv("META_REDIRECT_URI"),
        "code": code,
    }

    response = requests.get(META_TOKEN_URL, params=params).json()

    # STORE response["access_token"] SECURELY
    return {"platform": "meta", "token_received": True}