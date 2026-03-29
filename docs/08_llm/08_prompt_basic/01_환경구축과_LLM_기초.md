---
title: 1. 환경 구축과 LLM 기초
layout: default
parent: 프롬프트 엔지니어링 기초
grand_parent: LLM
nav_order: 1
permalink: /llm/prompt-basic/setup
---

# 1. 환경 구축과 LLM 기초

<a id="toc"></a>

## 진행 순서

1. [개발 환경 확인](#part1) - Colab 접속, API 키 등록, openai 설치, 첫 API 호출
2. [LLM이란?](#part2) - 토큰 예측 모델의 원리, 주요 모델 비교
3. [주요 파라미터 체험](#part3) - temperature, top_p 등 파라미터 의미와 실습

---

<a id="part1"></a>

## 1. 개발 환경 확인 [↑](#toc)

**학습목표**: Google Colab에서 OpenAI API 키를 등록하고 첫 번째 API 호출을 성공적으로 실행할 수 있다.

### API 키 등록 방법

Google Colab 좌측 패널에서 `🔑 Secrets` 탭을 클릭한 뒤 `+ 새 비밀 추가`를 눌러 다음과 같이 입력합니다.

| 항목 | 값 |
|------|----|
| 이름 | `OPENAI_API_KEY` |
| 값 | 발급받은 API 키 (`sk-...`) |
| 노트북 액세스 | 켜기 |

### openai 패키지 설치

```python
# openai 패키지 설치 (Colab에는 미리 설치되어 있지만 최신 버전 확인용)
!pip install -q openai
```

### 클라이언트 생성 및 첫 API 호출

```python
import os
from openai import OpenAI

# Colab Secrets에서 API 키 가져오기
from google.colab import userdata
os.environ['OPENAI_API_KEY'] = userdata.get('OPENAI_API_KEY')

# OpenAI 클라이언트 생성
client = OpenAI()

# 첫 번째 API 호출
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Python의 리스트와 딕셔너리의 차이를 신입 개발자도 이해할 수 있게 설명해주세요."}]
)

# 응답 출력
print(response.choices[0].message.content)
```

**핵심**: `client.chat.completions.create()`가 기본 호출 형태이며, `messages` 리스트에 대화를 담아 전달한다. `response.choices[0].message.content`로 텍스트 응답을 꺼낸다.

> **확인**: API 호출 후 응답이 정상적으로 출력되는가? 오류가 발생한다면 API 키 등록과 노트북 액세스 설정을 다시 확인한다.

---

<a id="part2"></a>

## 2. LLM이란? [↑](#toc)

**학습목표**: LLM의 핵심 작동 원리를 한 문장으로 설명하고, 주요 모델의 특징을 비교할 수 있다.

### 한 줄 정의

> **LLM(Large Language Model)**: 방대한 텍스트 데이터로 학습하여 **다음에 올 토큰을 예측**하는 거대한 언어 모델.

"토큰"은 단어 또는 단어의 일부(한국어는 보통 글자 단위)이며, LLM은 앞선 토큰들을 보고 가장 자연스러운 다음 토큰을 반복적으로 생성하면서 문장을 완성합니다.

### 2026년 3월 현재 주요 모델 비교

| 모델 | 제공사 | 특징 | 강점 |
|------|--------|------|------|
| **GPT-4.1 mini** | OpenAI | GPT-4o 대비 83% 저렴, 절반의 지연시간 | 빠른 응답, 실습 최적 |
| GPT-4.1 | OpenAI | 코딩·지시 따르기 특화 | 정밀한 코드 생성 |
| **Claude Sonnet 4.6** | Anthropic | 1M 토큰 컨텍스트, 강력한 코드 분석 | 코드 리뷰·문서 분석 |
| **Gemini 3 Flash** | Google | 멀티모달, 고속 추론 | 대용량 파일·이미지 처리 |
| **Llama 4 Scout** | Meta | 오픈소스, 10M 컨텍스트 | 로컬 실행, 커스터마이징 |

> **참고**: GPT-4o는 2026년 2월 ChatGPT에서 퇴역되었으나, API에서는 아직 사용 가능합니다. 신규 프로젝트에는 GPT-4.1 시리즈를 권장합니다.

### 실습용 모델 선택

이 과정에서는 비용 효율이 높은 **`gpt-4o-mini`** 를 기본 모델로 사용합니다. GPT-4.1 mini가 더 최신이지만, `gpt-4o-mini`는 여전히 API에서 지원되며 풍부한 예제와 문서가 있어 학습에 적합합니다.

> **팁**: 실습 후 `model="gpt-4.1-mini"`로 교체하여 성능 차이를 비교해 보세요.

**핵심**: LLM은 "다음 토큰 예측"을 반복하는 모델이다. 프롬프트를 어떻게 작성하느냐에 따라 예측 방향이 달라지기 때문에 프롬프트 엔지니어링이 중요하다.

> **확인**: GPT-4o와 GPT-4o-mini의 차이는 무엇인가? 어떤 상황에서 각각을 선택하면 좋을까?

---

<a id="part3"></a>

## 3. 주요 파라미터 체험 [↑](#toc)

**학습목표**: temperature, top_p 등 주요 파라미터의 의미를 설명하고, 파라미터 변경이 출력에 미치는 영향을 직접 확인할 수 있다.

### 주요 파라미터 정리

| 파라미터 | 기본값 | 범위 | 의미 |
|----------|--------|------|------|
| `temperature` | 1.0 | 0 ~ 2 | 높을수록 창의적·다양, 낮을수록 결정적·일관 |
| `top_p` | 1.0 | 0 ~ 1 | 누적 확률 상위 토큰만 고려 (temperature와 중복 사용 주의) |
| `max_tokens` | 모델 최대 | 정수 | 생성할 최대 토큰 수 |
| `n` | 1 | 정수 | 한 번 호출로 생성할 응답 수 |

> `temperature`와 `top_p`는 동시에 조정하지 않는 것을 권장합니다. 하나를 고정하고 나머지 하나만 변경하세요.

### temperature 비교 실습

```python
prompt = "신입 개발자가 첫 출근 전에 준비하면 좋을 것 한 가지를 추천해주세요."

for temp in [0.0, 0.7, 1.5]:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temp,
        max_tokens=100
    )
    print(f"[temperature={temp}]")
    print(response.choices[0].message.content)
    print()
```

### max_tokens 제한 실습

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "REST API가 무엇인지 한 문단으로 설명해주세요."}],
    max_tokens=50  # 응답을 50 토큰으로 제한
)
print(response.choices[0].message.content)
```

**핵심**: 같은 프롬프트도 파라미터에 따라 결과가 달라진다. `temperature=0`에 가까울수록 재현성이 높아지고, 높아질수록 다양하고 창의적인 답변이 나온다.

> **확인**: temperature를 0과 1.5로 설정하여 같은 프롬프트를 3번씩 실행해보자. 결과가 얼마나 달라지는가?
