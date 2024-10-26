import h3
import streamlit as st

# Streamlitアプリの設定
st.title("緯度と経度からH3インデックスを生成")
st.write("緯度と経度を入力してください。")


@st.fragment
def user_input():
    # ユーザー入力を取得
    lat = st.number_input("緯度", value=35.6895)
    lon = st.number_input("経度", value=139.6917)
    resolution = st.slider("H3解像度", 0, 15, value=9)

    # H3インデックス(16進数形式)を生成
    h3_index = h3.latlng_to_cell(lat, lon, resolution)

    # int関数を使ってstr → int変換
    h3_index_int = int(h3_index, 16)

    # hex関数を使ってint → str変換
    hex_num = hex(h3_index_int)

    # 結果を表示
    with st.container(border=True):
        st.write("H3インデックス (str): ", h3_index)
        st.write("H3インデックス (int): ", h3_index_int)
        st.write("H3解像度: ", h3.get_resolution(h3_index))
        st.write("再変換: ", hex_num[2:])

    st.divider()

    st.write("H3関数を使った変換")

    # H3関数でstr → int変換
    h = h3.str_to_int(h3_index)
    st.write(h)

    # H3関数でint → str変換
    h = h3.int_to_str(h)
    st.write(h)


user_input()
