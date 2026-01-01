"""
Creative Generator Engine
-------------------------
Generates ad creatives (headline, primary text, CTA)
using OpenAI when available, with a deterministic fallback.

SAFE TO IMPORT IN STREAMLIT.
"""

from typing import Dict
import os
import json

# -------------------------------------------------
# Optional OpenAI client (SAFE)
# -------------------------------------------------
OPENAI_AVAILABLE = False
client = None

try:
    from openai import OpenAI

    if os.getenv("OPENAI_API_KEY"):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False


# -------------------------------------------------
# Platform Rules (non-AI constraints)
# -------------------------------------------------
PLATFORM_RULES = {
    "meta": {
        "headline_max": 40,
        "text_style": "benefit-driven, scroll-stopping",
        "ctas": ["Shop Now", "Learn More", "Sign Up"],
    },
    "tiktok": {
        "headline_max": 30,
        "text_style": "casual, fast-paced, creator-style",
        "ctas": ["Shop Now", "Try It", "Watch More"],
    },
    "youtube": {
        "headline_max": 45,
        "text_style": "story-driven, curiosity-based",
        "ctas": ["Watch Now", "Learn More"],
    },
    "google": {
        "headline_max": 30,
        "text_style": "direct-response, keyword-rich",
        "ctas": ["Learn More", "Get Started"],
    },
}


# -------------------------------------------------
# CORE GENERATOR
# -------------------------------------------------
def generate_ad_copy(
    product: str,
    audience: str,
    goal: str,
    tone: str = "bold",
    platform: str = "meta",
    use_ai: bool = True,
) -> Dict[str, str]:
    """
    Generates structured ad creative.

    Returns:
    {
        headline: str,
        primary_text: str,
        cta: str,
        platform: str,
        source: "openai" | "fallback"
    }
    """

    platform = platform.lower()
    rules = PLATFORM_RULES.get(platform, PLATFORM_RULES["meta"])

    # =================================================
    # AI GENERATION PATH
    # =================================================
    if use_ai and OPENAI_AVAILABLE:
        try:
            system_prompt = (
                "You are an elite paid advertising copywriter. "
                "You specialize in performance marketing and conversions."
            )

            user_prompt = f"""
Create high-performing ad copy.

Platform: {platform}
Product: {product}
Target Audience: {audience}
Primary Goal: {goal}
Tone: {tone}

Constraints:
- Headline max length: {rules['headline_max']} characters
- Writing style: {rules['text_style']}
- CTA must be one of: {rules['ctas']}

Return ONLY valid JSON in this format:
{{
  "headline": "...",
  "primary_text": "...",
  "cta": "..."
}}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
            )

            raw = response.choices[0].message.content.strip()
            creative = json.loads(raw)

            return {
                "headline": creative["headline"],
                "primary_text": creative["primary_text"],
                "cta": creative["cta"],
                "platform": platform,
                "source": "openai",
            }

        except Exception as e:
            # AI failed → fall back safely
            print("⚠️ OpenAI generation failed, using fallback:", e)

    # =================================================
    # FALLBACK (NO AI / GUARANTEED)
    # =================================================
    headline = _fallback_headline(product, audience, goal, platform)
    primary_text = _fallback_primary_text(product, audience, tone, platform)
    cta = rules["ctas"][0]

    return {
        "headline": headline,
        "primary_text": primary_text,
        "cta": cta,
        "platform": platform,
        "source": "fallback",
    }


# -------------------------------------------------
# FALLBACK HELPERS
# -------------------------------------------------
def _fallback_headline(product: str, audience: str, goal: str, platform: str) -> str:
    if goal == "sales":
        return f"{product} Built for {audience}"
    if goal == "leads":
        return f"{audience}, Get Started Today"
    if goal == "awareness":
        return f"Discover {product}"
    return f"{product} That Converts"


def _fallback_primary_text(
    product: str,
    audience: str,
    tone: str,
    platform: str,
) -> str:
    if tone == "bold":
        text = (
            f"{product} designed for {audience}. "
            "Limited availability. Act now."
        )
    elif tone == "friendly":
        text = (
            f"Hey {audience}! "
            f"People are loving {product}."
        )
    else:
        text = f"{product} made with {audience} in mind."

    if platform == "tiktok":
        text += " 🔥"
    elif platform == "youtube":
        text += " Watch the full story."
    elif platform == "google":
        text += " Trusted by customers."

    return text
