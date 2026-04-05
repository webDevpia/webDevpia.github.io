---
title: 9. 통합 실습
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 9
permalink: /llm/langchain/practice
---


## 학습 목표

- 1~8장에서 배운 개념을 하나의 프로젝트에 통합하여 실습할 수 있다
- 여행 플래너 챗봇을 직접 만들며 각 개념이 실제로 어떻게 연결되는지 체험한다

<a id="toc"></a>

## 진행 순서

1. [프로젝트 개요](#part1) - 무엇을 만드는가 + 1~8장 개념 매핑
2. [환경 설정](#part2) - .env + 캐시 + LLM 초기화
3. [도구 정의](#part3) - 날씨/관광지/예산 도구 (mock)
4. [대화 체인 구성](#part4) - 프롬프트 + LCEL + 메모리
5. [구조화 출력](#part5) - 최종 여행 계획을 JSON으로
6. [터미널 챗봇 실행](#part6) - while 루프로 전체 통합
7. [Streamlit 웹 앱](#part7) - 동일 기능을 웹 UI로 구현
8. [실습 미션](#part8)

> **사전 준비:** [1장 개발환경](/llm/langchain/install)에서 `.env` 파일 설정과 패키지 설치를 완료한 상태에서 진행합니다.

---

# 여행 플래너 챗봇 — 1~8장 통합 실습

1~8장에서 배운 모든 개념을 하나의 **여행 플래너 챗봇**에 통합합니다. 단일 파일(`travel_planner.py`)로 구현하며, 각 개념이 코드 어디에 적용되는지 주석으로 표시합니다.

<a id="part1"></a>

## 1. 프로젝트 개요 [↑](#toc)

### 대화 시나리오

```
사용자: 파리 여행 계획을 세우고 싶어
AI: 파리 여행을 도와드리겠습니다! 며칠 일정인가요?
    🌤️ 파리 현재 날씨: 18℃, 맑음

사용자: 3박4일이요
AI: 파리 3박4일 일정을 추천해드립니다!
    🏛️ 추천 관광지: 에펠탑, 루브르 박물관, 몽마르트르
    💰 예상 예산: 약 $1,200

사용자: 아까 말한 예산을 좀 더 자세히 알려줘     ← 메모리: "파리/4일" 기억
AI: 파리 4일 예산 상세: 항공 $600, 숙박 $300, 식비 $200, 교통 $100

사용자: /plan                                   ← 구조화 출력: JSON
AI: { "destination": "파리", "days": 4, "highlights": [...], ... }
```

### 1~8장 개념 매핑

| 대화 시점 | 체감하는 개념 | 해당 장 |
|---|---|---|
| 프로그램 시작 | `.env`에서 API 키 로드 | 1장: 환경 설정 |
| 첫 질문 | `ChatOpenAI`로 LLM 호출 | 2장: 기본 사용 |
| 체인 실행 | `prompt \| llm \| parser` 파이프 | 3장: LCEL |
| 시스템 메시지 | `ChatPromptTemplate` + 변수 | 4장: 프롬프트 |
| `/plan` 명령 | `with_structured_output` → JSON | 5장: 출력 파서 |
| 날씨/관광지 조회 | `@tool` + `bind_tools` | 6장: 도구 |
| "아까 그 도시" | `RunnableWithMessageHistory` | 7장: 메모리 |
| 같은 도시 재질문 | `SQLiteCache` 히트 (0.00초) | 8장: 캐싱 |

---

<a id="part2"></a>

## 2. 환경 설정 [↑](#toc)

`.env`
```
OPENAI_API_KEY=본인의_OpenAI_API키
```

아래부터 `travel_planner.py` 파일의 내용입니다. 전체를 하나의 파일에 작성합니다.

```python
# ============================================================
# 여행 플래너 챗봇 — LangChain 1~8장 통합 실습
# ============================================================

# [1장] 환경 설정 — .env에서 API 키 로드
from dotenv import load_dotenv
load_dotenv()

# [8장] 캐싱 — 같은 질문 반복 시 API 비용 절감
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
import time

set_llm_cache(SQLiteCache(database_path="travel_cache.db"))

# [2장] LLM 초기화
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
```

> 💡 **Ollama 사용 시:** `from langchain_ollama import ChatOllama` 후 `llm = ChatOllama(model="gemma3:1b")`로 교체할 수 있습니다.

---

<a id="part3"></a>

## 3. 도구 정의 [↑](#toc)

> 아래 코드는 `travel_planner.py`에 이어서 작성합니다.

날씨, 관광지, 예산을 조회하는 도구를 정의합니다. 실제 API 대신 **mock(가짜) 데이터**를 반환하여, API 키 없이도 동작하도록 합니다.

```python
# [6장] 도구 — @tool 데코레이터로 LLM이 사용할 도구 정의
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """주어진 도시의 현재 날씨를 조회합니다."""
    # Mock 데이터 (실제 API로 교체 가능)
    weather_data = {
        "paris": "18℃, 맑음 ☀️",
        "tokyo": "22℃, 흐림 ☁️",
        "seoul": "15℃, 맑음 ☀️",
        "london": "12℃, 비 🌧️",
        "new york": "20℃, 맑음 ☀️",
    }
    result = weather_data.get(city.lower(), f"{city}: 20℃, 맑음 ☀️")
    return f"🌤️ {city} 현재 날씨: {result}"

@tool
def get_attractions(city: str) -> str:
    """주어진 도시의 인기 관광지를 조회합니다."""
    attractions_data = {
        "paris": "에펠탑, 루브르 박물관, 몽마르트르, 샹젤리제, 노트르담 대성당",
        "tokyo": "센소지, 시부야 스크램블, 도쿄타워, 아사쿠사, 신주쿠 교엔",
        "seoul": "경복궁, 남산타워, 북촌한옥마을, 명동, 이태원",
        "london": "빅벤, 런던아이, 대영박물관, 버킹엄궁, 타워브리지",
    }
    result = attractions_data.get(city.lower(), f"{city}의 주요 관광지")
    return f"🏛️ {city} 추천 관광지: {result}"

@tool
def estimate_budget(city: str, days: int) -> str:
    """주어진 도시와 일수에 맞는 여행 예산을 추정합니다."""
    daily_cost = {"paris": 300, "tokyo": 250, "seoul": 200, "london": 350}
    cost = daily_cost.get(city.lower(), 250)
    total = cost * days
    return (
        f"💰 {city} {days}일 예상 예산: 약 ${total:,}\n"
        f"   (항공 ${int(total*0.4):,} / 숙박 ${int(total*0.3):,} / "
        f"식비 ${int(total*0.2):,} / 교통 ${int(total*0.1):,})"
    )

tools = [get_weather, get_attractions, estimate_budget]
```

---

<a id="part4"></a>

## 4. 대화 체인 구성 [↑](#toc)

> 아래 코드는 `travel_planner.py`에 이어서 작성합니다.

프롬프트 템플릿, LCEL 체인, 메모리를 연결합니다.

```python
# [4장] 프롬프트 템플릿 — 시스템 역할 + 대화 히스토리 + 사용자 입력
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "당신은 전문 여행 플래너입니다.\n"
     "사용자의 여행 계획을 도와주세요.\n"
     "도구를 활용하여 날씨, 관광지, 예산 정보를 제공하세요.\n"
     "한국어로 친절하게 답변하세요."),
    MessagesPlaceholder("history"),       # [7장] 이전 대화가 여기에 삽입
    ("human", "{input}"),
])

# [3장] LCEL — 프롬프트 | LLM(도구 바인딩) | 파서 체인
from langchain_core.output_parsers import StrOutputParser

llm_with_tools = llm.bind_tools(tools)   # [6장] LLM에 도구 연결
chain = prompt | llm_with_tools | StrOutputParser()

# [7장] 메모리 — 세션별 대화 히스토리 관리
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)
```

---

<a id="part5"></a>

## 5. 구조화 출력 [↑](#toc)

> 아래 코드는 `travel_planner.py`에 이어서 작성합니다.

사용자가 `/plan`을 입력하면 대화 내용을 바탕으로 **구조화된 여행 계획(JSON)**을 생성합니다.

```python
# [5장] 출력 파서 — Pydantic 스키마로 구조화된 JSON 출력
from pydantic import BaseModel, Field

class TravelPlan(BaseModel):
    destination: str = Field(description="여행 도시")
    days: int = Field(description="여행 일수")
    highlights: list[str] = Field(description="추천 관광지 목록")
    estimated_budget: str = Field(description="예상 총 예산")
    tips: str = Field(description="여행 팁 한 줄")

plan_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "아래 대화 내용을 바탕으로 여행 계획을 구조화된 형식으로 정리하세요."),
    MessagesPlaceholder("history"),
    ("human", "지금까지 대화를 바탕으로 최종 여행 계획을 만들어줘."),
])

structured_llm = llm.with_structured_output(TravelPlan)
plan_chain = plan_prompt | structured_llm
```

---

<a id="part6"></a>

## 6. 터미널 챗봇 실행 [↑](#toc)

> 아래 코드는 `travel_planner.py`에 이어서 작성합니다.

모든 개념을 통합한 대화형 루프입니다.

```python
# ============================================================
# 대화형 루프 — 전체 통합
# ============================================================
import json

def run_chatbot():
    session_id = "travel-session-1"
    config = {"configurable": {"session_id": session_id}}

    print("=" * 50)
    print("  ✈️  여행 플래너 챗봇")
    print("  명령어: /plan (여행 계획 JSON) | /history (대화 기록) | q (종료)")
    print("=" * 50)

    while True:
        user_input = input("\n사용자: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["q", "quit", "종료"]:
            print("여행 계획을 즐겁게 세우셨길 바랍니다! 👋")
            break

        # /plan 명령: [5장] 구조화 출력으로 최종 계획 생성
        if user_input == "/plan":
            print("\n📋 최종 여행 계획을 생성합니다...\n")
            history = get_session_history(session_id)
            try:
                plan = plan_chain.invoke(
                    {"history": history.messages},
                )
                print(json.dumps(plan.model_dump(), ensure_ascii=False, indent=2))
            except Exception as e:
                print(f"여행 계획 생성 실패: {e}")
                print("먼저 여행지와 일정에 대해 대화해주세요.")
            continue

        # /history 명령: [7장] 저장된 대화 확인
        if user_input == "/history":
            history = get_session_history(session_id)
            print(f"\n=== 대화 기록 ({len(history.messages)}개 메시지) ===")
            for msg in history.messages:
                role = "사용자" if msg.type == "human" else "AI"
                print(f"  {role}: {msg.content[:60]}{'...' if len(msg.content) > 60 else ''}")
            continue

        # 일반 대화: [3장] LCEL + [6장] 도구 + [7장] 메모리 + [8장] 캐시
        start = time.time()
        response = chain_with_memory.invoke(
            {"input": user_input},
            config=config,
        )
        elapsed = time.time() - start

        print(f"\nAI: {response}")
        print(f"   ⏱️ {elapsed:.2f}초", "(캐시 히트!)" if elapsed < 0.1 else "")


if __name__ == "__main__":
    run_chatbot()
```

```bash
python travel_planner.py
```

**실행 예시:**
```
==================================================
  ✈️  여행 플래너 챗봇
  명령어: /plan (여행 계획 JSON) | /history (대화 기록) | q (종료)
==================================================

사용자: 파리 여행을 계획하고 싶어

AI: 파리 여행을 도와드리겠습니다! 먼저 파리의 현재 날씨를 알려드릴게요.
    🌤️ 파리 현재 날씨: 18℃, 맑음 ☀️
    며칠 일정으로 계획하시나요?
   ⏱️ 1.35초

사용자: 3박4일이요

AI: 파리 3박4일 여행을 추천해드립니다!
    🏛️ 추천 관광지: 에펠탑, 루브르 박물관, 몽마르트르, 샹젤리제, 노트르담 대성당
    💰 예상 예산: 약 $1,200 (항공 $480 / 숙박 $360 / 식비 $240 / 교통 $120)
   ⏱️ 2.10초

사용자: 아까 말한 예산 중 숙박을 좀 더 절약하려면?

AI: 파리에서 숙박비를 절약하는 방법을 알려드릴게요!
    1. 호스텔 이용: 1박 $30~50 (3박 $90~150 절약 가능)
    2. Airbnb: 중심부 외곽 지역으로 1박 $60~80
    3. 조기 예약: 2~3개월 전 예약 시 20~30% 할인
   ⏱️ 1.52초

사용자: /plan

📋 최종 여행 계획을 생성합니다...

{
  "destination": "파리",
  "days": 4,
  "highlights": ["에펠탑", "루브르 박물관", "몽마르트르", "샹젤리제", "노트르담 대성당"],
  "estimated_budget": "약 $1,200",
  "tips": "숙박비 절약을 위해 Airbnb나 호스텔을 활용하고, 2~3개월 전 조기 예약을 추천합니다."
}

사용자: q
여행 계획을 즐겁게 세우셨길 바랍니다! 👋
```

> 💡 같은 도시에 대해 다시 질문하면 `SQLiteCache`가 작동하여 응답 시간이 0.00초에 가까워집니다. `travel_cache.db` 파일이 프로젝트 폴더에 생성됩니다.

---

<a id="part7"></a>

## 7. Streamlit 웹 앱 [↑](#toc)

6장의 터미널 챗봇과 **동일한 기능**을 웹 UI로 구현합니다. 도구, 체인, 메모리, 캐시는 그대로 사용하고 UI만 Streamlit으로 교체합니다.

```
터미널 버전 (travel_planner.py)     Streamlit 버전 (travel_app.py)
┌──────────────────────┐           ┌──────────────────────────┐
│ input("사용자: ")     │    →     │ st.chat_input()           │
│ print("AI: ...")     │    →     │ st.chat_message("assistant") │
│ /plan → print(JSON)  │    →     │ 사이드바 버튼 → st.json() │
└──────────────────────┘           └──────────────────────────┘
```

`travel_app.py`
```python
# ============================================================
# 여행 플래너 챗봇 — Streamlit 웹 앱 버전
# ============================================================

import streamlit as st
import json
import time

# [1장] 환경 설정
from dotenv import load_dotenv
load_dotenv()

# [8장] 캐싱
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
set_llm_cache(SQLiteCache(database_path="travel_cache.db"))

# [2장] LLM 초기화
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# [6장] 도구 정의
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """주어진 도시의 현재 날씨를 조회합니다."""
    weather_data = {
        "paris": "18℃, 맑음", "tokyo": "22℃, 흐림",
        "seoul": "15℃, 맑음", "london": "12℃, 비",
    }
    result = weather_data.get(city.lower(), f"20℃, 맑음")
    return f"{city} 현재 날씨: {result}"

@tool
def get_attractions(city: str) -> str:
    """주어진 도시의 인기 관광지를 조회합니다."""
    data = {
        "paris": "에펠탑, 루브르 박물관, 몽마르트르, 샹젤리제",
        "tokyo": "센소지, 시부야 스크램블, 도쿄타워, 아사쿠사",
        "seoul": "경복궁, 남산타워, 북촌한옥마을, 명동",
    }
    return f"{city} 추천 관광지: {data.get(city.lower(), '주요 관광지')}"

@tool
def estimate_budget(city: str, days: int) -> str:
    """주어진 도시와 일수에 맞는 여행 예산을 추정합니다."""
    daily = {"paris": 300, "tokyo": 250, "seoul": 200, "london": 350}
    total = daily.get(city.lower(), 250) * days
    return f"{city} {days}일 예상 예산: 약 ${total:,}"

tools = [get_weather, get_attractions, estimate_budget]

# [4장] 프롬프트 + [3장] LCEL 체인
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "당신은 전문 여행 플래너입니다. 도구를 활용하여 날씨, 관광지, 예산 정보를 제공하세요. 한국어로 답변하세요."),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
])

llm_with_tools = llm.bind_tools(tools)
chain = prompt | llm_with_tools | StrOutputParser()

# [7장] 메모리
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain, get_session_history,
    input_messages_key="input", history_messages_key="history",
)

# [5장] 구조화 출력
from pydantic import BaseModel, Field

class TravelPlan(BaseModel):
    destination: str = Field(description="여행 도시")
    days: int = Field(description="여행 일수")
    highlights: list[str] = Field(description="추천 관광지 목록")
    estimated_budget: str = Field(description="예상 총 예산")
    tips: str = Field(description="여행 팁 한 줄")

plan_prompt = ChatPromptTemplate.from_messages([
    ("system", "대화 내용을 바탕으로 여행 계획을 구조화된 형식으로 정리하세요."),
    MessagesPlaceholder("history"),
    ("human", "최종 여행 계획을 만들어줘."),
])
plan_chain = plan_prompt | llm.with_structured_output(TravelPlan)


# ============================================================
# Streamlit UI
# ============================================================

st.set_page_config(page_title="여행 플래너", page_icon="✈️")
st.title("✈️ 여행 플래너 챗봇")
st.caption("1~8장 통합 실습 | LLM + 도구 + 메모리 + 캐싱 + 구조화 출력")

SESSION_ID = "streamlit-session"
config = {"configurable": {"session_id": SESSION_ID}}

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사이드바: 여행 계획 생성 버튼
with st.sidebar:
    st.header("명령")
    if st.button("📋 여행 계획 생성 (JSON)", use_container_width=True):
        history = get_session_history(SESSION_ID)
        if history.messages:
            with st.spinner("여행 계획을 생성하는 중..."):
                try:
                    plan = plan_chain.invoke({"history": history.messages})
                    st.json(plan.model_dump())
                except Exception as e:
                    st.error(f"생성 실패: {e}")
        else:
            st.warning("먼저 여행지에 대해 대화해주세요.")

    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        if SESSION_ID in store:
            store[SESSION_ID] = InMemoryChatMessageHistory()
        st.rerun()

# 대화 히스토리 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 채팅 입력
if user_input := st.chat_input("여행지를 입력해보세요 (예: 파리 여행 계획을 세우고 싶어)"):
    # 사용자 메시지 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 (스트리밍)
    with st.chat_message("assistant"):
        start = time.time()
        try:
            response = chain_with_memory.invoke(
                {"input": user_input}, config=config,
            )
            elapsed = time.time() - start
            cache_tag = " *(캐시 히트!)*" if elapsed < 0.1 else ""
            full_response = f"{response}\n\n`⏱️ {elapsed:.2f}초{cache_tag}`"
            st.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"응답 생성 중 오류: {e}")
```

```bash
streamlit run travel_app.py --server.port 8501
```

**화면 구성:**

```
┌─────────────┬──────────────────────────────────────┐
│  사이드바     │  채팅 영역                             │
│             │                                       │
│ [📋 여행     │  사용자: 파리 여행을 계획하고 싶어       │
│  계획 생성]  │                                       │
│             │  AI: 파리 여행을 도와드리겠습니다!       │
│ [🗑️ 대화    │      🌤️ 파리 현재 날씨: 18℃, 맑음    │
│  초기화]    │      며칠 일정인가요?                   │
│             │      ⏱️ 1.35초                         │
│             │                                       │
│             │  사용자: 3박4일이요                     │
│             │                                       │
│             │  AI: 파리 3박4일 추천!                  │
│             │      🏛️ 에펠탑, 루브르, 몽마르트르     │
│             │      💰 예상 예산: $1,200               │
│             │      ⏱️ 2.10초                         │
│             │                                       │
│             │  [여행지를 입력해보세요...]              │
└─────────────┴──────────────────────────────────────┘
```

> 💡 사이드바의 **📋 여행 계획 생성** 버튼을 누르면 대화 내용을 바탕으로 구조화된 JSON 계획이 사이드바에 표시됩니다.

### 터미널 vs Streamlit 비교

| | 터미널 (`travel_planner.py`) | Streamlit (`travel_app.py`) |
|---|---|---|
| 실행 | `python travel_planner.py` | `streamlit run travel_app.py` |
| 입력 | `input()` | `st.chat_input()` |
| 출력 | `print()` | `st.chat_message()` + `st.markdown()` |
| /plan | 터미널에 JSON 출력 | 사이드바에 `st.json()` |
| 대화 초기화 | 프로그램 재시작 | 사이드바 버튼 |
| 도구/체인/메모리 | 동일 | 동일 |

---

<a id="part8"></a>

## 8. 실습 미션 [↑](#toc)

### 기본

- 터미널 버전을 실행하고, 3개 이상의 도시에 대해 대화해보세요
- 같은 도시를 두 번 질문하고, 응답 시간 차이(캐시 효과)를 확인해보세요
- `/plan` 명령으로 JSON 계획이 올바르게 생성되는지 확인해보세요

### 중급

- Streamlit 버전을 실행하고, 터미널 버전과 동일한 대화를 해보세요
- `get_weather` 도구의 mock 데이터를 실제 OpenWeather API로 교체해보세요 (힌트: [6장 4.2](/llm/langchain/tool) 참고)
- `TravelPlan` 스키마에 `weather` 필드를 추가하고, 계획에 날씨가 포함되도록 수정해보세요

### 심화

- Streamlit 앱에 **사용자 이름 입력** 기능을 추가하여 `session_id`를 분리하고, 여러 사용자가 독립된 여행 계획을 세울 수 있게 만들어보세요
- Streamlit 앱에 **여행 계획 다운로드** 버튼(`st.download_button`)을 추가해보세요


---

## 전체 코드 요약

| 개념 (장) | 코드 위치 | 핵심 API |
|---|---|---|
| 1장: 환경 설정 | 맨 위 | `load_dotenv()` |
| 2장: LLM | 맨 위 | `ChatOpenAI(model="gpt-4o-mini")` |
| 3장: LCEL | 체인 구성 | `prompt \| llm_with_tools \| StrOutputParser()` |
| 4장: 프롬프트 | 체인 구성 | `ChatPromptTemplate`, `MessagesPlaceholder` |
| 5장: 파서 | 구조화 출력 | `llm.with_structured_output(TravelPlan)` |
| 6장: 도구 | 도구 정의 | `@tool`, `llm.bind_tools(tools)` |
| 7장: 메모리 | 체인 구성 | `RunnableWithMessageHistory`, `session_id` |
| 8장: 캐싱 | 맨 위 | `set_llm_cache(SQLiteCache(...))` |
