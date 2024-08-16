# -*- coding: utf-8 -*-
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming un indented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

"""

from typing import Any

import folium
import pandas as pd
import streamlit as st
from folium.plugins import HeatMap, MarkerCluster, MiniMap
from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit_folium import st_folium


@st.cache_data
def get_data(csv_file: UploadedFile) -> pd.DataFrame:
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


def add_marker(
    location: list[float], color: str, tooltip: str, mymap: MarkerCluster
) -> None:
    """Add markers by grouping

    Args:
        location (list[float]): Geocode
        color (str): Pin color
        tooltip (str): Tip
        mymap (MakerCluster): Pin map
    """
    folium.Marker(
        location=location,
        icon=folium.Icon(icon="home", icon_color="white", color=color),
        tooltip=tooltip,
    ).add_to(mymap)


st.set_page_config(layout="wide")

st.title(":satellite: Mapping")
st.subheader(
    ":mount_fuji: Traffic accidents",
    divider="rainbow",
)

upload_file: UploadedFile | None = st.file_uploader("Choose a file")

if upload_file is not None:
    data: pd.DataFrame = get_data(upload_file)

    if "lat" in data.columns and "lon" in data.columns:
        st.info("実行ボタンをクリックするとマップを表示します。")
    else:
        with st.expander("データフレームの編集"):
            st.info(
                "緯度・経度のあるカラム名を「緯度」「経度」に書き換えて実行すると、マップ表示ができます。"
            )
            st.dataframe(data)

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
        "ヒートマップ", value=True, help="オフにしても描画処理は変わりません。"
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

if upload_file is None:
    st.info("ファイルの読み込み後に地図を作成できます。")
    st.stop()

if st.button(":mag_right: 実行", type="primary"):
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
    m = folium.Map(
        location=map_center,
        tiles=map_tile,
        attr="""<a href="https://maps.gsi.go.jp/development/ichiran.html">地理院タイル</a>""",
        zoom_start=8,
    )

    if pin_map:
        with st.spinner("Cluster Making..."):
            try:
                # ピンをグループ化するマーカーグループクラスタを作成
                lightblue = MarkerCluster(name="負傷のみ")
                pink = MarkerCluster(name="単体死亡")
                red = MarkerCluster(name="複数死亡")

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
                        add_marker(
                            [row["緯度"], row["経度"]], "lightblue", tip, lightblue
                        )
                    elif count == 1:
                        add_marker([row["緯度"], row["経度"]], "pink", tip, pink)
                    else:
                        add_marker([row["緯度"], row["経度"]], "red", tip, red)

                lightblue.add_to(m)
                pink.add_to(m)
                red.add_to(m)

            except KeyError:
                st.info("ヒートマップのみ表示します。")

    if heat_map:
        heatmap_group = folium.FeatureGroup(name="ヒートマップ")
        coordinates: Any = df[["緯度", "経度"]].values.tolist()
        HeatMap(coordinates).add_to(heatmap_group)
        heatmap_group.add_to(m)

    folium.plugins.Geocoder(position="topleft", collapsed=True).add_to(m)  # type: ignore

    folium.plugins.Fullscreen(  # type: ignore
        position="topleft",
        title="Expand me",
        title_cancel="Exit me",
        force_separate_button=True,
    ).add_to(m)

    folium.LayerControl().add_to(m)

    MiniMap(toggle_display=True).add_to(m)

    with st.spinner("Map Making..."):
        st_folium(m, use_container_width=True, returned_objects=[])

    st.info(
        """
        ```
        地理院タイルにデータを追記して作成
        出典: 国土地理院 https://maps.gsi.go.jp/development/ichiran.html
        ```
        """
    )
