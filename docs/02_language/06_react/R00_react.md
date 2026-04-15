---
title: React
layout: default
parent: Language
nav_order: 6
has_children: true
permalink: /language/react
---

{% raw %}

# React 19 — 비전공자를 위한 모던 React

> "복잡한 이론보다 동작하는 코드 한 줄이 낫습니다."

---

## 학습 대상

| 항목 | 내용 |
|------|------|
| 대상 | 프로그래밍 경험이 있는 비전공자 |
| 선수 지식 | JavaScript 기초 (변수, 함수, 조건문, 반복문) |
| 목표 | React 19로 날씨 앱을 혼자 만들 수 있다 |

> **선수 지식이 부족하다면?** → 00장 (JavaScript 복습)부터 시작하세요.

---

## 사용 도구

| 도구 | 버전 | 용도 |
|------|------|------|
| React | 19.x | UI 라이브러리 |
| Vite | 6.x | 개발 서버 + 빌드 |
| Tailwind CSS | 4.x | 스타일링 |
| React Router | v7 | 페이지 라우팅 |
| Zustand | 5.x | 전역 상태 관리 |
| Vitest | 3.x | 테스트 |

---

## 전체 강의 구조

### Part 1 — 기초 다지기

| 챕터 | 제목 | 핵심 개념 |
|------|------|-----------|
| 00 | [JavaScript 복습](/language/react-new/js-review) | 화살표 함수, 구조분해, 스프레드, map |
| 01 | [환경 구축 + 첫 React 앱](/language/react-new/setup) | Node.js, Vite, Tailwind, DevTools |
| 02 | [JSX와 컴포넌트](/language/react-new/jsx-components) | 함수 컴포넌트, JSX 문법, import/export |
| 03 | [스타일링](/language/react-new/styling) | Tailwind 클래스, 반응형, 상태 스타일 |
| 04 | [Props](/language/react-new/props) | 데이터 전달, 기본값, children |

### Part 2 — 동적 UI

| 챕터 | 제목 | 핵심 개념 |
|------|------|-----------|
| 05 | 리스트와 렌더링 | map, filter, key prop |
| 06 | useState | 상태 선언, 업데이트, 불변성 |
| 07 | 이벤트 처리 | onClick, onChange, form 제어 |
| 08 | 조건부 렌더링 | &&, 삼항 연산자, 상태별 UI |
| 09 | useEffect | 사이드 이펙트, fetch, 클린업 |

### Part 3 — 컴포넌트 설계

| 챕터 | 제목 | 핵심 개념 |
|------|------|-----------|
| 10 | 폼과 제어 컴포넌트 | 입력 관리, 유효성 검사 |
| 11 | 커스텀 훅 | 로직 재사용, useFetch |
| 12 | Context API | props drilling 해결 |
| 13 | 성능 최적화 | memo, useCallback, useMemo |

### Part 4 — 실전 앱

| 챕터 | 제목 | 핵심 개념 |
|------|------|-----------|
| 14 | React Router v7 | 페이지 이동, 동적 경로, 중첩 라우팅 |
| 15 | Zustand | 전역 상태, persist |
| 16 | API 연동 | REST API, 로딩/에러 처리 |
| 17 | 날씨 앱 — 설계 | 컴포넌트 분리, 데이터 흐름 |
| 18 | 날씨 앱 — 구현 | 전체 기능 완성 |

### Part 5 — 마무리

| 챕터 | 제목 | 핵심 개념 |
|------|------|-----------|
| 19 | 테스트 (Vitest) | 컴포넌트 테스트, 모킹 |
| 20 | 배포 (Vercel) | 빌드, CI/CD, 환경 변수 |

---

## 전체 흐름

```
JS 복습 (00)
    │
    ▼
환경 구축 (01) ──▶ JSX + 컴포넌트 (02)
                          │
                          ▼
              스타일링 (03) ──▶ Props (04)
                                    │
                                    ▼
                        리스트 (05) ──▶ useState (06)
                                              │
                                              ▼
                              이벤트 (07) ──▶ useEffect (09)
                                                    │
                                                    ▼
                                   커스텀 훅 (11) ──▶ Router (14)
                                                          │
                                                          ▼
                                              Zustand (15) ──▶ 날씨 앱 (17-18)
```

---

## 최종 프로젝트 — 날씨 앱

강의를 마치면 다음 기능을 갖춘 날씨 앱을 완성합니다.

- 도시 이름으로 현재 날씨 검색
- 5일 예보 표시
- 검색 기록 저장 (Zustand + localStorage)
- 모바일/데스크탑 반응형 레이아웃
- OpenWeatherMap API 연동

---

## AI 사용 규칙

AI 도구(ChatGPT, GitHub Copilot 등)를 활용할 때의 권장 원칙입니다.

| 허용 | 주의 |
|------|------|
| 에러 메시지 설명 요청 | 과제 전체를 대신 작성하게 하기 |
| 개념 질문 ("useEffect가 뭐야?") | 이해 없이 코드 복붙 |
| 코드 리뷰 요청 | 동작만 확인하고 왜 되는지 모르는 채 진행 |

> AI는 "빠른 구글링"으로 사용하세요. 이해가 목적입니다.

---

## 시작하기

**[→ 00장: JavaScript 복습부터 시작하기](/language/react-new/js-review)**

{% endraw %}
