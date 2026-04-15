---
title: React 커리큘럼 리뉴얼 분석 보고서
layout: default
parent: React
nav_order: 99
permalink: /language/react/renewal-report
---

{% raw %}

# React 커리큘럼 리뉴얼 — 다중 페르소나 비판적 분석 보고서
{: .no_toc }

**작성일**: 2026-04-11  
**분석 방법**: 다중 페르소나 비판적 사고 기법 (Multi-Persona Critical Thinking)  
**분석 대상**: `docs/02_language/03_0_react/` (21개 파일) + `docs/02_language/03_1_react/` (8개 파일)  
**데이터 기반**: React 19 공식 문서, 2024-2026 교육 연구, 주요 플랫폼 커리큘럼 분석
{: .fs-5 .fw-300 }

---

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 1. 분석 개요

### 1.1 현재 상태

기존 프로젝트에는 **두 개의 React 시리즈**가 존재한다:

| 구분 | Series A (`03_0_react`) | Series B (`03_1_react`) |
|------|------------------------|------------------------|
| 파일 수 | 21개 | 8개 |
| 주제 | React 기초~풀스택 | 쇼핑몰 프로젝트 |
| 빌드 도구 | **Vite** (현행) | **Create React App** (폐기됨) |
| 컴포넌트 패턴 | 함수형 + Hooks | 함수형 |
| 상태 관리 | Zustand | 없음 |
| 스타일링 | Tailwind CSS v4 | React Bootstrap |
| 심각한 문제 | 코드 버그 3건, 챕터 번호 불일치 | **ch5 중복, ch6-7 완전 오류 콘텐츠** |

### 1.2 리뉴얼 목표

- **비전공자 대상**으로 난이도와 설명 재설계
- **React 19** 최신 문법과 패턴 반영
- 강사가 **자연스럽게 이어서 설명**할 수 있는 흐름
- 더 **이해하기 쉬운 예제**와 비유
- 누락된 핵심 주제 보강

### 1.3 분석 페르소나

| 페르소나 | 역할 | 관점 |
|---------|------|------|
| **Dr. 교육** | 교육공학 연구자 | 학습 흐름, 인지 부하, 비유/은유 설계 |
| **최 프론트엔드** | 시니어 프론트엔드 개발자 (12년차) | React 19, 현업 패턴, 기술 정확성 |
| **박 비평가** | 교육 비평가 / 회의론자 | 기존 콘텐츠 문제점, 위험, 구조적 결함 |
| **한 설계자** | 커리큘럼 설계 전문가 | 구조화, 강의 흐름, 실행 가능한 설계 |

---

## 2. 핵심 자료 요약

### 2.1 React 19 주요 변경사항 (2024.12 릴리스)

#### 새로운 Hooks

| Hook | 용도 | 교육적 영향 |
|------|------|-----------|
| `useActionState` | 폼 제출의 pending/error/success 일괄 관리 | **가장 큰 커리큘럼 변경** — 기존 3개 useState → 1개로 대체 |
| `useOptimistic` | 서버 응답 전 UI 선반영 | 중급 주제 |
| `useFormStatus` | 자식 컴포넌트에서 부모 폼 상태 읽기 | prop drilling 해소 |
| `use` | Promise/Context를 렌더 중 읽기 | 조건부 호출 가능 (기존 Hook 규칙 예외) |

#### 폐기/제거된 항목

| 항목 | 상태 | 대체 |
|------|------|------|
| `forwardRef` | **폐기 예정** | ref를 props로 직접 전달 |
| `Context.Provider` | **폐기 예정** | `<Context value={}>` 직접 사용 |
| `propTypes` | **런타임에서 제거** | TypeScript 또는 JSDoc |
| `defaultProps` (함수 컴포넌트) | **제거** | ES6 기본 매개변수 |
| `Create React App` | **공식 폐기** (2025.02) | Vite, Next.js, React Router v7 |

### 2.2 교육 플랫폼 공통 커리큘럼 구조

Scrimba, freeCodeCamp, Udemy(Jonas), Meta/Coursera, Joy of React 등 주요 5개+ 플랫폼이 동일한 4단계 순서를 따른다:

```
1. 정적 페이지 (Static)  → JSX, 컴포넌트, 스타일링
2. 데이터 기반 (Dynamic) → Props, 리스트 렌더링, map()
3. 상태 관리 (Stateful)  → useState, 이벤트, 폼, 조건부 렌더링
4. 비동기 (Async)        → useEffect, 데이터 가져오기, API 연동
```

### 2.3 비전공자가 React 전에 반드시 알아야 할 JS 9가지

6개 이상의 독립적 소스에서 일관되게 확인된 필수 전제 지식:

