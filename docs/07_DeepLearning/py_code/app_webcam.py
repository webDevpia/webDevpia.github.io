# app_webcam.py
import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

@st.cache_resource
def load_model():
    return YOLO("yolo26n.pt")

st.title("웹캠 객체 탐지")
model = load_model()
confidence = st.slider("신뢰도", 0.0, 1.0, 0.25, 0.05)

# st.camera_input: 브라우저 카메라로 사진 촬영
camera_image = st.camera_input("사진을 찍어주세요")

if camera_image:
    image = Image.open(camera_image)
    results = model(np.array(image), conf=confidence)

    st.image(results[0].plot(), channels="BGR", use_container_width=True)

    for box in results[0].boxes:
        cls = model.names[int(box.cls[0])]
        st.write(f"- {cls}: {float(box.conf[0]):.1%}")
