import streamlit as st
import pandas as pd

# =================================================
# MUST BE FIRST — MOBILE FRIENDLY
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =================================================
# IMPORTS
# =================================================
from oauth_meta import (
    meta_login_url,
    exchange_code_for_token,
    fetch_ad_accounts,
)

from oauth_google import (
    google_login_url,
    exchange_google_code_for_token,
)

# =================================================
# APP TITLE
# =================================================
st.title("🚀 Marketing Bot")

# =================================================
# QUERY PARAMS
# =================================================
query = st.experimental_get_query_params()

# =================================================
# SESSION DEFAULTS (CRITICAL)
# =================================================
st.session_state.setdefault("meta_access_token", None)
st.session_state.setdefault("google_access_token", None)
st.session_state.setdefault("ad_account_id", None)

# =================================================
# STEP 1 — META AUTH (REQUIRED)
# =================================================
st.subheader("🔵 Step 1: Connect Meta Ads")
st.markdown(f"[Connect Meta Ads]({meta_login_url()})")

if "code" in query and not st.session_state["meta_access_token"]:
    try:
        token = exchange_code_for_token(query["code"][0])
        st.session_state["meta_access_token"] = token
        st.success("Meta connected successfully")
        st.experimental_rerun()
    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)

# =================================================
# STEP 2 — GOOGLE AUTH (OPTIONAL / NON-BLOCKING)
# =================================================
st.divider()
st.subheader("🟢 Step 2: Connect Google (Optional)")

try:
    google_url = google_login_url()
    st.markdown(f"[Sign in with Google]({google_url})")

    if (
        "code" in query
        and not st.session_state["google_access_token"]
        and query.get("state", [""])[0] == "google"
    ):
        try:
            token = exchange_google_code_for_token(query["code"][0])
            st.session_state["google_access_token"] = token["access_token"]
            st.success("Google connected successfully")
            st.experimental_rerun()
        except Exception as e:
            st.warning("Google connection failed (optional)")
            st.exception(e)

except Exception:
    st.info("Google OAuth not configured yet")

# =================================================
# 🚦 UNLOCK LOGIC (THIS FIXES YOUR ISSUE)
# =================================================
if not st.session_state["meta_access_token"]:
    st.info("Connect Meta Ads to unlock the app")
    st.stop()

# =================================================
# FETCH AD ACCOUNTS
# =================================================
accounts_response = fetch_ad_accounts(st.session_state["meta_access_token"])
accounts = accounts_response.get("data", [])

if not accounts:
    st.error("No Meta ad accounts found")
    st.stop()

account_df = pd.DataFrame(accounts)[["id", "name"]]
account_df["clean_id"] = account_df["id"].str.replace("act_", "")

selected_name = st.selectbox(
    "Active Meta Ad Account",
    account_df["name"],
)

selected_account_id = account_df.loc[
    account_df["name"] == selected_name, "clean_id"
].iloc[0]

st.session_state["ad_account_id"] = selected_account_id

st.success(f"Using Meta account: {selected_account_id}")

# =================================================
# MAIN TABS (NOW ALWAYS LOAD)
# =================================================
tab_research, tab_creative, tab_campaigns, tab_strategy, tab_system = st.tabs(
    ["🔍 Research", "🎨 Creative", "📣 Campaigns", "🧠 Strategy", "🧰 System"]
)

# =================================================
# RESEARCH TAB
# =================================================
with tab_research:
    st.subheader("Market Research")
    st.info("Research modules load here")

    st.write("Google Connected:", bool(st.session_state["google_access_token"]))
    st.write("Meta Connected:", True)

# =================================================
# CREATIVE TAB
# =================================================
with tab_creative:
    st.subheader("Creative Builder")
    st.info("Creative generation ready")

# =================================================
# CAMPAIGNS TAB
# =================================================
with tab_campaigns:
    st.subheader("Campaign Builder")
    st.info("Campaign creation hooks ready")

# =================================================
# STRATEGY TAB
# =================================================
with tab_strategy:
    st.subheader("Strategy & Budgeting")
    st.info("Strategy engine ready")

# =================================================
# SYSTEM TAB
# =================================================
with tab_system:
    st.subheader("System Status")
    st.json({
        "meta_connected": bool(st.session_state["meta_access_token"]),
        "google_connected": bool(st.session_state["google_access_token"]),
        "ad_account_id": st.session_state["ad_account_id"],
    })