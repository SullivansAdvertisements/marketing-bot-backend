import os
import requests

# ============================================================
# Meta App Credentials
# ============================================================
META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")

if not META_APP_ID or not META_APP_SECRET:
    print("⚠️ META_APP_ID or META_APP_SECRET not set yet")
# ============================================================
# OAuth Redirect URI (MUST MATCH META DASHBOARD EXACTLY)
# ============================================================
REDIRECT_URI = "https://sullys-beginning-v1.streamlit.app/"

# ============================================================
# OAuth: Exchange Authorization Code for Access Token
# ============================================================
def exchange_code_for_token(code: str) -> str:
    """
    Exchanges Meta OAuth authorization code for an access token
    """

    params = {
        "client_id": META_APP_ID,
        "client_secret": META_APP_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }

    r = requests.get(
        "https://graph.facebook.com/v19.0/oauth/access_token",
        params=params,
        timeout=10,
    )

    data = r.json()
    print("META TOKEN RESPONSE:", data)  # 🔍 keep until confirmed working

    if "access_token" not in data:
        raise Exception(f"Meta OAuth error: {data}")

    return data["access_token"]

# ============================================================
# Fetch Ad Accounts
# ============================================================
def fetch_ad_accounts(access_token: str) -> dict:
    """
    Returns ad accounts available to the authenticated user
    """

    url = "https://graph.facebook.com/v19.0/me/adaccounts"
    params = {
        "access_token": access_token,
        "fields": "id,name,account_status,currency",
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if r.status_code != 200:
        raise Exception(f"Failed to fetch ad accounts: {data}")

    return data

# ============================================================
# Create Meta Campaign (Paused by Default)
# ============================================================
def create_meta_campaign(
    access_token: str,
    ad_account_id: str,
    name: str,
    objective: str,
    daily_budget: int,
) -> dict:
    """
    daily_budget is in CENTS (e.g. $10 = 1000)
    """

  clean_id = ad_account_id.replace("act_", "")
url = f"https://graph.facebook.com/v19.0/act_{clean_id}/campaigns"

    payload = {
        "name": name,
        "objective": objective,
        "status": "PAUSED",  # always create paused
        "daily_budget": daily_budget,
        "special_ad_categories": [],
        "access_token": access_token,
    }

    r = requests.post(url, data=payload, timeout=10)
    data = r.json()

    if r.status_code != 200:
        raise Exception(f"Campaign creation failed: {data}")

    return data