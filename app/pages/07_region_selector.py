import streamlit as st
from lib.region_builder import region_builder

# Streamlit アプリのタイトル
st.title("Region to Prefecture and City Selector")

prefecture, cities = region_builder()


if cities is None:
    st.success(f"都道府県:{prefecture}")

if cities is not None:
    st.write("選択された市区町村:")
    st.write(f"{city}　" for city in cities)

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
