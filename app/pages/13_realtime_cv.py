import av  # type: ignore
import cv2  # type: ignore
import streamlit as st
from streamlit_webrtc import webrtc_streamer  # type: ignore

# ブラウザで動くリアルタイム画像/音声処理アプリをStreamlitでサクッと作る
# https://zenn.dev/whitphx/articles/streamlit-realtime-cv-app

st.title("My first Streamlit app")
st.write("Hello, world")

threshold1 = st.slider("Threshold1", min_value=0, max_value=1000, step=1, value=100)
threshold2 = st.slider("Threshold2", min_value=0, max_value=1000, step=1, value=200)


def callback(frame):
    img = frame.to_ndarray(format="bgr24")

    img = cv2.cvtColor(cv2.Canny(img, threshold1, threshold2), cv2.COLOR_GRAY2BGR)

    return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="example",
    video_frame_callback=callback,
    rtc_configuration={  # Add this line
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
)
