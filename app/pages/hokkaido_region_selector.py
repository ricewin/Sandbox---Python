import pandas as pd
import streamlit as st


@st.cache_data
def _load_region() -> pd.DataFrame:
    # CSV ファイルを読み込む
    return pd.read_csv("./static/hokkaido_regionname_master.csv")


# Streamlit アプリのタイトル
st.title("City to Region of Hokkaido")

# ██████╗ ███████╗ ██████╗ ██╗ ██████╗ ███╗   ██╗
# ██╔══██╗██╔════╝██╔════╝ ██║██╔═══██╗████╗  ██║
# ██████╔╝█████╗  ██║  ███╗██║██║   ██║██╔██╗ ██║
# ██╔══██╗██╔══╝  ██║   ██║██║██║   ██║██║╚██╗██║
# ██║  ██║███████╗╚██████╔╝██║╚██████╔╝██║ ╚████║
# ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

# CSV ファイルを読み込む
df: pd.DataFrame = _load_region()

# regionname のユニークな値を取得
hokkaido_regions = df["regionname"].unique()

# regionname を選択するラジオボタン
selected_hokkaido_region = st.radio(
    "北海道の地域を選択してください",
    hokkaido_regions,
    horizontal=True,
)

# 選択された regionname に基づいて cityname を取得
cities = df[df["regionname"] == selected_hokkaido_region]["cityname"].tolist()

with st.expander("選択された地域の市区町村を表示", expanded=True):
    st.write(f"選択された地域: {selected_hokkaido_region}")
    st.write("該当する市区町村:")
    st.write(f"{city}　" for city in cities)

#  ██████╗██╗████████╗██╗███████╗███████╗
# ██╔════╝██║╚══██╔══╝██║██╔════╝██╔════╝
# ██║     ██║   ██║   ██║█████╗  ███████╗
# ██║     ██║   ██║   ██║██╔══╝  ╚════██║
# ╚██████╗██║   ██║   ██║███████╗███████║
#  ╚═════╝╚═╝   ╚═╝   ╚═╝╚══════╝╚══════╝

# cities を選択するマルチボックス
selected_cities = st.multiselect("市区町村を選択してください", cities)

with st.expander("選択された都道府県の市区町村を表示", expanded=True):
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
