# research/google_trends.py

from pytrends.request import TrendReq
import pandas as pd
import time
import random


def fetch_google_trends(keyword: str, country: str = "US"):
    """
    Enterprise-safe Google Trends fetcher.
    - No index limits
    - No slicing
    - No hard assumptions
    - Never crashes router
    """

    try:
        pytrends = TrendReq(
            hl="en-US",
            tz=360,
            timeout=(10, 25),
            retries=3,
            backoff_factor=0.4,
        )

        geo = "" if country == "Global" else country

        # ---- BUILD PAYLOAD (no limits) ----
        pytrends.build_payload(
            kw_list=[keyword],
            timeframe="today 12-m",  # max stable window
            geo=geo,
        )

        results = {}

        # ---- INTEREST OVER TIME (FULL) ----
        iot = pytrends.interest_over_time()
        if isinstance(iot, pd.DataFrame) and not iot.empty:
            iot = iot.drop(columns=["isPartial"], errors="ignore")
            results["Google Trends – Interest Over Time"] = iot

        # ---- RELATED QUERIES (ALL, NO LIMITS) ----
        rq = pytrends.related_queries()
        if rq and keyword in rq:
            for k, df in rq[keyword].items():
                if isinstance(df, pd.DataFrame) and not df.empty:
                    results[f"Google Trends – Related Queries ({k})"] = df

        # ---- RELATED TOPICS (ALL, NO LIMITS) ----
        rt = pytrends.related_topics()
        if rt and keyword in rt:
            for k, df in rt[keyword].items():
                if isinstance(df, pd.DataFrame) and not df.empty:
                    results[f"Google Trends – Related Topics ({k})"] = df

        # ---- INTEREST BY REGION (ALL REGIONS) ----
        try:
            regions = pytrends.interest_by_region(
                resolution="COUNTRY",
                inc_low_vol=True,
                inc_geo_code=False,
            )
            if isinstance(regions, pd.DataFrame) and not regions.empty:
                results["Google Trends – Interest by Region"] = regions
        except Exception:
            pass  # Region data is optional

        if not results:
            return {
                "Google Trends": {
                    "status": "blocked",
                    "reason": "Google returned empty response (captcha or rate-limit)",
                }
            }

        return results

    except Exception as e:
        return {
            "Google Trends": {
                "status": "error",
                "error": str(e),
                "note": "Google Trends blocks automated traffic aggressively",
            }
        }