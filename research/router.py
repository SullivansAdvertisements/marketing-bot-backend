import streamlit as st
import pandas as pd

from research.google_keywords import fetch_google_keywords
from research.google_trends import fetch_google_trends
from research.meta_ad_library import fetch_meta_ads
from research.tiktok_trends import fetch_tiktok_trends
from research.youtube_trends import fetch_youtube_trends


def render():
    st.header("🔎 Market Research")

    # -------------------------
    # SESSION STATE
    # -------------------------
    for key in ["research_results"]:
        if key not in st.session_state:
            st.session_state[key] = {}

    # -------------------------
    # INPUT PANEL
    # -------------------------
    with st.form("research_form"):
        col1, col2 = st.columns(2)

        with col1:
            keyword = st.text_input(
                "Keyword / Market",
                placeholder="streetwear hoodies",
            )

        with col2:
            country = st.selectbox(
                "Country",
                ["US", "CA", "UK", "AU", "Global"],
            )

        platforms = st.multiselect(
            "Platforms",
            [
                "Google Keywords",
                "Google Trends",
                "Meta Ads",
                "TikTok",
                "YouTube",
            ],
            default=["Google Keywords", "Google Trends"],
        )

        run = st.form_submit_button("Run Research")

    # -------------------------
    # EXECUTION
    # -------------------------
    if run and keyword:
        results = {}

        with st.spinner("Running market analysis..."):
            if "Google Keywords" in platforms:
                results["Google Keywords"] = fetch_google_keywords(keyword, country)

            if "Google Trends" in platforms:
                results["Google Trends"] = fetch_google_trends(keyword, country)

            if "Meta Ads" in platforms:
                results["Meta Ads"] = fetch_meta_ads(keyword)

            if "TikTok" in platforms:
                results["TikTok Trends"] = fetch_tiktok_trends(keyword)

            if "YouTube" in platforms:
                results["YouTube Trends"] = fetch_youtube_trends(keyword)

        st.session_state.research_results = results

    # -------------------------
    # OUTPUT
    # -------------------------
    if st.session_state.research_results:
        st.subheader("📊 Research Results")

        for source, data in st.session_state.research_results.items():
            st.markdown(f"### {source}")

            if isinstance(data, pd.DataFrame):
                st.dataframe(data, use_container_width=True)
            elif isinstance(data, list):
                st.dataframe(pd.DataFrame(data), use_container_width=True)
            else:
                st.json(data)

        st.subheader("🧠 AI Research Notes")
        st.info(
            "Use these insights to validate demand, pricing power, "
            "creative direction, and platform selection."
        )