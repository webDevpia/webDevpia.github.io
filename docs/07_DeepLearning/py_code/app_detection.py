# app_detection.py
import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

# ===== 모델 캐싱 (앱 시작 시 1회만 로드) =====
@st.cache_resource
def load_model(name):
    return YOLO(name)

st.set_page_config(page_title="YOLO26 객체 탐지", layout="wide")
st.title("YOLO26 객체 탐지")

# 사이드바 설정
with st.sidebar:
    st.header("설정")
    model_name = st.selectbox("모델", ["yolo26n.pt", "yolo26s.pt"])
    confidence = st.slider("신뢰도 임계값", 0.0, 1.0, 0.25, 0.05)

model = load_model(model_name)

# 이미지 업로드
uploaded = st.file_uploader("이미지 업로드", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded)
    results = model(np.array(image), conf=confidence)
    r = results[0]

    # 원본 / 결과 나란히
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("원본")
        st.image(image, use_container_width=True)
    with col2:
        st.subheader("탐지 결과")
        st.image(r.plot(), channels="BGR", use_container_width=True)

    # 상세 정보
    st.subheader("탐지 상세")
    for box in r.boxes:
        cls = r.names[int(box.cls[0])]
        conf_val = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        st.write(f"**{cls}** — {conf_val:.1%} — "
                 f"위치: ({x1:.0f},{y1:.0f})~({x2:.0f},{y2:.0f})")
else:
    st.info("이미지를 업로드하세요.")
