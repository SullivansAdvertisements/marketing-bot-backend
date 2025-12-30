import streamlit as st
import pandas as pd

# =================================================
# MUST BE FIRST — MOBILE FRIENDLY
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
# GOOGLE OAUTH (SAFE IMPORT)
# =================================================
from oauth_google import (
    google_login_url,
    exchange_google_code_for_token,
)

# =================================================
# APP TITLE
# =================================================
st.title("🚀 Marketing Bot")

# =================================================
# QUERY PARAMS
# =================================================
query = st.experimental_get_query_params()

# =================================================
# META AUTH
# =================================================
st.subheader("🔵 Meta Authentication")

st.markdown(f"[Connect Meta Ads]({meta_login_url()})")

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

META_ACCESS_TOKEN = st.session_state["meta_access_token"]

# =================================================
# FETCH AD ACCOUNTS
# =================================================
accounts_response = fetch_ad_accounts(META_ACCESS_TOKEN)
accounts = accounts_response.get("data", [])

if not accounts:
    st.error("No ad accounts found.")
    st.stop()

account_df = pd.DataFrame(accounts)[["id", "name"]]
account_df["clean_id"] = account_df["id"].str.replace("act_", "")

selected_row = st.selectbox(
    "Active Ad Account",
    account_df["name"]
)

selected_account_id = account_df.loc[
    account_df["name"] == selected_row, "clean_id"
].iloc[0]

st.session_state["ad_account_id"] = selected_account_id

# =================================================
# GOOGLE AUTH (SAFE — NO CRASH)
# =================================================
st.divider()
st.subheader("🟢 Google Authentication")

try:
    google_login = google_login_url()
    st.markdown(f"[Sign in with Google]({google_login})")

    if "code" in query and "google_access_token" not in st.session_state:
        try:
            token = exchange_google_code_for_token(query["code"][0])
            st.session_state["google_access_token"] = token["access_token"]
            st.success("Google connected successfully")
        except Exception as e:
            st.error("Google OAuth failed")
            st.exception(e)

except Exception:
    st.info("Google OAuth not configured yet.")

# =================================================
# MAIN TABS
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
            try:
                results = run_research(
                    platform=platform,
                    keyword=keyword,
                    geo=geo,
                    timeframe=timeframe,
                    access_token=st.session_state.get("google_access_token"),
                )

                if isinstance(results, list) and results:
                    st.dataframe(pd.DataFrame(results), use_container_width=True)
                elif isinstance(results, dict):
                    st.dataframe(pd.DataFrame([results]))
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

    st.divider()
    st.subheader("Push Creative to Meta")

    page_id = st.text_input("Facebook Page ID")
    destination_url = st.text_input("Destination URL")

    if st.button("Create Meta Creative"):
        creative = st.session_state.get("creative")

        if not creative:
            st.warning("Generate creative first")
        else:
            result = create_meta_ad_creative(
                access_token=META_ACCESS_TOKEN,
                ad_account_id=selected_account_id,
                page_id=page_id,
                headline=creative["headline"],
                primary_text=creative["primary_text"],
                destination_url=destination_url,
            )

            st.success("Meta creative created")
            st.json(result)

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

    st.write("Meta Connected:", True)
    st.write("Google Connected:", bool(st.session_state.get("google_access_token")))
    st.write("Ad Account:", st.session_state.get("ad_account_id"))
    st.write("Creative Cached:", bool(st.session_state.get("creative")))