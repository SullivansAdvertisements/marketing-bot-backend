# research/router.py
import streamlit as st
import pandas as pd

# SAFE IMPORTS (no execution)
try:
    from research.google_keywords import fetch_google_keywords
except Exception:
    fetch_google_keywords = None

try:
    from research.google_trends import fetch_google_trends
except Exception:
    fetch_google_trends = None

try:
    from research.meta_ad_library import fetch_meta_ads
except Exception:
    fetch_meta_ads = None

try:
    from research.tiktok_trends import fetch_tiktok_trends
except Exception:
    fetch_tiktok_trends = None

try:
    from research.youtube_trends import fetch_youtube_trends
except Exception:
    fetch_youtube_trends = None


def render():
    st.header("🔎 Market Research")

    # -------------------------
    # SESSION STATE SAFETY
    # -------------------------
    if "research_results" not in st.session_state:
        st.session_state.research_results = {}

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
    # RUN RESEARCH (SAFE)
    # -------------------------
    if submitted and keyword:
        results = {}

        with st.spinner("Collecting research data..."):
            if "Google Search" in platforms and fetch_google_keywords:
                try:
                    results["Google Keywords"] = fetch_google_keywords(keyword, country)
                except Exception as e:
                    results["Google Keywords"] = {"error": str(e)}

            if "Google Trends" in platforms and fetch_google_trends:
                try:
                    results["Google Trends"] = fetch_google_trends(keyword, country)
                except Exception as e:
                    results["Google Trends"] = {"error": str(e)}

            if "Meta Ads" in platforms and fetch_meta_ads:
                try:
                    results["Meta Ads"] = fetch_meta_ads(keyword)
                except Exception as e:
                    results["Meta Ads"] = {"error": str(e)}

            if "TikTok" in platforms and fetch_tiktok_trends:
                try:
                    results["TikTok Trends"] = fetch_tiktok_trends(keyword)
                except Exception as e:
                    results["TikTok Trends"] = {"error": str(e)}

            if "YouTube" in platforms and fetch_youtube_trends:
                try:
                    results["YouTube Trends"] = fetch_youtube_trends(keyword)
                except Exception as e:
                    results["YouTube Trends"] = {"error": str(e)}

        st.session_state.research_results = results

    # -------------------------
    # DISPLAY RESULTS
    # -------------------------
    if st.session_state.research_results:
        st.subheader("📊 Research Results")

        for source, data in st.session_state.research_results.items():
            st.markdown(f"### {source}")

            if isinstance(data, dict) and "error" in data:
                st.error(data["error"])
            elif isinstance(data, pd.DataFrame):
                st.dataframe(data, use_container_width=True)
            elif isinstance(data, list):
                st.dataframe(pd.DataFrame(data), use_container_width=True)
            else:
                st.json(data)

    # -------------------------
    # SUMMARY
    # -------------------------
    if st.session_state.research_results:
        st.subheader("🧠 Research Summary")
        st.info(
            "This data feeds Campaigns, Strategy, and Creative optimization automatically."
        )