import streamlit as st
from app.creative.router import generate_creative
from app.creative.meta_creatives import create_meta_ad_creative
from app.research.router import run_research
# =================================================
# MUST be first Streamlit call
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="wide",
)

# =================================================
# CORE IMPORTS (SAFE)
# =================================================
from oauth_meta import (
    meta_login_url,
    exchange_code_for_token,
    fetch_ad_accounts,
)

# Lazy imports (inside tabs later)
# from app.research.router import run_research
# from app.creative.router import generate_creative
# from app.strategy.router import run_strategy

# =================================================
# APP TITLE
# =================================================
st.title("🚀 Marketing Bot")

# =================================================
# AUTH / OAUTH HANDLING (GLOBAL)
# =================================================
query = st.experimental_get_query_params()

with st.sidebar:
    st.subheader("🔐 Authentication")
    st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")

    if "code" in query and "meta_access_token" not in st.session_state:
        try:
            token = exchange_code_for_token(query["code"][0])
            st.session_state["meta_access_token"] = token
            st.success("Meta connected")
        except Exception as e:
            st.error("OAuth failed")
            st.exception(e)

if "meta_access_token" not in st.session_state:
    st.warning("Please connect Meta Ads to continue.")
    st.stop()

ACCESS_TOKEN = st.session_state["meta_access_token"]

# =================================================
# FETCH AD ACCOUNTS (GLOBAL CONTEXT)
# =================================================
accounts_response = fetch_ad_accounts(ACCESS_TOKEN)
accounts = accounts_response.get("data", [])

if not accounts:
    st.error("No ad accounts found.")
    st.stop()

account_map = {
    acct.get("name", acct["id"]): acct["id"].replace("act_", "")
    for acct in accounts
}

# =================================================
# MAIN TABS
# =================================================
tab_auth, tab_research, tab_campaigns, tab_creative, tab_strategy, tab_utils = st.tabs(
    [
        "🔐 Auth",
        "🔍 Research",
        "📣 Campaigns",
        "🎨 Creative",
        "🧠 Strategy",
        "🧰 System",
    ]
)

# =================================================
# AUTH TAB
# =================================================
with tab_auth:
    st.header("🔐 Meta Connection")

    for name, acct_id in account_map.items():
        st.success(f"{name} ({acct_id})")

    selected_account = st.selectbox(
        "Active Ad Account",
        list(account_map.keys()),
    )

    st.session_state["ad_account_id"] = account_map[selected_account]

# =================================================
# RESEARCH TAB (PLACEHOLDER – SAFE)
# =================================================
# =================================================
# 🔍 RESEARCH ENGINE
# =================================================
st.divider()
st.header("🔍 Market Research Engine")

research_platform = st.selectbox(
    "Research Source",
    [
        "google_trends",
        "google_keywords",
        "youtube",
        "tiktok",
        "meta_ads",
    ],
)

research_keyword = st.text_input(
    "Keyword / Topic",
    placeholder="streetwear, gym clothing, skincare",
)

research_geo = st.selectbox(
    "Country",
    ["US", "CA", "GB", "AU"],
    index=0,
)

research_timeframe = st.selectbox(
    "Timeframe (Google Trends only)",
    ["today 7-d", "today 90-d", "today 12-m", "today 5-y"],
    index=2,
)

if st.button("📊 Run Research"):
    if not research_keyword:
        st.warning("Enter a keyword first")
        st.stop()

    try:
        results = run_research(
            platform=research_platform,
            keyword=research_keyword,
            geo=research_geo,
            timeframe=research_timeframe,
            access_token=st.session_state.get("meta_access_token"),
        )

        st.session_state["research_results"] = results
        st.success("Research completed")

        # ------------------------------
        # Display Results (Smart Render)
        # ------------------------------
        if isinstance(results, list) and results:
            st.subheader("Top Results")

            for row in results[:10]:
                st.json(row)

        elif isinstance(results, dict):
            st.json(results)

        else:
            st.warning("No data returned")

    except Exception as e:
        st.error("Research failed")
        st.exception(e)
# =================================================
# CAMPAIGNS TAB (PLACEHOLDER – SAFE)
# =================================================
with tab_campaigns:
    st.header("📣 Campaign Builder")

    st.info("Campaign creation module ready.")

    st.markdown("""
    This tab will use:
    - app/campaigns/meta_campaigns.py
    - app/utils/validators.py
    - app/utils/rate_limits.py
    """)

