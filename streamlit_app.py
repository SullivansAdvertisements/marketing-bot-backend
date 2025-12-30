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
# APP HEADER
# =================================================
st.title("🚀 Marketing Bot")

# =================================================
# QUERY PARAMS (SAFE / NON-EXPERIMENTAL)
# =================================================
query = dict(st.query_params)

# =================================================
# STEP 1 — META AUTH (REQUIRED)
# =================================================
st.subheader("🔵 Step 1: Connect Meta Ads")
st.markdown(f"[Connect Meta Ads]({meta_login_url()})")

if (
    "code" in query
    and "meta_access_token" not in st.session_state
    and query.get("state") == "meta"
):
    try:
        token = exchange_code_for_token(query["code"])
        st.session_state["meta_access_token"] = token

        # 🔒 Clear OAuth params (NO rerun needed)
        st.query_params.clear()

        st.success("Meta connected successfully")

    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)

# ⛔ HARD BLOCK — META REQUIRED
if "meta_access_token" not in st.session_state:
    st.info("Connect Meta Ads to unlock the app")
    st.stop()

META_ACCESS_TOKEN = st.session_state["meta_access_token"]

# =================================================
# STEP 2 — GOOGLE AUTH (OPTIONAL)
# =================================================
st.divider()
st.subheader("🟢 Step 2: Connect Google (Optional)")

try:
    google_url = google_login_url()
    st.markdown(f"[Sign in with Google]({google_url})")

    if (
        "code" in query
        and query.get("state") == "google"
        and "google_access_token" not in st.session_state
    ):
        try:
            token = exchange_google_code_for_token(query["code"])
            st.session_state["google_access_token"] = token["access_token"]

            # 🔒 Clear OAuth params
            st.query_params.clear()

            st.success("Google connected successfully")

        except Exception as e:
            st.warning("Google OAuth failed")
            st.exception(e)

except Exception:
    st.info("Google OAuth not configured")

# =================================================
# FETCH META AD ACCOUNTS
# =================================================
accounts_response = fetch_ad_accounts(META_ACCESS_TOKEN)
accounts = accounts_response.get("data", [])

if not accounts:
    st.error("No Meta ad accounts found")
    st.stop()

df = pd.DataFrame(accounts)[["id", "name"]]
df["clean_id"] = df["id"].str.replace("act_", "")

selected_account = st.selectbox(
    "Active Meta Ad Account",
    df["name"],
)

st.session_state["ad_account_id"] = df.loc[
    df["name"] == selected_account, "clean_id"
].iloc[0]

st.success(f"Using Meta account: {selected_account}")

# =================================================
# MAIN APP TABS (SAFE TO LOAD)
# =================================================
tab_research, tab_creative, tab_campaigns, tab_strategy, tab_system = st.tabs(
    ["🔍 Research", "🎨 Creative", "📣 Campaigns", "🧠 Strategy", "🧰 System"]
)

# =================================================
# RESEARCH TAB
# =================================================
with tab_research:
    st.header("🔍 Research")

    if "google_access_token" in st.session_state:
        st.success("Google connected — full research enabled")
    else:
        st.warning("Google not connected — limited research")

# =================================================
# CREATIVE TAB
# =================================================
with tab_creative:
    st.header("🎨 Creative")
    st.info("Creative tools load here")

# =================================================
# CAMPAIGNS TAB
# =================================================
with tab_campaigns:
    st.header("📣 Campaigns")
    st.info("Meta campaign builder ready")

# =================================================
# STRATEGY TAB
# =================================================
with tab_strategy:
    st.header("🧠 Strategy")
    st.info("Budget & planning tools")

# =================================================
# SYSTEM TAB
# =================================================
with tab_system:
    st.header("🧰 System Status")

    st.write("Meta Connected:", True)
    st.write("Google Connected:", "google_access_token" in st.session_state)
    st.write("Ad Account ID:", st.session_state.get("ad_account_id"))