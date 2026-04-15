---
title: AI Agent
layout: default
parent: LLM
nav_order: 6
has_children: true
permalink: /llm/ai-agent
---

# AI Agent (CrewAI)
{: .no_toc }

CrewAI 프레임워크를 활용한 AI 에이전트 개발 실습입니다. 2일(16시간) 과정.
{: .fs-6 .fw-300 }

## 학습 목표

- AI 에이전트의 개념과 작동 원리를 이해할 수 있다
- CrewAI를 활용하여 Agent, Task, Crew를 설계하고 실행할 수 있다
- 외부 도구(Tools)를 연동하여 에이전트의 능력을 확장할 수 있다
- 멀티에이전트 팀을 구성하여 복잡한 작업을 자동화할 수 있다

<a id="toc"></a>

## 커리큘럼

### Day 1 — 기초 다지기 (8시간)

| 장 | 주제 | 핵심 내용 |
|----|------|---------|
| 01 | [AI 에이전트 개론](/llm/ai-agent/intro) | 에이전트란? 챗봇과의 차이, 4가지 구성 요소 |
| 02 | [개발환경 준비](/llm/ai-agent/setup) | Python, CrewAI 설치, 첫 LLM 호출 |
| 03 | [CrewAI 핵심 개념](/llm/ai-agent/core-concepts) | Agent, Task, Crew, kickoff() |
| 04 | [Agent/Task 설계](/llm/ai-agent/design) | 효과적인 프롬프트 설계, 2인 협업 |
| 05 | [외부 도구 연동](/llm/ai-agent/tools) | 내장 도구, 커스텀 도구 만들기 |
| 06 | [멀티에이전트 협업](/llm/ai-agent/multi-agent) | Sequential, Hierarchical 프로세스 |
| 07 | [Day 1 종합 실습](/llm/ai-agent/day1-practice) | 뉴스 리서치 & 요약 에이전트 |

### Day 2 — 심화 실습 (8시간)

> Day 2 강의 자료는 추후 업로드됩니다.

---

## 사전 준비

### 필요한 것

- **Python 3.11 이상** 설치
- **OpenAI API 키** ([platform.openai.com](https://platform.openai.com) 에서 발급)
- **VS Code** 또는 Jupyter Notebook
- 예상 비용: GPT-4o-mini 기준 2일 실습 약 $0.50~$1.00

### 빠른 시작

```bash
# 프로젝트 폴더 생성 및 패키지 설치
uv init ai-agent-workshop
cd ai-agent-workshop
uv add crewai crewai-tools python-dotenv
```

---

## 이런 분께 적합합니다

- Python 기초 문법을 알고 있는 분 (함수, 클래스 개념 이해)
- AI/LLM에 관심이 있고 실무에 적용하고 싶은 분
- 챗봇을 넘어 자율적으로 행동하는 AI를 만들어보고 싶은 분
