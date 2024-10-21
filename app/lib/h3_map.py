"""
H3HexagonLayer
==============

Plot of values for a particular hex ID in the H3 geohashing scheme.

This example is adapted from the deck.gl documentation.
"""

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
    cols = st.columns([1, 1])
    with cols[0]:
        resolution = st.slider(
            "H3 resolution",
            min_value=1,
            max_value=10,
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

    if "dark" in map_style:
        line_color = [255, 250, 205]  # lemonchiffon
    else:
        line_color = [127, 255, 212]  # aquamarine

    # H3インデックスを作成
    df["hex"] = df.apply(
        lambda row: h3.latlng_to_cell(row["lat"], row["lon"], resolution), axis=1
    )

    # st.write(df)

    # pydeck用データの作成
    if calc == "count":
        deck_data = df.groupby("hex").size().astype(int).reset_index(name="count")  # type: ignore
        deck_data["max"] = int(deck_data["count"].max())

    if calc == "mean":
        deck_data = (
            df.groupby("hex")[target].mean().astype(int).reset_index(name="count")
        )
        deck_data["max"] = int(deck_data["count"].max())

    # st.dataframe(deck_data)

    layer = pdk.Layer(
        "H3HexagonLayer",
        deck_data,
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        get_hexagon="hex",
        # get_hexagons="hex",
        # 赤から青のグラデーション
        # get_fill_color="[255 - (count / max) * 255, 0, (count / max) * 255, 128]",
        # 青から赤のグラデーション
        get_fill_color="[(count / max) * 255, 0, 255 - (count / max) * 255, 144]",
        get_line_color=line_color,
        line_width_min_pixels=1,
    )

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
