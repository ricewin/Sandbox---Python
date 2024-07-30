import streamlit as st

st.title("30 Days of Streamlit")
st.markdown("### Day 10")

st.header("st.selectbox")

option = st.selectbox("What is your favorite color?", ("Blue", "Red", "Green"))

st.write("Your favorite color is", option)
