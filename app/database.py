from models.oauth_token import OAuthToken
from models.ad_account import AdAccount


def save_meta_token(db, user_id, access_token):
    token = OAuthToken(
        user_id=user_id,
        platform="meta",
        access_token=access_token
    )
    db.add(token)
    db.commit()


def save_meta_accounts(db, user_id, accounts):
    for acct in accounts:
        record = AdAccount(
            user_id=user_id,
            platform="meta",
            account_id=acct["id"],
            account_name=acct.get("name")
        )
        db.add(record)
    db.commit()