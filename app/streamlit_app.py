import streamlit as st
from auth.oauth_meta import (
    meta_login_url,
    exchange_code_for_token,
    fetch_meta_ad_accounts,
)
from database import SessionLocal, save_meta_token, save_meta_accounts
from models.ad_account import AdAccount

st.set_page_config(page_title="Marketing Bot", layout="wide")

st.title("🚀 Marketing Bot – Meta Setup")

USER_ID = "default-user"  # replace later with auth

# -------------------------
# 1️⃣ CONNECT META
# -------------------------
st.header("1️⃣ Connect Meta Ads")

st.markdown(
    f"[🔵 Connect Meta Ads]({meta_login_url()})",
    unsafe_allow_html=True
)

# -------------------------
# 2️⃣ HANDLE OAUTH CALLBACK
# -------------------------
query_params = st.experimental_get_query_params()

if "code" in query_params:
    code = query_params["code"][0]

    db = SessionLocal()

    token_data = exchange_code_for_token(code)

    if "access_token" in token_data:
        save_meta_token(db, USER_ID, token_data["access_token"])
        st.success("✅ Meta connected successfully")

        accounts = fetch_meta_ad_accounts(token_data["access_token"])
        save_meta_accounts(db, USER_ID, accounts)

        st.success(f"✅ {len(accounts)} ad accounts found")

# -------------------------
# 3️⃣ SELECT AD ACCOUNT
# -------------------------
st.header("2️⃣ Select Meta Ad Account")

db = SessionLocal()
accounts = db.query(AdAccount).filter_by(
    user_id=USER_ID,
    platform="meta"
).all()

if accounts:
    account_map = {
        f"{a.account_name or 'Ad Account'} ({a.account_id})": a.account_id
        for a in accounts
    }

    selected = st.radio(
        "Choose an account:",
        list(account_map.keys())
    )

    st.success(f"Selected account: {account_map[selected]}")
else:
    st.info("No Meta ad accounts connected yet.")
    from auth.oauth_google import google_login_url, exchange_code_for_token as google_exchange
from models.oauth_token import OAuthToken

# -------------------------
# GOOGLE ADS
# -------------------------
st.header("🔴 Connect Google Ads")

st.markdown(
    f"[🔴 Connect Google Ads]({google_login_url()})",
    unsafe_allow_html=True
)

if "code" in query_params and "google" in st.experimental_get_query_params().get("scope", [""])[0]:
    code = query_params["code"][0]

    db = SessionLocal()
    token_data = google_exchange(code)

    if "access_token" in token_data:
        db.add(OAuthToken(
            user_id=USER_ID,
            platform="google",
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token")
        ))
        db.commit()

        st.success("✅ Google Ads connected")