# =================================================
# CREATIVE TAB (PLACEHOLDER – SAFE)
# =================================================
st.divider()
st.header("🎨 Creative Builder (AI-Powered)")

product = st.text_input("Product / Offer", "Streetwear Hoodie")
audience = st.text_input("Target Audience", "Streetwear fans 18–30")

goal = st.selectbox(
    "Goal",
    ["sales", "leads", "traffic"]
)

tone = st.selectbox(
    "Tone",
    ["bold", "friendly", "premium"]
)

platform = st.selectbox(
    "Platform",
    ["meta", "tiktok", "youtube"]
)

use_ai = st.checkbox("Use AI (OpenAI)", value=True)

if st.button("✨ Generate Ad Copy"):
    creative = generate_creative(
        product=product,
        audience=audience,
        goal=goal,
        tone=tone,
        platform=platform,
        use_ai=use_ai,
    )
st.subheader("📤 Push Creative to Meta")

page_id = st.text_input("Facebook Page ID")
destination_url = st.text_input("Destination URL", "https://example.com")

if st.button("🚀 Create Meta Ad Creative"):
    creative = st.session_state.get("last_creative")

    if not creative:
        st.warning("Generate creative first")
    else:
        result = create_meta_ad_creative(
            access_token=st.session_state["meta_access_token"],
            ad_account_id=selected_account_id,
            page_id=page_id,
            headline=creative["headline"],
            primary_text=creative["primary_text"],
            destination_url=destination_url,
        )

        st.success("Meta Creative Created")
        st.json(result)
    st.subheader("Generated Creative")
    st.success(f"Headline: {creative['headline']}")
    st.write(creative["primary_text"])
    st.info(f"CTA: {creative['cta']}")
    st.caption(f"Source: {creative['source']}")

    st.session_state["last_creative"] = creative
# =================================================
# STRATEGY TAB
# =================================================
st.divider()
st.header("🧠 Strategy & Budget Planning")

from app.strategy.router import generate_strategy

# -----------------------------
# Inputs
# -----------------------------
total_budget = st.number_input(
    "Total Monthly Ad Budget ($)",
    min_value=100,
    value=1000,
    step=100
)

objective = st.selectbox(
    "Primary Objective",
    ["awareness", "traffic", "sales"]
)

risk_level = st.selectbox(
    "Risk Profile",
    ["conservative", "balanced", "aggressive"],
    index=1
)

average_order_value = st.number_input(
    "Average Order Value ($)",
    min_value=1,
    value=50,
    step=5
)

# -----------------------------
# Generate Strategy
# -----------------------------
if st.button("📊 Generate Strategy Plan"):
    try:
        strategy = generate_strategy(
            total_budget=total_budget,
            objective=objective,
            risk_level=risk_level,
            average_order_value=average_order_value,
        )

        st.success("Strategy generated successfully")

        # -----------------------------
        # Budget Allocation
        # -----------------------------
        st.subheader("💰 Budget Allocation")

        allocation = strategy["allocation"]

        for platform, amount in allocation.items():
            st.write(f"**{platform.upper()}**: ${amount:,.2f}")

        st.bar_chart(allocation)

        # -----------------------------
        # Performance Estimates
        # -----------------------------
        st.subheader("📈 Estimated Performance (Ranges)")

        projections = strategy["projections"]

        for platform, metrics in projections.items():
            st.markdown(f"### {platform.upper()}")

            if "note" in metrics:
                st.info(metrics["note"])
                continue

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Estimated Clicks",
                f"{metrics['estimated_clicks']:,}"
            )

            col2.metric(
                "Estimated Conversions",
                f"{metrics['estimated_conversions']}"
            )

            col3.metric(
                "Estimated Revenue",
                f"${metrics['estimated_revenue']:,.2f}"
            )

        # -----------------------------
        # Assumptions
        # -----------------------------
        st.subheader("⚠️ Planning Assumptions")
        st.json(strategy["assumptions"])

        st.caption(
            "All estimates are based on public platform benchmarks. "
            "Actual results may vary due to creative quality, audience, and offer."
        )

    except Exception as e:
        st.error("Strategy generation failed")
        st.exception(e)
# =================================================
# SYSTEM / UTILS TAB
# =================================================
with tab_utils:
    st.header("🧰 System Status")

    st.success("App loaded successfully")
    st.write("Access token stored:", bool(ACCESS_TOKEN))
    st.write("Ad account selected:", st.session_state.get("ad_account_id"))

    st.markdown("""
    Utilities active:
    - Logging
    - Rate limits
    - Validators
    """)