from operator import sub
from typing import Any

import folium
import geopandas as gpd  # type: ignore
import streamlit as st
from streamlit_folium import st_folium


# GeoJSONファイルを読み込む
@st.cache_data
def _load_file(file_path) -> Any:
    return gpd.read_file(file_path)


def get_unique_values_from_geojson(data, property_name) -> Any:
    """
    GeoJSON データから指定されたプロパティのユニークな値を取得する

    Args:
        data (_type_): GeoJSON データ
        property_name (_type_): 取得したいプロパティの名前

    Returns:
        set[Any]: ユニークな値のセット
    """
    return data.loc[:, [property_name]]


# Streamlit アプリのタイトル
st.title("北海道の振興局")

file_path: str = (
    "https://raw.githubusercontent.com/ricewin/simplify-japan-geojson/refs/heads/main/GeoJson/N03-20240101_01_subprefecture.json"
)
data = _load_file(file_path)

# ユニークな値を取得
property_name = "N03_002"
subprefectures: set[Any] = get_unique_values_from_geojson(data, property_name)


# 北海道の振興局を選択するラジオボタン
selected_region: str | None = st.radio(
    "地域を選択してください", subprefectures, horizontal=True
)

map_tile = "https://cyberjapandata.gsi.go.jp/xyz/blank/{z}/{x}/{y}.png"
# map_tile = "https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png"

m = folium.Map(
    location=[43, 143.5],
    zoom_start=7,
    tiles=map_tile,
    attr="""<a href="https://maps.gsi.go.jp/development/ichiran.html">地理院タイル</a>""",
)

folium.GeoJson(
    data,
    zoom_on_click=True,
    style_function=lambda feature: {
        "fillOpacity": 0.5,
        "fillColor": (
            "tomato"
            if selected_region in feature["properties"]["N03_002"].lower()
            else "olive"
        ),
        "color": "royalblue",
        "weight": 2,
        "dashArray": "5, 5",
    },
).add_to(m)

folium.plugins.Fullscreen(  # type: ignore
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
).add_to(m)

st_folium(m, use_container_width=True, returned_objects=[])
