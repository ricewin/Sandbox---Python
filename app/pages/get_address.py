"""A module that provides the ability to search for the location of landmarks."""

from typing import Any, Coroutine

import folium
import streamlit as st
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium


def get_address(symbol: str) -> Coroutine[Any, Any, Any | None] | Any | None:
    """
    Get Address

    Args:
        landmark (str): Symbol

    Returns:
        Coroutine[Any, Any, Any | None] | Any | None: location
    """
    geolocator = Nominatim(user_agent="anonymous")
    return geolocator.geocode(symbol)


# 検索する名称
landmark: str = st.text_input("Find a location")

location: Coroutine[Any, Any, Any | None] | Any | None = get_address(landmark)

if location is None:
    # st.snow()
    st.write("No maps.")
else:
    with st.expander("Raw data."):
        st.write(location.raw)  # type: ignore

    address = location.address  # type: ignore
    latitude = location.latitude  # type: ignore
    longitude = location.longitude  # type: ignore
    st.write("住所:", address)
    st.write("緯度:", latitude)
    st.write("経度:", longitude)

    # ランドマークを中心に、マーカーを追加
    m = folium.Map(location=[latitude, longitude], zoom_start=16)
    folium.Marker([latitude, longitude], popup=landmark, tooltip=landmark).add_to(m)

    # StreamlitでFoliumマップをレンダリングするために呼び出すが、
    # マップからデータを返さない（ユーザーが操作してもアプリが再実行されないようにするため）。
    st_folium(m, width=725, returned_objects=[])
