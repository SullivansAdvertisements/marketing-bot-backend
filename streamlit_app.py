# ============================================================
# SULLIVAN’S ADVERTISING — STREAMLIT APP (FULL PIPELINE)
# ============================================================

import streamlit as st
import pandas as pd

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Sullivan’s Advertising Intelligence",
    page_icon="🎯",
    layout="wide",
)

# ============================================================
# SESSION STATE
# ============================================================
st.session_state.setdefault("research_data", None)

# ============================================================
# SAFE / LAZY IMPORT
# ============================================================
def safe_import(module_path: str, symbol: str):
    try:
        module = __import__(module_path, fromlist=[symbol])
        return getattr(module, symbol), None
    except Exception as e:
        return None, str(e)

# ============================================================
# IMPORT RESEARCH PIPELINE (SAFE)
# ============================================================
validate_research_data, _ = safe_import(
    "research_data.validators", "validate_research_data"
)

normalize_google_keyword, _ = safe_import(
    "research_data.normalizers", "normalize_google_keyword"
)
normalize_google_trend, _ = safe_import(
    "research_data.normalizers", "normalize_google_trend"
)
normalize_youtube_trend, _ = safe_import(
    "research_data.normalizers", "normalize_youtube_trend"
)
normalize_tiktok_trend, _ = safe_import(
    "research_data.normalizers", "normalize_tiktok_trend"
)
normalize_meta_ad, _ = safe_import(
    "research_data.normalizers", "normalize_meta_ad"
)

export_keywords_df, _ = safe_import(
    "research_data.exporters", "export_keywords_df"
)
export_search_trends_df, _ = safe_import(
    "research_data.exporters", "export_search_trends_df"
)
export_content_trends_df, _ = safe_import(
    "research_data.exporters", "export_content_trends_df"
)
export_ad_intel_df, _ = safe_import(
    "research_data.exporters", "export_ad_intel_df"
)

export_top_keywords, _ = safe_import(
    "research_data.exporters", "export_top_keywords"
)
export_content_hooks, _ = safe_import(
    "research_data.exporters", "export_content_hooks"
)
export_competitor_angles, _ = safe_import(
    "research_data.exporters", "export_competitor_angles"
)

# ============================================================
# HEADER
# ============================================================
st.title("🚀 Sullivan’s Advertising Intelligence")
st.caption("Research → Contracts → Campaign Execution")

# ============================================================
# SIDEBAR
# ============================================================
tab = st.sidebar.radio("Navigation", ["Research", "Campaigns"])

# ============================================================
# ======================= RESEARCH TAB =======================
# ============================================================
if tab == "Research":

    st.subheader("🔍 Advanced Market Research")

    niche = st.text_input("Niche", placeholder="e.g. luxury streetwear")
    keyword = st.text_input("Primary Keyword", placeholder="e.g. designer hoodies")

    if st.button("Run Research"):
        if not niche or not keyword:
            st.warning("Both fields required")
            st.stop()

        research_data = {
            "niche": niche,
            "platforms": ["google", "youtube", "tiktok", "meta"],
            "keywords": [],
            "search_trends": [],
            "content_trends": [],
            "ad_intel": [],
            "audiences": {},
            "funnels": {},
            "angles": {},
            "budget_guidance": {},
            "sources": {},
        }

        # ---------------- GOOGLE KEYWORDS ----------------
        fetch_google_keywords, err = safe_import(
            "research.google_keywords", "fetch_google_keywords"
        )
        if fetch_google_keywords:
            for row in fetch_google_keywords(niche):
                research_data["keywords"].append(
                    normalize_google_keyword(row)
                )
            research_data["sources"]["google_keywords"] = "google_ads"

        # ---------------- GOOGLE TRENDS ----------------
        fetch_google_trends, err = safe_import(
            "research.google_trends", "fetch_google_trends"
        )
        if fetch_google_trends:
            trends = fetch_google_trends(keyword, "Global")
            if isinstance(trends, dict) and "Google Trends" in trends:
                df = trends["Google Trends"]
                if isinstance(df, pd.DataFrame):
                    for _, r in df.iterrows():
                        research_data["search_trends"].append(
                            normalize_google_trend(
                                keyword, r[keyword], "12m"
                            )
                        )
            research_data["sources"]["google_trends"] = "google_trends"

        # ---------------- YOUTUBE TRENDS ----------------
fetch_youtube_trends, err = safe_import(
    "research.youtube_trends", "fetch_youtube_trends"
)

if fetch_youtube_trends:
    try:
        yt_results = fetch_youtube_trends(keyword)
        for item in yt_results:
            research_data["content_trends"].append(
                normalize_youtube_trend(item)
            )
        research_data["sources"]["youtube"] = "youtube_api"

    except RuntimeError as e:
        st.warning(f"YouTube disabled: {e}")

    except Exception as e:
        st.warning(f"YouTube error: {e}")

else:
    st.warning(f"YouTube Trends unavailable: {err}")
        # ---------------- TIKTOK TRENDS ----------------
        fetch_tiktok_trends, err = safe_import(
            "research.tiktok_trends", "fetch_tiktok_trends"
        )
        if fetch_tiktok_trends:
            data = fetch_tiktok_trends(keyword)
            if isinstance(data, list):
                for item in data:
                    research_data["content_trends"].append(
                        normalize_tiktok_trend(item)
                    )
            research_data["sources"]["tiktok"] = "tiktok_api"

        # ---------------- META AD LIBRARY ----------------
        fetch_meta_ads, err = safe_import(
            "research.meta_ad_library", "fetch_meta_ads"
        )
        if fetch_meta_ads:
            for ad in fetch_meta_ads(keyword):
                research_data["ad_intel"].append(
                    normalize_meta_ad(ad)
                )
            research_data["sources"]["meta"] = "meta_ad_library"

        # ---------------- VALIDATE ----------------
        if validate_research_data:
            validate_research_data(research_data)

        st.session_state.research_data = research_data
        st.success("Research validated and stored")

    # ---------------- DISPLAY ----------------
    if st.session_state.research_data:
        st.divider()
        st.subheader("📊 Research Outputs")

        st.markdown("### 🔑 Top Keywords")
        st.dataframe(export_keywords_df(st.session_state.research_data))

        st.markdown("### 📈 Search Trends")
        st.dataframe(export_search_trends_df(st.session_state.research_data))

        st.markdown("### 🎬 Content Trends")
        st.dataframe(export_content_trends_df(st.session_state.research_data))

        st.markdown("### 🧠 Competitor Ads")
        st.dataframe(export_ad_intel_df(st.session_state.research_data))

# ============================================================
# ====================== CAMPAIGNS TAB =======================
# ============================================================
if tab == "Campaigns":

    st.subheader("🎯 Campaign Intelligence")

    if not st.session_state.research_data:
        st.info("Run research first")
        st.stop()

    st.markdown("### 🔥 Best Keywords to Target")
    st.write(export_top_keywords(st.session_state.research_data))

    st.markdown("### 🎯 High-Performing Content Hooks")
    st.write(export_content_hooks(st.session_state.research_data))

    st.markdown("### ⚔️ Competitor Messaging Angles")
    st.write(export_competitor_angles(st.session_state.research_data))

    campaigns_render, err = safe_import(
        "campaigns.router", "render"
    )

    if campaigns_render:
        st.divider()
        campaigns_render()
    else:
        st.warning("Campaign execution modules not installed")