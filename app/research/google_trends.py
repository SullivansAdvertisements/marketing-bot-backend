from pytrends.request import TrendReq

def get_google_trends(
    keyword: str,
    geo: str = "US",
    timeframe: str = "today 12-m"
):
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(
        [keyword],
        timeframe=timeframe,
        geo=geo
    )

    interest = pytrends.interest_over_time()

    if interest.empty:
        return []

    return interest.reset_index().to_dict(orient="records")