1. 화살표 함수 (`=>`)
2. 배열 메서드: `.map()`, `.filter()`, `.find()`
3. 구조분해 할당 (객체/배열)
4. 스프레드 연산자 (`...`)
5. 템플릿 리터럴 (`` ` ` ``)
6. ES 모듈 (`import`/`export`)
7. `const`/`let` 변수 선언
8. Promise와 `async`/`await`
9. 조건문, 반복문, 함수 기초

> **"React가 어려운 게 아니라 JavaScript가 부족한 것이다"**  
> — Josh Comeau, Scrimba, freeCodeCamp, GeeksforGeeks, Noble Desktop 등에서 독립적으로 확인된 공통 견해

### 2.4 초보자 8대 실수 (연구 기반)

| 순위 | 실수 | 해결 |
|------|------|------|
| 1 | 비동기 상태 업데이트 오해 — `setState` 직후 값 읽기 | 함수형 업데이터 `prev => prev + 1` 먼저 가르치기 |
| 2 | 하나의 거대한 컴포넌트 | "하나의 컴포넌트 = 하나의 역할" 원칙 |
| 3 | Props vs State 혼동 | "함수 매개변수 vs 내부 변수" 비유 |
| 4 | 상태 직접 변경 (mutation) | 항상 새 객체/배열 생성: `[...items, newItem]` |
| 5 | key prop 오용 (index 사용) | 고유 ID 사용 의무화 |
| 6 | `class` vs `className` | JSX ≠ HTML 차이를 초반에 명시 |
| 7 | 프레젠테이션/로직 혼재 | 분리 패턴 조기 소개 |
| 8 | **JavaScript 기초 부족** | JS-for-React 브릿지 모듈 필수 |

### 2.5 효과적인 비유 모음

| 개념 | 비유 | 출처 |
|------|------|------|
| 컴포넌트 | **레고 블록** — 각각 독립적인 모양과 역할, 조합해서 복잡한 UI 구성 | 업계 표준 |
| Props | **함수의 매개변수** — 외부에서 전달받는 읽기 전용 데이터 | 기술적으로 정확 |
| State | **컴포넌트의 기억** — 쇼핑 카트가 담긴 물건을 "기억"하는 것 | React 공식 문서 |
| Prop Drilling | **와인잔 탑** — 1층에서 6층까지 와인을 전달하는 비효율 | 시각적 학습자에게 효과적 |
| useEffect | **"저녁 먹고 나서 설거지"** — 렌더(식사) 후에 부수 효과(설거지) 실행 | 일상 비유 |
| Context | **도서관 게시판** — 중규모 공유. 전국 방송(Zustand)과 구분 | 범위 비유 |
| Virtual DOM | **설계도 비교** — 이전 설계도와 새 설계도를 비교해서 바뀐 부분만 시공 | 건축 비유 |

---

## 3. 기존 커리큘럼 문제점 — 페르소나별 분석

### 3.1 Dr. 교육 — 교육공학 연구자의 분석

#### 핵심 주장: "흐름이 끊기고, 인지 부하가 급등하는 구간이 3곳 있다"

**문제 1: 챕터 번호 불일치 — 학습자 혼란**

네비게이션의 `nav_order`와 파일 내부 챕터 번호가 일치하지 않는다:

```
nav_order 9 (11_09_react.md) → 내부에 "9장, 10장, 11장" 3개 주제
nav_order 10 (11_10_react.md) → 내부에 "12장, 13장, 14장" 3개 주제
nav_order 12 (11_12_react.md) → 내부에 "16장, 17장" 2개 주제
```

학습자가 "9장을 열었는데 3개 주제가 나온다"면, 어디까지 읽었는지 추적이 불가능하다. 강사도 "오늘은 10장까지"라고 말하기 어렵다 — 어떤 10장인지 모호하다.

**문제 2: 난이도 절벽 — useRef에서 풀스택으로**

```
14장: useRef (개별 Hook 학습)
  ↓ 갑자기
15장: Express + MongoDB + Koyeb 배포 + axios CRUD + Netlify 배포

비전공자에게 이 점프는:
- Node.js 서버 프레임워크 (Express)
- 데이터베이스 (MongoDB)
- 클라우드 배포 (Koyeb)
- HTTP 클라이언트 (axios)
- 정적 호스팅 (Netlify)
→ 5개의 새로운 기술을 한 번에 도입
```

인지 부하 이론(Cognitive Load Theory)에 따르면, 한 수업에서 새로운 개념은 **최대 2-3개**가 한계다. 5개 동시 도입은 비전공자에게 **학습 포기 트리거**가 된다.

**문제 3: "왜"가 없는 코드 나열**

대부분의 챕터가 "이렇게 작성합니다 → 실행하면 이렇게 됩니다"의 코드 나열 구조다.

