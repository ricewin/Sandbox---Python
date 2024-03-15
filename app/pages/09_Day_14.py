import pandas as pd
import streamlit as st
from streamlit_pandas_profiling import st_profile_report

st.title("30 Days of Streamlit")
st.markdown("### Day 14")

st.header("`streamlit_pandas_profiling`")

df = pd.read_csv(
    "https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv"
)

pr = df.profile_report()
st_profile_report(pr)
