import streamlit as st
import pandas as pd

def render():
    st.subheader("📊 Meta Performance Benchmarks")

    st.dataframe(pd.DataFrame([
        {"Metric": "CTR", "Good": "1.5%+", "Excellent": "2.5%+"},
        {"Metric": "CPM", "Good": "$8–$14", "Excellent": "< $8"},
        {"Metric": "Frequency", "Good": "< 2.5", "Risk": "> 3"},
        {"Metric": "ROAS", "Good": "2.5x", "Excellent": "4x+"},
    ]), use_container_width=True)

    st.info("Use reach estimates + these benchmarks to validate scaling.")