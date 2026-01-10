"""
research_data/validators.py

Strict validation. Fail fast. No silent coercion.
"""

from research_data.schema import (
    KEYWORD_SCHEMA,
    SEARCH_TREND_SCHEMA,
    CONTENT_TREND_SCHEMA,
    AD_LIBRARY_SCHEMA,
    RESEARCH_SCHEMA,
)


def _validate_dict(data: dict, schema: dict, label: str):
    for field, field_type in schema.items():
        if field not in data:
            raise ValueError(f"{label}: Missing field '{field}'")
        if not isinstance(data[field], field_type):
            raise ValueError(
                f"{label}: Field '{field}' must be {field_type}, got {type(data[field])}"
            )


def validate_keywords(keywords: list):
    for row in keywords:
        _validate_dict(row, KEYWORD_SCHEMA, "Keyword")


def validate_search_trends(trends: list):
    for row in trends:
        _validate_dict(row, SEARCH_TREND_SCHEMA, "Search Trend")


def validate_content_trends(trends: list):
    for row in trends:
        _validate_dict(row, CONTENT_TREND_SCHEMA, "Content Trend")


def validate_ad_intel(ads: list):
    for ad in ads:
        _validate_dict(ad, AD_LIBRARY_SCHEMA, "Ad Library")


def validate_research_data(data: dict):
    _validate_dict(data, RESEARCH_SCHEMA, "Research Data")

    validate_keywords(data.get("keywords", []))
    validate_search_trends(data.get("search_trends", []))
    validate_content_trends(data.get("content_trends", []))
    validate_ad_intel(data.get("ad_intel", []))