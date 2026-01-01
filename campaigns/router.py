import streamlit as st

from campaigns.google_ads import render as google_ads_render
from campaigns.meta_ads import render as meta_ads_render
from campaigns.meta_adsets import render as meta_adsets_render
from campaigns.meta_insights import render as meta_insights_render
from campaigns.tiktok_ads import render as tiktok_ads_render


def _ensure_state():
    defaults = {
        "google_connected": bool(st.secrets.get("GOOGLE_ADS_API_KEY")),
        "meta_connected": bool(st.secrets.get("META_ACCESS_TOKEN")),
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


def render():
    _ensure_state()

    st.header("📣 Campaign Management")

    # ---- STATUS ----
    with st.expander("🔐 Platform Status"):
        c1, c2 = st.columns(2)
        c1.success("Google Ads Connected" if st.session_state.google_connected else "Google Ads Not Connected")
        c2.success("Meta Ads Connected" if st.session_state.meta_connected else "Meta Ads Not Connected")

    tabs = st.tabs([
        "Overview",
        "Google Ads",
        "Meta Campaigns",
        "Meta Ad Sets",
        "Meta Insights",
        "TikTok Ads",
    ])

    with tabs[0]:
        st.markdown("""
        ### Campaign Control Center
        - Create campaigns
        - Manage ad sets
        - Review performance
        """)

    with tabs[1]:
        if st.session_state.google_connected:
            google_ads_render()
        else:
            st.warning("Google Ads API key not set.")

    with tabs[2]:
        if st.session_state.meta_connected:
            meta_ads_render()
        else:
            st.warning("Meta access token missing.")

    with tabs[3]:
        if st.session_state.meta_connected:
            meta_adsets_render()
        else:
            st.warning("Meta access token missing.")

    with tabs[4]:
        if st.session_state.meta_connected:
            meta_insights_render()
        else:
            st.warning("Meta access token missing.")

    with tabs[5]:
        tiktok_ads_render()