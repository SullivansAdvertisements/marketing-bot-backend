import os
import requests
from urllib.parse import urlencode

# =========================================================
# ENVIRONMENT VARIABLES (REQUIRED)
# =========================================================
META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")

# MUST MATCH META DASHBOARD *EXACTLY*
META_REDIRECT_URI = "https://sullys-beginning-v1.streamlit.app/"

GRAPH_API_VERSION = "v19.0"
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

if not META_APP_ID or not META_APP_SECRET:
    raise Exception("META_APP_ID or META_APP_SECRET is missing")

# =========================================================
# 1️⃣ META LOGIN URL
# =========================================================
def meta_login_url() -> str:
    params = {
        "client_id": META_APP_ID,
        "redirect_uri": META_REDIRECT_URI,
        "response_type": "code",
        "scope": ",".join([
            "ads_management",
            "ads_read",
            "business_management",
            "public_profile",
        ]),
    }

    return f"https://www.facebook.com/{GRAPH_API_VERSION}/dialog/oauth?{urlencode(params)}"


# =========================================================
# 2️⃣ EXCHANGE CODE → ACCESS TOKEN
# =========================================================
def exchange_code_for_token(code: str) -> str:
    url = f"{GRAPH_BASE}/oauth/access_token"

    params = {
        "client_id": META_APP_ID,
        "client_secret": META_APP_SECRET,
        "redirect_uri": META_REDIRECT_URI,
        "code": code,
    }
"state": "meta"
    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if "access_token" not in data:
        raise Exception(f"Meta OAuth error: {data}")

    return data["access_token"]


# =========================================================
# 3️⃣ FETCH AD ACCOUNTS
# =========================================================
def fetch_ad_accounts(access_token: str) -> dict:
    url = f"{GRAPH_BASE}/me/adaccounts"

    params = {
        "fields": "id,name,account_status,currency",
        "access_token": access_token,
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(f"Fetch ad accounts failed: {data}")

    return data


# =========================================================
# 4️⃣ CREATE META CAMPAIGN
# =========================================================
def create_meta_campaign(
    access_token: str,
    ad_account_id: str,
    name: str,
    objective: str,
    daily_budget: int,
) -> dict:
    account_id = ad_account_id.replace("act_", "")
    url = f"{GRAPH_BASE}/act_{account_id}/campaigns"

    payload = {
        "name": name,
        "objective": objective,
        "status": "PAUSED",
        "daily_budget": daily_budget,
        "special_ad_categories": [],
        "access_token": access_token,
    }

    r = requests.post(url, data=payload, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(f"Campaign creation failed: {data}")

    return data


# =========================================================
# 5️⃣ CREATE META AD SET
# =========================================================
def create_meta_adset(
    access_token: str,
    ad_account_id: str,
    campaign_id: str,
    name: str,
    daily_budget: int,
    start_time: str,
    end_time: str,
    geo_countries: list,
    age_min: int,
    age_max: int,
) -> dict:
    account_id = ad_account_id.replace("act_", "")
    url = f"{GRAPH_BASE}/act_{account_id}/adsets"

    payload = {
        "name": name,
        "campaign_id": campaign_id,
        "daily_budget": daily_budget,
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "LINK_CLICKS",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "targeting": {
            "geo_locations": {"countries": geo_countries},
            "age_min": age_min,
            "age_max": age_max,
        },
        "start_time": start_time,
        "end_time": end_time,
        "status": "PAUSED",
        "access_token": access_token,
    }

    r = requests.post(url, data=payload, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(f"Ad set creation failed: {data}")

    return data


# =========================================================
# 6️⃣ CREATE META AD CREATIVE (TEXT/LINK)
# =========================================================
def create_meta_ad_creative(
    access_token: str,
    ad_account_id: str,
    page_id: str,
    headline: str,
    primary_text: str,
    destination_url: str,
) -> dict:
    account_id = ad_account_id.replace("act_", "")
    url = f"{GRAPH_BASE}/act_{account_id}/adcreatives"

    payload = {
        "name": "Streamlit Creative",
        "object_story_spec": {
            "page_id": page_id,
            "link_data": {
                "message": primary_text,
                "link": destination_url,
                "name": headline,
            },
        },
        "access_token": access_token,
    }

    r = requests.post(url, json=payload, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(f"Creative creation failed: {data}")

    return data


# =========================================================
# 7️⃣ FETCH CAMPAIGN INSIGHTS
# =========================================================
def fetch_campaign_insights(
    access_token: str,
    campaign_id: str,
) -> dict:
    url = f"{GRAPH_BASE}/{campaign_id}/insights"

    params = {
        "fields": "impressions,clicks,spend,ctr,cpm",
        "access_token": access_token,
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(f"Insights fetch failed: {data}")

    return data