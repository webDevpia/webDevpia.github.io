---
title: 5. Parser
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 5
permalink: /llm/langchain/parser
--- 
# LangChain 출력 파서 (v0.3.x 기준 개선 버전, v2)

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
from langchain.prompts import ChatPromptTemplate
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

## 3. JSON 형식 강제 — `JsonOutputParser`

LLM이 JSON 형식으로 데이터를 주도록 강제하고 싶다면 `JsonOutputParser`를 사용합니다.

```python
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate
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

## 4. 구조적 응답 보장 — `StructuredOutputParser`

`StructuredOutputParser`는 **출력 구조를 미리 정의**할 수 있는 고급 파서입니다.

```python
from langchain.output_parsers.structured import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 1️⃣ 출력 스키마 정의
schemas = [
    ResponseSchema(name="name", description="랜드마크 이름"),
    ResponseSchema(name="location", description="도시명"),
]

# 2️⃣ StructuredOutputParser 생성
parser = StructuredOutputParser.from_response_schemas(schemas)

# 3️⃣ 모델에게 출력 형식을 지시할 포맷 정보
format_instructions = parser.get_format_instructions()
print("📘 출력 형식 지침:")
print(format_instructions)
print("=" * 50)

# 4️⃣ 프롬프트 구성
prompt = ChatPromptTemplate.from_template(
    "서울의 대표적인 명소 중 하나를 소개하세요.\n\n{format_instructions}"
)

# 5️⃣ LLM 연결
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 6️⃣ 체인 구성
chain = prompt | llm | parser

# 7️⃣ 실행
result = chain.invoke({"format_instructions": format_instructions})

# 8️⃣ 결과 출력
print("🏯 실제 모델 응답 (파싱된 결과):")
print(result)
```

출력 예시:
```
응답을 아래 JSON 형식으로 작성하세요:
{"name": string, "location": string}

🏯 실제 모델 응답 (파싱된 결과):
{'name': '경복궁', 'location': '서울'}
```

이 포맷을 프롬프트에 포함하면 LLM이 **정해진 스키마로 일관된 결과**를 반환하게 됩니다.

---

## 5. 오류 자동 보정 — `OutputFixingParser`

LLM이 JSON 형식을 약간 틀리게 반환하더라도 자동으로 수정할 수 있습니다.

```python
from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
parser = OutputFixingParser.from_llm(parser=JsonOutputParser(), llm=llm)

broken_json = '{"name": "경복궁" "location": "서울"}'  # 콤마 누락
fixed = parser.invoke(broken_json)
print(fixed)
```

출력 예시:
```python
{"name": "경복궁", "location": "서울"}
```

> ⚙️ LLM이 잘못된 JSON을 반환하더라도 `OutputFixingParser`가 자동으로 고쳐줍니다.

---

## 6. 재시도 기반 복구 — `RetryOutputParser`

형식 오류가 발생하면 **모델에게 재요청을 보내 자동 복구**하는 파서입니다.

```python
from langchain.output_parsers.retry import RetryOutputParser
from langchain.output_parsers.structured import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 1️⃣ LLM 설정
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2️⃣ 기본 파서 정의
schemas = [
    ResponseSchema(name="name", description="명소 이름"),
    ResponseSchema(name="region", description="지역명"),
]
base_parser = StructuredOutputParser.from_response_schemas(schemas)

# 3️⃣ RetryOutputParser 생성
retry_parser = RetryOutputParser.from_llm(llm=llm, parser=base_parser)

# 4️⃣ 프롬프트 구성
prompt = PromptTemplate.from_template(
    "서울의 명소 한 곳을 아래 JSON 형식으로 작성하세요.\n\n{format_instructions}"
)
format_instructions = base_parser.get_format_instructions()

# 5️⃣ LLM 호출
prompt_value = prompt.format_prompt(format_instructions=format_instructions)
model_output = llm.invoke(prompt_value)

