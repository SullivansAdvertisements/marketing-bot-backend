# streamlit_app.py
# ============================================================
# GLOBAL PATH FIX (CRITICAL FOR STREAMLIT CLOUD)
# ============================================================
import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

# ============================================================
# IMPORTS
# ============================================================
import streamlit as st

from research.router import render as research_render
from campaigns.router import render as campaigns_render
from strategy.router import render as strategy_render
from creative.router import generate_creative  # optional usage

# ============================================================
# STREAMLIT CONFIG
# ============================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
def init_session():
    defaults = {
        # platform tokens (background)
        "meta_token": None,
        "google_token": None,

        # ui
        "active_tab": "Research",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_session()

# ============================================================
# LOAD SECRETS (NO OAUTH)
# ============================================================
# These live in Streamlit Cloud → App → Settings → Secrets

if "META_ACCESS_TOKEN" in st.secrets:
    st.session_state.meta_token = st.secrets["META_ACCESS_TOKEN"]

if "GOOGLE_ADS_DEVELOPER_TOKEN" in st.secrets:
    st.session_state.google_token = st.secrets["GOOGLE_ADS_DEVELOPER_TOKEN"]

# ============================================================
# HEADER
# ============================================================
st.title("🚀 Marketing Bot")

st.caption(
    "Research → Strategy → Campaigns\n"
    "Platforms connect silently in the background"
)

# ============================================================
# PLATFORM STATUS (NON-BLOCKING)
# ============================================================
with st.expander("🔐 Platform Status", expanded=False):
    c1, c2 = st.columns(2)

    with c1:
        if st.session_state.meta_token:
            st.success("Meta Ads ready")
        else:
            st.warning("Meta Ads token missing")

    with c2:
        if st.session_state.google_token:
            st.success("Google Ads ready")
        else:
            st.warning("Google Ads token missing")

# ============================================================
# MAIN NAVIGATION (MOBILE FRIENDLY)
# ============================================================
tabs = st.tabs(
    [
        "🔎 Research",
        "📈 Strategy",
        "📣 Campaigns",
    ]
)

# ============================================================
# TAB 1 — RESEARCH
# ============================================================
with tabs[0]:
    research_render()

# ============================================================
# TAB 2 — STRATEGY
# ============================================================
with tabs[1]:
    strategy_render()

# ============================================================
# TAB 3 — CAMPAIGNS
# ============================================================
with tabs[2]:
    campaigns_render()

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption(
    "Marketing Bot • Modular • Token-safe • Mobile-ready"
)