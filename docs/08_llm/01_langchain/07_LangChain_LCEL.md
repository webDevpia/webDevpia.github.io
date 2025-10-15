---
title: 7. LCEL
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 7
permalink: /llm/langchain/lcel
---

# LCEL (LangChain Expression Language)

> LCEL은 LangChain의 모든 구성 요소(`Prompt`, `LLM`, `Tool`, `Memory` 등)를 **표준화된 실행 그래프** 형태로 연결하기 위한 방식입니다.  
> 기존의 `LLMChain`을 대체하며, 체인을 직관적이고 효율적으로 구성할 수 있습니다.

---

## 1. LCEL이란?

**LCEL (LangChain Expression Language)** 은 `|` 파이프 문법을 이용해 다양한 컴포넌트를 연결하는 방식입니다.

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("{topic}에 대해 한 줄로 설명해 주세요.")
parser = StrOutputParser()

# ✅ LCEL 파이프 방식
chain = prompt | llm | parser

print(chain.invoke({"topic": "LangChain"}))
```

출력:
```
LangChain은 LLM 애플리케이션을 손쉽게 개발하도록 돕는 오픈소스 프레임워크입니다.
```

---

## 2. LCEL 주요 구성 요소

| 구성 요소 | 설명 |
|------------|------|
| `RunnableSequence` | 순차적으로 연결된 실행 그래프 (기본 형태) |
| `RunnableParallel` | 여러 Runnable을 동시에 실행 후 결과 병합 |
| `RunnableLambda` | 사용자 정의 Python 함수를 체인 내 삽입 |
| `RunnableBranch` | 조건문 기반 분기 처리 |
| `RunnablePassthrough` | 입력을 그대로 다음 단계로 전달 |

---

## 3. RunnableSequence — 순차 실행

> LangChain v0.3.x 이후, `RunnableSequence`는 더 이상 `langchain.schema.runnable`이 아닌  
> `langchain_core.runnables`에서 자동으로 생성됩니다.  
> 보통 명시적으로 선언할 필요 없이, `|` 파이프 문법으로 대체됩니다.

```python
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("{topic}에 대해 설명해 주세요.")
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# ✅ 최신 문법
chain = RunnableSequence(first=prompt, middle=[llm], last=parser)

result = chain.invoke({"topic": "강화학습"})
print(result)
```

> 💡 `prompt | llm | parser` 문법이 내부적으로 `RunnableSequence`를 자동 생성합니다.

---

## 4. RunnableParallel — 병렬 실행

여러 LLM 호출이나 프롬프트를 동시에 처리할 때 사용합니다.

```python
from langchain_core.runnables import RunnableParallel

multi_chain = RunnableParallel({
    "요약": ChatPromptTemplate.from_template("{topic}을(를) 한 문장으로 요약해 주세요.") | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser(),
    "키워드": ChatPromptTemplate.from_template("{topic}의 핵심 키워드 3개를 알려주세요.") | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()
})

result = multi_chain.invoke({"topic": "생성형 AI"})
print(result)
```

출력 예:
```python
{
  "요약": "생성형 AI는 데이터를 학습하여 새로운 콘텐츠를 생성하는 기술입니다.",
  "키워드": "딥러닝, 콘텐츠 생성, 모델"
}
```

---

## 5. RunnableLambda — 사용자 정의 함수 삽입

LLM 처리 결과를 Python 함수로 직접 후처리할 수 있습니다.

```python
from langchain_core.runnables import RunnableLambda
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

def make_uppercase(text: str):
    return text.upper()

prompt = ChatPromptTemplate.from_template("{topic}에 대해 설명해 주세요.")
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

custom_chain = prompt | llm | parser | RunnableLambda(make_uppercase)

print(custom_chain.invoke({"topic": "OpenAI"}))
```

출력 예:
```
OPENAI는 인공지능 연구와 모델 개발을 선도하는 기업입니다.
```

---

## 6. RunnableBranch — 조건 분기 실행

조건에 따라 서로 다른 Runnable을 실행할 수 있습니다.

```python
from langchain_core.runnables import RunnableBranch
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# 조건 분기용 Runnable들
ai_chain = ChatPromptTemplate.from_template(
    "{topic}는 인공지능과 관련이 있습니다."
) | llm | parser

