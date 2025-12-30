import os
import requests
from urllib.parse import urlencode

# =================================================
# ENV (FROM STREAMLIT SECRETS)
# =================================================
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# 🚨 MUST MATCH GOOGLE CLOUD CONSOLE EXACTLY
GOOGLE_REDIRECT_URI = "https://sullys-beginning-v1.streamlit.app/"

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise Exception("Google OAuth env vars missing")

# =================================================
# CONSTANTS
# =================================================
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

# ✅ DEFINE SCOPES (THIS WAS YOUR ERROR)
SCOPES = [
    "openid",
    "email",
    "profile",
    "https://www.googleapis.com/auth/youtube.readonly",
]

# =================================================
# LOGIN URL
# =================================================
def google_login_url():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "state": "google",  # 👈 REQUIRED
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

# =================================================
# EXCHANGE CODE → TOKEN
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

    # 🔍 DEBUG VISIBILITY (CRITICAL)
    print("GOOGLE TOKEN RESPONSE:", token)

    if "error" in token:
        raise Exception(f"Google OAuth error: {token}")

    return token