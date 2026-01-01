import streamlit as st
import pandas as pd

from research.google_trends import google_trends_tab
from research.google_keywords import google_keywords_tab
from research.meta_ad_library import meta_ads_tab
from research.tiktok_trends import tiktok_trends_tab
from research.youtube_trends import youtube_trends_tab


def render():
    st.header("🔎 Advanced Market Research")

    tabs = st.tabs([
        "📈 Google Trends",
        "🔍 Google Keywords",
        "📘 Meta Ads",
        "🎵 TikTok Trends",
        "▶️ YouTube Trends",
    ])

    with tabs[0]:
        google_trends_tab()

    with tabs[1]:
        google_keywords_tab()

    with tabs[2]:
        meta_ads_tab()

    with tabs[3]:
        tiktok_trends_tab()

    with tabs[4]:
        youtube_trends_tab()