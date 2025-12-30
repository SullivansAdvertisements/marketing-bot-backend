import os
import requests
from urllib.parse import urlencode

# =================================================
# GOOGLE OAUTH CONFIG (STREAMLIT CLOUD)
# =================================================

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# 🚨 MUST MATCH GOOGLE CLOUD EXACTLY
GOOGLE_REDIRECT_URI = "https://sullys-beginning-v1.streamlit.app/"

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

# -------------------------------------------------
# Safety check
# -------------------------------------------------
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise Exception("Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET")

# =================================================
# 1️⃣ GOOGLE LOGIN URL
# =================================================
def google_login_url() -> str:
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join([
            "openid",
            "email",
            "profile",
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/adwords",
        ]),
        "access_type": "offline",
        "prompt": "consent",
    }

    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


# =================================================
# 2️⃣ EXCHANGE CODE → ACCESS TOKEN
# =================================================
def exchange_google_code_for_token(code: str) -> dict:
    payload = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_REDIRECT_URI,
    }

    r = requests.post(GOOGLE_TOKEN_URL, data=payload, timeout=10)
    token = r.json()

    # 🔴 Surface real Google errors
    if "error" in token:
        raise Exception(f"Google OAuth error: {token}")

    return token