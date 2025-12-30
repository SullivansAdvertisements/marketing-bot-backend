import streamlit as st
import pandas as pd

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
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("🚀 Marketing Bot")

# =================================================
# QUERY PARAMS (SAFE)
# =================================================
query = dict(st.query_params)

# =================================================
# META AUTH (OPTIONAL — NO GATING)
# =================================================
st.subheader("🔵 Meta Connection")

st.markdown(f"[Connect Meta Ads]({meta_login_url()})")

if (
    "code" in query
    and query.get("state") == "meta"
    and "meta_access_token" not in st.session_state
):
    try:
        token = exchange_code_for_token(query["code"])
        st.session_state["meta_access_token"] = token
        st.query_params.clear()
        st.success("Meta connected")
    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)

# =================================================
# GOOGLE AUTH (OPTIONAL — NO GATING)
# =================================================
st.divider()
st.subheader("🟢 Google Connection")

st.markdown(f"[Sign in with Google]({google_login_url()})")

if (
    "code" in query
    and query.get("state") == "google"
    and "google_access_token" not in st.session_state
):
    try:
        token = exchange_google_code_for_token(query["code"])
        st.session_state["google_access_token"] = token["access_token"]
        st.query_params.clear()
        st.success("Google connected")
    except Exception as e:
        st.warning("Google OAuth failed")
        st.exception(e)

# =================================================
# STATUS (NO STOPS ANYWHERE)
# =================================================
st.divider()
st.subheader("🔐 Connection Status")

st.write("Meta Connected:", "meta_access_token" in st.session_state)
st.write("Google Connected:", "google_access_token" in st.session_state)

# =================================================
# META ACCOUNTS (ONLY IF CONNECTED)
# =================================================
if "meta_access_token" in st.session_state:
    accounts = fetch_ad_accounts(st.session_state["meta_access_token"]).get("data", [])

    if accounts:
        df = pd.DataFrame(accounts)
        df["clean_id"] = df["id"].str.replace("act_", "")
        selected = st.selectbox("Meta Ad Account", df["name"])
        st.session_state["ad_account_id"] = df.loc[
            df["name"] == selected, "clean_id"
        ].iloc[0]

# =================================================
# MAIN APP TABS (ALWAYS LOAD)
# =================================================
tab_research, tab_creative, tab_campaigns, tab_strategy, tab_system = st.tabs(
    ["🔍 Research", "🎨 Creative", "📣 Campaigns", "🧠 Strategy", "🧰 System"]
)

with tab_research:
    st.info("Research tools ready")

with tab_creative:
    st.info("Creative generator ready")

with tab_campaigns:
    st.info("Campaign builder ready")

with tab_strategy:
    st.info("Strategy planner ready")

with tab_system:
    st.write("Session State")
    st.json(st.session_state)