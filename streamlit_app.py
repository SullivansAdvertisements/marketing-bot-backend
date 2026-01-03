import traceback
import streamlit as st

def safe_render(import_path: str):
    try:
        module = __import__(import_path, fromlist=["render"])
        return module.render
    except Exception as err:
        error_message = str(err)
        tb = traceback.format_exc()

        def _error():
            st.error(f"{import_path} failed to load")
            st.code(error_message)
            with st.expander("Traceback"):
                st.code(tb)

        return _error
# -----------------------------
# SAFE ROUTER IMPORTS
# -----------------------------
def safe_import(path, attr="render"):
    try:
        module = __import__(path, fromlist=[attr])
        return getattr(module, attr)
    except Exception as err:
        error_message = str(err)
        traceback_text = traceback.format_exc()

        def _error():
            st.error(f"{path} failed to load")
            st.code(error_message)
            st.expander("Traceback").code(traceback_text)

        return _error
# -----------------------------
# IMPORT ROUTERS
# -----------------------------
research_render = safe_import("research.router", "render")
campaigns_render = safe_import("campaigns.router", "render")
creative_render = safe_import("creative.router", "render")
strategy_render = safe_import("strategy.router", "render")

# Optional system/utils tab
def system_render():
    st.header("⚙️ System Status")

    secrets = [
        "OPENAI_API_KEY",
        "GOOGLE_ADS_DEVELOPER_TOKEN",
        "GOOGLE_ADS_CUSTOMER_ID",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID",
        "GOOGLE_ADS_REFRESH_TOKEN",
        "META_ACCESS_TOKEN",
        "META_AD_ACCOUNT_ID",
        "TIKTOK_API_KEY",
        "YOUTUBE_API_KEY",
    ]

    rows = []
    for key in secrets:
        rows.append({
            "Secret": key,
            "Status": "Connected" if st.secrets.get(key) else "Missing"
        })

    st.dataframe(rows, use_container_width=True)

    st.info("Secrets are read securely from Streamlit Cloud only.")


# -----------------------------
# NAVIGATION
# -----------------------------
tabs = st.tabs([
    "🔍 Research",
    "📣 Campaigns",
    "🎨 Creative",
    "📈 Strategy",
    "⚙️ System",
])

# -----------------------------
# TAB RENDERS
# -----------------------------
with tabs[0]:
    research_render()
import streamlit as st
import pandas as pd
from research.google_trends import fetch_google_trends

st.subheader("📈 Google Trends Research")

keywords = st.text_input(
    "Enter keywords (comma separated)",
    value="t shirt, streetwear, clothing brand"
)

geo = st.selectbox(
    "Target Country",
    ["US", "GB", "CA", "AU", "Worldwide"]
)

timeframe = st.selectbox(
    "Timeframe",
    ["today 3-m", "today 12-m", "today 5-y"]
)

if st.button("Run Google Trends Research"):
    with st.spinner("Fetching Google Trends data..."):
        data = fetch_google_trends(
            keywords=[k.strip() for k in keywords.split(",")],
            geo="" if geo == "Worldwide" else geo,
            timeframe=timeframe
        )

    # -----------------------------
    # Interest Over Time Table
    # -----------------------------
    if "interest_over_time" in data:
        st.markdown("### 📊 Interest Over Time")
        st.dataframe(
            data["interest_over_time"],
            use_container_width=True
        )

        st.download_button(
            "Download Interest Over Time CSV",
            data["interest_over_time"].to_csv(index=False),
            file_name="google_trends_interest_over_time.csv",
            mime="text/csv"
        )

    # -----------------------------
    # Related Queries Table
    # -----------------------------
    if "related_queries" in data:
        st.markdown("### 🔎 Related Queries")
        st.dataframe(
            data["related_queries"],
            use_container_width=True
        )

        st.download_button(
            "Download Related Queries CSV",
            data["related_queries"].to_csv(index=False),
            file_name="google_trends_related_queries.csv",
            mime="text/csv"
        )

    # -----------------------------
    # Related Topics Table
    # -----------------------------
    if "related_topics" in data:
        st.markdown("### 🧠 Related Topics")
        st.dataframe(
            data["related_topics"],
            use_container_width=True
        )

        st.download_button(
            "Download Related Topics CSV",
            data["related_topics"].to_csv(index=False),
            file_name="google_trends_related_topics.csv",
            mime="text/csv"
        )
with tabs[1]:
    campaigns_render()

with tabs[2]:
    creative_render()

with tabs[3]:
    strategy_render()

with tabs[4]:
    system_render()