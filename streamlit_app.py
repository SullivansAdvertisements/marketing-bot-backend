import streamlit as st

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(
    page_title="Sullivan’s Advertisements | Campaign Manager",
    page_icon="📣",
    layout="wide",
)

# -----------------------------
# GLOBAL STYLES (UX polish)
# -----------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
    }
    div[data-testid="stTabs"] button {
        font-size: 16px;
        padding: 12px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("## 📊 Sullivan’s Advertisements")
    st.caption("Unified Ad Campaign Control")
    st.divider()

    page = st.radio(
        "Navigate",
        ["🏠 Dashboard", "📣 Campaign Creation"],
        index=1
    )

    st.divider()
    st.caption("Connected Platforms")

    if st.secrets.get("GOOGLE_ADS_DEVELOPER_TOKEN"):
        st.success("Google Ads Connected")
    else:
        st.warning("Google Ads Not Connected")

    if st.secrets.get("META_ACCESS_TOKEN"):
        st.success("Meta Ads Connected")
    else:
        st.warning("Meta Ads Not Connected")

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
if page == "🏠 Dashboard":
    st.header("📈 Overview")
    st.info("""
    Use **Campaign Creation** to:
    - Estimate reach
    - Build Google campaigns
    - Configure Meta campaigns & ad sets
    - View performance benchmarks
    """)

# -----------------------------
# CAMPAIGN CREATION PAGE
# -----------------------------
if page == "📣 Campaign Creation":

    st.header("📣 Campaign Creation Center")
    st.caption("Create, estimate, and optimize campaigns across platforms")

    st.divider()

    # Import router ONLY when needed (avoids circular imports)
    from campaigns.router import render as campaign_router_render

    campaign_router_render()