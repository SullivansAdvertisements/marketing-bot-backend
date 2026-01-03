# research/google_trends.py

from pytrends.request import TrendReq
import pandas as pd

def fetch_google_trends(
    keywords,
    geo="US",
    timeframe="today 12-m"
):
    """
    Fetch full Google Trends data with:
    - Interest over time
    - Related queries
    - Related topics
    """

    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(
        kw_list=keywords,
        geo=geo,
        timeframe=timeframe
    )

    results = {}

    # -----------------------------
    # Interest Over Time
    # -----------------------------
    interest_df = pytrends.interest_over_time()
    if not interest_df.empty:
        interest_df = interest_df.reset_index()
        results["interest_over_time"] = interest_df

    # -----------------------------
    # Related Queries
    # -----------------------------
    related_queries = pytrends.related_queries()
    rq_rows = []

    for kw, data in related_queries.items():
        if data["top"] is not None:
            df = data["top"]
            df["keyword"] = kw
            df["type"] = "top"
            rq_rows.append(df)

        if data["rising"] is not None:
            df = data["rising"]
            df["keyword"] = kw
            df["type"] = "rising"
            rq_rows.append(df)

    if rq_rows:
        results["related_queries"] = pd.concat(rq_rows, ignore_index=True)

    # -----------------------------
    # Related Topics
    # -----------------------------
    related_topics = pytrends.related_topics()
    rt_rows = []

    for kw, data in related_topics.items():
        if data["top"] is not None:
            df = data["top"]
            df["keyword"] = kw
            df["type"] = "top"
            rt_rows.append(df)

        if data["rising"] is not None:
            df = data["rising"]
            df["keyword"] = kw
            df["type"] = "rising"
            rt_rows.append(df)

    if rt_rows:
        results["related_topics"] = pd.concat(rt_rows, ignore_index=True)

    return results