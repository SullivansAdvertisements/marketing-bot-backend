# app/campaigns/router.py

import streamlit as st

# ─────────────────────────────────────────────
# SAFE IMPORTS (do NOT execute on import)
# ─────────────────────────────────────────────
from .campaigns.google_ads import render as google_ads_render
from .campaigns.meta_ads import render as meta_ads_render
from .campaigns.meta_adsets import render as meta_adsets_render
from .campaigns.meta_insights import render as meta_insights_render
from .campaigns.tiktok_ads import render as tiktok_ads_render


# ─────────────────────────────────────────────
# SESSION STATE GUARDS
# ─────────────────────────────────────────────
def _ensure_session_state():
    defaults = {
        "meta_token": None,
        "google_token": None,
        "active_campaign_view": "overview",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────
# MAIN RENDER ENTRY (USED BY streamlit_app.py)
# ─────────────────────────────────────────────
def render():
    _ensure_session_state()

    st.header("📣 Campaigns")

    # ---- Connection Status (non-blocking) ----
    with st.expander("🔐 Platform Connection Status", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            if st.session_state.meta_token:
                st.success("Meta Ads connected")
            else:
                st.warning("Meta Ads not connected")

        with col2:
            if st.session_state.google_token:
                st.success("Google Ads connected")
            else:
                st.warning("Google Ads not connected")

    # ---- Campaign Navigation ----
    tabs = st.tabs([
        "Overview",
        "Google Ads",
        "Meta Campaigns",
        "Meta Ad Sets",
        "Meta Insights",
        "TikTok Ads",
    ])

    # ─────────────────────────────────────────
    # TAB 0 — OVERVIEW
    # ─────────────────────────────────────────
    with tabs[0]:
        st.subheader("Campaign Overview")

        st.markdown(
            """
            Use this section to:
            - Review connected platforms
            - Decide where to launch campaigns
            - Validate research before spend
            """
        )

        st.info("Campaign creation does not require both platforms connected.")

    # ─────────────────────────────────────────
    # TAB 1 — GOOGLE ADS
    # ─────────────────────────────────────────
    with tabs[1]:
        if not st.session_state.google_token:
            st.warning("Connect Google Ads to continue.")
        else:
            google_ads_render()

    # ─────────────────────────────────────────
    # TAB 2 — META CAMPAIGNS
    # ─────────────────────────────────────────
    with tabs[2]:
        if not st.session_state.meta_token:
            st.warning("Connect Meta Ads to continue.")
        else:
            meta_ads_render()

    # ─────────────────────────────────────────
    # TAB 3 — META AD SETS
    # ─────────────────────────────────────────
    with tabs[3]:
        if not st.session_state.meta_token:
            st.warning("Connect Meta Ads to continue.")
        else:
            meta_adsets_render()

    # ─────────────────────────────────────────
    # TAB 4 — META INSIGHTS
    # ─────────────────────────────────────────
    with tabs[4]:
        if not st.session_state.meta_token:
            st.warning("Connect Meta Ads to continue.")
        else:
            meta_insights_render()

    # ─────────────────────────────────────────
    # TAB 5 — TIKTOK ADS
    # ─────────────────────────────────────────
    with tabs[5]:
        tiktok_ads_render()
