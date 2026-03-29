---
title: 7. Memory
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 7
permalink: /llm/langchain/memory
--- 
# LangChain 메모리
---

{: .warning }
> **v1.0 참고**: LangChain v1.0에서 `ConversationBufferMemory`, `ConversationSummaryMemory` 등 레거시 메모리 클래스는 `langchain-classic` 패키지로 이동되었습니다. 이 교안에서 실습하는 `RunnableWithMessageHistory`와 `InMemoryChatMessageHistory`는 **v1.0에서도 동일하게 사용**됩니다. 에이전트 수준의 메모리 관리는 [LangGraph](/langgraph)의 `MemorySaver`를 참고하세요.

## 1. 메모리의 개념

LangChain의 “메모리”는 LLM이 **이전 대화 맥락을 유지**하고 **상태를 관리**하도록 돕는 핵심 구성 요소  
최근 버전에서는 메모리가 **`ChatMessageHistory` 기반의 전통적 방식**과  
**LCEL(`RunnableWithMessageHistory`) 기반의 현대적 방식**으로 구분됩니다.

---

## 2. 기본 구성 요소

| 구성요소 | 설명 |
|-----------|------|
| **ChatMessageHistory** | 개별 대화의 과거 메시지를 저장하는 기본 클래스. 인메모리(InMemory), Redis, SQLite 등 다양한 백엔드로 구현 가능. |
| **ConversationBufferMemory** | 대화 기록 전체를 순차적으로 저장하여 그대로 LLM에 전달. <br>→ 간단하지만 대화가 길어질수록 토큰 낭비 증가. |
| **ConversationSummaryMemory** | 오래된 대화를 요약(summary) 형태로 압축 저장. <br>→ 장기 대화에서 효율적 (요약 후 핵심 내용만 유지). |
| **ConversationBufferWindowMemory** | 최근 N개의 메시지만 유지 (슬라이딩 윈도우 방식). <br>→ 최신 맥락 중심의 응답에 적합. |
| **ConversationSummaryBufferMemory** | 최근 대화는 그대로 유지하고, 오래된 대화는 요약본으로 대체. <br>→ 실무에서 가장 많이 사용되는 하이브리드 방식. |


### 최신 버전 변화 포인트

| 항목 | 기존 방식 | 최신 방식 |
|------|------------|------------|
| 메모리 적용 방식 | 체인(Chain) 내부에서 직접 메모리 지정 | `RunnableWithMessageHistory`로 외부에서 래핑 |
| 주요 모듈 | `langchain.memory` | `langchain_core.chat_history` |
| 상태 관리 | 수동 전달 (`memory.load_memory_variables()`) | 자동 상태 주입 (`RunnableWithMessageHistory`) |
| 유연성 | 한 모델 1개의 메모리만 연결 | 여러 세션·사용자별 메모리 관리 가능 |

---

## 3. 예시: ChatMessageHistory

```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

# 1️⃣ 메모리(히스토리) 객체 생성
history = ChatMessageHistory()

# 2️⃣ 대화 저장
history.add_message(HumanMessage(content="안녕!"))
history.add_message(AIMessage(content="안녕하세요!"))
history.add_message(HumanMessage(content="오늘 날씨 어때?"))
history.add_message(AIMessage(content="서울은 맑아요."))

# 3️⃣ 대화 불러오기
for msg in history.messages:
    print(f"[{msg.type}] {msg.content}")
```

출력:
```
[human] 안녕!
[ai] 안녕하세요!
[human] 오늘 날씨 어때?
[ai] 서울은 맑아요.
```

---

## 4. RunnableWithMessageHistory 사용

### 🧩 1️⃣ 공통점

| 항목 | 설명 |
|------|------|
| 공통 기술 | `RunnableWithMessageHistory`를 사용해 LCEL 기반 메모리 통합 |
| 공통 기능 | LLM이 이전 대화를 기억하도록 상태(`chat_history`)를 관리 |
| 프롬프트 구조 | `ChatPromptTemplate` → `ChatOpenAI`로 구성된 파이프라인 |
| 세션 관리 | `config={"configurable": {"session_id": ...}}`로 세션 분리 가능 |


### 코드 ① — 단일 세션 / 단일 메모리 구조
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 비서입니다."),
    MessagesPlaceholder("chat_history"),   # 👈 반드시 키가 동일해야 함
    ("human", "{input}")
])

chain = prompt | llm

history = ChatMessageHistory()

chain_with_memory = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=lambda _: history, # 세션이 몇 개가 오든, 무조건 같은 히스토리 객체를 돌려줌
    input_messages_key="input",
    history_messages_key="chat_history",   # 👈 여기가 위와 동일
)

resp = chain_with_memory.invoke(
    {"input": "안녕하세요?"},
    config={"configurable": {"session_id": "1"}}
)
print(resp.content)
```

저장된 메시지 확인

```py
for msg in history.messages:
    print(f"{msg.type}: {msg.content}")
```
추가적인 질문

```py
resp = chain_with_memory.invoke(
    {"input": "가을에 여행지 추천해줘"},
    config={"configurable": {"session_id": "1"}}
)
print(resp.content)
```

기존 내용을 이용한 질문

```py
resp = chain_with_memory.invoke(
    {"input": "그 중에 첫번째 여행지에 대해 좀더 자세하게 정리해줄래"},
    config={"configurable": {"session_id": "1"}}
)
print(resp.content)
```

저장된 메시지 확인

```py
for msg in history.messages:
    print(f"{msg.type}: {msg.content}")
