import os
from urllib.parse import urlencode
import requests

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

GOOGLE_AUTH_BASE = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

def google_login_url():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"{GOOGLE_AUTH_BASE}?{urlencode(params)}"


def exchange_google_code(code: str) -> dict:
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    r = requests.post(GOOGLE_TOKEN_URL, data=data, timeout=10)
    token_data = r.json()

    if "access_token" not in token_data:
        raise Exception(token_data)

    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    user = requests.get(GOOGLE_USERINFO_URL, headers=headers).json()

    return {
        "email": user.get("email"),
        "name": user.get("name"),
        "picture": user.get("picture"),
    }