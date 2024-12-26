import branca.colormap as cm
import folium
import geopandas as gpd  # type: ignore
import pandas as pd
import streamlit as st
from shapely.geometry import box  # type: ignore
from streamlit_folium import st_folium

data = {"meshcode": ["5340", "533947", "53394659", "53394649"], "area": [1, 3, 4, 2]}
df = pd.DataFrame(data)


def meshcode_to_polygon(meshcode):
    if len(meshcode) == 4:  # 1次メッシュ
        lat_base = int(meshcode[:2]) * 2 / 3
        lon_base = int(meshcode[2:]) + 100
        lat_diff = 2 / 3
        lon_diff = 1
    elif len(meshcode) == 6:  # 2次メッシュ
        lat_base = int(meshcode[:2]) * 2 / 3 + int(meshcode[4]) * 5 / 60
        lon_base = int(meshcode[2:4]) + 100 + int(meshcode[5]) * 7.5 / 60
        lat_diff = 5 / 60
        lon_diff = 7.5 / 60
    elif len(meshcode) == 8:  # 3次メッシュ
        lat_base = (
            int(meshcode[:2]) * 2 / 3
            + int(meshcode[4]) * 5 / 60
            + int(meshcode[6]) * 30 / 3600
        )
        lon_base = (
            int(meshcode[2:4])
            + 100
            + int(meshcode[5]) * 7.5 / 60
            + int(meshcode[7]) * 45 / 3600
        )
        lat_diff = 30 / 3600
        lon_diff = 45 / 3600
    else:
        raise ValueError("Invalid meshcode length.")

    return box(lon_base, lat_base, lon_base + lon_diff, lat_base + lat_diff)


df["geometry"] = df["meshcode"].map(meshcode_to_polygon)  # type: ignore

st.dataframe(df["geometry"], hide_index=True, use_container_width=True)


def get_color(value):
    color_map = {
        0: "red",
        1: "yellow",
        2: "green",
        3: "cyan",
        4: "blue",
    }
    return color_map.get(value, "gray")  # デフォルトカラーを設定


df["color"] = df["area"].map(get_color)

gdf = gpd.GeoDataFrame(df, geometry="geometry")

m = folium.Map(location=[35.682839, 139.759455], zoom_start=10)

for _, row in gdf.iterrows():
    folium.GeoJson(
        row["geometry"].__geo_interface__,
        style_function=lambda x, color=row["color"]: {
            "color": color,
            "fillColor": color,
            "fillOpacity": 0.6,
            "weight": 1,
        },
        tooltip=f"Meshcode: {row['meshcode']}, Area: {row['area']}",
    ).add_to(m)

colormap = cm.StepColormap(
    ["r", "y", "g", "c", "b"], vmin=0, vmax=5, index=[0, 1, 2, 3, 4, 5]
)
colormap.caption = "Area"
colormap.add_to(m)

folium.LayerControl().add_to(m)

st_folium(m, use_container_width=True, returned_objects=[])
