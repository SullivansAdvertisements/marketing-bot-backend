#import os
import streamlit as st
import pandas as pd

# ---------------------------------
# PAGE CONFIG (MOBILE FIRST)
# ---------------------------------
st.set_page_config(
    page_title="Marketing Bot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("🚀 Marketing Bot")

# ---------------------------------
# SAFE ENV ACCESS
# ---------------------------------
def env(key):
    return os.getenv(key) or st.secrets.get(key, None)


# ---------------------------------
# PLATFORM KEY STATUS
# ---------------------------------
KEYS = {
    "Meta Access Token": env("META_ACCESS_TOKEN"),
    "Meta Ad Account ID": env("META_AD_ACCOUNT_ID"),
    "Google Developer Token": env("GOOGLE_DEVELOPER_TOKEN"),
    "Google Refresh Token": env("GOOGLE_REFRESH_TOKEN"),
    "OpenAI API Key": env("OPENAI_API_KEY"),
}

# ---------------------------------
# TABS (MOBILE FRIENDLY)
# ---------------------------------
tabs = st.tabs([
    "🔐 Status",
    "🔎 Research",
    "🎨 Creative",
    "📣 Campaigns",
])

# =================================
# TAB 1 — STATUS
# =================================
with tabs[0]:
    st.subheader("🔐 API Connection Status")

    rows = []
    for name, value in KEYS.items():
        rows.append({
            "Service": name,
            "Status": "✅ Connected" if value else "❌ Not Connected"
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    st.info(
        "The app continues to work even if some keys are missing. "
        "Only features that depend on missing keys will be disabled."
    )

# =================================
# TAB 2 — RESEARCH (SAFE)
# =================================
with tab_research:
    st.header("🔎 Advanced Market Research")

    # -----------------------------
    # SAFE IMPORTS (NO app. PREFIX)
    # -----------------------------
    from research.google_keywords import fetch_google_keywords
    from research.google_trends import fetch_google_trends
    from research.meta_ad_library import fetch_meta_ads
    from research.youtube_trends import fetch_youtube_trends
    from research.tiktok_trends import fetch_tiktok_trends

    # -----------------------------
    # SHARED INPUTS
    # -----------------------------
    keyword = st.text_input(
        "Primary Keyword / Topic",
        placeholder="e.g. streetwear hoodies",
        key="research_keyword",
    )

    country = st.selectbox(
        "Country",
        ["US", "CA", "UK", "AU", "Global"],
        key="research_country",
    )

    run_research = st.button("🚀 Run Full Research")

    if not keyword:
        st.info("Enter a keyword to unlock research.")
        st.stop()

    # -----------------------------
    # PLATFORM TABS (NEW)
    # -----------------------------
    r_tabs = st.tabs([
        "🔍 Google Search",
        "📈 Google Trends",
        "📣 Meta Ads",
        "🎥 YouTube",
        "🎵 TikTok",
    ])

    # =============================
    # GOOGLE SEARCH (KEYWORDS)
    # =============================
    with r_tabs[0]:
        st.subheader("Google Search Demand & CPC")

        if run_research:
            try:
                data = fetch_google_keywords(
                    seed_keyword=keyword,
                    geo_target_id="2840",  # US
                    language_id="1000",
                )

                if not data:
                    st.warning("No keyword data returned.")
                else:
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)

                    with st.expander("Raw Keyword Data"):
                        st.json(data)

            except Exception as e:
                st.error("Google Keywords failed")
                st.exception(e)

    # =============================
    # GOOGLE TRENDS
    # =============================
    with r_tabs[1]:
        st.subheader("Trend Velocity & Seasonality")

        if run_research:
            try:
                data = fetch_google_trends(keyword, geo=country)

                if not data:
                    st.warning("No trends data.")
                else:
                    st.json(data)

            except Exception as e:
                st.error("Google Trends failed")
                st.exception(e)

    # =============================
    # META ADS LIBRARY
    # =============================
    with r_tabs[2]:
        st.subheader("Active Competitor Ads")

        if run_research:
            try:
                ads = fetch_meta_ads(keyword)

                if not ads:
                    st.warning("No active ads found.")
                else:
                    df = pd.DataFrame(ads)
                    st.dataframe(df, use_container_width=True)

                    with st.expander("Raw Meta Ads"):
                        st.json(ads)

            except Exception as e:
                st.error("Meta Ads Library failed")
                st.exception(e)

    # =============================
    # YOUTUBE
    # =============================
    with r_tabs[3]:
        st.subheader("YouTube Demand & Content Patterns")

        if run_research:
            try:
                videos = fetch_youtube_trends(keyword)

                if not videos:
                    st.warning("No videos returned.")
                else:
                    df = pd.DataFrame(videos)
                    st.dataframe(df, use_container_width=True)

                    with st.expander("Raw YouTube Data"):
                        st.json(videos)

            except Exception as e:
                st.error("YouTube research failed")
                st.exception(e)

    # =============================
    # TIKTOK
    # =============================
    with r_tabs[4]:
        st.subheader("TikTok Virality & Hashtags")

        if run_research:
            try:
                data = fetch_tiktok_trends(keyword)

                if not data:
                    st.warning("No TikTok data.")
                else:
                    st.json(data)

            except Exception as e:
                st.error("TikTok research failed")
                st.exception(e)
# =================================
# TAB 3 — CREATIVE (AI SAFE)
# =================================
with tabs[2]:
    st.subheader("🎨 Creative Generator")

    product = st.text_input("Product / Offer")
    audience = st.text_input("Audience")
    goal = st.selectbox("Goal", ["Conversions", "Traffic", "Leads"])
    tone = st.selectbox("Tone", ["Bold", "Luxury", "Aggressive"])

    if st.button("Generate Creative"):
        if not env("OPENAI_API_KEY"):
            st.warning("OpenAI key not connected — using fallback copy.")

        creative = {
            "Headline": f"{product} That Converts",
            "Primary Text": f"Perfect for {audience}. Optimized for {goal}.",
            "CTA": "Learn More",
        }

        st.table(pd.DataFrame(creative.items(), columns=["Field", "Value"]))

# =================================
# TAB 4 — CAMPAIGNS (NON-BLOCKING)
# =================================
with tabs[3]:
    st.subheader("📣 Campaign Launcher")

    platforms = st.multiselect(
        "Platforms",
        ["Meta", "Google"],
        default=["Meta"],
    )

    budget = st.number_input("Budget ($)", min_value=100, value=500)

    if st.button("Prepare Campaign"):
        rows = []

        if "Meta" in platforms:
            rows.append({
                "Platform": "Meta",
                "Budget": f"${budget}",
                "Status": "Ready" if env("META_ACCESS_TOKEN") else "Missing API Key",
            })

        if "Google" in platforms:
            rows.append({
                "Platform": "Google",
                "Budget": f"${budget}",
                "Status": "Ready" if env("GOOGLE_DEVELOPER_TOKEN") else "Missing API Key",
            })

        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        st.info(
            "Campaigns are prepared safely. "
            "Publishing only activates when required keys are present."
        )