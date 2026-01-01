import streamlit as st
import requests
import os


META_TOKEN = st.secrets.get("META_ACCESS_TOKEN")
AD_ACCOUNT = st.secrets.get("META_AD_ACCOUNT_ID")


def render():
    st.subheader("Meta Campaign Creator")

    name = st.text_input("Campaign Name")
    objective = st.selectbox("Objective", ["LINK_CLICKS", "CONVERSIONS", "AWARENESS"])

    if st.button("Create Meta Campaign"):
        url = f"https://graph.facebook.com/v18.0/{AD_ACCOUNT}/campaigns"

        payload = {
            "name": name,
            "objective": objective,
            "status": "PAUSED",
            "access_token": META_TOKEN,
        }

        r = requests.post(url, data=payload)
        if r.status_code == 200:
            st.success("Campaign created successfully")
            st.json(r.json())
        else:
            st.error("Failed to create campaign")
            st.json(r.json())