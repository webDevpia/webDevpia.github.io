---
title: 2. 프롬프트 기초 & CRAFT
layout: default
grand_parent: LLM
parent: 프롬프트 엔지니어링 기초
nav_order: 2
permalink: llm/prompt-basic/craft
---
# 2. 프롬프트 기초 & CRAFT 프레임워크

## 학습 목표

1. CRAFT 프레임워크로 프롬프트를 구조화할 수 있다
2. Zero-shot, Few-shot, Role Prompting 기법을 상황에 맞게 선택할 수 있다
3. JSON 구조화 출력과 한국어 프롬프트 팁을 활용할 수 있다

> **실습 환경**: 이 장은 ChatGPT 웹에서 바로 실습할 수 있습니다. API 코드 예시도 함께 제공합니다.

<a id="toc"></a>
## 진행 순서

1. [CRAFT 프레임워크](#part1)
2. [Zero-shot Prompting](#part2)
3. [Few-shot Prompting](#part3)
4. [Role Prompting](#part4)
5. [JSON 구조화 출력](#part5)
6. [한국어 프롬프트 팁](#part6)

---

<a id="part1"></a>
## 1. CRAFT 프레임워크 [↑](#toc)

프롬프트를 잘 쓰는 가장 쉬운 방법은 **구조를 따르는 것**입니다. CRAFT는 비전공자에게 가장 직관적인 프롬프트 프레임워크입니다.

### CRAFT = Context + Role + Action + Format + Tone

| 요소 | 의미 | 예시 |
|------|------|------|
| **C** - Context (맥락) | 배경과 상황 | "파이썬을 배우기 시작한 비전공자 학생입니다" |
| **R** - Role (역할) | AI가 맡을 전문가 | "친절한 파이썬 튜터로서" |
| **A** - Action (행동) | 구체적 작업 | "리스트와 딕셔너리의 차이를 설명해줘" |
| **F** - Format (형식) | 출력 구조 | "비교표 + 코드 예시 포함" |
| **T** - Tone (톤/대상) | 말투와 대상 | "프로그래밍을 처음 배우는 학생이 이해할 수 있게" |

### 실습: CRAFT 적용 Before vs After

**Before (구조 없음):**
```
파이썬 리스트 알려줘
```

**After (CRAFT 적용):**
```
[Context] 파이썬을 배우기 시작한 비전공자 학생입니다.
          리스트는 배웠는데 딕셔너리와의 차이가 헷갈립니다.

[Role]    당신은 친절한 파이썬 튜터입니다.

[Action]  리스트와 딕셔너리의 차이를 실생활 비유와 함께 설명해주세요.

[Format]  비교표 형식으로 정리하고, 각각 언제 쓰는지 코드 예시를 포함해주세요:
          | 항목 | 리스트 | 딕셔너리 |

[Tone]    프로그래밍을 처음 배우는 학생이 이해할 수 있게 쉽게 설명해주세요.
```

> **ChatGPT에서 바로 해보기**: 위 두 프롬프트를 각각 입력해보세요. 결과의 구체성이 완전히 다릅니다.

### CRAFT API 코드 예시

```python
# CRAFT 프레임워크를 API 코드로 적용
response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        # Role: system 메시지로 역할 설정
        {"role": "system", "content": "당신은 친절한 파이썬 튜터입니다. 비전공자 학생이 이해할 수 있게 비유를 활용해 설명합니다."},
        # Context + Action + Format: user 메시지로 전달
        {"role": "user", "content": """파이썬을 배우기 시작한 비전공자 학생입니다.
리스트와 딕셔너리의 차이를 설명하고, 각각 언제 쓰는지 코드 예시와 함께 비교표로 정리해주세요.

| 항목 | 리스트 | 딕셔너리 |"""}
    ]
)
print(response.choices[0].message.content)
```

### 주요 프레임워크 비교

| 프레임워크 | 구성 | 특징 | 난이도 |
|-----------|------|------|:---:|
| **CRAFT** | Context, Role, Action, Format, Tone | 범용적, 가장 좋은 시작점 | ★☆☆ |
| COSTAR | Context, Objective, Style, Tone, Audience, Response | 전문적, 세밀한 제어 | ★★☆ |
| RISEN | Role, Instructions, Steps, End goal, Narrowing | 복잡한 다단계 작업 | ★★★ |

**COSTAR** — CRAFT보다 **독자(Audience)**와 **응답 형식(Response)**을 명시적으로 분리합니다. "누가 읽는 글인가"를 별도 항목으로 지정하므로, 보고서·기획서처럼 **읽는 사람이 명확한 문서 작성**에 적합합니다. 싱가포르 GPT-4 프롬프트 대회에서 우승한 프레임워크입니다.

```
[Context]   딥러닝 수업에서 CNN 프로젝트를 진행 중
[Objective] 이미지 분류 모델의 성능을 개선하기 위한 방법 정리
[Style]     기술적이지만 이해하기 쉬운 설명
[Tone]      격려하는 선배 개발자의 톤
[Audience]  딥러닝을 처음 배우는 학부생
[Response]  방법 3가지, 각각 설명+코드 스니펫+예상 효과를 포함
```

**RISEN** — 작업의 **순서(Steps)**와 **하지 말 것(Narrowing)**을 명시합니다. "1단계→2단계→3단계" 처럼 **순서가 중요한 복잡한 작업**이나, 원하지 않는 결과를 사전에 배제할 때 유용합니다.

```
[Role]         파이썬 코드 리뷰어
[Instructions] 학생이 제출한 코드를 리뷰하고 개선점을 제안
[Steps]        1. 코드 동작 여부 확인 → 2. 버그 및 논리 오류 식별 → 3. 가독성/효율성 개선안 작성
[End goal]     학생이 바로 수정할 수 있는 피드백 문서
[Narrowing]    코드를 대신 작성하지 말 것, 힌트와 방향만 제시
```

> **권장**: 처음에는 **CRAFT만 익히세요**. 80%의 상황에서 충분합니다. COSTAR/RISEN은 더 정밀한 제어가 필요할 때 참고하세요.

---

<a id="part2"></a>
## 2. Zero-shot Prompting — 예시 없이 바로 지시 [↑](#toc)

**예시를 제공하지 않고** 바로 지시하는 방식입니다. 가장 간단하고 토큰을 절약할 수 있습니다.

### ChatGPT에서 바로 해보기

```
다음 파이썬 에러 메시지의 원인을 '문법 오류', '타입 오류', '인덱스 오류' 중 하나로 분류해주세요.

에러: "TypeError: unsupported operand type(s) for +: 'int' and 'str'"

분류:
```

### API 코드

```python
prompt = """다음 파이썬 에러 메시지의 원인을 '문법 오류', '타입 오류', '인덱스 오류' 중 하나로 분류해주세요.

에러: "TypeError: unsupported operand type(s) for +: 'int' and 'str'"

분류:"""

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[{"role": "user", "content": prompt}]
)
print(response.choices[0].message.content)
```

### 언제 쓰나?

| 적합 | 부적합 |
|------|--------|
| 단순 분류, 번역, 요약 | 특정 형식/스타일이 필요한 작업 |
| 빠른 테스트 | 높은 정확도가 필요한 작업 |

---

<a id="part3"></a>
## 3. Few-shot Prompting — 예시로 패턴 가르치기 [↑](#toc)

**2~3개의 입력-출력 예시**를 먼저 보여주고, 같은 패턴으로 새 입력을 처리하게 합니다.

### ChatGPT에서 바로 해보기

```
다음 파이썬 에러 메시지를 분류해주세요.

에러: "SyntaxError: invalid syntax"
분류: 문법 오류

에러: "IndexError: list index out of range"
분류: 인덱스 오류

에러: "NameError: name 'x' is not defined"
분류: 이름 오류

에러: "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
분류:
```

### API 코드

```python
few_shot_prompt = """다음 파이썬 에러 메시지를 분류해주세요.

에러: "SyntaxError: invalid syntax"
분류: 문법 오류

에러: "IndexError: list index out of range"
분류: 인덱스 오류

에러: "NameError: name 'x' is not defined"
분류: 이름 오류

에러: "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
분류:"""

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[{"role": "user", "content": few_shot_prompt}]
)
print(response.choices[0].message.content)
```

### Zero-shot vs Few-shot 비교

| 항목 | Zero-shot | Few-shot |
|------|-----------|---------|
| 예시 | 없음 | 2~5개 |
| 토큰 | 적음 | 예시만큼 추가 |
| 결과 일관성 | 낮을 수 있음 | **높음** |
| 적합한 상황 | 단순 작업 | 특정 형식/스타일이 필요한 작업 |

---

<a id="part4"></a>
## 4. Role Prompting — AI에게 역할 부여 [↑](#toc)

**system 메시지**로 AI에게 특정 전문가 역할을 부여합니다. 같은 질문도 역할에 따라 답변이 완전히 달라집니다.

### ChatGPT에서 바로 해보기

```
당신은 3년차 백엔드 개발자이고, 신입 교육을 담당하고 있습니다. 쉬운 비유를 활용해 설명합니다.

질문: "파이썬에서 클래스와 인스턴스의 차이가 뭔가요?"
```

같은 질문을 다른 역할로도 해보세요:
```
당신은 대학교 컴퓨터공학과 교수입니다. 정확한 개념 정의와 함께 학술적으로 설명합니다.

질문: "파이썬에서 클래스와 인스턴스의 차이가 뭔가요?"
```

### API 코드: 역할별 응답 비교

```python
def ask_with_role(role_desc, question):
    """역할을 부여하고 질문하는 함수"""
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": role_desc},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

question = "CNN(합성곱 신경망)이 이미지를 인식하는 원리를 설명해주세요."

roles = {
    "신입 교육 담당 사수": "당신은 3년차 ML 엔지니어이고 신입 교육을 담당합니다. 쉬운 비유와 그림을 활용해 설명합니다.",
    "대학교 교수": "당신은 컴퓨터공학과 교수입니다. 정확한 수학적 개념과 논문 레퍼런스를 포함하여 설명합니다.",
    "유튜브 크리에이터": "당신은 IT 유튜버입니다. 재미있는 예시와 밈을 활용해 누구나 이해할 수 있게 설명합니다.",
}

for name, role in roles.items():
    print(f"\n{'='*50}")
    print(f"[{name}]")
    print(ask_with_role(role, question))
```

### 역할 설정 시 팁

| 좋은 역할 설정 | 나쁜 역할 설정 |
|--------------|--------------|
| "3년차 ML 엔지니어, 신입 교육 담당" | "개발자" |
| "친절한 파이썬 튜터, 비유 활용" | "선생님" |
| "컴공 교수, 수학적 개념 포함" | "교수" |

> **핵심**: 역할에 **경력, 전문 분야, 설명 방식**을 구체적으로 명시할수록 결과가 좋아집니다.

---

<a id="part5"></a>
## 5. JSON 구조화 출력 [↑](#toc)

AI 응답을 **표나 JSON 형식**으로 받으면, 후속 처리(분석, 저장, 시각화)가 훨씬 쉬워집니다.

### ChatGPT에서 바로 해보기

```
다음 파이썬 라이브러리 정보를 JSON 형식으로 정리해주세요.

라이브러리: pandas, 데이터 분석, 설치: pip install pandas, 최신버전: 2.2, 난이도: 중급

다음 형식을 따라주세요:
{
  "name": "이름",
  "category": "분류",
  "install": "설치 명령어",
  "version": "버전",
  "level": "난이도"
}
```

### API 코드: JSON 강제 출력

```python
import json

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role": "system", "content": "응답은 반드시 JSON 형식으로만 출력하세요."},
        {"role": "user", "content": """다음 파이썬 라이브러리 정보를 JSON으로 정리해주세요.
라이브러리: pandas, 데이터 분석, 설치: pip install pandas, 최신버전: 2.2, 난이도: 중급"""}
    ],
    response_format={"type": "json_object"}   # JSON 형식 강제
)

# JSON 문자열 → 파이썬 딕셔너리로 변환
data = json.loads(response.choices[0].message.content)
print(f"이름: {data['name']}")
print(f"분류: {data['category']}")
print(json.dumps(data, indent=2, ensure_ascii=False))  # 보기 좋게 출력
```

> **주의**: `response_format={"type": "json_object"}` 사용 시, 메시지에 "JSON"이라는 단어가 반드시 포함되어야 합니다.

---

<a id="part6"></a>
## 6. 한국어 프롬프트 팁 [↑](#toc)

한국어는 주어와 목적어를 자주 생략하는 **고맥락 언어**입니다. 프롬프트에서는 **명시적으로 작성**해야 AI가 정확히 이해합니다.

### 개선 전후 비교

| 항목 | 모호한 버전 | 명시적 버전 |
|------|-----------|-----------|
| 주어 생략 | "설명해줘" | "**AI가 무엇인지** 설명해줘" |
| 대상 불명확 | "쉽게 써줘" | "**마케팅 팀장이** 이해할 수 있게 쉽게 써줘" |
| 조건 부재 | "요약해줘" | "핵심 내용만 **3문장으로** 요약해줘" |
| 형식 미지정 | "정리해줘" | "**표 형식으로** 정리해줘" |

### 효과적인 한국어 프롬프트 체크리스트

- ✅ **누가** 읽는 글인가? (대상 명시)
- ✅ **무엇을** 해야 하는가? (행동 명시)
- ✅ **몇 개**, **몇 문장**으로? (수량 제한)
- ✅ **어떤 형식**으로? (표, 목록, JSON 등)
- ✅ **하지 말 것**은? (제외 조건)

> **확인**: "딥러닝 알려줘"라는 프롬프트를 CRAFT 프레임워크로 개선해보세요. 5가지 요소(C, R, A, F, T)를 모두 포함하여 작성합니다.


→ **다음 장**: [3. 고급기법과 실전활용](/llm/prompt-basic/advanced)
