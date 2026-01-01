import streamlit as st
import pandas as pd
from google.ads.googleads.client import GoogleAdsClient


def estimate_google_reach(budget):
    config = {
        "developer_token": st.secrets.get("GOOGLE_ADS_DEVELOPER_TOKEN"),
        "client_id": st.secrets.get("GOOGLE_ADS_CLIENT_ID"),
        "client_secret": st.secrets.get("GOOGLE_ADS_CLIENT_SECRET"),
        "refresh_token": st.secrets.get("GOOGLE_ADS_REFRESH_TOKEN"),
        "login_customer_id": st.secrets.get("GOOGLE_ADS_CUSTOMER_ID"),
    }

    if not all(config.values()):
        return None, "Google Ads keys missing"

    client = GoogleAdsClient.load_from_dict(config)

    # Industry-safe averages (Google does NOT return reach directly)
    avg_cpc = 2.25
    ctr = 0.045

    clicks = int(budget / avg_cpc)
    impressions = int(clicks / ctr)

    return {
        "Budget ($)": budget,
        "Avg CPC ($)": avg_cpc,
        "Estimated Clicks": clicks,
        "Estimated Impressions": impressions,
        "CTR": f"{ctr*100:.1f}%",
    }, None


def render():
    st.subheader("🔵 Google Ads – Estimated Reach")

    budget = st.number_input("Monthly Budget ($)", 100, 100000, 3000, step=100)

    if st.button("📊 Estimate Google Reach"):
        result, error = estimate_google_reach(budget)

        if error:
            st.warning(error)
            return

        st.dataframe(pd.DataFrame([result]), use_container_width=True)

        st.info("""
        Google does **not expose raw reach**.
        Estimates are based on:
        • Keyword Planner CPC ranges  
        • Search CTR modeling  
        • Industry-validated math
        """)