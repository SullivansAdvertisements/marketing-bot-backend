import streamlit as st
import os

from oauth_meta import (
    exchange_code_for_token,
    fetch_ad_accounts,
    create_meta_campaign,
)

# ============================
# META OAUTH CONFIG (PUT HERE)
# ============================
META_APP_ID = os.getenv("META_APP_ID")
REDIRECT_URI = "https://sullys-beginning-v1.streamlit.app/"

META_AUTH_URL = (
    "https://www.facebook.com/v19.0/dialog/oauth"
    f"?client_id={META_APP_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    "&scope=ads_read,ads_management,business_management"
)

# ----------------------------
# UI
# ----------------------------
st.title("Marketing Bot")

# ----------------------------
# OAuth Query Params
# ----------------------------
query = st.experimental_get_query_params()

# ----------------------------
# Connect Meta Ads
# ----------------------------

# ----------------------------
# Handle OAuth Callback
# ----------------------------
if "code" in query:
    try:
        token = exchange_code_for_token(query["code"][0])
        st.session_state["meta_access_token"] = token["access_token"]
        st.success("Meta connected successfully 🎉")
    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)

# ----------------------------
# Fetch Ad Accounts
# ----------------------------
if "meta_access_token" in st.session_state:
    accounts = fetch_ad_accounts(st.session_state["meta_access_token"])

    if accounts and "data" in accounts:
        for acct in accounts["data"]:
            acct_name = acct.get("name", "Unnamed Ad Account")
            st.success(f"{acct_name} ({acct['id']})")
    else:
        st.warning("No ad accounts found.")