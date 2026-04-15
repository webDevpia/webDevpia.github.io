---
title: 03. CrewAI 핵심 개념
layout: default
grand_parent: LLM
parent: AI Agent
nav_order: 3
permalink: /llm/ai-agent/core-concepts
---

# 03장. CrewAI 핵심 개념
{: .no_toc }

## 학습 목표

- CrewAI의 3가지 핵심 구성요소(Agent, Task, Crew)를 이해하고 사용할 수 있다
- 단일 에이전트를 만들어 실행할 수 있다

<a id="toc"></a>

## 진행 순서

1. [CrewAI의 구조](#part1) — 전체 그림 이해
2. [Agent (팀원)](#part2) — role, goal, backstory
3. [Task (업무)](#part3) — description, expected_output, agent
4. [Crew (팀)](#part4) — agents, tasks, process, kickoff()
5. [실습: Hello CrewAI](#part5) — 전체 코드 실행
6. [정리](#part6) — 구성요소 요약

---

<a id="part1"></a>

## 1️⃣ CrewAI의 구조 [↑](#toc)

### 프로젝트 팀 비유

> **Agent**는 팀원, **Task**는 업무, **Crew**는 팀 전체입니다.
> 팀을 꾸리고 업무를 배분하고 팀을 가동(`kickoff()`)하면 에이전트들이 협력하여 결과물을 만들어냅니다.

```
Crew (팀)
  ├── Agent 1 (리서치 전문가) ──→ Task 1 (관광지 조사)
  ├── Agent 2 (여행 작가)    ──→ Task 2 (블로그 글 작성)
  └── kickoff()  ──→ 결과물 반환
```

### CrewAI가 동작하는 방식

```python
# CrewAI의 기본 흐름
crew = Crew(agents=[...], tasks=[...])
result = crew.kickoff()  # "팀, 일 시작!"
```

`kickoff()`을 호출하면 CrewAI가 Task를 순서대로 Agent에게 배분하고, 각 Agent는 LLM을 사용해 Task를 수행합니다. 결과는 다음 Task로 전달되거나 최종 출력으로 반환됩니다.

---

<a id="part2"></a>

## 2️⃣ Agent (팀원) [↑](#toc)

### Agent란?

**Agent**는 특정 역할을 가진 AI 팀원입니다. 사람으로 치면 "리서치 전문가", "글쓰기 전문가" 같은 직책을 가진 팀원입니다.

```python
from crewai import Agent

researcher = Agent(
    role="리서치 전문가",
    goal="주어진 주제에 대해 정확하고 최신 정보를 수집한다",
    backstory="당신은 10년 경력의 리서치 전문가로, 복잡한 주제를 명확하게 정리하는 능력이 있습니다.",
    verbose=True  # 에이전트의 사고 과정을 콘솔에 출력
)
```

### 각 파라미터의 역할

| 파라미터 | 역할 | 비유 |
|---------|------|------|
| `role` | "이 사람은 누구인가?" (직함) | 명함의 직책 |
| `goal` | "무엇을 달성해야 하는가?" (목표) | 업무 목표 |
| `backstory` | "어떤 배경/전문성이 있는가?" (컨텍스트) | 이력서 |
| `verbose` | 사고 과정을 콘솔에 출력할지 여부 | 업무 일지 공개 |

### role, goal, backstory가 중요한 이유

이 세 가지가 합쳐져 **에이전트의 시스템 프롬프트**가 됩니다. LLM은 이 프롬프트를 읽고 "나는 이런 역할을 가진 전문가구나"라고 인식하여 그에 맞게 행동합니다.

```python
# role이 다르면 같은 Task도 다르게 처리합니다
agent_researcher = Agent(
    role="데이터 분석가",
    goal="숫자와 통계로 사실을 증명한다",
    backstory="수치와 데이터를 분석하는 것이 특기인 전문가입니다."
)

agent_writer = Agent(
    role="마케팅 카피라이터",
    goal="독자의 감정을 움직이는 글을 쓴다",
    backstory="독자의 마음을 사로잡는 스토리텔링 전문가입니다."
)
# 같은 "AI 트렌드" 주제를 줘도 전혀 다른 결과물이 나옵니다
```

### 자주 사용하는 추가 파라미터

```python
from crewai import Agent, LLM

researcher = Agent(
    role="리서치 전문가",
    goal="정확한 정보 수집",
    backstory="10년 경력의 리서처",
    llm=LLM(model="gpt-4o-mini"),   # 사용할 LLM 지정 (기본값: gpt-4o)
    tools=[],                          # 사용할 도구 목록 (05장에서 다룸)
    max_iter=5,                        # 최대 반복 횟수 (무한 루프 방지)
    verbose=True
)
```

---

<a id="part3"></a>

## 3️⃣ Task (업무) [↑](#toc)

### Task란?

**Task**는 Agent에게 주어지는 구체적인 업무 지시서입니다. "무엇을 해야 하는지"와 "어떤 결과물이 나와야 하는지"를 명시합니다.

```python
from crewai import Task

research_task = Task(
    description="서울 3박4일 여행 계획에 필요한 관광지, 맛집, 교통 정보를 조사하세요.",
    expected_output="관광지 5곳, 맛집 5곳, 교통 수단 정보를 포함한 마크다운 형식의 리서치 보고서",
    agent=researcher  # 이 Task를 담당할 Agent
)
```

### 각 파라미터의 역할

| 파라미터 | 역할 | 팁 |
|---------|------|-----|
| `description` | 무엇을 해야 하는가? | 구체적일수록 좋다 |
| `expected_output` | 어떤 결과물이 나와야 하는가? | 형식(마크다운, JSON 등)을 명시하면 좋다 |
| `agent` | 어떤 Agent가 담당하는가? | 역할에 맞는 Agent 지정 |

### expected_output을 잘 쓰는 법

```python
# 나쁜 예 — 너무 모호함
research_task = Task(
    description="서울 여행 정보 조사",
    expected_output="보고서",   # ← 무슨 형식? 얼마나 길게?
    agent=researcher
)

# 좋은 예 — 구체적인 형식 지정
research_task = Task(
    description="서울 3박4일 여행에 필요한 관광지, 맛집, 교통 정보를 조사하세요.",
    expected_output="""다음 형식의 마크다운 보고서:
    ## 관광지 (5곳)
    - 장소명: 설명, 운영시간, 입장료
    ## 맛집 (5곳)
    - 식당명: 대표 메뉴, 가격대, 위치
    ## 교통
    - 공항 → 시내 이동 방법 2가지 이상""",
    agent=researcher
)
```

---

<a id="part4"></a>

## 4️⃣ Crew (팀) [↑](#toc)

### Crew란?

**Crew**는 Agent들과 Task들을 묶어서 실제로 실행하는 조율자입니다. `kickoff()`을 호출하면 팀이 가동됩니다.

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher],          # 팀원 목록
    tasks=[research_task],        # 업무 목록
    process=Process.sequential,   # 실행 방식 (순차 실행)
    verbose=True                  # 전체 과정 출력
)

# 팀 가동!
result = crew.kickoff()
print(result)
```

### Process 종류

| Process | 방식 | 비유 |
|---------|------|------|
| `Process.sequential` | Task를 순서대로 실행 (기본값) | 릴레이 경주 |
| `Process.hierarchical` | 매니저 Agent가 Task를 배분 | 팀장이 업무 분배 |

> 멀티에이전트 협업에서 process는 매우 중요합니다. 06장에서 자세히 다룹니다.

### kickoff() 파라미터

```python
# 입력값을 넣어서 실행
result = crew.kickoff(
    inputs={
        "destination": "서울",
        "days": "3박4일"
    }
)
# Task description에서 {destination}, {days}로 참조 가능
```

---

<a id="part5"></a>

## 5️⃣ 실습: Hello CrewAI [↑](#toc)

세 구성요소를 합쳐서 처음으로 CrewAI를 실행해봅니다.

```python
# 파일: hello_crewai.py
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew, Process, LLM

# 1. LLM 설정
llm = LLM(model="gpt-4o-mini")

# 2. Agent 생성
researcher = Agent(
    role="여행 리서치 전문가",
    goal="여행지에 대한 유용하고 실용적인 정보를 수집한다",
    backstory="당신은 10년 경력의 여행 전문 기자로, 전 세계 200개국을 방문한 경험이 있습니다. "
              "실용적인 여행 정보를 명확하게 정리하는 것이 특기입니다.",
    llm=llm,
    verbose=True
)

# 3. Task 생성
research_task = Task(
    description="서울 2박3일 여행을 위한 필수 관광지 3곳을 조사하세요. "
                "각 관광지마다 특징, 운영 시간, 팁을 포함해주세요.",
    expected_output="3개의 서울 관광지 정보를 마크다운 형식으로 정리한 보고서. "
                    "각 관광지마다 이름, 특징 2줄, 운영시간, 방문 팁을 포함할 것.",
    agent=researcher
)

# 4. Crew 생성 및 실행
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)

print("=" * 50)
print("CrewAI 시작!")
print("=" * 50)

result = crew.kickoff()

print("\n" + "=" * 50)
print("최종 결과:")
print("=" * 50)
print(result)
```

### verbose 출력 읽는 법

`verbose=True`를 설정하면 아래와 같은 출력이 나옵니다. 에이전트의 사고 과정을 확인할 수 있습니다.

```
==================================================
CrewAI 시작!
==================================================

> Entering new CrewAgentExecutor chain...

Thought: 서울의 주요 관광지 3곳에 대한 정보를 제공해야 합니다.
현재 도구 없이 학습된 지식으로 답변하겠습니다.

Final Answer:
## 서울 필수 관광지 3곳

### 1. 경복궁 (Gyeongbokgung Palace)
**특징**: 조선 왕조의 정궁으로 1395년에 창건된 서울의 대표 유적지입니다.
웅장한 근정전과 아름다운 경회루 연못이 인상적입니다.
**운영시간**: 09:00 ~ 18:00 (화요일 휴무)
**방문 팁**: 한복 착용 시 무료 입장! 오전 일찍 방문하면 인파가 적습니다.

### 2. 북촌 한옥마을 (Bukchon Hanok Village)
**특징**: 600년 역사의 전통 한옥이 밀집한 주거 지역으로, 서울 시내에서
가장 아름다운 전통 경관을 감상할 수 있습니다.
**운영시간**: 항상 개방 (주민 거주 지역이므로 조용히 관람)
**방문 팁**: 북촌 8경 코스를 따라가면 사진 명소를 빠짐없이 볼 수 있습니다.

### 3. 명동 (Myeongdong)
**특징**: 쇼핑, 스트리트 푸드, K-뷰티 브랜드가 집중된 서울 최대 번화가입니다.
외국인 관광객이 가장 많이 찾는 쇼핑 명소입니다.
**운영시간**: 매장마다 상이, 대부분 10:00 ~ 22:00
**방문 팁**: 저녁에 방문하면 스트리트 푸드 노점상이 활발하게 운영됩니다.

> Finished chain.

==================================================
최종 결과:
==================================================
## 서울 필수 관광지 3곳
...
```

| verbose 출력 요소 | 의미 |
|----------------|------|
| `Thought:` | 에이전트가 지금 무슨 생각을 하는지 |
| `Action:` | 사용하려는 도구 이름 |
| `Action Input:` | 도구에 전달하는 입력값 |
| `Observation:` | 도구 실행 결과 |
| `Final Answer:` | 최종 답변 |

---

<a id="part6"></a>

## 6️⃣ 정리 [↑](#toc)

### Agent / Task / Crew 요약

| 구성요소 | 역할 | 핵심 파라미터 |
|---------|------|-------------|
| **Agent** | AI 팀원 — 특정 역할과 목표를 가짐 | `role`, `goal`, `backstory`, `llm`, `tools` |
| **Task** | 구체적인 업무 지시 | `description`, `expected_output`, `agent` |
| **Crew** | 팀 전체 조율 및 실행 | `agents`, `tasks`, `process` |
| **kickoff()** | 팀 가동 — 모든 Task 실행 | `inputs` (선택) |

### 코드 작성 순서 (항상 이 순서로!)

```
1. LLM 설정
2. Agent 생성
3. Task 생성 (agent 지정)
4. Crew 생성 (agents, tasks 묶기)
5. crew.kickoff() 실행
```

### 다음 장 미리보기

**04장: Agent/Task 설계와 프롬프트** — 더 나은 Agent와 Task를 설계하는 법, 두 에이전트가 협업하는 방법을 배웁니다.
