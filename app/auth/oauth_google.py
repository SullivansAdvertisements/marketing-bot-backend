import os, requests
from fastapi.responses import RedirectResponse

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

def google_login():
    url = (
        f"{GOOGLE_AUTH_URL}"
        f"?client_id={os.getenv('GOOGLE_CLIENT_ID')}"
        f"&redirect_uri={os.getenv('GOOGLE_REDIRECT_URI')}"
        f"&response_type=code"
        f"&scope=https://www.googleapis.com/auth/adwords "
        f"https://www.googleapis.com/auth/youtube.readonly"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return RedirectResponse(url)

def google_callback(code: str):
    data = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "code": code,
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
        "grant_type": "authorization_code",
    }

    token = requests.post(GOOGLE_TOKEN_URL, data=data).json()

    # STORE token["refresh_token"] + access_token
    return {"platform": "google", "token_received": True}