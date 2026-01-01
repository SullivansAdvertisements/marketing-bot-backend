import streamlit as st
import traceback

# -------------------------------------------------
# STREAMLIT CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Marketing Bot",
    layout="wide",
)

st.title("🚀 Marketing Bot")

# -------------------------------------------------
# SAFE RENDER WRAPPER
# -------------------------------------------------
def safe_render(name, fn):
    try:
        fn()
    except Exception as err:
        st.error(f"❌ {name} failed to load")
        st.code(str(err))
        st.expander("Traceback").code(traceback.format_exc())


# -------------------------------------------------
# SAFE ROUTER IMPORTS
# -------------------------------------------------
def load_router(import_path, label):
    try:
        module = __import__(import_path, fromlist=["render"])
        return module.render
    except Exception as err:
        def _fallback():
            st.error(f"❌ {label} unavailable")
            st.code(str(err))
        return _fallback


research_render = load_router("research.router", "Research")
campaigns_render = load_router("campaigns.router", "Campaigns")
creative_render = load_router("creative.router", "Creative")
strategy_render = load_router("strategy.router", "Strategy")
utils_render = load_router("utils.router", "Utils")

# -------------------------------------------------
# SESSION STATE BOOTSTRAP
# -------------------------------------------------
def bootstrap_state():
    defaults = {
        "google_token": st.secrets.get("GOOGLE_ADS_DEVELOPER_TOKEN"),
        "meta_token": st.secrets.get("META_ACCESS_TOKEN"),
        "openai_key": st.secrets.get("OPENAI_API_KEY"),
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

bootstrap_state()

# -------------------------------------------------
# API STATUS BAR
# -------------------------------------------------
with st.expander("🔐 API & Platform Status"):
    st.write({
        "Google Ads": bool(st.session_state.get("google_token")),
        "Meta Ads": bool(st.session_state.get("meta_token")),
        "OpenAI": bool(st.session_state.get("openai_key")),
    })

# -------------------------------------------------
# MAIN TABS
# -------------------------------------------------
tabs = st.tabs([
    "🔎 Research",
    "📣 Campaigns",
    "🎨 Creative",
    "📈 Strategy",
    "🛠 Utils",
])

with tabs[0]:
    safe_render("Research", research_render)

with tabs[1]:
    safe_render("Campaigns", campaigns_render)

with tabs[2]:
    safe_render("Creative", creative_render)

with tabs[3]:
    safe_render("Strategy", strategy_render)

with tabs[4]:
    safe_render("Utils", utils_render)