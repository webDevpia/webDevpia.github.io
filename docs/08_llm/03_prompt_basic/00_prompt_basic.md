---
title: 프롬프트 엔지니어링 기초
layout: default
parent: LLM
nav_order: 8
has_children: true
permalink: llm/prompt-basic
---

# 프롬프트 엔지니어링 기초

AI에게 원하는 결과를 얻어내는 기술, **프롬프트 엔지니어링**을 배웁니다. 코딩 경험이 없어도 ChatGPT 웹에서 바로 실습할 수 있으며, OpenAI API를 활용한 자동화까지 다룹니다.

## 학습 목표

1. 프롬프트 엔지니어링이 왜 필요한지 이해하고, CRAFT 프레임워크로 프롬프트를 구조화할 수 있다
2. Zero-shot, Few-shot, Role Prompting 기법을 상황에 맞게 선택할 수 있다
3. Chain-of-Thought(CoT) 기법으로 복잡한 추론 문제를 해결할 수 있다
4. 멀티턴 대화를 설계하고, API로 비용 효율적인 자동화를 구현할 수 있다
5. 프롬프트 결과를 체계적으로 평가하고 개선할 수 있다
6. 배운 기법을 조합한 미니 프로젝트를 완성할 수 있다

## 과정 구성 (5장)

| 장 | 제목 | 핵심 |
|:---:|------|------|
| 1 | [왜 프롬프트인가](/llm/prompt-basic/why-prompt) | 동기부여 + 환경설정 + LLM 기초 |
| 2 | [프롬프트 기초 & CRAFT](/llm/prompt-basic/craft) | CRAFT 프레임워크 + Zero/Few-shot + Role |
| 3 | [고급기법과 실전활용](/llm/prompt-basic/advanced) | CoT + 멀티턴 + 구조화 + API 비용 |
| 4 | [프롬프트 평가와 개선](/llm/prompt-basic/evaluation) | 4가지 평가 기준 + LLM-as-Judge |
| 5 | [미니프로젝트](/llm/prompt-basic/project) | AI 챗봇 + 자소서 첨삭 + 다음 단계 |

## 사전 준비

- **ChatGPT 계정**: [chat.openai.com](https://chat.openai.com) — 1~2장은 웹에서 실습 가능
- **OpenAI API 키**: [platform.openai.com](https://platform.openai.com)에서 발급 — 3장부터 필요
- **Google Colab**: 별도 설치 없이 브라우저에서 코드 실행
- API 키는 Colab Secrets(`🔑` 아이콘)에 `OPENAI_API_KEY` 이름으로 등록

## 다음 단계

이 과정을 마친 후 [AI-Native 개발](/llm/ai-native-dev) 과정에서 GitHub Copilot Agent Mode 커스터마이징을 배울 수 있습니다.
