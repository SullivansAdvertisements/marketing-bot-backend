import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

import streamlit as st
from app.auth.oauth_meta import meta_login_url, exchange_code_for_token

st.title("Import Test")

st.success("app.auth.oauth_meta imported successfully ✅")

st.markdown(f"[Connect Meta]({meta_login_url()})")