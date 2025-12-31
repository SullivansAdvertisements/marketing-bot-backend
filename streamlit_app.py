import streamlit as st
import pandas as pd

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =================================================
# OAUTH IMPORTS (ROOT FILES)
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
# APP HEADER
# =================================================
st.title("🚀 Marketing Bot")
st.caption(
    "Research, creatives, campaigns, and strategy. "
    "You can connect Meta and Google in any order."
)

# =================================================
# SESSION STATE INIT (CRITICAL)
# =================================================
st.session_state.setdefault("meta_access_token", None)
st.session_state.setdefault("google_access_token", None)
st.session_state.setdefault("ad_account_id", None)
st.session_state.setdefault("active_tab", "Research")
st.session_state.setdefault("research_df", None)
st.session_state.setdefault("last_keyword", "")

# =================================================
# READ QUERY PARAMS
# =================================================
query = st.query_params

# =================================================
# OAUTH CALLBACK HANDLER (STATE-AWARE, ONCE)
# =================================================
if "code" in query and "state" in query:
    code = query["code"]
    state = query["state"]

    # ---- META CALLBACK ----
    if state == "meta" and st.session_state["meta_access_token"] is None:
        try:
            meta_token = exchange_code_for_token(code)
            st.session_state["meta_access_token"] = meta_token
            st.success("✅ Meta connected")
        except Exception as e:
            st.error("❌ Meta OAuth failed")
            st.exception(e)

    # ---- GOOGLE CALLBACK ----
    if state == "google" and st.session_state["google_access_token"] is None:
        try:
            google_token = exchange_google_code_for_token(code)
            st.session_state["google_access_token"] = google_token["access_token"]
            st.success("✅ Google connected")
        except Exception as e:
            st.error("❌ Google OAuth failed")
            st.exception(e)

# =================================================
# CONNECTION STATUS
# =================================================
meta_connected = st.session_state["meta_access_token"] is not None
google_connected = st.session_state["google_access_token"] is not None

st.subheader("🔐 Connection Status")
c1, c2 = st.columns(2)
c1.metric("Meta Ads", "Connected" if meta_connected else "Not connected")
c2.metric("Google", "Connected" if google_connected else "Not connected")

# =================================================
# CONNECT BUTTONS (DO NOT RESET STATE)
# =================================================
with st.expander("🔑 Connect Platforms", expanded=not (meta_connected or google_connected)):
    if not meta_connected:
        st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")
    else:
        st.success("Meta already connected")

    if not google_connected:
        st.markdown(f"[🟢 Sign in with Google]({google_login_url()})")
    else:
        st.success("Google already connected")

# =================================================
# META AD ACCOUNTS (TABLE)
# =================================================
if meta_connected:
    st.divider()
    st.subheader("📂 Meta Ad Accounts")

    try:
        accounts = fetch_ad_accounts(
            st.session_state["meta_access_token"]
        ).get("data", [])

        if accounts:
            df_accounts = pd.DataFrame(accounts)[["id", "name"]]
            df_accounts["Ad Account ID"] = df_accounts["id"].str.replace(
                "act_", "", regex=False
            )
            df_accounts = df_accounts.drop(columns=["id"])

            st.dataframe(
                df_accounts,
                use_container_width=True,
                hide_index=True,
            )

            selected_name = st.selectbox(
                "Select Active Ad Account",
                df_accounts["name"],
            )

            selected_id = df_accounts.loc[
                df_accounts["name"] == selected_name, "Ad Account ID"
            ].iloc[0]

            st.session_state["ad_account_id"] = selected_id
            st.success(f"Active Meta Account: {selected_name}")

        else:
            st.info("No Meta ad accounts found.")

    except Exception as e:
        st.warning("Failed to load Meta ad accounts")
        st.exception(e)

# =================================================
# MAIN TABS (PERSISTENT)
# =================================================
tabs = ["Research", "Creative", "Campaigns", "Strategy", "System"]
active_index = tabs.index(st.session_state["active_tab"])

tab_research, tab_creative, tab_campaigns, tab_strategy, tab_system = st.tabs(tabs)

# =================================================
# 🔍 RESEARCH TAB (PERSISTENT TABLES)
# =================================================
with tab_research:
    st.session_state["active_tab"] = "Research"

    st.subheader("🔍 Market Research")

    col1, col2, col3 = st.columns(3)

    with col1:
        platform = st.selectbox(
            "Platform",
            ["Google Trends", "YouTube", "Google Keywords"],
        )

    with col2:
        keyword = st.text_input(
            "Keyword",
            value=st.session_state["last_keyword"],
            placeholder="streetwear, fitness, skincare",
        )

    with col3:
        geo = st.selectbox("Country", ["US", "CA", "GB", "AU"])

    timeframe = st.selectbox(
        "Timeframe",
        ["7 days", "90 days", "12 months", "5 years"],
    )

    if st.button("📊 Run Research", use_container_width=True):
        if not keyword:
            st.warning("Enter a keyword")
        elif not google_connected:
            st.warning("Connect Google to run research")
        else:
            # 🔧 Replace this with your real research engine
            dummy_results = [
                {"keyword": keyword, "metric": "Interest", "value": 72},
                {"keyword": keyword, "metric": "Trend Score", "value": 88},
                {"keyword": keyword, "metric": "Competition", "value": "Medium"},
            ]

            df = pd.DataFrame(dummy_results)
            st.session_state["research_df"] = df
            st.session_state["last_keyword"] = keyword

    if st.session_state["research_df"] is not None:
        st.divider()
        st.subheader("📈 Research Results")

        st.dataframe(
            st.session_state["research_df"],
            use_container_width=True,
            height=380,
        )

        with st.expander("⬇️ Export Results"):
            st.download_button(
                "Download CSV",
                st.session_state["research_df"].to_csv(index=False),
                file_name="research_results.csv",
                mime="text/csv",
            )

# =================================================
# 🎨 CREATIVE TAB
# =================================================
with tab_creative:
    st.session_state["active_tab"] = "Creative"

    st.subheader("🎨 Creative")
    st.info("Creative tools stay available regardless of OAuth order.")

# =================================================
# 📣 CAMPAIGNS TAB
# =================================================
with tab_campaigns:
    st.session_state["active_tab"] = "Campaigns"

    st.subheader("📣 Campaigns")

    if meta_connected:
        st.success("Meta connected — campaigns enabled")
    else:
        st.info("Connect Meta to create campaigns")

# =================================================
# 🧠 STRATEGY TAB
# =================================================
with tab_strategy:
    st.session_state["active_tab"] = "Strategy"

    st.subheader("🧠 Strategy")
    st.info("Strategy planning does not require OAuth.")

# =================================================
# 🧰 SYSTEM TAB
# =================================================
with tab_system:
    st.session_state["active_tab"] = "System"

    st.subheader("🧰 System Status")

    status_df = pd.DataFrame(
        [
            {"Component": "Meta OAuth", "Connected": meta_connected},
            {"Component": "Google OAuth", "Connected": google_connected},
            {
                "Component": "Ad Account Selected",
                "Connected": bool(st.session_state.get("ad_account_id")),
            },
            {
                "Component": "Research Cached",
                "Connected": st.session_state["research_df"] is not None,
            },
        ]
    )

    st.table(status_df)

    with st.expander("🔍 Session Debug"):
        st.json({k: bool(v) for k, v in st.session_state.items()})