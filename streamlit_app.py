import streamlit as st

# =================================================
# MUST be first Streamlit call
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="wide"
)

# =================================================
# Meta OAuth + Ads
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
# Research Engine
# =================================================
from app.research.router import run_research

# =================================================
# Title
# =================================================
st.title("🚀 Marketing Bot")

# =================================================
# OAuth Callback Handling (GLOBAL)
# =================================================
query = st.experimental_get_query_params()

st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")

if "code" in query and "meta_access_token" not in st.session_state:
    try:
        token = exchange_code_for_token(query["code"][0])
        st.session_state["meta_access_token"] = token
        st.success("Meta connected successfully 🎉")
    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)

# =================================================
# Tabs (MATCH YOUR FOLDERS)
# =================================================
tab_auth, tab_research, tab_campaigns, tab_creative, tab_strategy = st.tabs([
    "🔐 Auth",
    "🔍 Research",
    "📣 Campaigns",
    "🎨 Creative",
    "🧠 Strategy",
])

# =================================================
# 🔐 AUTH TAB
# =================================================
with tab_auth:
    st.subheader("Meta Authentication")

    if "meta_access_token" in st.session_state:
        st.success("Meta connected")
        st.code(st.session_state["meta_access_token"][:30] + "...", language="text")
    else:
        st.warning("Not connected to Meta Ads")

# =================================================
# 🔍 RESEARCH TAB
# =================================================
with tab_research:
    st.subheader("Market Research Engine")

    if "meta_access_token" not in st.session_state:
        st.warning("Connect Meta Ads first")
        st.stop()

    platform = st.selectbox(
        "Platform",
        ["google_trends", "youtube", "meta_ads"]
    )

    keyword = st.text_input("Keyword", "streetwear")
    geo = st.selectbox("Country", ["US", "CA", "GB", "AU"])
    timeframe = st.selectbox(
        "Timeframe",
        ["today 7-d", "today 90-d", "today 12-m", "today 5-y"]
    )

    if st.button("Run Research"):
        try:
            results = run_research(
                platform=platform,
                keyword=keyword,
                geo=geo,
                timeframe=timeframe,
                access_token=st.session_state["meta_access_token"],
            )
            st.session_state["research_results"] = results
            st.success("Research complete")

            if isinstance(results, list):
                st.dataframe(results)
            else:
                st.json(results)

        except Exception as e:
            st.error("Research failed")
            st.exception(e)

# =================================================
# 📣 CAMPAIGNS TAB
# =================================================
with tab_campaigns:
    st.subheader("Campaign Builder")

    if "meta_access_token" not in st.session_state:
        st.warning("Connect Meta Ads first")
        st.stop()

    accounts = fetch_ad_accounts(st.session_state["meta_access_token"]).get("data", [])

    if not accounts:
        st.warning("No ad accounts found")
        st.stop()

    acct_map = {
        acct.get("name", acct["id"]): acct["id"].replace("act_", "")
        for acct in accounts
    }

    selected_account = st.selectbox("Ad Account", list(acct_map.keys()))
    ad_account_id = acct_map[selected_account]

    campaign_name = st.text_input("Campaign Name", "My Campaign")
    objective = st.selectbox(
        "Objective",
        ["TRAFFIC", "LEAD_GENERATION", "OUTCOME_SALES", "OUTCOME_AWARENESS"]
    )
    daily_budget = st.number_input("Daily Budget ($)", 5, 1000, 10)

    if st.button("Create Campaign"):
        try:
            result = create_meta_campaign(
                access_token=st.session_state["meta_access_token"],
                ad_account_id=ad_account_id,
                name=campaign_name,
                objective=objective,
                daily_budget=int(daily_budget * 100),
            )
            st.session_state["campaign_id"] = result["id"]
            st.success("Campaign created")
            st.json(result)
        except Exception as e:
            st.error("Campaign failed")
            st.exception(e)

# =================================================
# 🎨 CREATIVE TAB
# =================================================
with tab_creative:
    st.subheader("Creative Builder")

    if "meta_access_token" not in st.session_state:
        st.warning("Connect Meta Ads first")
        st.stop()

    ad_account_id = st.text_input("Ad Account ID")
    page_id = st.text_input("Facebook Page ID")
    headline = st.text_input("Headline", "Shop the Drop")
    primary_text = st.text_area("Primary Text", "Limited stock. Tap now.")

    if st.button("Create Creative"):
        try:
            creative = create_meta_ad_creative(
                access_token=st.session_state["meta_access_token"],
                ad_account_id=ad_account_id,
                page_id=page_id,
                headline=headline,
                primary_text=primary_text,
            )
            st.success("Creative created")
            st.json(creative)
        except Exception as e:
            st.error("Creative failed")
            st.exception(e)

# =================================================
# 🧠 STRATEGY TAB (NEXT PHASE)
# =================================================
with tab_strategy:
    st.subheader("Strategy Engine (Coming Online)")

    st.info("""
    This tab will:
    • Turn research → targeting
    • Pick objectives automatically
    • Recommend budgets
    • Generate creatives with AI
    """)

    if "research_results" in st.session_state:
        st.success("Research data available for strategy engine")
        st.json(st.session_state["research_results"])
    else:
        st.warning("Run research first")