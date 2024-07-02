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
    ":mount_fuji: 交通事故のマッピング",
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

            # カラム名の編集フィールド
            data.columns = [
                st.text_input(f"{col} の新しい名前", value=col) for col in data.columns
            ]

col1, col2, col3 = st.columns(3)
with col1:
    pin_map: bool = st.toggle(
        "ピン", value=True, help="オフにすると描画処理が高速化されます。"
    )

with col2:
    heat_map: bool = st.toggle(
        "HeatMap", value=True, help="オフにしても描画処理はあまり変わらないと思います。"
    )

with col3:
    map_style: str | None = st.radio(
        "地図のスタイル",
        options=["標準", "淡色"],
        index=1,
        horizontal=True,
        help="淡色がおすすめ",
    )

if map_style == "標準":
    map_tile = "https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png"
else:
    map_tile = "https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png"

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
        tiles=map_tile,
        attr="""<a href="https://maps.gsi.go.jp/development/ichiran.html">地理院タイル</a>""",
        zoom_start=8,
    )

    if pin_map:
        # ピンをグループ化するマーカーグループクラスタを作成
        lightblue = MarkerCluster(name="負傷のみ").add_to(map)
        pink = MarkerCluster(name="単体死亡").add_to(map)
        red = MarkerCluster(name="複数死亡").add_to(map)

        # データフレームの各行に対して、ピンを作成してマップに追加
        def add_marker(location, color, tooltip, mymap) -> None:
            folium.Marker(
                location=location,
                icon=folium.Icon(icon="home", icon_color="white", color=color),
                tooltip=tooltip,
            ).add_to(mymap)

        for index, row in df.iterrows():
            count: Any = row["死者数"]

            tip: str = f"""
                発生日時: {row["発生日時"]}<br />
                天候: {row["天候"]}<br />
                路面状態: {row["路面状態"]}<br />
                当事者A: {row["車両の損壊程度（当事者A）"]}<br />
                当事者B: {row["車両の損壊程度（当事者B）"]}<br />
                負傷者数: {row["負傷者数"]} 人,
                死者数: {count} 人
            """

            if count == 0:
                add_marker([row["緯度"], row["経度"]], "lightblue", tip, lightblue)
            elif count < 2:
                add_marker([row["緯度"], row["経度"]], "pink", tip, pink)
            else:
                add_marker([row["緯度"], row["経度"]], "red", tip, red)

        lightblue.add_to(map)
        pink.add_to(map)
        red.add_to(map)

    if heat_map:
        heatmap_group = folium.FeatureGroup(name="ヒートマップ")
        coordinates: Any = df[["緯度", "経度"]].values.tolist()
        HeatMap(coordinates).add_to(heatmap_group)
        heatmap_group.add_to(map)

    folium.LayerControl().add_to(map)
    st_folium(map, use_container_width=True, returned_objects=[])

    st.info(
        """
        ```
        地理院タイルにデータを追記して作成
        出典: 国土地理院 https://maps.gsi.go.jp/development/ichiran.html
        ```
        """
    )
