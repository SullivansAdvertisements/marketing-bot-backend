# ============================================================
# SULLIVAN’S ADVERTISING — STREAMLIT APP (GOOGLE ADS KEYWORDS)
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
st.session_state.setdefault("research_data", None)
st.session_state.setdefault("generated_keywords", [])

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
        "content_trends": len(research_data.get("content_trends", [])),
        "competitor_ads": len(research_data.get("ad_intel", [])),
        "locations": len(research_data.get("locations", [])),
    }

    prompt = f"""
You are a senior paid media strategist.

Explain this research clearly to a business owner.
Do NOT invent metrics. Explain how this data should
be used to make advertising decisions.

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
st.caption("Guided research → real data → campaign execution")

# ============================================================
# SIDEBAR
# ============================================================
tab = st.sidebar.radio("Navigation", ["Research", "Campaigns"], index=0)

# ============================================================
# ======================= RESEARCH TAB =======================
# ============================================================
if tab == "Research":

    st.markdown("## 🔍 Research Center")
    st.markdown(
        "Use this section to **generate real Google Ads keywords**, "
        "validate demand, analyze competitors, and identify the best locations to advertise."
    )

    st.divider()

    niche = st.text_input("Business / Niche", placeholder="e.g. Streetwear Brand")
    seed_keyword = st.text_input("Seed Keyword", placeholder="e.g. graphic hoodies")

    # ========================================================
    # GOOGLE ADS KEYWORD GENERATOR
    # ========================================================
    st.markdown("## 🔑 Keyword Generator (Google Ads)")
    st.markdown(
        "This tool uses **Google Ads Keyword Planner** to generate keyword ideas "
        "with **real search volume, competition, and CPC estimates**."
    )

    country_map = {
        "United States": "2840",
        "United Kingdom": "2826",
        "Canada": "2124",
        "Australia": "2036",
    }

    col1, col2 = st.columns([1, 2])

    with col1:
        country = st.selectbox("Target Country", list(country_map.keys()))
        generate_btn = st.button("Generate Keywords")

    if generate_btn:
        if not seed_keyword:
            st.warning("Enter a seed keyword first.")
        else:
            with st.spinner("Generating keywords from Google Ads…"):
                fn, err = safe_import(
                    "research.google_keywords",
                    "generate_google_ads_keywords",
                )

                if not fn:
                    st.error(
                        "Google Ads keyword generator unavailable.\n\n"
                        "Ensure:\n"
                        "• google-ads SDK is installed\n"
                        "• GOOGLE_ADS credentials are configured"
                    )
                else:
                    try:
                        st.session_state.generated_keywords = fn(
                            seed_keyword,
                            country_map[country],
                        )
                        st.success(
                            f"Generated {len(st.session_state.generated_keywords)} keyword ideas"
                        )
                    except Exception as e:
                        st.error(str(e))

    if st.session_state.generated_keywords:
        st.markdown("### 📊 Keyword Opportunities")
        st.markdown("""
**How to read this table**
- **Avg Monthly Searches** → Demand
- **Competition** → Auction density
- **Top of Page CPC** → Estimated cost to compete
""")

        df_kw = pd.DataFrame(st.session_state.generated_keywords)
        df_kw = df_kw.sort_values(
            "avg_monthly_searches",
            ascending=False,
        )

        st.dataframe(df_kw, use_container_width=True)

    st.divider()

    # ========================================================
    # RUN FULL RESEARCH
    # ========================================================
    st.markdown("## 📈 Run Full Market Research")
    st.markdown(
        "This pulls **live platform data** (Google, Meta, YouTube, TikTok) "
        "to validate demand, competition, and location opportunities."
    )

    if st.button("Run Full Research"):
        if not niche or not seed_keyword:
            st.warning("Niche and seed keyword are required.")
            st.stop()

        research_data = {
            "niche": niche,
            "platforms": ["google", "meta", "youtube", "tiktok"],
            "keywords": [],
            "search_trends": [],
            "content_trends": [],
            "ad_intel": [],
            "locations": [],
            "sources": {},
        }

        # ---------------- GOOGLE KEYWORDS ----------------
        fn, _ = safe_import("research.google_keywords", "fetch_google_keywords")
        if fn:
            research_data["keywords"] = fn(seed_keyword)

        # ---------------- GOOGLE TRENDS ----------------
        fn, _ = safe_import("research.google_trends", "fetch_google_trends")
        if fn:
            res = fn(seed_keyword, "Global")
            if isinstance(res, dict) and "Google Trends" in res:
                df = res["Google Trends"]
                for _, row in df.iterrows():
                    research_data["search_trends"].append({
                        "term": seed_keyword,
                        "interest": int(row[seed_keyword]),
                    })

        # ---------------- YOUTUBE / TIKTOK / META ----------------
        for module, fn_name, key in [
            ("research.youtube_trends", "fetch_youtube_trends", "content_trends"),
            ("research.tiktok_trends", "fetch_tiktok_trends", "content_trends"),
            ("research.meta_ad_library", "fetch_meta_ads", "ad_intel"),
        ]:
            fn, _ = safe_import(module, fn_name)
            if fn:
                try:
                    data = fn(seed_keyword)
                    if isinstance(data, list):
                        research_data[key].extend(data)
                except Exception:
                    pass

        st.session_state.research_data = research_data
        st.success("Research completed")

    # ========================================================
    # DISPLAY RESULTS
    # ========================================================
    if st.session_state.research_data:
        st.divider()

        st.markdown("## 🧾 What This Data Means")
        with st.expander("Click to understand each dataset", expanded=True):
            st.markdown("""
**Keywords** – Search demand & commercial intent  
**Search Trends** – Rising or declining interest  
**Content Trends** – What content formats perform  
**Competitor Ads** – What others are actively running  
**Locations** – Where demand is strongest  
""")

        st.markdown("## 🧠 AI Research Summary")
        if st.button("Explain Research Results"):
            with st.spinner("Analyzing…"):
                st.write(
                    generate_research_explanation(
                        st.session_state.research_data
                    )
                )

        if st.session_state.research_data["keywords"]:
            st.markdown("## 📈 Google Keyword Data")
            st.dataframe(
                pd.DataFrame(st.session_state.research_data["keywords"]),
                use_container_width=True,
            )

        if st.session_state.research_data["content_trends"]:
            st.markdown("## 🎬 Content Trends")
            st.dataframe(
                pd.DataFrame(st.session_state.research_data["content_trends"]),
                use_container_width=True,
            )

        if st.session_state.research_data["ad_intel"]:
            st.markdown("## 📣 Competitor Ads")
            st.dataframe(
                pd.DataFrame(st.session_state.research_data["ad_intel"]),
                use_container_width=True,
            )

# ============================================================
# ======================= CAMPAIGNS TAB ======================
# ============================================================
if tab == "Campaigns":

    st.subheader("🎯 Campaign Builder")

    if not st.session_state.research_data:
        st.info("Run research first to unlock campaigns.")
        st.stop()

    fn, err = safe_import("campaigns.router", "render")
    if not fn:
        st.error(f"Campaign module unavailable: {err}")
        st.stop()

    fn()