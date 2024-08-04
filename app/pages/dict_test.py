import pandas as pd
import streamlit as st


@st.cache_data
def _load_region() -> pd.DataFrame:
    return pd.read_csv("./static/regioncode_master_utf8_2020.csv")


@st.cache_data
def _load_city() -> pd.DataFrame:
    return pd.read_csv("./static/prefcode_citycode_master_utf8_2020.csv")


col1, col2 = st.columns(2)
with col1:
    df = _load_region()

    pref_dict = dict(zip(df["prefcode"], df["prefname"]))

    st.write(pref_dict)

with col2:
    df = _load_city()

    city_dict = dict(zip(df["citycode"], df["cityname"]))

    st.write(city_dict)
