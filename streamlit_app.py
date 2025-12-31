import streamlit as st
import pandas as pd

# =================================================
# PAGE CONFIG — MUST BE FIRST
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =================================================
# OAUTH IMPORTS (repo root)
# =================================================
from oauth_meta import (
    meta_login_url,
    exchange_meta_code_for_token,
)

from oauth_google import (
    google_login_url,
    exchange_google_code_for_token,
)

# =================================================
# SESSION STATE INIT (DO NOT RESET)
# =================================================
for key in [
    "meta_token",
    "google_token",
    "active_tab",
    "research_df",
]:
    if key not in st.session_state:
        st.session_state[key] = None

if st.session_state["active_tab"] is None:
    st.session_state["active_tab"] = "Research"

# =================================================
# GLOBAL OAUTH CALLBACK HANDLER (CRITICAL)
# =================================================
query = st.query_params

if "code" in query and "state" in query:
    try:
        if query["state"] == "meta" and st.session_state["meta_token"] is None:
            st.session_state["meta_token"] = exchange_meta_code_for_token(query["code"])
            st.toast("Meta connected", icon="✅")

        elif query["state"] == "google" and st.session_state["google_token"] is None:
            st.session_state["google_token"] = exchange_google_code_for_token(query["code"])
            st.toast("Google connected", icon="✅")

        # prevent reprocessing
        st.query_params.clear()

    except Exception as e:
        st.error("OAuth failed")
        st.exception(e)

# =================================================
# APP TITLE
# =================================================
st.title("🚀 Marketing Bot")

# =================================================
# CONNECTION STATUS + LOGIN
# =================================================
st.subheader("🔐 Platform Connections")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Meta Ads",
        "Connected" if st.session_state["meta_token"] else "Not connected",
    )
    st.markdown(
        f"[🔵 Connect Meta Ads]({meta_login_url(state='meta')})"
    )

with c2:
    st.metric(
        "Google",
        "Connected" if st.session_state["google_token"] else "Not connected",
    )
    st.markdown(
        f"[🟢 Sign in with Google]({google_login_url(state='google')})"
    )

# =================================================
# RECONNECT BUTTONS (SAFE)
# =================================================
with st.expander("🔁 Reconnect Platforms"):
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state["meta_token"]:
            if st.button("Reconnect Meta"):
                st.session_state["meta_token"] = None
                st.info("Meta disconnected. Reconnect when ready.")

    with col2:
        if st.session_state["google_token"]:
            if st.button("Reconnect Google"):
                st.session_state["google_token"] = None
                st.info("Google disconnected. Reconnect when ready.")

# =================================================
# TABS (ALWAYS RENDER)
# =================================================
tabs = ["Research", "Creative", "Campaigns", "Strategy", "System"]
active_index = tabs.index(st.session_state["active_tab"])

tab_research, tab_creative, tab_campaigns, tab_strategy, tab_system = st.tabs(tabs)

# =================================================
# 🔍 RESEARCH TAB
# =================================================
with tab_research:
    st.session_state["active_tab"] = "Research"
    st.subheader("🔍 Market Research")

    if not st.session_state["google_token"]:
        st.warning("Connect Google to run research")

    keyword = st.text_input("Keyword", placeholder="streetwear, fitness, skincare")
    geo = st.selectbox("Country", ["US", "CA", "GB", "AU"])
    timeframe = st.selectbox(
        "Timeframe",
        ["7 days", "90 days", "12 months", "5 years"],
    )

    if st.button("Run Research", use_container_width=True):
        if not keyword:
            st.warning("Enter a keyword")
        elif not st.session_state["google_token"]:
            st.warning("Google not connected")
        else:
            # placeholder for real research engine
            df = pd.DataFrame(
                [
                    {"keyword": keyword, "interest": 82, "geo": geo},
                    {"keyword": f"{keyword} brand", "interest": 64, "geo": geo},
                ]
            )
            st.session_state["research_df"] = df

    if st.session_state["research_df"] is not None:
        st.divider()
        st.subheader("📊 Results")
        st.dataframe(
            st.session_state["research_df"],
            use_container_width=True,
            height=350,
        )

# =================================================
# 🎨 CREATIVE TAB
# =================================================
with tab_creative:
    st.session_state["active_tab"] = "Creative"
    st.subheader("🎨 Creative Builder")

    product = st.text_input("Product")
    audience = st.text_input("Audience")
    goal = st.selectbox("Goal", ["sales", "leads", "traffic"])

    if st.button("Generate Creative"):
        creative = {
            "headline": f"{product} for {audience}",
            "primary_text": "Limited offer. Act now.",
            "cta": "Shop Now",
        }
        st.json(creative)

# =================================================
# 📣 CAMPAIGNS TAB
# =================================================
with tab_campaigns:
    st.session_state["active_tab"] = "Campaigns"
    st.subheader("📣 Campaigns")

    if not st.session_state["meta_token"]:
        st.warning("Connect Meta to create campaigns")
    else:
        st.success("Meta connected — campaign tools ready")

# =================================================
# 🧠 STRATEGY TAB
# =================================================
with tab_strategy:
    st.session_state["active_tab"] = "Strategy"
    st.subheader("🧠 Strategy Planner")

    budget = st.number_input("Monthly Budget", min_value=100, value=1000)
    objective = st.selectbox("Objective", ["awareness", "traffic", "sales"])

    if st.button("Generate Strategy"):
        st.success("Strategy generated")
        st.json(
            {
                "Meta": budget * 0.6,
                "Google": budget * 0.4,
            }
        )

# =================================================
# 🧰 SYSTEM TAB
# =================================================
with tab_system:
    st.session_state["active_tab"] = "System"
    st.subheader("🧰 System Status")

    st.table(
        {
            "Platform": ["Meta", "Google"],
            "Connected": [
                bool(st.session_state["meta_token"]),
                bool(st.session_state["google_token"]),
            ],
        }
    )