---
layout: default
title: LangChain
nav_order: 10
parent: LLM
has_children: true
permalink: /llm/langchain
---

# LangChain
{: .no_toc }

{: .fs-6 .fw-300 }

---

## 학습 경로 안내

이 과정은 **비전공자도 따라할 수 있는** LangChain 기초부터 RAG 프로젝트까지의 과정입니다.

### 필수 코스 (Level 1~2)

| 순서 | 주제 | 핵심 내용 |
|------|------|----------|
| 1 | [개발환경 설정](/llm/langchain/setting) | Conda, VS Code, API 키 |
| 2 | [LangChain 개요](/llm/langchain/preview) | 핵심 개념, LCEL 맛보기, 다양한 LLM 연결 |
| 3 | [LCEL](/llm/langchain/lcel) | 파이프라인 기반 — 이후 모든 교안에서 사용 |
| 4 | [프롬프트 템플릿](/llm/langchain/template) | 재사용 가능한 프롬프트 설계 |
| 5 | [출력 파서](/llm/langchain/parser) | JSON, Pydantic으로 구조화된 출력 |
| 6 | [도구](/llm/langchain/tool) | 외부 API 연결, 에이전트 기초 |
| 7 | [메모리](/llm/langchain/memory) | 대화 맥락 유지, 세션 관리 |

### 선택 코스

| 주제 | 대상 | 비고 |
|------|------|------|
| [캐싱](/llm/langchain/cache) | API 비용 최적화 시 | InMemory, SQLite, Redis 캐시 |
| [투자보고서 프로젝트](/llm/langchain/project) | 종합 실습 | yfinance + Streamlit |

### RAG 코스 (Level 2~3)

| 순서 | 주제 | 핵심 내용 |
|------|------|----------|
| 10 | RAG 개요 | VectorDB, 임베딩 모델 개념 |
| 11 | KNN/ANN/HNSW | 벡터 검색 알고리즘 이론 |
| 12 | 임베딩 모델과 인덱스 구축 | Pinecone 실습 |
| 13 | 벡터 검색 | 시맨틱 검색 + 메타데이터 필터 |
| 14 | AI 소믈리에 프로젝트 | 이미지→와인 추천 RAG 앱 |
| 15 | 주택청약 챗봇 | PDF 기반 RAG + Streamlit |

> **RAG 심화**(BM25, RRF, HyDE, 리랭킹 등)는 [RAG Retrieval](/ragretrieval) 과정을 참고하세요.

### 다음 단계

LangChain 기초를 마쳤다면 → [LangGraph](/langgraph)에서 **AI 에이전트**를 만들어 보세요.

---

## LangChain v1.0 호환성 안내 (2025.11~)

LangChain v1.0에서 다음 변경 사항이 있습니다. 이 교안은 순차적으로 업데이트 중입니다.

| 항목 | 변경 전 (v0) | 변경 후 (v1.0) |
|------|-------------|---------------|
| 에이전트 생성 | `create_react_agent()` | `create_agent()` (langchain.agents) |
| 프롬프트 파라미터 | `prompt=` | `system_prompt=` |
| 레거시 체인 | `LLMChain`, `AgentExecutor` | `langchain-classic` 패키지로 이동 |
| 레거시 메모리 | `ConversationBufferMemory` | `RunnableWithMessageHistory` (이미 교안에 반영) |

> 최신 API는 [LangChain v1.0 릴리즈 노트](https://blog.langchain.com/langchain-langgraph-1dot0/)를 참고하세요.