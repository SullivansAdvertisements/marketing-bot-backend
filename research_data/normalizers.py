def normalize_google_keyword(row: dict) -> dict:
    return {
        "keyword": row["keyword"],
        "avg_monthly_searches": row["avg_monthly_searches"],
        "competition": row["competition"],
        "competition_index": row.get("competition_index"),
        "top_of_page_cpc_low": row.get("top_of_page_cpc_low"),
        "top_of_page_cpc_high": row.get("top_of_page_cpc_high"),
        "source": "google_ads"
    }