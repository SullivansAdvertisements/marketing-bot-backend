# oauth_google.py
import os
import requests
from urllib.parse import urlencode

# ============================================================
# GOOGLE OAUTH CONSTANTS (REQUIRED)
# ============================================================

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# REQUIRED SCOPES FOR ADS + RESEARCH
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/adwords",
    "https://www.googleapis.com/auth/analytics.readonly",
]

# ============================================================
# BUILD LOGIN URL (STATE SAFE)
# ============================================================

def google_login_url(state="google"):
    """
    Returns Google OAuth login URL.
    Accepts `state` so Streamlit can distinguish platform callbacks.
    """

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(GOOGLE_SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }

    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

# ============================================================
# EXCHANGE AUTH CODE FOR TOKEN
# ============================================================

def exchange_google_code_for_token(code):
    """
    Exchanges Google OAuth code for access + refresh token.
    """

    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_REDIRECT_URI,
    }

    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    token_data = response.json()

    if "error" in token_data:
        raise Exception(token_data)

    return token_data