```
현재 패턴:
  코드 블록 → 결과 설명 → 다음 코드 블록 → 결과 설명

효과적 패턴:
  문제 제시 ("이것을 하고 싶은데 안 됩니다") 
  → 왜 안 되는지 설명
  → 해결 코드 제시
  → "이것이 바로 useState입니다"
```

**useContext 챕터가 대표적 사례**: prop drilling이 왜 고통스러운지 먼저 경험시키지 않고, 바로 Context 코드를 보여준다. 학습자는 "이걸 왜 쓰는지" 이해하지 못한 채 문법만 따라치게 된다.

#### 평가

| 항목 | 판정 |
|------|------|
| 전체 흐름 | **구조적 결함** — 번호 불일치 + 난이도 절벽 |
| 비전공자 적합도 | **부적합** — "왜"가 없는 코드 나열, 비유/은유 부재 |
| 강사 사용성 | **불편** — 한 파일에 3개 주제가 혼재되어 강의 단위 구분 불가 |

---

### 3.2 최 프론트엔드 — 시니어 개발자의 분석

#### 핵심 주장: "2026년 기준으로 폐기된 패턴이 3곳, 코드 버그가 3건 있다"

**폐기된 패턴 1: PropTypes (ch4)**

```javascript
// 현재 교재 — 폐기된 패턴
import PropTypes from 'prop-types';

Student.propTypes = {
  name: PropTypes.string,
  age: PropTypes.number
};
```

React 19에서 `propTypes`는 **런타임에서 제거**되었다. 2026년 현업에서 타입 검증은 **TypeScript**가 표준이다.

**폐기된 패턴 2: Create React App (Series B 전체)**

```bash
# Series B — 2025년 2월 공식 폐기
npx create-react-app my-app
```

React 팀이 공식적으로 CRA 사용을 중단하고 Vite/Next.js/React Router v7를 권장한다.

**폐기된 패턴 3: Context.Provider (ch13)**

```jsx
// 현재 교재
<UserContext.Provider value={user}>

// React 19 권장
<UserContext value={user}>
```

`Context.Provider`는 React 19에서 **폐기 예정**이다.

**코드 버그 1: `class` vs `className` (ch1, `11_01_react.md`)**

```jsx
// 현재 교재 — 버그
<div class="card">

// 올바른 JSX
<div className="card">
```

React 19에서는 `class`도 동작하지만 React 18에서는 경고가 발생하며, JSX에서는 `className`이 표준이다.

**코드 버그 2: Fragment 누락 (ch7, `11_07_react.md`)**

```jsx
// 현재 교재 — 컴파일 에러
function ProfilePicture() {
  return (
    <img src="..." />
    <button>Change</button>  // 형제 요소 — Fragment 필요
  );
}
```

**코드 버그 3: document.getElementById 안티패턴 (ch10, `11_10_react.md`)**

```javascript
// 현재 교재 — React 패러다임 위반
const input = document.getElementById("foodInput");
const food = input.value;
```

React에서는 DOM 직접 접근 대신 **제어 컴포넌트(controlled component)** 또는 `useRef`를 사용해야 한다. 앞 챕터에서 가르친 내용과 모순된다.

**누락된 핵심 주제 (현업 기준)**

| 주제 | 중요도 | 현재 상태 |
|------|--------|----------|
| Custom Hooks | **필수** | 완전 부재 |
| useMemo / useCallback | 높음 | 완전 부재 |
| useReducer | 높음 | 완전 부재 |
| Error Boundary | 높음 | 완전 부재 |
| 테스팅 (Vitest + Testing Library) | 높음 | 완전 부재 |
| React DevTools 사용법 | 높음 | 완전 부재 |
| TypeScript with React | **필수** (현업 표준) | 완전 부재 |
| React 19 신규 Hooks | 중간 | 완전 부재 |
| 환경 변수 (.env) | 높음 | 완전 부재 |
| 제어/비제어 컴포넌트 개념 | 높음 | 시연되지만 명명/설명 없음 |

#### 평가

| 항목 | 판정 |
|------|------|
| 기술 정확성 | **수정 필요** — 버그 3건 + 폐기 패턴 3건 |
| 현업 적합도 | **부분 적합** — Vite+Zustand은 현행이지만 핵심 주제 다수 누락 |
| React 19 반영도 | **미반영** — 파일 하나에 "React 19" 언급만 있을 뿐 신규 API 교육 없음 |

---

### 3.3 박 비평가 — 교육 비평가의 분석

#### 핵심 주장: "Series B는 즉시 폐기하거나 전면 재작성해야 한다"

**Series B의 치명적 문제**

```
05_react.md (장바구니):
  → 04_react.md (라우터)의 완전 복사본. "장바구니" 내용 없음.

06_react.md (검색 및 정렬):
  → React 내용이 아님. "SuperCodex + Speckit CRM 전략 메모"가 들어있음.

07_react.md (게시판):
  → 06_react.md의 복사본. 역시 React 내용 아님.
```

