---
layout: default
title: LangGraph
parent: LLM
nav_order: 12
has_children: true
permalink: /langgraph
---

# LangGraph
{: .no_toc }

AI 에이전트를 그래프 구조로 설계하는 프레임워크
{: .fs-6 .fw-300 }

---

## 학습 경로 안내

LangGraph는 **AI 에이전트를 그래프 구조로 설계**하는 프레임워크입니다. 노드(처리 단계), 엣지(전환), 상태(공유 메모리)를 조합하여 복잡한 AI 워크플로우를 만들 수 있습니다.

> **선수 학습**: [LangChain](/llm/langchain) 과정의 1~8번(기초~도구)을 먼저 수강하세요.

---

## 전체 구성

### Part 1: 기초 (ch 1~5)

| 순서 | 주제 | 핵심 내용 |
|:----:|------|----------|
| 1 | [개발환경](/llm/langgraph/env) | uv 환경, 패키지 설치, 프로젝트 구조 |
| 2 | [기본 개념](/llm/langgraph/preview) | 노드, 엣지, 상태 — 그래프 구조 이해 |
| 3 | [챗봇](/llm/langgraph/chat) | StateGraph로 간단한 챗봇 만들기 |
| 4 | [챗봇 + 도구](/llm/langgraph/chat_tool) | Tavily 검색 연동, ToolNode |
| 5 | [챗봇 + 메모리](/llm/langgraph/chat_memory) | InMemorySaver, SqliteSaver, thread_id |

### Part 2: 심화 (ch 6~8)

| 순서 | 주제 | 핵심 내용 |
|:----:|------|----------|
| 6 | [상태 관리 심화](/llm/langgraph/state_deep) | Reducer 패턴, 복합 상태, MessagesState |
| 7 | [Human-in-the-Loop](/llm/langgraph/chat_human) | interrupt/resume, 승인 게이트, Time Travel |
| 8 | [스트리밍 심화](/llm/langgraph/streaming) | stream_mode 비교, 토큰 단위 스트리밍 |

### Part 3: 고급 (ch 9~12)

| 순서 | 주제 | 핵심 내용 |
|:----:|------|----------|
| 9 | [서브그래프](/llm/langgraph/subgraph) | 그래프 안의 그래프, 모듈화와 재사용 |
| 10 | [멀티 에이전트 패턴](/llm/langgraph/multi_agent) | Router, Supervisor, Handoff 패턴 |
| 11 | [에러 처리와 재시도](/llm/langgraph/error_handling) | retry, fallback, 타임아웃, 출력 검증 |
| 12 | [비동기 패턴](/llm/langgraph/async) | async/await, 병렬 팬아웃 (Send API) |

### Part 4: 프로젝트 (ch 13~17)

| 순서 | 주제 | 핵심 내용 |
|:----:|------|----------|
| 13 | [커스텀 상태 실습](/llm/langgraph/chat_lab) | Kakao API 연동 장소 검색 챗봇 |
| 14 | [프로덕션 준비](/llm/langgraph/production) | 테스트, 모니터링, 체크포인터, 보안 |
| 15 | [프로젝트 정의서](/llm/langgraph/agent_proj) | 음식/활동 추천 멀티 에이전트 설계 |
| 16 | [프로젝트 구현](/llm/langgraph/agent_task) | 10개 에이전트 구현 + 그래프 통합 |
| 17 | [Streamlit UI 배포](/llm/langgraph/deployment) | Streamlit 채팅 UI + 클라우드 배포 |

---

## LangGraph v1.0 변경 사항

| 항목 | 변경 전 | 변경 후 |
|------|--------|--------|
| 에이전트 생성 | `langgraph.prebuilt.create_react_agent` | `langchain.agents.create_agent` (함수명도 변경) |
| 체크포인터 | `MemorySaver` | `InMemorySaver` (권장 명칭 변경) |
| 시작점 설정 | `set_entry_point("node")` | `add_edge(START, "node")` |
| Tavily 도구 | `langchain_community.tools.tavily_search.TavilySearchResults` | `langchain_tavily.TavilySearch` (별도 패키지) |

> 이 교안의 `ToolNode`, `tools_condition`, `StateGraph` 등 핵심 API는 v1.0에서도 동일하게 사용됩니다. 단, 일부 보조 API(체크포인터, Tavily 도구 등)는 변경되었으므로 각 단원의 안내를 참고하세요.
