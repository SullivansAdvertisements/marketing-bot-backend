import streamlit as st
import pandas as pd
from campaigns.meta_delivery import fetch_meta_delivery_estimate

def render():
    st.subheader("🟦 Meta Ad Set — Estimated Reach")

    budget = st.number_input("Daily Budget ($)", min_value=5.0, value=20.0)
    age_min, age_max = st.slider("Age Range", 18, 65, (18, 44))

    if st.button("📊 Estimate Meta Reach"):
        token = st.secrets.get("META_ACCESS_TOKEN")
        ad_account = st.secrets.get("META_AD_ACCOUNT_ID")

        if not token or not ad_account:
            st.warning("Meta API keys missing")
            return

        result, error = fetch_meta_delivery_estimate(
            token,
            ad_account,
            budget,
            ["US"],
            age_min,
            age_max,
        )

        if error:
            st.warning(error)
            return

        st.dataframe(pd.DataFrame([result]), use_container_width=True)
        st.success("Meta estimate pulled from live API")