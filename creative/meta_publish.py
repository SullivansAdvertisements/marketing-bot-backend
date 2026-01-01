import os
import requests

META_TOKEN = os.getenv("META_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID")


def publish_meta_creative(headline, primary_text, cta):
    url = f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}/adcreatives"

    payload = {
        "access_token": META_TOKEN,
        "object_story_spec": {
            "page_id": "YOUR_PAGE_ID",
            "link_data": {
                "message": primary_text,
                "link": "https://yourwebsite.com",
                "name": headline,
                "call_to_action": {
                    "type": cta.upper().replace(" ", "_"),
                    "value": {"link": "https://yourwebsite.com"},
                },
            },
        },
    }

    res = requests.post(url, json=payload)

    if res.status_code != 200:
        raise Exception(res.text)

    return res.json()