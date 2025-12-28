import streamlit as st

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
with tab_research:
    st.header("🔍 Research Engine")

    st.info("Research module ready. Wiring comes next.")

    st.markdown("""
    This tab will use:
    - app/research/google_trends.py
    - app/research/youtube_trends.py
    - app/research/meta_ad_library.py
    """)

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

    st.subheader("Generated Creative")
    st.success(f"Headline: {creative['headline']}")
    st.write(creative["primary_text"])
    st.info(f"CTA: {creative['cta']}")
    st.caption(f"Source: {creative['source']}")

    st.session_state["last_creative"] = creative
# =================================================
# STRATEGY TAB (PLACEHOLDER – SAFE)
# =================================================
with tab_strategy:
    st.header("🧠 Strategy Engine")

    st.info("Strategy logic ready for wiring.")

    st.markdown("""
    This tab will use:
    - app/strategy/*
    - Research + Performance signals
    """)

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