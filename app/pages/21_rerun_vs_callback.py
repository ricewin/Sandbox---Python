"""StreamlitでコードとUIをスッキリさせるためのノウハウをまとめてみた

https://nttdocomo-developers.jp/entry/20231216_1
"""

from time import sleep

import streamlit as st

ss = st.session_state


def countup():
    ss.view1 += 1


def reset():
    ss.view1 = 0


if "view0" not in ss:
    ss.view0 = 0
    reset()

# アプリ本体=================================
st.title("❹rerunとコールバックの比較")
st.radio("", ["rerun", "コールバック"], key="which", horizontal=True)

if ss.which == "rerun":
    if ss.view0 == 0:
        with st.spinner("初期化中ですのでお待ちください..."):
            sleep(3)
        st.subheader("はじめに")
        st.warning("冒頭の操作説明文")
        if st.button("ステップ1へ"):
            ss.view0 = 1
            st.rerun()
    if ss.view0 == 1:
        st.subheader("ステップ1")
        st.info("さあ実行しましょう")
        if st.button("実行ボタン"):
            ss.view0 = 2
            st.rerun()
    if ss.view0 == 2:
        st.subheader("ステップ2")
        with st.spinner("処理を実行中です。お待ちください..."):
            sleep(3)
            st.success("完了！")
            if st.button("はじめからやり直す"):
                ss.view0 = 0
                st.rerun()
else:
    if ss.view1 == 0:
        with st.spinner("初期化中ですのでお待ちください..."):
            sleep(3)
        st.subheader("はじめに")
        st.warning("冒頭の操作説明文")
        st.button("ステップ1へ", on_click=countup)
    if ss.view1 == 1:
        st.subheader("ステップ1")
        st.info("さあ実行しましょう")
        st.button("実行ボタン", on_click=countup)
    if ss.view1 == 2:
        st.subheader("ステップ2")
        with st.spinner("処理を実行中です。お待ちください..."):
            sleep(3)
            st.success("完了！")
        st.button("はじめからやり直す", on_click=reset)
