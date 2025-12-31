import streamlit as st
import pandas as pd

# =================================================
# PAGE CONFIG (MOBILE SAFE)
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

query = st.query_params

# ---- Initialize once ----
st.session_state.setdefault("meta_access_token", None)
st.session_state.setdefault("google_access_token", None)

# ---- OAuth callback ----
if "code" in query and "state" in query:
    code = query["code"]
    state = query["state"]

    # META
    if state == "meta" and st.session_state["meta_access_token"] is None:
        from oauth_meta import exchange_code_for_token
        try:
            meta_token = exchange_code_for_token(code)
            st.session_state["meta_access_token"] = meta_token
        except Exception as e:
            st.session_state["meta_error"] = str(e)

    # GOOGLE
    if state == "google" and st.session_state["google_access_token"] is None:
        from oauth_google import exchange_google_code_for_token
        try:
            google_token = exchange_google_code_for_token(code)
            st.session_state["google_access_token"] = google_token["access_token"]
        except Exception as e:
            st.session_state["google_error"] = str(e)

# =================================================
# APP HEADER
# =================================================
st.title("🚀 Marketing Bot")

# =================================================
# READ QUERY PARAMS (NON-EXPERIMENTAL)
# =================================================
query = st.query_params

# -------------------------------
# META CALLBACK
# -------------------------------
if (
    "code" in query
    and query.get("state") == "meta"
    and "meta_access_token" not in st.session_state
):
    try:
        from oauth_meta import exchange_code_for_token
        token = exchange_code_for_token(query["code"])
        st.session_state["meta_access_token"] = token
    except Exception as e:
        st.session_state["meta_error"] = str(e)

# -------------------------------
# GOOGLE CALLBACK
# -------------------------------
if (
    "code" in query
    and query.get("state") == "google"
    and "google_access_token" not in st.session_state
):
    try:
        from oauth_google import exchange_google_code_for_token
        token = exchange_google_code_for_token(query["code"])
        st.session_state["google_access_token"] = token["access_token"]
    except Exception as e:
        st.session_state["google_error"] = str(e)
# =================================================
# CONNECTION STATUS
# =================================================
meta_connected = "meta_access_token" in st.session_state
google_connected = "google_access_token" in st.session_state

st.subheader("🔐 Connection Status")

col1, col2 = st.columns(2)
col1.metric("Meta Connected", meta_connected)
col2.metric("Google Connected", google_connected)

# =================================================
# LOGIN BUTTONS (ALWAYS VISIBLE)
# =================================================
st.divider()
st.subheader("🔑 Connect Accounts")

if not meta_connected:
    st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")

if not google_connected:
    st.markdown(f"[🟢 Sign in with Google]({google_login_url()})")

# =================================================
# FETCH META AD ACCOUNTS (ONLY IF CONNECTED)
# =================================================
if meta_connected:
    try:
        accounts_response = fetch_ad_accounts(st.session_state["meta_access_token"])
        accounts = accounts_response.get("data", [])

        if accounts:
            df = pd.DataFrame(accounts)[["id", "name"]]
            df["clean_id"] = df["id"].str.replace("act_", "", regex=False)

            selected = st.selectbox("Active Meta Ad Account", df["name"])
            selected_id = df.loc[df["name"] == selected, "clean_id"].iloc[0]

            st.session_state["ad_account_id"] = selected_id
            st.success(f"Using Meta account: {selected_id}")

        else:
            st.warning("No Meta ad accounts found")

    except Exception as e:
        st.error("Failed to load Meta accounts")
        st.exception(e)

# =================================================
# MAIN APP TABS (NEVER BLOCKED)
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

    if google_connected:
        st.success("Google connected — research enabled")
        st.info("Wire Google Trends / YouTube / Keywords here")
    else:
        st.warning("Connect Google to enable research")

# =================================================
# 🎨 CREATIVE TAB
# =================================================
with tab_creative:
    st.subheader("Creative Generator")

    if meta_connected:
        st.success("Meta connected — creative deployment enabled")
        st.info("Wire creative generation + Meta push here")
    else:
        st.warning("Connect Meta to push creatives")

# =================================================
# 📣 CAMPAIGNS TAB
# =================================================
with tab_campaigns:
    st.subheader("Campaign Builder")

    if meta_connected:
        st.success("Meta connected — campaign creation enabled")
        st.info("Wire campaign creation logic here")
    else:
        st.warning("Connect Meta to create campaigns")

# =================================================
# 🧠 STRATEGY TAB
# =================================================
with tab_strategy:
    st.subheader("Strategy & Budget Planning")
    st.info("Strategy logic goes here (independent of OAuth)")

# =================================================
# 🧰 SYSTEM TAB
# =================================================
with tab_system:
    st.subheader("System Status")
    st.write("Meta token stored:", meta_connected)
    st.write("Google token stored:", google_connected)
    st.write("Session keys:", list(st.session_state.keys()))