import streamlit as st

st.set_page_config(page_title="Marketing Bot", layout="wide")

st.title("Marketing Bot")
st.success("Fresh Render deploy successful.")
import streamlit as st

query = st.experimental_get_query_params()

# Data Deletion Page
if "data-deletion" in query:
    st.title("User Data Deletion Instructions")
    st.write("""
    If you have used Marketing Bot and would like your data deleted, please follow the instructions below.
    
    **How to request deletion**
    - Send an email to: **sullysmarketing7@gmail.com**
    - Include the subject: **"Data Deletion Request"**
    - Include the email address you used to authenticate

    We will permanently delete all associated data within 30 days.
    """)
    st.stop()
    import streamlit as st
from app.auth.oauth_meta import exchange_code_for_token

query = st.experimental_get_query_params()

if "code" in query:
    try:
        with st.spinner("Connecting to Meta..."):
            token_data = exchange_code_for_token(query["code"][0])

        st.success("Meta connected successfully 🎉")
        st.json(token_data)

        # Clear URL params (important)
        st.experimental_set_query_params()

    except Exception as e:
        st.error("Meta connection failed")
        st.exception(e)