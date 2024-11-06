"""
H3HexagonLayer
==============

Plot of values for a particular hex ID in the H3 geohashing scheme.
"""

from typing import List

import branca.colormap as cm
import h3
import pandas as pd
import pydeck as pdk
import streamlit as st


@st.cache_resource(ttl="2d")
def get_quantiles(df_column: pd.Series, quantiles: List) -> pd.Series:
    return df_column.quantile(quantiles)


@st.cache_resource(ttl="2d")
def get_color(
    df_column: pd.Series, colors: List, vmin: int, vmax: int, index: pd.Series
) -> pd.Series:
    color_map = cm.LinearColormap(colors, vmin=vmin, vmax=vmax, index=index)  # type: ignore
    return df_column.apply(color_map.rgb_bytes_tuple)


@st.cache_resource(ttl="2d")
def get_layer(df: pd.DataFrame) -> pdk.Layer:
    return pdk.Layer(
        "H3HexagonLayer",
        df,
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        get_hexagon="hex",
        get_fill_color="color",
        get_line_color="color",
        line_width_min_pixels=1,
        get_elevation="count",
        auto_highlight=True,
        elevation_scale=50,
        elevation_range=[0, 3000],
        coverage=1,
        opacity=0.5,
    )


@st.fragment
def h3_layer_map(
    df: pd.DataFrame,
    target: str,
    calc: str = "count",
    resolution: int = 5,
    zoom: int = 6,
    pitch: int = 0,
) -> None:
    """
    H3HexagonLayer

    Args:
        df (pd.DataFrame): _description_
        target (str): _description_
        calc (str, optional): count, mean. Defaults to "count".
        resolution (int, optional): 解像度レベル. Defaults to 5.
        zoom (int, optional): ズームレベル. 1 to 10. Defaults to 6.
        pitch (int, optional): ビューの角度. Defaults to 0.
    """
    # st.write(df.head())

    cols = st.columns(3)
    with cols[0]:
        resolution = st.slider(
            "H3 resolution",
            min_value=2,
            max_value=9,
            value=resolution,
        )

    with cols[1]:
        map_style = st.selectbox(
            "Map style",
            [
                "dark",
                "light",
                "dark_no_labels",
                "light_no_labels",
                "road",
            ],
        )

    with cols[2]:
        style_option = st.selectbox("Style schema", ("Contrast", "Snowflake"))

    # H3インデックスを作成
    df["hex"] = df.apply(
        lambda row: h3.latlng_to_cell(row["lat"], row["lon"], resolution), axis=1
    )

    # pydeck用データの作成
    if calc == "count":
        deck_data = df.groupby("hex").size().astype(int).reset_index(name="count")  # type: ignore
        deck_data["max"] = int(deck_data["count"].max())

    if calc == "mean":
        deck_data = (
            df.groupby("hex")[target].mean().astype(int).reset_index(name="count")
        )
        deck_data["max"] = int(deck_data["count"].max())

    if style_option == "Contrast":
        quantiles = get_quantiles(deck_data["count"], [0, 0.25, 0.5, 0.75, 1])
        colors = ["gray", "blue", "green", "yellow", "orange", "red"]
    if style_option == "Snowflake":
        quantiles = get_quantiles(deck_data["count"], [0, 0.33, 0.66, 1])
        colors = ["#666666", "#24BFF2", "#126481", "#D966FF"]

    deck_data["color"] = get_color(
        deck_data["count"], colors, quantiles.min(), quantiles.max(), quantiles
    )

    # st.write(deck_data.head())

    layer = get_layer(deck_data)

    # Set the viewport location
    view_state = pdk.ViewState(
        latitude=df["lat"].mean(),
        longitude=df["lon"].mean(),
        zoom=zoom,
        bearing=0,
        pitch=pitch,
    )

    # Set view deck
    deck = pdk.Deck(
        map_style=map_style,
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Count: {count}"},  # type: ignore
    )

    # Render the map in Streamlit
    st.pydeck_chart(deck, use_container_width=True, height=800)
