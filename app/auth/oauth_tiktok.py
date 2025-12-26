import os, requests
from fastapi.responses import RedirectResponse

TIKTOK_AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
TIKTOK_TOKEN_URL = "https://business-api.tiktok.com/open_api/v1.3/oauth2/access_token/"

def tiktok_login():
    url = (
        f"{TIKTOK_AUTH_URL}"
        f"?client_key={os.getenv('TIKTOK_APP_ID')}"
        f"&redirect_uri={os.getenv('TIKTOK_REDIRECT_URI')}"
        f"&response_type=code"
        f"&scope=ads_management"
    )
    return RedirectResponse(url)

def tiktok_callback(code: str):
    payload = {
        "client_id": os.getenv("TIKTOK_APP_ID"),
        "client_secret": os.getenv("TIKTOK_APP_SECRET"),
        "code": code,
        "grant_type": "authorization_code",
    }

    token = requests.post(TIKTOK_TOKEN_URL, json=payload).json()

    # STORE token["access_token"]
    return {"platform": "tiktok", "token_received": True}