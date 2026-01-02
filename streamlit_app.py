import streamlit as st
import importlib
import traceback

st.set_page_config(
    page_title="Marketing Intelligence Platform",
    layout="wide",
)

# ----------------------------
# SAFE TAB RENDERER
# ----------------------------
def render_tab(module_path: str, label: str):
    try:
        module = importlib.import_module(module_path)
        if not hasattr(module, "render"):
            raise AttributeError(f"{module_path}.render() not found")
        module.render()
    except Exception as e:
        st.error(f"{label} failed to load")
        st.code(str(e))
        st.expander("Full traceback").code(traceback.format_exc())


# ----------------------------
# HEADER
# ----------------------------
st.title("🚀 Marketing Intelligence Platform")

with st.expander("🔐 API & Platform Status", expanded=False):
    def ok(k): return "✅ Connected" if st.secrets.get(k) else "❌ Missing"

    st.write("OpenAI:", ok("OPENAI_API_KEY"))
    st.write("Google Ads:", ok("GOOGLE_ADS_DEVELOPER_TOKEN"))
    st.write("Meta:", ok("META_ACCESS_TOKEN"))
    st.write("TikTok:", ok("TIKTOK_API_KEY"))
    st.write("YouTube:", ok("YOUTUBE_API_KEY"))

# ----------------------------
# MAIN NAV
# ----------------------------
tabs = st.tabs([
    "🔍 Research",
    "🎨 Creative",
    "📣 Campaigns",
    "📈 Strategy",
    "⚙️ System",
])

# ----------------------------
# TAB ROUTING
# ----------------------------
with tabs[0]:
    render_tab("research.router", "Research")

with tabs[1]:
    render_tab("creative.router", "Creative")

with tabs[2]:
    render_tab("campaigns.router", "Campaigns")

with tabs[3]:
    render_tab("strategy.router", "Strategy")

with tabs[4]:
    st.header("⚙️ System Diagnostics")
    st.json({
        "env": st.secrets.get("ENV"),
        "log_level": st.secrets.get("LOG_LEVEL"),
        "python": "ok",
        "streamlit": "ok",
    })