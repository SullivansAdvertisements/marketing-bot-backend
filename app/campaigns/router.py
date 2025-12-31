def render(meta_token=None, google_token=None):
    import streamlit as st
    import pandas as pd

    st.subheader("Market Research")

    query = st.text_input("Search market / keyword")

    if query:
        df = pd.DataFrame({
            "Metric": ["Search Volume", "Competition", "CPC"],
            "Value": ["High", "Medium", "$1.45"]
        })
        st.dataframe(df, use_container_width=True)