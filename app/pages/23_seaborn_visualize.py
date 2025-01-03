"""StreamlitでコードとUIをスッキリさせるためのノウハウをまとめてみた

https://nttdocomo-developers.jp/entry/20231216_1
"""

import seaborn as sns
import streamlit as st

ss = st.session_state

# 定数====================================
DATA = [
    "anagrams",
    "anscombe",
    "attention",
    "car_crashes",
    "diamonds",
    "dots",
    "dowjones",
    "exercise",
    "fmri",
    "geyser",
    "glue",
    "healthexp",
    "iris",
    "mpg",
    "penguins",
    "planets",
    "seaice",
    "taxis",
    "tips",
    "titanic",
]  # seabornのデータセット

# 状態変数==================================
if "now" not in ss:  # 初期化
    ss.now = 0
    ss.rst = False


def countup(reset):  # コールバック関数(1/3):次へ
    ss.now += 1
    ss.rst = reset


def countdown():  # コールバック関数(2/3):戻る
    ss.now -= 1


def reset():  # コールバック関数(3/3):リセット
    ss.now = 0


# UIパーツ=================================
def buttons(now, _reset=False):
    col = st.columns([1, 1, 2])
    if now <= 1:
        col[0].button("次へ進む", on_click=countup, args=(_reset,))
    if now >= 1:
        col[1].button("前へ戻る", on_click=countdown)
    if now >= 2:
        col[2].button("はじめからやり直す", on_click=reset)


# アプリ本体=================================
st.title("❻seabornデータ")
if ss.now == 0:
    st.write("### ステップ1: データの選択")
    st.info("Seabornに載っているデータセットです。可視化するものを選択してください。")
    if "idx0" not in ss:  # 初期化
        ss.idx0 = 0
    ss.ds = st.radio(
        "dataset", DATA, ss.idx0, horizontal=True, label_visibility="collapsed"
    )
    ss.idx0 = [i for i, e in enumerate(DATA) if e == ss.ds][0]  # 状態の記憶
    ss.df = sns.load_dataset(ss.ds)  # データセットを読み込む
    st.write("選択中のデータ：(行の数, 列の数) = ({}, {})".format(*ss.df.shape))
    buttons(ss.now, True)
elif ss.now == 1:
    st.write("### ステップ2: 列の選択")
    st.info(f"『`{ss.ds}`』データにおいて可視化したい列を選択してください。")
    if "flg1" not in ss or ss.rst:  # 初期化
        ss.flg1 = [False] * ss.df.shape[1]
        ss.rst = False
    for c, f in zip(ss.df.columns, ss.flg1):
        ss[c] = st.checkbox(c, f)
    ss.flg1 = [ss[c] for c in ss.df.columns]  # 状態の記憶
    ss.clmn = ss.df.columns[ss.flg1]
    buttons(ss.now)
elif ss.now == 2:
    st.write("### ステップ3: 可視化")
    msg = st.empty()
    if len(ss.clmn) == 0:
        msg.error("ステップ2で列が選択されていません。")
    else:
        msg.success("指定された条件で可視化しました。")
        col = st.columns([3, 2])
        with col[0]:
            st.write("##### グラフ")
            try:
                st.line_chart(ss.df[ss.clmn])
            except Exception:
                msg.error(
                    "グラフが表示できないので、列の組み合わせを見直してください。"
                )
        with col[1]:
            st.write("##### テーブル")
            st.dataframe(ss.df[ss.clmn])
    buttons(ss.now)
