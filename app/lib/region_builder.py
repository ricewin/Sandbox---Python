"""Region Builder

Use:
    Prefecture, cities = region_builder()
"""

from typing import Any, Literal

import pandas as pd
import streamlit as st


@st.cache_data
def _load_region() -> pd.DataFrame:
    # CSV ファイルを読み込む
    return pd.read_csv("./static/regioncode_master_utf8_2020.csv")


@st.cache_data
def _load_city() -> pd.DataFrame:
    # CSV ファイルを読み込む
    return pd.read_csv("./static/prefcode_citycode_master_utf8_2020.csv")


def region_builder(
    is_pref: bool = False,
    is_disabled: bool = False,
) -> (
    tuple[Literal["北海道"], None]
    | tuple[Any | None, None]
    | tuple[Any | None, list[Any]]
):
    """
        リージョンを選択して返す


    Args:
        is_pref: bool: Switch region. Defaults to False,
        is_disabled: bool: Disabled toggle. Defaults to False,

    Returns:
        str, list[str]: 都道府県、市区町村

    """
    until_prefecture = st.toggle(
        "都道府県まで",
        value=is_pref,
        disabled=is_disabled,
    )

    # ██████╗ ███████╗ ██████╗ ██╗ ██████╗ ███╗   ██╗
    # ██╔══██╗██╔════╝██╔════╝ ██║██╔═══██╗████╗  ██║
    # ██████╔╝█████╗  ██║  ███╗██║██║   ██║██╔██╗ ██║
    # ██╔══██╗██╔══╝  ██║   ██║██║██║   ██║██║╚██╗██║
    # ██║  ██║███████╗╚██████╔╝██║╚██████╔╝██║ ╚████║
    # ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

    df = _load_region()

    # regionname のユニークな値を取得
    regions = df["regionname"].unique()

    # regionname を選択するラジオボタン
    selected_region: str | None = st.radio(
        "地域を選択してください", regions, horizontal=True
    )

    if until_prefecture:
        if selected_region == "北海道":
            return selected_region, None

    # 選択された regionname に基づいて prefname を取得
    prefectures = df[df["regionname"] == selected_region]["prefname"].tolist()

    # ██████╗ ██████╗ ███████╗███████╗███████╗ ██████╗████████╗██╗   ██╗██████╗ ███████╗███████╗
    # ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗██╔════╝██╔════╝
    # ██████╔╝██████╔╝█████╗  █████╗  █████╗  ██║        ██║   ██║   ██║██████╔╝█████╗  ███████╗
    # ██╔═══╝ ██╔══██╗██╔══╝  ██╔══╝  ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗██╔══╝  ╚════██║
    # ██║     ██║  ██║███████╗██║     ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║███████╗███████║
    # ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝

    # CSV ファイルを読み込む
    df: pd.DataFrame = _load_city()

    # prefname を選択するセレクトボックス
    selected_prefecture = st.radio(
        "都道府県を選択してください", prefectures, horizontal=True
    )

    if until_prefecture:
        return selected_prefecture, None

    # 選択された prefname に基づいて cityname を取得
    cities = df[df["prefname"] == selected_prefecture]["cityname"].tolist()

    #  ██████╗██╗████████╗██╗███████╗███████╗
    # ██╔════╝██║╚══██╔══╝██║██╔════╝██╔════╝
    # ██║     ██║   ██║   ██║█████╗  ███████╗
    # ██║     ██║   ██║   ██║██╔══╝  ╚════██║
    # ╚██████╗██║   ██║   ██║███████╗███████║
    #  ╚═════╝╚═╝   ╚═╝   ╚═╝╚══════╝╚══════╝

    return selected_prefecture, st.multiselect("市区町村を選択してください", cities)
