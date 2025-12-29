import streamlit as st

# ================================
# Meta OAuth (repo root)
# ================================
from oauth_meta import (
    meta_login_url,
    exchange_code_for_token,
    fetch_ad_accounts,
)

# ================================
# Google OAuth (optional / safe)
# ================================
GOOGLE_OAUTH_AVAILABLE = False

try:
    from google_oauth import (
        google_login_url,
        exchange_google_code_for_token,
    )
    GOOGLE_OAUTH_AVAILABLE = True
except Exception as e:
    GOOGLE_OAUTH_AVAILABLE = False
# =================================================
# APP TITLE
# =================================================
st.title("🚀 Marketing Bot")

# =================================================
# GLOBAL QUERY PARAMS (USED BY BOTH OAUTH FLOWS)
# =================================================
query = st.experimental_get_query_params()

# =================================================
# 🔐 AUTH HANDLING (META + GOOGLE)
# =================================================
with st.sidebar:
    st.subheader("🔐 Authentication")

    # -------- META OAUTH --------
    st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")

    if "code" in query and "meta_access_token" not in st.session_state:
        try:
            meta_token = exchange_code_for_token(query["code"][0])
            st.session_state["meta_access_token"] = meta_token
            st.success("Meta connected")
        except Exception:
            pass

    # -------- GOOGLE OAUTH --------
    st.markdown("---")
    st.markdown(f"[🟢 Sign in with Google]({google_login_url()})")

    if "code" in query and "google_user" not in st.session_state:
        try:
            user = exchange_google_code(query["code"][0])
            st.session_state["google_user"] = user
            st.success(f"Signed in as {user['email']}")
        except Exception:
            pass

# =================================================
# REQUIRE META AUTH TO CONTINUE
# =================================================
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
# MAIN TABS
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
    st.subheader("Connected Accounts")

    if "google_user" in st.session_state:
        user = st.session_state["google_user"]
        st.image(user.get("picture"), width=64)
        st.write(user.get("name"))
        st.caption(user.get("email"))
    else:
        st.warning("Not signed in with Google")

    selected_account = st.selectbox(
        "Active Meta Ad Account",
        list(account_map.keys())
    )

    st.session_state["ad_account_id"] = account_map[selected_account]
    st.success(f"Using Meta account: {selected_account}")

# =================================================
# 🔍 RESEARCH TAB (TABLES)
# =================================================
with tab_research:
    from app.research.router import run_research

    st.subheader("🔍 Market Research")

    platform = st.selectbox(
        "Platform",
        ["google_trends", "youtube", "meta_ads"]
    )

    keyword = st.text_input("Keyword / Topic")
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

        st.success("Research completed")

        if isinstance(results, list) and results:
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True, hide_index=True)

            with st.expander("🔎 Raw Data"):
                st.json(results)
        else:
            st.warning("No data returned")

# =================================================
# 🎨 CREATIVE TAB
# =================================================
with tab_creative:
    from app.creative.router import generate_creative
    from app.creative.meta_creatives import create_meta_ad_creative

    st.subheader("🎨 Creative Generator")

    product = st.text_input("Product", "Streetwear Hoodie")
    audience = st.text_input("Audience", "Streetwear fans 18–30")
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
        st.markdown(f"### {creative['headline']}")
        st.write(creative["primary_text"])

        col1, col2 = st.columns(2)
        col1.metric("CTA", creative["cta"])
        col2.metric("Source", creative["source"].upper())

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

            with st.expander("📦 Meta API Response"):
                st.json(result)

# =================================================
# 📣 CAMPAIGNS TAB
# =================================================
with tab_campaigns:
    st.subheader("📣 Campaign Builder")
    st.info("Meta campaign automation ready to wire.")

# =================================================
# 🧠 STRATEGY TAB
# =================================================
with tab_strategy:
    from app.strategy.router import generate_strategy

    st.subheader("🧠 Strategy Planner")

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

        alloc_df = pd.DataFrame(
            strategy["allocation"].items(),
            columns=["Platform", "Budget ($)"]
        )

        st.subheader("💰 Budget Allocation")
        st.dataframe(alloc_df, use_container_width=True)
        st.bar_chart(alloc_df.set_index("Platform"))

        st.subheader("📊 Projections")
        st.dataframe(
            pd.DataFrame(strategy["projections"]).T,
            use_container_width=True
        )

# =================================================
# 🧰 SYSTEM TAB
# =================================================
with tab_utils:
    st.subheader("🧰 System Status")

    st.metric("Meta Connected", "Yes")
    st.metric("Google Signed In", "Yes" if "google_user" in st.session_state else "No")
    st.metric("Creative Cached", bool(st.session_state.get("last_creative")))

    st.subheader("🔐 Environment")
    st.write({
        "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY")),
        "YOUTUBE_API_KEY": bool(os.getenv("YOUTUBE_API_KEY")),
        "GOOGLE_CLIENT_ID": bool(os.getenv("GOOGLE_CLIENT_ID")),
    })