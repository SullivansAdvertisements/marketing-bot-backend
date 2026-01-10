# ============================================================
# SULLIVAN’S ADVERTISING — STREAMLIT APP (LOCATION-ENABLED)
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
# SAFE IMPORT
# ============================================================
def safe_import(module_path: str, symbol: str):
    try:
        module = __import__(module_path, fromlist=[symbol])
        return getattr(module, symbol), None
    except Exception as e:
        return None, str(e)

# ============================================================
# PIPELINE IMPORTS
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
normalize_location, _ = safe_import(
    "research_data.normalizers", "normalize_location"
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

# ============================================================
# HEADER
# ============================================================
st.title("🚀 Sullivan’s Advertising Intelligence")
st.caption("Research → Validation → Campaign Execution")

# ============================================================
# SIDEBAR
# ============================================================
tab = st.sidebar.radio("Navigation", ["Research", "Campaigns"])

# ============================================================
# ======================= RESEARCH TAB =======================
# ============================================================
if tab == "Research":

    st.subheader("🔍 Advanced Market Research")

    niche = st.text_input("Niche", placeholder="e.g. Music")
    keyword = st.text_input("Primary Keyword", placeholder="e.g. Lil Baby")

    if st.button("Run Research"):
        if not niche or not keyword:
            st.warning("Both fields are required")
            st.stop()

        research_data = {
            "niche": niche,
            "platforms": ["google", "youtube", "tiktok", "meta"],
            "keywords": [],
            "search_trends": [],
            "content_trends": [],
            "ad_intel": [],
            "locations": [],
            "audiences": {},
            "funnels": {},
            "angles": {},
            "budget_guidance": {},
            "sources": {},
        }

        # ---------------- GOOGLE KEYWORDS ----------------
        fetch_google_keywords, _ = safe_import(
            "research.google_keywords", "fetch_google_keywords"
        )
        if fetch_google_keywords:
            for row in fetch_google_keywords(niche):
                research_data["keywords"].append(
                    normalize_google_keyword(row)
                )
            research_data["sources"]["google_keywords"] = "google_ads"

        # ---------------- GOOGLE TRENDS ----------------
        fetch_google_trends, _ = safe_import(
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

        # ---------------- GOOGLE TREND LOCATIONS ----------------
        fetch_google_trend_locations, _ = safe_import(
            "research.google_trends", "fetch_google_trends_locations"
        )
        if fetch_google_trend_locations and normalize_location:
            for row in fetch_google_trend_locations(keyword):
                research_data["locations"].append(
                    normalize_location(
                        platform="google",
                        location=row["location"],
                        metric="interest",
                        value=row["value"],
                        source="google_trends",
                    )
                )

        # ---------------- YOUTUBE TRENDS ----------------
        fetch_youtube_trends, _ = safe_import(
            "research.youtube_trends", "fetch_youtube_trends"
        )
        if fetch_youtube_trends:
            try:
                for item in fetch_youtube_trends(keyword):
                    research_data["content_trends"].append(
                        normalize_youtube_trend(item)
                    )
                research_data["sources"]["youtube"] = "youtube_api"
            except Exception as e:
                st.warning(f"YouTube disabled: {e}")

        # ---------------- TIKTOK TRENDS ----------------
        fetch_tiktok_trends, _ = safe_import(
            "research.tiktok_trends", "fetch_tiktok_trends"
        )
        if fetch_tiktok_trends:
            try:
                data = fetch_tiktok_trends(keyword)
                if isinstance(data, list):
                    for item in data:
                        research_data["content_trends"].append(
                            normalize_tiktok_trend(item)
                        )
                        if item.get("region_code"):
                            research_data["locations"].append(
                                normalize_location(
                                    platform="tiktok",
                                    location=item["region_code"],
                                    metric="videos",
                                    value=1,
                                    source="tiktok_api",
                                )
                            )
                research_data["sources"]["tiktok"] = "tiktok_api"
            except Exception as e:
                st.warning(f"TikTok error: {e}")

        # ---------------- META AD LIBRARY ----------------
        fetch_meta_ads, _ = safe_import(
            "research.meta_ad_library", "fetch_meta_ads"
        )
        if fetch_meta_ads:
            try:
                for ad in fetch_meta_ads(keyword):
                    research_data["ad_intel"].append(
                        normalize_meta_ad(ad)
                    )
                    for loc in ad.get("locations", []):
                        research_data["locations"].append(
                            normalize_location(
                                platform="meta",
                                location=loc,
                                metric="ads",
                                value=1,
                                source="meta_ad_library",
                            )
                        )
                research_data["sources"]["meta"] = "meta_ad_library"
            except Exception as e:
                st.warning(f"Meta error: {e}")

        # ---------------- VALIDATE ----------------
        if validate_research_data:
            validate_research_data(research_data)

        st.session_state.research_data = research_data
        st.success("Research validated and stored")

    # ---------------- DISPLAY ----------------
    if st.session_state.research_data:
        st.divider()
        st.subheader("📊 Research Outputs")

        st.markdown("### 🔑 Keywords")
        st.dataframe(export_keywords_df(st.session_state.research_data))

        st.markdown("### 📈 Search Trends")
        st.dataframe(export_search_trends_df(st.session_state.research_data))

        st.markdown("### 🎬 Content Trends")
        st.dataframe(export_content_trends_df(st.session_state.research_data))

        st.markdown("### 🧠 Competitor Ads")
        st.dataframe(export_ad_intel_df(st.session_state.research_data))

        if st.session_state.research_data.get("locations"):
            st.markdown("### 🌍 Location Demand (All Platforms)")
            st.dataframe(
                pd.DataFrame(st.session_state.research_data["locations"]),
                use_container_width=True,
            )

# ============================================================
# ====================== CAMPAIGNS TAB =======================
# ============================================================
if tab == "Campaigns":
    st.subheader("🎯 Campaign Builder")
    if not st.session_state.research_data:
        st.info("Run research first")
        st.stop()

    st.json(st.session_state.research_data, expanded=False)