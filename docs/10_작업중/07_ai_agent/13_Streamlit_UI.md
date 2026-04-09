---
title: 13. Streamlit UI 연동
layout: default
grand_parent: LLM
parent: AI Agent
nav_order: 13
permalink: /llm/ai-agent/streamlit
---

## 학습 목표

- 12장의 여행 플래너에 Streamlit 웹 인터페이스를 연결할 수 있다

<a id="toc"></a>

## 진행 순서

1. [Streamlit 기본](#part1) - 입력/출력 위젯과 레이아웃
2. [여행 플래너 UI 설계](#part2) - 입력 폼과 결과 표시
3. [전체 코드](#part3) - travel_planner.py + app.py 완성본
4. [정리](#part4) - 실행 방법 및 확장 아이디어

---

# 13장. Streamlit UI 연동

<a id="part1"></a>

## 1️⃣ Streamlit 기본 [↑](#toc)

**Streamlit**은 Python 코드만으로 웹 앱을 만들 수 있는 라이브러리입니다. HTML/CSS/JavaScript 없이도 AI 에이전트에 사용자 인터페이스를 붙일 수 있습니다.

### 주요 위젯

```python
import streamlit as st

# ─── 입력 위젯 ───────────────────────────────────────────────
name = st.text_input("이름을 입력하세요")          # 한 줄 텍스트 입력
content = st.text_area("내용을 입력하세요")         # 여러 줄 텍스트 입력
option = st.selectbox("옵션 선택", ["A", "B", "C"]) # 드롭다운 선택
number = st.number_input("숫자 입력", min_value=0)  # 숫자 입력
clicked = st.button("실행")                         # 버튼

# ─── 출력 위젯 ───────────────────────────────────────────────
st.title("앱 제목")         # 큰 제목
st.header("섹션 제목")      # 섹션 제목
st.subheader("소제목")      # 소제목
st.write("일반 텍스트")     # 텍스트 출력
st.markdown("**굵은 글씨**")  # 마크다운 렌더링
st.success("성공 메시지")   # 초록 박스
st.warning("경고 메시지")   # 노랑 박스
st.error("오류 메시지")     # 빨간 박스
st.info("정보 메시지")      # 파랑 박스

# ─── 레이아웃 ────────────────────────────────────────────────
col1, col2 = st.columns(2)     # 2열 레이아웃
with col1:
    st.write("왼쪽")
with col2:
    st.write("오른쪽")

with st.expander("자세히 보기"):  # 접을 수 있는 섹션
    st.write("숨겨진 내용")

with st.spinner("처리 중..."):    # 로딩 스피너
    # 오래 걸리는 작업
    pass
```

### 기본 앱 구조

```python
import streamlit as st

st.set_page_config(
    page_title="AI 여행 플래너",
    page_icon="✈️",
    layout="wide"
)

st.title("AI 여행 플래너")

# 사용자 입력
destination = st.text_input("여행지")

if st.button("실행"):
    with st.spinner("처리 중..."):
        result = "처리 결과"   # 실제로는 AI 에이전트 호출
    st.success("완료!")
    st.write(result)
```

---

<a id="part2"></a>

## 2️⃣ 여행 플래너 UI 설계 [↑](#toc)

12장의 `TravelPlannerFlow`를 웹 UI에 연결합니다.

### UI 구성

```
┌─────────────────────────────────────────────────────┐
│  🌍 AI 여행 플래너                                    │
├─────────────────────────────────────────────────────┤
│  [사이드바]           [메인 영역]                      │
│                                                     │
│  여행지 입력          결과가 여기 표시됨               │
│  여행 기간 선택        - 여행지 특징                   │
│  예산 슬라이더         - 관광지 목록                   │
│  여행 스타일 선택      - 맛집 목록                     │
│                       - 일자별 일정                   │
│  [여행 계획 생성]      - 예산 분석                     │
│                       - 여행 팁                      │
└─────────────────────────────────────────────────────┘
```

### 핵심 연동 코드

```python
import streamlit as st
from travel_planner import TravelPlannerFlow, TravelPlan

st.title("🌍 AI 여행 플래너")

destination = st.text_input("여행지를 입력하세요", placeholder="예: 도쿄, 방콕, 파리")
days = st.selectbox("여행 기간", ["1박2일", "2박3일", "3박4일", "4박5일", "5박6일"])

if st.button("여행 계획 생성"):
    with st.spinner("AI 팀이 계획을 만들고 있습니다..."):
        flow = TravelPlannerFlow()
        result = flow.kickoff(inputs={
            "destination": destination,
            "days": days
        })
    st.success("여행 계획이 완성되었습니다!")
    st.markdown(result)
```

---

<a id="part3"></a>

## 3️⃣ 전체 코드 [↑](#toc)

### travel_planner.py — 에이전트 로직 분리

```python
# 파일명: travel_planner.py
# 12장의 코드를 모듈로 분리 (재사용 가능하도록)

from crewai import Agent, Task, Crew
from crewai.flow.flow import Flow, listen, start
from crewai.task import TaskOutput
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

# ─── 모델 ───────────────────────────────────────────────────
class TravelFlowState(BaseModel):
    destination: str = ""
    duration: str = ""
    budget: int = 0
    style: str = ""
    research_result: str = ""
    budget_analysis: str = ""

class TravelPlan(BaseModel):
    destination: str = Field(description="여행지")
    duration: str = Field(description="여행 기간")
    total_budget: int = Field(description="총 예산 (원)")
    budget_breakdown: dict = Field(default_factory=dict)
    highlights: List[str] = Field(description="여행지 주요 특징")
    attractions: List[str] = Field(description="추천 관광지")
    restaurants: List[str] = Field(description="추천 맛집")
    itinerary: List[str] = Field(description="일자별 일정")
    transportation: str = Field(description="교통 안내")
    accommodation: str = Field(description="숙박 안내")
    tips: List[str] = Field(description="여행 팁")

# ─── Guardrail ────────────────────────────────────────────────
def validate_plan(output: TaskOutput) -> tuple[bool, str]:
    try:
        plan = output.pydantic
    except Exception as e:
        return False, f"형식 오류: {e}"

    if plan.total_budget <= 0:
        return False, "총 예산이 0보다 커야 합니다."
    if len(plan.attractions) < 3:
        return False, f"관광지 최소 3곳 필요 (현재: {len(plan.attractions)}곳)"
    if len(plan.restaurants) < 2:
        return False, f"맛집 최소 2곳 필요 (현재: {len(plan.restaurants)}곳)"
    if len(plan.itinerary) == 0:
        return False, "일자별 일정이 비어 있습니다."

    return True, ""

# ─── Flow ────────────────────────────────────────────────────
class TravelPlannerFlow(Flow[TravelFlowState]):

    @start()
    def set_inputs(self):
        return self.state.destination

    @listen(set_inputs)
    def research_phase(self):
        researcher = Agent(
            role="여행지 리서치 전문가",
            goal="여행지의 핵심 정보를 조사한다",
            backstory="세계 각지를 방문한 여행 블로거입니다.",
            verbose=False
        )
        task = Task(
            description=(
                f"'{self.state.destination}' {self.state.duration} 여행을 위한 "
                f"리서치를 수행하세요. 여행 스타일: {self.state.style}\n"
                "관광지 5곳 이상, 맛집 3곳 이상, 교통·숙박 정보를 포함하세요."
            ),
            expected_output="상세 리서치 결과 (500자 이상)",
            agent=researcher
        )
        crew = Crew(agents=[researcher], tasks=[task], verbose=False)
        result = crew.kickoff()
        self.state.research_result = str(result)
        return self.state.research_result

    @listen(research_phase)
    def budget_phase(self):
        analyst = Agent(
            role="여행 예산 분석가",
            goal="여행 예산을 항목별로 최적화한다",
            backstory="재무 컨설턴트 출신 여행 예산 전문가입니다.",
            verbose=False
        )
        task = Task(
            description=(
                f"여행지: {self.state.destination}, "
                f"기간: {self.state.duration}, "
                f"총 예산: {self.state.budget:,}원\n\n"
                f"리서치 자료:\n{self.state.research_result}\n\n"
                "숙박/교통/식비/관광/기타 항목으로 예산을 배분하세요."
            ),
            expected_output="항목별 예산 배분과 절약 팁",
            agent=analyst
        )
        crew = Crew(agents=[analyst], tasks=[task], verbose=False)
        result = crew.kickoff()
        self.state.budget_analysis = str(result)
        return self.state.budget_analysis

    @listen(budget_phase)
    def planning_phase(self):
        planner = Agent(
            role="여행 계획 작가",
            goal="완성도 높은 여행 계획을 작성한다",
            backstory="10년 경력의 여행 가이드북 작가입니다.",
            verbose=False
        )
        task = Task(
            description=(
                f"여행지: {self.state.destination}, 기간: {self.state.duration}\n"
                f"총 예산: {self.state.budget:,}원, 스타일: {self.state.style}\n\n"
                f"[리서치]\n{self.state.research_result}\n\n"
                f"[예산 분석]\n{self.state.budget_analysis}\n\n"
                "관광지 3곳 이상, 맛집 2곳 이상, 일자별 일정 포함한 완성 계획을 작성하세요."
            ),
            expected_output="모든 필드가 채워진 완성된 여행 계획",
            output_pydantic=TravelPlan,
            guardrail=validate_plan,
            agent=planner
        )
        crew = Crew(agents=[planner], tasks=[task], verbose=False)
        crew.kickoff()
        plan: TravelPlan = task.output.pydantic
        return plan
```

### app.py — Streamlit 웹 인터페이스

```python
# 파일명: app.py
import streamlit as st
from travel_planner import TravelPlannerFlow, TravelPlan

# ─── 페이지 설정 ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI 여행 플래너",
    page_icon="✈️",
    layout="wide"
)

# ─── 사이드바: 입력 폼 ────────────────────────────────────────
with st.sidebar:
    st.header("여행 조건 입력")

    destination = st.text_input(
        "여행지",
        placeholder="예: 도쿄, 방콕, 파리, 제주도"
    )

    days = st.selectbox(
        "여행 기간",
        ["1박2일", "2박3일", "3박4일", "4박5일", "5박6일"]
    )

    budget = st.slider(
        "예산 (만원)",
        min_value=30,
        max_value=500,
        value=100,
        step=10
    )
    budget_won = budget * 10000   # 원 단위로 변환

    style = st.selectbox(
        "여행 스타일",
        ["관광 명소 중심", "미식/맛집 투어", "역사·문화 탐방",
         "자연·힐링", "쇼핑 중심", "액티비티/체험"]
    )

    st.markdown("---")
    generate_btn = st.button(
        "여행 계획 생성",
        type="primary",
        use_container_width=True,
        disabled=(not destination)   # 여행지 미입력 시 비활성화
    )

    if not destination:
        st.caption("여행지를 입력하면 버튼이 활성화됩니다.")

# ─── 메인 영역 ────────────────────────────────────────────────
st.title("🌍 AI 여행 플래너")
st.caption("CrewAI 멀티에이전트가 맞춤형 여행 계획을 만들어드립니다.")

if generate_btn and destination:
    # 진행 상태 표시
    progress_placeholder = st.empty()

    with st.spinner(f"AI 팀이 {destination} 여행 계획을 만들고 있습니다..."):
        progress_placeholder.info("1단계: 여행지 리서치 중...")

        try:
            flow = TravelPlannerFlow()
            result = flow.kickoff(inputs={
                "destination": destination,
                "duration": days,
                "budget": budget_won,
                "style": style
            })

            progress_placeholder.empty()

            if isinstance(result, TravelPlan):
                plan = result
                st.success(f"✅ {destination} {days} 여행 계획이 완성되었습니다!")

                # ─── 개요 카드 ──────────────────────────────
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("여행지", plan.destination)
                with col2:
                    st.metric("기간", plan.duration)
                with col3:
                    st.metric("총 예산", f"{plan.total_budget:,}원")

                st.markdown("---")

                # ─── 탭 레이아웃으로 결과 표시 ─────────────
                tab1, tab2, tab3, tab4 = st.tabs(
                    ["📍 관광지 & 맛집", "📅 일정표", "💰 예산 분석", "💡 여행 팁"]
                )

                with tab1:
                    col_att, col_rest = st.columns(2)

                    with col_att:
                        st.subheader("추천 관광지")
                        for i, att in enumerate(plan.attractions, 1):
                            st.write(f"{i}. {att}")

                    with col_rest:
                        st.subheader("추천 맛집")
                        for i, rest in enumerate(plan.restaurants, 1):
                            st.write(f"{i}. {rest}")

                    if plan.highlights:
                        st.subheader("여행지 특징")
                        for h in plan.highlights:
                            st.write(f"• {h}")

                with tab2:
                    st.subheader("일자별 일정")
                    for day_plan in plan.itinerary:
                        st.write(day_plan)

                    st.markdown("---")
                    col_trans, col_acc = st.columns(2)
                    with col_trans:
                        st.subheader("교통 안내")
                        st.write(plan.transportation)
                    with col_acc:
                        st.subheader("숙박 안내")
                        st.write(plan.accommodation)

                with tab3:
                    st.subheader("예산 항목별 분류")
                    if plan.budget_breakdown:
                        # 예산 표로 표시
                        breakdown_data = {
                            "항목": list(plan.budget_breakdown.keys()),
                            "금액": [
                                f"{int(v):,}원" if isinstance(v, (int, float))
                                else str(v)
                                for v in plan.budget_breakdown.values()
                            ]
                        }
                        st.table(breakdown_data)
                    else:
                        st.info("예산 상세 정보가 없습니다.")

                with tab4:
                    st.subheader("실용적인 여행 팁")
                    for tip in plan.tips:
                        st.write(f"• {tip}")

            else:
                # 구조화 출력이 아닌 경우 텍스트로 출력
                st.success("여행 계획이 완성되었습니다!")
                st.markdown(str(result))

        except Exception as e:
            progress_placeholder.empty()
            st.error(f"오류가 발생했습니다: {str(e)}")
            st.info("API 키와 네트워크 연결을 확인해주세요.")

elif not generate_btn:
    # 초기 화면
    st.markdown("""
    ### 사용 방법

    1. 왼쪽 사이드바에서 **여행 조건**을 입력합니다
    2. **여행지**, 기간, 예산, 스타일을 선택하세요
    3. **여행 계획 생성** 버튼을 클릭하면 AI 팀이 계획을 만들어드립니다

    ---

    ### AI 팀 소개

    | 에이전트 | 역할 |
    |---------|------|
    | 여행지 리서치 전문가 | 관광지, 맛집, 교통, 숙박 정보 수집 |
    | 예산 분석가 | 항목별 예산 최적화 |
    | 여행 계획 작가 | 일정 종합 및 최종 계획 작성 |
    """)
```

---

<a id="part4"></a>

## 4️⃣ 정리 [↑](#toc)

### 실행 방법

```bash
# 1. 패키지 설치
pip install crewai crewai-tools streamlit python-dotenv

# 2. .env 파일 설정
# OPENAI_API_KEY=sk-...

# 3. 앱 실행
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하면 웹 앱이 열립니다.

### 파일 구조

```
프로젝트/
├── .env                  # API 키 (git에 절대 포함 금지!)
├── travel_planner.py     # Flow + 에이전트 로직
└── app.py                # Streamlit UI
```

### Streamlit 주요 위젯 요약

| 위젯 | 함수 | 사용 예 |
|------|------|--------|
| 텍스트 입력 | `st.text_input()` | 여행지 입력 |
| 드롭다운 | `st.selectbox()` | 여행 기간 선택 |
| 슬라이더 | `st.slider()` | 예산 조절 |
| 버튼 | `st.button()` | 실행 트리거 |
| 로딩 중 | `st.spinner()` | 에이전트 실행 중 표시 |
| 탭 | `st.tabs()` | 결과 분류 표시 |
| 지표 | `st.metric()` | 숫자 강조 표시 |

### 확장 아이디어

| 기능 | 방법 |
|------|------|
| 결과 PDF 다운로드 | `st.download_button()` + `reportlab` |
| 지도 시각화 | `st.map()` 또는 `folium` |
| 대화형 채팅 | `st.chat_input()`, `st.chat_message()` |
| 로그인 | `st.secrets` + 세션 상태 |
| 결과 저장 | SQLite + `st.session_state` |

### 핵심 요약

- `travel_planner.py`와 `app.py`를 분리하여 **로직과 UI를 독립적으로 관리**
- `st.spinner()`로 에이전트 실행 중 사용자에게 진행 상황 안내
- `st.tabs()`로 풍부한 결과를 탭별로 구조화하여 가독성 향상
- `st.sidebar`로 입력 폼을 분리하여 메인 영역은 결과 표시에 집중

> **다음 장 미리보기:** 2일간의 학습을 정리하고 실무 적용을 위한 팁과 다음 학습 로드맵을 안내합니다.
