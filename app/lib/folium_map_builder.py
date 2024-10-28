from typing import Any

import folium
import pandas as pd
import streamlit as st
from folium.plugins import HeatMap, MarkerCluster, MiniMap
from streamlit.delta_generator import DeltaGenerator
from streamlit_folium import st_folium


def _add_marker(
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


@st.fragment
def folium_map_builder(df: pd.DataFrame) -> None:
    """
    Map Component

    Args:
        df (pd.DataFrame): Map data
    """
    with st.form("my_form"):
        header: list[DeltaGenerator] = st.columns(4)
        header[0].subheader("Pin")
        header[1].subheader("Circle")
        header[2].subheader("Heat map")
        header[3].subheader("Style")

        row1: list[DeltaGenerator] = st.columns(4)
        pin_map: bool = row1[0].toggle(
            "ピン", help="ピンを表示すると処理が重くなります。"
        )

        circle_map: bool = row1[1].toggle("サークル", help="サークル。")

        heat_map: bool = row1[2].toggle(
            "ヒートマップ", value=True, help="オフにしても体感は変わりません。"
        )

        map_style: str | None = row1[3].radio(
            "地図のスタイル",
            options=["標準", "淡色"],
            index=1,
            horizontal=True,
            help="淡色がおすすめ。",
        )

        item: str | None = st.selectbox(
            "Choose item",
            [
                col
                for col in df.columns
                if df[col].dtype == "int64" or df[col].dtype == "float64"
            ],
            help="アイテムを選んでください",
        )

        st.form_submit_button("Update map")

    if map_style == "標準":
        map_tile = "https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png"
    else:
        map_tile = "https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png"

    try:
        # 位置情報のないレコードをドロップ
        df = df.dropna(subset=["lat", "lon"])

        # 地図の初期位置を設定
        map_center: list[float] = [df["lat"].mean(), df["lon"].mean()]

    except KeyError:
        st.error("地図表示できません。「lat」「lon」を指定しているか確認してください。")
        st.stop()

    except TypeError:
        st.error("地図表示できません。間違った列を指定しています。")
        st.stop()

    st.write(f"有効件数: {len(df)} / {len(df)}")

    # マップを作成
    m = folium.Map(
        location=map_center,
        tiles=map_tile,
        attr="""<a href="https://maps.gsi.go.jp/development/ichiran.html"target="_blank">地理院タイル</a>
            Shoreline data is derived from: United States.
            National Imagery and Mapping Agency.
            "Vector Map Level 0 (VMAP0)." Bethesda, MD: Denver, CO: The Agency;
            USGS Information Services, 1997.""",
        zoom_start=8,
    )

    if pin_map:
        with st.spinner("Cluster Making..."):
            try:
                # ピンをグループ化するマーカーグループクラスタを作成
                # lightblue = MarkerCluster(name="負傷のみ")
                # pink = MarkerCluster(name="単体死亡")
                # red = MarkerCluster(name="複数死亡")
                red = MarkerCluster(name=item)

                for index, row in df.iterrows():
                    count: Any = row[item]

                    tip: str = f"""
                        Count: {count}
                    """

                    # if count == 0:
                    #     _add_marker(
                    #         [row["lat"], row["lon"]], "lightblue", tip, lightblue
                    #     )
                    # elif count == 1:
                    #     _add_marker([row["lat"], row["lon"]], "pink", tip, pink)
                    # else:
                    _add_marker([row["lat"], row["lon"]], "red", tip, red)

                # lightblue.add_to(m)
                # pink.add_to(m)
                red.add_to(m)

            except KeyError:
                st.info("ヒートマップのみ表示します。")

    if circle_map:
        with st.spinner("Circle Making..."):
            # Define a function to determine the color based on the target value
            def get_color(value):
                if value == 0:
                    return "red"

                if value == 1:
                    return "yellow"

                if value == 2:
                    return "green"

                return "blue"

            df["max"] = df[item].max()
            radius = 100

            circle = folium.FeatureGroup(name="サークル")
            # Assuming you have a DataFrame `df` with `lat`, `lon`, and `target` columns
            for _, row in df.iterrows():
                color = get_color(row[item])
                folium.Circle(
                    location=[row["lat"], row["lon"]],
                    radius=radius,
                    color=color,
                    weight=1,
                    fill_opacity=0.4,
                    opacity=1,
                    fill_color=color,
                    fill=True,  # Enable fill with the specified fill_color
                    popup="{} meters".format(radius),
                    tooltip=f"Count: {row[item]}",
                ).add_to(circle)

            circle.add_to(m)

    if heat_map:
        heatmap_group = folium.FeatureGroup(name="ヒートマップ")
        coordinates: Any = df[["lat", "lon", item]].values.tolist()
        HeatMap(coordinates).add_to(heatmap_group)
        heatmap_group.add_to(m)

    folium.plugins.Geocoder(position="topleft", collapsed=True).add_to(m)  # type: ignore

    folium.plugins.Fullscreen(  # type: ignore
        title="Expand me",
        title_cancel="Exit me",
    ).add_to(m)

    folium.LayerControl().add_to(m)
    MiniMap(toggle_display=True).add_to(m)

    with st.spinner("Map Making..."):
        st_folium(m, use_container_width=True, returned_objects=[])
