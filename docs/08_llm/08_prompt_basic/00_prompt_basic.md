---
title: 프롬프트 엔지니어링 기초
layout: default
parent: LLM
nav_order: 8
has_children: true
permalink: /llm/prompt-basic
---

# 프롬프트 엔지니어링 기초

이 과정은 LLM 프롬프트 엔지니어링 입문 과정입니다. OpenAI API를 활용하여 실습 중심으로 프롬프트 작성 기술을 익히고, 간단한 자동화 도구를 직접 만들어봅니다.

## 학습 목표

1. Zero-shot 및 Few-shot 프롬프트를 작성하고 차이를 비교할 수 있다
2. Role Prompting으로 원하는 답변 스타일을 이끌어낼 수 있다
3. Chain-of-Thought(CoT) 기법으로 복잡한 추론 문제를 해결할 수 있다
4. OpenAI Python API를 이용해 프롬프트를 코드로 실행할 수 있다
5. 멀티턴 대화 구조를 이해하고 대화 흐름을 설계할 수 있다
6. 프롬프트 결과를 평가하고 개선할 수 있다
7. 배운 기법을 조합한 미니 프로젝트를 완성할 수 있다

## 과정 구성

### DAY 1 (약 120분)

| 순서 | 제목 | 시간 |
|------|------|------|
| 1 | [환경 구축과 LLM 기초](./01_환경구축과_LLM_기초) | 20분 |
| 2 | [프롬프트 구조와 기초 기법](./02_프롬프트_구조와_기초기법) | 50분 |
| 3 | [고급 기법과 API 활용](./03_고급기법과_API활용) | 50분 |

### DAY 2 (약 300분)

DAY 2에서는 멀티턴 대화 설계, 프롬프트 평가, 실무 활용 시나리오, 미니 프로젝트를 다룹니다.

## 사전 준비

- **OpenAI API 키**: [platform.openai.com](https://platform.openai.com)에서 발급
- **Google Colab**: 별도 환경 설치 없이 브라우저에서 실습 가능
- API 키는 Colab Secrets(`🔑` 아이콘)에 `OPENAI_API_KEY` 이름으로 등록
