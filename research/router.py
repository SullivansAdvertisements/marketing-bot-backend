# app/research/router.py

import streamlit as st
import pandas as pd

from app.research.google_keywords import fetch_google_keywords
from app.research.google_trends import fetch_google_trends
from app.research.meta_ad_library import fetch_meta_ads
from app.research.tiktok_trends import fetch_tiktok_trends
from app.research.youtube_trends import fetch_youtube_trends


def render():
    st.header("🔎 Market Research")

    # -------------------------
    # SESSION STATE SAFETY
    # -------------------------
    for key in [
        "research_keyword",
        "research_country",
        "research_platforms",
        "research_results",
    ]:
        if key not in st.session_state:
            st.session_state[key] = None

    # -------------------------
    # INPUTS
    # -------------------------
    with st.form("research_form"):
        keyword = st.text_input(
            "Primary Keyword / Topic",
            placeholder="e.g. streetwear hoodies",
        )

        country = st.selectbox(
            "Target Country",
            ["US", "CA", "UK", "AU", "Global"],
        )

        platforms = st.multiselect(
            "Platforms to Research",
            [
                "Google Search",
                "Google Trends",
                "Meta Ads",
                "TikTok",
                "YouTube",
            ],
            default=["Google Search", "Google Trends"],
        )

        submitted = st.form_submit_button("Run Research")

    # -------------------------
    # RUN RESEARCH
    # -------------------------
    if submitted and keyword:
        results = {}

        with st.spinner("Collecting research data..."):
            if "Google Search" in platforms:
                results["Google Keywords"] = fetch_google_keywords(
                    keyword, country
                )

            if "Google Trends" in platforms:
                results["Google Trends"] = fetch_google_trends(
                    keyword, country
                )

            if "Meta Ads" in platforms:
                results["Meta Ads"] = fetch_meta_ads(keyword)

            if "TikTok" in platforms:
                results["TikTok Trends"] = fetch_tiktok_trends(keyword)

            if "YouTube" in platforms:
                results["YouTube Trends"] = fetch_youtube_trends(keyword)

        st.session_state.research_results = results

    # -------------------------
    # DISPLAY RESULTS
    # -------------------------
    if st.session_state.research_results:
        st.subheader("📊 Research Results")

        for source, data in st.session_state.research_results.items():
            st.markdown(f"### {source}")

            if data is None or len(data) == 0:
                st.info("No data returned.")
                continue

            if isinstance(data, pd.DataFrame):
                st.dataframe(data, use_container_width=True)
            elif isinstance(data, list):
                st.table(pd.DataFrame(data))
            else:
                st.json(data)

    # -------------------------
    # INSIGHT SUMMARY
    # -------------------------
    if st.session_state.research_results:
        st.subheader("🧠 Research Summary")

        st.markdown(
            """
            Use this research to:
            - Identify **high-intent keywords**
            - Spot **creative trends**
            - Validate **platform demand**
            - Feed **campaign & budget strategy**
            """
        )
