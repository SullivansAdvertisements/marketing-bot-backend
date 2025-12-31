from fastapi import APIRouter
from app.auth.oauth_meta import meta_login, meta_callback
from app.auth.oauth_google import google_login, google_callback
from app.auth.oauth_tiktok import tiktok_login, tiktok_callback

router = APIRouter()

router.add_api_route("/meta/login", meta_login, methods=["GET"])
router.add_api_route("/meta/callback", meta_callback, methods=["GET"])

router.add_api_route("/google/login", google_login, methods=["GET"])
router.add_api_route("/google/callback", google_callback, methods=["GET"])

router.add_api_route("/tiktok/login", tiktok_login, methods=["GET"])
router.add_api_route("/tiktok/callback", tiktok_callback, methods=["GET"])

def render(meta_token=None, google_token=None):
    import streamlit as st
    import pandas as pd

    st.subheader("Market Research")

    query = st.text_input("Search market / keyword")

    if query:
        df = pd.DataFrame({
            "Metric": ["Search Volume", "Competition", "CPC"],
            "Value": ["High", "Medium", "$1.45"]
        })
        st.dataframe(df, use_container_width=True)