```

#### 특징

| 항목 | 설명 |
|------|------|
| **메모리 클래스** | `ChatMessageHistory` (기본형, 인메모리) |
| **세션 관리** | 단일 세션만 지원 (`lambda _: history`) |
| **저장 위치** | 코드 실행 중 메모리에만 저장 (종료 시 사라짐) |
| **적용 대상** | 간단한 챗봇, 단일 사용자 테스트, 실습용 |
| **입출력 구조** | `{input: "..."} → chat_history에 자동 저장 후 응답 반환` |

#### 동작 방식
- `lambda _: history`는 세션 구분 없이 모든 대화를 **같은 history 객체**에 저장합니다.  
- 즉, 한 사용자의 대화가 다른 사용자 입력에 섞일 수 있습니다.  
- 메모리 저장이 단순해서 **테스트나 데모용**으로 적합합니다.

#### 장점
- 코드 간결, 빠르게 테스트 가능  
- 기본 메모리 로직 이해용으로 적합  

#### 단점
- 세션 구분 불가 → 여러 사용자가 동시에 사용할 수 없음  
- 지속성 없음 → 재시작 시 모든 기록 손실  
- 실제 서비스에는 부적합  

### 🧩 코드 ② — 다중 세션 / 실서비스용 구조

```python
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain.prompts import ChatPromptTemplate

# ✅ LLM과 프롬프트 정의
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("사용자 질문: {input}")

# ✅ 사용자별 메모리 생성
store = {}  # 세션별 메모리 저장소

def get_session_history(session_id: str):
    """세션별 대화 기록 관리 함수"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# ✅ 메모리와 LLM을 결합
chain_with_memory = RunnableWithMessageHistory(
    runnable=prompt | llm,
    get_session_history=get_session_history,
    input_messages_key="input",
)

# 세션 ID 지정
session_id = "user1"

# ✅ 대화 실행
response = chain_with_memory.invoke(
    {"input": "가을 여행지 추천해줘"},
    config={"configurable": {"session_id": session_id}}
)

response = chain_with_memory.invoke(
    {"input": "첫번째 여행지에서 반드시 먹어야할 음식 추천도 부탁해"},
    config={"configurable": {"session_id": session_id}}
)

# 세션 ID 지정
session_id = "user2"

# 대화 실행
response = chain_with_memory.invoke(
    {"input": "겨울 여행지 추천해줘"},
    config={"configurable": {"session_id": session_id}}
)

# ✅ 세션별 저장된 메시지 확인
for sid, history in store.items():
    print(f"\n=== 🗂 세션 ID: {sid} ===")
    for msg in history.messages:
        role = "사용자" if msg.type == "human" else "AI"
        print(f"{role}: {msg.content}")

```
#### 특징

| 항목 | 설명 |
|------|------|
| **메모리 클래스** | `InMemoryChatMessageHistory` (LangChain Core 권장 버전) |
| **세션 관리** | 사용자별 세션(`session_id`)로 구분 |
| **저장 위치** | 세션별 딕셔너리(`store`)에 저장 |
| **적용 대상** | 다중 사용자 챗봇, 대화형 앱, RAG 파이프라인 등 |
| **입출력 구조** | 각 세션별로 독립된 대화 맥락 유지 가능 |

#### 동작 방식
- `RunnableWithMessageHistory`가 `get_session_history()` 함수를 통해  
  세션별로 별도의 메모리 객체를 가져옵니다.  
- `config={"configurable": {"session_id": "user1"}}`에 따라  
  사용자마다 고유한 메모리 공간을 유지합니다.

#### 장점
- 세션 독립적 메모리 관리 → 여러 사용자 동시 지원  
- 실제 서비스나 챗봇 앱에 바로 적용 가능  
- 지속성 백엔드(DB/Redis 등)로 쉽게 확장 가능  

#### 단점
- 구조가 약간 복잡함 (세션 관리 필요)  
- 단일 사용자 실습에는 다소 과함  

---

## 비교 요약

| 구분 | 코드 ① (단일 세션) | 코드 ② (다중 세션) |
|------|----------------------|----------------------|
| 메모리 타입 | `ChatMessageHistory` | `InMemoryChatMessageHistory` |
| 세션 관리 | 없음 (고정 history) | 있음 (`session_id` 기반 분리) |
| 적용 범위 | 간단한 테스트 / 학습용 | 다중 사용자 / 실제 서비스용 |
| 메모리 지속성 | 런타임 한정 | 확장 가능 (DB/Redis 연동) |
| 코드 복잡도 | 간단 | 약간 복잡 |
| LangChain 권장 | ⚠️ 구버전 예제 호환 | ✅ 최신 권장 방식 |

---

## 정리 — 어떤 걸 써야 할까?

| 상황 | 추천 코드 | 이유 |
|------|------------|------|
| 빠른 실습, 단일 대화 테스트 | **코드①** | 간단하고 직관적 |
| 챗봇 서비스, 멀티 유저 환경 | **코드②** | 세션별 메모리 분리, 확장성 높음 |
| LCEL 기반 최신 설계 | **코드②** | `InMemoryChatMessageHistory`는 공식 권장 클래스 |
| Redis/DB 연동 고려 | **코드② 기반 확장** | 구조적으로 쉽게 교체 가능 |