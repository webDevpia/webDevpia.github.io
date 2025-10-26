---
title: 5. Parser
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 5
permalink: /llm/langchain/parser
--- 
# LangChain 출력 파서 (v1)

## 1. 출력 파서(Output Parser)란?

LLM의 출력은 사람이 읽기에는 편하지만, **프로그램이 처리하기에는 불안정**한 경우가 많습니다.  
예를 들어 다음과 같은 문제가 생길 수 있습니다.

- 응답이 문장 형태로 들쭉날쭉함  
- JSON 형식이 깨져서 파싱 오류 발생  
- 숫자, 리스트 등의 구조적 데이터가 섞임  

➡️ **OutputParser**는 LLM 응답을 일정한 형식으로 가공해주는 도구입니다.

---

## 2. 기본 사용법 — `StrOutputParser`

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-5-nano")
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

## 3. JSON 형식 강제 — `JsonOutputParser`

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

## 4. 정적 타입 검증 — `with_structured_output()`

Python의 **데이터 모델링 도구**인 `pydantic`을 이용하여 LLM 출력의 형식을 **엄격하게 보장**합니다.

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# ✅ 1️⃣ Pydantic 모델 정의
class Landmark(BaseModel):
    name: str = Field(description="명소 이름")
    location: str = Field(description="명소가 위치한 도시")
    description: str = Field(description="짧은 설명")

# ✅ 2️⃣ LLM 정의
llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

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

## 5. 실전 예시: JSON 결과를 DB로 저장하기

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

## 🎯 실습 포인트

LLM 응답이 불안정하다면 반드시 파서를 사용하세요.  

