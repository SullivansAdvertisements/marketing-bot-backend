"""
research_data/exporters.py

Exports validated research data into DataFrames or
campaign-ready slices.
"""

import pandas as pd


# -------------------------
# UI EXPORTS
# -------------------------

def export_keywords_df(research_data: dict) -> pd.DataFrame:
    return pd.DataFrame(research_data.get("keywords", []))


def export_search_trends_df(research_data: dict) -> pd.DataFrame:
    return pd.DataFrame(research_data.get("search_trends", []))


def export_content_trends_df(research_data: dict) -> pd.DataFrame:
    return pd.DataFrame(research_data.get("content_trends", []))


def export_ad_intel_df(research_data: dict) -> pd.DataFrame:
    return pd.DataFrame(research_data.get("ad_intel", []))


# -------------------------
# CAMPAIGN EXPORTS
# -------------------------

def export_top_keywords(research_data: dict, limit: int = 10):
    return sorted(
        research_data.get("keywords", []),
        key=lambda k: k["avg_monthly_searches"],
        reverse=True
    )[:limit]


def export_content_hooks(research_data: dict, limit: int = 10):
    return [
        trend["title"]
        for trend in research_data.get("content_trends", [])
    ][:limit]


def export_competitor_angles(research_data: dict):
    return [
        ad["ad_copy"]
        for ad in research_data.get("ad_intel", [])
        if ad.get("active")
    ]