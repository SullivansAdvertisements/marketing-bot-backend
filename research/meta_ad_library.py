def fetch_meta_ads(keyword: str):
    results = []

    # ... your API call logic above ...

    for ad in response.get("data", []):
        if not isinstance(ad, dict):
            continue  # 🚫 skip malformed entries

        results.append({
            "platform": "facebook",
            "page_name": ad.get("page_name") or ad.get("page_name_en") or "Unknown",
            "ad_creative": (
                ad.get("ad_creative_body")
                or ad.get("creative_bodies", [""])[0]
                if isinstance(ad.get("creative_bodies"), list)
                else ""
            ),
            "ad_copy": (
                ad.get("ad_creative_body")
                or ad.get("ad_snapshot_url", "")
            ),
            "cta": ad.get("call_to_action_type", ""),
            "active": True,
            "source": "meta_ad_library",
            "locations": ad.get("delivery_by_region", []),
        })

    return results
