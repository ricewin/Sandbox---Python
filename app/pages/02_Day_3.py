import streamlit as st

st.title("30 Days of Streamlit")
st.markdown("Start the challenge")
st.markdown("### Day 3")

st.header("st.button")
if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")
