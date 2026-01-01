import streamlit as st
import pandas as pd
import requests


def fetch_meta_delivery_estimate(budget):
    token = st.secrets.get("META_ACCESS_TOKEN")
    ad_account = st.secrets.get("META_AD_ACCOUNT_ID")

    if not token or not ad_account:
        return None, "Meta API keys missing"

    url = f"https://graph.facebook.com/v18.0/act_{ad_account}/delivery_estimate"

    payload = {
        "access_token": token,
        "optimization_goal": "LINK_CLICKS",
        "daily_budget": int(budget * 100),
        "targeting_spec": {
            "geo_locations": {"countries": ["US"]},
            "publisher_platforms": ["facebook", "instagram"],
        },
    }

    response = requests.post(url, json=payload).json()

    if "data" not in response:
        return None, "Meta API returned no estimate"

    est = response["data"][0]

    return {
        "Daily Budget ($)": budget,
        "Estimated Reach": est.get("users"),
        "Estimated Impressions": est.get("impressions"),
        "Platform": "Facebook / Instagram",
    }, None


def render():
    st.subheader("🟦 Meta Ad Set – Estimated Reach")

    budget = st.number_input("Daily Budget ($)", 5, 1000, 25)

    if st.button("📊 Estimate Meta Reach"):
        result, error = fetch_meta_delivery_estimate(budget)

        if error:
            st.warning(error)
            return

        st.dataframe(pd.DataFrame([result]), use_container_width=True)

        st.success("Data provided directly by Meta Delivery Estimate API")