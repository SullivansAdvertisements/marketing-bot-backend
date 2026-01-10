# ============================================================
# SULLIVAN’S ADVERTISING — STREAMLIT APP (HARDENED)
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
DEFAULT_STATE = {
    "research_data": None,
}

for k, v in DEFAULT_STATE.items():
    st.session_state.setdefault(k, v)

# ============================================================
# SAFE / LAZY IMPORT HELPERS
# ============================================================

def safe_import(path: str, name: str):
    """
    Import a symbol lazily and safely.
    Returns (callable, error_message)
    """
    try:
        module = __import__(path, fromlist=[name])
        return getattr(module, name), None
    except Exception as e:
        return None, str(e)

# ============================================================
# HEADER
# ============================================================
st.title("🚀 Sullivan’s Advertising Intelligence")
st.caption("Research → Validation → Campaign Execution")

# ============================================================
# SIDEBAR NAV
# ============================================================
with st.sidebar:
    tab = st.radio(
        "Navigation",
        ["Research", "Campaigns"],
        index=0,
    )

# ============================================================
# ======================= RESEARCH TAB =======================
# ============================================================
if tab == "Research":

    st.subheader("🔍 Research")

    niche = st.text_input("Niche")
    keyword = st.text_input("Primary Keyword")

    if st.button("Run Research"):
        if not niche or not keyword:
            st.warning("Niche and keyword required")
            st.stop()

        research_data = {
            "niche": niche,
            "platforms": ["google", "meta", "youtube", "tiktok"],
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
            research_data["keywords"] = fetch_google_keywords(keyword)
            research_data["sources"]["google_keywords"] = "Google Ads API"
        else:
            st.warning(f"Google Keywords unavailable: {err}")

        # ---------------- GOOGLE TRENDS ----------------
        fetch_google_trends, err = safe_import(
            "research.google_trends", "fetch_google_trends"
        )
        if fetch_google_trends:
            research_data["search_trends"] = fetch_google_trends(keyword)
            research_data["sources"]["google_trends"] = "Google Trends"
        else:
            st.warning(f"Google Trends unavailable: {err}")

        # ---------------- YOUTUBE TRENDS ----------------
        fetch_youtube_trends, err = safe_import(
            "research.youtube_trends", "fetch_youtube_trends"
        )
        if fetch_youtube_trends:
            research_data["content_trends"] += fetch_youtube_trends(keyword)
            research_data["sources"]["youtube"] = "YouTube Data API"
        else:
            st.warning(f"YouTube Trends unavailable: {err}")

        # ---------------- TIKTOK TRENDS ----------------
        fetch_tiktok_trends, err = safe_import(
            "research.tiktok_trends", "fetch_tiktok_trends"
        )
        if fetch_tiktok_trends:
            research_data["content_trends"] += fetch_tiktok_trends(keyword)
            research_data["sources"]["tiktok"] = "TikTok Trends"
        else:
            st.warning(f"TikTok Trends unavailable: {err}")

        # ---------------- META AD LIBRARY ----------------
        fetch_meta_ads, err = safe_import(
            "research.meta_ad_library", "fetch_meta_ads"
        )
        if fetch_meta_ads:
            research_data["ad_intel"] = fetch_meta_ads(keyword)
            research_data["sources"]["meta"] = "Meta Ad Library"
        else:
            st.warning(f"Meta Ad Library unavailable: {err}")

        st.session_state.research_data = research_data
        st.success("Research complete")

    # ---------------- DISPLAY ----------------
    if st.session_state.research_data:
        st.divider()
        st.subheader("📊 Research Results")

        if st.session_state.research_data["keywords"]:
            st.markdown("**Google Keywords**")
            st.dataframe(
                pd.DataFrame(st.session_state.research_data["keywords"]),
                use_container_width=True,
            )

        if st.session_state.research_data["search_trends"]:
            st.markdown("**Google Trends**")
            st.dataframe(
                pd.DataFrame(st.session_state.research_data["search_trends"]),
                use_container_width=True,
            )

        if st.session_state.research_data["content_trends"]:
            st.markdown("**Content Trends (YouTube / TikTok)**")
            st.dataframe(
                pd.DataFrame(st.session_state.research_data["content_trends"]),
                use_container_width=True,
            )

        if st.session_state.research_data["ad_intel"]:
            st.markdown("**Meta Ad Library**")
            st.dataframe(
                pd.DataFrame(st.session_state.research_data["ad_intel"]),
                use_container_width=True,
            )

# ============================================================
# ====================== CAMPAIGNS TAB =======================
# ============================================================
if tab == "Campaigns":

    st.subheader("🎯 Campaigns")

    if not st.session_state.research_data:
        st.info("Run research first to unlock campaigns")
        st.stop()

    campaigns_render, err = safe_import(
        "campaigns.router", "render"
    )

    if not campaigns_render:
        st.error(
            "Campaigns module unavailable.\n\n"
            "This usually means a required SDK (Google Ads / Meta) "
            "is not installed.\n\n"
            f"Error: {err}"
        )
        st.stop()

    campaigns_render()