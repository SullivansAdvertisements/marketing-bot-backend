import streamlit as st
import pandas as pd
import traceback

# =========================================================
# PAGE CONFIG (MUST BE FIRST)
# =========================================================
st.set_page_config(
    page_title="Marketing Intelligence OS",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================================================
# SAFE SECRET ACCESS
# =========================================================
def secret(key: str):
    return st.secrets.get(key)

def has_secret(key: str) -> bool:
    return bool(secret(key))

# =========================================================
# SESSION STATE BOOTSTRAP
# =========================================================
SESSION_DEFAULTS = {
    "research_results": {},
    "research_bundle": {},
    "google_token": secret("GOOGLE_ADS_REFRESH_TOKEN"),
    "meta_token": secret("META_ACCESS_TOKEN"),
}

for k, v in SESSION_DEFAULTS.items():
    st.session_state.setdefault(k, v)

# =========================================================
# PLATFORM STATUS
# =========================================================
PLATFORM_STATUS = {
    "OpenAI": has_secret("OPENAI_API_KEY"),
    "Google Ads": has_secret("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "Meta Ads": has_secret("META_ACCESS_TOKEN"),
    "TikTok": has_secret("TIKTOK_API_KEY"),
    "YouTube": has_secret("YOUTUBE_API_KEY"),
}

# =========================================================
# SAFE IMPORT HELPER (NEVER CRASH)
# =========================================================
def safe_import(path: str):
    try:
        module = __import__(path, fromlist=["render"])
        return module.render
    except Exception as e:
        def _error():
            st.error(f"{path} failed to load")
            st.code(str(e))
        return _error

# =========================================================
# LOAD ROUTERS (MATCHES YOUR REPO)
# =========================================================
research_render   = safe_import("research.router")
creative_render   = safe_import("creative.router")
campaigns_render  = safe_import("campaigns.router")
strategy_render   = safe_import("strategy.router")

# =========================================================
# SAFE TAB EXECUTION (NO MORE 'e' BUGS)
# =========================================================
def render_tab(fn, name):
    try:
        fn()
    except Exception:
        st.error(f"{name} tab crashed")
        st.code(traceback.format_exc())

# =========================================================
# APP HEADER
# =========================================================
st.title("🚀 Marketing Intelligence OS")

with st.expander("🔐 API & Platform Status", expanded=True):
    df = pd.DataFrame([
        {"Platform": k, "Status": "✅ Connected" if v else "❌ Missing"}
        for k, v in PLATFORM_STATUS.items()
    ])
    st.dataframe(df, use_container_width=True)

# =========================================================
# MAIN NAV TABS
# =========================================================
tabs = st.tabs([
    "🔎 Research",
    "🎨 Creative",
    "📣 Campaigns",
    "📈 Strategy",
    "🧰 System",
])

# =========================================================
# RESEARCH
# =========================================================
with tabs[0]:
    render_tab(research_render, "Research")

# =========================================================
# CREATIVE (OPENAI)
# =========================================================
with tabs[1]:
    if not PLATFORM_STATUS["OpenAI"]:
        st.warning("OpenAI key missing — creative generation disabled.")
    render_tab(creative_render, "Creative")

# =========================================================
# CAMPAIGNS
# =========================================================
with tabs[2]:
    if not (PLATFORM_STATUS["Google Ads"] or PLATFORM_STATUS["Meta Ads"]):
        st.warning("No ad platforms connected — read-only mode.")
    render_tab(campaigns_render, "Campaigns")

# =========================================================
# STRATEGY
# =========================================================
with tabs[3]:
    render_tab(strategy_render, "Strategy")

# =========================================================
# SYSTEM / DEBUG
# =========================================================
with tabs[4]:
    st.subheader("🧰 System Diagnostics")

    st.json({
        "ENV": secret("ENV"),
        "LOG_LEVEL": secret("LOG_LEVEL"),
        "Secrets Loaded": list(st.secrets.keys()),
        "Session Keys": list(st.session_state.keys()),
    })

    st.markdown("""
    **System Guarantees**
    - No tab can crash the app
    - Missing APIs degrade gracefully
    - Secrets-only auth (Streamlit Cloud safe)
    - Research feeds Creative & Strategy
    """)

# =========================================================
# FOOTER
# =========================================================
st.caption("Enterprise-safe • Secrets-only • Mobile-ready • AI-powered")