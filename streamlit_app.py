import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from research.router import render as research_render
from campaigns.router import render as campaigns_render
from strategy.router import render as strategy_render

# =================================================
# STREAMLIT CONFIG (MUST BE FIRST)
# =================================================
st.set_page_config(
    page_title="Marketing Bot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =================================================
# SAFE SESSION STATE BOOTSTRAP
# =================================================
DEFAULT_STATE = {
    "meta_token": None,
    "google_token": None,
    "active_tab": "Research",
}

for k, v in DEFAULT_STATE.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =================================================
# SAFE ROUTER IMPORTS (NO SIDE EFFECTS)
# =================================================
from research.router import render as research_render
from app.campaigns.router import render as campaigns_render
from app.strategy.router import render as strategy_render
from app.creative.router import generate_creative

# =================================================
# APP HEADER
# =================================================
st.title("🚀 Marketing Bot")
st.caption("Research → Strategy → Campaign Execution")

# =================================================
# GLOBAL CONNECTION STATUS (NON-BLOCKING)
# =================================================
with st.expander("🔐 Platform Connection Status", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.meta_token:
            st.success("Meta Ads Connected")
        else:
            st.warning("Meta Ads Not Connected")

    with col2:
        if st.session_state.google_token:
            st.success("Google Ads Connected")
        else:
            st.warning("Google Ads Not Connected")

# =================================================
# MAIN NAVIGATION (MOBILE SAFE)
# =================================================
tabs = st.tabs([
    "🔎 Research",
    "📈 Strategy",
    "📣 Campaigns",
    "🎨 Creative",
])

# =================================================
# TAB — RESEARCH
# =================================================
with tabs[0]:
    try:
        research_render()
    except Exception as e:
        st.error("Research module failed to load.")
        st.exception(e)

# =================================================
# TAB — STRATEGY
# =================================================
with tabs[1]:
    try:
        strategy_render()
    except Exception as e:
        st.error("Strategy module failed to load.")
        st.exception(e)

# =================================================
# TAB — CAMPAIGNS
# =================================================
with tabs[2]:
    try:
        campaigns_render()
    except Exception as e:
        st.error("Campaigns module failed to load.")
        st.exception(e)

# =================================================
# TAB — CREATIVE (AI)
# =================================================
with tabs[3]:
    st.subheader("🎨 Creative Generator")

    with st.form("creative_form"):
        product = st.text_input("Product / Offer")
        audience = st.text_input("Target Audience")
        goal = st.selectbox(
            "Goal",
            ["Conversions", "Leads", "Traffic", "Awareness"],
        )
        tone = st.selectbox(
            "Tone",
            ["bold", "luxury", "aggressive", "minimal"],
        )
        platform = st.selectbox(
            "Platform",
            ["meta", "google", "tiktok"],
        )

        submitted = st.form_submit_button("Generate Creative")

    if submitted and product and audience:
        creative = generate_creative(
            product=product,
            audience=audience,
            goal=goal,
            tone=tone,
            platform=platform,
            use_ai=True,
        )

        st.subheader("🧠 AI Output")

        st.table([
            {"Field": "Headline", "Value": creative["headline"]},
            {"Field": "Primary Text", "Value": creative["primary_text"]},
            {"Field": "CTA", "Value": creative["cta"]},
            {"Field": "Platform", "Value": creative["platform"]},
            {"Field": "Source", "Value": creative["source"]},
        ])