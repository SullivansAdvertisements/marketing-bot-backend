import streamlit as st
from oauth_meta import meta_login_url, exchange_code_for_token

st.title("Marketing Bot")

st.success("Imports resolved ✅")

st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")

query = st.experimental_get_query_params()

if "code" in query:
    try:
        token = exchange_code_for_token(query["code"][0])
        st.success("Meta connected successfully 🎉")
        st.json(token)
        st.experimental_set_query_params()
    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)
