import streamlit as st
import urllib.parse
from auth.oauth_meta import meta_login_url, meta_exchange_code
from database import SessionLocal
from models.oauth_token import OAuthToken

st.set_page_config(page_title="Marketing Bot", layout="wide")

st.title("🚀 Marketing Bot")

# ----------------------------------
# CONNECT META ADS
# ----------------------------------
st.header("1️⃣ Connect Meta Ads")

meta_auth_url = meta_login_url()

st.markdown(
    f"[🔵 Connect Meta Ads]({meta_auth_url})",
    unsafe_allow_html=True
)

# ----------------------------------
# HANDLE OAUTH CALLBACK
# ----------------------------------
query_params = st.experimental_get_query_params()

if "code" in query_params:
    code = query_params["code"][0]

    db = SessionLocal()

    token_data = meta_exchange_code(code)

    token = OAuthToken(
        user_id="demo-user",  # replace later
        platform="meta",
        access_token=token_data["access_token"]
    )

    db.add(token)
    db.commit()

    st.success("Meta account connected successfully ✅")