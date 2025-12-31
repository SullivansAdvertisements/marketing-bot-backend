import streamlit as st
import pandas as pd

from oauth_meta import meta_login_url, exchange_meta_code_for_token
from oauth_google import google_login_url, exchange_google_code_for_token

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("🚀 Marketing Bot")
st.caption("Research, campaigns, and strategy. Connect platforms anytime.")

# ============================================================
# SESSION STATE INIT (NON-BLOCKING)
# ============================================================
for key in [
    "meta_token",
    "google_token",
]:
    if key not in st.session_state:
        st.session_state[key] = None

# ============================================================
# HANDLE OAUTH CALLBACKS (BACKGROUND ONLY)
# ============================================================
query = st.query_params

if "code" in query and "state" in query:
    try:
        if query["state"] == "meta" and st.session_state["meta_token"] is None:
            token = exchange_meta_code_for_token(query["code"])
            st.session_state["meta_token"] = token
            st.success("✅ Meta connected")

        if query["state"] == "google" and st.session_state["google_token"] is None:
            token = exchange_google_code_for_token(query["code"])
            st.session_state["google_token"] = token
            st.success("✅ Google connected")

    except Exception as e:
        st.error("OAuth failed")
        st.exception(e)

    # ✅ CLEAR URL WITHOUT RELOAD BREAKING STATE
    st.query_params.clear()

# ============================================================
# CONNECTION STATUS (INFORMATION ONLY)
# ============================================================
st.subheader("🔐 Platform Connections")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Meta Ads**")
    st.write("Connected" if st.session_state["meta_token"] else "Not connected")
    if not st.session_state["meta_token"]:
        st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url(state='meta')})")

with col2:
    st.markdown("**Google Ads**")
    st.write("Connected" if st.session_state["google_token"] else "Not connected")
    if not st.session_state["google_token"]:
        st.markdown(f"[🟢 Sign in with Google]({google_login_url(state='google')})")

st.divider()

# ============================================================
# APP TABS (ALWAYS AVAILABLE)
# ============================================================
tabs = st.tabs([
    "🔍 Research",
    "🎨 Creative",
    "📊 Campaigns",
    "🧠 Strategy",
    "⚙️ System",
])

# ============================================================
# RESEARCH TAB
# ============================================================
with tabs[0]:
    st.subheader("Market Research")

    platform = st.selectbox(
        "Platform",
        ["Google", "Meta"],
    )

    keyword = st.text_input("Keyword")
    country = st.selectbox("Country", ["US", "CA", "UK"])

    st.button("Run Research")

    st.info(
        "Google or Meta can be connected independently. "
        "Research works even if only one platform is connected."
    )

# ============================================================
# CREATIVE TAB
# ============================================================
with tabs[1]:
    st.subheader("Creative Generator")
    st.text_area("Ad Concept")
    st.button("Generate Creatives")

# ============================================================
# CAMPAIGNS TAB
# ============================================================
with tabs[2]:
    st.subheader("Campaign Builder")

    if not st.session_state["meta_token"] and not st.session_state["google_token"]:
        st.warning("Connect at least one platform to launch campaigns.")

    st.button("Create Campaign")

# ============================================================
# STRATEGY TAB
# ============================================================
with tabs[3]:
    st.subheader("Strategy")
    st.write("Cross-platform planning and budget allocation.")

# ============================================================
# SYSTEM TAB
# ============================================================
with tabs[4]:
    st.subheader("System Status")

    st.json({
        "meta_connected": bool(st.session_state["meta_token"]),
        "google_connected": bool(st.session_state["google_token"]),
    })

    if st.button("Reset Connections"):
        st.session_state["meta_token"] = None
        st.session_state["google_token"] = None
        st.success("Connections cleared")