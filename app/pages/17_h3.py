import h3
import streamlit as st

st.title("H3 セル ID を生成してみる")


@st.fragment
def main() -> None:
    # 事前準備
    lat: float = st.number_input("緯度", value=35.6895)
    lon: float = st.number_input("経度", value=139.6917)
    resolution: int = st.slider("H3解像度", 0, 15, value=8)

    st.info("H3セルID 整数(int) ⇔ 16進数(str) の相互変換は、組み込み関数でも行えます。")

    st.header("Example", divider="orange")

    # 準備: H3セルID(16進数) を生成する
    hex_id = h3.latlng_to_cell(lat, lon, resolution)
    st.write(
        "H3 セル ID (str):",
        hex_id,
    )

    with st.echo():
        # ここから比較
        col1, col2 = st.columns(2)
        with col1:
            st.caption("H3 関数")

            # H3関数で str → int 変換する場合
            h3_int = h3.str_to_int(hex_id)
            st.write(h3_int)

            # H3関数で int → str 変換する場合
            h3_str = h3.int_to_str(h3_int)
            st.write(h3_str)

        with col2:
            st.caption("組み込み関数")

            # int関数を使って str → int 変換する場合
            built_int: int = int(hex_id, 16)
            st.write(built_int)

            # hex関数を使って int → str 変換する場合
            built_hex: str = hex(built_int)
            st.write(built_hex)

        # 結果を表示
        with st.container(border=True):

            st.write(
                "str から int の変換で比較:",
                h3_int == built_int,
            )

            st.write(
                "int から str の変換で比較:",
                h3_str == built_hex,
            )

            st.info("hex関数で変換したときは、プレフィックスを取り除くと一致する")

            st.write(
                "“0x” を削除して比較:",
                h3_str == built_hex[2:],
            )


if __name__ == "__main__":
    main()
