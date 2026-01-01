import streamlit as st
import pandas as pd
import os
import json
from typing import List, Dict

from openai import OpenAI

# -------------------------
# OPENAI CLIENT
# -------------------------
def get_openai_client():
    key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY missing")
    return OpenAI(api_key=key)


# -------------------------
# PROMPT BUILDER (MAX CONTEXT)
# -------------------------
def build_creative_prompt(
    product: str,
    goal: str,
    platform: str,
    research_bundle: Dict,
):
    return f"""
You are a senior paid media strategist.

Generate HIGH-PERFORMING ad creatives using the research below.

RESEARCH DATA (summarized):
{json.dumps(research_bundle, indent=2)}

REQUIREMENTS:
• Platform: {platform}
• Goal: {goal}
• Product: {product}

OUTPUT RULES:
1. Generate 5 DISTINCT ANGLES (emotional, logical, social proof, urgency, contrarian)
2. For EACH angle generate:
   - 3 Headlines
   - 2 Primary Texts
   - 1 CTA
3. Assign each angle a performance score (0–100)
4. Explain WHY the angle should work
5. Output valid JSON ONLY

JSON FORMAT:
[
  {{
    "angle": "",
    "score": 0,
    "why": "",
    "headlines": [],
    "primary_texts": [],
    "cta": ""
  }}
]
"""


# -------------------------
# OPENAI CREATIVE ENGINE
# -------------------------
def generate_creatives(
    product: str,
    goal: str,
    platform: str,
    research_bundle: Dict,
) -> List[Dict]:

    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an elite paid advertising strategist."},
            {"role": "user", "content": build_creative_prompt(
                product, goal, platform, research_bundle
            )},
        ],
        temperature=0.9,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception:
        raise RuntimeError("OpenAI returned invalid JSON")
    

# -------------------------
# STREAMLIT RENDER
# -------------------------
def render():
    st.header("🎨 Creative Intelligence (OpenAI Powered)")

    if "research_bundle" not in st.session_state:
        st.warning("Run Research first to unlock full creative power.")
        return

    product = st.text_input("Product / Offer")
    goal = st.selectbox("Goal", ["Conversions", "Traffic", "Leads"])
    platform = st.selectbox("Platform", ["Meta", "Google"])

    run = st.button("🚀 Generate Creative Matrix")

    if not run:
        return

    with st.spinner("Generating multi-angle creatives using OpenAI…"):
        creatives = generate_creatives(
            product=product,
            goal=goal,
            platform=platform,
            research_bundle=st.session_state["research_bundle"],
        )

    # -------------------------
    # DISPLAY RESULTS
    # -------------------------
    rows = []
    for c in creatives:
        rows.append({
            "Angle": c["angle"],
            "Score": c["score"],
            "Why it Works": c["why"],
            "Headlines": " | ".join(c["headlines"]),
            "Primary Texts": " | ".join(c["primary_texts"]),
            "CTA": c["cta"],
        })

    df = pd.DataFrame(rows).sort_values("Score", ascending=False)

    st.subheader("🏆 Creative Performance Matrix")
    st.dataframe(df, use_container_width=True)

    top = df.iloc[0]
    st.subheader("🔥 Top Performing Angle")
    st.json(top.to_dict())