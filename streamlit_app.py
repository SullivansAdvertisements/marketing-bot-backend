import streamlit as st
from oauth_meta import meta_login_url, exchange_code_for_token, fetch_ad_accounts

st.title("Marketing Bot")

st.success("Imports OK")

# OAuth callback handling
query = st.experimental_get_query_params()

if "code" in query:
    try:
        token = exchange_code_for_token(query["code"][0])
        st.success("Meta connected successfully 🎉")
        st.session_state["meta_access_token"] = token["access_token"]
        accounts = fetch_ad_accounts(st.session_state["meta_access_token"])
        st.json(accounts)
        accounts = fetch_ad_accounts(token["access_token"])
        st.json(accounts)

    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)
else:
    st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")