import json
from typing import Any, Literal

import folium
import pandas as pd
from shapely.geometry.base import BaseGeometry
import streamlit as st
from lib.region_builder import region_builder
from shapely import Point
from shapely.geometry import shape
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🍨",
    layout="wide",
    initial_sidebar_state="expanded",
)

map_tile = "https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png"


@st.cache_data
def _load_region() -> pd.DataFrame:
    """
    GeoJSON ファイルパスの一覧を取得する

    Returns:
        pd.DataFrame: ファイルパスの一覧
    """
    return pd.read_csv("./static/unit.csv")


@st.cache_data
def _load_file(area) -> Any:
    """
    選択したエリアの GeoJSON ファイルを読み込む

    Args:
        area (_type_): _description_

    Returns:
        Any: GeoJSON
    """
    df: pd.DataFrame = _load_region()
    file = df[df["unit"] == area]["filename"].tolist()
    file_path: str = f"./static/GeoJSON/{file[0]}"

    # GeoJSONファイルを読み込む
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


@st.cache_data
def _base_map(center) -> folium.Map:
    """
    ベースマップを作成する

    Args:
        center ([float, float]): マップの中心位置

    Returns:
        folium.Map: ベースマップ
    """
    return folium.Map(
        location=center,
        zoom_start=8,
        center=center,
        tiles=map_tile,
        attr="""<a href="https://maps.gsi.go.jp/development/ichiran.html">地理院タイル</a>""",
    )


def _map_center(geo_json_data) -> tuple[float, float]:
    """
    GeoJson の中心位置を求める

    Args:
        geo_json_data (_type_): _description_

    Returns:
        tuple[float, float]: latitude, longitude
    """
    try:
        # GeoJSONデータからシェイプを作成
        geom = shape(geo_json_data["features"][0]["geometry"])
        # st.code(0)
    except AttributeError:
        geom: BaseGeometry = shape(geo_json_data["features"][1]["geometry"])
        # st.code(1)

    centroid: Point = geom.centroid
    return centroid.y, centroid.x


prefecture, cities = region_builder(True, True)

if cities is None:
    st.success(f"都道府県:{prefecture}")
    area: Any | None | Literal["北海道"] = prefecture

if cities is not None:
    st.write("選択された市区町村:")
    st.write(f"{city}　" for city in cities)
    area = cities

geo_json_data = _load_file(area)

latitude, longitude = _map_center(geo_json_data)

m: folium.Map = _base_map([latitude, longitude])

folium.GeoJson(
    geo_json_data,
    zoom_on_click=True,
    style_function=lambda feature: {
        "fillColor": (
            "tomato"
            if prefecture in feature["properties"]["N03_001"].lower()
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

st_folium(m, use_container_width=True, height=900, returned_objects=[])
