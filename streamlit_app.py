import streamlit as st

from app.database import get_session
from app.auth.oauth_meta import meta_login_url

st.set_page_config(page_title="Marketing Bot", layout="wide")

st.title("Marketing Bot")

st.write("Connect your ad accounts to begin.")

# -------------------------
# CONNECT META ADS
# -------------------------
st.header("Meta Ads")

meta_url = meta_login_url()

st.markdown(
    f"[🔵 Connect Meta Ads]({meta_url})",
    unsafe_allow_html=True
)

# -------------------------
# DATABASE USAGE (SAFE)
# -------------------------
if st.button("Test database connection"):
    try:
        db = get_session()
        st.success("Database connection established ✅")
        db.close()
    except Exception as e:
        st.error(f"Database error: {e}")