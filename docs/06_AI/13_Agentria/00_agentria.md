---
layout: default
title: Agentria
nav_order: 13
has_children: true
permalink: /agentria
---

# Agentria 기반 AI 에이전트 부트캠프
{: .no_toc }

동의대학교 × 제네시스랩 AI 부트캠프 교육 과정입니다.

## 과정 구성

| 과정 | 시간 | 핵심 학습 범위 | 대상 |
|------|------|---------------|------|
| [중급 공통과정](/agentria/common) | 45시간 (5일×9시간) | Ability (워크플로우) 마스터 | 전공자 (AI Agent 비경험자) |
| [중급 전문(1) 과정](/agentria/advanced) | 45시간 (5일×9시간) | Agent (자율형) 고급 구축 | 공통과정 이수자 |

## Agentria 3계층 아키텍처

```mermaid
flowchart TD
    Agent["🤖 Agent<br/>(자율형 판단 주체)<br/>ReAct + 메모리"]
    Ability["⚙️ Ability<br/>(자동화 워크플로우)<br/>노드들의 연결"]
    LLM["LLM 노드"]
    Python["Python 노드"]
    Tool["도구 노드<br/>Gmail / Slack"]

    Agent -->|"도구로 호출"| Ability
    Ability -->|"구성 요소"| LLM
    Ability -->|"구성 요소"| Python
    Ability -->|"구성 요소"| Tool

    style Agent fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Ability fill:#2196F3,stroke:#1565C0,color:#fff
    style LLM fill:#E3F2FD,stroke:#1565C0
    style Python fill:#E3F2FD,stroke:#1565C0
    style Tool fill:#E3F2FD,stroke:#1565C0
```

## 참고 자료

- [Agentria 공식 문서](https://agentria.ai/docs/about-agentria-ko)
- [교육설계 분석 보고서](/agentria/analysis)
