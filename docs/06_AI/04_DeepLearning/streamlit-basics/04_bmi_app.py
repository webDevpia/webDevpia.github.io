# 04_bmi_app.py — BMI 계산기 (미니 프로젝트)
# 실행: uv run streamlit run 04_bmi_app.py
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="BMI 계산기", page_icon="⚖️")

# 사이드바 — 입력
st.sidebar.title("신체 정보 입력")
name = st.sidebar.text_input("이름", value="사용자")
height = st.sidebar.slider("키 (cm)", 100, 220, 170)
weight = st.sidebar.slider("몸무게 (kg)", 30, 200, 70)

# 메인 — 결과
st.title("⚖️ BMI 계산기")
st.write(f"**{name}**님의 BMI를 계산합니다.")

# BMI 계산
height_m = height / 100
bmi = weight / (height_m ** 2)

# 2단 컬럼 레이아웃
col1, col2 = st.columns(2)

with col1:
    st.metric("키", f"{height} cm")
    st.metric("몸무게", f"{weight} kg")

with col2:
    st.metric("BMI", f"{bmi:.1f}")

    # BMI 판정
    if bmi < 18.5:
        st.info("저체중")
    elif bmi < 23:
        st.success("정상")
    elif bmi < 25:
        st.warning("과체중")
    else:
        st.error("비만")

# 구분선 + BMI 기준표
st.divider()
st.subheader("BMI 판정 기준")
st.write("""
| 범위 | 판정 |
|------|------|
| 18.5 미만 | 저체중 |
| 18.5 ~ 22.9 | 정상 |
| 23 ~ 24.9 | 과체중 |
| 25 이상 | 비만 |
""")
