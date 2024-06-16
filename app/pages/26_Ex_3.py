from io import StringIO
from typing import Any

import folium
import pandas as pd
import streamlit as st
from folium.plugins import HeatMap, MarkerCluster
from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.title(":satellite: マッピング")
st.subheader(
    ":mount_fuji: 緯度・経度が入った CSV ファイルからマップ表示するテスト",
    divider="rainbow",
)

upload_file: UploadedFile | None = st.file_uploader("Choose a file")

if upload_file is not None:
    bytes_data: bytes = upload_file.getvalue()
    stringio = StringIO(upload_file.getvalue().decode("utf-8"))
    string_data: str = stringio.read()
    data: pd.DataFrame = pd.read_csv(upload_file)

    if "緯度" in data.columns and "経度" in data.columns:
        st.info("実行ボタンをクリックするとマップを表示します。")
    else:
        with st.expander("データフレームの編集", expanded=True):
            st.info(
                "緯度・経度のあるカラム名を「緯度」「経度」に書き換えて実行すると、マップ表示ができます。"
            )
            st.write(data)

            # カラム名の編集フィールドを作成する
            new_columns: list[Any] = []
            for col in data.columns:
                new_col: str = st.text_input(f"{col} の新しい名前", value=col)
                new_columns.append(new_col)

            # 新しいカラム名を適用する
            data.columns = new_columns

    heatmap = st.toggle("HeatMap")

    if st.button(":mag_right: 実行"):
        try:
            # 位置情報のないレコードをドロップ
            df: pd.DataFrame = data.dropna(subset=["緯度", "経度"])

            # 地図の初期位置を設定
            map_center: list[float] = [df["緯度"].mean(), df["経度"].mean()]

        except KeyError:
            st.error(
                "地図表示できません。「緯度」「経度」を指定しているか確認してください。"
            )
            st.stop()

        except TypeError:
            st.error("地図表示できません。間違った列を指定しています。")
            st.stop()

        st.write(f"有効件数: {len(df)} / {len(data)}")

        # マップを作成
        map = folium.Map(
            location=map_center,
            tiles="https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png",
            attr="国土地理院",
            zoom_start=8,
        )

        # ピンをグループ化するマーカーグループクラスタを作成
        marker_cluster: MarkerCluster = MarkerCluster().add_to(map)

        # データフレームの各行に対して、ピンを作成してマップに追加
        for index, row in df.iterrows():
            pop = f"""{row["緯度"]} {row["経度"]}"""

            folium.Marker(
                location=[row["緯度"], row["経度"]],
                popup=pop,
                icon=folium.Icon(icon="home", icon_color="white", color="red"),
            ).add_to(marker_cluster)

        if heatmap:
            # ヒートマップ表示を追加
            coordinates: Any = df[["緯度", "経度"]].values.tolist()
            HeatMap(coordinates).add_to(map)

        st_folium(map, use_container_width=True, returned_objects=[])

        st.info(
            """
            ```
            地理院タイルにデータを追記して作成
            出典: 国土地理院 https://maps.gsi.go.jp/development/ichiran.html
            ```
            """
        )
