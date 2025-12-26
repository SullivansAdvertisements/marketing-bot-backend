import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)
import streamlit as st
from app.auth.oauth_meta import meta_login_url, exchange_code_for_token
# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Marketing Bot",
    layout="wide",
)

st.title("Marketing Bot")
st.caption("Connect ad platforms to build real campaigns")
query = st.experimental_get_query_params()
# -------------------------------------------------
# META ADS CONNECT
# -------------------------------------------------
st.header("Meta Ads")

meta_url = meta_login_url()

if meta_url:
    st.markdown(
        f"[🔵 Connect Meta Ads]({meta_url})",
        unsafe_allow_html=True,
    )
else:
    st.warning("Meta OAuth not configured yet.")

# -------------------------------------------------
# HANDLE META OAUTH CALLBACK
# -------------------------------------------------
if "code" in query:
    st.divider()
    st.subheader("Meta OAuth Callback")

    try:
        with st.spinner("Exchanging code for Meta access token..."):
            token_data = exchange_code_for_token(query["code"][0])

        st.success("Meta connected successfully 🎉")
        st.json(token_data)

        st.experimental_set_query_params()

    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)

# -------------------------------------------------
# PLACEHOLDERS FOR NEXT STEPS
# -------------------------------------------------
st.divider()
st.subheader("Next steps (coming next)")

st.markdown(
    """
- Fetch Meta ad accounts  
- Select an ad account  
- Save token + account to database  
- Build real campaigns  
"""
)