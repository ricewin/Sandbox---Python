import folium
import streamlit as st
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium


def GetAddress(landmark: str):
    geolocator = Nominatim(user_agent="anonymous")
    g = geolocator.geocode(landmark)
    return g


# 検索する名称
landmark = st.text_input("Destination")

location = GetAddress(landmark)


if location is None:
    st.snow()
    st.write("No maps.")
else:
    with st.expander("Raw data."):
        st.write(location.raw)

    address = location.address
    latitude = location.latitude
    longitude = location.longitude
    st.write("住所:", address)
    st.write("緯度:", latitude)
    st.write("経度:", longitude)

    # ランドマークを中心に、マーカーを追加
    m = folium.Map(location=[latitude, longitude], zoom_start=16)
    folium.Marker([latitude, longitude], popup=landmark, tooltip=landmark).add_to(m)

    # StreamlitでFoliumマップをレンダリングするために呼び出すが、
    # マップからデータを返さない（ユーザーが操作してもアプリが再実行されないようにするため）。
    st_folium(m, width=725, returned_objects=[])
