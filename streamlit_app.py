import streamlit as st
import os
import traceback

# ============================================================
# STREAMLIT CONFIG
# ============================================================
st.set_page_config(
    page_title="Marketing Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SAFE ERROR HANDLER (NO e SCOPE BUG)
# ============================================================
def render_tab(fn, label):
    try:
        fn()
    except Exception as err:
        st.error(f"{label} failed to load")
        st.code(str(err))
        st.code(traceback.format_exc())

# ============================================================
# SESSION STATE + SECRETS BOOTSTRAP
# ============================================================
def init_state():
    secrets = st.secrets

    st.session_state.setdefault("openai_ready", bool(secrets.get("OPENAI_API_KEY")))
    st.session_state.setdefault("google_ready", bool(secrets.get("GOOGLE_ADS_DEVELOPER_TOKEN")))
    st.session_state.setdefault("meta_ready", bool(secrets.get("META_ACCESS_TOKEN")))
    st.session_state.setdefault("tiktok_ready", bool(secrets.get("TIKTOK_API_KEY")))
    st.session_state.setdefault("youtube_ready", bool(secrets.get("YOUTUBE_API_KEY")))

    st.session_state.setdefault("research_results", {})
    st.session_state.setdefault("research_bundle", {})

init_state()

# ============================================================
# SAFE ROUTER IMPORTS
# ============================================================
def safe_import(path, fallback_name):
    try:
        module = __import__(path, fromlist=["render"])
        return module.render
    except Exception:
        def fallback():
            st.warning(f"{fallback_name} module not available")
        return fallback

research_render   = safe_import("research.router", "Research")
campaigns_render  = safe_import("campaigns.router", "Campaigns")
creative_render   = safe_import("creative.router", "Creative")
strategy_render   = safe_import("strategy.router", "Strategy")

# ============================================================
# SIDEBAR – PLATFORM STATUS
# ============================================================
with st.sidebar:
    st.title("🔐 Platform Status")

    def status(label, ok):
        st.success(f"{label} Connected") if ok else st.error(f"{label} Not Connected")

    status("OpenAI", st.session_state.openai_ready)
    status("Google Ads", st.session_state.google_ready)
    status("Meta Ads", st.session_state.meta_ready)
    status("TikTok", st.session_state.tiktok_ready)
    status("YouTube", st.session_state.youtube_ready)

    st.divider()
    st.caption("Secrets-only · No OAuth · Production-safe")

# ============================================================
# MAIN NAV
# ============================================================
tabs = st.tabs([
    "🔍 Research",
    "📣 Campaigns",
    "🎨 Creative",
    "📈 Strategy",
    "⚙️ System",
])

# ============================================================
# TAB RENDERING
# ============================================================
with tabs[0]:
    render_tab(research_render, "Research")

with tabs[1]:
    render_tab(campaigns_render, "Campaigns")

with tabs[2]:
    render_tab(creative_render, "Creative")

with tabs[3]:
    render_tab(strategy_render, "Strategy")

with tabs[4]:
    st.header("⚙️ System Overview")

    st.json({
        "ENV": st.secrets.get("ENV"),
        "LOG_LEVEL": st.secrets.get("LOG_LEVEL"),
        "OPENAI_READY": st.session_state.openai_ready,
        "GOOGLE_READY": st.session_state.google_ready,
        "META_READY": st.session_state.meta_ready,
        "TIKTOK_READY": st.session_state.tiktok_ready,
        "YOUTUBE_READY": st.session_state.youtube_ready,
    })

    st.success("System healthy. Tabs isolated. Errors contained.")