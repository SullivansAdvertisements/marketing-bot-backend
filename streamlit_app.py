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