default_chain = ChatPromptTemplate.from_template(
    "{topic}는 일반 주제입니다."
) | llm | parser

# ✅ 최신 문법: 마지막 인자는 'default' Runnable 이어야 함 (조건 튜플 X)
branch = RunnableBranch(
    (lambda x: "AI" in x["topic"], ai_chain),
    default_chain,
)

print(branch.invoke({"topic": "AI 모델"}))
print(branch.invoke({"topic": "음식 문화"}))
```


---

## 7. 실행 방식 비교

| 메서드 | 설명 | 예시 |
|--------|------|------|
| `.invoke()` | 단일 입력을 한 번 실행
 | `chain.invoke({"topic": "LLM"})` |
| `.batch()` | 여러 입력을 한 번에 처리 (병렬 요청) | `chain.batch([{...}, {...}])` |
| `.stream()` | 실시간으로 토큰 단위 출력 | `for chunk in chain.stream(...):` |

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 구성요소 정의
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_template("{topic}에 대해 간단히 설명해 주세요.")
parser = StrOutputParser()

# LCEL 체인 구성
chain = prompt | llm | parser

# ① 단일 실행
result = chain.invoke({"topic": "강화학습"})
print("단일 실행 결과:")
print(result)

# ② 배치 실행 (한 번에 여러 입력)
batch_results = chain.batch([
    {"topic": "LangChain"},
    {"topic": "OpenAI"},
    {"topic": "Python"},
])
print("\n배치 실행 결과:")
for i, r in enumerate(batch_results, 1):
    print(f"{i}. {r}")

# ③ 스트리밍 실행 (토큰 단위 출력)
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

---

## 8. LCEL 실전 예제 — 요약 + 키워드 추출 + JSON 변환

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 1️⃣ 프롬프트 정의
summary_prompt = ChatPromptTemplate.from_template(
    "{text}를 한 문장으로 요약해 주세요."
)
keyword_prompt = ChatPromptTemplate.from_template(
    "{text}에서 핵심 키워드 3개를 추출해 주세요."
)

# 2️⃣ 모델 및 파서 설정
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# 3️⃣ RunnableParallel 구성
# 내부에서 각각의 Runnable이 실행된 뒤 dict 형태로 결과가 합쳐짐
chain = RunnableParallel({
    "요약": summary_prompt | llm | parser,
    "키워드": keyword_prompt | llm | parser,
})

# 4️⃣ 입력 텍스트
text = "생성형 AI는 방대한 데이터를 학습해 새로운 텍스트나 이미지를 생성하는 인공지능 기술입니다."

# 5️⃣ 실행
result = chain.invoke({"text": text})

# 6️⃣ 결과 출력
print("병렬 실행 결과:")
print(result)
```

출력 예:
```json
{
  "요약": "생성형 AI는 데이터를 학습해 새로운 콘텐츠를 만드는 기술입니다.",
  "키워드": ["데이터", "생성", "AI"]
}
```

---

## 9. LCEL에서 자주 사용하는 Runnable 요약

| Runnable | 설명 | 사용 예 |
|-----------|------|----------|
| `RunnableSequence` | 순차 실행 | `prompt | llm | parser` |
| `RunnableParallel` | 병렬 실행 | 여러 LLM 호출 병렬 처리 |
| `RunnableLambda` | 함수 삽입 | 결과 후처리 / 가공 |
| `RunnableBranch` | 조건 분기 | 입력 조건에 따라 분기 실행 |
| `RunnablePassthrough` | 그대로 전달 | 입력 유지 / Debug 용 |

---

## 10. 요약 및 실습 팁

1. LCEL은 **체인 설계를 단순화**하고 **코드 가독성을 향상**시킵니다.  
2. `LLMChain`은 더 이상 권장되지 않으며, LCEL(`|` 문법)을 사용하는 것이 표준입니다.  
3. `RunnableParallel`과 `RunnableLambda`를 활용하면 **데이터 처리 파이프라인**처럼 동작시킬 수 있습니다.  
4. `.stream()` 메서드를 이용하면 실시간 스트리밍 출력도 가능합니다.  

---

> 💡 **Tip:** LCEL은 단순한 문법 변화가 아니라, LangChain을 **컴포넌트 기반 그래프 프레임워크**로 발전시키는 핵심 구조입니다.
