# app/strategy/router.py

import streamlit as st
import pandas as pd

from strategy.budget_allocator import allocate_budget
from strategy.performance_estimator import estimate_performance


def render():
    st.header("📈 Strategy & Budget Optimization")

    # ----------------------------
    # PLATFORM AVAILABILITY
    # ----------------------------
    meta_connected = bool(st.session_state.get("meta_token"))
    google_connected = bool(st.session_state.get("google_token"))

    st.subheader("Connected Platforms")

    cols = st.columns(2)
    with cols[0]:
        st.metric("Meta Ads", "Connected" if meta_connected else "Not connected")
    with cols[1]:
        st.metric("Google Ads", "Connected" if google_connected else "Not connected")

    available_platforms = []
    if meta_connected:
        available_platforms.append("Meta")
    if google_connected:
        available_platforms.append("Google")

    if not available_platforms:
        st.warning("Connect at least one platform to run strategy optimization.")
        return

    # ----------------------------
    # USER INPUTS
    # ----------------------------
    st.subheader("Strategy Inputs")

    platforms = st.multiselect(
        "Choose platforms to include",
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

    run = st.button("🚀 Run Optimization")

    if not run:
        return

    if not platforms:
        st.error("Select at least one platform.")
        return

    # ----------------------------
    # PERFORMANCE ESTIMATION
    # ----------------------------
    st.subheader("📊 Performance Estimates")

    estimates = []

    if "Meta" in platforms:
        meta_estimate = estimate_performance(
            platform="meta",
            token=st.session_state["meta_token"],
            objective=objective,
            budget=total_budget,
        )
        estimates.append(meta_estimate)

    if "Google" in platforms:
        google_estimate = estimate_performance(
            platform="google",
            token=st.session_state["google_token"],
            objective=objective,
            budget=total_budget,
        )
        estimates.append(google_estimate)

    estimates_df = pd.DataFrame(estimates)
    st.dataframe(estimates_df, use_container_width=True)

    # ----------------------------
    # BUDGET ALLOCATION
    # ----------------------------
    st.subheader("💰 Optimized Budget Allocation")

    allocation = allocate_budget(
        total_budget=total_budget,
        platform_estimates=estimates,
        objective=objective,
    )

    allocation_df = pd.DataFrame(allocation)
    st.dataframe(allocation_df, use_container_width=True)

    # ----------------------------
    # FINAL STRATEGY SUMMARY
    # ----------------------------
    st.subheader("🧠 Strategy Summary")

    for row in allocation:
        st.markdown(
            f"""
            **{row['platform']}**
            - Budget: **${row['budget']:,}**
            - Expected Results: **{row['expected_result']}**
            """
        )