**8개 파일 중 3개(37.5%)가 완전히 잘못된 콘텐츠**다. 이는 교육 자료의 신뢰도를 근본적으로 훼손한다. 학생이 이 파일을 열면:
- 이전 챕터와 중복된 내용에 혼란
- AI 도구 전략 메모를 React 강의 내용으로 착각
- **교재 전체에 대한 신뢰 상실**

**Series A와 B의 관계 미정의**

두 시리즈의 관계가 어디에도 설명되지 않는다:
- 순차적으로 학습해야 하는가?
- 독립적인 과정인가?
- 같은 대상을 위한 것인가?

학습자가 두 시리즈를 모두 발견하면 "어느 것을 따라야 하지?"라는 결정 마비가 발생한다.

**JS 전제 지식 모순**

| 챕터 | JS 수준 가정 |
|------|-------------|
| ch6 (데이터 정렬) | `Array.sort()`를 처음부터 가르침 → **완전 초보자** 가정 |
| ch15 (axios) | Express, MongoDB, 클라우드 배포를 안다고 가정 → **경험자** 가정 |
| ch18 (Supabase Auth) | OAuth 개념, GitHub 계정을 안다고 가정 → **중급자** 가정 |

한 과정 내에서 대상 수준이 **초보자→중급자→경험자**로 무작위 변동한다.

**보안 문제**

- ch18 (`11_18_react.md`): Supabase URL이 클라이언트 코드에 하드코딩. `.env` 파일 사용법 미교육.
- ch15 (`11_15_react.md`): MongoDB 연결 문자열이 주석에 노출.
- 전체적으로 환경 변수 개념이 교육되지 않음.

**연습 문제 완전 부재**

21개 파일 중 **단 하나도** 학습자가 독립적으로 풀어볼 연습 문제가 없다. 모든 챕터가 "강사가 보여주는 코드를 따라치기" 구조다. 비전공자에게 이 패턴은:
- 수동적 학습 → 기억 정착률 20% 이하 (Edgar Dale의 학습 피라미드)
- "강의 중에는 이해했는데 혼자 하면 못 한다" 현상 유발

#### 평가

| 항목 | 판정 |
|------|------|
| Series B | **즉시 폐기 또는 전면 재작성** — 37.5%가 오류 콘텐츠 |
| Series A | **대폭 보강 필요** — 코드 버그 수정, 설명 보강, 연습 문제 추가 |
| 비전공자 적합도 | **부적합** — 비유 부재, 연습 부재, 난이도 무작위 변동 |

---

### 3.4 한 설계자 — 커리큘럼 설계 전문가의 분석

#### 핵심 주장: "4단계 순서를 따르고, 1주제 1파일로 재구성해야 한다"

앞선 세 전문가의 분석과 교육 플랫폼 조사 결과를 종합하여, 리뉴얼 커리큘럼을 제안한다.

**설계 원칙**

1. **정적→동적→상태→비동기** 4단계 순서 (업계 검증된 공통 구조)
2. **1주제 1파일** — 강사가 "오늘은 5장까지"라고 말할 수 있어야 한다
3. **문제→고통→해결** 패턴 — "왜 이게 필요한지"를 먼저 경험
4. **매 챕터 연습 문제** — 기본/도전 2단계
5. **비유 선행** — 코드 전에 일상 비유로 개념 설명
6. **React 19 기준** — 폐기된 API 제거, 신규 Hook 포함

**리뉴얼 커리큘럼 구조 (20장)**

```
Part 0: 준비 (2장)
├── 00. React를 위한 JavaScript 복습
└── 01. 환경 구축 + 첫 React 앱

Part 1: 정적 React (3장)
├── 02. JSX와 컴포넌트
├── 03. 스타일링 (Tailwind CSS)
└── 04. Props — 컴포넌트 간 데이터 전달

Part 2: 동적 React (3장)
├── 05. 리스트 렌더링과 key
├── 06. 조건부 렌더링
└── 07. 이벤트 처리

Part 3: 상태 관리 (5장)
├── 08. useState — 컴포넌트의 기억
├── 09. 폼과 입력 처리
├── 10. 객체/배열 상태 관리
├── 11. 컴포넌트 간 상태 공유 (Lifting State)
└── 12. 미니 프로젝트: ToDo 앱

Part 4: 심화 Hooks (4장)
├── 13. useEffect — 부수 효과
├── 14. useRef — DOM 접근과 값 보존
├── 15. useContext — 전역 상태
└── 16. Custom Hooks — 로직 재사용

Part 5: 실전 (3장)
├── 17. React Router — 페이지 이동
├── 18. 데이터 가져오기 (fetch + API)
├── 19. Zustand — 상태 관리 라이브러리
└── 20. 통합 프로젝트: 날씨 앱
```

