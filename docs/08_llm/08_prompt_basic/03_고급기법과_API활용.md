---
title: 3. 고급 기법과 API 활용
layout: default
parent: 프롬프트 엔지니어링 기초
grand_parent: LLM
nav_order: 3
permalink: /llm/prompt-basic/advanced
---

# 3. 고급 기법과 API 활용

<a id="toc"></a>

## 진행 순서

1. [Chain-of-Thought Prompting](#part1) - 단계별 추론으로 정확도 향상
2. [구조화된 프롬프트 작성법](#part2) - 마크다운, 조건, 출력 형식 지정
3. [Python API 활용](#part3) - 배치 처리, 응답 시간, 토큰 사용량
4. [DAY1 복습 질문](#part4) - 핵심 개념 확인
5. [DAY1 심화 과제](#part5) - 스스로 도전해보기

---

<a id="part1"></a>

## 1. Chain-of-Thought Prompting [↑](#toc)

**학습목표**: CoT 프롬프트가 복잡한 추론 문제에서 정확도를 높이는 원리를 설명하고, CoT 없음/있음을 비교 실험할 수 있다.

### 개념

"단계별로 생각해 보세요(Let's think step by step)"라는 한 줄을 추가하는 것만으로도 수학, 논리, 코드 디버깅 등 복잡한 추론 문제에서 정확도가 크게 향상됩니다.

### CoT 없음 vs CoT 있음 비교

```python
import time

# 테스트 문제
problem = """
다음 Flask 코드에서 /users 엔드포인트 호출 시 500 에러가 발생합니다. 원인이 무엇인가요?

from flask import Flask, jsonify
app = Flask(__name__)

users = None

@app.route('/users')
def get_users():
    return jsonify(users.values())
"""

# CoT 없음
no_cot_prompt = problem + "\n답:"

# CoT 있음
cot_prompt = problem + "\n단계별로 분석해 보세요.\n답:"

print("=== CoT 없음 ===")
resp_no_cot = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": no_cot_prompt}],
    temperature=0  # 재현성을 위해 0으로 설정
)
print(resp_no_cot.choices[0].message.content)

print("\n=== CoT 있음 ===")
resp_cot = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": cot_prompt}],
    temperature=0
)
print(resp_cot.choices[0].message.content)
```

### CoT가 효과적인 상황

| 상황 | 예시 |
|------|------|
| 수학 계산 | 다단계 사칙연산, 비율 계산 |
| 논리 추론 | 조건이 여러 개인 문제 |
| 코드 디버깅 | 오류 원인 분석 |
| 의사결정 | 장단점 비교 후 결론 도출 |

### 구조화된 CoT 프롬프트

```python
structured_cot = """다음 SQL 쿼리가 느린 이유를 분석하고 개선해주세요.

SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
ORDER BY o.total_price DESC;

다음 형식으로 답해주세요:
1단계 - 현재 쿼리의 문제점:
2단계 - 성능 저하 원인 분석:
3단계 - 개선된 쿼리:
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": structured_cot}],
    temperature=0
)
print(response.choices[0].message.content)
```

**핵심**: 복잡한 추론에서는 CoT가 정확도를 크게 향상시킨다. 모델이 중간 과정을 출력하게 만드는 것이 핵심이다.

> **확인**: CoT 프롬프트를 사용할 때와 사용하지 않을 때, 답변의 정확도와 설명의 질이 어떻게 다른가?

---

<a id="part2"></a>

## 2. 구조화된 프롬프트 작성법 [↑](#toc)

**학습목표**: 마크다운 형식, 조건 명시, 출력 형식 지정을 활용하여 복잡한 작업을 명확하게 지시할 수 있다.

### 마크다운 형식 활용

복잡한 지시 사항은 마크다운 구조로 작성하면 모델이 각 요구 사항을 구분하기 쉽습니다.

```python
structured_prompt = """# 역할
당신은 IT 기업의 채용 담당자입니다.

## 작업
아래 지원자 정보를 바탕으로 면접 질문 3개를 만들어주세요.

## 지원자 정보
- 직무: 백엔드 개발자
- 경력: 신입
- 주요 기술: Python, Django, MySQL

## 제약 조건
- 반드시 코딩 관련 질문 1개, 시스템 설계 질문 1개, 인성 질문 1개를 포함해야 한다
- 각 질문은 1~2문장으로 작성한다
- 번호를 붙여 목록 형식으로 출력한다

## 출력 형식
1. [코딩] 질문 내용
2. [시스템 설계] 질문 내용
3. [인성] 질문 내용
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": structured_prompt}]
)
print(response.choices[0].message.content)
```

### 조건 명시 패턴

| 패턴 | 예시 |
|------|------|
| 반드시 포함 | "반드시 ~를 포함해야 한다" |
| 금지 사항 | "~하지 마라", "~는 제외한다" |
| 우선순위 | "가장 중요한 것부터 나열한다" |
| 수량 제한 | "3개 이내로", "최소 2개" |

### 출력 형식 지정 예시

```python
format_examples = {
    "JSON": "JSON 형식으로 반환해주세요.",
    "표": "마크다운 표 형식으로 정리해주세요.",
    "3줄 요약": "핵심 내용을 bullet point 3줄로 요약해주세요.",
    "단계별": "1단계, 2단계, 3단계 형식으로 설명해주세요.",
    "비교": "장점과 단점을 나누어 설명해주세요."
}

# 표 형식 출력 예시
table_prompt = """Python과 JavaScript를 신입 개발자의 첫 웹 프로젝트 관점에서 비교하는 표를 만들어주세요.
비교 항목: 학습 곡선, 취업 수요, 풀스택 가능 여부, 대표 프레임워크, 커뮤니티 활성도
마크다운 표 형식으로 출력해주세요."""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": table_prompt}]
)
print(response.choices[0].message.content)
```

**핵심**: 구조화된 프롬프트는 긴 지시 사항을 명확하게 전달한다. 제약 조건을 "반드시"와 "하지 마라"로 명시하면 모델이 놓치는 경우를 줄일 수 있다.

> **확인**: 구조 없이 한 단락으로 작성한 프롬프트와 마크다운 구조로 작성한 프롬프트를 비교해보자. 어떤 차이가 있는가?

---

<a id="part3"></a>

## 3. Python API 활용 [↑](#toc)

**학습목표**: 여러 프롬프트를 배치로 처리하고, 응답 시간과 토큰 사용량을 측정할 수 있다.

### 기본 호출 구조 정리

```python
# 기본 호출 구조 전체 흐름
response = client.chat.completions.create(
    model="gpt-4o-mini",          # 사용할 모델
    messages=[                     # 대화 메시지 목록
        {"role": "system", "content": "시스템 지시"},
        {"role": "user", "content": "사용자 입력"}
    ],
    temperature=0.7,               # 창의성 조절 (0~2)
    max_tokens=500,                # 최대 출력 토큰
    n=1,                           # 생성할 응답 수
)

# 응답에서 텍스트 추출
text = response.choices[0].message.content
```

### 여러 프롬프트 배치 처리

```python
# 여러 주제에 대해 한 줄 설명 생성
topics = ["Docker", "CI/CD", "REST API", "GraphQL"]

results = []
for topic in topics:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"{topic}을(를) 신입 개발자도 이해할 수 있게 한 문장으로 설명해주세요."}],
        max_tokens=100
    )
    result = response.choices[0].message.content.strip()
    results.append({"topic": topic, "description": result})
    print(f"[{topic}] {result}")
```

### 응답 시간 측정

```python
import time

def timed_completion(prompt, model="gpt-4o-mini"):
    """응답 시간을 측정하는 함수"""
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    elapsed = time.time() - start
    text = response.choices[0].message.content
    print(f"응답 시간: {elapsed:.2f}초")
    print(f"응답 길이: {len(text)}자")
    return text

# 짧은 응답 vs 긴 응답 시간 비교
print("=== 짧은 응답 ===")
timed_completion("다음 코드의 시간 복잡도를 Big-O 표기법 한 줄로만 답해주세요.\n\nfor i in range(n):\n    for j in range(n):\n        print(i, j)")

print("\n=== 긴 응답 ===")
timed_completion("2026년 현재 신입 웹 개발자가 알아야 할 핵심 기술 스택을 프론트엔드, 백엔드, 인프라로 나누어 500자로 정리해주세요.")
```

### 토큰 사용량 확인

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Python, JavaScript, TypeScript의 웹 백엔드 프레임워크를 각각 1개씩 추천하고 장단점을 비교해주세요."}]
)

# 토큰 사용량 출력
usage = response.usage
print(f"입력 토큰:  {usage.prompt_tokens}")
print(f"출력 토큰:  {usage.completion_tokens}")
print(f"총 토큰:    {usage.total_tokens}")

# 비용 추정 (gpt-4o-mini 기준, 2026년 3월 기준 근사값)
input_cost = usage.prompt_tokens * 0.00000015   # $0.15 / 1M tokens
output_cost = usage.completion_tokens * 0.0000006  # $0.60 / 1M tokens
print(f"예상 비용:  ${input_cost + output_cost:.6f}")
```

### 토큰 절약 팁

| 방법 | 효과 |
|------|------|
| `max_tokens` 제한 | 불필요하게 긴 응답 차단 |
| 프롬프트 간결화 | 입력 토큰 절감 |
| `gpt-4o-mini` 선택 | GPT-4o 대비 약 10배 저렴 |
| Few-shot 예시 최소화 | 예시당 수십~수백 토큰 절약 |

**핵심**: `response.usage`로 실제 사용 토큰을 항상 모니터링하자. 배치 처리 시에는 불필요한 반복 호출을 줄이는 것이 비용 절감의 핵심이다.

> **확인**: 같은 작업을 `gpt-4o`와 `gpt-4o-mini`로 각각 실행하여 응답 시간과 품질을 비교해보자.

---

<a id="part4"></a>

## 4. DAY1 복습 질문 [↑](#toc)

**학습목표**: DAY1에서 배운 핵심 개념을 스스로 설명할 수 있다.

1. **Zero-shot과 Few-shot의 차이는 무엇인가?**
   - 예시 제공 여부와 그로 인한 출력 품질의 차이를 설명해보자.

2. **Role Prompting에서 system 메시지의 역할은 무엇인가?**
   - user 메시지와 system 메시지의 차이를 생각해보자.

3. **CoT가 효과적인 상황은 언제인가?**
   - 단순 질문 응답과 복잡한 추론 과제를 비교해보자.

4. **temperature 0과 1의 차이는 무엇인가?**
   - 어떤 작업에 각각 적합한지 예를 들어 설명해보자.

5. **토큰이란 무엇인가?**
   - "안녕하세요"는 몇 개의 토큰일까? 영어와 한국어의 토큰 효율 차이는?

---

<a id="part5"></a>

## 5. DAY1 심화 과제 [↑](#toc)

**학습목표**: 배운 기법을 조합하여 스스로 문제를 해결할 수 있다.

### 과제 1: 자동 뉴스 요약기

여러 뉴스 기사 텍스트를 입력받아 다음 형식으로 요약하는 코드를 작성하세요.

```
제목: (한 줄)
핵심 요약: (2~3문장)
키워드: (5개, 쉼표 구분)
카테고리: 정치/경제/사회/문화/IT 중 하나
```

- Zero-shot과 Few-shot 버전을 각각 만들어 결과를 비교할 것
- JSON 형식으로 출력되도록 `response_format`을 활용할 것

### 과제 2: 역할별 이메일 작성기

같은 내용("미팅 일정 변경 요청")을 다음 3가지 역할로 작성하는 코드를 만드세요.
- 상사에게 보내는 공식적인 이메일
- 동료에게 보내는 편안한 이메일
- 고객에게 보내는 정중한 이메일

각 이메일의 어조와 표현 방식의 차이를 분석해보세요.

### 과제 3: CoT 수학 풀이 검증기

5개의 수학 문제를 CoT 프롬프트로 풀게 한 뒤, 각 문제의 정답 여부를 확인하는 코드를 작성하세요.
- `temperature=0`으로 설정하여 재현성 확보
- 풀이 과정과 최종 답을 JSON으로 출력하도록 구조화
- 정답률을 계산하여 출력

**핵심**: DAY1의 핵심은 프롬프트 설계가 결과를 결정한다는 것이다. Zero-shot → Few-shot → Role → CoT 순서로 기법을 쌓아가면 점점 더 정교한 결과를 얻을 수 있다.

> **확인**: 심화 과제 중 하나를 완성한 뒤, 프롬프트를 개선하면서 결과가 어떻게 변하는지 3회 이상 반복해보자.
