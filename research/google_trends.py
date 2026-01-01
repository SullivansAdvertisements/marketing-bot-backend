from pytrends.request import TrendReq

def fetch_google_trends(keyword, geo="US", timeframe="today 5-y"):
    pytrends = TrendReq(hl="en-US", tz=360)

    pytrends.build_payload(
        [keyword],
        timeframe=timeframe,
        geo=geo,
        gprop=""
    )

    return {
        "interest_over_time": pytrends.interest_over_time().reset_index().to_dict(),
        "related_queries": pytrends.related_queries(),
        "related_topics": pytrends.related_topics(),
        "interest_by_region": pytrends.interest_by_region().reset_index().to_dict(),
    }