#### 상세 설계 — 각 Part

**Part 0: 준비 (2장)**

| 장 | 내용 | 비전공자 포인트 |
|----|------|---------------|
| 00 | JS 복습: 화살표 함수, 구조분해, 스프레드, map/filter, 모듈, async/await | 9가지 필수 전제 지식을 30분씩 집중 복습 |
| 01 | Node.js 설치, `npm create vite@latest`, 프로젝트 구조 설명, 첫 컴포넌트 실행 | React DevTools 첫 날부터 설치 |

**Part 1: 정적 React (3장) — "화면에 보여주기"**

| 장 | 핵심 비유 | 기존 대비 변화 |
|----|----------|-------------|
| 02 | "컴포넌트 = 레고 블록" | JSX vs HTML 차이를 명시적으로 표로 비교 |
| 03 | "Tailwind = 옷에 이름표 붙이기" | 기존 3가지 CSS 방식 → Tailwind 단일 표준 |
| 04 | "Props = 택배 — 보내는 사람이 내용을 결정" | PropTypes 제거, ES6 기본 매개변수로 대체 |

**Part 2: 동적 React (3장) — "데이터에 따라 바뀌기"**

| 장 | 핵심 비유 | 기존 대비 변화 |
|----|----------|-------------|
| 05 | "map = 출석부 한 명씩 부르기" | key prop 안티패턴(index) 명시적 경고 |
| 06 | "조건부 렌더링 = 날씨에 따라 옷 고르기" | 삼항, &&, 조기 return 3가지 패턴 정리 |
| 07 | "이벤트 = 초인종 — 누르면 반응" | 기존 ch7의 Fragment 버그 수정 |

**Part 3: 상태 관리 (5장) — "기억하고 바꾸기"**

| 장 | 핵심 비유 | 기존 대비 변화 |
|----|----------|-------------|
| 08 | **"State = 컴포넌트의 기억"** (React 공식) | 비동기 setState를 첫날부터 설명 |
| 09 | "제어 컴포넌트 = 리모컨으로 조종" | document.getElementById 안티패턴 제거 |
| 10 | "불변성 = 원본 보존 복사" | 스프레드로 객체/배열 불변 업데이트 |
| 11 | **"Lifting State = 형제에게 메모 전달 시 부모 경유"** | **신규 추가** — 가장 중요한 React 멘탈 모델 |
| 12 | ToDo 앱 프로젝트 | CRUD + 필터 + 정렬 종합 |

**Part 4: 심화 Hooks (4장) — "더 강력한 도구들"**

| 장 | 핵심 비유 | 기존 대비 변화 |
|----|----------|-------------|
| 13 | "useEffect = 저녁 먹고 설거지" | 의존성 배열 시각적 다이어그램 추가 |
| 14 | "useRef = 메모장 — 바꿔도 리렌더 안 됨" | state vs ref vs 변수 비교표 유지 (좋은 기존 콘텐츠) |
| 15 | "Context = 도서관 게시판" | `<Context value={}>` React 19 문법으로 업데이트 |
| 16 | **Custom Hooks** | **완전 신규** — useFetch, useLocalStorage 등 |

**Part 5: 실전 (4장) — "진짜 앱 만들기"**

| 장 | 내용 | 기존 대비 변화 |
|----|------|-------------|
| 17 | React Router v7 (SPA 모드) | v6 → v7 업데이트, 단일 패키지 `react-router` |
| 18 | fetch API + JSONPlaceholder → 로딩/에러 상태 | Express/MongoDB 풀스택 제거 → 프론트엔드 집중 |
| 19 | Zustand | 기존 ch17 유지 (좋은 콘텐츠) |
| 20 | 날씨 앱 통합 프로젝트 | API 연동 + Router + Zustand 종합 |

---

## 4. 쟁점별 페르소나 간 교차 분석

### 4.1 "Series B를 어떻게 처리하는가?"

| 페르소나 | 입장 | 근거 |
|---------|------|------|
| Dr. 교육 | 폐기 후 Series A에 프로젝트 챕터로 통합 | 두 시리즈 병존은 학습자 혼란 |
| 최 프론트엔드 | 폐기 — CRA 기반이라 전면 재작성 필요 | CRA 공식 폐기 (2025.02) |
| 박 비평가 | **즉시 폐기** — 37.5%가 오류 콘텐츠 | 교재 신뢰도 훼손 |
| 한 설계자 | 쇼핑몰 아이디어만 Series A의 고급 프로젝트로 재활용 | 좋은 프로젝트 아이디어를 버리지 않음 |

**합의**: Series B는 **폐기**하고, 쇼핑몰 프로젝트 아이디어는 리뉴얼 과정의 선택적 프로젝트로 재활용한다.

### 4.2 "PropTypes를 TypeScript로 대체하는가?"

