from datetime import datetime

import streamlit as st
from dateutil.relativedelta import relativedelta

st.title("確認用")
st.header("日付リスト生成", divider="rainbow")

position = st.radio(
    "基準月を選択",
    [0, 1, 2, 3],
    captions=["当月", "1 月前", "2 月前", "3 月前"],
    horizontal=True,
)

past_future = st.radio(
    "過去・未来",
    ["過去", "未来"],
    horizontal=True,
)

date_span = st.radio(
    "日付を作成する期間を選択",
    [6, 12, 24, 48, 60],
    format_func=lambda x: f"{x} か月",
    captions=["半年", "1 年", "2 年", "4 年", "5 年"],
    horizontal=True,
)

st.write(f"{past_future} {date_span} か月分を生成します。")

# 基準月をセット
start_date = datetime.now() - relativedelta(months=position)

# 降順でリストにする
dates = [start_date - relativedelta(months=i) for i in range(date_span)]  # type: ignore

selected_month = st.selectbox(
    "抽出したい利用年月を選んでください",
    options=dates,
    format_func=lambda x: f"{x.strftime('%Y年%m月')}",
)

# Debug
st.write(selected_month)
# st.write(dates)

if past_future == "過去":
    dates = [start_date - relativedelta(months=i) for i in range(date_span)]  # type: ignore

if past_future == "未来":
    dates = [start_date + relativedelta(months=i + 1) for i in range(date_span)]  # type: ignore

# Debug
st.write(dates)
