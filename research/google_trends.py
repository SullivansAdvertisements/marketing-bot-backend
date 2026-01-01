import streamlit as st
import pandas as pd
from pytrends.request import TrendReq


def google_trends_tab():
    st.subheader("📈 Google Trends Analysis")

    keyword = st.text_input("Keyword", key="gt_keyword")
    region = st.selectbox("Region", ["US", "Worldwide"])

    if st.button("Analyze Trends"):
        try:
            pytrends = TrendReq(hl="en-US", tz=360)
            pytrends.build_payload([keyword], geo=region if region != "Worldwide" else "")
            data = pytrends.interest_over_time()

            if data.empty:
                st.warning("No trend data found.")
                return

            df = data.reset_index()
            st.line_chart(df.set_index("date")[keyword])
            st.dataframe(df.tail(12), use_container_width=True)

        except Exception as e:
            st.error("Google Trends unavailable.")
            st.caption(str(e))