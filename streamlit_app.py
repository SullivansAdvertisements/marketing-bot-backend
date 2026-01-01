import streamlit as st
import traceback

# --------------------------------------------------
# STREAMLIT CONFIG (MUST BE FIRST)
# --------------------------------------------------
st.set_page_config(
    page_title="Marketing Intelligence Platform",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🚀 Marketing Intelligence Platform")

# --------------------------------------------------
# SAFE IMPORT HELPER
# --------------------------------------------------
def safe_import(module_path, label):
    try:
        module = __import__(module_path, fromlist=["render"])
        return module.render
    except Exception as e:
        def _error():
            st.error(f"❌ {label} failed to load")
            st.code(str(e))
        return _error


# --------------------------------------------------
# LOAD TAB RENDERERS (SAFE)
# --------------------------------------------------
research_render = safe_import("research.router", "Research")
campaigns_render = safe_import("campaigns.router", "Campaigns")
creative_render = safe_import("creative.router", "Creative")
strategy_render = safe_import("strategy.router", "Strategy")
utils_render = safe_import("utils.logging", "Utils")  # placeholder


# --------------------------------------------------
# GLOBAL API STATUS
# --------------------------------------------------
with st.expander("🔐 API & Platform Status", expanded=False):
    st.markdown("### Active Connections")

    def status(name, key):
        connected = bool(st.secrets.get(key))
        st.success(f"{name} Connected") if connected else st.warning(f"{name} Not Connected")

    status("Google Ads", "GOOGLE_ADS_API_KEY")
    status("Meta Ads", "META_ACCESS_TOKEN")
    status("OpenAI", "OPENAI_API_KEY")
    status("TikTok", "TIKTOK_API_KEY")
    status("YouTube", "YOUTUBE_API_KEY")


# --------------------------------------------------
# MAIN NAV TABS
# --------------------------------------------------
tabs = st.tabs([
    "🔎 Research",
    "📣 Campaigns",
    "🎨 Creative",
    "📈 Strategy",
    "🛠 Utils",
])

# --------------------------------------------------
# TAB EXECUTION (ISOLATED & SAFE)
# --------------------------------------------------
with tabs[0]:
    try:
        research_render()
    except Exception:
        st.error("Research tab crashed")
        st.code(traceback.format_exc())

with tabs[1]:
    try:
        campaigns_render()
    except Exception:
        st.error("Campaigns tab crashed")
        st.code(traceback.format_exc())

with tabs[2]:
    try:
        creative_render()
    except Exception:
        st.error("Creative tab crashed")
        st.code(traceback.format_exc())

with tabs[3]:
    try:
        strategy_render()
    except Exception:
        st.error("Strategy tab crashed")
        st.code(traceback.format_exc())

with tabs[4]:
    st.header("🛠 Utilities")
    st.markdown("""
    This section contains:
    - Logging
    - Validators
    - Rate limits
    """)
    st.success("Utilities loaded successfully")