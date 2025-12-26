from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

def create_meta_campaign(account_id, name, objective):
    account = AdAccount(account_id)
    return account.create_campaign(params={
        "name": name,
        "objective": objective,
        "status": "PAUSED"
    })