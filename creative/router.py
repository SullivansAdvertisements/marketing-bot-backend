import streamlit as st
from creative.pipeline import generate_creatives

def render():
    st.header("🎨 AI Creative Engine")

    if "research_results" not in st.session_state:
        st.warning("Run research first.")
        return

    goal = st.selectbox(
        "Campaign Objective",
        ["Conversions", "Traffic", "Leads", "Brand Awareness"],
    )

    platform = st.selectbox(
        "Platform",
        ["Meta", "Google", "TikTok"],
    )

    variations = st.slider(
        "Number of creative variations",
        min_value=3,
        max_value=10,
        value=5,
    )

    if st.button("⚡ Generate High-Performance Creatives"):
        with st.spinner("Generating performance-grade creatives…"):
            creatives = generate_creatives(
                research_data=st.session_state.research_results,
                goal=goal,
                platform=platform,
                n_variations=variations,
            )

        for i, c in enumerate(creatives, 1):
            with st.expander(f"Creative #{i} — {c['Angle']}"):
                st.markdown(f"**Headline:** {c['Headline']}")
                st.markdown(f"**Primary Text:** {c['Primary Text']}")
                st.markdown(f"**CTA:** {c['CTA']}")