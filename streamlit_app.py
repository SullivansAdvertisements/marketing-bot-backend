import streamlit as st
import pandas as pd

# =================================================
# PAGE CONFIG (MUST BE FIRST)
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =================================================
# AUTH IMPORTS (ROOT FILES)
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
# QUERY PARAMS (SAFE)
# =================================================
query = dict(st.query_params)

# =================================================
# SESSION STATE DEFAULTS (CRITICAL)
# =================================================
st.session_state.setdefault("meta_access_token", None)
st.session_state.setdefault("google_access_token", None)
st.session_state.setdefault("ad_account_id", None)

# =================================================
# 🔵 META AUTH (OPTIONAL — NO GATING)
# =================================================
st.subheader("🔵 Meta Ads")

st.markdown(f"[Connect Meta Ads]({meta_login_url()})")

if (
    "code" in query
    and query.get("state") == "meta"
    and st.session_state["meta_access_token"] is None
):
    try:
        token = exchange_code_for_token(query["code"])
        st.session_state["meta_access_token"] = token
        st.query_params.clear()
        st.success("Meta connected successfully")
    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)

# =================================================
# 🟢 GOOGLE AUTH (OPTIONAL — NO GATING)
# =================================================
st.divider()
st.subheader("🟢 Google")

st.markdown(f"[Sign in with Google]({google_login_url()})")

if (
    "code" in query
    and query.get("state") == "google"
    and st.session_state["google_access_token"] is None
):
    try:
        token = exchange_google_code_for_token(query["code"])
        st.session_state["google_access_token"] = token["access_token"]
        st.query_params.clear()
        st.success("Google connected successfully")
    except Exception as e:
        st.warning("Google OAuth failed")
        st.exception(e)

# =================================================
# CONNECTION STATUS (NEVER BLOCKS UI)
# =================================================
st.divider()
st.subheader("🔐 Connection Status")

col1, col2 = st.columns(2)
col1.metric("Meta Connected", bool(st.session_state["meta_access_token"]))
col2.metric("Google Connected", bool(st.session_state["google_access_token"]))

# =================================================
# META AD ACCOUNTS (ONLY IF META CONNECTED)
# =================================================
if st.session_state["meta_access_token"]:
    try:
        accounts = fetch_ad_accounts(
            st.session_state["meta_access_token"]
        ).get("data", [])

        if accounts:
            df = pd.DataFrame(accounts)[["id", "name"]]
            df["clean_id"] = df["id"].str.replace("act_", "")

            selected = st.selectbox(
                "Meta Ad Account",
                df["name"]
            )

            st.session_state["ad_account_id"] = df.loc[
                df["name"] == selected, "clean_id"
            ].iloc[0]

            st.success(f"Using Meta account: {selected}")

    except Exception as e:
        st.warning("Could not load Meta ad accounts")
        st.exception(e)

# =================================================
# MAIN APP TABS (ALWAYS LOAD)
# =================================================
tab_research, tab_creative, tab_campaigns, tab_strategy, tab_system = st.tabs(
    ["🔍 Research", "🎨 Creative", "📣 Campaigns", "🧠 Strategy", "🧰 System"]
)

# =================================================
# RESEARCH TAB
# =================================================
with tab_research:
    st.header("🔍 Research")

    if st.session_state["google_access_token"]:
        st.success("Google connected — research enabled")
    else:
        st.info("Connect Google to unlock full research")

# =================================================
# CREATIVE TAB
# =================================================
with tab_creative:
    st.header("🎨 Creative")
    st.info("Creative tools ready")

# =================================================
# CAMPAIGNS TAB
# =================================================
with tab_campaigns:
    st.header("📣 Campaigns")

    if st.session_state["meta_access_token"]:
        st.success("Meta campaigns available")
    else:
        st.info("Connect Meta to create campaigns")

# =================================================
# STRATEGY TAB
# =================================================
with tab_strategy:
    st.header("🧠 Strategy")
    st.info("Strategy engine ready")

# =================================================
# SYSTEM TAB (DEBUG SAFE)
# =================================================
with tab_system:
    st.header("🧰 System Status")

    st.json({
        "meta_connected": bool(st.session_state["meta_access_token"]),
        "google_connected": bool(st.session_state["google_access_token"]),
        "ad_account_id": st.session_state.get("ad_account_id"),
    })