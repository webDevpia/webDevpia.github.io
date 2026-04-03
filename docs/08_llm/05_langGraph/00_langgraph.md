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

{: .fs-6 .fw-300 }

---

## 학습 경로 안내

LangGraph는 **AI 에이전트를 그래프 구조로 설계**하는 프레임워크입니다.

> **선수 학습**: [LangChain](/llm/langchain) 과정의 1~8번(기초~도구)을 먼저 수강하세요.

### 필수 코스

| 순서 | 주제 | 핵심 내용 |
|------|------|----------|
| 1 | 개발환경 | Conda 환경, 패키지 설치 |
| 2 | 기본 개념 | 노드, 엣지, 상태 — 그래프 구조 이해 |
| 3 | 챗봇 | StateGraph로 간단한 챗봇 만들기 |
| 4 | 챗봇 + 도구 | Tavily 검색 연동, ToolNode |
| 5 | 챗봇 + 메모리 | MemorySaver, thread_id로 대화 유지 |

### 선택 심화

| 주제 | 대상 | 비고 |
|------|------|------|
| 6. Human-in-the-Loop | 에이전트 안전성 관심자 | interrupt/resume 패턴 |
| 7. 커스텀 상태 실습 | 실무 프로젝트 | Kakao API 연동 장소 검색 챗봇 |
| 8~9. 에이전트 프로젝트 | 종합 실습 | 음식/활동 추천 멀티 에이전트 |

### LangGraph v1.0 변경 사항

| 항목 | 변경 전 | 변경 후 |
|------|--------|--------|
| 에이전트 생성 | `langgraph.prebuilt.create_react_agent` | `langchain.agents.create_agent` |
| 프롬프트 | `prompt=` | `system_prompt=` |
| 스트리밍 | `version="v1"` | `version="v2"` (type-safe) |

> 이 교안의 `ToolNode`, `tools_condition`, `StateGraph` 등 핵심 API는 v1.0에서도 동일하게 사용됩니다.