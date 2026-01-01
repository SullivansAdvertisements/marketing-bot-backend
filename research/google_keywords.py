from google.ads.googleads.client import GoogleAdsClient

def fetch_google_keywords(
    customer_id: str,
    seed_keyword: str,
    geo_target_id: str = "2840",  # US
    language_id: str = "1000"     # English
):
    client = GoogleAdsClient.load_from_storage()

    service = client.get_service("KeywordPlanIdeaService")
    geo_service = client.get_service("GeoTargetConstantService")

    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = f"languageConstants/{language_id}"
    request.geo_target_constants.append(
        geo_service.geo_target_constant_path(geo_target_id)
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
            "low_bid": metrics.low_top_of_page_bid_micros / 1e6,
            "high_bid": metrics.high_top_of_page_bid_micros / 1e6,
            "trend": list(metrics.monthly_search_volumes),
        })

    return results