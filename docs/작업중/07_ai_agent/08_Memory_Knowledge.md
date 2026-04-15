---
title: 08. Memory & Knowledge
layout: default
grand_parent: LLM
parent: AI Agent
nav_order: 8
permalink: /llm/ai-agent/memory
---

## 학습 목표

- CrewAI의 메모리 시스템(단기/장기/엔티티)을 이해하고 활성화할 수 있다
- Knowledge 기능으로 외부 문서를 에이전트에 연결할 수 있다

<a id="toc"></a>

## 진행 순서

1. [메모리란?](#part1) - 단기/장기/엔티티 메모리 개념
2. [메모리 활성화](#part2) - Crew에서 memory=True 설정
3. [Knowledge — 외부 문서 연결](#part3) - Agentic RAG
4. [실습: 메모리가 있는 고객 상담 에이전트](#part4) - 이전 대화를 기억하는 에이전트
5. [정리](#part5) - 메모리 종류 비교표, Knowledge vs RAG

---

# 08장. Memory & Knowledge

<a id="part1"></a>

## 1️⃣ 메모리란? [↑](#toc)

AI 에이전트가 단순히 "한 번 대화하고 끝"이라면 사용자는 매번 같은 정보를 반복해서 입력해야 합니다. **메모리(Memory)**는 에이전트가 정보를 기억하고 활용할 수 있도록 해주는 기능입니다.

### 수첩 비유

> **단기 메모리**는 오늘 회의 중 메모한 포스트잇,
> **장기 메모리**는 지난달 프로젝트 전체 기록이 담긴 수첩,
> **엔티티 메모리**는 "고객사별 담당자 연락처 카드"입니다.

CrewAI는 세 가지 메모리 유형을 제공합니다:

| 메모리 유형 | 영문명 | 보존 범위 | 특징 |
|------------|--------|-----------|------|
| 단기 메모리 | Short-term Memory | 현재 Crew 실행 내 | 태스크 간 정보 공유 |
| 장기 메모리 | Long-term Memory | 실행 간(영구 저장) | 이전 실행 결과 학습 |
| 엔티티 메모리 | Entity Memory | 현재 실행 내 | 인물/장소/개념 단위 관리 |

### 단기 메모리 (Short-term Memory)

현재 Crew 실행 내에서 에이전트들이 서로 정보를 공유합니다. Task A의 결과를 Task B에서 참조하는 것이 단기 메모리의 대표적인 활용입니다.

```python
# 단기 메모리 활용 예시: 앞 Task의 결과가 자동으로 다음 Task에 전달됨
research_task = Task(
    description="서울의 인기 카페 5곳을 조사하세요.",
    expected_output="카페 이름, 위치, 특징을 포함한 목록",
    agent=researcher
)

summary_task = Task(
    description="조사된 카페 정보를 바탕으로 추천 이유를 작성하세요.",
    expected_output="각 카페의 추천 이유 1~2문장",
    agent=writer,
    context=[research_task]  # 앞 태스크의 결과를 컨텍스트로 전달
)
```

### 장기 메모리 (Long-term Memory)

Crew 실행이 끝난 이후에도 학습 결과를 유지합니다. SQLite 데이터베이스에 저장되므로, 다음 실행 시 이전 실행에서 얻은 지식을 활용할 수 있습니다.

### 엔티티 메모리 (Entity Memory)

대화 중 등장하는 **사람, 장소, 개념, 조직** 등을 별도로 추출하여 관리합니다. 예를 들어 "김철수 고객은 서울 거주, VIP 등급"처럼 엔티티별 정보를 축적합니다.

---

<a id="part2"></a>

## 2️⃣ 메모리 활성화 [↑](#toc)

메모리 활성화는 `Crew` 생성 시 `memory=True` 옵션 하나로 가능합니다.

```python
from crewai import Agent, Task, Crew

# 에이전트 정의
agent = Agent(
    role="고객 상담사",
    goal="고객의 문제를 친절하고 정확하게 해결한다",
    backstory="5년 경력의 고객 서비스 전문가로, 고객의 상황을 빠르게 파악하고 맞춤형 해결책을 제시합니다.",
    verbose=True
)

task = Task(
    description="고객의 문의사항에 답변하세요: {customer_query}",
    expected_output="친절하고 명확한 답변",
    agent=agent
)

# memory=True 로 모든 메모리 유형 활성화
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,      # 단기 + 장기 + 엔티티 메모리 모두 활성화
    verbose=True
)

result = crew.kickoff(inputs={"customer_query": "환불 정책이 어떻게 되나요?"})
print(result)
```

### 메모리 세부 설정

각 메모리 유형을 개별적으로 제어할 수도 있습니다:

```python
from crewai import Crew
from crewai.memory import ShortTermMemory, LongTermMemory, EntityMemory

crew = Crew(
    agents=[agent],
    tasks=[task],
    # 각 메모리를 개별 활성화
    short_term_memory=ShortTermMemory(),   # 현재 실행 내 공유
    long_term_memory=LongTermMemory(),     # 실행 간 지속
    entity_memory=EntityMemory(),          # 엔티티별 관리
    verbose=True
)
```

> **참고:** `memory=True`는 세 가지 메모리를 기본 설정으로 모두 활성화하는 단축 옵션입니다. 개별 설정이 필요할 때만 위처럼 따로 지정합니다.

---

<a id="part3"></a>

## 3️⃣ Knowledge — 외부 문서 연결 (Agentic RAG) [↑](#toc)

**Knowledge**는 에이전트가 작업 중 참고할 수 있는 **외부 문서나 데이터**를 연결하는 기능입니다.

### 참고 자료집 비유

> **Knowledge**는 에이전트의 참고 자료집입니다.
> 의사에게 최신 의학 논문을, 법률 에이전트에게 법령집을 제공하는 것처럼,
> 에이전트가 필요할 때마다 찾아볼 수 있는 전문 자료를 붙여두는 기능입니다.

### 지원하는 Knowledge Source 유형

| 유형 | 클래스 | 설명 |
|------|--------|------|
| 텍스트 파일 | `TextFileKnowledgeSource` | `.txt` 파일 연결 |
| PDF 파일 | `PDFKnowledgeSource` | PDF 문서 연결 |
| CSV 파일 | `CSVKnowledgeSource` | 표 형식 데이터 연결 |
| 웹 페이지 | `WebsiteKnowledgeSource` | URL 기반 웹 문서 |
| 직접 입력 | `StringKnowledgeSource` | 문자열로 직접 지식 제공 |

### 텍스트 파일 Knowledge 연결

```python
from crewai import Agent, Task, Crew
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

# company_info.txt 파일을 Knowledge Source로 등록
source = TextFileKnowledgeSource(file_paths=["company_info.txt"])

# 에이전트에 Knowledge Source 연결
agent = Agent(
    role="회사 안내 전문가",
    goal="회사에 관한 질문에 정확히 답변한다",
    backstory="회사의 모든 정보를 숙지하고 있는 공식 안내 담당자입니다.",
    knowledge_sources=[source],   # Knowledge 연결!
    verbose=True
)

task = Task(
    description="다음 질문에 답변하세요: {question}",
    expected_output="회사 정보를 바탕으로 한 정확한 답변",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff(inputs={"question": "회사의 환불 정책은 무엇인가요?"})
```

### PDF Knowledge 연결

```python
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

# PDF 파일 연결
pdf_source = PDFKnowledgeSource(file_paths=["product_manual.pdf"])

agent = Agent(
    role="제품 기술 지원 전문가",
    goal="제품 매뉴얼을 바탕으로 기술 문의에 답변한다",
    backstory="제품의 모든 기술적 세부사항을 파악하고 있는 기술 지원 담당자입니다.",
    knowledge_sources=[pdf_source],
    verbose=True
)
```

### 문자열로 직접 Knowledge 제공

파일 없이 코드 내에서 직접 지식을 제공할 수도 있습니다:

```python
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# 문자열로 직접 지식 제공
company_info = """
회사명: 테크스타트 주식회사
설립: 2020년 3월
주요 제품: AI 기반 고객 서비스 솔루션
환불 정책: 구매 후 30일 이내 전액 환불 가능
고객센터: 1234-5678 (평일 09:00~18:00)
"""

string_source = StringKnowledgeSource(content=company_info)

agent = Agent(
    role="고객 지원 에이전트",
    goal="회사 정보를 바탕으로 고객 문의에 답변한다",
    backstory="회사의 공식 고객 지원 담당자입니다.",
    knowledge_sources=[string_source]
)
```

### Knowledge vs 일반 RAG의 차이

| 구분 | Knowledge (CrewAI) | 일반 RAG |
|------|-------------------|---------|
| 설정 방식 | 에이전트/Crew 레벨에서 직접 연결 | 별도 파이프라인 구축 필요 |
| 관리 주체 | CrewAI 프레임워크 자동 처리 | 개발자 직접 구현 |
| 검색 시점 | 에이전트가 필요할 때 자동 조회 | 명시적 검색 호출 필요 |
| 통합 방식 | Agent/Task 정의에 포함 | 별도 도구로 주입 |

---

<a id="part4"></a>

## 4️⃣ 실습: 메모리가 있는 고객 상담 에이전트 [↑](#toc)

이전 질문을 기억하여 더 자연스럽게 대화하는 고객 상담 에이전트를 만들어봅니다.

### 실습 목표

- 같은 질문을 2번 실행하면 두 번째 실행에서는 이전 답변을 참고
- 장기 메모리로 대화 내용이 실행 간 유지됨을 확인

### 전체 코드

```python
# 파일명: 08_memory_agent.py
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

load_dotenv()  # .env에서 OPENAI_API_KEY 로드

# ─── 에이전트 정의 ───────────────────────────────────────────
consultant = Agent(
    role="고객 상담 전문가",
    goal="고객의 질문에 친절하고 정확하게 답변하며, 이전 대화 내용을 활용한다",
    backstory=(
        "당신은 10년 경력의 고객 서비스 전문가입니다. "
        "고객의 이전 문의 기록을 참고하여 더욱 개인화된 서비스를 제공합니다."
    ),
    verbose=True
)

# ─── 태스크 정의 ─────────────────────────────────────────────
def create_task(query: str) -> Task:
    return Task(
        description=f"다음 고객 문의에 답변하세요: {query}",
        expected_output="명확하고 친절한 답변 (이전 문의 내용이 있다면 참고)",
        agent=consultant
    )

# ─── Crew 생성 (memory=True) ────────────────────────────────
def run_consultation(query: str):
    task = create_task(query)
    crew = Crew(
        agents=[consultant],
        tasks=[task],
        memory=True,    # 장기/단기/엔티티 메모리 활성화
        verbose=True
    )
    result = crew.kickoff()
    print(f"\n[답변]\n{result}\n")
    return result

# ─── 실행: 같은 주제로 2번 문의 ───────────────────────────────
if __name__ == "__main__":
    # 첫 번째 문의
    print("=" * 50)
    print("첫 번째 문의")
    print("=" * 50)
    run_consultation("노트북을 구매했는데 배터리 수명이 짧습니다.")

    # 두 번째 문의 (이전 대화 기억)
    print("=" * 50)
    print("두 번째 문의 (이전 대화 참고 여부 확인)")
    print("=" * 50)
    run_consultation("아까 말씀드린 배터리 문제로 환불을 받고 싶습니다.")
```

### 실행 방법

```bash
# 환경 준비
pip install crewai python-dotenv

# 실행
python 08_memory_agent.py
```

### 예상 결과

두 번째 실행에서 에이전트가 첫 번째 문의(배터리 문제)를 참고하여 환불 절차를 안내합니다. `verbose=True` 덕분에 에이전트가 메모리에서 이전 정보를 조회하는 과정을 터미널에서 확인할 수 있습니다.

---

<a id="part5"></a>

## 5️⃣ 정리 [↑](#toc)

### 메모리 종류 비교표

| 메모리 유형 | 활성화 방법 | 저장 위치 | 사라지는 시점 | 주요 활용 |
|------------|-----------|---------|------------|---------|
| 단기 메모리 | `memory=True` | 메모리 내 | Crew 실행 종료 시 | Task 간 컨텍스트 공유 |
| 장기 메모리 | `memory=True` | SQLite DB | 명시적 삭제 전까지 | 실행 간 학습, 개인화 |
| 엔티티 메모리 | `memory=True` | 메모리 내 | Crew 실행 종료 시 | 인물/장소/개념 추적 |

### Knowledge vs RAG 차이

| 관점 | Knowledge | 별도 RAG 파이프라인 |
|------|-----------|-----------------|
| 설정 난이도 | 쉬움 (파라미터 1개) | 높음 (벡터DB, 임베딩 등 별도 구축) |
| 유연성 | CrewAI 내 표준 방식 | 완전 커스텀 가능 |
| 추천 상황 | 빠른 프로토타이핑, 표준 문서 연결 | 대규모 문서, 특수 검색 요구사항 |

### 핵심 요약

- `memory=True` 한 줄로 세 가지 메모리(단기/장기/엔티티)를 모두 활성화
- `knowledge_sources=[source]`로 에이전트에게 참고 문서를 제공 (Agentic RAG)
- 장기 메모리는 SQLite에 저장되어 다음 실행에서도 유지됨
- Knowledge는 파일/PDF/CSV/URL/문자열 등 다양한 형식 지원

> **다음 장 미리보기:** 여러 Crew를 연결하여 복잡한 워크플로를 구성하는 **Flow** 기능을 배웁니다.
