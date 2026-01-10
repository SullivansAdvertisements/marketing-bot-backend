# ============================================================
# SULLIVAN’S ADVERTISING — STREAMLIT APP (HARDENED + EXPLAINABLE)
# ============================================================

import streamlit as st
import pandas as pd
import os

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
# SAFE IMPORT HELPER
# ============================================================
def safe_import(path: str, name: str):
    try:
        module = __import__(path, fromlist=[name])
        return getattr(module, name), None
    except Exception as e:
        return None, str(e)

# ============================================================
# OPENAI EXPLANATION
# ============================================================
def generate_research_explanation(research_data: dict) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        return "OpenAI SDK not installed."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY not set."

    client = OpenAI(api_key=api_key)

    summary = {
        "niche": research_data.get("niche"),
        "platforms": research_data.get("platforms"),
        "keyword_count": len(research_data.get("keywords", [])),
        "search_trends_count": len(research_data.get("search_trends", [])),
        "content_trends_count": len(research_data.get("content_trends", [])),
        "ad_intel_count": len(research_data.get("ad_intel", [])),
        "locations_sample": research_data.get("locations", [])[:10],
    }

    prompt = f"""
You are a senior digital marketing analyst.

Explain the following research data clearly for a business owner.
Do NOT invent metrics. Explain what the data means and how it can
be used for targeting, budgeting, and scaling.

Data:
{summary}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()

# ============================================================
# HEADER
# ============================================================
st.title("🚀 Sullivan’s Advertising Intelligence")
st.caption("Research → Validation → Campaign Execution")

# ============================================================
# SIDEBAR NAV
# ============================================================
with st.sidebar:
    tab = st.radio("Navigation", ["Research", "Campaigns"], index=0)

# ============================================================
# ======================= RESEARCH TAB =======================
# ============================================================
if tab == "Research":

    st.subheader("🔍 Advanced Market Research")

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
            "locations": [],
            "audiences": {},
            "funnels": {},
            "angles": {},
            "budget_guidance": {},
            "sources": {},
        }

        # ---------------- GOOGLE KEYWORDS ----------------
        fn, err = safe_import("research.google_keywords", "fetch_google_keywords")
        if fn:
            research_data["keywords"] = fn(keyword)
            research_data["sources"]["google_keywords"] = "Google Ads API"
        else:
            st.warning(f"Google Keywords disabled: {err}")

        # ---------------- GOOGLE TRENDS ----------------
        fn, err = safe_import("research.google_trends", "fetch_google_trends")
        if fn:
            result = fn(keyword, "Global")
            if isinstance(result, dict) and "Google Trends" in result:
                df = result["Google Trends"]
                if isinstance(df, pd.DataFrame):
                    for _, row in df.iterrows():
                        research_data["search_trends"].append({
                            "term": keyword,
                            "interest_score": int(row[keyword]),
                            "timeframe": "12m",
                            "platform": "google",
                            "source": "google_trends",
                        })
                        research_data["locations"].append({
                            "platform": "google",
                            "location": "Global",
                            "metric": "interest",
                            "value": int(row[keyword]),
                            "source": "google_trends",
                        })
            research_data["sources"]["google_trends"] = "Google Trends"
        else:
            st.warning(f"Google Trends disabled: {err}")

        # ---------------- YOUTUBE TRENDS ----------------
        fn, err = safe_import("research.youtube_trends", "fetch_youtube_trends")
        if fn:
            try:
                yt = fn(keyword)
                for item in yt:
                    research_data["content_trends"].append(item)
                    research_data["locations"].append({
                        "platform": "youtube",
                        "location": "Global",
                        "metric": "views_rank",
                        "value": 1,
                        "source": "youtube_api",
                    })
                research_data["sources"]["youtube"] = "YouTube API"
            except Exception as e:
                st.warning(f"YouTube disabled: {e}")
        else:
            st.warning(f"YouTube disabled: {err}")

        # ---------------- TIKTOK TRENDS ----------------
        fn, err = safe_import("research.tiktok_trends", "fetch_tiktok_trends")
        if fn:
            try:
                tk = fn(keyword)
                if isinstance(tk, dict):
                    tk = tk.get("data", [])
                for item in tk:
                    research_data["content_trends"].append(item)
                    research_data["locations"].append({
                        "platform": "tiktok",
                        "location": item.get("region", "Global"),
                        "metric": "trend",
                        "value": 1,
                        "source": "tiktok_api",
                    })
                research_data["sources"]["tiktok"] = "TikTok API"
            except Exception as e:
                st.warning(f"TikTok error: {e}")
        else:
            st.warning(f"TikTok disabled: {err}")

        # ---------------- META AD LIBRARY ----------------
        fn, err = safe_import("research.meta_ad_library", "fetch_meta_ads")
        if fn:
            ads = fn(keyword)
            research_data["ad_intel"] = ads
            for ad in ads:
                research_data["locations"].append({
                    "platform": "meta",
                    "location": ad.get("country", "US"),
                    "metric": "active_ads",
                    "value": 1,
                    "source": "meta_ad_library",
                })
            research_data["sources"]["meta"] = "Meta Ad Library"
        else:
            st.warning(f"Meta Ad Library disabled: {err}")

        st.session_state.research_data = research_data
        st.success("Research validated and stored")

    # ========================================================
    # ===================== OUTPUTS ==========================
    # ========================================================
    if st.session_state.research_data:

        st.divider()

        # ---------------- DATA KEY ----------------
        st.markdown("## 🧾 Research Data Key")
        with st.expander("What does this data mean?", expanded=True):
            st.markdown("""
