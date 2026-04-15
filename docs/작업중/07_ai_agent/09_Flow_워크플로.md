---
title: 09. Flow - 워크플로 오케스트레이션
layout: default
grand_parent: LLM
parent: AI Agent
nav_order: 9
permalink: /llm/ai-agent/flow
---

## 학습 목표

- Flow를 사용하여 여러 Crew를 연결하는 워크플로를 구성할 수 있다
- `@start`, `@listen`, `@router`로 흐름을 제어할 수 있다

<a id="toc"></a>

## 진행 순서

1. [Flow란?](#part1) - Crew를 연결하는 워크플로 개념
2. [기본 Flow 구조](#part2) - @start, @listen 데코레이터
3. [@router — 조건 분기](#part3) - 조건에 따른 실행 경로 분기
4. [상태(State) 관리](#part4) - Pydantic으로 타입 안전한 상태 관리
5. [실습: 리서치 → 분석 → 보고서 Flow](#part5) - 3단계 Flow 구현
6. [정리](#part6) - Flow 데코레이터 요약, Crew vs Flow 비교

---

# 09장. Flow — 워크플로 오케스트레이션

<a id="part1"></a>

## 1️⃣ Flow란? [↑](#toc)

**Flow**는 여러 Crew(또는 작업 단위)를 **연결하여 복잡한 워크플로를 구성**하는 상위 계층의 오케스트레이션 도구입니다.

### 공장 생산 라인 비유

> 원재료 투입(`@start`) → 1차 가공(`@listen`) → 품질 검사 후 분기(`@router`) → 완성품 출하
>
> **Crew**가 "전문 팀"이라면, **Flow**는 "여러 팀을 조율하는 프로젝트 매니저"입니다.

### Crew만으로는 부족한 경우

```
단순 작업: Crew 하나로 충분
   Agent1 → Agent2 → Agent3 (순차 실행)

복잡한 워크플로: Flow 필요
   리서치 Crew → (결과에 따라) 예산 분석 Crew
                              또는
                              간략 요약 Crew → 최종 보고서 Crew
```

### Crew vs Flow

| 비교 항목 | Crew | Flow |
|----------|------|------|
| 구성 단위 | Agent + Task | Crew 또는 함수 |
| 흐름 제어 | 순차/계층적 실행 | 데코레이터 기반 유연한 연결 |
| 조건 분기 | 불가 | `@router`로 가능 |
| 상태 공유 | `context` 파라미터 | `self.state` 공유 객체 |
| 주요 용도 | 하나의 목표를 팀이 협력 | 여러 단계의 파이프라인 |

---

<a id="part2"></a>

## 2️⃣ 기본 Flow 구조 [↑](#toc)

Flow는 **파이썬 클래스**로 정의하며, 각 단계를 메서드로 구현하고 데코레이터로 연결합니다.

### 핵심 데코레이터

| 데코레이터 | 역할 | 사용 예 |
|-----------|------|--------|
| `@start()` | Flow의 시작점 | 사용자 입력 받기 |
| `@listen(메서드명)` | 특정 메서드 완료 후 실행 | 앞 단계 결과 받아 처리 |
| `@router(메서드명)` | 조건에 따라 다음 경로 분기 | 예산에 따라 다른 경로 선택 |

### 기본 Flow 예시 — 여행 계획 3단계

```python
# 파일명: 09_basic_flow.py
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

# ─── 상태(State) 정의 — 단계 간 공유되는 데이터 ────────────────
class TravelState(BaseModel):
    destination: str = ""   # 여행지
    research: str = ""      # 리서치 결과
    plan: str = ""          # 최종 계획

# ─── Flow 클래스 정의 ──────────────────────────────────────────
class TravelFlow(Flow[TravelState]):

    @start()
    def get_destination(self):
        """1단계: 여행지 설정 (Flow 시작점)"""
        self.state.destination = "도쿄"
        print(f"[1단계] 여행지 설정: {self.state.destination}")
        return self.state.destination

    @listen(get_destination)
    def research_destination(self):
        """2단계: 여행지 리서치 (1단계 완료 후 실행)"""
        destination = self.state.destination
        # 실제 구현에서는 Crew를 여기서 실행
        self.state.research = f"{destination}의 주요 관광지: 신주쿠, 시부야, 아사쿠사"
        print(f"[2단계] 리서치 완료: {self.state.research}")
        return self.state.research

    @listen(research_destination)
    def create_plan(self):
        """3단계: 여행 계획 작성 (2단계 완료 후 실행)"""
        self.state.plan = (
            f"[{self.state.destination} 여행 계획]\n"
            f"조사된 정보: {self.state.research}\n"
            f"추천 일정: 1일차 신주쿠, 2일차 시부야, 3일차 아사쿠사"
        )
        print(f"[3단계] 계획 완성")
        return self.state.plan

# ─── Flow 실행 ──────────────────────────────────────────────
if __name__ == "__main__":
    flow = TravelFlow()
    result = flow.kickoff()
    print("\n[최종 결과]")
    print(result)
```

### Crew를 Flow 안에서 실행하기

실제 활용에서는 각 메서드 안에서 Crew를 실행합니다:

```python
from crewai import Agent, Task, Crew
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class ResearchState(BaseModel):
    topic: str = ""
    research_result: str = ""

class ResearchFlow(Flow[ResearchState]):

    @start()
    def set_topic(self):
        self.state.topic = "인공지능 최신 트렌드"
        return self.state.topic

    @listen(set_topic)
    def run_research_crew(self):
        """Crew를 실행하여 리서치 수행"""
        # 에이전트 정의
        researcher = Agent(
            role="리서치 전문가",
            goal=f"{self.state.topic}을 깊이 있게 조사한다",
            backstory="최신 기술 동향을 추적하는 AI 리서처입니다.",
            verbose=True
        )

        # 태스크 정의
        research_task = Task(
            description=f"{self.state.topic}에 대해 최신 동향을 조사하고 요약하세요.",
            expected_output="핵심 트렌드 3~5가지와 각각의 설명",
            agent=researcher
        )

        # Crew 실행
        crew = Crew(
            agents=[researcher],
            tasks=[research_task],
            verbose=True
        )

        result = crew.kickoff()
        self.state.research_result = str(result)
        return self.state.research_result
```

---

<a id="part3"></a>

## 3️⃣ @router — 조건 분기 [↑](#toc)

`@router`는 반환 값에 따라 다음에 실행할 메서드를 **분기**시킵니다.

### 예산에 따른 여행 계획 분기

```python
from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel

class BudgetTravelState(BaseModel):
    destination: str = ""
    budget: int = 0           # 예산 (원)
    plan: str = ""

class BudgetTravelFlow(Flow[BudgetTravelState]):

    @start()
    def get_inputs(self):
        """여행지와 예산 입력"""
        self.state.destination = "파리"
        self.state.budget = 800000   # 80만원
        return self.state.destination

    @router(get_inputs)
    def check_budget(self):
        """예산에 따라 분기 결정"""
        if self.state.budget >= 1500000:    # 150만원 이상
            return "luxury"
        elif self.state.budget >= 800000:   # 80만원 이상
            return "standard"
        else:
            return "budget"

    @listen("luxury")
    def luxury_plan(self):
        """고급 여행 계획"""
        self.state.plan = (
            f"[{self.state.destination}] 럭셔리 여행 계획\n"
            "- 5성급 호텔 숙박\n"
            "- 미슐랭 레스토랑 디너\n"
            "- 전용 가이드 투어"
        )
        return self.state.plan

    @listen("standard")
    def standard_plan(self):
        """일반 여행 계획"""
        self.state.plan = (
            f"[{self.state.destination}] 일반 여행 계획\n"
            "- 3성급 호텔 숙박\n"
            "- 현지 레스토랑 이용\n"
            "- 대중교통 + 도보 투어"
        )
        return self.state.plan

    @listen("budget")
    def budget_plan(self):
        """절약 여행 계획"""
        self.state.plan = (
            f"[{self.state.destination}] 절약 여행 계획\n"
            "- 게스트하우스 숙박\n"
            "- 슈퍼마켓 자취\n"
            "- 무료 관광지 중심"
        )
        return self.state.plan

# ─── 실행 ───────────────────────────────────────────────────
if __name__ == "__main__":
    flow = BudgetTravelFlow()
    result = flow.kickoff()
    print("\n[여행 계획]")
    print(result)
```

### router 동작 흐름

```
get_inputs() 실행
      ↓
check_budget() — 라우터
      ├─ "luxury"  → luxury_plan()
      ├─ "standard" → standard_plan()
      └─ "budget"  → budget_plan()
```

---

<a id="part4"></a>

## 4️⃣ 상태(State) 관리 [↑](#toc)

Flow의 각 단계는 **`self.state`** 객체를 통해 데이터를 공유합니다. 상태는 **Pydantic BaseModel**로 정의하여 타입 안전성을 보장합니다.

### 상태 정의 패턴

```python
from pydantic import BaseModel
from typing import List, Optional

class TravelPlanState(BaseModel):
    # 입력 데이터
    destination: str = ""
    days: int = 3
    budget: int = 0

    # 단계별 결과 누적
    research_result: str = ""
    budget_analysis: str = ""
    final_plan: str = ""

    # 제어 플래그
    is_international: bool = False
    selected_tier: str = "standard"   # "luxury" | "standard" | "budget"

    # 리스트 타입
    attractions: List[str] = []
    restaurants: List[str] = []
```

### 상태 접근과 수정

```python
class MyFlow(Flow[TravelPlanState]):

    @start()
    def initialize(self):
        # 상태 읽기
        print(f"여행지: {self.state.destination}")

        # 상태 쓰기
        self.state.destination = "방콕"
        self.state.days = 5
        self.state.attractions.append("왓 프라깨우")

        return self.state.destination
```

### 외부에서 초기 상태 주입

`kickoff()`에 `inputs` 딕셔너리를 전달하여 초기 상태를 설정할 수 있습니다:

```python
flow = TravelPlanFlow()

# inputs로 초기 상태값 전달
result = flow.kickoff(inputs={
    "destination": "방콕",
    "days": 5,
    "budget": 1200000
})
```

---

<a id="part5"></a>

## 5️⃣ 실습: 리서치 → 분석 → 보고서 Flow [↑](#toc)

3단계로 이루어진 리서치 Flow를 구현합니다. 각 단계에서 Crew를 실행하고 결과를 다음 단계로 전달합니다.

### 전체 코드

```python
# 파일명: 09_research_flow.py
from crewai import Agent, Task, Crew
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# ─── 상태 정의 ───────────────────────────────────────────────
class ReportState(BaseModel):
    topic: str = ""
    raw_research: str = ""
    analysis: str = ""
    final_report: str = ""

# ─── Flow 정의 ───────────────────────────────────────────────
class ResearchReportFlow(Flow[ReportState]):

    @start()
    def set_topic(self):
        """주제 설정"""
        self.state.topic = "2025년 AI 에이전트 시장 동향"
        print(f"[시작] 주제: {self.state.topic}")
        return self.state.topic

    @listen(set_topic)
    def research_phase(self):
        """1단계: 리서치"""
        print("[1단계] 리서치 시작...")

        researcher = Agent(
            role="리서치 전문가",
            goal="주어진 주제에 대한 최신 정보를 수집하고 정리한다",
            backstory=(
                "10년 경력의 시장조사 전문가로, "
                "신뢰할 수 있는 데이터와 인사이트를 제공합니다."
            ),
            verbose=True
        )

        task = Task(
            description=(
                f"다음 주제에 대해 리서치하세요: {self.state.topic}\n"
                "주요 트렌드, 시장 규모, 주요 플레이어를 포함하세요."
            ),
            expected_output="구조화된 리서치 결과 (트렌드 3~5가지 + 근거)",
            agent=researcher
        )

        crew = Crew(agents=[researcher], tasks=[task], verbose=False)
        result = crew.kickoff()
        self.state.raw_research = str(result)
        print("[1단계] 리서치 완료")
        return self.state.raw_research

    @listen(research_phase)
    def analysis_phase(self):
        """2단계: 분석"""
        print("[2단계] 분석 시작...")

        analyst = Agent(
            role="데이터 분석가",
            goal="리서치 결과를 분석하여 핵심 인사이트를 도출한다",
            backstory=(
                "비즈니스 인텔리전스 전문가로, "
                "데이터에서 실행 가능한 인사이트를 찾아냅니다."
            ),
            verbose=True
        )

        task = Task(
            description=(
                f"다음 리서치 결과를 분석하세요:\n{self.state.raw_research}\n\n"
                "기회와 위협 요인, 핵심 시사점을 도출하세요."
            ),
            expected_output="SWOT 분석 또는 기회/위협 요인 분석",
            agent=analyst
        )

        crew = Crew(agents=[analyst], tasks=[task], verbose=False)
        result = crew.kickoff()
        self.state.analysis = str(result)
        print("[2단계] 분석 완료")
        return self.state.analysis

    @listen(analysis_phase)
    def report_phase(self):
        """3단계: 보고서 작성"""
        print("[3단계] 보고서 작성 시작...")

        writer = Agent(
            role="비즈니스 보고서 작가",
            goal="리서치와 분석 결과를 읽기 쉬운 보고서로 작성한다",
            backstory=(
                "경영 컨설팅 보고서 전문가로, "
                "복잡한 내용을 명확하고 설득력 있게 전달합니다."
            ),
            verbose=True
        )

        task = Task(
            description=(
                f"다음 자료를 바탕으로 '{self.state.topic}' 보고서를 작성하세요.\n\n"
                f"[리서치]\n{self.state.raw_research}\n\n"
                f"[분석]\n{self.state.analysis}"
            ),
            expected_output="제목, 요약, 본문(3~5섹션), 결론이 포함된 완성된 보고서",
            agent=writer
        )

        crew = Crew(agents=[writer], tasks=[task], verbose=False)
        result = crew.kickoff()
        self.state.final_report = str(result)
        print("[3단계] 보고서 완성")
        return self.state.final_report

# ─── 실행 ───────────────────────────────────────────────────
if __name__ == "__main__":
    flow = ResearchReportFlow()
    final = flow.kickoff()

    print("\n" + "=" * 60)
    print("최종 보고서")
    print("=" * 60)
    print(final)
```

### 실행 방법

```bash
python 09_research_flow.py
```

### 실행 흐름 확인

```
[시작] 주제: 2025년 AI 에이전트 시장 동향
[1단계] 리서치 시작...
[1단계] 리서치 완료
[2단계] 분석 시작...
[2단계] 분석 완료
[3단계] 보고서 작성 시작...
[3단계] 보고서 완성
============================================================
최종 보고서
============================================================
(보고서 내용 출력)
```

---

<a id="part6"></a>

## 6️⃣ 정리 [↑](#toc)

### Flow 데코레이터 요약

| 데코레이터 | 문법 | 역할 |
|-----------|------|------|
| `@start()` | `@start()` | Flow 시작점 (여러 개 가능) |
| `@listen()` | `@listen(메서드명)` 또는 `@listen("라우터 반환값")` | 특정 이벤트 발생 후 실행 |
| `@router()` | `@router(메서드명)` | 반환 문자열로 다음 경로 결정 |

### Crew vs Flow 차이표

| 비교 항목 | Crew | Flow |
|----------|------|------|
| 주요 역할 | 에이전트 팀 협업 | 여러 Crew/단계 연결 |
| 구성 요소 | Agent + Task | 메서드 + 데코레이터 |
| 조건 분기 | 불가 | `@router`로 지원 |
| 상태 공유 | `context` 파라미터 | `self.state` 공유 객체 |
| 재사용성 | Crew 단위로 재사용 | Flow 클래스로 재사용 |
| 적합한 규모 | 단일 목표, 3~7개 에이전트 | 복잡한 다단계 파이프라인 |

### 핵심 요약

- Flow = 여러 Crew를 연결하는 **워크플로 오케스트레이터**
- `@start` → `@listen` → `@router` 데코레이터로 흐름을 선언적으로 정의
- `self.state`를 통해 단계 간 데이터 공유 (Pydantic으로 타입 보장)
- `kickoff(inputs={...})`로 외부에서 초기값 주입 가능

> **다음 장 미리보기:** MCP(Model Context Protocol)로 표준화된 도구를 연결하고, Ollama로 로컬 LLM을 사용하는 방법을 배웁니다.
