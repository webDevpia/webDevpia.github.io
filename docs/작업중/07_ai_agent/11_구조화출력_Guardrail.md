---
title: 11. 구조화 출력과 Guardrail
layout: default
grand_parent: LLM
parent: AI Agent
nav_order: 11
permalink: /llm/ai-agent/structured-output
---

## 학습 목표

- Pydantic 모델로 에이전트 출력을 구조화할 수 있다
- Guardrail과 Planning 기능으로 에이전트의 품질을 높일 수 있다

<a id="toc"></a>

## 진행 순서

1. [구조화 출력이란?](#part1) - Pydantic으로 출력 형식 강제
2. [Guardrail — 품질 검증](#part2) - 출력 자동 검증 및 재시도
3. [Planning — 자동 계획 수립](#part3) - AI가 먼저 계획하고 실행
4. [실습: 구조화된 여행 계획 + Guardrail](#part4) - 완성 예제
5. [정리](#part5) - 구조화 출력 장점, Guardrail 패턴

---

# 11장. 구조화 출력과 Guardrail

<a id="part1"></a>

## 1️⃣ 구조화 출력이란? [↑](#toc)

AI 에이전트의 기본 출력은 **자유 형식 텍스트**입니다. 하지만 실무에서는 출력을 데이터베이스에 저장하거나, 다른 시스템에 전달하거나, 특정 형식으로 가공해야 하는 경우가 많습니다. 이때 **구조화 출력(Structured Output)**이 필요합니다.

### 양식 비유

> 자유 형식 에세이가 아닌, **정해진 칸에 맞춰 작성하는 양식**입니다.
>
> 입사지원서를 생각해보세요. "자기소개를 자유롭게 써주세요"는 자유 형식,
> "이름: \_\_\_ / 생년월일: \_\_\_ / 경력: \_\_\_"는 구조화 출력입니다.

### 구조화 출력의 장점

| 일반 텍스트 출력 | 구조화 출력 (Pydantic) |
|----------------|----------------------|
| 파싱 어려움 | 바로 Python 객체로 사용 |
| 형식 일관성 없음 | 항상 동일한 구조 보장 |
| 타입 검증 불가 | 자동 타입 검증 |
| JSON 변환 수동 | `.model_dump()` 한 줄 |

### Pydantic 모델로 출력 형식 정의

```python
from pydantic import BaseModel, Field
from typing import List

class TravelPlan(BaseModel):
    """여행 계획 구조화 출력 모델"""
    destination: str = Field(description="여행지 이름")
    duration: str = Field(description="여행 기간 (예: 3박4일)")
    budget: int = Field(description="예산 (원 단위)")
    attractions: List[str] = Field(description="추천 관광지 목록")
    restaurants: List[str] = Field(description="추천 맛집 목록")
    tips: str = Field(description="여행 팁 또는 주의사항")
```

### Task에 Pydantic 모델 연결

```python
from crewai import Agent, Task, Crew
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

# ─── 출력 모델 정의 ──────────────────────────────────────────
class TravelPlan(BaseModel):
    destination: str
    duration: str
    budget: int
    attractions: List[str]
    restaurants: List[str]
    tips: str

# ─── 에이전트 정의 ───────────────────────────────────────────
planner = Agent(
    role="여행 계획 전문가",
    goal="주어진 조건에 맞는 완벽한 여행 계획을 수립한다",
    backstory="10년 경력의 여행 컨설턴트로, 예산과 일정에 최적화된 여행 계획을 제안합니다.",
    verbose=True
)

# ─── Task에 output_pydantic 연결 ─────────────────────────────
task = Task(
    description="서울 3박4일 여행 계획을 작성하세요. 예산은 50만원 이내로 잡으세요.",
    expected_output="구조화된 여행 계획 (목적지, 기간, 예산, 관광지, 맛집, 팁 포함)",
    output_pydantic=TravelPlan,   # Pydantic 모델 지정!
    agent=planner
)

crew = Crew(agents=[planner], tasks=[task], verbose=True)
result = crew.kickoff()

# ─── 결과 사용 ───────────────────────────────────────────────
plan: TravelPlan = task.output.pydantic  # Pydantic 객체로 접근

print(f"여행지: {plan.destination}")
print(f"기간: {plan.duration}")
print(f"예산: {plan.budget:,}원")
print(f"\n관광지:")
for a in plan.attractions:
    print(f"  - {a}")
print(f"\n맛집:")
for r in plan.restaurants:
    print(f"  - {r}")

# JSON으로 내보내기
import json
plan_dict = plan.model_dump()
print(json.dumps(plan_dict, ensure_ascii=False, indent=2))
```

### output_json 옵션 — JSON 딕셔너리 반환

Pydantic 모델 대신 딕셔너리로 받고 싶을 때:

```python
task = Task(
    description="여행 계획을 작성하세요.",
    expected_output="JSON 형식의 여행 계획",
    output_json=TravelPlan,   # JSON 딕셔너리로 반환
    agent=planner
)

result = crew.kickoff()
plan_json: dict = task.output.json_dict
print(plan_json["destination"])
```

---

<a id="part2"></a>

## 2️⃣ Guardrail — 품질 검증 [↑](#toc)

**Guardrail**은 에이전트 출력이 특정 기준을 충족하는지 **자동으로 검증**하는 기능입니다. 검증 실패 시 에이전트가 자동으로 재시도합니다.

### 품질 검사 비유

> 공장의 **품질 검사관**처럼, 에이전트가 만든 결과물이 기준에 맞는지 자동으로 확인합니다.
> 기준 미달이면 에이전트에게 다시 만들도록 요청합니다.

### Guardrail 기본 구조

```python
from crewai import Task
from crewai.task import TaskOutput

def validate_travel_plan(output: TaskOutput) -> tuple[bool, str]:
    """
    Guardrail 함수:
    - 검증 통과: (True, "") 반환
    - 검증 실패: (False, "오류 메시지") 반환
    """
    plan = output.pydantic  # Pydantic 모델 객체

    # 검증 1: 예산 확인
    if plan.budget <= 0:
        return False, "예산은 0보다 커야 합니다."

    # 검증 2: 최대 예산 초과 확인
    if plan.budget > 2000000:
        return False, "예산이 200만원을 초과했습니다. 더 합리적인 계획을 세워주세요."

    # 검증 3: 관광지 최소 개수
    if len(plan.attractions) < 3:
        return False, "관광지를 최소 3곳 이상 포함해야 합니다."

    # 검증 4: 맛집 최소 개수
    if len(plan.restaurants) < 2:
        return False, "맛집을 최소 2곳 이상 포함해야 합니다."

    return True, ""  # 검증 통과

task = Task(
    description="제주도 2박3일 여행 계획 (예산: 80만원 이내)",
    expected_output="구조화된 여행 계획",
    output_pydantic=TravelPlan,
    guardrail=validate_travel_plan,   # Guardrail 연결!
    agent=planner
)
```

### 실전 Guardrail 패턴들

```python
from crewai.task import TaskOutput

# ─── 패턴 1: 길이 검증 ──────────────────────────────────────
def validate_report_length(output: TaskOutput) -> tuple[bool, str]:
    """보고서가 충분히 상세한지 확인"""
    text = output.raw
    if len(text) < 500:
        return False, "보고서가 너무 짧습니다. 더 상세한 내용을 포함해주세요."
    return True, ""

# ─── 패턴 2: 키워드 포함 여부 ───────────────────────────────
def validate_contains_keywords(output: TaskOutput) -> tuple[bool, str]:
    """필수 키워드 포함 여부 확인"""
    required_keywords = ["결론", "권장사항", "예산"]
    text = output.raw.lower()
    missing = [kw for kw in required_keywords if kw not in text]
    if missing:
        return False, f"다음 항목이 누락되었습니다: {', '.join(missing)}"
    return True, ""

# ─── 패턴 3: 숫자 범위 검증 ─────────────────────────────────
def validate_budget_range(output: TaskOutput) -> tuple[bool, str]:
    """예산이 합리적인 범위인지 확인"""
    plan = output.pydantic
    min_budget = 100000   # 10만원
    max_budget = 5000000  # 500만원

    if not (min_budget <= plan.budget <= max_budget):
        return False, (
            f"예산이 합리적인 범위({min_budget:,}원~{max_budget:,}원)를 벗어났습니다. "
            f"현재 설정된 예산: {plan.budget:,}원"
        )
    return True, ""

# ─── 패턴 4: 외부 API 검증 ──────────────────────────────────
def validate_destination_exists(output: TaskOutput) -> tuple[bool, str]:
    """여행지가 실제로 존재하는지 검증 (외부 서비스 활용 예시)"""
    plan = output.pydantic
    # 실제로는 지오코딩 API 등을 호출할 수 있음
    invalid_destinations = ["화성", "달나라", "무인도"]
    if plan.destination in invalid_destinations:
        return False, f"'{plan.destination}'은 여행 상품이 없는 곳입니다."
    return True, ""
```

---

<a id="part3"></a>

## 3️⃣ Planning — 자동 계획 수립 [↑](#toc)

**Planning**은 Crew가 실제 작업을 시작하기 전에 **AI가 먼저 전체 계획을 수립**하도록 하는 기능입니다.

### 여행 전 일정표 작성 비유

> 해외여행을 떠나기 전 꼼꼼하게 **일정표를 작성**하는 것처럼,
> Planning은 에이전트들이 작업에 착수하기 전에 최적의 실행 계획을 먼저 세웁니다.

### Planning 활성화

```python
from crewai import Agent, Task, Crew, LLM

# planning=True 로 활성화
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, report_task],
    planning=True,   # AI가 먼저 계획을 세우고 실행!
    verbose=True
)

result = crew.kickoff()
```

### Planning에 특정 LLM 지정

계획 수립 단계에서 더 강력한 LLM을 사용하여 최적의 계획을 세울 수 있습니다:

```python
from crewai import LLM

# 계획 수립에는 GPT-4o 사용, 실행에는 GPT-4o-mini 사용
planning_llm = LLM(model="gpt-4o")

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    planning=True,
    planning_llm=planning_llm,  # 계획 수립 전용 LLM
    verbose=True
)
```

### Planning 동작 방식

```
Planning=True로 Crew.kickoff() 호출
         ↓
1. 계획 수립 단계 (planning_llm이 실행)
   "task1은 어떤 순서로? task2에 필요한 정보는?"
   → 최적 실행 순서와 각 태스크 접근 방법 결정
         ↓
2. 실행 단계 (각 에이전트가 계획에 따라 실행)
   agent1이 task1 실행 → agent2가 task2 실행
         ↓
3. 최종 결과 반환
```

---

<a id="part4"></a>

## 4️⃣ 실습: 구조화된 여행 계획 + Guardrail [↑](#toc)

구조화 출력, Guardrail, Planning을 모두 조합한 완성 예제입니다.

### 전체 코드

```python
# 파일명: 11_structured_output.py
from crewai import Agent, Task, Crew
from crewai.task import TaskOutput
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

# ─── 출력 모델 정의 ──────────────────────────────────────────
class TravelPlan(BaseModel):
    destination: str = Field(description="여행지 이름")
    duration: str = Field(description="여행 기간 (예: 3박4일)")
    budget: int = Field(description="총 예산 (원 단위)")
    budget_breakdown: dict = Field(
        description="예산 항목별 분류 (숙박, 식비, 교통, 관광)",
        default_factory=dict
    )
    attractions: List[str] = Field(description="추천 관광지 목록 (최소 3곳)")
    restaurants: List[str] = Field(description="추천 맛집 목록 (최소 2곳)")
    itinerary: List[str] = Field(description="일자별 일정")
    tips: str = Field(description="여행 팁")

# ─── Guardrail 함수 ───────────────────────────────────────────
def validate_travel_plan(output: TaskOutput) -> tuple[bool, str]:
    """여행 계획 품질 검증"""
    try:
        plan = output.pydantic
    except Exception:
        return False, "출력이 올바른 형식이 아닙니다."

    # 예산 검증 (10만원~200만원)
    if not (100000 <= plan.budget <= 2000000):
        return False, (
            f"예산({plan.budget:,}원)이 합리적인 범위(10만~200만원)를 벗어났습니다."
        )

    # 관광지 최소 3곳
    if len(plan.attractions) < 3:
        return False, f"관광지가 {len(plan.attractions)}곳입니다. 최소 3곳이 필요합니다."

    # 맛집 최소 2곳
    if len(plan.restaurants) < 2:
        return False, f"맛집이 {len(plan.restaurants)}곳입니다. 최소 2곳이 필요합니다."

    # 일정 항목 수 확인 (기간과 일치하는지 대략 확인)
    if len(plan.itinerary) == 0:
        return False, "일자별 일정이 비어 있습니다."

    return True, ""

# ─── 에이전트 정의 ───────────────────────────────────────────
travel_planner = Agent(
    role="여행 계획 전문가",
    goal="예산에 맞는 완벽하고 실용적인 여행 계획을 수립한다",
    backstory=(
        "15년 경력의 여행 전문 컨설턴트입니다. "
        "국내외 수백 개의 여행지를 직접 방문하고 여행 계획을 수립한 경험이 있으며, "
        "예산과 일정을 최적화하여 최고의 여행 경험을 제공합니다."
    ),
    verbose=True
)

# ─── Task 정의 ───────────────────────────────────────────────
planning_task = Task(
    description=(
        "다음 조건에 맞는 여행 계획을 수립하세요:\n"
        "- 여행지: {destination}\n"
        "- 기간: {duration}\n"
        "- 예산: {budget}원 이내\n"
        "- 여행 스타일: {style}\n\n"
        "관광지 최소 3곳, 맛집 최소 2곳, 일자별 상세 일정, 예산 항목별 분류를 포함하세요."
    ),
    expected_output="구조화된 여행 계획 (모든 필수 항목 포함)",
    output_pydantic=TravelPlan,
    guardrail=validate_travel_plan,   # Guardrail 적용
    agent=travel_planner
)

# ─── Crew 실행 (Planning 활성화) ─────────────────────────────
crew = Crew(
    agents=[travel_planner],
    tasks=[planning_task],
    planning=True,   # 실행 전 계획 수립
    verbose=True
)

result = crew.kickoff(inputs={
    "destination": "부산",
    "duration": "2박3일",
    "budget": 600000,
    "style": "맛집 중심의 미식 여행"
})

# ─── 결과 출력 ───────────────────────────────────────────────
plan: TravelPlan = planning_task.output.pydantic

print("\n" + "=" * 50)
print(f"여행지: {plan.destination}")
print(f"기간: {plan.duration}")
print(f"총 예산: {plan.budget:,}원")
print("\n[예산 항목별 분류]")
for item, amount in plan.budget_breakdown.items():
    print(f"  {item}: {amount:,}원")
print("\n[추천 관광지]")
for i, att in enumerate(plan.attractions, 1):
    print(f"  {i}. {att}")
print("\n[추천 맛집]")
for i, rest in enumerate(plan.restaurants, 1):
    print(f"  {i}. {rest}")
print("\n[일자별 일정]")
for day in plan.itinerary:
    print(f"  {day}")
print(f"\n[여행 팁]\n  {plan.tips}")
```

### 실행 방법

```bash
python 11_structured_output.py
```

### Guardrail 동작 확인

출력이 검증 기준에 맞지 않으면 CrewAI가 자동으로 에이전트에게 재시도를 요청합니다:

```
[에이전트 첫 번째 시도]
  예산: 50,000원 (← 10만원 미만)

[Guardrail 검증 실패]
  오류: "예산(50,000원)이 합리적인 범위(10만~200만원)를 벗어났습니다."

[에이전트 재시도]
  에이전트가 오류 메시지를 받고 수정된 답변 생성...
  예산: 600,000원 (← 검증 통과)

[Guardrail 검증 통과]
  결과 반환
```

---

<a id="part5"></a>

## 5️⃣ 정리 [↑](#toc)

### 구조화 출력 장점 요약

| 활용 시나리오 | 이점 |
|-------------|------|
| API 연동 | 출력을 바로 JSON으로 직렬화 |
| 데이터베이스 저장 | 필드별로 정확한 타입 보장 |
| 다음 단계 처리 | 파싱 없이 바로 Python 객체 사용 |
| UI 렌더링 | 필드별로 구조화된 HTML 생성 |

### Guardrail 활용 패턴

| 패턴 | 설명 | 예시 |
|------|------|------|
| 범위 검증 | 숫자가 허용 범위 내에 있는지 | 예산 1만~500만원 |
| 최소 개수 | 리스트에 최소 N개 항목 | 관광지 3곳 이상 |
| 키워드 포함 | 필수 내용 포함 여부 | "결론", "권장사항" 포함 |
| 길이 검증 | 텍스트 길이 범위 | 500자 이상 |
| 외부 검증 | API 호출로 유효성 확인 | 주소 유효성, 날짜 범위 등 |

### 세 기능 비교

| 기능 | 목적 | 설정 위치 |
|------|------|---------|
| `output_pydantic` | 출력 형식 강제 | Task 파라미터 |
| `guardrail` | 출력 품질 검증 | Task 파라미터 |
| `planning=True` | 실행 전 계획 수립 | Crew 파라미터 |

### 핵심 요약

- `output_pydantic=모델클래스`로 에이전트 출력을 구조화된 Python 객체로 받기
- Guardrail 함수는 `(bool, str)` 튜플 반환 — `True`면 통과, `False`면 오류 메시지와 함께 재시도
- `planning=True`는 모든 태스크 실행 전에 AI가 최적 계획을 먼저 수립
- 세 기능을 함께 사용하면 에이전트 출력의 품질과 신뢰성이 크게 높아짐

> **다음 장 미리보기:** Day 1~2에서 배운 모든 개념을 통합하여 완성도 높은 멀티에이전트 여행 플래너를 만들어봅니다.