| 페르소나 | 입장 | 근거 |
|---------|------|------|
| Dr. 교육 | Phase 1에서는 JavaScript만, 고급 과정에서 TypeScript | 비전공자에게 JS+React+TS 동시 학습은 과부하 |
| 최 프론트엔드 | TypeScript 필수 — 현업 표준 | 2026년 신규 React 프로젝트의 90%+ |
| 박 비평가 | 초급 과정에서 TS는 좌절감만 줌 | 비전공자 이탈 위험 |
| 한 설계자 | ES6 기본 매개변수로 대체, TS는 별도 장(선택) | 절충 |

**합의**: 본 과정에서 PropTypes 제거, ES6 기본 매개변수 사용. TypeScript는 **별도 후속 과정**으로 안내.

### 4.3 "풀스택(Express+MongoDB)을 포함하는가?"

| 페르소나 | 입장 | 근거 |
|---------|------|------|
| Dr. 교육 | 제외 — 난이도 절벽의 원인 | 인지 부하 급등 |
| 최 프론트엔드 | 별도 과정으로 분리 | 프론트엔드와 백엔드는 다른 역량 |
| 박 비평가 | 제외 — 비전공자에게 DB+서버+배포 동시 학습 불가 | 학습 포기 트리거 |
| 한 설계자 | **무료 API(JSONPlaceholder, OpenWeatherMap)로 대체** | fetch만 가르치고 백엔드는 분리 |

**합의**: 풀스택 내용 **제외**. 공개 API로 데이터 가져오기만 가르친다. 풀스택은 별도 과정(기존 `11_react_fastapi.md` 활용).

### 4.4 "React 19 신규 Hooks를 가르치는가?"

| 페르소나 | 입장 | 근거 |
|---------|------|------|
| Dr. 교육 | 핵심 Hooks 후에 보너스 장으로 | 기초가 먼저 |
| 최 프론트엔드 | `useActionState`는 필수 — 폼 처리 패러다임 변화 | 가장 큰 커리큘럼 변경 |
| 박 비평가 | 초급 과정에서는 코어 Hooks만 | 혼란 방지 |
| 한 설계자 | 폼 챕터(09장)에서 기존 방식 먼저 보여주고 `useActionState` 소개 | "이전 방식 → 새 방식" 대비 |

**합의**: 코어 Hooks를 먼저 가르치되, 폼 처리 챕터에서 `useActionState`를 **"이렇게 더 간단해졌습니다"**로 소개한다.

### 4.5 "강의 흐름을 어떻게 자연스럽게 만드는가?"

한 설계자의 **"브릿지 문장"** 설계:

각 챕터의 마지막에 **다음 챕터로의 자연스러운 연결 문장**을 배치한다:

```
ch02 끝: "컴포넌트를 만들었지만, 아직 밋밋합니다. 
         다음 장에서 Tailwind로 예쁘게 꾸며봅시다."

ch04 끝: "Props로 데이터를 전달했지만, 배열 데이터를 
         하나씩 전달하면 힘들겠죠? 다음 장에서 map()으로 해결합니다."

ch07 끝: "버튼을 클릭하면 alert이 뜹니다. 하지만 화면 자체가 
         바뀌면 더 좋겠죠? 다음 장에서 useState를 배우면 가능합니다."

ch10 끝: "상태를 잘 관리하게 되었습니다. 그런데 두 컴포넌트가 
         같은 데이터를 공유하려면? 다음 장의 'Lifting State'가 답입니다."

ch12 끝: "ToDo 앱을 완성했습니다! 하지만 새로고침하면 데이터가 
         사라집니다. 다음 장에서 useEffect로 데이터를 저장하는 법을 배웁니다."
```

이 패턴은 **"고통 → 해결"** 구조를 챕터 간에도 적용한 것이다. 강사가 "자, 이렇게 하면 불편하죠? 다음 시간에 해결합니다"로 마무리하면 학생의 **호기심이 유지**된다.

---

## 5. 비전공자를 위한 핵심 설계 원칙

### 5.1 매 챕터 구조 표준

```
┌─ 이 장의 목표 (학습 목표 2-3개)
├─ 비유로 시작 (일상 비유 → 개념 설명)
├─ 문제 제시 ("이것을 하고 싶은데...")
├─ 해결 코드 (단계별, 주석 풍부)
├─ React DevTools로 확인 (상태/props 시각화)
├─ 실습 과제 (기본 / 도전)
└─ 정리 + 다음 장 브릿지
```

### 5.2 "보여주고 → 설명하기" 순서

비전공자에게는 **결과를 먼저 보여주고** 코드를 설명하는 것이 효과적이다:

