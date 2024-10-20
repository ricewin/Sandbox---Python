import pandas as pd
import streamlit as st
from lib.folium_map_builder import folium_map_builder
from streamlit.runtime.uploaded_file_manager import UploadedFile
from lib.h3_map import h3_layer_map

st.set_page_config(
    page_title="Traffic accident",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "has_st_map" not in st.session_state:
    st.session_state["has_st_map"] = False


def _get_data(csv_file: UploadedFile) -> pd.DataFrame:
    """Read CSV file

    Args:
        csv_file (UploadedFile): Up file

    Returns:
        pd.DataFrame: DataFrame
    """
    try:
        return pd.read_csv(csv_file)
    except UnicodeDecodeError:
        st.error("ファイルのエンコードは Utf-8 のみ有効です。")
        st.stop()


with st.expander("README"):
    st.info(
        """
        1. ファイルを読み込む
        1. 「データフレームの編集」を開いて、緯度・経度のあるカラム名を「lat」「lon」に変更する
        1. 「Generate new points」ボタンをクリック
        1. 「Update map」ボタンをクリック
        1. Separate ヘッダーのパラメーターを変更する（項目の値が 数値になっているカラムを選ぶ）
        1. 「Update map」ボタンをクリック
        """
    )

upload_file: UploadedFile | None = st.file_uploader("Choose a file")

if upload_file is not None:
    df: pd.DataFrame = _get_data(upload_file)

    if not ("lat" in df.columns and "lon" in df.columns):
        # カラム名を変更
        df.rename(
            columns={"地点　緯度（北緯）": "lat", "地点　経度（東経）": "lon"},
            inplace=True,
        )
        with st.expander("データフレームの編集"):
            st.info(
                "緯度・経度のあるカラム名を「lat」「lon」に書き換えると、表示できます。"
            )
            st.dataframe(df)

            # カラム名の編集フィールド
            df.columns = [
                st.text_input(f"{col} の新しい名前", value=col) for col in df.columns
            ]

if st.button("Generate new points", type="primary"):
    st.session_state.df = df

if "df" not in st.session_state:
    st.stop()

if not ("lat" in st.session_state.df.columns and "lon" in st.session_state.df.columns):
    st.error("カラム名に「lat」「lon」が存在しません。")
    st.info("「データフレームの編集」を開いてカラム名を変更してください。")
    st.stop()

df = st.session_state.df

st.session_state["has_st_map"] = st.toggle(
    "folium.map ⇔ st.map", value=st.session_state["has_st_map"]
)

if st.session_state["has_st_map"]:
    h3_layer_map(df, "負傷者数")
else:
    folium_map_builder(df)
