---
title: 04. Agent/Task 설계와 프롬프트
layout: default
grand_parent: LLM
parent: AI Agent
nav_order: 4
permalink: /llm/ai-agent/design
---

# 04장. Agent/Task 설계와 프롬프트
{: .no_toc }

## 학습 목표

- 효과적인 Agent의 role/goal/backstory를 설계할 수 있다
- Task 간 의존관계(context)를 설정하여 2인 에이전트 협업을 구현할 수 있다

<a id="toc"></a>

## 진행 순서

1. [좋은 Agent 설계법](#part1) — 구체성, 측정 가능성, 전문성
2. [좋은 Task 설계법](#part2) — 명확한 지시, 형식 지정, context 연결
3. [2인 에이전트 협업](#part3) — 리서처 + 작가
4. [실습: 블로그 작성 에이전트 팀](#part4) — 전체 코드 실행
5. [정리](#part5) — 설계 체크리스트

---

<a id="part1"></a>

## 1️⃣ 좋은 Agent 설계법 [↑](#toc)

### 채용 공고 비유

> 좋은 Agent 설계는 좋은 채용 공고 작성과 같습니다.
> "열정 있는 분" (X) → "Google Analytics 3년 이상 경력자" (O)
> 구체적일수록 에이전트가 역할을 더 잘 수행합니다.

### role: 구체적인 직책

```python
# 나쁜 예 — 너무 일반적
role = "AI 어시스턴트"         # 무엇을 잘 하는지 불명확
role = "리서처"               # 어떤 분야인지 불명확

# 좋은 예 — 구체적인 전문 직책
role = "IT 기술 트렌드 리서치 전문가"
role = "여행 블로그 전문 작가"
role = "데이터 기반 마케팅 분석가"
```

### goal: 측정 가능한 목표

```python
# 나쁜 예 — 모호한 목표
goal = "좋은 결과를 만든다"
goal = "열심히 일한다"

# 좋은 예 — 구체적이고 측정 가능한 목표
goal = "최신 IT 뉴스 중 비개발자도 이해할 수 있는 인사이트 3가지를 추출한다"
goal = "초보 여행자도 바로 활용할 수 있는 실용적인 여행 정보를 제공한다"
```

### backstory: 전문성과 개성 부여

backstory는 에이전트의 **시스템 프롬프트**에 직접 반영됩니다. 전문성, 말투, 접근 방식을 결정합니다.

```python
# 나쁜 예 — 정보가 없음
backstory = "당신은 AI 어시스턴트입니다."

# 좋은 예 — 전문성, 경험, 특기를 상세히
backstory = (
    "당신은 15년 경력의 IT 전문 저널리스트입니다. "
    "테크크런치, 와이어드 등 해외 매체를 매일 모니터링하며 "
    "최신 기술 트렌드를 한국 독자에게 쉽게 전달하는 것이 특기입니다. "
    "전문 용어를 일상 언어로 풀어 설명하는 능력이 뛰어납니다."
)
```

### 나쁜 예 vs 좋은 예 비교

| 항목 | 나쁜 예 | 좋은 예 |
|------|--------|--------|
| role | "AI 어시스턴트" | "여행 블로그 전문 작가" |
| goal | "좋은 글을 쓴다" | "초보 여행자가 바로 활용할 수 있는 여행 정보를 800자 블로그 글로 작성한다" |
| backstory | "당신은 글을 잘 씁니다" | "10년간 트래블러 매거진 수석 편집장으로 근무하며 연간 50편 이상의 여행기를 집필했습니다. 독자의 시선을 사로잡는 도입부 작성이 특기입니다." |

---

<a id="part2"></a>

## 2️⃣ 좋은 Task 설계법 [↑](#toc)

### description: 5W1H로 작성

```python
# 나쁜 예 — 모호한 지시
description = "서울 여행 정보 정리해줘"

# 좋은 예 — 구체적인 지시
description = (
    "서울에서 처음 여행하는 30대 직장인을 위한 2박3일 여행 정보를 조사하세요. "
    "다음 항목을 포함해주세요:\n"
    "1. 필수 관광지 3곳 (위치, 운영시간, 입장료, 방문 팁)\n"
    "2. 현지인 추천 맛집 3곳 (메뉴, 가격대, 예약 필요 여부)\n"
    "3. 숙소 추천 지역 2곳 (장단점)\n"
    "4. 공항에서 시내까지 교통편 옵션"
)
```

### expected_output: 출력 형식을 명확히

```python
# 나쁜 예 — 형식 미지정
expected_output = "여행 보고서"

# 좋은 예 — 형식, 길이, 구조 명시
expected_output = (
    "마크다운 형식의 여행 가이드 (총 600자 이상).\n"
    "## 관광지, ## 맛집, ## 숙소, ## 교통 섹션으로 구성.\n"
    "각 항목은 불릿 리스트로 작성."
)
```

### context: Task 간 결과 전달

`context` 파라미터는 이전 Task의 출력을 다음 Task의 입력으로 전달합니다. 에이전트 협업의 핵심입니다.

```python
research_task = Task(
    description="서울 여행 정보 조사",
    expected_output="관광지, 맛집, 교통 정보 보고서",
    agent=researcher
)

writing_task = Task(
    description="조사 결과를 바탕으로 여행 블로그 글 작성",
    expected_output="독자를 위한 서울 여행 블로그 포스팅",
    agent=writer,
    context=[research_task]  # ← researcher의 결과를 writer가 참고!
)
```

### context 없을 때 vs 있을 때

```
# context 없을 때
writing_task: 작가가 처음부터 스스로 여행 정보를 생각해내야 함 → 부정확할 수 있음

# context 있을 때
writing_task: 작가가 researcher의 조사 결과를 읽고 → 그 내용을 바탕으로 글 작성 → 정확하고 일관성 있음
```

---

<a id="part3"></a>

## 3️⃣ 2인 에이전트 협업 [↑](#toc)

### 분업의 힘

> 혼자서 조사도 하고 글도 쓰면 결과물의 질이 떨어집니다.
> 전문가를 분리하면 각자 자기 역할에 집중할 수 있습니다.

```
리서처 (Researcher)          작가 (Writer)
       ↓                           ↑
  [관광지/맛집/교통 조사]  →  [context로 전달]  →  [블로그 글 작성]
```

### 에이전트 2명 설계

```python
from crewai import Agent, LLM

llm = LLM(model="gpt-4o-mini")

# 에이전트 1: 리서치 전문가
researcher = Agent(
    role="여행 리서치 전문가",
    goal="여행지의 관광지, 맛집, 교통 정보를 정확하고 실용적으로 수집한다",
    backstory=(
        "당신은 15년간 여행 정보 전문 기자로 일했습니다. "
        "국내외 주요 여행지를 직접 방문하여 검증된 정보만을 제공합니다. "
        "데이터와 현지 경험을 바탕으로 한 실용적인 정보 제공이 특기입니다."
    ),
    llm=llm,
    verbose=True
)

# 에이전트 2: 여행 블로그 작가
writer = Agent(
    role="여행 블로그 전문 작가",
    goal="독자가 실제로 여행을 떠나고 싶어지는 생동감 있는 블로그 글을 작성한다",
    backstory=(
        "당신은 인기 여행 블로그 '어디든 가자'를 운영하는 작가입니다. "
        "구독자 50만 명을 보유하고 있으며, "
        "복잡한 여행 정보를 읽기 쉽고 재미있게 풀어내는 것이 특기입니다. "
        "독자의 시선을 사로잡는 도입부와 생생한 묘사로 유명합니다."
    ),
    llm=llm,
    verbose=True
)
```

### Task 2개 — context로 연결

```python
from crewai import Task

# Task 1: 리서치 (researcher 담당)
research_task = Task(
    description=(
        "서울 2박3일 여행을 위한 다음 정보를 조사하세요:\n"
        "1. 인기 관광지 3곳 (이름, 특징, 운영시간, 교통편)\n"
        "2. 현지 맛집 3곳 (메뉴, 가격대, 위치)\n"
        "3. 숙소 추천 지역 (강남, 홍대, 명동 중 선택 이유)"
    ),
    expected_output=(
        "마크다운 형식의 서울 여행 리서치 보고서. "
        "## 관광지, ## 맛집, ## 숙소 추천 섹션 포함."
    ),
    agent=researcher
)

# Task 2: 블로그 글 작성 (writer 담당, researcher 결과 참고)
writing_task = Task(
    description=(
        "리서치 결과를 바탕으로 서울 여행 블로그 포스팅을 작성하세요.\n"
        "대상 독자: 처음 서울을 방문하는 20~30대 여행자\n"
        "톤: 친근하고 설레는 여행의 느낌\n"
        "구성: 매력적인 제목, 흥미로운 도입부, 본문, 마무리"
    ),
    expected_output=(
        "600자 이상의 서울 여행 블로그 포스팅. "
        "제목, 도입부(분위기 유도), 관광/맛집/숙소 소개, 마무리 포함."
    ),
    agent=writer,
    context=[research_task]  # researcher의 조사 결과를 참고
)
```

---

<a id="part4"></a>

## 4️⃣ 실습: 블로그 작성 에이전트 팀 [↑](#toc)

```python
# 파일: blog_writer_crew.py
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew, Process, LLM

llm = LLM(model="gpt-4o-mini")

# ── 에이전트 설정 ──────────────────────────────────────
researcher = Agent(
    role="여행 리서치 전문가",
    goal="여행지의 관광지, 맛집, 교통 정보를 정확하고 실용적으로 수집한다",
    backstory=(
        "당신은 15년간 여행 정보 전문 기자로 일했습니다. "
        "데이터와 현지 경험을 바탕으로 한 실용적인 정보 제공이 특기입니다."
    ),
    llm=llm,
    verbose=True
)

writer = Agent(
    role="여행 블로그 전문 작가",
    goal="독자가 실제로 여행을 떠나고 싶어지는 생동감 있는 블로그 글을 작성한다",
    backstory=(
        "당신은 구독자 50만 명의 여행 블로그 운영자입니다. "
        "복잡한 정보를 읽기 쉽고 재미있게 풀어내는 것이 특기입니다."
    ),
    llm=llm,
    verbose=True
)

# ── Task 설정 ──────────────────────────────────────────
research_task = Task(
    description=(
        "서울 2박3일 여행을 위한 핵심 정보를 조사하세요:\n"
        "- 관광지 3곳 (이름, 특징, 운영시간)\n"
        "- 맛집 3곳 (메뉴, 가격대)\n"
        "- 숙소 추천 지역 1곳 (이유)"
    ),
    expected_output="마크다운 형식의 서울 여행 리서치 보고서",
    agent=researcher
)

writing_task = Task(
    description=(
        "리서치 결과를 바탕으로 서울 여행 블로그 포스팅을 작성하세요.\n"
        "대상: 20~30대 초보 여행자 / 톤: 친근하고 설레는 느낌"
    ),
    expected_output="600자 이상의 서울 여행 블로그 포스팅 (제목 포함)",
    agent=writer,
    context=[research_task]
)

# ── Crew 실행 ──────────────────────────────────────────
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()

print("\n" + "=" * 60)
print("최종 블로그 포스팅:")
print("=" * 60)
print(result)
```

### 실행 결과 (요약)

```
> Entering new CrewAgentExecutor chain... (researcher)
Thought: 서울 2박3일 여행 정보를 조사하겠습니다.
Final Answer:
## 관광지
- **경복궁**: 조선 왕조 정궁, 09:00~18:00, 입장료 3,000원
- **북촌 한옥마을**: 전통 한옥 밀집 지역, 상시 개방
- **홍대 거리**: 젊음의 문화 중심지, 오전~심야

## 맛집
- **광장시장**: 전통 시장 먹거리 (빈대떡, 순대) — 1인 5,000~15,000원
- **홍대 떡볶이 골목**: 다양한 분식 — 1인 5,000~10,000원
- **을지로 골목식당**: 서민 한식 — 1인 8,000~15,000원

## 숙소 추천
- **홍대/합정**: 젊고 활기찬 분위기, 대중교통 접근성 최고

> Entering new CrewAgentExecutor chain... (writer)
Thought: 리서치 결과를 바탕으로 생동감 있는 블로그 글을 작성하겠습니다.
Final Answer:

# 서울 2박3일, 처음이어도 완벽한 여행 가이드 🗺️

비행기에서 내리는 순간부터 심장이 두근거렸습니다.
서울이라는 도시는 처음 방문하는 이에게도 마치 오래된 친구처럼 따뜻하게 맞아줍니다...

[본문 계속...]

> Finished chain.

============================================================
최종 블로그 포스팅:
============================================================
# 서울 2박3일, 처음이어도 완벽한 여행 가이드
...
```

---

<a id="part5"></a>

## 5️⃣ 정리 [↑](#toc)

### Agent 설계 체크리스트

- [ ] `role`이 구체적인 직함인가? ("AI 어시스턴트" X → "여행 리서치 전문가" O)
- [ ] `goal`이 측정 가능한 목표인가? ("잘 하기" X → "3가지 인사이트 추출" O)
- [ ] `backstory`에 전문성, 경험, 특기가 포함되어 있는가?
- [ ] 한 Agent가 너무 많은 역할을 맡지 않는가? (역할 분리 원칙)

### Task 설계 체크리스트

- [ ] `description`에 무엇을, 어떻게, 얼마나 해야 하는지 명시했는가?
- [ ] `expected_output`에 형식(마크다운, JSON 등)과 길이를 지정했는가?
- [ ] 이전 Task의 결과가 필요하면 `context`를 연결했는가?
- [ ] Task 하나가 너무 많은 일을 하지는 않는가? (단일 책임 원칙)

### 핵심 패턴 요약

```python
# 2인 협업 패턴 (가장 자주 쓰는 패턴)
task_1 = Task(..., agent=agent_1)
task_2 = Task(..., agent=agent_2, context=[task_1])  # task_1 결과를 참고

crew = Crew(
    agents=[agent_1, agent_2],
    tasks=[task_1, task_2],
    process=Process.sequential  # task_1 완료 후 task_2 실행
)
```

### 다음 장 미리보기

**05장: 외부 도구(Tools) 연동** — 에이전트에게 웹 검색, 계산기 등 실제 도구를 연결하여 더 강력하게 만들어봅니다.