```
기존 (비효과적):
  "useState는 상태를 관리하는 Hook입니다. 이렇게 작성합니다..."
  → 코드 → 실행 → 결과 확인

리뉴얼 (효과적):
  "버튼을 누르면 숫자가 올라가는 카운터를 봅시다" (데모)
  → "이게 어떻게 작동하는 걸까요?"
  → 코드 한 줄씩 설명
  → "이 마법을 가능하게 하는 것이 useState입니다"
```

### 5.3 React DevTools 활용 — "보이지 않는 것을 보이게"

React의 가장 큰 학습 장벽은 **상태와 props가 보이지 않는다**는 것이다. React DevTools를 첫 날부터 설치하고 매 챕터에서 활용한다:

```
- ch04 (Props): DevTools에서 props 값 확인
- ch08 (useState): DevTools에서 상태 변화 실시간 관찰
- ch13 (useEffect): DevTools에서 리렌더링 횟수 확인
- ch15 (useContext): DevTools에서 Context 값 추적
```

---

## 6. 기존 콘텐츠 재활용 판정

### 6.1 유지할 것 (좋은 기존 콘텐츠)

| 파일 | 내용 | 판정 |
|------|------|------|
| `11_08_react.md` | useState 카운터 예제 | **유지** — 명확한 예제 |
| `11_14_react.md` | state vs ref vs 변수 비교표 | **유지** — 훌륭한 교육 자료 |
| `11_17_react.md` | Zustand props vs store 비교 | **유지** — 효과적인 before/after |
| `11_11_react.md` | ToDo 앱 | **유지 + 보강** — 연습 문제 추가 |
| `11_12_react.md` | useEffect + 디지털 시계 | **유지 + 보강** — 의존성 배열 설명 강화 |

### 6.2 수정할 것

| 파일 | 문제 | 수정 내용 |
|------|------|----------|
| `11_01_react.md` | `class=` 버그 | `className=`으로 수정 |
| `11_04_react.md` | PropTypes | ES6 기본 매개변수로 대체 |
| `11_07_react.md` | Fragment 누락 | `<>...</>` 추가 |
| `11_10_react.md` | document.getElementById | 제어 컴포넌트로 대체 |
| `11_13_react.md` | Context.Provider | `<Context value={}>` 로 업데이트 |
| `11_09_react.md` | 3개 주제 혼재 | 1주제 1파일로 분리 |
| `11_16_react.md` | React Router v6 | v7로 업데이트 |

### 6.3 제거/대체할 것

| 파일 | 이유 | 대체 |
|------|------|------|
| `11_15_react.md` (Express+MongoDB) | 난이도 절벽, 프론트엔드 과정과 무관 | fetch + 공개 API |
| `11_18_react.md` (Supabase Auth) | 고급 주제, 보안 이슈 | 선택적 보너스 또는 별도 과정 |
| Series B 전체 | CRA 기반 + 오류 콘텐츠 | 폐기 |

---

## 7. 종합 권고안

### 7.1 리뉴얼 로드맵

```
[즉시] 긴급 수정 (1일)
  ├── 코드 버그 3건 수정
  ├── Series B ch5-7 삭제 또는 경고 표시
  └── PropTypes → ES6 기본 매개변수

[Phase 1] 구조 재설계 (1주)
  ├── 1주제 1파일로 분리
  ├── 챕터 번호 정규화
  ├── 매 챕터 연습 문제 추가
  └── 비유/은유 + 브릿지 문장 삽입

[Phase 2] 콘텐츠 보강 (2주)
  ├── Part 0 신설 (JS 복습)
  ├── Custom Hooks 챕터 신설
  ├── Lifting State 챕터 신설
  ├── React 19 문법 업데이트
  └── React DevTools 활용 가이드 추가

[Phase 3] 실전 파트 재설계 (1주)
  ├── 풀스택 → fetch + 공개 API
  ├── React Router v6 → v7
  ├── 날씨 앱 통합 프로젝트
  └── 쇼핑몰 프로젝트 (선택적 보너스)
```

### 7.2 확정된 결정사항

| 항목 | 결정 | 근거 |
|------|------|------|
| 대상 | **비전공자** | 사용자 확정 |
| React 버전 | **React 19** | 최신 안정 버전 |
| 빌드 도구 | **Vite** | 기존 Series A 유지, React 공식 권장 |
| 스타일링 | **Tailwind CSS** | 기존 Series A 유지, 비전공자에게 가장 효율적 |
| 상태 관리 | **Context → Zustand** 순서 | 점진적 복잡성 |
| 라우팅 | **React Router v7** | 최신 버전 |
| PropTypes | **제거** | React 19에서 런타임 제거됨 |
| TypeScript | **별도 후속 과정** | 비전공자 인지 부하 고려 |
| 풀스택 | **제거** (fetch + 공개 API로 대체) | 난이도 절벽 해소 |
| Series B | **폐기** | CRA 폐기 + 오류 콘텐츠 |
| 연습 문제 | **매 챕터 필수** | 능동적 학습 필수 |
| React DevTools | **1장부터 설치** | "보이지 않는 것을 보이게" |

