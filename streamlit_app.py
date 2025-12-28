import streamlit as st

# =================================================
# MUST be first Streamlit call
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="wide"
)

# =================================================
# Imports – OAuth + Campaign System
# =================================================
from oauth_meta import (
    meta_login_url,
    exchange_code_for_token,
    fetch_ad_accounts,
    create_meta_campaign,
    create_meta_adset,
    create_meta_ad_creative,
    fetch_campaign_insights,
)

# =================================================
# Imports – Research Engine
# =================================================
from app.research.router import run_research

# =================================================
# Imports – Creative AI Engine (OPENAI WIRED HERE)
# =================================================
from app.creative.router import generate_creative

# =================================================
# Title
# =================================================
st.title("🚀 Marketing Bot")

# =================================================
# OAuth callback handling
# =================================================
query = st.experimental_get_query_params()

st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")

if "code" in query and "meta_access_token" not in st.session_state:
    try:
        access_token = exchange_code_for_token(query["code"][0])
        st.session_state["meta_access_token"] = access_token
        st.success("Meta connected successfully 🎉")
    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)

# =================================================
# Require auth beyond this point
# =================================================
if "meta_access_token" not in st.session_state:
    st.stop()

# =================================================
# Fetch Ad Accounts
# =================================================
st.header("📂 Ad Accounts")

accounts_response = fetch_ad_accounts(st.session_state["meta_access_token"])
accounts = accounts_response.get("data", [])

if not accounts:
    st.warning("No ad accounts found.")
    st.stop()

account_map = {}
for acct in accounts:
    label = acct.get("name", acct["id"])
    clean_id = acct["id"].replace("act_", "")
    account_map[label] = clean_id
    st.success(f"{label} ({acct['id']})")

selected_account_name = st.selectbox(
    "Select Ad Account",
    list(account_map.keys())
)

selected_account_id = account_map[selected_account_name]

# =================================================
# 🔍 RESEARCH TAB
# =================================================
st.divider()
st.header("🔍 Research Engine")

research_platform = st.selectbox(
    "Platform",
    ["google_trends", "youtube", "meta_ads"]
)

research_keyword = st.text_input("Keyword", "streetwear")
research_geo = st.selectbox("Country", ["US", "CA", "GB", "AU"])
research_timeframe = st.selectbox(
    "Timeframe",
    ["today 7-d", "today 90-d", "today 12-m", "today 5-y"],
)

if st.button("Run Research"):
    try:
        results = run_research(
            platform=research_platform,
            keyword=research_keyword,
            geo=research_geo,
            timeframe=research_timeframe,
            access_token=st.session_state["meta_access_token"],
        )

        st.session_state["research_results"] = results
        st.success("Research complete")

        st.json(results)

    except Exception as e:
        st.error("Research failed")
        st.exception(e)

# =================================================
# 🧠 CREATIVE AI TAB (OPENAI WIRED)
# =================================================
st.divider()
st.header("🎨 Creative AI Generator")

product = st.text_input("Product", "Streetwear Hoodie")
audience = st.text_input("Audience", "Gen Z streetwear fans")

goal = st.selectbox(
    "Goal",
    ["sales", "leads", "awareness"]
)

tone = st.selectbox(
    "Tone",
    ["bold", "friendly", "professional"]
)

platform = st.selectbox(
    "Platform",
    ["meta", "tiktok", "youtube"]
)

use_ai = st.checkbox(
    "Use OpenAI (fallback if unavailable)",
    value=True
)

if st.button("Generate Ad Copy"):
    try:
        creative = generate_creative(
            product=product,
            audience=audience,
            goal=goal,
            tone=tone,
            platform=platform,
        )

        st.success("Creative generated")

        st.subheader("Headline")
        st.write(creative["headline"])

        st.subheader("Primary Text")
        st.write(creative["primary_text"])

        st.subheader("CTA")
        st.write(creative["cta"])

        st.caption(f"Source: {creative.get('source')}")

        st.session_state["last_creative"] = creative

    except Exception as e:
        st.error("Creative generation failed")
        st.exception(e)

# =================================================
# 📣 CAMPAIGN BUILDER
# =================================================
st.divider()
st.header("📣 Campaign Builder")

campaign_name = st.text_input("Campaign Name", "My First Campaign")

OBJECTIVES = {
    "Traffic": "TRAFFIC",
    "Leads": "LEAD_GENERATION",
    "Sales": "OUTCOME_SALES",
    "Awareness": "OUTCOME_AWARENESS",
    "Engagement": "POST_ENGAGEMENT",
}

objective_label = st.selectbox("Objective", list(OBJECTIVES.keys()))
objective = OBJECTIVES[objective_label]

daily_budget = st.number_input(
    "Daily Budget ($)",
    min_value=5,
    value=10,
    step=5
)

if st.button("🚀 Create Campaign"):
    try:
        result = create_meta_campaign(
            access_token=st.session_state["meta_access_token"],
            ad_account_id=selected_account_id,
            name=campaign_name,
            objective=objective,
            daily_budget=int(daily_budget * 100),
        )
        st.success("Campaign created (PAUSED)")
        st.session_state["campaign_id"] = result["id"]
        st.json(result)
    except Exception as e:
        st.error("Campaign creation failed")
        st.exception(e)

# =================================================
# 📊 INSIGHTS
# =================================================
st.divider()
st.header("📊 Campaign Insights")

insights_campaign_id = st.text_input(
    "Campaign ID",
    value=st.session_state.get("campaign_id", "")
)

if st.button("Load Insights"):
    try:
        insights = fetch_campaign_insights(
            st.session_state["meta_access_token"],
            insights_campaign_id
        )
        st.json(insights)
    except Exception as e:
        st.error("Failed to load insights")
        st.exception(e)