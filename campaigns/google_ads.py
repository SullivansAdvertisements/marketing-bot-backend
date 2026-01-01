import streamlit as st
import pandas as pd


def render():
    st.subheader("Google Ads Campaign Builder")

    campaign = st.text_input("Campaign Name")
    budget = st.number_input("Daily Budget ($)", min_value=5, value=20)
    objective = st.selectbox("Objective", ["Traffic", "Leads", "Sales"])

    if st.button("Create Campaign Plan"):
        df = pd.DataFrame([{
            "campaign": campaign,
            "budget": budget,
            "objective": objective,
            "status": "READY"
        }])

        st.success("Campaign plan created (ready for push)")
        st.dataframe(df, use_container_width=True)