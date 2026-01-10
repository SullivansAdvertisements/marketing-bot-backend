# ============================================================
# SULLIVAN’S ADVERTISING – ENTERPRISE STREAMLIT APP
# ============================================================

import streamlit as st
import pandas as pd

# ============================================================
# UTILS (GLOBAL GUARDRAILS)
# ============================================================
from utils import (
    get_logger,
    rate_limit,
    validate_budget,
    validate_age_range,
    validate_countries,
)

logger = get_logger("streamlit_app")

# ============================================================
# RESEARCH
# ============================================================
from research.google_keywords import fetch_google_keywords
from research.google_trends import fetch_google_trends
from research.youtube_trends import fetch_youtube_trends
from research.tiktok_trends import fetch_tiktok_trends
from research.meta_ad_library import fetch_meta_ads

# ============================================================
# RESEARCH DATA CONTRACT (MANDATORY)
# ============================================================
from research_data import (
    validate_research_data,
    export_keywords_df,
)

# ============================================================
# CREATIVE
# ============================================================
from creative.router import generate_creatives

# ============================================================
# INTEGRATIONS
# ============================================================
from integrations.meta_ads import (
    build_meta_targeting,
    fetch_meta_audience_insights,
)

# ============================================================
# CAMPAIGNS UI
# ============================================================
from campaigns.router import render as campaigns_render

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Sullivan’s Advertising AI",
    page_icon="🎯",
    layout="wide",
)

# ============================================================
# SESSION STATE
# ============================================================
DEFAULT_STATE = {
    "validated_research": None,
    "meta_insights": None,
    "creatives": None,
}

for k, v in DEFAULT_STATE.items():
    st.session_state.setdefault(k, v)

# ============================================================
# SIDEBAR INPUTS
# ============================================================
with st.sidebar:
    st.header("⚙️ Campaign Inputs")

    niche = st.text_input("Niche")
    product = st.text_input("Product / Offer")
    keyword = st.text_input("Primary Keyword")

    countries = st.multiselect("Target Countries", ["US"], default=["US"])
    age_min, age_max = st.slider("Age Range", 18, 65, (18, 44))
    daily_budget = st.number_input("Daily Budget ($)", min_value=1.0, value=20.0)

    st.divider()

    run_research = st.button("🔍 Run Research")
    generate_ads = st.button("🎨 Generate Creatives")

# ============================================================
# MAIN HEADER
# ============================================================
st.title("🚀 Sullivan’s Advertising Intelligence")
st.caption("Validated Research → Creative → Campaign Execution")

# ============================================================
# VALIDATION (USER INPUT)
# ============================================================
try:
    validate_countries(countries)
    validate_age_range(age_min, age_max)
    validate_budget(daily_budget)
except ValueError as e:
    st.error(str(e))
    st.stop()

# ============================================================
# RESEARCH PIPELINE
# ============================================================
if run_research:
    if not niche or not keyword:
        st.error("Niche and keyword are required")
        st.stop()

    try:
        rate_limit("research", max_calls=5, window_seconds=60)

        with st.spinner("Fetching real platform data…"):
            research_data = {
                "niche": niche,
                "platforms": ["google", "meta", "youtube", "tiktok"],
                "keywords": fetch_google_keywords(keyword),
                "audiences": {
                    "meta": fetch_meta_ads(keyword),
                },
                "funnels": {},
                "angles": {},
                "budget_guidance": {
                    "daily_budget": daily_budget
                },
                "sources": {
                    "google_trends": fetch_google_trends(keyword, "US"),
                    "youtube": fetch_youtube_trends(keyword),
                    "tiktok": fetch_tiktok_trends(keyword),
                },
            }

            # 🔒 HARD CONTRACT ENFORCEMENT
            validate_research_data(research_data)

            st.session_state.validated_research = research_data
            logger.info("Research validated successfully")

        st.success("Research validated and locked")

    except Exception as e:
        logger.exception(e)
        st.error(str(e))
        st.stop()

# ============================================================
# SHOW VALIDATED RESEARCH
# ============================================================
if st.session_state.validated_research:
    st.subheader("📊 Validated Research")

    with st.expander("🔑 Keywords"):
        df = export_keywords_df(st.session_state.validated_research)
        st.dataframe(df, use_container_width=True)

    with st.expander("📡 Sources"):
        st.json(st.session_state.validated_research["sources"])

# ============================================================
# META AUDIENCE INSIGHTS
# ============================================================
if st.session_state.validated_research:
    st.subheader("🎯 Meta Audience Estimates")

    targeting = build_meta_targeting(
        countries=countries,
        age_min=age_min,
        age_max=age_max,
        interests=[keyword],
    )

    try:
        rate_limit("meta_insights", max_calls=5, window_seconds=60)
        insights = fetch_meta_audience_insights(targeting)
        st.session_state.meta_insights = insights
        st.json(insights)
    except Exception as e:
        st.warning(str(e))

# ============================================================
# CREATIVE GENERATION
# ============================================================
if generate_ads:
    if not product or not st.session_state.validated_research:
        st.error("Validated research and product required")
        st.stop()

    with st.spinner("Generating ranked creatives…"):
        creatives = generate_creatives(
            product=product,
            goal="Conversions",
            platform="Meta",
            research_bundle={
                **st.session_state.validated_research,
                "meta_audience": st.session_state.meta_insights,
            },
        )

        st.session_state.creatives = creatives

# ============================================================
# SHOW CREATIVES
# ============================================================
if st.session_state.creatives:
    st.subheader("🏆 Creative Rankings")

    df = pd.DataFrame([
        {
            "Angle": c["angle"],
            "Score": c["score"],
            "Headlines": " | ".join(c["headlines"]),
            "Primary Text": " | ".join(c["primary_texts"]),
            "CTA": c["cta"],
        }
        for c in st.session_state.creatives
    ]).sort_values("Score", ascending=False)

    st.dataframe(df, use_container_width=True)

# ============================================================
# CAMPAIGN MANAGEMENT (FULL UI)
# ============================================================
if st.session_state.validated_research:
    st.divider()
    campaigns_render()
else:
    st.info("Run validated research to unlock campaign management")