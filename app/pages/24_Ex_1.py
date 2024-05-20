from datetime import datetime

import streamlit as st
from dateutil.relativedelta import relativedelta

st.title("確認用")
st.header("日付リスト")

# 日付を作成する期間をセット
span = st.radio(
    "取得する期間を選択",
    [6, 12, 18, 24, 28, 60, 72],
    horizontal=True,
)

# 基準月をセット
position = st.radio(
    "ベーステーブルを選択",
    [1, 2, 3, 4, 5, 6, 7],
    horizontal=True,
)

# 基準月をセット
start_date = datetime.now() - relativedelta(months=position)

# 降順でリストにする
dates = [start_date - relativedelta(months=i) for i in range(span)]  # type: ignore

selected_month = st.selectbox(
    "抽出したい利用年月を選んでください",
    options=dates,
    format_func=lambda x: f"{x.strftime('%Y年%m月')}",
)

# Debug
st.write(selected_month)
st.write(dates)
