---
title: 4. Template
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 4
permalink: /llm/langchain/template
---


## 학습 목표

- 프롬프트 템플릿의 필요성을 이해하고, PromptTemplate과 ChatPromptTemplate을 상황에 맞게 사용할 수 있다
- system/user 역할 분리로 LLM의 응답 품질을 제어할 수 있다
- partial()과 체인 조합으로 복합적인 프롬프트 흐름을 설계할 수 있다

<a id="toc"></a>

## 진행 순서

1. [왜 프롬프트 템플릿인가?](#part1) - 하드코딩 vs 템플릿 비교
2. [PromptTemplate — 기본 텍스트 템플릿](#part2) - 변수 삽입과 format()
3. [ChatPromptTemplate — 역할 분리 템플릿](#part3) - system/user 역할
4. [LLM과 연결해서 실행하기](#part4) - 체인 구성과 invoke()
5. [partial() — 변수 미리 고정하기](#part5) - 반복 값 설정
6. [여러 프롬프트를 연결한 체인](#part6) - 프롬프트 조합
7. [시나리오 기반 프롬프트 작성](#part7) - 이메일 작성 예시
8. [정리](#part8)

> **사전 준비:** [1장 개발환경](/llm/langchain/install)에서 `.env` 파일 설정과 패키지 설치를 완료한 상태에서 진행합니다. 모든 코드는 `.env`에 `OPENAI_API_KEY`가 설정되어 있어야 동작합니다.

---

# LangChain 프롬프트 템플릿

<a id="part1"></a>

## 1. 왜 프롬프트 템플릿인가? [↑](#toc)

이전 챕터에서 `ChatPromptTemplate.from_template()`으로 프롬프트를 만들어 봤습니다. 이번 챕터에서는 이 템플릿의 다양한 기능과 활용법을 깊이 살펴봅니다.

### 편지지 비유로 이해하기

프롬프트 템플릿은 **빈칸이 있는 편지지**와 같습니다.

```
📝 프롬프트 템플릿 = 빈칸이 있는 편지지

"___님께, 오늘 ___에 대해 알려드립니다."
      ↓ 빈칸을 채우면
"영희님께, 오늘 인공지능에 대해 알려드립니다."
```

한 번 만들어 두면 빈칸({변수})만 바꿔서 **여러 번 재사용**할 수 있습니다.

### 하드코딩 vs 템플릿 비교

```python
# ❌ 하드코딩 — 매번 전체 문장을 다시 작성
response1 = llm.invoke("'안녕하세요'를 영어로 번역해 주세요.")
response2 = llm.invoke("'감사합니다'를 영어로 번역해 주세요.")
response3 = llm.invoke("'잘 부탁드립니다'를 일본어로 번역해 주세요.")
# → 포맷이 조금씩 달라질 수 있고, 실수 가능성이 높음

# ✅ 템플릿 — 빈칸만 바꿔서 재사용
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("'{text}'를 {language}로 번역해 주세요.")
# → 한 번 만들면 변수만 바꿔 사용. 포맷 일관성 보장.
```

> 💡 파이썬의 f-string(`f"'{text}'를 {language}로 번역해 주세요"`)과 비슷한 원리입니다. 다만 LangChain 템플릿은 **나중에 값을 넣을 수 있고**, **체인에 연결**할 수 있고, **변수 이름을 자동 추적**하는 등 LLM 전용 기능을 제공합니다.

---

<a id="part2"></a>

## 2. PromptTemplate — 기본 텍스트 템플릿 [↑](#toc)

가장 단순한 형태의 템플릿입니다. `{변수명}`으로 빈칸을 만들고, `.format()`으로 값을 채웁니다.

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("'{text}'를 {language}로 번역해 주세요.")

# format()으로 변수에 값을 채움 → 완성된 문자열 반환
formatted = prompt.format(text="안녕하세요", language="영어")
print(formatted)
```

출력:
```
'안녕하세요'를 영어로 번역해 주세요.
```

> 💡 `.format()`은 **문자열만 반환**합니다. LLM을 호출하지 않습니다. LLM에 보내려면 뒤에서 배울 체인 연결이 필요합니다.

---

<a id="part3"></a>

## 3. ChatPromptTemplate — 역할 분리 템플릿 [↑](#toc)

`ChatPromptTemplate`은 **역할극 대본**과 같습니다. AI에게 "당신은 번역가입니다"라고 역할을 지정하고(system), 사용자의 질문을 전달합니다(user).

```
🎭 ChatPromptTemplate = 역할극 대본

감독 지시(system): "당신은 친절한 번역가입니다."
배우 대사(user): "'안녕하세요'를 일본어로 번역해 주세요."
```

### system 역할이 왜 중요한가?

같은 질문이라도 **system 메시지에 따라 AI의 답변이 완전히 달라집니다**.

| system 메시지 | 같은 질문에 대한 답변 스타일 |
|---|---|
| "당신은 친절한 번역가입니다" | 정확하고 자연스러운 번역 제공 |
| "당신은 개그맨입니다" | 재미있는 말장난으로 번역 |
| (system 없음) | AI가 알아서 판단 — 일관성 없음 |

### 코드

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 번역가입니다."),    # AI의 역할 설정
    ("user", "'{text}'를 {language}로 번역해 주세요.")  # 사용자 질문
])

# format_messages()로 Message 객체 리스트 생성
messages = prompt.format_messages(text="안녕하세요", language="일본어")
for msg in messages:
    print(f"{msg.type.upper()}: {msg.content}")
```

출력:
```
SYSTEM: 당신은 친절한 번역가입니다.
HUMAN: '안녕하세요'를 일본어로 번역해 주세요.
```

### PromptTemplate vs ChatPromptTemplate — 언제 뭘 쓰나?

| | PromptTemplate | ChatPromptTemplate |
|---|---|---|
| **형태** | 단일 텍스트 문자열 | system/user 역할 구분된 메시지 리스트 |
| **비유** | 빈칸 편지지 | 역할극 대본 |
| **사용 시점** | 단순 텍스트가 필요할 때 | **대부분의 경우 (권장)** |
| **장점** | 간결함 | 역할 제어로 응답 품질 향상 |

> 💡 **실무 가이드**: 대부분의 경우 `ChatPromptTemplate`을 사용하세요. `PromptTemplate`은 체인 중간에서 단순 텍스트 조합이 필요할 때만 사용합니다.

---

<a id="part4"></a>

## 4. LLM과 연결해서 실행하기 [↑](#toc)

3장에서 배운 LCEL 파이프로 템플릿을 LLM에 연결합니다.

```python
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 서울 여행 전문가입니다."),
    ("user", "{season}에 서울에서 방문하기 좋은 장소를 추천해 주세요.")
])

# 템플릿 → LLM → 파서 체인 연결
chain = prompt | llm | parser

response = chain.invoke({"season": "봄"})
print(response)
```

출력 예:
```
봄에는 여의도 윤중로 벚꽃길, 석촌호수, 경복궁을 추천합니다. 벚꽃이 만개하는 4월 초가 가장 좋습니다.
```

> 💡 `.format()`은 문자열만 반환하고, `.invoke()`는 **체인 전체를 실행**해서 LLM 응답까지 받습니다.

---

{: .warning }
> **여기부터 심화 내용입니다.** 위의 1~4번만으로도 프롬프트 템플릿의 핵심을 충분히 활용할 수 있습니다. 아래 내용은 필요할 때 돌아와서 학습해도 됩니다.

---

<a id="part5"></a>

## 5. partial() — 변수 미리 고정하기 [↑](#toc)

### 이런 상황을 상상해 보세요

> "고객센터 챗봇을 만드는데, **회사명**과 **오늘 날짜**는 항상 같고, **고객 질문**만 매번 바뀌어요."

`partial()`은 양식의 일부를 **미리 인쇄해두는 것**과 같습니다. 회사명은 이미 찍혀 있고, 이름만 쓰면 됩니다.

```python
from datetime import datetime
from langchain_core.prompts import PromptTemplate

# 날짜를 미리 고정
prompt = PromptTemplate.from_template(
    "오늘 날짜는 {date}입니다. {topic}에 대한 짧은 뉴스를 생성해 주세요."
).partial(date=datetime.now().strftime("%Y-%m-%d"))

# 실행할 때는 topic만 전달하면 됨
print(prompt.format(topic="인공지능"))
```

출력 예:
```
오늘 날짜는 2026-04-02입니다. 인공지능에 대한 짧은 뉴스를 생성해 주세요.
```

> 💡 `partial()`을 쓰지 않으면 매번 `prompt.format(date="2026-04-02", topic="인공지능")`처럼 날짜도 함께 전달해야 합니다. 반복되는 값을 미리 고정하면 실행 시 필요한 변수만 전달할 수 있어 편리합니다.

---

<a id="part6"></a>

## 6. 여러 프롬프트를 연결한 체인 [↑](#toc)

### 이런 상황을 상상해 보세요

> "서울의 대표 음식이 뭔지 물어보고, 그 음식을 파는 인기 식당을 다시 물어보고 싶어요."

두 개의 질문을 **순서대로 연결**하면, 첫 번째 답변을 두 번째 질문에 자동으로 넘길 수 있습니다.

```
🔗 프롬프트 체인 = 릴레이

"서울의 유명한 음식?" → LLM → "불고기"
                                    ↓
"불고기 맛집은?" → LLM → "우래옥"
```

### 단계별 코드

```python
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# 1단계: 음식 찾기
p1 = ChatPromptTemplate.from_template("{city}의 가장 유명한 음식은?")

# 2단계: 식당 찾기
p2 = ChatPromptTemplate.from_template("{food}를 판매하는 가장 인기 있는 식당은?")

# 1단계 실행
food_chain = p1 | llm | parser
food_result = food_chain.invoke({"city": "서울"})
print(f"1단계 결과: {food_result}")

# 2단계 실행 (1단계 결과를 변수로 전달)
restaurant_chain = p2 | llm | parser
restaurant_result = restaurant_chain.invoke({"food": food_result})
print(f"2단계 결과: {restaurant_result}")
```

출력 예:
```
1단계 결과: 서울의 대표 음식은 불고기입니다.
2단계 결과: 불고기를 판매하는 가장 인기 있는 식당은 우래옥입니다.
```

### 한 줄 체인으로 축약 (심화)

위 코드를 LCEL 파이프 한 줄로 연결할 수도 있습니다.
위 코드에 아래 코드를 추가해서 실행해 봅니다.
```python
from langchain_core.runnables import RunnableLambda

# 중간 변환 함수: LLM 출력 문자열을 다음 프롬프트의 변수로 매핑
def to_food_input(text):
    """앞 단계의 출력을 {"food": "..."} 형태로 변환합니다."""
    return {"food": text}

# 한 줄 체인: p1 → LLM → 문자열 → 변수 매핑 → p2 → LLM → 문자열
full_chain = p1 | llm | parser | RunnableLambda(to_food_input) | p2 | llm | parser

result = full_chain.invoke({"city": "서울"})
print(result)
```

> 💡 중간에 `RunnableLambda(to_food_input)`이 필요한 이유: 첫 번째 LLM의 출력은 문자열("불고기")이지만, 두 번째 프롬프트(`p2`)는 `{"food": "불고기"}` 형태의 딕셔너리를 기대하기 때문입니다.

---

<a id="part7"></a>

## 7. 시나리오 기반 프롬프트 작성 [↑](#toc)

다양한 변수를 조합하여 실용적인 프롬프트를 만들 수 있습니다.

### 예시: 마케팅 이메일 자동 작성

```python
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 마케팅 이메일 카피 전문가입니다."),
    ("user", "{product}를 홍보하는 이메일을 {tone} 톤으로 작성해 주세요.")
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

# 변수만 바꿔서 다양한 이메일 생성
print(chain.invoke({"product": "스마트워치", "tone": "따뜻한"}))
```

출력 예:
```
안녕하세요! 바쁜 일상 속에서도 건강을 챙기고 싶은 당신을 위해, 새로운 스마트워치를 소개합니다...
```

> 💡 product와 tone만 바꾸면 "헤드폰을 유머러스하게", "노트북을 전문적으로" 등 다양한 이메일을 생성할 수 있습니다.

---

<a id="part8"></a>

## 8. 정리 [↑](#toc)

### 핵심 개념

| 구분 | 비유 | 설명 |
|------|------|------|
| **PromptTemplate** | 빈칸 편지지 | 단순 텍스트 기반 프롬프트 |
| **ChatPromptTemplate** | 역할극 대본 | system/user 역할 구분 **(대부분 이것을 사용)** |
| **.format()** | 빈칸 채우기 | 변수에 값을 넣어 문자열 반환 |
| **.invoke()** | 편지 보내기 | 체인 전체를 실행해서 LLM 응답 반환 |
| **.partial()** | 미리 인쇄 | 일부 변수를 미리 고정 |

### 실습 과제

- **기본**: "당신은 ___입니다" system 메시지를 3가지 다르게 설정하고, 같은 질문에 대한 답변 차이를 비교해 보세요
- **중급**: `partial()`로 회사명을 고정하고, 고객 질문만 바꿔가며 고객센터 프롬프트를 만들어 보세요
- **심화**: 6번처럼 프롬프트 2개를 연결하여, "도시 → 관광지 → 관광지 역사" 3단계 체인을 만들어 보세요

---

> 💡 **Tip:** 프롬프트는 모델 성능만큼 중요합니다. 잘 설계된 프롬프트 하나가 LLM 품질을 좌우합니다.


→ **다음 장**: [5. Parser](/llm/langchain/parser)
