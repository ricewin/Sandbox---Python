import json

import numpy as np
import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator


def _color_name():
    file_path = "./static/named_color.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def st_map_builder(df: pd.DataFrame) -> None:
    """
    Map Component

    Args:
        df (pd.DataFrame): Map data
    """
    colors = _color_name()

    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("Choose a color name")

        color_nameA = st.selectbox(
            "Team A",
            colors.keys(),
            index=116,
        )
        color_codeA = colors[color_nameA]

        color_nameB = st.selectbox(
            "Team B",
            colors.keys(),
            index=87,
        )
        color_codeB = colors[color_nameB]

        color_nameC = st.selectbox(
            "Team C",
            colors.keys(),
            index=86,
        )
        color_codeC = colors[color_nameC]

    with col2:
        with st.form("my_form"):
            header: list[DeltaGenerator] = st.columns([1, 2, 2])
            header[0].subheader("Color")
            header[1].subheader("Opacity")
            header[2].subheader("Size")

            row1: list[DeltaGenerator] = st.columns([1, 2, 2])
            colorA = row1[0].color_picker("Team A", color_codeA)
            opacityA = row1[1].slider(
                "A opacity", 20, 100, 35, label_visibility="hidden"
            )
            sizeA = row1[2].slider(
                "A size", 50, 200, 100, step=10, label_visibility="hidden"
            )

            row2: list[DeltaGenerator] = st.columns([1, 2, 2])
            colorB = row2[0].color_picker("Team B", color_codeB)
            opacityB = row2[1].slider(
                "B opacity", 20, 100, 50, label_visibility="hidden"
            )
            sizeB = row2[2].slider(
                "B size", 50, 200, 150, step=10, label_visibility="hidden"
            )

            row3: list[DeltaGenerator] = st.columns([1, 2, 2])
            colorC = row3[0].color_picker("Team C", color_codeC)
            opacityC = row3[1].slider(
                "C opacity", 20, 100, 60, label_visibility="hidden"
            )
            sizeC = row3[2].slider(
                "C size", 50, 200, 200, step=10, label_visibility="hidden"
            )

            header: list[DeltaGenerator] = st.columns([2, 3])
            header[0].subheader("Separate")

            row4: list[DeltaGenerator] = st.columns([2, 3])
            target = row4[0].selectbox(
                "Divide into teams",
                df.columns.to_list(),
                help="数値でチームを分けます。A: 0, B: 1, C: more",
            )

            st.form_submit_button("Update map", type="primary")

    alphaA = int(opacityA * 255 / 100)
    alphaB = int(opacityB * 255 / 100)
    alphaC = int(opacityC * 255 / 100)

    df["color"] = np.where(
        df[target] == 0,
        colorA + f"{alphaA:02x}",
        np.where(df[target] == 1, colorB + f"{alphaB:02x}", colorC + f"{alphaC:02x}"),
    )

    df["size"] = np.where(
        df[target] == 0, sizeA, np.where(df[target] == 1, sizeB, sizeC)
    )

    # st.dataframe(df)

    try:
        st.map(df, size="size", color="color", use_container_width=True)
    except Exception:
        st.stop()
