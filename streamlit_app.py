import streamlit as st
from oauth_meta import meta_login_url, exchange_code_for_token

st.title("Marketing Bot")

st.success("Imports resolved ✅")

st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")

query = st.experimental_get_query_params()

if "code" in query:
    try:
        token = exchange_code_for_token(query["code"][0])

        st.success("Meta connected successfully 🎉")

        accounts = fetch_ad_accounts(token["access_token"])

        st.subheader("Your Meta Ad Accounts")

        if not accounts:
            st.warning("No ad accounts found.")
        else:
            for acc in accounts:
                st.write(
                    f"🧾 {acc['name']} "
                    f"({acc['id']}) | "
                    f"{acc['currency']} | "
                    f"{acc['timezone_name']}"
                )

        st.experimental_set_query_params()

    except Exception as e:
        st.error("Meta OAuth or account fetch failed")
        st.exception(e)