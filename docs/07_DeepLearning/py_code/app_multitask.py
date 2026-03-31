# app_multitask.py
import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

TASKS = {
    "Detection": "yolo26n.pt",
    "Segmentation": "yolo26n-seg.pt",
    "Pose": "yolo26n-pose.pt",
    "OBB": "yolo26n-obb.pt",
    "Classification": "yolo26n-cls.pt",
}

@st.cache_resource
def load_model(path):
    return YOLO(path)

st.title("YOLO26 멀티 비전 태스크")

with st.sidebar:
    task = st.radio("태스크 선택", list(TASKS.keys()))
    confidence = st.slider("신뢰도", 0.0, 1.0, 0.25, 0.05)

model = load_model(TASKS[task])
uploaded = st.file_uploader("이미지 업로드", type=["jpg", "jpeg", "png","webp"])

if uploaded:
    image = Image.open(uploaded)
    results = model(np.array(image), conf=confidence)
    r = results[0]

    # 태스크별 결과 표시
    if task == "Classification" and r.probs:
        # Classification: 원본 이미지 + Top-5 바 차트
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="원본", use_container_width=True)
        with col2:
            st.subheader("분류 결과")
            top1_name = r.names[int(r.probs.top1)]
            top1_conf = float(r.probs.top1conf)
            st.success(f"**{top1_name}** ({top1_conf:.1%})")
            for idx, conf_val in zip(r.probs.top5, r.probs.top5conf):
                name = r.names[int(idx)]
                pct = float(conf_val)
                st.write(f"{name}: {pct:.1%}")
                st.progress(pct)
    else:
        # Detection / Segmentation / Pose / OBB: 원본 + 어노테이션 이미지
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="원본", use_container_width=True)
        with col2:
            st.image(r.plot(), caption=f"{task} 결과", channels="BGR",
                     use_container_width=True)

        if task == "Pose" and r.keypoints is not None:
            st.subheader(f"탐지된 사람: {r.keypoints.xy.shape[0]}명")
        elif r.boxes is not None:
            st.subheader(f"탐지된 객체: {len(r.boxes)}개")
            for box in r.boxes:
                st.write(f"- {r.names[int(box.cls[0])]}: {float(box.conf[0]):.1%}")
