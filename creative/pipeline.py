import os
import openai
from typing import Dict, List

openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------------------------------------
# STEP 1: EXTRACT INSIGHTS FROM RESEARCH
# -------------------------------------------------
def extract_insights(research_data: Dict) -> Dict:
    insights = {
        "top_keywords": [],
        "audience_intent": [],
        "hooks": [],
        "platform_trends": {},
    }

    for source, data in research_data.items():
        if not data:
            continue

        # Google Keywords
        if "Keyword" in str(data):
            insights["top_keywords"] += data["Keyword"].head(10).tolist()

        # Meta Ads
        if "creative_text" in str(data).lower():
            insights["hooks"] += data["creative_text"].head(10).tolist()

        # TikTok / YouTube trends
        if isinstance(data, list):
            insights["platform_trends"][source] = data[:10]

    insights["top_keywords"] = list(set(insights["top_keywords"]))[:10]
    insights["hooks"] = list(set(insights["hooks"]))[:10]

    return insights


# -------------------------------------------------
# STEP 2: BUILD CREATIVE BRIEF
# -------------------------------------------------
def build_creative_brief(insights: Dict, goal: str) -> str:
    return f"""
You are a senior performance marketing strategist.

GOAL:
{goal}

TOP KEYWORDS:
{', '.join(insights['top_keywords'])}

TOP HOOKS / ANGLES:
{', '.join(insights['hooks'])}

PLATFORM TRENDS:
{insights['platform_trends']}

Create high-converting ad creatives.
"""


# -------------------------------------------------
# STEP 3: GENERATE MULTI-CREATIVE SET
# -------------------------------------------------
def generate_creatives(
    research_data: Dict,
    goal: str,
    platform: str,
    n_variations: int = 5,
) -> List[Dict]:

    insights = extract_insights(research_data)
    brief = build_creative_brief(insights, goal)

    prompt = f"""
{brief}

PLATFORM: {platform}

Generate {n_variations} DIFFERENT ad creatives.

Each creative must include:
- Headline
- Primary Text
- CTA
- Angle (emotion / logic / trend / urgency)

Respond in JSON list format.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
    )

    return eval(response.choices[0].message.content)