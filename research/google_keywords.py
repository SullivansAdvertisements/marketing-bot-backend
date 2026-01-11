import os

# 🔒 FORCE PROTO MODE BEFORE SDK LOADS
os.environ["GOOGLE_ADS_USE_PROTO_PLUS"] = "True"

from google.ads.googleads.client import GoogleAdsClient


def generate_google_ads_keywords(seed_keyword: str, country_id: str = "2840"):

    config = {
        "developer_token": os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
        "client_id": os.environ["GOOGLE_ADS_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_ADS_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
        "login_customer_id": os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"].replace("-", ""),
        "use_proto_plus": True,
    }

    client = GoogleAdsClient.load_from_dict(config)

    service = client.get_service("KeywordPlanIdeaService")
    geo_service = client.get_service("GeoTargetConstantService")

    geo = geo_service.geo_target_constant_path(country_id)

    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = config["login_customer_id"]
    request.geo_target_constants.append(geo)
    request.language = "languageConstants/1000"
    request.keyword_plan_network = (
        client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
    )
    request.keyword_seed.keywords.append(seed_keyword)

    response = service.generate_keyword_ideas(request=request)

    results = []
    for idea in response:
        metrics = idea.keyword_idea_metrics
        results.append({
            "keyword": idea.text,
            "avg_monthly_searches": metrics.avg_monthly_searches,
            "competition": metrics.competition.name,
            "competition_index": metrics.competition_index,
            "top_of_page_cpc_low": (
                metrics.low_top_of_page_bid_micros / 1e6
                if metrics.low_top_of_page_bid_micros
                else 0
            ),
            "top_of_page_cpc_high": (
                metrics.high_top_of_page_bid_micros / 1e6
                if metrics.high_top_of_page_bid_micros
                else 0
            ),
            "source": "google_ads",
        })

    return results