---
title: "17. Streamlit UI 배포"
layout: default
grand_parent: LLM
parent: LangGraph
nav_order: 17
permalink: /llm/langgraph/deployment
---

# 🚀 Streamlit UI 배포

"아, 뭐 먹지? 뭐 하지?" LangGraph 프로젝트를 Streamlit으로 감싸 누구나 접근할 수 있는 웹 서비스로 배포합니다.  
이 장은 15~16장에서 완성한 LangGraph 그래프를 실제 사용자가 쓸 수 있는 형태로 만드는 마지막 단계입니다.

---

<a id="toc"></a>

## 진행 순서

1. [Streamlit 채팅 UI 기초](#part1)
2. [LangGraph + Streamlit 통합](#part2)
3. [음식/활동 추천 챗봇 UI 구현](#part3)
4. [스트리밍 응답 구현](#part4)
5. [배포하기](#part5)
6. [배포 후 확인](#part6)
7. [정리](#part7)

---

<a id="part1"></a>

## 1️⃣ Streamlit 채팅 UI 기초 [↑](#toc)

### st.chat_message와 st.chat_input 소개

Streamlit 1.22 이상에서 제공하는 채팅 전용 컴포넌트입니다.

| 컴포넌트 | 역할 |
|---------|------|
| `st.chat_message(role)` | 말풍선 형태의 메시지 블록. `"user"` 또는 `"assistant"` |
| `st.chat_input(placeholder)` | 하단 고정 입력창. 엔터 또는 전송 버튼으로 제출 |
| `st.session_state` | 페이지 새로고침 없이 상태(대화 히스토리)를 유지 |

> 💡 `st.chat_input`은 반환값이 `None`(아무것도 입력 안 됨)이거나 입력 문자열입니다.  
> `:= (walrus operator)`를 활용하면 입력 감지와 처리를 한 줄에 쓸 수 있습니다.

### Session State로 대화 히스토리 관리

Streamlit 앱은 사용자가 메시지를 보낼 때마다 스크립트 전체를 재실행합니다.  
대화 내용을 유지하려면 `st.session_state`에 메시지 목록을 저장해야 합니다.

```python
# 세션 상태 초기화 (최초 실행 시에만)
if "messages" not in st.session_state:
    st.session_state.messages = []
```

### 기본 채팅 루프

```python
import streamlit as st

st.title("🍽 뭐 먹지? 뭐 하지?")

# 1. 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. 기존 대화 내용 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 3. 사용자 입력 처리
if prompt := st.chat_input("무엇이 궁금하세요?"):
    # 사용자 메시지 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # LangGraph 호출 및 응답 표시
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            response = get_response(prompt)
        st.write(response)

    # 어시스턴트 메시지 저장
    st.session_state.messages.append({"role": "assistant", "content": response})
```

> ⚠️ `st.session_state.messages`에 저장하지 않으면 페이지 재실행 시 대화 내용이 사라집니다.

---

<a id="part2"></a>

## 2️⃣ LangGraph + Streamlit 통합 [↑](#toc)

### 그래프를 Streamlit 세션에 연결하는 패턴

LangGraph 그래프 컴파일은 비용이 큰 작업입니다.  
매번 요청마다 다시 컴파일하면 응답 속도가 느려집니다.  
`@st.cache_resource`를 사용하면 앱이 처음 실행될 때 한 번만 컴파일하고 이후에는 캐시된 그래프를 재사용합니다.

```python
import streamlit as st
from run_graph import build_graph  # 그래프 생성 함수

@st.cache_resource
def get_graph():
    """앱 시작 시 한 번만 그래프를 컴파일합니다."""
    return build_graph()

graph = get_graph()
```

### Thread_id를 세션 ID로 사용

LangGraph의 메모리(체크포인터)를 활용할 경우, 각 사용자의 대화 맥락을 구분하기 위해 고유한 `thread_id`가 필요합니다.  
Streamlit 세션 ID를 thread_id로 활용하면 사용자별 대화 맥락을 자연스럽게 분리할 수 있습니다.

```python
import uuid

# 세션 ID 초기화 (사용자당 고유 ID)
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}

# 그래프 호출 시 config 전달
result = graph.invoke(initial_state, config)
```

### 에러 처리

그래프 실행 도중 API 오류, 네트워크 오류 등이 발생할 수 있습니다.  
사용자에게 오류를 그대로 노출하지 않고 친절한 안내 메시지를 표시합니다.

```python
def get_response(user_input: str, location: str = "홍대") -> str:
    """LangGraph를 실행하고 최종 메시지를 반환합니다."""
    initial_state = {
        "user_input": user_input,
        "location": location
    }
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    try:
        result = graph.invoke(initial_state, config)
        return result.get("final_message", "추천 결과를 가져올 수 없습니다.")
    except Exception as e:
        # 개발 환경에서는 오류 내용을 표시, 운영 환경에서는 일반 메시지만 표시
        return f"죄송해요, 잠시 오류가 발생했습니다. 다시 시도해 주세요. 😊"
```

> 💡 운영 환경에서는 `st.error()` 또는 `st.warning()`으로 오류를 별도 표시하고,  
> 메인 채팅 흐름은 계속 진행되도록 설계하는 것이 좋습니다.

---

<a id="part3"></a>

## 3️⃣ 음식/활동 추천 챗봇 UI 구현 [↑](#toc)

### 전체 app.py 구현

15~16장 프로젝트를 Streamlit으로 래핑한 완전한 구현 코드입니다.

```python
# app.py
import streamlit as st
import uuid
from datetime import datetime
from run_graph import build_graph

# ─── 페이지 기본 설정 ────────────────────────────────────────────
st.set_page_config(
    page_title="뭐 먹지? 뭐 하지?",
    page_icon="🍽",
    layout="wide"
)

# ─── 그래프 초기화 (캐시 적용) ───────────────────────────────────
@st.cache_resource
def get_graph():
    return build_graph()

graph = get_graph()


# ─── 현재 상황 정보 계산 ─────────────────────────────────────────
def get_current_time_slot() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return "아침 🌅"
    elif 11 <= hour < 16:
        return "점심 ☀️"
    elif 16 <= hour < 22:
        return "저녁 🌆"
    else:
        return "야간 🌙"


def get_current_season() -> str:
    month = datetime.now().month
    if 3 <= month <= 5:
        return "봄 🌸"
    elif 6 <= month <= 8:
        return "여름 ☀️"
    elif 9 <= month <= 11:
        return "가을 🍂"
    else:
        return "겨울 ❄️"


# ─── LangGraph 응답 함수 ─────────────────────────────────────────
def get_response(user_input: str, location: str) -> dict:
    """LangGraph를 실행하고 전체 최종 상태를 반환합니다."""
    initial_state = {
        "user_input": user_input,
        "location": location
    }
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    try:
        result = graph.invoke(initial_state, config)
        return result
    except Exception:
        return {"final_message": "죄송해요, 잠시 오류가 발생했습니다. 다시 시도해 주세요. 😊"}


# ─── 세션 상태 초기화 ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())


# ─── 사이드바: 현재 상황 표시 ────────────────────────────────────
with st.sidebar:
    st.title("📌 현재 상황")
    st.metric("시간대", get_current_time_slot())
    st.metric("계절", get_current_season())

    st.divider()

    st.subheader("📍 내 위치")
    location = st.text_input("지역 입력", value="홍대", placeholder="예: 홍대, 강남, 신촌")

    st.divider()

    if st.button("🗑 대화 초기화"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()


# ─── 메인 영역: 채팅 ──────────────────────────────────────────────
st.title("🍽 뭐 먹지? 뭐 하지?")
st.caption("지금 기분이나 상황을 자연스럽게 말해보세요.")

# 기존 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and isinstance(msg.get("data"), dict):
            # 추천 결과 카드 형태로 표시
            data = msg["data"]

            # 추천 음식/활동 카드
            items = data.get("recommended_items", [])
            if items:
                intent = data.get("intent", "food")
                label = "🍲 추천 음식" if intent == "food" else "🎯 추천 활동"
                st.subheader(label)
                cols = st.columns(len(items))
                for i, item in enumerate(items):
                    with cols[i]:
                        st.info(f"**{item}**")

            # 장소 정보
            place = data.get("recommended_place", {})
            if place and place.get("name"):
                st.subheader("📍 추천 장소")
                place_name = place.get("name", "")
                place_addr = place.get("address", "")
                place_url = place.get("url", "")
                if place_url:
                    st.markdown(f"**{place_name}**  \n{place_addr}  \n[카카오맵에서 보기]({place_url})")
                else:
                    st.markdown(f"**{place_name}**  \n{place_addr}")

            # 최종 메시지
            st.write(data.get("final_message", ""))
        else:
            st.write(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input("무엇이 궁금하세요? (예: 배고파, 심심해, 뭐하지?)"):
    # 사용자 메시지 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 어시스턴트 응답
    with st.chat_message("assistant"):
        with st.spinner("생각 중... 🤔"):
            result = get_response(prompt, location)

        # 추천 결과 카드 표시
        items = result.get("recommended_items", [])
        if items:
            intent = result.get("intent", "food")
            label = "🍲 추천 음식" if intent == "food" else "🎯 추천 활동"
            st.subheader(label)
            cols = st.columns(len(items))
            for i, item in enumerate(items):
                with cols[i]:
                    st.info(f"**{item}**")

        # 장소 정보
        place = result.get("recommended_place", {})
        if place and place.get("name"):
            st.subheader("📍 추천 장소")
            place_name = place.get("name", "")
            place_addr = place.get("address", "")
            place_url = place.get("url", "")
            if place_url:
                st.markdown(f"**{place_name}**  \n{place_addr}  \n[카카오맵에서 보기]({place_url})")
            else:
                st.markdown(f"**{place_name}**  \n{place_addr}")

        # 최종 메시지
        final_msg = result.get("final_message", "추천 결과를 가져올 수 없습니다.")
        st.write(final_msg)

    # 세션에 저장 (데이터 포함)
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_msg,
        "data": result
    })
```

> 💡 사이드바의 "대화 초기화" 버튼을 누르면 `thread_id`도 새로 생성되어 LangGraph 메모리도 초기화됩니다.

---

<a id="part4"></a>

## 4️⃣ 스트리밍 응답 구현 [↑](#toc)

### st.write_stream()으로 토큰 단위 스트리밍

LangGraph의 `graph.stream()`을 Streamlit의 `st.write_stream()`과 연동하면  
응답이 생성되는 즉시 화면에 출력됩니다.  
사용자 입장에서는 로딩 대기 없이 실시간으로 결과를 확인할 수 있습니다.

```python
with st.chat_message("assistant"):
    response = st.write_stream(stream_response(prompt))
```

### 스트리밍 응답 생성기 함수

```python
def stream_response(user_input: str, location: str = "홍대"):
    """LangGraph 스트리밍 실행 결과를 토큰 단위로 yield합니다."""
    initial_state = {
        "user_input": user_input,
        "location": location
    }
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    try:
        for event in graph.stream(initial_state, config):
            # 각 노드 실행 결과를 순서대로 처리
            for node_name, node_output in event.items():
                if node_name == "summarize_message":
                    # 최종 메시지만 스트리밍 출력
                    final_msg = node_output.get("final_message", "")
                    if final_msg:
                        # 단어 단위로 나눠서 yield (간단한 스트리밍 시뮬레이션)
                        for word in final_msg.split(" "):
                            yield word + " "
    except Exception:
        yield "죄송해요, 오류가 발생했습니다. 다시 시도해 주세요. 😊"
```

### LangGraph stream 이벤트 구조 이해

```python
# graph.stream()은 각 노드 실행마다 딕셔너리를 yield합니다
for event in graph.stream(initial_state):
    # event 예시: {"classify_intent": {"intent": "food"}}
    node_name = list(event.keys())[0]
    node_output = event[node_name]
    print(f"[{node_name}] 완료: {node_output}")
```

> ⚠️ 실제 OpenAI API의 토큰 수준 스트리밍을 구현하려면 `ChatOpenAI(streaming=True)`와 함께  
> `astream_events()` 메서드를 활용해야 합니다. 위 코드는 노드 단위 스트리밍입니다.

---

<a id="part5"></a>

## 5️⃣ 배포하기 [↑](#toc)

### 로컬 실행

```bash
# 가상환경 활성화 후 실행
streamlit run app.py
```

실행 후 브라우저에서 `http://localhost:8501`로 접속합니다.

### requirements.txt 작성

배포 전에 의존 패키지를 명시한 `requirements.txt`를 작성합니다.

```text
# requirements.txt
langchain>=0.2.0
langchain-openai>=0.1.0
langchain-community>=0.2.0
langgraph>=0.1.0
streamlit>=1.35.0
python-dotenv>=1.0.0
requests>=2.31.0
```

```bash
# 현재 환경의 패키지 목록을 자동으로 생성하려면
pip freeze > requirements.txt
```

> ⚠️ `pip freeze`로 생성한 파일에는 불필요한 패키지가 많이 포함될 수 있습니다.  
> 직접 필요한 패키지만 명시하는 것을 권장합니다.

### secrets.toml 설정 (Streamlit Cloud용 환경변수)

로컬에서는 `.env` 파일을 사용하지만, Streamlit Cloud 배포 시에는 `secrets.toml` 또는 대시보드의 Secrets 설정을 사용합니다.

```toml
# .streamlit/secrets.toml  (로컬 테스트용, .gitignore에 추가 필수!)
OPENAI_API_KEY = "sk-..."
TAVILY_API_KEY = "tvly-..."
KAKAO_API_KEY = "..."
WEATHER_API_KEY = "..."
```

코드에서 secrets에 접근하는 방법:

```python
import streamlit as st

# Streamlit Secrets 접근 (Cloud 배포 시)
openai_key = st.secrets["OPENAI_API_KEY"]

# 또는 환경변수와 동시 지원
import os
openai_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
```

### Streamlit Community Cloud 배포 단계

**사전 준비:**
- GitHub 계정
- 프로젝트 코드가 GitHub 저장소에 push된 상태

**배포 절차:**

1. **GitHub에 코드 push**

```bash
git add .
git commit -m "Add Streamlit app"
git push origin main
```

2. **share.streamlit.io 접속**  
   [https://share.streamlit.io](https://share.streamlit.io)에 접속하여 GitHub 계정으로 로그인합니다.

3. **새 앱 배포**  
   - `New app` 버튼 클릭  
   - Repository: 본인의 GitHub 저장소 선택  
   - Branch: `main`  
   - Main file path: `app.py`  
   - `Deploy!` 클릭

4. **Secrets 설정**  
   배포 화면 또는 앱 설정(`⋮` → Settings → Secrets)에서 API 키를 입력합니다.

```
OPENAI_API_KEY = "sk-..."
TAVILY_API_KEY = "tvly-..."
KAKAO_API_KEY = "..."
WEATHER_API_KEY = "..."
```

5. **배포 완료**  
   배포가 완료되면 `https://[username]-[appname].streamlit.app` 형태의 URL이 생성됩니다.

> 💡 Streamlit Community Cloud는 **무료**로 사용할 수 있습니다.  
> 단, 무료 플랜에서는 일정 시간 접속이 없으면 앱이 잠자기 상태(sleep)로 전환됩니다.

---

<a id="part6"></a>

## 6️⃣ 배포 후 확인 [↑](#toc)

### 배포된 URL 접속 확인

배포 직후에는 다음을 확인합니다.

- 앱이 정상적으로 실행되는지 확인
- 챗봇에 "배고파"를 입력했을 때 추천 결과가 나오는지 확인
- API 키가 올바르게 설정되어 있는지 확인 (오류 메시지 없음)

### 모바일 반응형 확인

Streamlit은 기본적으로 반응형 디자인을 지원합니다.  
스마트폰 브라우저에서 접속하여 다음을 확인합니다.

- 채팅 입력창이 하단에 고정되어 있는지
- 추천 카드가 세로로 쌓여서 표시되는지 (모바일에서는 가로 배치가 좁을 수 있음)
- 사이드바가 접혀서 메뉴 버튼으로 표시되는지

> 💡 모바일 최적화를 위해 `st.set_page_config(layout="centered")`를 사용하면  
> 콘텐츠가 중앙에 적절한 너비로 표시됩니다.

### 에러 로그 확인 방법

#### Streamlit Cloud 로그

1. [share.streamlit.io](https://share.streamlit.io) 접속
2. 배포된 앱 선택
3. 우상단 `⋮` 메뉴 → **Manage app** 클릭
4. 하단 **Logs** 탭에서 실시간 로그 확인

#### 주요 에러 유형과 해결책

| 에러 메시지 | 원인 | 해결책 |
|------------|------|--------|
| `ModuleNotFoundError` | requirements.txt에 패키지 누락 | requirements.txt에 패키지 추가 후 재배포 |
| `KeyError: 'OPENAI_API_KEY'` | Secrets 미설정 | 앱 설정에서 API 키 입력 |
| `openai.AuthenticationError` | 잘못된 API 키 | 올바른 API 키로 교체 |
| `ConnectionError` | 외부 API 접속 실패 | 잠시 후 재시도 또는 API 서버 상태 확인 |

---

<a id="part7"></a>

## 7️⃣ 정리 [↑](#toc)

### 전체 과정 회고 (1장 → 17장 여정 요약)

이 과정에서 우리는 다음 여정을 함께 걸었습니다.

| 장 | 내용 |
|----|------|
| 1~2장 | LangGraph 소개 및 개발 환경 구축 |
| 3장 | 기본 개념: 상태(State), 노드(Node), 엣지(Edge) |
| 4~7장 | 채팅봇 구현: 도구 사용, 메모리, Human-in-the-loop |
| 8~9장 | 실전 프로젝트: "뭐 먹지? 뭐 하지?" 설계 및 구현 |
| 10~12장 | 서브그래프, 멀티 에이전트, 비동기 처리 |
| 13~14장 | 스트리밍, 에러 처리 |
| 15~16장 | 프로젝트 완성: 10개 에이전트 그래프 통합 |
| 17장 | Streamlit UI 구현 및 배포 |

### 다음 단계로: 학습 경로

이 과정을 마친 후 도전해볼 수 있는 주제들입니다.

#### LangGraph Platform (클라우드 배포)
- LangGraph의 공식 배포 플랫폼
- 그래프를 API 서버로 자동 배포
- 실시간 모니터링, 스레드 관리, 재실행 기능 제공
- [langchain-ai.github.io/langgraph/cloud](https://langchain-ai.github.io/langgraph/cloud/)

#### LangSmith (모니터링/평가)
- LangGraph 및 LangChain 실행을 추적하고 디버깅하는 도구
- 각 노드의 입출력, 실행 시간, 비용을 시각적으로 확인
- A/B 테스트 및 프롬프트 평가 기능

```python
# LangSmith 연동 (환경변수 설정으로 자동 활성화)
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls-..."
os.environ["LANGCHAIN_PROJECT"] = "뭐-먹지-프로젝트"
```

#### 멀티모달 에이전트 (이미지/음성)
- 사진을 찍으면 음식을 인식하고 추천해주는 비전 에이전트
- 음성 입력(`Whisper API`)으로 "배고파"를 말하면 동작하는 음성 에이전트
- GPT-4o의 비전 기능과 LangGraph를 결합하는 방법

#### MCP (Model Context Protocol)
- Anthropic이 제안한 AI 에이전트 표준 프로토콜
- 다양한 도구(Tool)와 데이터 소스를 표준화된 방식으로 연결
- LangGraph 에이전트를 MCP 서버로 배포하는 방법

---

### 학습 체크리스트

이 과정을 모두 마쳤다면 아래 항목을 점검해보세요.

- [ ] LangGraph의 State, Node, Edge, Conditional Edge 개념을 설명할 수 있다
- [ ] `StateGraph`를 사용하여 멀티 에이전트 그래프를 직접 설계할 수 있다
- [ ] LangGraph 그래프를 Mermaid로 시각화하고 흐름을 파악할 수 있다
- [ ] OpenAI API를 활용한 LLM 노드를 구현할 수 있다
- [ ] 외부 API(날씨, 지도)를 LangGraph 노드로 통합할 수 있다
- [ ] Streamlit으로 LangGraph 챗봇 UI를 만들 수 있다
- [ ] Streamlit Community Cloud에 앱을 배포할 수 있다
- [ ] `get_openai_callback`으로 API 비용을 추적할 수 있다

---

### 🎯 실습 미션

이 과정을 마무리하는 최종 미션입니다.

**미션: 나만의 추천 챗봇 완성하기**

1. "뭐 먹지? 뭐 하지?" 프로젝트를 본인의 GitHub 저장소에 push합니다.
2. Streamlit Community Cloud에 배포합니다.
3. 배포된 앱 URL을 확인하고 모바일에서도 동작하는지 테스트합니다.
4. 아래 확장 중 하나를 직접 구현해봅니다:
   - "다른 거 추천해줘"를 입력했을 때 다른 추천을 주는 대화형 흐름
   - 사용자 피드백(👍/👎)을 수집하는 버튼 추가
   - 추천 히스토리를 CSV로 저장하는 기능

---

이 과정을 모두 마쳤습니다. 축하합니다! 🎉

LangGraph와 Streamlit을 함께 활용하여 실제로 동작하는 AI 서비스를 처음부터 끝까지 만들어보았습니다.  
배운 개념과 패턴을 바탕으로 나만의 에이전트 서비스를 만들어보세요.

> 💡 학습 과정에서 만든 코드는 포트폴리오로 활용할 수 있습니다.  
> README.md에 시스템 구조도(Mermaid)와 사용법을 잘 정리해두면 더욱 좋습니다.
