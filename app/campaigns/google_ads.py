def create_google_campaign(client, customer_id):
    service = client.get_service("CampaignService")
    # real campaign creation request