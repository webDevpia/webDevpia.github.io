---
title: 5. Parser
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 5
permalink: /llm/langchain/parser
---


## 학습 목표

- StrOutputParser, JsonOutputParser로 LLM 출력을 원하는 형식으로 변환할 수 있다
- with_structured_output()을 사용할 수 있다

<a id="toc"></a>

## 진행 순서

1. [출력 파서(Output Parser)란?](#part1) - OutputParser의 필요성과 개념
2. [기본 사용법 — StrOutputParser](#part2) - 문자열 출력 처리
3. [JSON 형식 강제 — JsonOutputParser](#part3) - 구조화된 JSON 출력
4. [정적 타입 검증 — with_structured_output()](#part4) - Pydantic 스키마 기반 출력 보장
5. [실전 예시: JSON 결과를 DB로 저장하기](#part5) - SQLite 연동 실습
6. [실습 과제](#part6) - 핵심 정리


---

# LangChain 출력 파서

이전 챕터에서 `StrOutputParser()`를 사용해 LLM 응답을 깔끔한 문자열로 받아봤습니다. 이번 챕터에서는 문자열 외에 **JSON, Python 객체** 등 다양한 형식으로 출력을 제어하는 방법을 배웁니다.

<a id="part1"></a>

## 1. 출력 파서(Output Parser)란? [↑](#toc)

### 택배 포장 비유

> 파서는 **택배 포장 직원**과 같습니다. LLM이 만든 답변(내용물)을 받아서, 받는 사람(프로그램)이 원하는 포장 형태(문자열, JSON, 객체)로 정리해 줍니다. 포장이 엉망이면 받는 쪽에서 열기 어렵듯, 파서 없이는 프로그램이 LLM 응답을 처리하기 어렵습니다.

LLM의 출력은 사람이 읽기에는 편하지만, **프로그램이 처리하기에는 불안정**한 경우가 많습니다.

```
❌ 파서 없이 — LLM이 자유롭게 답변
"서울의 명소로는 경복궁, 남산타워, 광화문 등이 있습니다."
→ 프로그램: "이걸 어떻게 리스트로 쪼개지?" 😱

✅ JsonOutputParser 사용 — 구조화된 출력
[{"name": "경복궁"}, {"name": "남산타워"}, {"name": "광화문"}]
→ 프로그램: result[0]["name"] 으로 바로 접근 가능 👍
```

### 파서 종류 한눈에 보기

| 파서 | 비유 | 출력 형태 | 사용 시점 |
|------|------|----------|----------|
| `StrOutputParser` | 일반 택배 | 문자열 | 대부분의 경우 (기본) |
| `JsonOutputParser` | 규격 박스 | dict/list | 구조화된 데이터 필요 시 |
| `with_structured_output()` | 맞춤 제작 상자 | Pydantic 객체 | 타입 검증까지 필요 시 **(권장)** |

---

<a id="part2"></a>

## 2. 기본 사용법 — `StrOutputParser` [↑](#toc)

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("{topic}에 대해 한 줄로 설명해 주세요.")
parser = StrOutputParser()

chain = prompt | llm | parser

print(chain.invoke({"topic": "LangChain"}))
```

결과:
```
LangChain은 자연어 처리(NLP) 모델을 효과적으로 구축하고 배포할 수 있도록 지원하는 프레임워크입니다.
```

`StrOutputParser`는 가장 기본적인 파서로, LLM의 응답을 **단순 문자열로 반환**합니다.

---

<a id="part3"></a>

## 3. JSON 형식 강제 — `JsonOutputParser` [↑](#toc)

LLM이 JSON 형식으로 데이터를 주도록 강제하고 싶다면 `JsonOutputParser`를 사용합니다.

```python
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template(
    "서울의 대표 명소 3곳을 JSON 배열로 반환하세요."
)

chain = prompt | llm | parser

result = chain.invoke({})
print(result)
```

예시 출력:
```python
[
  {"name": "경복궁", "location": "서울 종로구"},
  {"name": "남산타워", "location": "용산구"},
  {"name": "광화문", "location": "종로구"}
]
```

💡 이렇게 하면 Python 코드에서 `dict`나 `list` 형태로 바로 사용할 수 있습니다.

---

<a id="part4"></a>

## 4. 정적 타입 검증 — `with_structured_output()` [↑](#toc)

`with_structured_output()`은 LLM 출력을 **Python 객체**로 바로 받을 수 있는 가장 강력한 방법입니다.

> **주문서 비유**: Pydantic 모델은 **주문서 양식**과 같습니다. "이름은 반드시 문자, 위치도 반드시 문자, 설명도 반드시 문자"라고 양식을 정해두면, LLM이 양식에 맞지 않는 답변을 주면 자동으로 걸러냅니다.

`pydantic`의 `BaseModel`은 **"이런 형태의 데이터를 원합니다"라고 LLM에게 알려주는 양식**입니다.

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# ✅ 1️⃣ Pydantic 모델 정의
class Landmark(BaseModel):
    name: str = Field(description="명소 이름")
    location: str = Field(description="명소가 위치한 도시")
    description: str = Field(description="짧은 설명")

# ✅ 2️⃣ LLM 정의
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ✅ 3️⃣ with_structured_output() 사용
structured_llm = llm.with_structured_output(Landmark)

# ✅ 4️⃣ 실행
result = structured_llm.invoke("서울의 유명한 명소 한 곳을 소개해 주세요.")
print("🏯 결과:")
print(result)

```

| 항목 | 설명 |
|------|------|
| **정적 타입 보장** | IDE 자동완성 및 타입 힌트 지원 |
| **형식 오류 방지** | 모델 출력이 스키마에 맞는지 자동 검증 |
| **활용성 높음** | ORM, DB 모델, FastAPI 응답 등과 연동 용이 |

---

{: .warning }
> **여기부터 심화 내용입니다.** StrOutputParser, JsonOutputParser, with_structured_output()만으로도 대부분의 상황을 처리할 수 있습니다. 아래 내용은 필요할 때 돌아와서 학습해도 됩니다.

<a id="part5"></a>

## 5. 실전 예시: JSON 결과를 DB로 저장하기 [↑](#toc)

```python {% raw %}
import sqlite3
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# 1️⃣ 모델 및 파서 설정
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = JsonOutputParser()

# ✅ 2️⃣ 중괄호 이스케이프 처리된 프롬프트
prompt = ChatPromptTemplate.from_template(
    '서울의 대표적인 관광지 3곳을 JSON 배열 형식으로 반환하세요. '
    '형식 예시: [{{"name": "경복궁", "location": "종로구"}}, '
    '{{"name": "남산타워", "location": "용산구"}}, '
    '{{"name": "북촌한옥마을", "location": "종로구"}}]'
)

# 3️⃣ LCEL 체인 구성
chain = prompt | llm | parser

# 4️⃣ 실행
results = chain.invoke({})

# 5️⃣ JSON 문자열일 경우 파싱
if isinstance(results, str):
    try:
        results = json.loads(results)
    except json.JSONDecodeError as e:
        print("❌ JSON 파싱 실패:", e)
        print("LLM 출력 내용:", results)
        raise

# 6️⃣ SQLite에 저장
conn = sqlite3.connect("tourist_spots.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS places (name TEXT, location TEXT)")

# 7️⃣ 데이터 삽입
for place in results:
    name = place.get("name")
    location = place.get("location")
    if name and location:
        cur.execute("INSERT INTO places (name, location) VALUES (?, ?)", (name, location))

conn.commit()
conn.close()

print("✅ 데이터가 DB에 성공적으로 저장되었습니다!"){% endraw %}
```
---

<a id="part6"></a>

## 🎯 실습 과제 [↑](#toc)

- **기본**: `StrOutputParser`와 `JsonOutputParser`를 각각 사용하여 "좋아하는 영화 3편"을 문자열/JSON으로 받아보세요
- **중급**: `with_structured_output()`으로 영화의 제목, 장르, 평점을 Pydantic 모델로 정의하고 받아보세요
- **심화**: JsonOutputParser로 받은 결과를 SQLite에 저장하는 코드를 작성해 보세요

> 💡 **Tip:** 실무에서는 `with_structured_output()`이 가장 안정적입니다. 타입 검증까지 자동으로 해주므로 프로그램이 예상치 못한 형태의 데이터를 받을 걱정이 없습니다.

