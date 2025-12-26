def allocate_budget(total_budget, platforms):
    allocation = {}
    remaining = total_budget

    if "google" in platforms and total_budget >= 300:
        allocation["google"] = 0.4 * total_budget
        remaining -= allocation["google"]

    if "meta" in platforms:
        allocation["meta"] = remaining * 0.5

    if "tiktok" in platforms:
        allocation["tiktok"] = remaining * 0.5

    return allocation