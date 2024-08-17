import numpy as np
import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.uploaded_file_manager import UploadedFile

st.set_page_config(
    page_title="st.map",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def _get_data(csv_file: UploadedFile) -> pd.DataFrame:
    """Read CSV file

    Args:
        csv_file (UploadedFile): Up file

    Returns:
        pd.DataFrame: DataFrame
    """
    try:
        df: pd.DataFrame = pd.read_csv(csv_file)

    except UnicodeDecodeError:
        st.error("ファイルのエンコードは Utf-8 のみ有効です。")
        st.stop()

    return df


upload_file: UploadedFile | None = st.file_uploader("Choose a file")

if upload_file is None:
    st.stop()

if upload_file is not None:
    df: pd.DataFrame = _get_data(upload_file)

    if not ("lat" in df.columns and "lon" in df.columns):
        with st.expander("データフレームの編集"):
            st.info(
                "緯度・経度のあるカラム名を「lat」「lon」に書き換えて実行すると、マップ表示ができます。"
            )
            st.dataframe(df)

            # カラム名の編集フィールド
            df.columns = [
                st.text_input(f"{col} の新しい名前", value=col) for col in df.columns
            ]


if st.button("Generate new points"):
    st.session_state.df = df

if "df" not in st.session_state:
    st.session_state.df = df

df = st.session_state.df

with st.form("my_form"):
    header: list[DeltaGenerator] = st.columns([1, 2, 2])
    header[0].subheader("Color")
    header[1].subheader("Opacity")
    header[2].subheader("Size")

    row1: list[DeltaGenerator] = st.columns([1, 2, 2])
    colorA = row1[0].color_picker("Team A", "#fff0f5")
    opacityA = row1[1].slider("A opacity", 20, 100, 50, label_visibility="hidden")
    sizeA = row1[2].slider("A size", 50, 200, 100, step=10, label_visibility="hidden")

    row2: list[DeltaGenerator] = st.columns([1, 2, 2])
    colorB = row2[0].color_picker("Team B", "#66cdaa")
    opacityB = row2[1].slider("B opacity", 20, 100, 55, label_visibility="hidden")
    sizeB = row2[2].slider("B size", 50, 200, 150, step=10, label_visibility="hidden")

    row3: list[DeltaGenerator] = st.columns([1, 2, 2])
    colorC = row3[0].color_picker("Team C", "#800000")
    opacityC = row3[1].slider("C opacity", 20, 100, 60, label_visibility="hidden")
    sizeC = row3[2].slider("C size", 50, 200, 200, step=10, label_visibility="hidden")

    header: list[DeltaGenerator] = st.columns([2, 3])
    header[0].subheader("Separate")

    row4: list[DeltaGenerator] = st.columns([2, 3])
    target = row4[0].selectbox(
        "Divide into teams",
        df.columns.to_list(),
        help="数値でチームを分けます。A: 0, B: 1, C: more",
    )

    st.form_submit_button("Update map")

alphaA = int(opacityA * 255 / 100)
alphaB = int(opacityB * 255 / 100)
alphaC = int(opacityC * 255 / 100)

df["color"] = np.where(
    df[target] == 0,
    colorA + f"{alphaA:02x}",
    np.where(df[target] == 1, colorB + f"{alphaB:02x}", colorC + f"{alphaC:02x}"),
)

df["size"] = np.where(df[target] == 0, sizeA, np.where(df[target] == 1, sizeB, sizeC))

# st.dataframe(df)

try:
    st.map(df, size="size", color="color", use_container_width=True)
except Exception:
    st.stop()
