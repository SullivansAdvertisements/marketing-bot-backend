import streamlit as st

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(
    page_title="Marketing Bot",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================
# AUTH IMPORTS
# ============================
from oauth_meta import meta_login_url, exchange_meta_code_for_token
from oauth_google import google_login_url, exchange_google_code_for_token

# ============================
# MODULE ROUTERS
# ============================
from app.research.router import render as research_render
from app.strategy.router import render as strategy_render
from app.creative.router import render as creative_render
from app.campaigns.router import render as campaigns_render

# ============================
# SESSION STATE
# ============================
for key in ["meta_token", "google_token"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ============================
# HANDLE OAUTH CALLBACK (ONCE)
# ============================
query = st.query_params

if "code" in query and "state" in query:
    try:
        if query["state"] == "meta" and not st.session_state.meta_token:
            st.session_state.meta_token = exchange_meta_code_for_token(query["code"])
            st.success("Meta connected")

        if query["state"] == "google" and not st.session_state.google_token:
            st.session_state.google_token = exchange_google_code_for_token(query["code"])
            st.success("Google connected")

        st.query_params.clear()

    except Exception as e:
        st.error(f"Auth error: {e}")

# ============================
# HEADER
# ============================
st.title("🚀 Marketing Bot")
st.caption("Research → Strategy → Creative → Campaigns")

# ============================
# PLATFORM STATUS
# ============================
c1, c2 = st.columns(2)

with c1:
    st.subheader("Meta Ads")
    if st.session_state.meta_token:
        st.success("Connected")
        st.markdown(f"[Reconnect Meta]({meta_login_url(state='meta')})")
    else:
        st.warning("Not connected")
        st.markdown(f"[Connect Meta Ads]({meta_login_url(state='meta')})")

with c2:
    st.subheader("Google Ads")
    if st.session_state.google_token:
        st.success("Connected")
        st.markdown(f"[Reconnect Google]({google_login_url(state='google')})")
    else:
        st.warning("Not connected")
        st.markdown(f"[Sign in with Google]({google_login_url(state='google')})")

st.divider()

# ============================
# MAIN TABS (REAL MODULES)
# ============================
tabs = st.tabs([
    "🔍 Research",
    "📊 Strategy",
    "🎨 Creative",
    "📣 Campaigns",
])

with tabs[0]:
    research_render(
        meta_token=st.session_state.meta_token,
        google_token=st.session_state.google_token
    )

with tabs[1]:
    strategy_render(
        meta_token=st.session_state.meta_token,
        google_token=st.session_state.google_token
    )

with tabs[2]:
    creative_render(
        meta_token=st.session_state.meta_token,
        google_token=st.session_state.google_token
    )

with tabs[3]:
    campaigns_render(
        meta_token=st.session_state.meta_token,
        google_token=st.session_state.google_token
    )

# ============================
# DEBUG (OPTIONAL)
# ============================
with st.expander("Debug"):
    st.json({
        "meta_connected": bool(st.session_state.meta_token),
        "google_connected": bool(st.session_state.google_token),
    })