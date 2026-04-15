---
title: AI-Native Development
layout: default
nav_order: 11
has_children: true
permalink: /ai-native
---

# AI-Native Development
{: .no_toc }

GitHub Copilot을 활용한 AI 네이티브 소프트웨어 개발 실습입니다. 2일(12시간) 과정.
{: .fs-6 .fw-300 }

---

## 과정 소개

AI가 개발 도구의 중심이 된 지금, 중요한 것은 코드를 얼마나 빨리 쓰느냐가 아닙니다.
AI와 협업해서 **검증 가능한 결과물**을 안정적으로 만들어내는 능력입니다.

이 과정은 GitHub Copilot의 커스터마이징 기능을 단계적으로 익히고, Todo Manager 프로젝트를 AI와 함께 완성하는 실습 중심 교육입니다.

## 전체 흐름

```
환경 구축 → AI-Native 이해 → Custom Instructions → Prompt Files → Custom Agents → TDD → 통합
```

| 장 | 제목 | 핵심 내용 |
|----|------|-----------|
| 01 | [실습환경 구축](/ai-native/setup) | uv, Python 3.12, VS Code, GitHub Copilot Chat 설치 및 검증 |
| 02 | [AI-Native 개발 개요](/ai-native/overview) | 전통 개발과 AI-Native 개발의 차이, 에이전트 생태계 |
| 03 | [Copilot 커스터마이징과 Custom Instructions](/ai-native/instructions) | 3요소 구조 이해, Instructions 파일 실습 |
| 04 | [Prompt Files](/ai-native/prompt-files) | 반복 작업 템플릿화, 동적 변수 활용 |

## 최종 산출물

이 과정이 끝나면 `.github/` 폴더에 아래 파일들이 채워진 Todo Manager 프로젝트가 완성됩니다.

```
.github/
├── copilot-instructions.md       # 프로젝트 공통 규칙
├── instructions/
│   ├── general.instructions.md   # Python 코딩 규칙
│   └── testing.instructions.md   # pytest + AAA 패턴 규칙
├── prompts/
│   ├── new-feature.prompt.md     # 새 기능 추가 템플릿
│   ├── write-tests.prompt.md     # 테스트 작성 템플릿
│   └── code-review.prompt.md     # 코드 리뷰 템플릿
└── agents/
    └── ...                       # (이후 과정에서 추가)
```