# 6️⃣ 파서로 파싱 (자동 재시도 포함)
result = retry_parser.parse_with_prompt(model_output.content, prompt_value)

print("✅ 파싱된 결과:", result)
```

> 💡 모델이 잘못된 형식으로 응답하면 LangChain이 **자동으로 재시도**합니다.

---

## 7. 정적 타입 검증 — `PydanticOutputParser`

`PydanticOutputParser`는 Python의 **데이터 모델링 도구**인 `pydantic`을 이용하여  
LLM 출력의 형식을 **엄격하게 보장**합니다.

```python
ffrom pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# ✅ 1️⃣ Pydantic 모델 정의
class Landmark(BaseModel):
    name: str = Field(description="명소 이름")
    location: str = Field(description="명소가 위치한 도시")
    description: str = Field(description="짧은 설명")

# ✅ 2️⃣ 파서 생성
parser = PydanticOutputParser(pydantic_object=Landmark)

# ✅ 3️⃣ 포맷 지침 생성
format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_template("서울의 유명한 명소 한 곳을 소개하세요.{format_instructions}")

# ✅ 4️⃣ LCEL 체인으로 연결
llm = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | llm | parser

# ✅ 5️⃣ 실행
result = chain.invoke({"format_instructions": format_instructions})
print(result)

```

| 항목 | 설명 |
|------|------|
| **정적 타입 보장** | IDE 자동완성 및 타입 힌트 지원 |
| **형식 오류 방지** | 모델 출력이 스키마에 맞는지 자동 검증 |
| **활용성 높음** | ORM, DB 모델, FastAPI 응답 등과 연동 용이 |

---

## 8. 실전 예시: JSON 결과를 DB로 저장하기

```python
import sqlite3
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# 1️⃣ 모델과 파서 설정
llm = ChatOpenAI(model="gpt-4o-mini")
parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template(
    "서울의 관광지 3곳을 JSON 배열로 반환하세요."
)
chain = prompt | llm | parser

# 2️⃣ LLM 실행 → JSON 결과 받기
results = chain.invoke({})

# 3️⃣ SQLite에 저장
conn = sqlite3.connect("tourist_spots.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS places (name TEXT, location TEXT)")

for place in results:
    cur.execute("INSERT INTO places (name, location) VALUES (?, ?)", 
                (place["name"], place["location"]))

conn.commit()
conn.close()

print("✅ 데이터가 DB에 성공적으로 저장되었습니다!")
```
---

## 9. 최신 LCEL 스타일 요약

| 파서 | 설명 | 특징 |
|------|------|------|
| `StrOutputParser` | 문자열 반환 | 기본 파서 |
| `JsonOutputParser` | JSON → dict | 가장 일반적 |
| `StructuredOutputParser` | 스키마 기반 JSON | 일관된 구조 보장 |
| `PydanticOutputParser` | Pydantic 모델 기반 | 정적 타입 안전성 |
| `OutputFixingParser` | 오류 자동 수정 | 복원 기능 |
| `RetryOutputParser` | 재시도 기반 복구 | 안정성 강화 |

---

## 🎯 실습 포인트

1. LLM 응답이 불안정하다면 반드시 파서를 사용하세요.  
2. `JsonOutputParser`는 API 연동 및 DB 저장 시 매우 유용합니다.  
3. `StructuredOutputParser`는 모델의 일관성을 높이고 후처리를 단순화합니다.  
4. `PydanticOutputParser`는 타입 안정성과 유지보수성을 모두 강화합니다.  
5. `OutputFixingParser`와 `RetryOutputParser`를 결합하면 **실패율 0%에 가까운 안정성**을 확보할 수 있습니다.

---

> 💡 **Tip:** OutputParser는 단순한 보조 도구가 아니라, LLM을 **API처럼 안정적으로 제어**하기 위한 핵심 구성 요소입니다.
