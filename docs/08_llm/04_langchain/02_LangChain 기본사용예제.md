---
title: 2. 기본 사용 예제
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 2
permalink: /llm/langchain/example
---


## 학습 목표

- 다양한 LLM(Ollama, OpenAI, Gemini)을 LangChain으로 호출할 수 있다
- LCEL 파이프 문법의 기본 패턴(`prompt | llm | parser`)을 이해한다

<a id="toc"></a>

## 진행 순서

1. [환경 구성](#part1)
2. [Ollama 모델](#part2)
3. [LM Studio 모델 (OpenAI 호환)](#part3)
4. [OpenAI 모델](#part4)
5. [Gemini 모델](#part5)
6. [공통 패턴 정리](#part6)


---

# LangChain 기본 사용 예제

> LangChain 개요와 핵심 개념은 [LangChain 메인 페이지](/llm/langchain)를 참고합니다.

---

<a id="part1"></a>

## 환경 구성 [↑](#toc)

프로젝트 디렉토리에 `.env` 파일을 만들고 API 키를 저장합니다 (따옴표 없이 입력):

```plaintext
OPENAI_API_KEY=sk-********************
GOOGLE_API_KEY=AI***********
```

```python
from dotenv import load_dotenv
import os

load_dotenv()

print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY') is not None}")
print(f"GOOGLE_API_KEY: {os.getenv('GOOGLE_API_KEY') is not None}")
```

출력 예:
```
OPENAI_API_KEY: True
GOOGLE_API_KEY: True
```

---

<a id="part2"></a>

## 1) Ollama 모델 [↑](#toc)

```python
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="gemma3:1b", base_url="http://127.0.0.1:11434")
prompt = ChatPromptTemplate.from_template("{city}에서 가장 유명한 랜드마크는?")
parser = StrOutputParser()

chain = prompt | llm | parser
response = chain.invoke({"city": "서울"})

print(response)
```

출력 예:
```
서울에서 가장 유명한 랜드마크는 경복궁입니다. 조선 왕조의 대표적인 궁궐로...
```

> `ChatOllama`는 채팅 모델 래퍼로, `ChatPromptTemplate`과 함께 사용할 때 권장됩니다.
> 단순 문자열 입출력만 필요하면 `OllamaLLM`도 사용 가능하다.

---

<a id="part3"></a>

## 2) LM Studio 모델 (OpenAI 호환) [↑](#toc)

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gemma-3-4b-it", base_url="http://127.0.0.1:1234/v1", api_key="dummy")
prompt = ChatPromptTemplate.from_template("{city}에서 가장 유명한 랜드마크는?")
parser = StrOutputParser()

chain = prompt | llm | parser
response = chain.invoke({"city": "서울"})

print(response)
```

> LM Studio는 OpenAI 호환 API를 제공하므로 `ChatOpenAI`에 `base_url`만 지정하면 됩니다.

---

<a id="part4"></a>

## 3) OpenAI 모델 [↑](#toc)

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# colab 에서 
# import os
# from google.colab import userdata
# os.environ['OPENAI_API_KEY'] = userdata.get('OPENAI_API_KEY')

# 로컬에서 
from dotenv import load_dotenv
# .env 파일에서 OPENAI_API_KEY를 자동으로 읽어옴
load_dotenv()

# import os
# print(os.getenv("OPENAI_API_KEY"))

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("{city}에서 가장 유명한 랜드마크는?")
parser = StrOutputParser()

chain = prompt | llm | parser
response = chain.invoke({"city": "서울"})

print(response)
```

---

<a id="part5"></a>

## 4) Gemini 모델 [↑](#toc)

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
prompt = ChatPromptTemplate.from_template("{city}의 대표적인 음식은?")
parser = StrOutputParser()

chain = prompt | llm | parser
result = chain.invoke({"city": "파리"})

print(result)
```

출력 예:
```
파리의 대표적인 음식으로는 크루아상, 에스카르고(달팽이 요리), 크렘 브륄레...
```

> `GOOGLE_API_KEY` 환경변수가 설정되어 있으면 `api_key` 파라미터는 생략 가능합니다.

---

<a id="part6"></a>

## 공통 패턴 정리 [↑](#toc)

모든 예제는 동일한 LCEL 패턴을 따릅니다:

```
Prompt → Chat Model → Output Parser
```

```python
chain = prompt | llm | parser
result = chain.invoke({"변수명": "값"})
```

| 메서드 | 설명 |
|---|---|
| `.invoke()` | 단일 입력 실행 |
| `.stream()` | 스트리밍 출력 |
| `.batch()` | 여러 입력 일괄 실행 |
