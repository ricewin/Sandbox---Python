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

    @st.cache_resource(ttl="2d")
    def get_quantiles(df_column: pd.Series, quantiles: List) -> pd.Series:
        return df_column.quantile(quantiles)

    @st.cache_resource(ttl="2d")
    def get_color(
        df_column: pd.Series, colors: List, vmin: int, vmax: int, index: pd.Series
    ) -> pd.Series:
        color_map = cm.LinearColormap(colors, vmin=vmin, vmax=vmax, index=index)
        return df_column.apply(color_map.rgb_bytes_tuple)

    @st.cache_resource(ttl="2d")
    def get_layer(df: pd.DataFrame) -> pdk.Layer:
        return pdk.Layer(
            "H3HexagonLayer",
            df,
            get_hexagon="H3",
            get_fill_color="COLOR",
            get_line_color="COLOR",
            get_elevation="COUNT",
            auto_highlight=True,
            elevation_scale=50,
            pickable=True,
            elevation_range=[0, 3000],
            extruded=False,
            coverage=1,
            opacity=0.5,
        )

    # H3インデックスを作成
    df["HEX"] = df.apply(
        lambda row: h3.latlng_to_cell(row["lat"], row["lon"], resolution), axis=1
    )

    # pydeck用データの作成
    if calc == "count":
        df = df.groupby("HEX").size().astype(int).reset_index(name="COUNT")  # type: ignore
        df["COUNT"] = int(df["COUNT"].max())

    if calc == "mean":
        df = (
            df.groupby("HEX")[target].mean().astype(int).reset_index(name="COUNT")
        )
        df["COUNT"] = int(df["COUNT"].max())

    col1, col2 = st.columns(2)

    with col1:
        pass
        # h3_resolution = st.slider("H3 resolution", min_value=2, max_value=7, value=2)

    with col2:
        style_option = st.selectbox("Style schema", ("Contrast", "Snowflake"), index=0)

    # df = get_df(h3_resolution)

    if style_option == "Contrast":
        quantiles = get_quantiles(df["COUNT"], [0, 0.25, 0.5, 0.75, 1])
        colors = ["gray", "blue", "green", "yellow", "orange", "red"]
    if style_option == "Snowflake":
        quantiles = get_quantiles(df["COUNT"], [0, 0.33, 0.66, 1])
        colors = ["#666666", "#24BFF2", "#126481", "#D966FF"]


    df["COLOR"] = get_color(
        df["COUNT"], colors, quantiles.min(), quantiles.max(), quantiles
    )
    layer = get_layer(df)

    st.write(df)
    st.pydeck_chart(
        pdk.Deck(
            map_style="light",
            initial_view_state=pdk.ViewState(
                latitude=136, longitude=35, zoom=6
            ),
            tooltip={
                "html": "<b>Cell towers:</b> {COUNT}",
                "style": {"color": "white"},
            },  # type: ignore
            layers=[layer],
        )
    )
