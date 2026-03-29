# 02_rerun_demo.py — 재실행 모델 체험
# 실행: uv run streamlit run 02_rerun_demo.py
# 슬라이더를 움직일 때마다 "실행 시각"이 바뀌는 것을 관찰하세요!
import streamlit as st
import datetime

st.title("재실행 모델 체험")

# 스크립트가 실행될 때마다 현재 시각을 표시
current_time = datetime.datetime.now().strftime("%H:%M:%S")
st.write(f"스크립트 실행 시각: **{current_time}**")

# 슬라이더를 움직여 보세요 → 시각이 바뀝니다!
value = st.slider("숫자를 선택하세요", 0, 100, 50)
st.write(f"선택한 값: **{value}**")

# 결과 계산 — 위젯 값에 따라 자동 갱신
st.write(f"선택한 값의 제곱: **{value ** 2}**")

st.divider()
st.info(
    "👆 슬라이더를 움직일 때마다 '실행 시각'이 바뀌는 것을 관찰하세요.\n\n"
    "Streamlit은 위젯 값이 변경되면 **스크립트 전체를 처음부터 다시 실행**합니다."
)
