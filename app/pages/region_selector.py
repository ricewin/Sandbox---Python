from typing import Any

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


# Streamlit アプリのタイトル
st.title("Region to Prefecture and City Selector")

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
selected_region: Any | None = st.radio(
    "地域を選択してください", regions, horizontal=True
)

# 選択された regionname に基づいて prefname を取得
prefectures = df[df["regionname"] == selected_region]["prefname"].tolist()

# ██████╗ ██████╗ ███████╗███████╗███████╗ ██████╗████████╗██╗   ██╗██████╗ ███████╗███████╗
# ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗██╔════╝██╔════╝
# ██████╔╝██████╔╝█████╗  █████╗  █████╗  ██║        ██║   ██║   ██║██████╔╝█████╗  ███████╗
# ██╔═══╝ ██╔══██╗██╔══╝  ██╔══╝  ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗██╔══╝  ╚════██║
# ██║     ██║  ██║███████╗██║     ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║███████╗███████║
# ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝

# CSV ファイルを読み込む
df = _load_city()

# prefname を選択するセレクトボックス
selected_prefecture = st.radio(
    "都道府県を選択してください",
    prefectures,
    horizontal=True
)

# 選択された prefname に基づいて cityname を取得
cities = df[df["prefname"] == selected_prefecture]["cityname"].tolist()

#  ██████╗██╗████████╗██╗███████╗███████╗
# ██╔════╝██║╚══██╔══╝██║██╔════╝██╔════╝
# ██║     ██║   ██║   ██║█████╗  ███████╗
# ██║     ██║   ██║   ██║██╔══╝  ╚════██║
# ╚██████╗██║   ██║   ██║███████╗███████║
#  ╚═════╝╚═╝   ╚═╝   ╚═╝╚══════╝╚══════╝

selected_cities = st.multiselect("市区町村を選択してください", cities)

st.write("選択された市区町村:")
st.write(f"{city}　" for city in selected_cities)

st.write("---")

#  ██████╗ ██╗   ██╗███████╗██████╗ ██╗   ██╗
# ██╔═══██╗██║   ██║██╔════╝██╔══██╗╚██╗ ██╔╝
# ██║   ██║██║   ██║█████╗  ██████╔╝ ╚████╔╝
# ██║▄▄ ██║██║   ██║██╔══╝  ██╔══██╗  ╚██╔╝
# ╚██████╔╝╚██████╔╝███████╗██║  ██║   ██║
#  ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝

# TODO: 続きを書く

st.write("---")

st.info(
    """
    本コンテンツの一部は「**G空間情報センター**」より利用しています。

        regioncode_master: 地方区分コードのマスタファイル
        prefcode_citycode_master: 都道府県コード、市区町村コードのマスタファイル

    マスタファイルは以下のリンクより取得してください。
    """
)

# st.markdown(
#     """
#     [「全国の人流オープンデータ」（国土交通省）](
#     https://www.geospatial.jp/ckan/dataset/mlit-1km-fromto) を加工して作成
#     """
# )

st.markdown(
    """
    出典：[「全国の人流オープンデータ」（国土交通省）](https://www.geospatial.jp/ckan/dataset/mlit-1km-fromto)
    """
)
