# research/google_trends.py
import pandas as pd
from pytrends.request import TrendReq
import traceback

def fetch_google_trends(keyword: str, country: str = "US"):
    """
    Google Trends fetch with ZERO retry config.
    No index limits.
    No slicing.
    No crashes.
    """

    try:
        pytrends = TrendReq(
            hl="en-US",
            tz=360,
            timeout=(10, 25),
        )

        geo = "" if country == "Global" else country

        pytrends.build_payload(
            kw_list=[keyword],
            geo=geo,
            timeframe="today 12-m"
        )

        df = pytrends.interest_over_time()

        if df is None or df.empty:
            return {
                "Google Trends": {
                    "status": "empty",
                    "keyword": keyword,
                    "note": "No trend data returned (low volume or blocked)"
                }
            }

        if "isPartial" in df.columns:
            df = df.drop(columns=["isPartial"])

        df.reset_index(inplace=True)

        return {
            "Google Trends": df
        }

    except Exception as e:
        return {
            "Google Trends": {
                "status": "error",
                "keyword": keyword,
                "error": str(e),
                "note": "Google Trends blocks automated traffic aggressively",
                "trace": traceback.format_exc()
            }
        }
        
def fetch_google_trends_locations(keyword: str):
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload([keyword], timeframe="today 12-m")

    df = pytrends.interest_by_region(resolution="COUNTRY")

    if df is None or df.empty:
        return []

    return [
        {
            "location": idx,
            "value": int(row[keyword]),
        }
        for idx, row in df.iterrows()
        if row[keyword] > 0
    ]