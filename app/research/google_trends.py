from pytrends.request import TrendReq

def fetch_google_trends(keyword, geo, timeframe):
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)
    return pytrends.interest_over_time().to_dict()