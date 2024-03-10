import streamlit as st
from datetime import time, datetime

st.title("30 Days of Streamlit")
st.markdown("### Day 8")
st.header("st.slider")

age = st.slider("How old are you?", 0, 130, 25)
st.write("I'm", age, "years old")

st.subheader("Range slider")

values = st.slider(
    "Select a range pf values",
    0.0, 100.0, (25.0, 75.0)
)
st.write("Values:", values)
