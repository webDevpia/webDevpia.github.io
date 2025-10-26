---
title: 4. Template
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 4
permalink: /llm/langchain/template
--- 
# LangChain 프롬프트 템플릿 (v0.3.x 기준)

## 1. 프롬프트 템플릿이란?

LLM은 같은 질문이라도 표현 방식에 따라 완전히 다른 답변을 냅니다.  
**PromptTemplate**은 이런 프롬프트를 **일관되고 구조적으로 관리**하도록 도와주는 도구입니다.  
쉽게 말해, "LLM에게 던지는 질문을 템플릿처럼 미리 만들어 재사용하는 기능"입니다.

---

## 2. 기본 사용법

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("'{text}'를 {language}로 번역해 주세요.")
formatted = prompt.format(text="안녕하세요", language="영어")
print(formatted)
```

출력:
```
'안녕하세요'를 영어로 번역해 주세요.
```

이처럼 `{변수명}` 형태로 동적 값을 삽입할 수 있습니다.

---

## 3. 대화형 프롬프트 (ChatPromptTemplate)

`ChatPromptTemplate`은 대화 기반 모델(`ChatOpenAI`)에 사용할 수 있습니다.

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 번역가입니다."),
    ("user", "'{text}'를 {language}로 번역해 주세요.")
])

messages = prompt.format_messages(text="안녕하세요", language="일본어")
print(messages)
```

출력 예:
```
System: 당신은 친절한 번역가입니다.
User: '안녕하세요'를 일본어로 번역해 주세요.
```

---

## 4. LLM과 연결하기 (LCEL 방식)

LangChain v0.3 이후부터는 **LCEL (LangChain Expression Language)** 문법으로 체인을 연결할 수 있습니다.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-5-nano")

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 서울 여행 전문가입니다."),
    ("user", "{season}에 서울에서 방문하기 좋은 장소를 추천해 주세요.")
])

chain = prompt | llm  # 프롬프트 → LLM 연결

response = chain.invoke({"season": "봄"})
print(response.content)
```

---

## 5. partial()로 동적 변수 주입

`partial()`은 템플릿 안의 일부 값을 미리 고정해 두는 기능입니다.

```python
from datetime import datetime
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "오늘 날짜는 {date}입니다. {topic}에 대한 짧은 뉴스를 생성해 주세요."
).partial(date=datetime.now().strftime("%Y-%m-%d"))

print(prompt.format(topic="인공지능"))
```

출력 예:
```
오늘 날짜는 2025-10-13입니다. 인공지능에 대한 짧은 뉴스를 생성해 주세요.
```

---

## 6. 여러 프롬프트를 조합한 체인

두 개 이상의 프롬프트를 연결해 복합적인 질문 흐름을 만들 수 있습니다.

```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-5-nano")

# 첫 번째 프롬프트: 음식 찾기
p1 = PromptTemplate.from_template("{city}의 가장 유명한 음식은?")

# 두 번째 프롬프트: 식당 찾기
p2 = PromptTemplate.from_template("{food}를 판매하는 가장 인기 있는 식당은?")

chain = p1 | llm | p2 | llm

result = chain.invoke({"city": "서울"})
print(result.content)
```

출력 예:
```
서울의 대표 음식은 불고기입니다.
불고기를 판매하는 가장 인기 있는 식당은 우래옥입니다.
```

---

## 7. 고급: 프롬프트 변형 및 시나리오 기반 작성

`ChatPromptTemplate`은 유연하게 구성할 수 있습니다. 예를 들어, 이메일 자동 작성:

```python
from langchain_core.prompts import ChatPromptTemplate

email_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 마케팅 이메일 카피 전문가입니다."),
    ("user", "{product}를 홍보하는 이메일을 {tone} 톤으로 작성해 주세요.")
])

formatted = email_prompt.format_messages(product="스마트워치", tone="따뜻한")
for msg in formatted:
    print(f"{msg.type.upper()}: {msg.content}")
```

출력:
```
SYSTEM: 당신은 마케팅 이메일 카피 전문가입니다.
USER: 스마트워치를 홍보하는 이메일을 따뜻한 톤으로 작성해 주세요.
```

---

## 8. 요약

| 구분 | 설명 |
|------|------|
| **PromptTemplate** | 일반 텍스트 기반 프롬프트 |
| **ChatPromptTemplate** | 대화형 프롬프트 (system/user 구분) |
| **.format()** | 변수 채우기 |
| **.partial()** | 일부 변수 미리 고정 |
| **prompt \| llm** | LCEL 문법으로 체인 연결 |
| **invoke()** | 체인 실행 (결과 반환) |

---

## 🎯 실습 포인트
1. 같은 질문을 다른 템플릿으로 구성해 결과 차이를 비교해보세요.  
2. `.partial()`을 이용해 날짜, 지역명, 회사명 등 반복되는 정보를 미리 설정하면 효율적입니다.  
3. `ChatPromptTemplate`을 사용하면 **system/user 역할을 분리**해 더 정확한 대화 흐름을 제어할 수 있습니다.

---

> 💡 **Tip:** 프롬프트는 모델 성능만큼 중요합니다. 잘 설계된 프롬프트 하나가 LLM 품질을 좌우합니다.