### 7.3 리뉴얼 전후 비교

| 항목 | 현재 | 리뉴얼 후 |
|------|------|----------|
| 파일 수 | 21개 (+ Series B 8개) | **20개** (단일 시리즈) |
| 1파일 주제 수 | 1~3개 (불규칙) | **1개** (일관) |
| JS 전제 학습 | 없음 | **Part 0: JS 복습 2장** |
| 비유/은유 | 없음 | **매 챕터 1개 이상** |
| 연습 문제 | 없음 | **매 챕터 기본+도전** |
| 브릿지 문장 | 없음 | **매 챕터 마지막** |
| React DevTools | 미사용 | **1장부터 활용** |
| PropTypes | 교육 | **제거** (ES6 기본값) |
| CRA | Series B 전체 | **완전 제거** |
| 풀스택 | Express+MongoDB | **fetch + 공개 API** |
| Custom Hooks | 없음 | **1개 챕터 신설** |
| Lifting State | 없음 | **1개 챕터 신설** |
| React 19 | 미반영 | **전면 반영** |

---

## 8. 결론 — 페르소나 간 최종 합의

### 4인이 동의하는 것

1. **Series B는 폐기**하고 Series A를 리뉴얼하는 것이 유일한 합리적 선택이다
2. **코드 버그 3건과 폐기 패턴 3건**은 즉시 수정해야 한다
3. **1주제 1파일** 구조가 강사와 학습자 모두에게 필수적이다
4. **비유 선행 + 문제→해결 패턴**이 비전공자에게 가장 효과적이다
5. **연습 문제**가 없는 코딩 교육은 수동적 학습에 머무른다
6. **정적→동적→상태→비동기** 4단계 순서는 업계 검증된 표준이다
7. **React DevTools**를 첫 날부터 사용해야 한다
8. **풀스택 내용은 분리**하고 프론트엔드에 집중해야 한다
9. **챕터 간 브릿지 문장**이 강사의 자연스러운 전환을 돕는다

### 4인이 동의하지 않는 것

| 쟁점 | 범위 |
|------|------|
| TypeScript 포함 여부 | 최 프론트엔드(필수) vs 나머지 3인(별도 과정) |
| React 19 신규 Hook 깊이 | 최 프론트엔드(상세히) vs Dr. 교육(소개만) |
| 쇼핑몰 프로젝트 포함 | 한 설계자(보너스로 포함) vs 박 비평가(불필요) |

---

## 부록: 참고 문헌

### React 공식 문서
- [React v19 Release](https://react.dev/blog/2024/12/05/react-19)
- [React 19 Upgrade Guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide)
- [Sunsetting Create React App](https://react.dev/blog/2025/02/14/sunsetting-create-react-app)
- [Built-in React Hooks](https://react.dev/reference/react/hooks)
- [State: A Component's Memory](https://react.dev/learn/state-a-components-memory)

### 교육 플랫폼 및 커리큘럼
- Scrimba — Bob Ziroll React Course (11시간 무료 / 81.6시간 Career Path)
- freeCodeCamp — Full Stack Curriculum 2025 Update (브라우저 기반 React 학습)
- Joy of React — Josh W. Comeau (멀티모달 학습: 비디오 + 인터랙티브 + 미니게임)
- Meta / Coursera — React Professional Certificate

### 교육 연구 및 전문가 의견
- Josh W. Comeau — [Common Beginner Mistakes with React](https://www.joshwcomeau.com/react/common-beginner-mistakes/)
- Josh W. Comeau — [Making Sense of React Server Components](https://www.joshwcomeau.com/react/server-components/)
- freeCodeCamp — [Hard Parts of React](https://www.freecodecamp.org/news/hard-parts-of-react/)
- LogRocket — [10 Mistakes React Developers Make](https://blog.logrocket.com/10-mistakes-react-developers-make/)

### 기술 동향
- React Router v7 — [LogRocket Guide](https://blog.logrocket.com/react-router-v7-guide/)
- Vite vs Next.js 2025 — [Strapi Comparison](https://strapi.io/blog/vite-vs-nextjs-2025-developer-framework-comparison)
- State Management 2025 — [DEV Community](https://dev.to/hijazi313/state-management-in-2025-when-to-use-context-redux-zustand-or-jotai-2d2k)
- AI-Assisted Coding Study — [arXiv 2025](https://arxiv.org/html/2511.04427v2)

---

*본 보고서는 다중 페르소나 비판적 사고 기법(Multi-Persona Critical Thinking)을 적용하여,*  
*교육공학자, 시니어 개발자, 교육 비평가, 커리큘럼 설계자 4가지 관점에서 독립 분석한 후 종합하였습니다.*

{% endraw %}
