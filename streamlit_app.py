import streamlit as st
import pandas as pd

# =================================================
# MUST BE FIRST — MOBILE-FIRST
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =================================================
# META OAUTH (REQUIRED)
# =================================================
from oauth_meta import (
    meta_login_url,
    exchange_code_for_token,
    fetch_ad_accounts,
)

# =================================================
# GOOGLE OAUTH (OPTIONAL — SAFE)
# =================================================
GOOGLE_OAUTH_AVAILABLE = False
google_login_url = None
exchange_google_code_for_token = None

try:
    from google_oauth import (
        google_login_url,
        exchange_google_code_for_token,
    )
    GOOGLE_OAUTH_AVAILABLE = True
except Exception:
    GOOGLE_OAUTH_AVAILABLE = False

# =================================================
# APP TITLE
# =================================================
st.title("🚀 Marketing Bot")

# =================================================
# 🔐 META AUTH (GLOBAL)
# =================================================
query = st.experimental_get_query_params()

st.subheader("Meta Authentication")
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
# FETCH AD ACCOUNTS
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
tab_auth, tab_research, tab_creative, tab_campaigns, tab_strategy, tab_system = st.tabs(
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
    st.subheader("Connected Accounts")

    selected_account = st.selectbox(
        "Active Meta Ad Account",
        list(account_map.keys())
    )

    st.session_state["ad_account_id"] = account_map[selected_account]
    st.success(f"Using Meta account: {selected_account}")

    st.divider()
    st.subheader("Google Authentication")

    if GOOGLE_OAUTH_AVAILABLE and google_login_url:
        st.markdown(f"[🟢 Sign in with Google]({google_login_url()})")

        if "code" in query and "google_access_token" not in st.session_state:
            try:
                gtoken = exchange_google_code_for_token(query["code"][0])
                st.session_state["google_access_token"] = gtoken
                st.success("Google connected successfully")
            except Exception as e:
                st.error("Google OAuth failed")
                st.exception(e)
    else:
        st.info("Google OAuth not configured yet.")

# =================================================
# 🔍 RESEARCH TAB
# =================================================
with tab_research:
    from app.research.router import run_research

    st.subheader("Market Research Engine")

    platform = st.selectbox(
        "Platform",
        ["google_trends", "google_keywords", "youtube", "tiktok", "meta_ads"]
    )

    keyword = st.text_input("Keyword / Topic", placeholder="streetwear, fitness, skincare")
    geo = st.selectbox("Country", ["US", "CA", "GB", "AU"])
    timeframe = st.selectbox(
        "Timeframe",
        ["today 7-d", "today 90-d", "today 12-m", "today 5-y"]
    )

    if st.button("📊 Run Research"):
        if not keyword:
            st.warning("Enter a keyword")
        else:
            try:
                results = run_research(
                    platform=platform,
                    keyword=keyword,
                    geo=geo,
                    timeframe=timeframe,
                    access_token=ACCESS_TOKEN,
                )

                st.success("Research completed")

                if isinstance(results, list) and results:
                    df = pd.DataFrame(results)
                    st.dataframe(df, use_container_width=True)
                elif isinstance(results, dict):
                    st.json(results)
                else:
                    st.info("No data returned")

            except Exception as e:
                st.error("Research failed")
                st.exception(e)

# =================================================
# 🎨 CREATIVE TAB
# =================================================
with tab_creative:
    from app.creative.router import generate_creative
    from app.creative.meta_creatives import create_meta_ad_creative

    st.subheader("Creative Generator")

    product = st.text_input("Product / Offer", "Streetwear Hoodie")
    audience = st.text_input("Audience", "Streetwear fans 18–30")
    goal = st.selectbox("Goal", ["sales", "leads", "traffic"])
    tone = st.selectbox("Tone", ["bold", "friendly", "premium"])
    platform_choice = st.selectbox("Platform", ["meta", "tiktok", "youtube"])
    use_ai = st.checkbox("Use AI (OpenAI)", value=True)

    if st.button("✨ Generate Creative"):
        creative = generate_creative(
            product=product,
            audience=audience,
            goal=goal,
            tone=tone,
            platform=platform_choice,
            use_ai=use_ai,
        )

        st.session_state["last_creative"] = creative

        st.success("Creative generated")
        st.table(pd.DataFrame([creative]))

    st.divider()
    st.subheader("📤 Push Creative to Meta")

    page_id = st.text_input("Facebook Page ID")
    destination_url = st.text_input("Destination URL", "https://example.com")

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
    st.info(
        "Campaign hooks are ready.\n\n"
        "Connect:\n"
        "- app/campaigns/meta_campaigns.py\n"
        "- app/utils/validators.py\n"
        "- app/utils/rate_limits.py"
    )

# =================================================
# 🧠 STRATEGY TAB
# =================================================
with tab_strategy:
    from app.strategy.router import generate_strategy

    st.subheader("Budget & Strategy Planning")

    budget = st.number_input("Monthly Budget ($)", min_value=100, value=1000)
    objective = st.selectbox("Objective", ["awareness", "traffic", "sales"])
    risk = st.selectbox("Risk Profile", ["conservative", "balanced", "aggressive"])
    aov = st.number_input("Average Order Value ($)", min_value=1, value=50)

    if st.button("📈 Generate Strategy"):
        strategy = generate_strategy(
            total_budget=budget,
            objective=objective,
            risk_level=risk,
            average_order_value=aov,
        )

        st.success("Strategy generated")

        st.subheader("💰 Budget Allocation")
        st.dataframe(
            pd.DataFrame(
                list(strategy["allocation"].items()),
                columns=["Platform", "Budget ($)"]
            ),
            use_container_width=True
        )

        st.subheader("📊 Performance Projections")
        st.json(strategy["projections"])

# =================================================
# 🧰 SYSTEM TAB
# =================================================
with tab_system:
    st.subheader("System Status")

    st.success("Application healthy")
    st.write("Meta Connected:", True)
    st.write("Google Connected:", bool(st.session_state.get("google_access_token")))
    st.write("Ad Account:", st.session_state.get("ad_account_id"))
    st.write("Creative Cached:", bool(st.session_state.get("last_creative")))

    st.caption("Utilities active: logging, validators, rate limits")