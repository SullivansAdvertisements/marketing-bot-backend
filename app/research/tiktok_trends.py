import requests

def get_tiktok_trends(keyword: str):
    url = "https://www.tiktok.com/api/search/general/full/"

    params = {
        "keyword": keyword,
        "offset": 0,
        "count": 10,
    }

    r = requests.get(url, params=params)
    data = r.json()

    return [
        {
            "desc": item.get("desc"),
            "likes": item.get("stats", {}).get("diggCount"),
            "shares": item.get("stats", {}).get("shareCount"),
            "plays": item.get("stats", {}).get("playCount"),
        }
        for item in data.get("item_list", [])
    ]