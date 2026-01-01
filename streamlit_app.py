# =========================================================
# STREAMLIT CORE
# =========================================================
import os
import streamlit as st

# =========================================================
# PAGE CONFIG (MUST BE FIRST)
# =========================================================
st.set_page_config(
    page_title="Marketing Bot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# SAFE ENV HELPER (CRITICAL FIX)
# =========================================================
def env(key: str):
    """
    Safe environment loader.
    Works with:
    - os.environ
    - Streamlit secrets
    - Missing keys (returns None)
    """
    try:
        return os.getenv(key) or st.secrets.get(key, None)
    except Exception:
        return None

# =========================================================
# SESSION STATE SAFETY
# =========================================================
DEFAULT_SESSION_KEYS = {
    "meta_token": env("META_ACCESS_TOKEN"),
    "google_token": env("GOOGLE_ADS_API_KEY"),
    "openai_key": env("OPENAI_API_KEY"),
}

for k, v in DEFAULT_SESSION_KEYS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# API STATUS (NON-BLOCKING)
# =========================================================
API_STATUS = {
    "Meta Ads": bool(st.session_state.meta_token),
    "Google Ads": bool(st.session_state.google_token),
    "OpenAI": bool(st.session_state.openai_key),
}

# =========================================================
# SAFE ROUTER IMPORTS (NO app.)
# =========================================================
try:
    from research.router import render as research_render
except Exception as e:
    research_render = lambda: st.error(f"Research tab failed to load: {e}")

try:
    from campaigns.router import render as campaigns_render
except Exception as e:
    campaigns_render = lambda: st.error(f"Campaigns tab failed to load: {e}")

try:
    from strategy.router import render as strategy_render
except Exception as e:
    strategy_render = lambda: st.error(f"Strategy tab failed to load: {e}")

try:
    from creative.router import render as creative_render
except Exception as e:
    creative_render = lambda: st.error(f"Creative tab failed to load: {e}")

# =========================================================
# HEADER
# =========================================================
st.title("🚀 Marketing Bot")

# =========================================================
# SIDEBAR — API STATUS (SAFE)
# =========================================================
with st.sidebar:
    st.subheader("🔐 API Status")

    for name, active in API_STATUS.items():
        if active:
            st.success(f"{name}: Connected")
        else:
            st.warning(f"{name}: Not Connected")

    st.divider()
    st.caption("App runs even if APIs are disconnected.")

# =========================================================
# MAIN NAVIGATION TABS
# =========================================================
tabs = st.tabs([
    "🔎 Research",
    "📣 Campaigns",
    "📈 Strategy",
    "🎨 Creative",
])

# =========================================================
# TAB ROUTING
# =========================================================
with tabs[0]:
    research_render()

with tabs[1]:
    campaigns_render()

with tabs[2]:
    strategy_render()

with tabs[3]:
    creative_render()
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