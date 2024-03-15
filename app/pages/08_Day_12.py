import streamlit as st

st.title("30 Days of Streamlit")
st.markdown("### Day 12")

st.header("st.checkbox")

st.write("What would you like to order?")

icecream = st.checkbox("Ice cream")
coffee = st.checkbox("Coffee")
cola = st.checkbox("Cola")

if icecream:
    st.write("Great! Here's some more :icecream:")

if coffee:
    st.write("Okay, here's some coffee :coffee:")

if cola:
    st.write("Here you go :tumbler_glass:")
