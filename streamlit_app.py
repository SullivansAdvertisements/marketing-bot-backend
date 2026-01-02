import streamlit as st
import pandas as pd

# =========================================================
# MUST BE FIRST — MOBILE FRIENDLY
# =========================================================
st.set_page_config(
    page_title="Marketing Intelligence Bot",
    layout="
    initial_sidebar_state="collapsed",
)

# =========================================================
# SAFE SECRET ACCESS
# =========================================================
def has_secret(key: str) -> bool:
    return bool(st.secrets.get(key))

# =========================================================
# CONNECTION STATE (NO OAUTH REQUIRED)
# =========================================================
st.session_state.setdefault("google_connected", has_secret("GOOGLE_ADS_DEVELOPER_TOKEN"))
st.session_state.setdefault("meta_connected", has_secret("META_ACCESS_TOKEN"))
st.session_state.setdefault("openai_connected", has_secret("OPENAI_API_KEY"))
st.session_state.setdefault("tiktok_connected", has_secret("TIKTOK_API_KEY"))
st.session_state.setdefault("youtube_connected", has_secret("YOUTUBE_API_KEY"))

# Tokens (used by routers)
st.session_state.setdefault("google_token", st.secrets.get("GOOGLE_ADS_REFRESH_TOKEN"))
st.session_state.setdefault("meta_token", st.secrets.get("META_ACCESS_TOKEN"))

# =========================================================
# SAFE RENDER WRAPPER (PREVENTS CRASHES)
# =========================================================
def safe_render(fn, label: str):
    try:
        fn()
    except Exception as e:
        st.error(f"{label} failed to load")
        st.exception(e)

# =========================================================
# APP TITLE
# =========================================================
st.title("🚀 Marketing Intelligence Bot")

# =========================================================
# 🔐 SYSTEM STATUS TAB (ALWAYS LOADS)
# =========================================================
with st.expander("🔐 Platform Connection Status", expanded=True):
    status_data = [
        {"Platform": "OpenAI", "Connected": st.session_state.openai_connected},
        {"Platform": "Google Ads", "Connected": st.session_state.google_connected},
        {"Platform": "Meta Ads", "Connected": st.session_state.meta_connected},
        {"Platform": "TikTok", "Connected": st.session_state.tiktok_connected},
        {"Platform": "YouTube", "Connected": st.session_state.youtube_connected},
    ]

    df = pd.DataFrame(status_data)
    df["Status"] = df["Connected"].apply(lambda x: "✅ Connected" if x else "❌ Missing")
    st.dataframe(df[["Platform", "Status"]], use_container_width=True)

# =========================================================
# LAZY ROUTER IMPORTS (SAFE)
# =========================================================
def load_router(path, name):
    try:
        module = __import__(path, fromlist=[name])
        return getattr(module, name)
    except Exception as e:
        return lambda: st.error(f"{path} failed to load: {e}")

research_render = load_router("research.router", "render")
creative_render = load_router("creative.router", "render")
campaigns_render = load_router("campaigns.router", "render")
strategy_render = load_router("strategy.router", "render")

# =========================================================
# MAIN TABS
# =========================================================
tabs = st.tabs([
    "🔎 Research",
    "🎨 Creative",
    "📣 Campaigns",
    "📈 Strategy",
    "🧰 System",
])

# =========================================================
# 🔎 RESEARCH TAB
# =========================================================
with tabs[0]:
    safe_render(research_render, "Research")

# =========================================================
# 🎨 CREATIVE TAB
# =========================================================
with tabs[1]:
    if not st.session_state.openai_connected:
        st.warning("OpenAI key missing — creative generation disabled.")
    safe_render(creative_render, "Creative")

# =========================================================
# 📣 CAMPAIGNS TAB
# =========================================================
with tabs[2]:
    safe_render(campaigns_render, "Campaigns")

# =========================================================
# 📈 STRATEGY TAB
# =========================================================
with tabs[3]:
    safe_render(strategy_render, "Strategy")

# =========================================================
# 🧰 SYSTEM / DEBUG TAB
# =========================================================
with tabs[4]:
    st.subheader("🧰 System Diagnostics")

    st.json({
        "ENV": st.secrets.get("ENV", "unknown"),
        "LOG_LEVEL": st.secrets.get("LOG_LEVEL", "INFO"),
        "Google Connected": st.session_state.google_connected,
        "Meta Connected": st.session_state.meta_connected,
        "OpenAI Connected": st.session_state.openai_connected,
        "TikTok Connected": st.session_state.tiktok_connected,
        "YouTube Connected": st.session_state.youtube_connected,
    })

    st.info("""
    This app:
    • Never blocks access if a platform is missing  
    • Uses real APIs where available  
    • Gracefully degrades when keys are absent  
    • Keeps Research → Creative → Strategy connected  
    """)

# =========================================================
# FOOTER
# =========================================================
st.caption("Production-safe • Mobile-friendly • Real API intelligence")