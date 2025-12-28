from pytrends.request import TrendReq

def get_google_trends(
    keyword: str,
    geo: str = "US",
    timeframe: str = "today 12-m",
):
    pytrends = TrendReq(hl="en-US", tz=360)

    pytrends.build_payload(
        kw_list=[keyword],
        geo=geo,
        timeframe=timeframe,
    )

    interest = pytrends.interest_over_time()

    if interest.empty:
        return []

    interest = interest.reset_index()

    return [
        {
            "date": str(row["date"]),
            "interest": int(row[keyword]),
        }
        for _, row in interest.iterrows()
    ]