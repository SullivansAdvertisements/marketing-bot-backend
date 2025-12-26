from google.ads.googleads.client import GoogleAdsClient

def fetch_keywords(client: GoogleAdsClient, keyword):
    service = client.get_service("KeywordPlanIdeaService")
    # real keyword planner request