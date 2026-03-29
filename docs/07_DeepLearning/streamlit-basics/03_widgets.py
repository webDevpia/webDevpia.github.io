# 03_widgets.py — 핵심 위젯 5종 놀이터
# 실행: uv run streamlit run 03_widgets.py
import streamlit as st

st.title("위젯 놀이터")

# 1. 텍스트 입력
name = st.text_input("이름", value="학생")

# 2. 슬라이더
score = st.slider("점수", 0, 100, 75)

# 3. 드롭다운
grade = st.selectbox("학년", ["1학년", "2학년", "3학년", "4학년"])

# 결과 표시
st.divider()
st.write(f"**{name}**님은 {grade}이고, 점수는 **{score}점**입니다.")

if score >= 90:
    st.success("우수합니다!")
elif score >= 70:
    st.info("양호합니다.")
else:
    st.warning("더 노력이 필요합니다.")

# 4. 버튼
if st.button("축하 버튼"):
    st.balloons()

# 5. 파일 업로드
st.divider()
uploaded = st.file_uploader("이미지를 선택하세요", type=["png", "jpg", "jpeg"])
if uploaded is not None:
    st.image(uploaded, caption="업로드한 이미지", width=300)
