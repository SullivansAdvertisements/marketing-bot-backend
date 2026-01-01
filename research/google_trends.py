from pytrends.request import TrendReq
import pandas as pd


def fetch_google_trends(keyword: str, country: str = "US"):
    if not keyword:
        return pd.DataFrame()

    pytrends = TrendReq(hl="en-US", tz=360)

    geo = "" if country == "Global" else country
    pytrends.build_payload([keyword], timeframe="today 12-m", geo=geo)

    df = pytrends.interest_over_time()

    if df.empty:
        return pd.DataFrame()

    df = df.reset_index()
    df.rename(columns={keyword: "interest"}, inplace=True)

    return df[["date", "interest"]]