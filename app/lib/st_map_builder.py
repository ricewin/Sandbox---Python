import json
from typing import Any

import numpy as np
import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator


def _color_name() -> Any:
    """
    <named-color> を読み込む

    Returns:
        data: json
    """
    file_path = "./static/named_color.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def _create_team_row(
    team_name: str, default_color: str, default_opacity: int, default_size: int
) -> tuple[str, int, int]:
    """
    st.map の設定アイテム

    Args:
        team_name (str): チーム名
        default_color (str): 既定色
        default_opacity (int): 透明度
        default_size (int): サイズ

    Returns:
        tuple[str, int, int]: カラー、透明度、サイズ
    """
    row: list[DeltaGenerator] = st.columns([1, 2, 2])
    return (
        row[0].color_picker(team_name, default_color),
        row[1].slider("Opacity", 20, 100, default_opacity, label_visibility="hidden"),
        row[2].slider(
            "Size",
            50,
            200,
            default_size,
            step=10,
            label_visibility="hidden",
        ),
    )


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

        color_nameA: Any | None = st.selectbox(
            "Team A",
            colors.keys(),
            index=116,
        )
        color_codeA = colors[color_nameA]

        color_nameB: Any | None = st.selectbox(
            "Team B",
            colors.keys(),
            index=87,
        )
        color_codeB = colors[color_nameB]

        color_nameC: Any | None = st.selectbox(
            "Team C",
            colors.keys(),
            index=86,
        )
        color_codeC = colors[color_nameC]

    with col2:
        with st.form("map_form"):
            header: list[DeltaGenerator] = st.columns([1, 2, 2])
            header[0].subheader("Color")
            header[1].subheader("Opacity")
            header[2].subheader("Size")

            colorA, opacityA, sizeA = _create_team_row("Team A", color_codeA, 35, 100)
            colorB, opacityB, sizeB = _create_team_row("Team B", color_codeB, 50, 150)
            colorC, opacityC, sizeC = _create_team_row("Team C", color_codeC, 60, 200)

            header = st.columns([2, 3])
            header[0].subheader("Separate")

            row4: list[DeltaGenerator] = st.columns([2, 3])
            target: str | None = row4[0].selectbox(
                "Divide into teams",
                [col for col in df.columns if "数" in col],
                # 値の型で判断するなら
                # [col for col in df.columns if df[col].dtype == "int64"],
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