**Keywords** – Google Ads demand & competition  
**Search Trends** – Interest over time (0–100 scale)  
**Content Trends** – Top videos/posts driving attention  
**Competitor Ads** – Active Meta ads & messaging  
**Location Demand** – Regional demand signals per platform  
""")

        # ---------------- AI EXPLANATION ----------------
        st.markdown("## 🧠 AI Research Summary")
        if st.button("Explain this research"):
            with st.spinner("Analyzing research…"):
                explanation = generate_research_explanation(
                    st.session_state.research_data
                )
                st.write(explanation)

        # ---------------- KEYWORDS ----------------
        if st.session_state.research_data["keywords"]:
            st.markdown("## 🔑 Google Keywords")
            st.dataframe(
                pd.DataFrame(st.session_state.research_data["keywords"]),
                use_container_width=True,
            )

        # ---------------- CONTENT ----------------
        if st.session_state.research_data["content_trends"]:
            st.markdown("## 🎥 Content Trends")
            st.dataframe(
                pd.DataFrame(st.session_state.research_data["content_trends"]),
                use_container_width=True,
            )

        # ---------------- ADS ----------------
        if st.session_state.research_data["ad_intel"]:
            st.markdown("## 📣 Competitor Ads")
            st.dataframe(
                pd.DataFrame(st.session_state.research_data["ad_intel"]),
                use_container_width=True,
            )

        # ---------------- LOCATION FILTER ----------------
        if st.session_state.research_data["locations"]:
            st.markdown("## 🌍 Location Demand")

            df = pd.DataFrame(st.session_state.research_data["locations"])

            platforms = sorted(df["platform"].unique())
            selected_platforms = st.multiselect(
                "Platforms",
                platforms,
                default=platforms,
            )

            df = df[df["platform"].isin(selected_platforms)]

            regions = sorted(df["location"].unique())
            selected_regions = st.multiselect(
                "Regions / Countries",
                regions,
                default=regions[:10],
            )

            df = df[df["location"].isin(selected_regions)]

            st.dataframe(
                df.sort_values("value", ascending=False),
                use_container_width=True,
            )

# ============================================================
# ======================= CAMPAIGNS TAB ======================
# ============================================================
if tab == "Campaigns":

    st.subheader("🎯 Campaigns")

    if not st.session_state.research_data:
        st.info("Run research first to unlock campaigns")
        st.stop()

    fn, err = safe_import("campaigns.router", "render")
    if not fn:
        st.error(f"Campaign module unavailable: {err}")
        st.stop()

    fn()