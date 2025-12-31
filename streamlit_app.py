import streamlit as st
import pandas as pd

from oauth_meta import meta_login_url, exchange_meta_code_for_token, fetch_ad_accounts
from oauth_google import google_login_url, exchange_google_code_for_token

# =================================================
# PAGE CONFIG — MOBILE SAFE
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("🚀 Marketing Bot")
st.caption("Research, creatives, campaigns, and strategy. Connect platforms in any order.")

# =================================================
# SESSION STATE INIT
# =================================================
for key in [
    "meta_token",
    "google_token",
    "meta_accounts",
]:
    if key not in st.session_state:
        st.session_state[key] = None

# =================================================
# HANDLE OAUTH CALLBACK (SAFE)
# =================================================
query = st.query_params

if "code" in query and "state" in query:
    try:
        if query["state"] == "meta" and not st.session_state["meta_token"]:
            st.session_state["meta_token"] = exchange_meta_code_for_token(query["code"])
            st.success("✅ Meta connected")

        if query["state"] == "google" and not st.session_state["google_token"]:
            st.session_state["google_token"] = exchange_google_code_for_token(query["code"])
            st.success("✅ Google connected")

    except Exception as e:
        st.error("OAuth failed")
        st.exception(e)

# =================================================
# CONNECTION STATUS
# =================================================
st.subheader("🔐 Connection Status")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Meta Ads",
        "Connected" if st.session_state["meta_token"] else "Not connected",
    )

with col2:
    st.metric(
        "Google",
        "Connected" if st.session_state["google_token"] else "Not connected",
    )

# =================================================
# CONNECT BUTTONS (NO LOCKING)
# =================================================
with st.expander("🔑 Connect Platforms", expanded=True):
    if not st.session_state["meta_token"]:
        st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")
    else:
        st.success("Meta already connected")

    if not st.session_state["google_token"]:
        st.markdown(f"[🟢 Sign in with Google]({google_login_url()})")
    else:
        st.success("Google already connected")

# =================================================
# LOAD META ACCOUNTS (ONCE)
# =================================================
if st.session_state["meta_token"] and not st.session_state["meta_accounts"]:
    try:
        data = fetch_ad_accounts(st.session_state["meta_token"])
        st.session_state["meta_accounts"] = pd.DataFrame(data["data"])
    except Exception as e:
        st.error("Failed to load Meta accounts")
        st.exception(e)

# =================================================
# MAIN APP TABS (ALWAYS AVAILABLE)
# =================================================
tabs = st.tabs(["🔍 Research", "🎨 Creative", "📣 Campaigns", "🧠 Strategy", "🧰 System"])

# =================================================
# 🔍 RESEARCH TAB
# =================================================
with tabs[0]:
    st.subheader("Market Research")

    if not st.session_state["google_token"]:
        st.info("Connect Google to unlock research features.")
    else:
        st.success("Google connected — research enabled")

        data = [
            {"Keyword": "Streetwear hoodies", "Interest": 78},
            {"Keyword": "Graphic tees", "Interest": 64},
        ]
        st.dataframe(pd.DataFrame(data), use_container_width=True)

# =================================================
# 🎨 CREATIVE TAB
# =================================================
with tabs[1]:
    st.subheader("Creative Builder")

    st.text_input("Product")
    st.text_input("Audience")
    st.selectbox("Platform", ["Meta", "Google", "TikTok"])

# =================================================
# 📣 CAMPAIGNS TAB
# =================================================
with tabs[2]:
    st.subheader("Campaigns")

    if st.session_state["meta_accounts"] is not None:
        st.dataframe(
            st.session_state["meta_accounts"][["name", "id"]],
            use_container_width=True,
        )
    else:
        st.info("Connect Meta to manage campaigns.")

# =================================================
# 🧠 STRATEGY TAB
# =================================================
with tabs[3]:
    st.subheader("Strategy & Budgeting")
    st.number_input("Monthly Budget", 100, 100000, 1000)

# =================================================
# 🧰 SYSTEM TAB
# =================================================
with tabs[4]:
    st.subheader("System Status")
    st.json({
        "meta_connected": bool(st.session_state["meta_token"]),
        "google_connected": bool(st.session_state["google_token"]),
    })