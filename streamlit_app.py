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
# IMPORT OAUTH MODULES
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
# APP TITLE
# =================================================
st.title("🚀 Marketing Bot")

st.caption(
    "Connect Meta and Google to unlock research, creatives, campaigns, and strategy — "
    "you can use either or both at the same time."
)

# =================================================
# SESSION STATE INIT
# =================================================
st.session_state.setdefault("meta_access_token", None)
st.session_state.setdefault("google_access_token", None)
st.session_state.setdefault("ad_account_id", None)

# =================================================
# READ QUERY PARAMS
# =================================================
query = st.query_params

# =================================================
# OAUTH CALLBACK HANDLER (SAFE)
# =================================================
if "code" in query and "state" in query:
    code = query["code"]
    state = query["state"]

    # META
    if state == "meta" and st.session_state["meta_access_token"] is None:
        try:
            token = exchange_code_for_token(code)
            st.session_state["meta_access_token"] = token
            st.success("✅ Meta connected successfully")
        except Exception as e:
            st.error("❌ Meta OAuth failed")
            st.exception(e)

    # GOOGLE
    if state == "google" and st.session_state["google_access_token"] is None:
        try:
            token = exchange_google_code_for_token(code)
            st.session_state["google_access_token"] = token["access_token"]
            st.success("✅ Google connected successfully")
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
# CONNECT BUTTONS
# =================================================
with st.expander("🔑 Connect Platforms", expanded=not (meta_connected or google_connected)):
    if not meta_connected:
        st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")
    else:
        st.success("Meta is connected")

    if not google_connected:
        st.markdown(f"[🟢 Sign in with Google]({google_login_url()})")
    else:
        st.success("Google is connected")

# =================================================
# META AD ACCOUNTS (TABLE VIEW)
# =================================================
if meta_connected:
    st.divider()
    st.subheader("📂 Meta Ad Accounts")

    try:
        accounts = fetch_ad_accounts(
            st.session_state["meta_access_token"]
        ).get("data", [])

        if not accounts:
            st.info("No ad accounts found for this Meta user.")
        else:
            df = pd.DataFrame(accounts)[["id", "name"]]
            df["Ad Account ID"] = df["id"].str.replace("act_", "", regex=False)
            df = df.drop(columns=["id"])

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

            selected_name = st.selectbox(
                "Select Active Ad Account",
                df["name"],
            )

            selected_id = df.loc[
                df["name"] == selected_name, "Ad Account ID"
            ].iloc[0]

            st.session_state["ad_account_id"] = selected_id
            st.success(f"Active Meta Ad Account: {selected_name}")

    except Exception as e:
        st.warning("Could not load Meta ad accounts")
        st.exception(e)

# =================================================
# MAIN APP TABS
# =================================================
st.divider()
tab_research, tab_creative, tab_campaigns, tab_strategy, tab_system = st.tabs(
    ["🔍 Research", "🎨 Creative", "📣 Campaigns", "🧠 Strategy", "🧰 System"]
)

# =================================================
# 🔍 RESEARCH TAB
# =================================================
with tab_research:
    st.subheader("Market Research")

    if not google_connected:
        st.info("Connect Google to enable research tools.")
    else:
        st.success("Google connected — research ready")

        st.markdown(
            """
            **Available research sources (next wiring):**
            - Google Trends
            - YouTube trends
            - Google keyword planning
            """
        )

# =================================================
# 🎨 CREATIVE TAB
# =================================================
with tab_creative:
    st.subheader("Creative Tools")

    st.markdown(
        """
        Generate headlines, primary text, and CTAs.
        You can generate creatives **without** Meta connected,
        but Meta is required to publish them.
        """
    )

    if meta_connected:
        st.success("Meta connected — publishing enabled")
    else:
        st.info("Connect Meta to publish creatives")

# =================================================
# 📣 CAMPAIGNS TAB
# =================================================
with tab_campaigns:
    st.subheader("Campaign Builder")

    if not meta_connected:
        st.warning("Connect Meta to create campaigns.")
    else:
        st.success("Meta connected — campaign creation ready")

        st.markdown(
            """
            **This tab will support:**
            - Campaign creation
            - Ad set creation
            - Creative assignment
            """
        )

# =================================================
# 🧠 STRATEGY TAB
# =================================================
with tab_strategy:
    st.subheader("Strategy & Budget Planning")

    st.markdown(
        """
        Strategy planning does **not** require OAuth.
        Use this section to plan budgets and channel allocation.
        """
    )

# =================================================
# 🧰 SYSTEM TAB
# =================================================
with tab_system:
    st.subheader("System Status")

    status_df = pd.DataFrame(
        [
            {"Component": "Meta OAuth", "Status": meta_connected},
            {"Component": "Google OAuth", "Status": google_connected},
            {"Component": "Ad Account Selected", "Status": bool(st.session_state.get("ad_account_id"))},
        ]
    )

    st.table(status_df)

    with st.expander("🔍 Session Debug"):
        st.json({k: bool(v) for k, v in st.session_state.items()})