import h3
import streamlit as st

st.title("緯度と経度から H3 インデックスを生成してみる")


@st.fragment
def main() -> None:
    # 事前準備
    lat: float = st.number_input("緯度", value=35.6895)
    lon: float = st.number_input("経度", value=139.6917)
    resolution: int = st.slider("H3解像度", 0, 15, value=8)

    with st.echo():
        st.subheader("Example", divider="orange")

        # 準備: H3インデックス(16進数形式)[str] を生成する
        h3_index = h3.latlng_to_cell(lat, lon, resolution)

        # ここから比較

        # H3関数で str → int 変換する場合
        h3_int = h3.str_to_int(h3_index)

        # H3関数で int → str 変換する場合
        h3_str = h3.int_to_str(h3_int)

        # int関数を使って str → int 変換する場合
        num_int: int = int(h3_index, 16)

        # hex関数を使って int → str 変換する場合
        num_hex: str = hex(num_int)

        # 結果を表示
        with st.container(border=True):
            st.write(
                "H3 インデックス (str):",
                h3_index,
            )

            st.write(
                "str から int の変換で比較:",
                h3_int,
                num_int,
                h3_int == num_int,
            )

            st.write(
                "int から str の変換で比較:",
                h3_str,
                num_hex,
                h3_str == num_hex,
            )

            st.info("hex関数で変換した場合は、プレフィックスを取り除くと一致する")

            st.write(
                h3_str,
                num_hex[2:],
                h3_str == num_hex[2:],
            )


if __name__ == "__main__":
    main()
