---
title: TypeScript
layout: default
parent: Language
nav_order: 5
has_children: true
permalink: /language/typescript
---

{% raw %}

## 학습 목표

- TypeScript가 JavaScript와 어떻게 다른지 설명할 수 있다
- 타입 시스템이 왜 대규모 프로젝트에서 필수인지 이해할 수 있다

<a id="toc"></a>

## 진행 순서

1. [과정 소개](#intro) - 학습 대상, 사용 도구
2. [과정 구조](#structure) - 4 Parts, 16 chapters
3. [전체 흐름](#flow) - 학습 로드맵
4. [최종 프로젝트](#project) - JS 과정 앱을 TS로 리팩터링

---

# TypeScript — 비전공자를 위한 타입 안전한 JavaScript

<a id="intro"></a>

## 1️⃣ 과정 소개 [↑](#toc)

### 학습 대상

이 과정은 **JavaScript 과정(06_javascript) 이수자**를 위한 과정입니다.
JS 과정에서 배운 변수, 함수, 객체, 비동기 개념을 기반으로 TypeScript의 타입 시스템을 배웁니다.

> "JavaScript를 알고 있다면 TypeScript는 이미 절반은 배운 것입니다."
> TypeScript는 새로운 언어가 아니라 JavaScript에 타입이라는 안전망을 추가한 것입니다.

### 사용 도구

| 도구 | 용도 | 설치 방법 |
|------|------|-----------|
| TypeScript 5.x | 타입 시스템 제공 언어 | `npm install -g typescript` |
| tsx | TypeScript 즉시 실행기 | `npm install -g tsx` |
| VS Code | 코드 편집기 (TS 지원 최고) | [code.visualstudio.com](https://code.visualstudio.com) |
| TypeScript Playground | 브라우저 기반 실습 | [typescriptlang.org/play](https://www.typescriptlang.org/play) |

### 이 과정을 마치면

- JS 코드에 타입 주석을 추가하여 버그를 사전에 차단할 수 있다
- 인터페이스와 타입으로 객체 구조를 명확하게 정의할 수 있다
- 제네릭으로 재사용 가능한 타입 안전 함수를 작성할 수 있다
- JS 과정의 ToDo앱과 날씨앱을 TypeScript로 리팩터링할 수 있다

---

<a id="structure"></a>

## 2️⃣ 과정 구조 [↑](#toc)

### Part 1 — TypeScript 기초 (1~2일차)

| 장 | 제목 | 핵심 개념 |
|----|------|-----------|
| 01 | [TypeScript란?](/language/typescript/intro) | 왜 타입이 필요한가, JS와의 차이 |
| 02 | [개발 환경 설정](/language/typescript/setup) | Playground, tsx, tsconfig |
| 03 | [기본 타입과 타입 추론](/language/typescript/basic-types) | string, number, boolean, 추론 |
| 04 | [함수와 타입](/language/typescript/functions) | 매개변수, 반환 타입, void |

### Part 2 — 타입 구성 (3일차)

| 장 | 제목 | 핵심 개념 |
|----|------|-----------|
| 05 | [유니언 타입과 리터럴 타입](/language/typescript/union-literal) | `\|` 연산자, 리터럴 타입 |
| 06 | [타입 별칭과 인터페이스](/language/typescript/type-interface) | `type`, `interface`, `extends` |
| 07 | [타입 좁히기](/language/typescript/narrowing) | `typeof`, `in`, 타입 가드 |
| 08 | [제네릭 기초](/language/typescript/generics) | `<T>`, 재사용 가능한 타입 |

### Part 3 — 실전 패턴 (4일차)

| 장 | 제목 | 핵심 개념 |
|----|------|-----------|
| 09 | [클래스와 타입](/language/typescript/classes) | `class`, 접근 제어자 |
| 10 | [모듈과 타입](/language/typescript/modules) | `import`/`export`, 타입 선언 |
| 11 | [유틸리티 타입](/language/typescript/utility-types) | `Partial`, `Required`, `Pick` |
| 12 | [타입과 DOM](/language/typescript/dom) | `HTMLElement`, 이벤트 타입 |

### Part 4 — 프로젝트 (5일차)

| 장 | 제목 | 핵심 개념 |
|----|------|-----------|
| 13 | [tsconfig 심화](/language/typescript/tsconfig) | 프로젝트 설정 전체 |
| 14 | [에러 처리 패턴](/language/typescript/error-handling) | Result 타입, `unknown` |
| 15 | [프로젝트 1 — ToDo앱 리팩터링](/language/typescript/project-todo) | JS → TS 전환 실습 |
| 16 | [프로젝트 2 — 날씨앱 리팩터링](/language/typescript/project-weather) | API 타입, fetch 타입 |

---

<a id="flow"></a>

## 3️⃣ 전체 흐름 [↑](#toc)

```
JS 과정 완료
     ↓
[Part 1] 타입 기초
  01장 왜 TS인가? → 02장 환경 설정 → 03장 기본 타입 → 04장 함수 타입
     ↓
[Part 2] 타입 구성
  05장 유니언/리터럴 → 06장 interface/type → 07장 타입 좁히기 → 08장 제네릭
     ↓
[Part 3] 실전 패턴
  09장 클래스 → 10장 모듈 → 11장 유틸리티 → 12장 DOM 타입
     ↓
[Part 4] 프로젝트
  13장 tsconfig → 14장 에러 처리 → 15장 ToDo앱 TS화 → 16장 날씨앱 TS화
```

---

<a id="project"></a>

## 4️⃣ 최종 프로젝트 [↑](#toc)

JS 과정에서 만든 두 앱을 TypeScript로 다시 작성합니다.

### 프로젝트 1 — ToDo앱 TS 리팩터링 (JS 10장 → TS 15장)

- JS 10장의 ToDo앱 소스 기반
- `Todo` 인터페이스 정의
- DOM 요소 타입 명시
- 이벤트 핸들러 타입 추가

### 프로젝트 2 — 날씨앱 TS 리팩터링 (JS 14장 → TS 16장)

- JS 14장의 날씨앱 소스 기반
- OpenWeather API 응답 타입 정의
- `fetch` 반환 타입 처리
- 에러 처리 패턴 적용

> 두 프로젝트 모두 **기존 JS 코드를 보면서 TS로 변환**하는 과정을 단계별로 진행합니다.
> "JS로 작동하는 코드 → TS 타입 추가 → 타입 에러 수정" 순서로 리팩터링합니다.

---

### 실습 과제

**기본**: [TypeScript Playground](https://www.typescriptlang.org/play)에 접속해서 `let x = "안녕"` 입력 후 컴파일된 JS 출력을 확인해보세요.

**중급**: JS 과정의 `hello.js`를 `hello.ts`로 이름을 바꾸고 어떤 에러가 발생하는지 확인해보세요.

**심화**: TypeScript 공식 핸드북(typescriptlang.org/docs/handbook)에서 "The Basics" 섹션을 읽어보세요.

{% endraw %}
