import streamlit as st
from creative.generator import generate_ad_copy
from creative.meta_publish import publish_meta_creative
from creative.google_publish import publish_google_ad


def render():
    st.header("🎨 Creative → Live Platforms")

    product = st.text_input("Product")
    audience = st.text_input("Audience")
    goal = st.selectbox("Goal", ["Conversions", "Traffic", "Leads"])
    tone = st.selectbox("Tone", ["Bold", "Luxury", "Aggressive"])

    platform = st.multiselect(
        "Send to platforms",
        ["Meta", "Google"],
        default=["Meta"],
    )

    if st.button("Generate & Push Live"):
        creative = generate_ad_copy(
            product=product,
            audience=audience,
            goal=goal,
            tone=tone,
            platform="Multi",
        )

        st.text_area("Generated Copy", creative["output"], height=200)

        if "Meta" in platform:
            with st.spinner("Publishing to Meta…"):
                meta = publish_meta_creative(
                    headline="🔥 " + product,
                    primary_text=creative["output"],
                    cta="Learn More",
                )
                st.success("Meta creative created")
                st.json(meta)

        if "Google" in platform:
            with st.spinner("Preparing Google creative…"):
                google = publish_google_ad(
                    headline=product,
                    description=creative["output"][:90],
                )
                st.success("Google creative ready")
                st.json(google)