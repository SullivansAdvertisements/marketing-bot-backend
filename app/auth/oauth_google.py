import os
import requests
from urllib.parse import urlencode

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# MUST MATCH Streamlit app URL EXACTLY
GOOGLE_REDIRECT_URI = "https://sullys-beginning-v1.streamlit.app/"

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise Exception("Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET")


def google_login_url() -> str:
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "select_account",
    }

    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


def exchange_google_code(code: str) -> dict:
    payload = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
        "code": code,
    }

    token_res = requests.post(GOOGLE_TOKEN_URL, data=payload, timeout=10)
    token_data = token_res.json()

    if "access_token" not in token_data:
        raise Exception(f"Google OAuth failed: {token_data}")

    headers = {
        "Authorization": f"Bearer {token_data['access_token']}"
    }

    user_res = requests.get(
        GOOGLE_USERINFO_URL,
        headers=headers,
        timeout=10
    )

    user_data = user_res.json()

    return {
        "email": user_data.get("email"),
        "name": user_data.get("name"),
        "picture": user_data.get("picture"),
    }