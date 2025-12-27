#import streamlit as st
from urllib.parse import urlencode

# ===============================
# IMPORT HARDEST SYSTEM LOGIC
# ===============================
from oauth_meta import (
    meta_login_url,
    exchange_code_for_token,
    fetch_ad_accounts,
)

st.set_page_config(page_title="Marketing Bot", layout="wide")

st.title("Marketing Bot")

# ===============================
# 1️⃣ HANDLE OAUTH CALLBACK (HARDEST PART)
# ===============================
query = st.experimental_get_query_params()

if "code" in query and "meta_access_token" not in st.session_state:
    st.subheader("Meta OAuth Callback")

    try:
        token = exchange_code_for_token(query["code"][0])

        # 🔐 STORE TOKEN (CRITICAL)
        st.session_state["meta_access_token"] = token["access_token"]

        st.success("Meta connected successfully 🎉")

    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)

# ===============================
# 2️⃣ CONNECT BUTTON (LOGIN ENTRY)
# ===============================
st.markdown("### Meta Ads")

if "meta_access_token" not in st.session_state:
    st.markdown(
        f"[🔵 Connect Meta Ads]({meta_login_url()})",
        unsafe_allow_html=True
    )
    st.stop()

st.success("Meta connected ✅")

# ===============================
# 3️⃣ FETCH AD ACCOUNTS (REAL POWER CHECK)
# ===============================
if accounts and "data" in accounts:
    for acct in accounts["data"]:
        acct_name = acct.get("name", "Unnamed Ad Account")
        st.success(f"{acct_name} ({acct['id']})")
else:
    st.warning("No ad accounts found.")

# ===============================
# 4️⃣ NEXT SYSTEM TABS (STUBS)
# ===============================
st.divider()

st.subheader("Next Steps (Coming Next)")
st.markdown("""
- Campaign Builder  
- Creative Generator  
- Insights Dashboard  
- Budget Optimizer  
""")