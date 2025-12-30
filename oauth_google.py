def exchange_google_code_for_token(code: str) -> dict:
    payload = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_REDIRECT_URI,
    }

    r = requests.post(GOOGLE_TOKEN_URL, data=payload, timeout=10)
    token = r.json()

    # 👇 THIS IS CRITICAL
    print("GOOGLE TOKEN RESPONSE:", token)

    if "error" in token:
        raise Exception(token)

    return token