def validate_research_data(data: dict) -> None:
    required = [
        "niche",
        "platforms",
        "keywords",
        "audiences",
        "funnels",
        "angles",
        "budget_guidance",
        "sources"
    ]

    for key in required:
        if key not in data:
            raise ValueError(f"Missing research_data key: {key}")

    if not data["keywords"]:
        raise ValueError("No real keyword data provided")

    for kw in data["keywords"]:
        if "avg_monthly_searches" not in kw:
            raise ValueError("Keyword missing search volume")

    return None