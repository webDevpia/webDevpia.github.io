# 01_hello.py — Streamlit Hello World
# 실행: uv run streamlit run 01_hello.py
import streamlit as st

st.title("안녕하세요!")
st.write("Streamlit으로 만든 첫 번째 웹 앱입니다.")
st.write("아래는 `st.write()`로 출력한 다양한 데이터입니다.")

# st.write()는 거의 모든 것을 출력합니다
st.write("### 텍스트 (마크다운)")
st.write(1 + 2 + 3)  # 숫자
st.write({"이름": "철수", "나이": 25})  # 딕셔너리
