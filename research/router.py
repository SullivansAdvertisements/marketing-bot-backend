# research/router.py
import streamlit as st
import pandas as pd
import os
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

# -------------------------------------------------
# SAFE IMPORTS (NO EXECUTION AT IMPORT TIME)
# -------------------------------------------------
def _safe_import():
    modules = {}

    def _try(name, fn):
        try:
            modules[name] = fn
        except Exception:
            modules[name] = None

    try:
        from research.google_keywords import fetch_google_keywords
        _try("google_keywords", fetch_google_keywords)
    except Exception:
        modules["google_keywords"] = None

    try:
        from research.google_trends import fetch_google_trends
        _try("google_trends", fetch_google_trends)
    except Exception:
        modules["google_trends"] = None

    try:
        from research.meta_ad_library import fetch_meta_ads
        _try("meta_ads", fetch_meta_ads)
    except Exception:
        modules["meta_ads"] = None

    try:
        from research.tiktok_trends import fetch_tiktok_trends
        _try("tiktok", fetch_tiktok_trends)
    except Exception:
        modules["tiktok"] = None

    try:
        from research.youtube_trends import fetch_youtube_trends
        _try("youtube", fetch_youtube_trends)
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
# NORMALIZER (NO LIMITS)
# -------------------------------------------------
def normalize_result(data, source):
    """
    Accepts ANY return type and converts it into
    a safe, renderable structure without indexing.
    """
    if data is None:
        return None

    if isinstance(data, pd.DataFrame):
        return {"type": "table", "source": source, "data": data}

    if isinstance(data, list):
        return {"type": "list", "source": source, "data": data}

    if isinstance(data, dict):
        return {"type": "json", "source": source, "data": data}

    return {"type": "raw", "source": source, "data": str(data)}


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
    st.session_state.setdefault("research_results", {})
    st.session_state.setdefault("research_bundle", {})

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
    # EXECUTION (UNLIMITED)
    # -------------------------
    results = {}
    research_bundle = {}

    with st.spinner("Running unlimited market intelligence scan…"):
        with ThreadPoolExecutor(max_workers=len(platforms) or 1) as executor:
            futures = {}

            def submit(name, fn, *args):
                if fn:
                    futures[executor.submit(fn, *args)] = name

            submit("Google Keywords", modules["google_keywords"], keyword, country)
            submit("Google Trends", modules["google_trends"], keyword, country)
            submit("Meta Ads Library", modules["meta_ads"], keyword)
            submit("TikTok Trends", modules["tiktok"], keyword)
            submit("YouTube Trends", modules["youtube"], keyword)

            for future in as_completed(futures):
                source = futures[future]
                try:
                    raw = future.result()
                    normalized = normalize_result(raw, source)

                    if normalized:
                        key = f"{source} · {uuid.uuid4().hex[:6]}"
                        results[key] = normalized
                        research_bundle[source] = raw

                except Exception as e:
                    results[f"{source} · ERROR"] = {
                        "type": "error",
                        "source": source,
                        "data": str(e),
                    }

    if not results:
        st.warning("No data returned.")
        return

    # -------------------------
    # STORE FOR OTHER TABS
    # -------------------------
    st.session_state.research_results = results
    st.session_state.research_bundle = research_bundle

    # -------------------------
    # DISPLAY RESULTS (NO INDEXING)
    # -------------------------
    st.subheader("📊 Platform Intelligence")

    tabs = st.tabs(list(results.keys()))

    for tab, (_, payload) in zip(tabs, results.items()):
        with tab:
            if payload["type"] == "table":
                st.dataframe(payload["data"], use_container_width=True)

            elif payload["type"] == "json":
                st.json(payload["data"])

            elif payload["type"] == "list":
                st.json(payload["data"])

            elif payload["type"] == "error":
                st.error(payload["data"])

            else:
                st.write(payload["data"])

    # -------------------------
    # INSIGHTS
    # -------------------------
    st.subheader("🧠 Cross-Platform Insights")

    st.markdown(
        """
        **What this unlocks:**
        - Unlimited keyword & trend depth  
        - Full creative saturation analysis  
        - Platform demand alignment  
        - Campaign + Creative intelligence reuse  
        """
    )

    st.success("Research fully unlocked for Creative, Campaigns & Strategy.")