import streamlit as st

# =================================================
# MUST BE FIRST
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="centered",  # MOBILE-FIRST
    initial_sidebar_state="collapsed",
)

# =================================================
# CORE IMPORTS (SAFE AT TOP)
# =================================================
from oauth_meta import (
    meta_login_url,
    exchange_code_for_token,
    fetch_ad_accounts,
)

# =================================================
# APP TITLE
# =================================================
st.title("🚀 Marketing Bot")

# =================================================
# META AUTH (GLOBAL CONTEXT)
# =================================================
query = st.experimental_get_query_params()

st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")

if "code" in query and "meta_access_token" not in st.session_state:
    try:
        token = exchange_code_for_token(query["code"][0])
        st.session_state["meta_access_token"] = token
        st.success("Meta connected successfully")
    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)

if "meta_access_token" not in st.session_state:
    st.warning("Connect Meta Ads to unlock the app.")
    st.stop()

ACCESS_TOKEN = st.session_state["meta_access_token"]

# =================================================
# FETCH AD ACCOUNTS (GLOBAL)
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
# MAIN TABS (MOBILE SAFE)
# =================================================
tab_auth, tab_research, tab_creative, tab_campaigns, tab_strategy, tab_utils = st.tabs(
    [
        "🔐 Auth",
        "🔍 Research",
        "🎨 Creative",
        "📣 Campaigns",
        "🧠 Strategy",
        "🧰 System",
    ]
)

# =================================================
# 🔐 AUTH TAB
# =================================================
with tab_auth:
    st.subheader("Connected Ad Accounts")

    selected_account_name = st.selectbox(
        "Active Ad Account",
        list(account_map.keys())
    )

    st.session_state["ad_account_id"] = account_map[selected_account_name]

    st.success(f"Using account: {selected_account_name}")

# =================================================
# 🔍 RESEARCH TAB
# =================================================
with tab_research:
    from app.research.router import run_research

    st.subheader("Market Research")

    platform = st.selectbox(
        "Platform",
        ["google_trends", "google_keywords", "youtube", "tiktok", "meta_ads"]
    )

    keyword = st.text_input("Keyword", placeholder="streetwear, gym wear")

    geo = st.selectbox("Country", ["US", "CA", "GB", "AU"])

    timeframe = st.selectbox(
        "Timeframe",
        ["today 7-d", "today 90-d", "today 12-m", "today 5-y"]
    )

    if st.button("📊 Run Research"):
        if not keyword:
            st.warning("Enter a keyword")
            st.stop()

        results = run_research(
            platform=platform,
            keyword=keyword,
            geo=geo,
            timeframe=timeframe,
            access_token=ACCESS_TOKEN,
        )

        st.session_state["research_results"] = results
        st.success("Research completed")

        if isinstance(results, list):
            for row in results[:10]:
                st.json(row)
        else:
            st.json(results)

# =================================================
# 🎨 CREATIVE TAB
# =================================================
with tab_creative:
    from app.creative.router import generate_creative
    from app.creative.meta_creatives import create_meta_ad_creative

    st.subheader("Ad Creative Generator")

    product = st.text_input("Product")
    audience = st.text_input("Audience")
    goal = st.selectbox("Goal", ["sales", "leads", "traffic"])
    tone = st.selectbox("Tone", ["bold", "friendly", "premium"])
    platform = st.selectbox("Platform", ["meta", "tiktok", "youtube"])
    use_ai = st.checkbox("Use AI (OpenAI)", value=True)

    if st.button("✨ Generate Creative"):
        creative = generate_creative(
            product=product,
            audience=audience,
            goal=goal,
            tone=tone,
            platform=platform,
            use_ai=use_ai,
        )

        st.session_state["last_creative"] = creative

        st.success("Creative generated")
        st.metric("Headline", creative["headline"])
        st.write(creative["primary_text"])
        st.caption(f"CTA: {creative['cta']} | Source: {creative['source']}")

    st.divider()
    st.subheader("📤 Push to Meta")

    page_id = st.text_input("Facebook Page ID")
    destination_url = st.text_input("Destination URL")

    if st.button("🚀 Create Meta Creative"):
        creative = st.session_state.get("last_creative")

        if not creative:
            st.warning("Generate creative first")
        else:
            result = create_meta_ad_creative(
                access_token=ACCESS_TOKEN,
                ad_account_id=st.session_state["ad_account_id"],
                page_id=page_id,
                headline=creative["headline"],
                primary_text=creative["primary_text"],
                destination_url=destination_url,
            )

            st.success("Meta Creative Created")
            st.json(result)

# =================================================
# 📣 CAMPAIGNS TAB
# =================================================
with tab_campaigns:
    st.subheader("Campaign Builder")
    st.info("Campaign creation wired separately (Meta Ads API ready).")

# =================================================
# 🧠 STRATEGY TAB
# =================================================
with tab_strategy:
    from app.strategy.router import generate_strategy

    st.subheader("Budget & Strategy Planning")

    budget = st.number_input("Monthly Budget ($)", 100, value=1000)
    objective = st.selectbox("Objective", ["awareness", "traffic", "sales"])
    risk = st.selectbox("Risk Profile", ["conservative", "balanced", "aggressive"])
    aov = st.number_input("Average Order Value", 1, value=50)

    if st.button("📈 Generate Strategy"):
        strategy = generate_strategy(
            total_budget=budget,
            objective=objective,
            risk_level=risk,
            average_order_value=aov,
        )

        st.success("Strategy generated")
        st.bar_chart(strategy["allocation"])
        st.json(strategy["projections"])

# =================================================
# 🧰 SYSTEM TAB
# =================================================
with tab_utils:
    st.subheader("System Status")
    st.success("App running normally")
    st.write("Meta connected:", True)
    st.write("Ad Account:", st.session_state.get("ad_account_id"))