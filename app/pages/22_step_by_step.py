"""StreamlitでコードとUIをスッキリさせるためのノウハウをまとめてみた

https://nttdocomo-developers.jp/entry/20231216_1
"""

import streamlit as st

ss = st.session_state

# 状態変数==================================
if "now" not in ss:  # 初期化
    ss.now = 0  # 初期化


def countup():  # コールバック関数(1/3):次へ
    ss.now += 1


def countdown():  # コールバック関数(2/3):戻る
    ss.now -= 1


def reset():  # コールバック関数(3/3):リセット
    ss.now = 0


# UIパーツ=================================
def buttons(now):
    col = st.columns(3)
    if ss.now < 3:
        col[0].button("次へ進む", on_click=countup)
    if ss.now > 0:
        col[1].button("前へ戻る", on_click=countdown)
    if ss.now > 1:
        col[2].button("はじめから", on_click=reset)


# アプリ本体=================================
col = st.columns([2, 1])
col[0].title("❺ステップbyステップ")
if col[1].toggle("ステップbyステップ", True):
    st.write("### A) ステップ毎に表示")
    if ss.now == 0:
        st.write("#### ステップ1")
        st.error("ここにステップ1の処理を記述します")
        buttons(ss.now)
    elif ss.now == 1:
        st.write("#### ステップ2")
        st.warning("ここにステップ2の処理を記述します")
        buttons(ss.now)
    elif ss.now == 2:
        st.write("#### ステップ3")
        st.info("ここにステップ3の処理を記述します")
        buttons(ss.now)
    else:
        st.write("### 完了！")
        st.success("全てのステップが完了しました")
        buttons(ss.now)
else:
    st.write("### B) 全てを常時表示")
    st.write("#### ステップ1")
    st.error("ここにステップ1の処理を記述します")
    st.write("#### ステップ2")
    st.warning("ここにステップ2の処理を記述します")
    st.write("#### ステップ3")
    st.info("ここにステップ3の処理を記述します")
    st.success("以上で全てのステップが完了です。")
