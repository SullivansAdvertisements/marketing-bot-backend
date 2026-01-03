# research/router.py
import streamlit as st
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# -------------------------------------------------
# SAFE IMPORTS (no execution at import time)
# -------------------------------------------------
def _safe_import():
    modules = {}

    try:
        from research.google_keywords import fetch_google_keywords
        modules["google_keywords"] = fetch_google_keywords
    except Exception:
        modules["google_keywords"] = None

    try:
        from research.google_trends import fetch_google_trends
        modules["google_trends"] = fetch_google_trends
    except Exception:
        modules["google_trends"] = None

    try:
        from research.meta_ad_library import fetch_meta_ads
        modules["meta_ads"] = fetch_meta_ads
    except Exception:
        modules["meta_ads"] = None

    try:
        from research.tiktok_trends import fetch_tiktok_trends
        modules["tiktok"] = fetch_tiktok_trends
    except Exception:
        modules["tiktok"] = None

    try:
        from research.youtube_trends import fetch_youtube_trends
        modules["youtube"] = fetch_youtube_trends
    except Exception:
        modules["youtube"] = None

    return modules


# -------------------------------------------------
# KEY STATUS
# -------------------------------------------------
def _key_status():
    return {
        "Google Ads": bool(os.getenv("GOOGLE_ADS_API_KEY") or st.secrets.get("GOOGLE_ADS_API_KEY")),
        "Meta Ads": bool(os.getenv("META_ACCESS_TOKEN") or st.secrets.get("META_ACCESS_TOKEN")),
        "TikTok": bool(os.getenv("TIKTOK_API_KEY") or st.secrets.get("TIKTOK_API_KEY")),
        "YouTube": bool(os.getenv("YOUTUBE_API_KEY") or st.secrets.get("YOUTUBE_API_KEY")),
    }


# -------------------------------------------------
# MAIN RENDER
# -------------------------------------------------
def render():
    st.header("🔎 Advanced Market Research Engine")

    modules = _safe_import()
    keys = _key_status()

    # -------------------------
    # SESSION STATE
    # -------------------------
    if "research_results" not in st.session_state:
        st.session_state.research_results = {}

    # -------------------------
    # API STATUS
    # -------------------------
    with st.expander("🔐 API Connection Status"):
        for k, v in keys.items():
            st.success(f"{k} connected") if v else st.warning(f"{k} not connected")

    # -------------------------
    # INPUTS
    # -------------------------
    with st.form("research_form"):
        keyword = st.text_input(
            "Primary Keyword / Market Topic",
            placeholder="e.g. luxury streetwear hoodies",
        )

        country = st.selectbox(
            "Target Country",
            ["US", "CA", "UK", "AU", "Global"],
            index=0,
        )

        platforms = st.multiselect(
            "Platforms to Analyze",
            [
                "Google Keywords",
                "Google Trends",
                "Meta Ads Library",
                "TikTok Trends",
                "YouTube Trends",
            ],
            default=[
                "Google Keywords",
                "Google Trends",
                "Meta Ads Library",
            ],
        )

        run = st.form_submit_button("🚀 Run Full Market Scan")

    if not run or not keyword:
        return

    # -------------------------
    # EXECUTION (PARALLEL)
    # -------------------------
    results = {}

    with st.spinner("Running deep market intelligence scan…"):
        with ThreadPoolExecutor(max_workers=5) as executor:
            tasks = []

            if "Google Keywords" in platforms and modules["google_keywords"]:
                tasks.append(executor.submit(modules["google_keywords"], keyword, country))

            if "Google Trends" in platforms and modules["google_trends"]:
                tasks.append(executor.submit(modules["google_trends"], keyword, country))

            if "Meta Ads Library" in platforms and modules["meta_ads"]:
                tasks.append(executor.submit(modules["meta_ads"], keyword))

            if "TikTok Trends" in platforms and modules["tiktok"]:
                tasks.append(executor.submit(modules["tiktok"], keyword))

            if "YouTube Trends" in platforms and modules["youtube"]:
                tasks.append(executor.submit(modules["youtube"], keyword))

            if not tasks:
                st.warning("No platforms available to run research.")
                return

            for future in as_completed(tasks):
                try:
                    data = future.result()

                    if not data:
                        continue

                    if isinstance(data, dict):
                        results.update(data)

                    elif isinstance(data, pd.DataFrame) and not data.empty:
                        results[f"Table {len(results)+1}"] = data

                except Exception as e:
                    results[f"Error {len(results)+1}"] = {"error": str(e)}

    # -------------------------
    # RESULTS
    # -------------------------
    if not results:
        st.warning("No data returned.")
        return

    st.session_state.research_results = results

    st.subheader("📊 Platform Intelligence")

    tabs = st.tabs(list(results.keys()))

    for tab, (source, data) in zip(tabs, results.items()):
        with tab:
            if isinstance(data, dict) and "error" in data:
                st.error(data["error"])
            elif isinstance(data, pd.DataFrame):
                st.dataframe(data, use_container_width=True)
            else:
                st.json(data)

    # -------------------------
    # CROSS-PLATFORM INSIGHTS
    # -------------------------
    st.subheader("🧠 Cross-Platform Insights")

    st.markdown(
        """
        **What this data unlocks:**
        - Keyword intent vs creative saturation
        - Platform demand alignment
        - Early trend detection
        - Budget & creative prioritization
        """
    )

    st.success("Research is now ready for Creative, Campaigns & Strategy.")