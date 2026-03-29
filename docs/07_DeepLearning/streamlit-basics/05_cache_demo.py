# 05_cache_demo.py — 캐싱 체험
# 실행: uv run streamlit run 05_cache_demo.py
# 왼쪽(캐싱 없음)과 오른쪽(캐싱 있음)의 속도 차이를 비교하세요!
import streamlit as st
import time

st.set_page_config(page_title="캐싱 체험", layout="wide")
st.title("캐싱 있음 vs 없음 비교")


# 캐싱 없는 함수
def load_data_no_cache():
    """2초 걸리는 데이터 로드 시뮬레이션 (캐싱 없음)"""
    time.sleep(2)
    return list(range(1, 101))


# 캐싱 있는 함수
@st.cache_data
def load_data_cached():
    """2초 걸리는 데이터 로드 시뮬레이션 (캐싱 있음)"""
    time.sleep(2)
    return list(range(1, 101))


col1, col2 = st.columns(2)

with col1:
    st.header("캐싱 없음")
    if st.button("데이터 로드 (캐싱 없음)"):
        start = time.time()
        data = load_data_no_cache()
        elapsed = time.time() - start
        st.write(f"데이터 {len(data)}개 로드 완료")
        st.warning(f"소요 시간: {elapsed:.1f}초")
        st.write("→ 버튼을 누를 때마다 매번 2초 대기")

with col2:
    st.header("캐싱 있음 (@st.cache_data)")
    if st.button("데이터 로드 (캐싱 있음)"):
        start = time.time()
        data = load_data_cached()
        elapsed = time.time() - start
        st.write(f"데이터 {len(data)}개 로드 완료")
        if elapsed < 0.1:
            st.success(f"소요 시간: {elapsed:.3f}초 (캐시 히트!)")
        else:
            st.info(f"소요 시간: {elapsed:.1f}초 (최초 로드)")
        st.write("→ 첫 실행만 2초, 이후는 즉시!")

st.divider()
st.info(
    "**캐싱 원리**: `@st.cache_data`는 함수의 결과를 메모리에 저장합니다. "
    "같은 입력으로 다시 호출하면 함수를 실행하지 않고 저장된 결과를 바로 반환합니다.\n\n"
    "다음 시간(CNN)에서는 ML 모델을 로드할 때 `@st.cache_resource`를 사용합니다."
)
