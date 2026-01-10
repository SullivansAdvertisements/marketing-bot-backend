# ============================================================
# SULLIVAN’S ADVERTISING — STREAMLIT APP (UX + KEYWORD GEN)
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
# OPENAI HELPERS
# ============================================================
def openai_client():
    try:
        from openai import OpenAI
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    except Exception:
        return None


def generate_keywords_ai(niche: str, seed: str, limit: int = 20):
    client = openai_client()
    if not client:
        return []

    prompt = f"""
You are a senior paid media strategist.

Generate high-intent advertising keywords for:
Niche: {niche}
Seed keyword: {seed}

Rules:
- Commercial / buyer intent only
- No fluff keywords
- Output as a simple list
- Max {limit} keywords
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    lines = response.choices[0].message.content.split("\n")
    return [l.strip("-• ").strip() for l in lines if l.strip()]


def generate_research_explanation(research_data: dict) -> str:
    client = openai_client()
    if not client:
        return "OpenAI not configured."

    summary = {
        "niche": research_data.get("niche"),
        "keywords": len(research_data.get("keywords", [])),
        "search_trends": len(research_data.get("search_trends", [])),
        "content_trends": len(research_data.get("content_trends", [])),
        "competitor_ads": len(research_data.get("ad_intel", [])),
        "locations": len(research_data.get("locations", [])),
    }

    prompt = f"""
Explain this marketing research to a business owner in plain English.
Focus on:
- What the data means
- How to use it for ads
- What to do next

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
st.caption("Guided research → clear insights → campaign execution")

# ============================================================
# SIDEBAR
# ============================================================
tab = st.sidebar.radio("Navigation", ["Research", "Campaigns"])

# ============================================================
# ======================= RESEARCH TAB =======================
# ============================================================
if tab == "Research":

    st.markdown("## 🔍 Research Center")
    st.markdown(
        "This section helps you **discover demand, competition, content trends, "
        "and the best locations to advertise** — all before launching campaigns."
    )

    st.divider()

    niche = st.text_input("Business / Niche", placeholder="e.g. Streetwear Brand")
    seed_keyword = st.text_input("Seed Keyword", placeholder="e.g. graphic hoodies")

    # ========================================================
    # KEYWORD GENERATION
    # ========================================================
    st.markdown("## 🧠 Keyword Generator")
    st.markdown(
        "Generate **high-intent keywords** you can use for Google Ads, Meta interests, "
        "and creative angles."
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button("Generate Keywords"):
            if not niche or not seed_keyword:
                st.warning("Enter niche and seed keyword first.")
            else:
                with st.spinner("Generating keywords…"):
                    st.session_state.generated_keywords = generate_keywords_ai(
                        niche, seed_keyword
                    )

    with col2:
        if st.session_state.generated_keywords:
            st.success("High-intent keywords generated")
            st.write(st.session_state.generated_keywords)

    st.divider()

    # ========================================================
    # RUN FULL RESEARCH
    # ========================================================
    st.markdown("## 📊 Run Market Research")
    st.markdown(
        "This pulls **real platform data** (Google, Meta, TikTok, YouTube) "
        "to validate demand and competition."
    )

    if st.button("Run Full Research"):
        if not niche or not seed_keyword:
            st.warning("Niche and seed keyword required.")
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
**Keywords** – Search demand and commercial intent  
**Search Trends** – Rising or declining interest  
**Content Trends** – What type of content performs  
**Competitor Ads** – What others are actively running  
**Locations** – Where demand is strongest  
""")

        st.markdown("## 🧠 AI Summary")
        if st.button("Explain Research Results"):
            with st.spinner("Analyzing…"):
                st.write(generate_research_explanation(
                    st.session_state.research_data
                ))

        if st.session_state.generated_keywords:
            st.markdown("## 🔑 Generated Keywords")
            st.dataframe(
                pd.DataFrame(
                    {"keyword": st.session_state.generated_keywords}
                ),
                use_container_width=True,
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