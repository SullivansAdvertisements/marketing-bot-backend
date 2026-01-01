import streamlit as st
import requests

TOKEN = st.secrets.get("META_ACCESS_TOKEN")
ACCOUNT = st.secrets.get("META_AD_ACCOUNT_ID")


def render():
    st.subheader("Meta Performance Insights")

    url = f"https://graph.facebook.com/v18.0/{ACCOUNT}/insights"
    params = {
        "fields": "campaign_name,spend,impressions,clicks",
        "access_token": TOKEN,
    }

    r = requests.get(url, params=params)
    if r.status_code == 200:
        st.dataframe(r.json().get("data", []), use_container_width=True)
    else:
        st.error("Failed to fetch insights")