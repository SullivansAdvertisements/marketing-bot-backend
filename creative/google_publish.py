from google.ads.googleads.client import GoogleAdsClient
import os


def publish_google_ad(headline, description):
    config = {
        "developer_token": os.getenv("GOOGLE_DEVELOPER_TOKEN"),
        "refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN"),
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "use_proto_plus": True,
    }

    client = GoogleAdsClient.load_from_dict(config)
    customer_id = os.getenv("GOOGLE_CUSTOMER_ID")

    return {
        "status": "ready",
        "headline": headline,
        "description": description,
        "customer_id": customer_id,
    }