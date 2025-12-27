import os
import sys
import streamlit as st

st.title("Streamlit Debug")

st.write("Current working directory:")
st.code(os.getcwd())

st.write("Files in current directory:")
st.code(os.listdir(os.getcwd()))

st.write("sys.path:")
st.code(sys.path)