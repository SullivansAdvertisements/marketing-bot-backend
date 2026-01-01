import streamlit as st
import os

# -------------------------------------------------
# PAGE CONFIG (MOBILE FIRST)
# -------------------------------------------------
st.set_page_config(
    page_title="Marketing Bot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------------------------------
# SAFE ROUTER IMPORTS
# -------------------------------------------------
def safe_import(path, fallback_name):
    try:
        module = __import__(path, fromlist=["render"])
        return module.render
    except Exception as e:
        def _fallback():
            st.error(f"{fallback_name} failed to load.")
            st.code(str(e))
        return _fallback


research_render = safe_import("research.router", "Research")
campaigns_render = safe_import("campaigns.router", "Campaigns")
creative_render = safe_import("creative.router", "Creative")
strategy_render = safe_import("strategy.router", "Strategy")

# -------------------------------------------------
# GLOBAL API STATUS
# -------------------------------------------------
def get_api_status():
    def has(key):
        return bool(os.getenv(key) or st.secrets.get(key, None))

    return {
        "Google Ads": has("GOOGLE_ADS_API_KEY"),
        "Meta Ads": has("META_ACCESS_TOKEN"),
        "OpenAI": has("OPENAI_API_KEY"),
        "TikTok": has("TIKTOK_API_KEY"),
        "YouTube": has("YOUTUBE_API_KEY"),
    }


# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("🚀 Marketing Bot")

with st.expander("🔐 API & Platform Status", expanded=False):
    cols = st.columns(5)
    for col, (name, ok) in zip(cols, get_api_status().items()):
        col.success(name) if ok else col.warning(name)

st.divider()

# -------------------------------------------------
# MAIN NAV TABS
# -------------------------------------------------
tabs = st.tabs([
    "🔎 Research",
    "📣 Campaigns",
    "🎨 Creative",
    "📊 Strategy",
    "🛠 Utilities",
])

# -------------------------------------------------
# RESEARCH
# -------------------------------------------------
with tabs[0]:
    research_render()

    # Promote research into creative + strategy
    if "research_results" in st.session_state and st.session_state.research_results:
        st.session_state["research_bundle"] = st.session_state.research_results

# -------------------------------------------------
# CAMPAIGNS
# -------------------------------------------------
with tabs[1]:
    campaigns_render()

# -------------------------------------------------
# CREATIVE (OPENAI)
# -------------------------------------------------
with tabs[2]:
    creative_render()

# -------------------------------------------------
# STRATEGY
# -------------------------------------------------
with tabs[3]:
    strategy_render()

# -------------------------------------------------
# UTILITIES
# -------------------------------------------------
with tabs[4]:
    st.header("🛠 System Utilities")

    st.subheader("Environment Diagnostics")
    env = {
        "GOOGLE_ADS_API_KEY": bool(os.getenv("GOOGLE_ADS_API_KEY") or st.secrets.get("GOOGLE_ADS_API_KEY", None)),
        "META_ACCESS_TOKEN": bool(os.getenv("META_ACCESS_TOKEN") or st.secrets.get("META_ACCESS_TOKEN", None)),
        "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)),
        "TIKTOK_API_KEY": bool(os.getenv("TIKTOK_API_KEY") or st.secrets.get("TIKTOK_API_KEY", None)),
        "YOUTUBE_API_KEY": bool(os.getenv("YOUTUBE_API_KEY") or st.secrets.get("YOUTUBE_API_KEY", None)),
    }

    st.table(
        [{"Key": k, "Status": "Connected" if v else "Missing"} for k, v in env.items()]
    )

    st.subheader("Session State")
    st.json({k: type(v).__name__ for k, v in st.session_state.items()})

    st.info(
        """
        Utilities exist to:
        • Monitor API connectivity  
        • Debug session state  
        • Prevent silent failures  
        """
    )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.divider()
st.caption("Marketing Bot • Modular • API-Driven • Research-First")