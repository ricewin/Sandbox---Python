# import folium
import pandas as pd
import streamlit as st
from lib.h3_map import h3_layer_map
from streamlit.runtime.uploaded_file_manager import UploadedFile

st.set_page_config(
    page_title="Meteorite Landings",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="auto",
)

ss_key = "meteorite"


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


def _rename_columns(df):
    try:
        # カラム名を変更
        df = df.rename(
            columns={"reclat": "lat", "reclong": "lon", "mass (g)": "mass"},
        )
    except ValueError:
        st.info(
            "緯度・経度のあるカラム名を「lat」「lon」に書き換えると、表示できます。"
        )
    finally:
        if not ("lat" in df.columns and "lon" in df.columns):
            with st.expander("データフレームの編集"):
                # カラム名の編集フィールド
                df.columns = [
                    st.text_input(f"{col} の新しい名前", value=col)
                    for col in df.columns
                ]

        return df


upload_file: UploadedFile | None = st.file_uploader("Choose a file")

if upload_file is not None:
    df: pd.DataFrame = _get_data(upload_file)

    if not ("lat" in df.columns and "lon" in df.columns):
        df = _rename_columns(df)

btns = st.columns([1, 1, 2])
with btns[0]:
    if st.button("Generate", type="primary"):
        if upload_file is not None:
            try:
                st.session_state[ss_key] = df
            except NameError:
                st.stop()

with btns[1]:
    if st.button("Delete", type="primary"):
        if ss_key in st.session_state.keys():
            del st.session_state[ss_key]


if ss_key not in st.session_state:
    st.stop()

with st.expander("Original"):
    st.dataframe(st.session_state[ss_key])

if not (
    "lat" in st.session_state[ss_key].columns
    and "lon" in st.session_state[ss_key].columns
):
    st.error("カラム名に「lat」「lon」が存在しません。")
    st.info("「データフレームの編集」を開いてカラム名を変更してください。")
    st.stop()

df = st.session_state[ss_key]

# 位置情報のないレコードをドロップ
df = df.dropna(subset=["lat", "lon"])

item: str | None = st.selectbox(
    "Choose item",
    [
        col
        for col in df.columns
        if df[col].dtype == "int64" or df[col].dtype == "float64"
    ],
    help="アイテムを選んでください",
)

# NaNを0で埋める
df[item].fillna(0, inplace=True)

plot = st.selectbox("Plot", ["Count", "Mean"])

if plot == "Count":
    h3_layer_map(df, item, "count", zoom=1, resolution=2)

if plot == "Mean":
    h3_layer_map(df, item, "mean", zoom=1, resolution=2)
