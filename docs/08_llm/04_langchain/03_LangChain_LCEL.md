---
title: 3. LCEL
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 3
permalink: /llm/langchain/lcel
---


## 학습 목표

- LCEL 파이프(`|`) 문법의 원리를 이해하고 체인을 구성할 수 있다
- invoke, stream, batch 3가지 실행 방식을 사용할 수 있다
- RunnableParallel, RunnableLambda, RunnableBranch를 상황에 맞게 활용할 수 있다

<a id="toc"></a>

## 진행 순서

1. [LCEL이란?](#part1) - 이전 챕터와의 연결, 공장 비유
2. [실행 방식 3가지](#part2) - invoke, stream, batch
3. [RunnableParallel — 동시에 여러 작업](#part3) - 요약 + 키워드를 한 번에
4. [RunnableLambda — 내 함수 끼워넣기](#part4) - LLM 결과 후처리
5. [RunnableBranch — 조건에 따라 분기](#part5) - 입력에 따라 다른 체인 실행
6. [실전 예제 — 요약 + 키워드 동시 추출](#part6)
7. [정리](#part7)

---


# LCEL (LangChain Expression Language)

<a id="part1"></a>

## 1. LCEL이란? [↑](#toc)

이전 챕터에서 이런 코드를 사용했던 것을 기억하시나요?

```python
chain = prompt | llm | parser
response = chain.invoke({"city": "서울"})
```

**이것이 바로 LCEL입니다!** 이미 사용하고 계셨습니다.

LCEL은 `|` (파이프) 기호로 LangChain의 구성 요소들을 연결하는 방식입니다.

### 공장 조립 라인으로 이해하기

LCEL은 **공장의 조립 라인**과 같습니다.

```
🏭 LCEL = 공장 조립 라인

원재료(사용자 입력)
    │
    ▼
[1번 기계: Prompt] ──→ 질문을 정해진 형식으로 만듦
    │
    ▼ (파이프 = 컨베이어 벨트)
[2번 기계: LLM] ──→ AI가 답변을 생성
    │
    ▼ (파이프 = 컨베이어 벨트)
[3번 기계: Parser] ──→ 답변을 깔끔한 문자열로 정리
    │
    ▼
완제품(최종 응답)
```

`|` 기호가 바로 기계와 기계를 연결하는 **컨베이어 벨트**입니다. 왼쪽의 출력이 오른쪽의 입력으로 자동 전달됩니다.

### 기본 예제

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 각 "기계"를 준비
prompt = ChatPromptTemplate.from_template("{topic}에 대해 한 줄로 설명해 주세요.")
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# 파이프(|)로 조립 라인 구성
chain = prompt | llm | parser

# 원재료 투입 → 완제품 출력
print(chain.invoke({"topic": "LangChain"}))
```

출력 예:
```
LangChain은 LLM 애플리케이션을 손쉽게 개발하도록 돕는 오픈소스 프레임워크입니다.
```

### LCEL로 할 수 있는 것들

| 상황 | LCEL 기능 | 비유 |
|------|----------|------|
| 순서대로 실행하고 싶을 때 | `prompt \| llm \| parser` | 조립 라인 (순차) |
| 여러 작업을 동시에 하고 싶을 때 | `RunnableParallel` | 밥 짓는 동안 반찬도 만들기 |
| LLM 결과를 내 방식으로 가공하고 싶을 때 | `RunnableLambda` | 조립 라인에 내 공정 추가 |
| 입력에 따라 다른 처리를 하고 싶을 때 | `RunnableBranch` | 무게별 자동 분류기 |

> 💡 `prompt | llm | parser` 문법은 내부적으로 `RunnableSequence`라는 객체를 자동 생성합니다. 직접 만들 필요는 없고, 파이프 문법만 사용하면 됩니다.

---

<a id="part2"></a>

## 2. 실행 방식 3가지: invoke, stream, batch [↑](#toc)

체인을 만들었으면 3가지 방법으로 실행할 수 있습니다.

| 메서드 | 비유 | 설명 |
|--------|------|------|
| `.invoke()` | 1인분 주문 | 입력 1개 → 결과 1개 |
| `.batch()` | 단체 주문 | 입력 여러 개 → 결과 여러 개 (한 번에) |
| `.stream()` | 뷔페 | 결과가 나오는 대로 바로 받기 (실시간) |

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_template("{topic}에 대해 간단히 설명해 주세요.")
parser = StrOutputParser()

chain = prompt | llm | parser

# ① invoke: 1인분 주문
result = chain.invoke({"topic": "강화학습"})
print("단일 실행 결과:")
print(result)

# ② batch: 단체 주문 (3개를 한 번에)
batch_results = chain.batch([
    {"topic": "LangChain"},
    {"topic": "OpenAI"},
    {"topic": "Python"},
])
print("\n배치 실행 결과:")
for i, r in enumerate(batch_results, 1):  # 1부터 번호를 매기며 순회
    print(f"{i}. {r}")

# ③ stream: 뷔페 (글자가 나오는 대로 바로 출력)
print("\n스트리밍 실행 결과:")
for chunk in chain.stream({"topic": "생성형 AI"}):
    print(chunk, end="")
```

출력 예:
```
단일 실행 결과:
강화학습은 보상 기반으로 행동을 학습하는 머신러닝 기법입니다.

배치 실행 결과:
1. LangChain은 LLM 애플리케이션을 쉽게 만들 수 있는 프레임워크입니다.
2. OpenAI는 인공지능 연구를 선도하는 기업입니다.
3. Python은 데이터 과학과 AI 분야에서 널리 사용되는 언어입니다.

스트리밍 실행 결과:
생성형 AI는 데이터를 학습해 새로운 콘텐츠를 생성하는 인공지능입니다.
```

> 💡 **stream은 언제 쓰나요?** ChatGPT처럼 답변이 한 글자씩 나타나는 효과를 만들 때 사용합니다. 사용자가 긴 답변을 기다리지 않아도 되어 체감 속도가 빨라집니다.

---

<a id="part3"></a>

## 3. RunnableParallel — 동시에 여러 작업 [↑](#toc)

### 이런 상황을 상상해 보세요

> "하나의 문서에 대해 **요약**도 하고 **키워드**도 뽑고 싶어요."

순서대로 하면 2번 기다려야 합니다. 하지만 두 작업은 서로 독립적이므로 **동시에** 할 수 있습니다.

```
📊 RunnableParallel = 동시에 여러 요리 만들기

                 ┌→ [요약 체인] → 요약 결과 ─┐
입력 ("생성형 AI") │                           ├→ {"요약": "...", "키워드": "..."}
                 └→ [키워드 체인] → 키워드 결과 ┘
```

### 코드

```python
from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# 두 개의 체인을 동시에 실행
multi_chain = RunnableParallel({
    "요약": ChatPromptTemplate.from_template("{topic}을(를) 한 문장으로 요약해 주세요.") | llm | parser,
    "키워드": ChatPromptTemplate.from_template("{topic}의 핵심 키워드 3개를 알려주세요.") | llm | parser,
})

result = multi_chain.invoke({"topic": "생성형 AI"})
print(result)
```

출력 예:
```
{
  '요약': '생성형 AI는 데이터를 학습하여 새로운 콘텐츠를 생성하는 기술입니다.',
  '키워드': '딥러닝, 콘텐츠 생성, 모델'
}
```

> 💡 결과가 딕셔너리(`{키: 값}`) 형태로 합쳐져서 나옵니다. 각 키("요약", "키워드")가 각 체인의 결과에 매핑됩니다.

---

<a id="part4"></a>

## 4. RunnableLambda — 내 함수 끼워넣기 [↑](#toc)

### 이런 상황을 상상해 보세요

> "LLM 응답에서 **첫 문장만 추출**하고 싶어요." 또는 "응답의 **글자 수를 세**고 싶어요."

LLM이 만든 결과를 **내가 원하는 대로 가공**하고 싶을 때 `RunnableLambda`를 사용합니다. 조립 라인 중간에 **내 공정을 끼워넣는** 것입니다.

```
🔧 RunnableLambda = 조립 라인에 내 공정 추가

입력 → [Prompt] → [LLM] → [Parser] → [내 함수] → 가공된 출력
```

### 코드 — 첫 문장만 추출하기

```python
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 내가 만든 후처리 함수: 첫 문장만 추출
def extract_first_sentence(text: str):
    """마침표 기준으로 첫 번째 문장만 반환합니다."""
    return text.split(".")[0] + "."

prompt = ChatPromptTemplate.from_template("{topic}에 대해 설명해 주세요.")
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# 체인 끝에 내 함수를 연결
chain = prompt | llm | parser | RunnableLambda(extract_first_sentence)

print(chain.invoke({"topic": "OpenAI"}))
```

출력 예:
```
OpenAI는 인공지능 연구와 모델 개발을 선도하는 기업입니다.
```

### 다른 활용 예시

```python
# 글자 수 추가
def add_char_count(text: str):
    return f"{text}\n\n(총 {len(text)}자)"

# 간단한 감정 태그 붙이기
def add_sentiment_tag(text: str):
    if "좋" in text or "추천" in text:
        return f"[긍정] {text}"
    elif "나쁘" in text or "비추" in text:
        return f"[부정] {text}"
    return f"[중립] {text}"
```

> 💡 `RunnableLambda`에는 **어떤 Python 함수든** 넣을 수 있습니다. 입력을 받아서 출력을 반환하는 함수면 됩니다.

---

{: .warning }
> **여기부터 심화 내용입니다.** 위의 1~4번만으로도 대부분의 LangChain 프로젝트를 구현할 수 있습니다. 아래 내용은 필요할 때 돌아와서 학습해도 됩니다.

---

<a id="part5"></a>

## 5. RunnableBranch — 조건에 따라 분기 [↑](#toc)

### 이런 상황을 상상해 보세요

> "사용자가 **프로그래밍 질문**을 하면 코딩 전문가로, **일반 질문**을 하면 일반 비서로 응답하고 싶어요."

입력 내용에 따라 **다른 체인을 실행**하는 것이 `RunnableBranch`입니다. 공장의 **자동 분류기**처럼, 조건에 따라 다른 라인으로 보냅니다.

```
🔀 RunnableBranch = 조건별 자동 분류기

              ┌─ "AI" 포함? → [AI 전문 체인] → 결과
입력 ────────→│
              └─ 그 외 → [기본 체인] → 결과
```

### 코드

```python
from langchain_core.runnables import RunnableBranch
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# 분기별 체인 준비
ai_chain = ChatPromptTemplate.from_template(
    "AI 전문가로서 {topic}에 대해 기술적으로 설명해 주세요."
) | llm | parser

default_chain = ChatPromptTemplate.from_template(
    "{topic}에 대해 일반인이 이해할 수 있게 쉽게 설명해 주세요."
) | llm | parser

# 조건 판별 함수 (topic에 "AI"가 포함되어 있는지 확인)
def is_ai_topic(input_dict):
    """입력의 topic에 'AI'가 포함되어 있으면 True를 반환합니다."""
    return "AI" in input_dict["topic"]

# 분기 설정: (조건 함수, 실행할 체인) 쌍 + 마지막은 기본 체인
branch = RunnableBranch(
    (is_ai_topic, ai_chain),   # 조건이 True면 ai_chain 실행
    default_chain,              # 어떤 조건도 안 맞으면 default_chain 실행
)

print("AI 질문:", branch.invoke({"topic": "AI 모델"}))
print("일반 질문:", branch.invoke({"topic": "음식 문화"}))
```

출력 예:
```
AI 질문: AI 모델은 대규모 데이터셋으로 훈련된 신경망 기반의 수학적 함수입니다...
일반 질문: 음식 문화란 한 지역이나 나라에서 전통적으로 먹는 음식과 식사 방식을 말합니다...
```

> 💡 조건을 여러 개 추가할 수도 있습니다: `RunnableBranch((조건1, 체인1), (조건2, 체인2), 기본_체인)`

---

<a id="part6"></a>

## 6. 실전 예제 — 요약 + 키워드 동시 추출 [↑](#toc)

지금까지 배운 기법을 조합한 실전 예제입니다. 하나의 텍스트를 넣으면 **요약과 키워드를 동시에 추출**합니다.

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 프롬프트 정의
summary_prompt = ChatPromptTemplate.from_template(
    "{text}를 한 문장으로 요약해 주세요."
)
keyword_prompt = ChatPromptTemplate.from_template(
    "{text}에서 핵심 키워드 3개를 쉼표로 구분해 알려주세요."
)

# 모델 및 파서
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# 병렬 체인 구성
chain = RunnableParallel({
    "요약": summary_prompt | llm | parser,
    "키워드": keyword_prompt | llm | parser,
})

# 실행
text = "생성형 AI는 방대한 데이터를 학습해 새로운 텍스트나 이미지를 생성하는 인공지능 기술입니다."
result = chain.invoke({"text": text})

print("요약:", result["요약"])
print("키워드:", result["키워드"])
```

출력 예:
```
요약: 생성형 AI는 데이터를 학습해 새로운 콘텐츠를 만드는 기술입니다.
키워드: 데이터, 생성, AI
```

---

<a id="part7"></a>

## 7. 정리 [↑](#toc)

### LCEL 핵심 구성 요소

| 구성 요소 | 비유 | 언제 쓰나? |
|----------|------|-----------|
| `prompt \| llm \| parser` | 조립 라인 (순차) | 기본 체인 구성 |
| `RunnableParallel` | 동시 요리 (병렬) | 여러 작업을 한 번에 |
| `RunnableLambda` | 내 공정 추가 | LLM 결과 후처리 |
| `RunnableBranch` | 자동 분류기 (분기) | 조건별 다른 처리 |
| `RunnablePassthrough` | 그대로 전달 | 입력 유지 (RAG에서 사용) |

### 실행 방식 요약

| 메서드 | 비유 | 사용 상황 |
|--------|------|----------|
| `.invoke()` | 1인분 주문 | 일반적인 단일 실행 |
| `.batch()` | 단체 주문 | 여러 입력을 한 번에 처리 |
| `.stream()` | 뷔페 | 실시간 스트리밍 (챗봇 UI) |

### 핵심 포인트

1. `|` 파이프는 **왼쪽 출력 → 오른쪽 입력**으로 자동 전달하는 컨베이어 벨트입니다
2. 이전 챕터에서 사용한 `prompt | llm | parser`가 LCEL의 기본 형태입니다
3. `.stream()`을 사용하면 ChatGPT처럼 실시간 응답이 가능합니다
4. `RunnableParallel`로 여러 작업을 동시에 처리하면 시간을 절약할 수 있습니다

### 실습 과제

- **기본**: `.invoke()`, `.batch()`, `.stream()` 세 가지를 모두 실행해 보고 차이를 체감해 보세요
- **중급**: `RunnableParallel`로 "번역 + 요약"을 동시에 하는 체인을 만들어 보세요
- **심화**: `RunnableBranch`로 한국어/영어 질문을 자동 분류하는 체인을 만들어 보세요
