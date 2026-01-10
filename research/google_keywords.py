def generate_google_ads_keywords(seed_keyword: str, country_id: str = "2840"):
    """
    Generate keyword ideas using Google Ads Keyword Planner.
    country_id: 2840 = United States
    """

    try:
        from google.ads.googleads.client import GoogleAdsClient
    except ImportError:
        raise RuntimeError("google-ads SDK not installed")

    client = GoogleAdsClient.load_from_env()

    customer_id = client.login_customer_id or client.customer_id
    keyword_plan_idea_service = client.get_service(
        "KeywordPlanIdeaService"
    )

    geo_target_service = client.get_service("GeoTargetConstantService")

    location_rn = geo_target_service.geo_target_constant_path(country_id)

    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.geo_target_constants.append(location_rn)
    request.language = "languageConstants/1000"  # English
    request.keyword_plan_network = (
        client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
    )
    request.keyword_seed.keywords.append(seed_keyword)

    response = keyword_plan_idea_service.generate_keyword_ideas(
        request=request
    )

    results = []

    for idea in response:
        metrics = idea.keyword_idea_metrics
        results.append({
            "keyword": idea.text,
            "avg_monthly_searches": metrics.avg_monthly_searches,
            "competition": metrics.competition.name,
            "competition_index": metrics.competition_index,
            "top_of_page_cpc_low": (
                metrics.low_top_of_page_bid_micros / 1_000_000
                if metrics.low_top_of_page_bid_micros else 0
            ),
            "top_of_page_cpc_high": (
                metrics.high_top_of_page_bid_micros / 1_000_000
                if metrics.high_top_of_page_bid_micros else 0
            ),
            "source": "google_ads",
        })

    return results