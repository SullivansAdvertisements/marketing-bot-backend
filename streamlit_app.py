import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Marketing Intelligence Bot",
    layout="wide",
)

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

with tabs[1]:
    campaigns_render()

with tabs[2]:
    creative_render()

with tabs[3]:
    strategy_render()

with tabs[4]:
    system_render()