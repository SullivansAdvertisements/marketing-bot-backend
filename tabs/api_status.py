import streamlit as st
import os

def api_status_tab():
    st.header("🔌 API Connection Status")

    google_ok = all([
        os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
        os.getenv("GOOGLE_ADS_CLIENT_ID"),
        os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
        os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
        os.getenv("GOOGLE_ADS_CUSTOMER_ID"),
    ])

    meta_ok = all([
        os.getenv("META_ACCESS_TOKEN"),
        os.getenv("META_AD_ACCOUNT_ID"),
    ])

    st.session_state["api_status"] = {
        "google": google_ok,
        "meta": meta_ok,
    }

    st.metric("Google Ads API", "✅ Connected" if google_ok else "❌ Not Connected")
    st.metric("Meta Marketing API", "✅ Connected" if meta_ok else "❌ Not Connected")

    if not google_ok or not meta_ok:
        st.error("Research and Campaigns are locked until APIs are connected.")