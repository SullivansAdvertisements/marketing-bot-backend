# research/google_trends.py
import pandas as pd
from pytrends.request import TrendReq
import traceback

def fetch_google_trends(keyword: str, country: str = "US"):
    """
    Unlimited, index-safe Google Trends fetch.
    Never assumes list positions.
    Never crashes router.
    """

    try:
        pytrends = TrendReq(
            hl="en-US",
            tz=360,
            timeout=(10, 25),
            retries=2,
            backoff_factor=0.2,
        )

        geo = "" if country == "Global" else country

        pytrends.build_payload(
            kw_list=[keyword],
            geo=geo,
            timeframe="today 12-m"
        )

        interest = pytrends.interest_over_time()

        if interest is None or interest.empty:
            return {
                "Google Trends": {
                    "status": "empty",
                    "keyword": keyword,
                    "note": "Google returned no trend data (common for low-volume or blocked queries)"
                }
            }

        # Remove isPartial column if present
        if "isPartial" in interest.columns:
            interest = interest.drop(columns=["isPartial"])

        interest.reset_index(inplace=True)

        return {
            "Google Trends": interest
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