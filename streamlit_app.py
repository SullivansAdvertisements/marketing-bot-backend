import streamlit as st
import pandas as pd

# =================================================
# MUST BE FIRST — STREAMLIT CONFIG
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =================================================
# IMPORTS — OAUTH (ROOT FILES)
# =================================================
from oauth_meta import (
    meta_login_url,
    exchange_code_for_token,
    fetch_ad_accounts,
)
from oauth_google import (
    google_login_url,
    exchange_google_code_for_token,
)
# =================================================
# IMPORTS — OAUTH (ROOT FILES)
# =================================================
from oauth_meta import meta_login_url, exchange_code_for_token, fetch_ad_accounts
from oauth_google import google_login_url, exchange_google_code_for_token
import streamlit as st

# 1️⃣ Page config (MUST be first Streamlit call)
st.set_page_config(...)

# 2️⃣ Imports
from oauth_meta import ...
from oauth_google import ...

# 🔥 3️⃣ STEP 2 GOES HERE (OAuth handler)
#    👇👇👇👇👇👇👇👇👇👇

query = st.experimental_get_query_params()
code = query.get("code", [None])[0]
state = query.get("state", [None])[0]

if code and state == "meta" and "meta_access_token" not in st.session_state:
    token = exchange_code_for_token(code)
    st.session_state["meta_access_token"] = token
    st.experimental_set_query_params()

if code and state == "google" and "google_access_token" not in st.session_state:
    token = exchange_google_code_for_token(code)
    st.session_state["google_access_token"] = token["access_token"]
    st.experimental_set_query_params()

# ⛔ NOTHING ABOVE THIS SHOULD USE st.title(), tabs, sidebar, etc.

# 4️⃣ Now UI starts
st.title("🚀 Marketing Bot")

# 5️⃣ Tabs
tab_auth, tab_research, tab_creative = st.tabs(...)
# =================================================
# APP TITLE
# =================================================
st.title("🚀 Marketing Bot")

# =================================================
# QUERY PARAMS (OAUTH CALLBACK)
# =================================================
query = st.experimental_get_query_params()
oauth_code = query.get("code", [None])[0]
oauth_state = query.get("state", [None])[0]

# =================================================
# AUTH STATUS
# =================================================
meta_connected = "meta_access_token" in st.session_state
google_connected = "google_access_token" in st.session_state

# =================================================
# 🔵 STEP 1 — META AUTH
# =================================================
st.subheader("🔵 Step 1: Connect Meta Ads")

if not meta_connected:
    st.markdown(f"[Connect Meta Ads]({meta_login_url()})")

    if oauth_code and oauth_state == "meta":
        try:
            token = exchange_code_for_token(oauth_code)
            st.session_state["meta_access_token"] = token
            st.success("Meta connected successfully")
            st.experimental_set_query_params()  # clear URL
            st.rerun()
        except Exception as e:
            st.error("Meta OAuth failed")
            st.exception(e)

# =================================================
# 🟢 STEP 2 — GOOGLE AUTH (ALWAYS RENDERS)
# =================================================
st.divider()
st.subheader("🟢 Step 2: Connect Google")

if not google_connected:
    st.markdown(f"[Sign in with Google]({google_login_url()})")

    if oauth_code and oauth_state == "google":
        try:
            token = exchange_google_code_for_token(oauth_code)
            st.session_state["google_access_token"] = token["access_token"]
            st.success("Google connected successfully")
            st.experimental_set_query_params()  # clear URL
            st.rerun()
        except Exception as e:
            st.error("Google OAuth failed")
            st.exception(e)

# =================================================
# 🚫 HARD GATE — BOTH REQUIRED
# =================================================
if not meta_connected or not google_connected:
    st.info("Connect both Meta and Google to unlock the app.")
    st.stop()

# =================================================
# ✅ AUTH COMPLETE
# =================================================
st.success("✅ Meta & Google connected — App unlocked")

META_ACCESS_TOKEN = st.session_state["meta_access_token"]
GOOGLE_ACCESS_TOKEN = st.session_state["google_access_token"]

# =================================================
# FETCH META AD ACCOUNTS
# =================================================
accounts_response = fetch_ad_accounts(META_ACCESS_TOKEN)
accounts = accounts_response.get("data", [])

if not accounts:
    st.error("No Meta ad accounts found.")
    st.stop()

df = pd.DataFrame(accounts)[["id", "name"]]
df["clean_id"] = df["id"].str.replace("act_", "")

selected_account = st.selectbox("Active Meta Ad Account", df["name"])
st.session_state["ad_account_id"] = df.loc[
    df["name"] == selected_account, "clean_id"
].iloc[0]

# =================================================
# MAIN APP TABS
# =================================================
tab_research, tab_creative, tab_strategy, tab_system = st.tabs(
    ["🔍 Research", "🎨 Creative", "🧠 Strategy", "🧰 System"]
)

# =================================================
# 🔍 RESEARCH TAB
# =================================================
with tab_research:
    from app.research.router import run_research

    st.subheader("Market Research")

    platform = st.selectbox(
        "Platform",
        ["google_trends", "youtube", "meta_ads"]
    )
    keyword = st.text_input("Keyword")
    geo = st.selectbox("Country", ["US", "CA", "GB", "AU"])
    timeframe = st.selectbox(
        "Timeframe",
        ["today 7-d", "today 90-d", "today 12-m", "today 5-y"]
    )

    if st.button("Run Research"):
        if not keyword:
            st.warning("Enter a keyword")
        else:
            results = run_research(
                platform=platform,
                keyword=keyword,
                geo=geo,
                timeframe=timeframe,
                access_token=GOOGLE_ACCESS_TOKEN,
            )

            if isinstance(results, list):
                st.dataframe(pd.DataFrame(results), use_container_width=True)
            else:
                st.json(results)

# =================================================
# 🎨 CREATIVE TAB
# =================================================
with tab_creative:
    from app.creative.router import generate_creative

    st.subheader("Creative Generator")

    product = st.text_input("Product")
    audience = st.text_input("Audience")
    goal = st.selectbox("Goal", ["sales", "leads", "traffic"])
    tone = st.selectbox("Tone", ["bold", "friendly", "premium"])
    platform_choice = st.selectbox("Platform", ["meta", "tiktok", "youtube"])

    if st.button("Generate Creative"):
        creative = generate_creative(
            product=product,
            audience=audience,
            goal=goal,
            tone=tone,
            platform=platform_choice,
        )
        st.session_state["creative"] = creative
        st.dataframe(pd.DataFrame([creative]))

# =================================================
# 🧠 STRATEGY TAB
# =================================================
with tab_strategy:
    from app.strategy.router import generate_strategy

    st.subheader("Budget Strategy")

    budget = st.number_input("Monthly Budget ($)", 100, 100000, 1000)
    objective = st.selectbox("Objective", ["awareness", "traffic", "sales"])
    risk = st.selectbox("Risk Level", ["conservative", "balanced", "aggressive"])
    aov = st.number_input("Average Order Value", 1, 1000, 50)

    if st.button("Generate Strategy"):
        strategy = generate_strategy(
            total_budget=budget,
            objective=objective,
            risk_level=risk,
            average_order_value=aov,
        )

        st.dataframe(
            pd.DataFrame(strategy["allocation"].items(),
                         columns=["Platform", "Budget"])
        )

# =================================================
# 🧰 SYSTEM TAB
# =================================================
with tab_system:
    st.subheader("System Status")

    st.write("Meta Connected:", meta_connected)
    st.write("Google Connected:", google_connected)
    st.write("Ad Account:", st.session_state.get("ad_account_id"))