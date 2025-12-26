import os
import requests

META_TOKEN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"

def exchange_code_for_token(code: str):
    redirect_uri = os.getenv("META_REDIRECT_URI")

    payload = {
        "client_id": os.getenv("META_APP_ID"),
        "client_secret": os.getenv("META_APP_SECRET"),
        "redirect_uri": redirect_uri,
        "code": code,
    }

    r = requests.get(META_TOKEN_URL, params=payload, timeout=10)

    # DO NOT raise yet — inspect response first
    try:
        data = r.json()
    except Exception:
        raise Exception(f"Non-JSON response from Meta: {r.text}")

    # If Meta returned an error, surface it clearly
    if r.status_code != 200:
        raise Exception(f"Meta OAuth error: {data}")

    return data