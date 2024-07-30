import pandas as pd
import streamlit as st

st.title("30 Days of Streamlit")
st.markdown("### Day 18")

st.header("st.file_uploader")
st.subheader("Input CSV")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("DataFrame")
    st.write(df)
    st.subheader("Descriptive Statitics")
    st.write(df.describe())
else:
    st.info("Upload a CSV file")
