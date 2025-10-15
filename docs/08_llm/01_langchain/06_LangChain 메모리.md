---
title: 6. Memory
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 6
permalink: /llm/langchain/memory
--- 
# LangChain 메모리 (v0.3.x 기준)

---

## 1. 메모리의 개념

LLM은 기본적으로 상태가 없습니다(stateless).  
이전 대화 내용을 기억하지 못하므로, “맥락을 이어가는 대화”를 위해 메모리가 필요합니다.

---

## 2. 기본 구조

LangChain의 메모리는 다음 두 요소로 구성됩니다.

| 구성요소 | 설명 |
|-----------|------|
| **ChatMessageHistory** | 과거 대화 메시지를 저장 |
| **ConversationBufferMemory** | 단순 대화 기록 유지 |
| **ConversationSummaryBufferMemory** | 요약 기반으로 오래된 대화 축약 저장 |

---

## 3. 예시: ConversationBufferMemory

```python
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

memory.save_context({"input": "안녕!"}, {"output": "안녕하세요!"})
memory.save_context({"input": "오늘 날씨 어때?"}, {"output": "서울은 맑아요."})

print(memory.load_memory_variables({}))
```

출력:
```
{'chat_history': [HumanMessage(content='안녕!'), AIMessage(content='안녕하세요!'), ...]}
```

---

## 4. 예시: ConversationSummaryBufferMemory

요약 기반 메모리는 LLM을 통해 오래된 대화를 축약합니다.

```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

memory = ConversationSummaryBufferMemory(llm=llm, memory_key="chat_history", max_token_limit=100)

memory.save_context({"input": "나는 홍길동이야."}, {"output": "반가워요, 홍길동님."})
memory.save_context({"input": "내 이름을 기억하나요?"}, {"output": "물론이죠, 홍길동님."})

print(memory.load_memory_variables({}))
```

---

## 5. RunnableWithMessageHistory 사용 (최신 구조)

```python
from langchain_core.runnables import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("{input}")
chain = prompt | llm

history = ChatMessageHistory()

chain_with_memory = RunnableWithMessageHistory(
    chain,
    lambda _: history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

response = chain_with_memory.invoke({"input": "안녕"}, config={"configurable": {"session_id": "1"}})
print(response.content)
```

---

## 6. 정리 요약

| 유형 | 특징 |
|------|------|
| **BufferMemory** | 모든 대화 저장 |
| **SummaryBufferMemory** | 오래된 대화 요약 저장 |
| **RunnableWithMessageHistory** | 최신 구조 (체인과 메모리 통합) |

✅ **한 줄 요약:**  
LangChain의 메모리는 “LLM이 과거 대화를 잊지 않게 하는 기억장치”입니다.
