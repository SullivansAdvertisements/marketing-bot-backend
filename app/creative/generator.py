from typing import Dict
import os

OPENAI_AVAILABLE = False
client = None


def get_openai_client():
    global client, OPENAI_AVAILABLE

    if client is not None:
        return client

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        OPENAI_AVAILABLE = True
        return client
    except Exception as e:
        print("OpenAI init failed:", e)
        return None


def generate_ad_copy(
    product: str,
    audience: str,
    goal: str,
    tone: str = "bold",
    platform: str = "meta",
    use_ai: bool = True,
) -> Dict[str, str]:

    # -----------------------------
    # AI PATH (SAFE)
    # -----------------------------
    if use_ai:
        client = get_openai_client()
        if client:
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

                import json
                creative = json.loads(response.choices[0].message.content)

                return {
                    "headline": creative["headline"],
                    "primary_text": creative["primary_text"],
                    "cta": creative["cta"],
                    "source": "openai",
                }

            except Exception as e:
                print("OpenAI failed, falling back:", e)

    # -----------------------------
    # FALLBACK (ALWAYS WORKS)
    # -----------------------------
    if goal == "sales":
        headline = f"{product} That {audience} Can't Ignore"
        cta = "Shop Now"
    elif goal == "leads":
        headline = f"{audience}, Get Started Today"
        cta = "Sign Up"
    else:
        headline = f"Discover {product}"
        cta = "Learn More"

    primary_text = f"{product} built for {audience}. Limited availability."

    return {
        "headline": headline,
        "primary_text": primary_text,
        "cta": cta,
        "source": "fallback",
    }