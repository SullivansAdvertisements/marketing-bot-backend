import streamlit as st

# MUST be first Streamlit call
st.set_page_config(
    page_title="Marketing Bot",
    layout="wide"
)

# -------------------------------------------------
# Imports (match your oauth_meta.py exactly)
# -------------------------------------------------
from oauth_meta import (
    meta_login_url,
    exchange_code_for_token,
    fetch_ad_accounts,
    create_meta_campaign,
    create_meta_adset,
    create_meta_ad_creative,
    fetch_campaign_insights,
)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("🚀 Marketing Bot")

# -------------------------------------------------
# OAuth callback handling
# -------------------------------------------------
query = st.experimental_get_query_params()

st.markdown(f"[🔵 Connect Meta Ads]({meta_login_url()})")

if "code" in query and "meta_access_token" not in st.session_state:
    try:
        access_token = exchange_code_for_token(query["code"][0])
        st.session_state["meta_access_token"] = access_token
        st.success("Meta connected successfully 🎉")
    except Exception as e:
        st.error("Meta OAuth failed")
        st.exception(e)

# -------------------------------------------------
# Require auth beyond this point
# -------------------------------------------------
if "meta_access_token" not in st.session_state:
    st.stop()

# -------------------------------------------------
# Fetch Ad Accounts
# -------------------------------------------------
st.header("📂 Ad Accounts")

accounts_response = fetch_ad_accounts(st.session_state["meta_access_token"])
accounts = accounts_response.get("data", [])

if not accounts:
    st.warning("No ad accounts found.")
    st.stop()

account_map = {}
for acct in accounts:
    label = acct.get("name", acct["id"])
    clean_id = acct["id"].replace("act_", "")
    account_map[label] = clean_id
    st.success(f"{label} ({acct['id']})")

selected_account_name = st.selectbox(
    "Select Ad Account",
    list(account_map.keys())
)

selected_account_id = account_map[selected_account_name]

# -------------------------------------------------
# CAMPAIGN BUILDER
# -------------------------------------------------
st.divider()
st.header("📣 Campaign Builder")

campaign_name = st.text_input("Campaign Name", "My First Campaign")

OBJECTIVES = {
    "Traffic": "TRAFFIC",
    "Leads": "LEAD_GENERATION",
    "Sales": "OUTCOME_SALES",
    "Awareness": "OUTCOME_AWARENESS",
    "Engagement": "POST_ENGAGEMENT",
}

objective_label = st.selectbox("Objective", list(OBJECTIVES.keys()))
objective = OBJECTIVES[objective_label]

daily_budget = st.number_input(
    "Daily Budget ($)",
    min_value=5,
    value=10,
    step=5
)

if st.button("🚀 Create Campaign"):
    try:
        result = create_meta_campaign(
            access_token=st.session_state["meta_access_token"],
            ad_account_id=selected_account_id,
            name=campaign_name,
            objective=objective,
            daily_budget=int(daily_budget * 100),
        )
        st.success("Campaign created (PAUSED)")
        st.session_state["campaign_id"] = result["id"]
        st.json(result)
    except Exception as e:
        st.error("Campaign creation failed")
        st.exception(e)

# -------------------------------------------------
# AD SET BUILDER
# -------------------------------------------------
st.divider()
st.header("🎯 Ad Set Builder")

campaign_id = st.text_input(
    "Campaign ID",
    value=st.session_state.get("campaign_id", "")
)

adset_name = st.text_input("Ad Set Name", "Ad Set 1")

age_min = st.slider("Age Min", 18, 65, 18)
age_max = st.slider("Age Max", 18, 65, 45)

countries = st.multiselect(
    "Countries",
    ["US", "CA", "GB", "AU"],
    default=["US"]
)

start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

adset_budget = st.number_input(
    "Daily Ad Set Budget ($)",
    min_value=5,
    value=10,
    step=5
)

if st.button("Create Ad Set"):
    try:
        result = create_meta_adset(
            access_token=st.session_state["meta_access_token"],
            ad_account_id=selected_account_id,
            campaign_id=campaign_id,
            name=adset_name,
            daily_budget=int(adset_budget * 100),
            start_time=str(start_date),
            end_time=str(end_date),
            geo_countries=countries,
            age_min=age_min,
            age_max=age_max,
        )
        st.success("Ad Set created (PAUSED)")
        st.session_state["adset_id"] = result["id"]
        st.json(result)
    except Exception as e:
        st.error("Ad Set creation failed")
        st.exception(e)

# -------------------------------------------------
# CREATIVE BUILDER
# -------------------------------------------------
st.divider()
st.header("🎨 Creative Builder")

page_id = st.text_input("Facebook Page ID")
headline = st.text_input("Headline", "Shop the New Drop")
primary_text = st.text_area(
    "Primary Text",
    "Limited stock. Tap to shop now."
)

if st.button("Create Creative"):
    try:
        creative = create_meta_ad_creative(
            access_token=st.session_state["meta_access_token"],
            ad_account_id=selected_account_id,
            page_id=page_id,
            headline=headline,
            primary_text=primary_text,
        )
        st.success("Creative created")
        st.json(creative)
    except Exception as e:
        st.error("Creative creation failed")
        st.exception(e)

# -------------------------------------------------
# INSIGHTS
# -------------------------------------------------
st.divider()
st.header("📊 Campaign Insights")

insights_campaign_id = st.text_input(
    "Campaign ID for Insights",
    value=campaign_id
)

if st.button("Load Insights"):
    try:
        insights = fetch_campaign_insights(
            st.session_state["meta_access_token"],
            insights_campaign_id
        )
        st.json(insights)
    except Exception as e:
        st.error("Failed to load insights")
        st.exception(e)