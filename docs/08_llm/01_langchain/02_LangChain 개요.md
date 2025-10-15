---
title: 2. langchain 개요
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 2
permalink: /llm/langchain/preview
--- 

# LangChain 개요 (v0.3.x 기준)

---

## 1. LangChain이란?

LangChain은 **대형 언어 모델(LLM)** 을 쉽고 체계적으로 다룰 수 있도록 도와주는 파이썬 프레임워크입니다.

> "LLM을 하나의 API로 끝내지 않고, 프롬프트 설계 → 모델 실행 → 결과 처리 → 메모리/도구 확장까지 단계적으로 조합할 수 있게 해주는 도구"입니다.

과거에는 OpenAI, Gemini, Ollama 등 각각의 모델 API를 따로 호출해야 했지만,
LangChain을 사용하면 공통 인터페이스로 다양한 모델을 연결할 수 있습니다.

---

## 2. LangChain의 핵심 구성요소

| 구성요소 | 역할 | 예시 클래스 | 설명 |
|-----------|------|--------------|------|
| **PromptTemplate** | 입력 설계 | `ChatPromptTemplate` | 사용자 입력을 템플릿 형태로 구성 |
| **Model(LLM)** | 모델 호출 | `ChatOpenAI`, `ChatGoogleGenerativeAI`, `OllamaLLM` | 실제 LLM API와 연결 |
| **OutputParser** | 결과 처리 | `StrOutputParser`, `JsonOutputParser` | 모델의 응답을 사람이 쓰기 좋은 형태로 변환 |
| **Memory** | 대화 맥락 유지 | `ConversationBufferMemory` 등 | 이전 대화를 기억하여 응답 품질 향상 |
| **LCEL** | 실행 파이프라인 | `prompt | llm | parser` | 체인을 연결하는 최신 방식 |
| **Tool / Agent** | 외부 기능 호출 | `create_tool_calling_agent` | 검색, 계산기, API 연동 등 |

---

## 3. 최신 패키지 구조 (LangChain v0.3)

LangChain은 2024년 이후 모듈이 분리되었습니다. 이제 하나의 패키지가 아닌 여러 모듈로 나뉩니다.

```
langchain-core          → 기본 구조 (Runnable, LCEL 등)
langchain-openai        → OpenAI 모델 (GPT 계열)
langchain-google-genai  → Gemini 모델
langchain-ollama        → Ollama 로컬 모델
langchain-community     → 커뮤니티 통합 기능 (Loaders, Tools 등)
```

> ✅ **핵심 요약:**
> `langchain-core`는 모든 프로젝트에 필수이며, 나머지는 필요한 모델/기능에 따라 선택 설치합니다.

---

## 4. 기본 사용 예제

###  0) 설치 및 환경 구성

```bash
pip install langchain langchain_community langchain_ollama langchain-openai langchain_google_genai python-dotenv
```

프로젝트 디렉토리에 `.env` 파일을 만들고 다음과 같이 API 키를 저장합니다 (따옴표 없이 입력):

```plaintext
OPENAI_API_KEY=sk-********************
GOOGLE_API_KEY=AI***********
```

```py
import langchain
from dotenv import load_dotenv
import os

load_dotenv()

print(f"langchain version: {langchain.__version__}")
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY') is not None}")
print(f"GOOGLE_API_KEY: {os.getenv('GOOGLE_API_KEY') is not None}")
```

### 🧠 1) Ollama 모델 예시
```python
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

ollama_url = "http://127.0.0.1:11434"  
llm = OllamaLLM(model="gemma3:1b", base_url=ollama_url)
prompt = ChatPromptTemplate.from_template("{city}에서 가장 유명한 랜드마크는?")

chain = prompt | llm
response = chain.invoke({"city": "서울"})

print(response)
```

### 🧠 3) lmstudio 모델 예시
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

lmstudio_url = "http://127.0.0.1:1234/v1"
llm = ChatOpenAI(model="gemma-3-4b-it", base_url=lmstudio_url, api_key="dummy")

prompt = ChatPromptTemplate.from_template("{city}에서 가장 유명한 랜드마크는?")

chain = prompt | llm
response = chain.invoke({"city": "서울"})

print(response.content)
```


### 🧠 4) OpenAI 모델 예시
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template("{city}에서 가장 유명한 랜드마크는?")

chain = prompt | llm
response = chain.invoke({"city": "서울"})

print(response.content)
```

### 🤖 5) Gemini 모델 예시
```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))

prompt = ChatPromptTemplate.from_template("{city}의 대표적인 음식은?")

chain = prompt | llm
result = chain.invoke({"city": "파리"})

print(result.content)
```

> ✅ `.invoke()`는 LCEL에서 표준 실행 메서드입니다. 예전의 `.run()`보다 더 강력하고 유연합니다.

---

## 5. LCEL (LangChain Expression Language)

LCEL은 LangChain 1.x 버전 이후 도입된 **표현 언어(파이프라인 연결 시스템)** 입니다.

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("{topic}에 대한 한 문장 요약을 작성해 주세요.")
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke({"topic": "LangChain"})
print(result)
```

📊 **데이터 흐름 시각화:**
```
입력 → Prompt → LLM → Parser → 출력
```

이처럼 LCEL은 각 단계를 **Runnable 객체**로 연결하여, 직관적이고 디버깅하기 쉬운 구조를 제공합니다.

---

## 6. 정리 요약

| 핵심 개념 | 설명 |
|-------------|------|
| **LangChain** | LLM 기반 애플리케이션 개발 프레임워크 |
| **LCEL** | LangChain Expression Language, 체인 연결 방식 |
| **invoke()** | LCEL 실행 메서드 (이전 run() 대체) |
| **Runnable** | LangChain의 모든 실행 가능한 단위 객체 |
| **Prompt LLM Parser** | LCEL 파이프라인의 기본 구성 |

✅ **한 줄 요약:**  
LangChain은 LLM을 단순 호출에서 벗어나, **“프롬프트 → 모델 → 결과”의 체계를 손쉽게 조립하는 플랫폼**입니다.
