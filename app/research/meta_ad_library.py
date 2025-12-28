import requests

def search_meta_ad_library(
    keyword: str,
    country: str = "US",
    access_token: str = None
):
    url = "https://graph.facebook.com/v19.0/ads_archive"

    params = {
        "search_terms": keyword,
        "ad_active_status": "ALL",
        "ad_type": "ALL",
        "countries": [country],
        "fields": "ad_creative_body,ad_creative_link_title,page_name",
        "access_token": access_token,
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if "error" in data:
        raise Exception(data)

    return data.get("data", [])