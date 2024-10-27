import h3.api.memview_int as h3
import streamlit as st

st.title("memview_int")

h = h3.latlng_to_cell(0, 0, 0)

st.write(h)

mv = h3.grid_ring(h, 1)

st.write(mv)
st.write(mv[0])
st.write(list(mv))
