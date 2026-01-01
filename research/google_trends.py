import pandas as pd
import datetime


def fetch_google_trends(keyword: str, country: str = "US"):
    """
    Streamlit-safe Google Trends stub.
    Never crashes the app.

    Returns:
        pd.DataFrame
    """

    if not keyword:
        return pd.DataFrame()

    # Simulated trend data (replace later with pytrends)
    today = datetime.date.today()

    data = {
        "date": [
            today - datetime.timedelta(days=30),
            today - datetime.timedelta(days=21),
            today - datetime.timedelta(days=14),
            today - datetime.timedelta(days=7),
            today,
        ],
        "interest": [42, 55, 63, 71, 78],
        "keyword": [keyword] * 5,
        "country": [country] * 5,
    }

    return pd.DataFrame(data)