import streamlit as st
import pandas as pd

from strategy.budget_allocator import allocate_budget
from strategy.performance_estimator import estimate_performance


def render():
    st.header("📈 Strategy & Budget Optimization")

    meta_token = (
        st.secrets.get("META_ACCESS_TOKEN")
        or st.session_state.get("META_ACCESS_TOKEN")
    )
    google_token = (
        st.secrets.get("GOOGLE_ADS_API_KEY")
        or st.session_state.get("GOOGLE_ADS_API_KEY")
    )

    meta_connected = bool(meta_token)
    google_connected = bool(google_token)

    st.subheader("Connected Platforms")

    c1, c2 = st.columns(2)
    c1.metric("Meta Ads", "Connected" if meta_connected else "Not Connected")
    c2.metric("Google Ads", "Connected" if google_connected else "Not Connected")

    available_platforms = []
    if meta_connected:
        available_platforms.append("Meta")
    if google_connected:
        available_platforms.append("Google")

    if not available_platforms:
        st.warning("Connect at least one platform to run strategy optimization.")
        return

    st.subheader("Strategy Inputs")

    platforms = st.multiselect(
        "Platforms to include",
        available_platforms,
        default=available_platforms,
    )

    total_budget = st.number_input(
        "Total Monthly Budget ($)",
        min_value=100,
        value=2000,
        step=100,
    )

    objective = st.selectbox(
        "Optimization Objective",
        ["Maximize Conversions", "Maximize ROAS", "Maximize Clicks"],
    )

    if not st.button("🚀 Run Optimization"):
        return

    if not platforms:
        st.error("Select at least one platform.")
        return

    st.subheader("📊 Performance Estimates")

    estimates = []

    if "Meta" in platforms and meta_token:
        estimates.append(
            estimate_performance(
                platform="meta",
                token=meta_token,
                objective=objective,
                budget=total_budget,
            )
        )

    if "Google" in platforms and google_token:
        estimates.append(
            estimate_performance(
                platform="google",
                token=google_token,
                objective=objective,
                budget=total_budget,
            )
        )

    if not estimates:
        st.warning("No estimates returned.")
        return

    st.dataframe(pd.DataFrame(estimates), use_container_width=True)

    st.subheader("💰 Optimized Budget Allocation")

    allocation = allocate_budget(
        total_budget=total_budget,
        platform_estimates=estimates,
        objective=objective,
    )

    st.dataframe(pd.DataFrame(allocation), use_container_width=True)

    st.subheader("🧠 Strategy Summary")

    for row in allocation:
        st.markdown(
            f"""
            **{row['platform']}**
            - Budget: **${row['budget']:,}**
            - Expected Results: **{row['expected_result']}**
            """
        )