---
title: "14. 프로덕션 준비"
layout: default
grand_parent: LLM
parent: LangGraph
nav_order: 14
permalink: /llm/langgraph/production
---
# 프로덕션 준비

지금까지 LangGraph로 에이전트를 만들고 실행해봤습니다. 이번 장에서는 실제 서비스에 배포할 때 고려해야 할 **프로덕션 준비** 사항들을 살펴봅니다. 체크포인터 선택, 비용 모니터링, 테스트 전략, 로깅, 보안까지 한 번에 다룹니다.

<a id="toc"></a>

## 진행 순서

1. [프로덕션 체크포인터](#part1)
2. [비용과 성능 모니터링](#part2)
3. [테스트 전략](#part3)
4. [로깅과 디버깅](#part4)
5. [보안 고려사항](#part5)
6. [실습: 테스트 스위트 작성](#part6)
7. [정리](#part7)

---

<a id="part1"></a>

## 1️⃣ 프로덕션 체크포인터 [↑](#toc)

### 체크포인터 진화 경로

LangGraph에서 **체크포인터(Checkpointer)**는 그래프 실행 상태를 저장하는 역할을 합니다. 개발 단계에서 운영 단계로 올라갈수록 더 견고한 저장소가 필요합니다.

```
InMemorySaver  →  SqliteSaver  →  PostgresSaver
(개발/테스트)     (소규모 운영)    (대규모 운영)
```

| 단계 | 체크포인터 | 특징 |
|------|-----------|------|
| 개발/테스트 | `InMemorySaver` | 메모리 저장, 재시작 시 초기화 |
| 소규모 운영 | `SqliteSaver` | 파일 기반, 단일 서버에 적합 |
| 대규모 운영 | `PostgresSaver` | DB 기반, 멀티 서버, 고가용성 |

### InMemorySaver (개발용)

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
graph = graph_builder.compile(checkpointer=checkpointer)
```

- 프로세스 재시작 시 모든 대화 기록이 사라집니다.
- 빠른 프로토타이핑과 테스트에 적합합니다.
- 멀티 프로세스 환경에서는 사용 불가합니다.

### SqliteSaver (소규모 운영)

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# SQLite 파일 경로 지정
with SqliteSaver.from_conn_string("./checkpoints.db") as checkpointer:
    graph = graph_builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "user_123"}}
    result = graph.invoke({"messages": [HumanMessage(content="안녕")]}, config)
```

- 단일 SQLite 파일에 모든 상태가 저장됩니다.
- 서버 재시작 후에도 대화 기록이 유지됩니다.
- 동시 접속자가 많으면 성능이 저하될 수 있습니다.
- 소규모 프로젝트나 1인 서비스에 적합합니다.

> 💡 **Tip:** SQLite는 쓰기 락(write lock) 때문에 동시에 여러 요청을 처리하면 병목이 생깁니다. 사용자가 수십 명 이하인 환경에서 사용하세요.

### PostgresSaver (대규모 운영)

프로덕션 수준의 동시 접속과 고가용성이 필요하다면 PostgreSQL을 사용합니다.

먼저 패키지를 설치합니다:
```bash
uv add langgraph-checkpoint-postgres psycopg[binary]
```

```python
from langgraph.checkpoint.postgres import PostgresSaver
import psycopg

DB_URI = "postgresql://user:password@localhost:5432/langgraph"

with psycopg.connect(DB_URI) as conn:
    checkpointer = PostgresSaver(conn)
    checkpointer.setup()  # 체크포인트 테이블 자동 생성
    graph = graph_builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "user_456"}}
    result = graph.invoke(
        {"messages": [HumanMessage(content="오늘 날씨 어때?")]},
        config
    )
```

- `checkpointer.setup()`: 처음 한 번만 실행하면 필요한 테이블이 자동으로 생성됩니다.
- 연결 풀(connection pool)을 사용하면 성능이 더 좋아집니다.
- 여러 서버 인스턴스가 같은 DB를 공유할 수 있습니다.

#### 연결 풀 사용 (권장)

```python
from psycopg_pool import ConnectionPool

DB_URI = "postgresql://user:password@localhost:5432/langgraph"

connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}

with ConnectionPool(
    conninfo=DB_URI,
    max_size=20,
    kwargs=connection_kwargs,
) as pool:
    checkpointer = PostgresSaver(pool)
    checkpointer.setup()
    graph = graph_builder.compile(checkpointer=checkpointer)
```

### 체크포인터 비교 표

| 항목 | InMemorySaver | SqliteSaver | PostgresSaver |
|------|:---:|:---:|:---:|
| 재시작 후 유지 | ❌ | ✅ | ✅ |
| 별도 설치 필요 | ❌ | ❌ | ✅ |
| 동시 접속 | 제한적 | 낮음 | 높음 |
| 멀티 서버 지원 | ❌ | ❌ | ✅ |
| 운영 환경 권장 | 개발만 | 소규모 | 중·대규모 |
| 설정 복잡도 | 낮음 | 낮음 | 중간 |

> ⚠️ **주의:** 운영 환경의 DB 비밀번호는 절대 코드에 직접 쓰지 마세요. 환경 변수나 시크릿 매니저를 사용하세요. 자세한 내용은 [5️⃣ 보안 고려사항](#part5)에서 다룹니다.

---

<a id="part2"></a>

## 2️⃣ 비용과 성능 모니터링 [↑](#toc)

LLM API는 사용량에 따라 비용이 발생합니다. 운영 환경에서는 **얼마나 썼는지**, **어디서 느린지**를 파악하는 것이 중요합니다.

### 토큰 카운팅 패턴

`langchain_community`의 콜백을 사용하면 호출 한 번으로 토큰 사용량과 비용을 자동 집계할 수 있습니다.

먼저 패키지를 설치합니다:
```bash
uv add langchain-community
```

```python
from langchain_community.callbacks import get_openai_callback

config = {"configurable": {"thread_id": "cost_test_1"}}

with get_openai_callback() as cb:
    result = graph.invoke(
        {"messages": [HumanMessage(content="대전 맛집 추천해줘")]},
        config
    )
    print(f"총 토큰: {cb.total_tokens}")
    print(f"입력 토큰: {cb.prompt_tokens}")
    print(f"출력 토큰: {cb.completion_tokens}")
    print(f"LLM 호출 횟수: {cb.successful_requests}")
    print(f"비용: ${cb.total_cost:.4f}")
```

출력 예시:
```
총 토큰: 1245
입력 토큰: 987
출력 토큰: 258
LLM 호출 횟수: 3
비용: $0.0003
```

### 노드별 실행 시간 측정

LangGraph의 스트리밍 모드를 활용하면 각 노드의 실행 시간을 측정할 수 있습니다.

```python
import time

node_times = {}

for event in graph.stream(
    {"messages": [HumanMessage(content="서울 카페 추천")]},
    config,
    stream_mode="updates"
):
    for node_name, update in event.items():
        if node_name not in node_times:
            node_times[node_name] = {"start": time.time(), "end": None}
        else:
            node_times[node_name]["end"] = time.time()

# 결과 출력
for node, times in node_times.items():
    if times["end"]:
        elapsed = times["end"] - times["start"]
        print(f"{node}: {elapsed:.3f}초")
```

또는 `time` 모듈을 래핑하는 방식으로 노드 함수를 계측할 수 있습니다:

```python
import time
import functools

def timed_node(func):
    """노드 함수의 실행 시간을 측정하는 데코레이터"""
    @functools.wraps(func)
    def wrapper(state):
        start = time.perf_counter()
        result = func(state)
        elapsed = time.perf_counter() - start
        print(f"[{func.__name__}] 실행 시간: {elapsed:.3f}초")
        return result
    return wrapper

@timed_node
def chatbot_node(state):
    ai_response = llm_with_tools.invoke(state["messages"])
    return {"messages": [ai_response]}
```

### 비용 최적화 팁

| 방법 | 설명 | 절약 효과 |
|------|------|-----------|
| 작은 모델 선택 | `gpt-4o` → `gpt-4o-mini` | 최대 15배 절약 |
| 프롬프트 간소화 | 불필요한 지시문 제거 | 10~30% 절약 |
| 결과 캐싱 | 동일 질문에 LLM 재호출 방지 | 반복 쿼리에 효과적 |
| 메시지 트리밍 | 오래된 메시지 요약 또는 삭제 | 컨텍스트가 길수록 효과적 |
| 스트리밍 활용 | 사용자 체감 속도 향상 | 비용은 동일, UX 개선 |

### API별 예상 비용 (2024년 기준)

| API | 단가 | 월 1,000회 기준 |
|-----|------|----------------|
| GPT-4o-mini (입력) | $0.15 / 1M 토큰 | ~$0.15 |
| GPT-4o-mini (출력) | $0.60 / 1M 토큰 | ~$0.30 |
| GPT-4o (입력) | $2.50 / 1M 토큰 | ~$2.50 |
| Tavily Search | $5 / 1,000회 | $5.00 |
| OpenWeather (무료 플랜) | 무료 (1,000회/일) | $0 |
| Kakao API (무료 플랜) | 무료 | $0 |

> 💡 **Tip:** 개발 초반에는 `gpt-4o-mini`로 모든 기능을 검증하고, 품질이 부족한 특정 노드에만 `gpt-4o`를 사용하는 전략이 비용 대비 효율적입니다.

---

<a id="part3"></a>

## 3️⃣ 테스트 전략 [↑](#toc)

LLM 기반 에이전트는 출력이 비결정적이기 때문에 테스트가 까다롭습니다. 하지만 체계적인 전략으로 신뢰성을 높일 수 있습니다.

### 테스트 계층

```
단위 테스트 (Unit)   →  빠름, 저렴, 결정적
통합 테스트 (Integration)  →  중간, 실제 흐름 검증
E2E 테스트 (End-to-End)  →  느림, 비용 발생, 전체 검증
```

### 단위 테스트: 개별 노드 함수 테스트

노드 함수는 `state` 딕셔너리를 받아 딕셔너리를 반환하는 순수한 함수입니다. LLM 없이 로직만 테스트하거나, LLM을 모킹하여 결정적으로 테스트할 수 있습니다.

```python
# test_nodes.py
import pytest
from langchain_core.messages import HumanMessage, AIMessage

def test_classify_intent():
    """의도 분류 노드 단위 테스트"""
    state = {"messages": [HumanMessage(content="치킨 먹고 싶어")]}
    result = classify_intent(state)
    assert "intent" in result
    assert result["intent"] in ["food", "activity", "weather"]

def test_classify_intent_weather():
    """날씨 관련 의도 분류 테스트"""
    state = {"messages": [HumanMessage(content="오늘 서울 날씨 어때?")]}
    result = classify_intent(state)
    assert result["intent"] == "weather"
    assert result.get("place") == "서울"

def test_weather_node_mock_data():
    """날씨 노드: API 키 없을 때 모의 데이터 반환 확인"""
    state = {"place": "대전", "messages": []}
    result = weather_node(state)
    assert "weather" in result
    assert result["weather"]["city"] == "대전"
    assert isinstance(result["weather"]["temperature"], float)
```

### LLM 모킹: 결정적 테스트

LLM 호출을 `unittest.mock`으로 교체하면 비용 없이 빠르게 테스트할 수 있습니다.

```python
# test_with_mock.py
import json
import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage

def test_classify_intent_with_mock():
    """LLM을 모킹하여 의도 분류 테스트"""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = AIMessage(
        content='{"intent": "food", "place": "대전"}'
    )

    with patch("your_module.llm", mock_llm):
        state = {"messages": [HumanMessage(content="대전 맛집 알려줘")]}
        result = classify_intent_node(state)

    assert result["intent"] == "food"
    assert result["place"] == "대전"
    mock_llm.invoke.assert_called_once()   # LLM이 정확히 한 번 호출됐는지 확인

def test_chatbot_node_with_mock():
    """챗봇 노드 모킹 테스트"""
    mock_response = AIMessage(content="안녕하세요! 무엇을 도와드릴까요?")
    mock_llm_with_tools = MagicMock()
    mock_llm_with_tools.invoke.return_value = mock_response

    with patch("your_module.llm_with_tools", mock_llm_with_tools):
        state = {"messages": [HumanMessage(content="안녕")]}
        result = chatbot_node(state)

    assert len(result["messages"]) == 1
    assert result["messages"][0].content == "안녕하세요! 무엇을 도와드릴까요?"
```

### 통합 테스트: 전체 그래프 실행

```python
# test_integration.py
import pytest
from langchain_core.messages import HumanMessage

@pytest.mark.integration
def test_full_graph_food_query():
    """음식 관련 질문에 대한 전체 그래프 실행 테스트"""
    from langgraph.checkpoint.memory import MemorySaver

    checkpointer = MemorySaver()
    graph = build_graph(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "test_food_1"}}
    result = graph.invoke(
        {"messages": [HumanMessage(content="대전 빵집 추천해줘")],
         "search_results": []},
        config
    )

    # 마지막 메시지가 AI 응답인지 확인
    last_message = result["messages"][-1]
    assert hasattr(last_message, "content")
    assert len(last_message.content) > 0

    # 검색이 수행됐는지 확인 (search_query가 설정됨)
    assert result.get("search_query") is not None
```

### pytest fixture 패턴

공통적으로 사용하는 객체는 `conftest.py`의 fixture로 관리합니다.

```python
# conftest.py
import pytest
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import MemorySaver

@pytest.fixture
def mock_llm():
    """기본 모의 LLM fixture"""
    llm = MagicMock()
    llm.invoke.return_value = AIMessage(content='{"intent": "food", "place": "서울"}')
    return llm

@pytest.fixture
def memory_checkpointer():
    """테스트용 인메모리 체크포인터"""
    return MemorySaver()

@pytest.fixture
def test_config():
    """테스트용 그래프 설정"""
    return {"configurable": {"thread_id": "test_thread_001"}}

@pytest.fixture
def sample_food_state():
    """음식 추천 테스트용 초기 상태"""
    from langchain_core.messages import HumanMessage
    return {
        "messages": [HumanMessage(content="서울 파스타 맛집 추천해줘")],
        "search_results": [],
        "intent": None,
        "search_query": None,
        "place": None,
        "weather": None,
    }
```

---

<a id="part4"></a>

## 4️⃣ 로깅과 디버깅 [↑](#toc)

### LangGraph 디버그 모드

그래프 실행 시 `debug=True`를 설정하면 각 노드의 입출력이 상세하게 출력됩니다.

```python
# 디버그 모드로 실행
result = graph.invoke(
    {"messages": [HumanMessage(content="대전 카페 알려줘")]},
    config,
    debug=True   # 상세 로그 출력
)
```

출력 예시:
```
[langgraph] Entering node: chatbot
[langgraph] State input: {'messages': [HumanMessage(content='대전 카페 알려줘')]}
[langgraph] Entering node: tools
...
[langgraph] Exiting node: chatbot
```

### 구조화된 로깅

운영 환경에서는 `print` 대신 `logging` 모듈을 사용하여 로그 레벨과 포맷을 제어합니다.

```python
import logging

# 로거 기본 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("langgraph.agent")

def chatbot_node(state):
    logger.info("chatbot_node 시작 - 메시지 수: %d", len(state["messages"]))
    ai_response = llm_with_tools.invoke(state["messages"])
    if ai_response.tool_calls:
        logger.info("도구 호출 요청: %s", [tc["name"] for tc in ai_response.tool_calls])
    else:
        logger.info("최종 응답 생성 완료")
    return {"messages": [ai_response]}

def weather_node(state):
    city = state.get("place", "서울")
    logger.info("날씨 조회 요청 - 도시: %s", city)
    weather = get_weather(city)
    logger.info("날씨 조회 완료 - %s: %s, %.1f°C",
                weather["city"], weather["condition"], weather["temperature"])
    return {"weather": weather}
```

### 상태 스냅샷 디버깅

체크포인터가 설정된 그래프에서는 `get_state()`로 현재 저장된 상태를 확인할 수 있습니다.

```python
config = {"configurable": {"thread_id": "debug_session_1"}}

# 그래프 실행
graph.invoke(
    {"messages": [HumanMessage(content="부산 횟집 알려줘")]},
    config
)

# 저장된 상태 스냅샷 확인
snapshot = graph.get_state(config)
print("현재 상태:")
print(f"  메시지 수: {len(snapshot.values['messages'])}")
print(f"  검색 의도: {snapshot.values.get('intent')}")
print(f"  검색 키워드: {snapshot.values.get('search_query')}")
print(f"  날씨 정보: {snapshot.values.get('weather')}")
print(f"  검색 결과 수: {len(snapshot.values.get('search_results', []))}")

# 상태 히스토리 확인
for i, state in enumerate(graph.get_state_history(config)):
    print(f"\n스냅샷 {i}: {state.metadata}")
```

### 일반적인 디버깅 체크리스트

그래프가 예상대로 동작하지 않을 때 순서대로 확인해보세요:

1. **노드가 실행되고 있는가?**
   - `debug=True`로 실행하여 각 노드 진입/퇴장 로그를 확인합니다.

2. **상태가 올바르게 전달되는가?**
   - 각 노드 함수 내에서 `logger.info` 또는 `print`로 입력 상태를 출력해봅니다.

3. **조건부 엣지가 올바른 노드로 향하는가?**
   - `tools_condition` 또는 커스텀 라우터 함수의 반환값을 로깅합니다.

4. **API 키가 올바르게 로드됐는가?**
   - `os.getenv("OPENAI_API_KEY")` 등을 직접 출력해봅니다.

5. **LLM 응답이 예상 형식인가?**
   - JSON을 파싱하는 노드라면 파싱 전 `response.content`를 출력합니다.

6. **도구 함수가 올바른 값을 반환하는가?**
   - 도구 함수를 독립적으로 직접 호출하여 반환값을 확인합니다.

---

<a id="part5"></a>

## 5️⃣ 보안 고려사항 [↑](#toc)

### API 키 관리

API 키가 외부에 노출되면 예상치 못한 비용이 발생하거나 서비스가 악용될 수 있습니다.

**절대 하지 말 것:**
```python
# ❌ 코드에 직접 입력 - 절대 금지
openai_client = ChatOpenAI(api_key="sk-proj-1234abcd...")

# ❌ 공개 저장소에 .env 파일 커밋 - 절대 금지
# git add .env  → 이렇게 하지 마세요
```

**올바른 방법:**
```python
# ✅ 환경 변수 사용
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 로드
api_key = os.getenv("OPENAI_API_KEY")

# .env 파일은 .gitignore에 추가
# .gitignore 내용:
# .env
# .env.local
# *.env
```

`.gitignore` 설정:
```
# API 키 파일
.env
.env.local
.env.production
*.env

# 데이터베이스 파일
*.db
*.sqlite
checkpoints.db
```

### 입력 검증

사용자 입력을 그대로 LLM에 전달하면 **프롬프트 인젝션** 공격이 발생할 수 있습니다.

```python
MAX_INPUT_LENGTH = 500  # 최대 입력 길이

def validate_user_input(user_input: str) -> str:
    """사용자 입력을 검증하고 정제합니다."""
    # 길이 제한
    if len(user_input) > MAX_INPUT_LENGTH:
        raise ValueError(f"입력이 너무 깁니다. 최대 {MAX_INPUT_LENGTH}자까지 허용됩니다.")

    # 위험 패턴 감지 (간단한 예시)
    dangerous_patterns = [
        "ignore previous instructions",
        "이전 지시를 무시",
        "system prompt",
        "당신은 이제",
    ]
    lower_input = user_input.lower()
    for pattern in dangerous_patterns:
        if pattern.lower() in lower_input:
            raise ValueError("허용되지 않는 입력 패턴이 감지되었습니다.")

    return user_input.strip()

# 사용 예시
try:
    safe_input = validate_user_input(user_message)
    state = {"messages": [HumanMessage(content=safe_input)]}
    result = graph.invoke(state, config)
except ValueError as e:
    print(f"입력 오류: {e}")
```

### Rate Limiting (요청 속도 제한)

운영 환경에서 특정 사용자가 너무 많은 요청을 보내면 비용이 급증하고 다른 사용자의 서비스가 저하됩니다.

```python
from collections import defaultdict
from datetime import datetime, timedelta

# 간단한 인메모리 Rate Limiter
request_counts = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 10

def check_rate_limit(user_id: str) -> bool:
    """사용자별 분당 요청 횟수를 확인합니다."""
    now = datetime.now()
    minute_ago = now - timedelta(minutes=1)

    # 1분 이내 요청 필터링
    request_counts[user_id] = [
        t for t in request_counts[user_id] if t > minute_ago
    ]

    if len(request_counts[user_id]) >= MAX_REQUESTS_PER_MINUTE:
        return False  # 한도 초과

    request_counts[user_id].append(now)
    return True  # 허용

# 사용 예시
user_id = "user_123"
if not check_rate_limit(user_id):
    print("요청이 너무 많습니다. 잠시 후 다시 시도해주세요.")
else:
    result = graph.invoke(state, config)
```

> ⚠️ **주의:** 위 Rate Limiter는 단일 프로세스에서만 동작합니다. 멀티 서버 환경에서는 Redis 같은 공유 저장소를 사용하세요.

---

<a id="part6"></a>

## 6️⃣ 실습: 테스트 스위트 작성 [↑](#toc)

이전 장에서 만든 **음식/활동 추천 에이전트**의 핵심 노드 3개에 대해 pytest 테스트를 작성해봅니다.

### 프로젝트 구조

```
my_agent/
├── agent.py          # 그래프 정의
├── nodes.py          # 노드 함수 모음
├── conftest.py       # pytest 공통 설정
├── test_nodes.py     # 노드 단위 테스트
├── test_integration.py  # 통합 테스트
└── .env              # API 키 (git에 올리지 않음)
```

### conftest.py 설정

```python
# conftest.py
import pytest
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver

@pytest.fixture(scope="session")
def mock_llm_food():
    """음식 추천 응답용 모의 LLM"""
    llm = MagicMock()
    llm.invoke.return_value = AIMessage(
        content='{"intent": "food", "place": "서울"}'
    )
    return llm

@pytest.fixture(scope="session")
def mock_llm_activity():
    """활동 추천 응답용 모의 LLM"""
    llm = MagicMock()
    llm.invoke.return_value = AIMessage(
        content='{"intent": "activity", "place": "부산"}'
    )
    return llm

@pytest.fixture
def memory_saver():
    """각 테스트마다 새 MemorySaver 생성"""
    return MemorySaver()

@pytest.fixture
def base_state():
    """기본 빈 상태"""
    return {
        "messages": [],
        "intent": None,
        "search_query": None,
        "place": None,
        "weather": None,
        "search_results": [],
    }
```

### test_nodes.py: 노드 단위 테스트

```python
# test_nodes.py
import pytest
import json
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage

class TestClassifyIntentNode:
    """의도 분류 노드 테스트"""

    def test_food_intent(self, mock_llm_food, base_state):
        """음식 관련 질문은 food 의도로 분류돼야 함"""
        base_state["messages"] = [HumanMessage(content="파스타 맛집 알려줘")]
        with patch("nodes.llm", mock_llm_food):
            from nodes import classify_intent_node
            result = classify_intent_node(base_state)
        assert result["intent"] == "food"

    def test_activity_intent(self, mock_llm_activity, base_state):
        """활동 관련 질문은 activity 의도로 분류돼야 함"""
        base_state["messages"] = [HumanMessage(content="부산 여행 뭐 할까?")]
        with patch("nodes.llm", mock_llm_activity):
            from nodes import classify_intent_node
            result = classify_intent_node(base_state)
        assert result["intent"] == "activity"

    def test_place_extraction(self, mock_llm_food, base_state):
        """장소명이 올바르게 추출돼야 함"""
        base_state["messages"] = [HumanMessage(content="서울 떡볶이 맛집")]
        with patch("nodes.llm", mock_llm_food):
            from nodes import classify_intent_node
            result = classify_intent_node(base_state)
        assert result.get("place") is not None


class TestWeatherNode:
    """날씨 노드 테스트"""

    def test_weather_returns_weatherinfo(self, base_state):
        """날씨 노드는 WeatherInfo 딕셔너리를 반환해야 함"""
        base_state["place"] = "서울"
        from nodes import weather_node
        result = weather_node(base_state)
        assert "weather" in result
        assert "city" in result["weather"]
        assert "temperature" in result["weather"]
        assert "condition" in result["weather"]

    def test_weather_default_city(self, base_state):
        """place가 없으면 기본값 '서울'을 사용해야 함"""
        base_state["place"] = None
        from nodes import weather_node
        result = weather_node(base_state)
        assert result["weather"]["city"] in ["서울", "Seoul"]

    def test_weather_temperature_is_float(self, base_state):
        """온도는 float 타입이어야 함"""
        base_state["place"] = "대전"
        from nodes import weather_node
        result = weather_node(base_state)
        assert isinstance(result["weather"]["temperature"], float)


class TestResponseNode:
    """응답 생성 노드 테스트"""

    def test_response_adds_ai_message(self, base_state):
        """응답 노드는 AIMessage를 messages에 추가해야 함"""
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(content="오늘 날씨 좋네요! 카페 추천해드릴게요.")
        base_state["messages"] = [HumanMessage(content="서울 카페 추천해줘")]
        base_state["weather"] = {"city": "서울", "temperature": 22.0, "condition": "맑음"}
        base_state["search_results"] = [{"name": "스타벅스", "address": "서울 강남", "url": ""}]

        with patch("nodes.llm", mock_llm):
            from nodes import response_node
            result = response_node(base_state)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], AIMessage)
```

### test_integration.py: 통합 테스트

```python
# test_integration.py
import pytest
from langchain_core.messages import HumanMessage, AIMessage

@pytest.mark.integration
class TestFullGraph:
    """전체 그래프 통합 테스트 (실제 API 호출 없음 - 모킹 사용)"""

    def test_graph_completes_successfully(self, memory_saver):
        """그래프가 오류 없이 완료돼야 함"""
        from unittest.mock import patch, MagicMock

        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(
            content='{"intent": "food", "place": "서울"}'
        )
        mock_llm.bind_tools.return_value = mock_llm

        with patch("agent.llm", mock_llm):
            from agent import build_graph
            graph = build_graph(checkpointer=memory_saver)
            config = {"configurable": {"thread_id": "integration_test_1"}}
            result = graph.invoke(
                {"messages": [HumanMessage(content="서울 맛집")],
                 "search_results": []},
                config
            )

        assert "messages" in result
        assert len(result["messages"]) >= 1

    def test_conversation_state_persists(self, memory_saver):
        """두 번째 메시지에서도 이전 대화가 유지돼야 함"""
        from unittest.mock import patch, MagicMock

        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(content="네, 알겠습니다.")
        mock_llm.bind_tools.return_value = mock_llm

        with patch("agent.llm", mock_llm):
            from agent import build_graph
            graph = build_graph(checkpointer=memory_saver)
            config = {"configurable": {"thread_id": "persist_test_1"}}

            # 첫 번째 메시지
            graph.invoke(
                {"messages": [HumanMessage(content="안녕")],
                 "search_results": []},
                config
            )
            # 두 번째 메시지
            result = graph.invoke(
                {"messages": [HumanMessage(content="서울 카페")],
                 "search_results": []},
                config
            )

        # 두 번째 실행 후에도 누적된 메시지가 있어야 함
        assert len(result["messages"]) >= 2
```

### 실행 방법

```bash
# 전체 테스트 실행
uv run pytest -v

# 단위 테스트만 실행
uv run pytest test_nodes.py -v

# 통합 테스트 제외
uv run pytest -v -m "not integration"

# 특정 클래스만 실행
uv run pytest test_nodes.py::TestWeatherNode -v

# 커버리지 포함
uv run pytest --cov=nodes --cov-report=term-missing
```

예상 출력:
```
test_nodes.py::TestClassifyIntentNode::test_food_intent PASSED
test_nodes.py::TestClassifyIntentNode::test_activity_intent PASSED
test_nodes.py::TestClassifyIntentNode::test_place_extraction PASSED
test_nodes.py::TestWeatherNode::test_weather_returns_weatherinfo PASSED
test_nodes.py::TestWeatherNode::test_weather_default_city PASSED
test_nodes.py::TestWeatherNode::test_temperature_is_float PASSED
test_nodes.py::TestResponseNode::test_response_adds_ai_message PASSED

7 passed in 0.45s
```

---

<a id="part7"></a>

## 7️⃣ 정리 [↑](#toc)

### 프로덕션 준비 체크리스트

배포 전 아래 항목을 모두 확인하세요:

- [ ] **체크포인터**: 운영 환경에 맞는 체크포인터 선택 (소규모: SqliteSaver, 대규모: PostgresSaver)
- [ ] **API 키**: 모든 키가 환경 변수로 관리되며 코드나 저장소에 노출되지 않음
- [ ] **입력 검증**: 사용자 입력 길이 제한 및 위험 패턴 필터링 구현
- [ ] **Rate Limiting**: 사용자별 분당 요청 횟수 제한 적용
- [ ] **로깅**: `logging` 모듈 설정, 중요 이벤트 로그 기록
- [ ] **에러 처리**: API 오류, 네트워크 오류, 파싱 오류에 대한 예외 처리
- [ ] **비용 모니터링**: `get_openai_callback`으로 토큰 사용량 추적
- [ ] **단위 테스트**: 각 노드 함수에 대한 테스트 작성 및 통과
- [ ] **통합 테스트**: 전체 그래프 실행 테스트 통과
- [ ] **.gitignore**: `.env`, `*.db`, `checkpoints.db` 등 민감 파일 제외

### 학습 체크리스트

이 장을 완료하면 다음 내용을 이해해야 합니다:

- [ ] InMemorySaver / SqliteSaver / PostgresSaver 각각의 용도와 차이를 설명할 수 있다.
- [ ] `get_openai_callback`으로 토큰 사용량과 비용을 측정하는 코드를 작성할 수 있다.
- [ ] `unittest.mock`으로 LLM을 모킹하여 결정적 테스트를 작성할 수 있다.
- [ ] `conftest.py`에서 pytest fixture를 정의하고 재사용할 수 있다.
- [ ] `logging` 모듈로 구조화된 로그를 남기는 코드를 작성할 수 있다.
- [ ] API 키를 안전하게 관리하는 방법을 설명할 수 있다.

### 🎯 실습 미션

**미션 1**: SqliteSaver 적용하기

이전에 만든 음식/활동 추천 에이전트에 `SqliteSaver`를 적용해보세요. 프로그램을 종료했다가 다시 실행해도 이전 대화가 이어지는지 확인하세요.

```python
# 힌트
from langgraph.checkpoint.sqlite import SqliteSaver

with SqliteSaver.from_conn_string("my_agent.db") as checkpointer:
    graph = build_graph(checkpointer=checkpointer)
    # thread_id를 동일하게 유지하면 대화가 이어집니다
    config = {"configurable": {"thread_id": "my_user_1"}}
```

**미션 2**: 비용 측정 래퍼 작성하기

`get_openai_callback`을 사용하여 그래프 한 번 실행에 드는 비용을 측정하는 함수를 작성하세요. 세 가지 다른 질문에 대해 비용을 비교하고, 어떤 질문이 가장 많은 토큰을 소비하는지 분석해보세요.

**미션 3**: 테스트 커버리지 80% 달성하기

앞서 배운 테스트 패턴을 참고하여 자신의 에이전트 코드에 대한 테스트를 작성하세요. `uv run pytest --cov=. --cov-report=term-missing` 명령으로 커버리지를 측정하고 80% 이상 달성하는 것을 목표로 합니다.

---

→ **다음 장**: [15. 프로젝트 정의서](/llm/langgraph/agent_proj)
