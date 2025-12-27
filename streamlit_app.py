import streamlit as st

st.set_page_config(
    page_title="Marketing Bot",
    layout="wide"
)

from oauth_meta import (
    exchange_code_for_token,
    fetch_ad_accounts,
    create_meta_campaign,
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
st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")

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