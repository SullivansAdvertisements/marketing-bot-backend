from typing import Dict
import os

from openai import OpenAI

# -------------------------------------------------
# OpenAI client (uses OPENAI_API_KEY env var)
# -------------------------------------------------
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_ad_copy(
    product: str,
    audience: str,
    goal: str,
    tone: str = "bold",
    platform: str = "meta",
    use_ai: bool = True,
) -> Dict[str, str]:
    """
    Core creative generator.
    Uses OpenAI if available, otherwise falls back to rules.
    """

    # -------------------------------------------------
    # AI GENERATION PATH
    # -------------------------------------------------
    if use_ai and os.getenv("OPENAI_API_KEY"):
        try:
            prompt = f"""
            Create high-performing ad copy.

            Product: {product}
            Audience: {audience}
            Goal: {goal}
            Tone: {tone}
            Platform: {platform}

            Return JSON with:
            - headline
            - primary_text
            - cta
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an elite performance advertiser."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            content = response.choices[0].message.content

            # VERY IMPORTANT: enforce JSON safety
            import json
            creative = json.loads(content)

            return {
                "headline": creative["headline"],
                "primary_text": creative["primary_text"],
                "cta": creative["cta"],
                "source": "openai",
            }

        except Exception as e:
            # Fall through to deterministic logic
            print("OpenAI failed, using fallback:", e)

    # -------------------------------------------------
    # FALLBACK (DETERMINISTIC / NO AI)
    # -------------------------------------------------
    if goal == "sales":
        headline = f"{product} That {audience} Can't Ignore"
        cta = "Shop Now"
    elif goal == "leads":
        headline = f"{audience}, Get Started Today"
        cta = "Sign Up"
    else:
        headline = f"Discover {product}"
        cta = "Learn More"

    if tone == "bold":
        primary_text = (
            f"{product} built for {audience}. "
            "Limited availability. No excuses."
        )
    elif tone == "friendly":
        primary_text = (
            f"Hey {audience}! "
            f"{product} is here and people are loving it."
        )
    else:
        primary_text = f"{product} designed with {audience} in mind."

    if platform == "tiktok":
        primary_text += " 🔥"
    elif platform == "youtube":
        primary_text += " Watch now."

    return {
        "headline": headline,
        "primary_text": primary_text,
        "cta": cta,
        "source": "fallback",
    }