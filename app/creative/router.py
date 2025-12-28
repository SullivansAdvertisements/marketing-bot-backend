"""
Creative Router
---------------
Thin interface between Streamlit and the creative generator.
DO NOT put business logic here.
"""

from typing import Dict

from .generator import generate_ad_copy


def generate_creative(
    product: str,
    audience: str,
    goal: str,
    tone: str = "bold",
    platform: str = "meta",
    use_ai: bool = True,
) -> Dict[str, str]:
    """
    Public creative generation entrypoint.

    This is what Streamlit imports.

    Returns:
    {
        headline: str,
        primary_text: str,
        cta: str,
        platform: str,
        source: "openai" | "fallback"
    }
    """

    creative = generate_ad_copy(
        product=product,
        audience=audience,
        goal=goal,
        tone=tone,
        platform=platform,
        use_ai=use_ai,
    )

    return creative