from typing import Dict
from .generator import generate_ad_copy

def generate_creative(
    product: str,
    audience: str,
    goal: str,
    tone: str,
    platform: str,
) -> Dict[str, str]:
    """
    Router for creative generation.
    This is what Streamlit imports.
    """

    creative = generate_ad_copy(
        product=product,
        audience=audience,
        goal=goal,
        tone=tone,
        platform=platform,
    )

    return creative