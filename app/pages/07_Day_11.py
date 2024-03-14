import streamlit as st

st.title("30 Days of Streamlit")
st.markdown("### Day 11")

st.header("st.multiselect")

options = st.multiselect(
    "What are your favorite colors",
    ["Green", "Yellow", "Red", "Blue"],
    ["Yellow", "Red"],
)

st.write("You selected:", options)
