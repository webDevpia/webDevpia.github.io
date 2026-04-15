---
title: 01. TypeScript란?
layout: default
grand_parent: Language
parent: TypeScript
nav_order: 1
permalink: /language/typescript/intro
---

{% raw %}

## 학습 목표

- JavaScript의 동적 타입이 만들어내는 버그 3가지를 설명할 수 있다
- TypeScript가 JavaScript의 상위 집합(Superset)임을 이해할 수 있다
- 컴파일 타임 에러와 런타임 에러의 차이를 설명할 수 있다

<a id="toc"></a>

## 진행 순서

1. [JavaScript의 자유, 그리고 대가](#part1) - 동적 타입의 함정
2. [TypeScript = JavaScript + 타입](#part2) - TS의 본질
3. [상자 비유 확장](#part3) - JS 02장 상자에 라벨 추가
4. [TypeScript가 잡아주는 버그들](#part4) - Before/After 비교
5. [TypeScript의 역사와 현재](#part5) - Microsoft, 2012, 현재 표준
6. [정리](#part6) - 핵심 개념 요약

---

# 01장. TypeScript란? — 왜 타입이 필요한가

<a id="part1"></a>

## 1️⃣ JavaScript의 자유, 그리고 대가 [↑](#toc)

JavaScript는 세상에서 가장 유연한 언어 중 하나입니다. 변수에 어떤 값이든 넣을 수 있고, 함수에 어떤 인자든 전달할 수 있습니다. 이 자유로움은 초보자에게 편리하지만, 프로젝트가 커질수록 **예상치 못한 버그**로 돌아옵니다.

> JavaScript에서는 실수를 해도 코드를 실행해봐야 알 수 있습니다.
> 운전 중에 처음 알게 되는 자동차 결함 같은 것입니다.

### 버그 1 — 잘못된 인자 타입

```javascript
// JS: 함수가 숫자를 기대하지만, 문자열을 전달해도 에러가 없다
function calculateTax(price) {
  return price * 0.1; // 부가세 10% 계산
}

console.log(calculateTax(10000));  // 1000 (정상)
console.log(calculateTax("만원")); // NaN — 실행해봐야 알 수 있음! ❌
```

실행 결과:
```
1000
NaN
```

`calculateTax("만원")`을 호출하는 실수를 코드 작성 시점에 알 수 없습니다. 실행해봐야, 그것도 해당 경로가 실행되어야만 발견할 수 있습니다.

---

### 버그 2 — 오타 난 속성 접근

```javascript
// JS: 존재하지 않는 속성에 접근해도 에러가 없다
const user = {
  name: "김철수",
  email: "kim@example.com"
};

// 오타: "email" → "eamil"
console.log(user.name);   // "김철수"
console.log(user.eamil);  // undefined — 오타인지 실수인지 모름! ❌
```

실행 결과:
```
김철수
undefined
```

`undefined`가 출력될 때 오타 때문인지, 실제로 없는 속성인지 바로 알기 어렵습니다. 이 `undefined`가 이메일 발송 로직으로 흘러가면 더 심각한 버그를 만듭니다.

---

### 버그 3 — null 접근으로 인한 충돌

```javascript
// JS: null인 값의 속성에 접근하면 런타임 에러
function getUserName(user) {
  return user.name.toUpperCase(); // user가 null이면?
}

const activeUser = { name: "이영희" };
const deletedUser = null;

console.log(getUserName(activeUser));  // "이영희" (정상)
console.log(getUserName(deletedUser)); // ❌ TypeError: Cannot read properties of null
```

실행 결과:
```
이영희
TypeError: Cannot read properties of null (reading 'name')
    at getUserName ...
```

이 에러는 웹사이트가 운영 중에 터지는 **런타임 에러**입니다. 사용자가 오류 화면을 보게 됩니다.

---

**이 세 가지 버그의 공통점:** 코드를 **실행해봐야** 알 수 있다는 것입니다. TypeScript는 이 문제를 코드를 **작성하는 시점**에 잡아줍니다.

---

<a id="part2"></a>

## 2️⃣ TypeScript = JavaScript + 타입 [↑](#toc)

### TypeScript는 새로운 언어가 아닙니다

> TypeScript는 JavaScript에 **타입 레이어를 얹은 것**입니다.
> 모든 JavaScript 코드는 그대로 TypeScript 코드입니다.
> TypeScript는 `.ts` 파일을 컴파일하면 결국 `.js` 파일이 됩니다.

```
TypeScript 코드 (.ts)
        ↓
   tsc (컴파일러)
        ↓
JavaScript 코드 (.js)
        ↓
 브라우저/Node.js 실행
```

브라우저는 TypeScript를 직접 이해하지 못합니다. TypeScript는 개발하는 동안 타입을 검사하고, 배포할 때는 순수 JavaScript로 변환됩니다.

---

### TypeScript Playground에서 직접 확인

[TypeScript Playground](https://www.typescriptlang.org/play)는 브라우저에서 TypeScript를 바로 실행할 수 있는 공식 도구입니다.

왼쪽에 TypeScript 코드를 입력하면, 오른쪽에서 컴파일된 JavaScript를 확인할 수 있습니다.

```typescript
// TypeScript 코드 (왼쪽)
function greet(name: string): string {
  return `안녕하세요, ${name}님!`;
}

console.log(greet("홍길동"));
```

컴파일된 JavaScript (오른쪽):
```javascript
// JavaScript 코드 (타입 주석이 모두 제거됨)
function greet(name) {
  return `안녕하세요, ${name}님!`;
}

console.log(greet("홍길동"));
```

TypeScript의 `: string` 같은 타입 주석은 컴파일 과정에서 완전히 제거됩니다. 브라우저에는 순수 JavaScript만 전달됩니다.

---

### 컴파일 타임 vs 런타임

TypeScript의 핵심 가치는 **컴파일 타임**에 에러를 잡는 것입니다.

| | 컴파일 타임 에러 (TS) | 런타임 에러 (JS) |
|---|---|---|
| **발생 시점** | 코드 저장 즉시 | 코드 실행 중 |
| **발견 방법** | VS Code 빨간 줄 | 콘솔 에러, 사용자 신고 |
| **영향** | 개발자만 영향 | 실제 사용자도 영향 |
| **수정 난이도** | 즉시 수정 가능 | 재현 → 디버그 → 수정 |

> 컴파일 타임 에러는 **"출발 전 지도 확인"**, 런타임 에러는 **"길 잃고 나서야 지도 꺼내기"** 입니다.

---

<a id="part3"></a>

## 3️⃣ 상자 비유 확장 [↑](#toc)

JS 02장에서 변수를 **이름표가 붙은 상자**로 배웠습니다. TypeScript에서는 그 상자에 **내용물 종류 라벨**이 추가됩니다.

> **JS 02장**: 상자에 아무거나 넣을 수 있었다
> **TS**: 상자에 라벨이 붙어서 정해진 것만 넣을 수 있다

```javascript
// JavaScript — 상자에 아무거나 넣기 가능
let box = "문자열";
box = 42;       // 숫자로 바꿔도 괜찮음
box = true;     // 불리언으로 바꿔도 괜찮음
box = null;     // 심지어 null도 괜찮음
```

```typescript
// TypeScript — 상자에 라벨이 붙음
let box: string = "문자열";
box = "다른 문자열";  // ✅ 같은 종류(string)는 가능
// box = 42;          // ❌ 에러: 숫자는 string 상자에 못 넣음
// box = true;        // ❌ 에러: 불리언은 string 상자에 못 넣음
```

상자에 라벨이 생기면:

1. **실수로 잘못된 값을 넣을 때 즉시 알 수 있습니다**
2. **이 상자에서 꺼낸 값이 무엇인지 항상 알 수 있습니다**
3. **VS Code가 그 값에 무슨 메서드가 있는지 자동완성해줍니다**

---

<a id="part4"></a>

## 4️⃣ TypeScript가 잡아주는 버그들 [↑](#toc)

앞서 본 JS 버그들을 TypeScript로 다시 작성해봅니다.

### 버그 1 해결 — 잘못된 인자 타입

```typescript
// TypeScript: 매개변수 타입을 명시하면 잘못된 호출을 즉시 감지
function calculateTax(price: number): number {
  return price * 0.1;
}

calculateTax(10000);  // ✅ 정상
// calculateTax("만원"); // ❌ 컴파일 에러: Argument of type 'string' is not assignable to parameter of type 'number'.
```

VS Code에서 `calculateTax("만원")`을 입력하는 순간 빨간 줄이 그어집니다. 실행하기 전에 알 수 있습니다.

---

### 버그 2 해결 — 오타 난 속성 접근

```typescript
// TypeScript: 객체 구조를 타입으로 정의하면 오타를 즉시 감지
interface User {
  name: string;
  email: string;
}

const user: User = {
  name: "김철수",
  email: "kim@example.com"
};

console.log(user.name);   // ✅ 정상
// console.log(user.eamil); // ❌ 컴파일 에러: Property 'eamil' does not exist on type 'User'.
```

오타를 입력하는 즉시 에러가 표시됩니다. 또한 `user.`를 입력하면 `name`, `email`이 자동완성으로 제시됩니다.

---

### 버그 3 해결 — null 접근 방지

```typescript
// TypeScript (strict 모드): null 가능성을 명시하고 처리를 강제
interface User {
  name: string;
}

function getUserName(user: User | null): string {
  // user가 null일 수 있으므로 반드시 확인 후 접근
  if (user === null) {
    return "알 수 없음";
  }
  return user.name.toUpperCase(); // ✅ 여기서는 null이 아님이 보장됨
}

const activeUser: User = { name: "이영희" };
const deletedUser = null;

console.log(getUserName(activeUser));  // "이영희"
console.log(getUserName(deletedUser)); // "알 수 없음"
```

실행 결과:
```
이영희
알 수 없음
```

TypeScript는 `user`가 `null`일 수 있으면 null 체크 없이 `.name`에 접근하려는 코드를 **컴파일 에러**로 막아줍니다.

---

### 정리 — JS vs TS 에러 비교

| 버그 종류 | JavaScript | TypeScript |
|-----------|-----------|------------|
| 잘못된 타입 인자 | 런타임에 `NaN` | 컴파일 타임 에러 |
| 오타 속성 접근 | 런타임에 `undefined` | 컴파일 타임 에러 |
| null 접근 | 런타임 `TypeError` 충돌 | 컴파일 타임 에러 |

---

<a id="part5"></a>

## 5️⃣ TypeScript의 역사와 현재 [↑](#toc)

### 탄생 배경

2010년대 초, Microsoft는 내부적으로 대규모 JavaScript 프로젝트를 진행하면서 JS의 한계를 느꼈습니다. 코드베이스가 수십만 줄로 커지면서 타입 없는 JavaScript는 유지보수가 어려워졌습니다.

### 역사

| 연도 | 사건 |
|------|------|
| 2012 | Microsoft, TypeScript 0.8 공개 |
| 2014 | TypeScript 1.0 정식 출시 |
| 2016 | Angular 2가 TypeScript 채택 → 프론트엔드 표준화 시작 |
| 2019 | VS Code 자체가 TypeScript로 작성되어 있음을 공개 |
| 2020 | npm 다운로드 주간 1억 회 돌파 |
| 2023 | GitHub, Stack Overflow 조사에서 상위 5위 언어로 진입 |
| 현재 | 프론트엔드(React, Vue, Angular) 프로젝트의 사실상 표준 |

### 현재 사용 현황

- **GitHub**: 오픈소스 프로젝트의 30% 이상이 TypeScript 사용
- **npm 주간 다운로드**: 5천만 회 이상
- **주요 사용 기업**: Microsoft, Google, Airbnb, Slack, Asana
- **프레임워크**: Next.js, NestJS, Angular가 기본 TypeScript 사용

> TypeScript를 배우면 JavaScript 프로젝트 거의 어디에서나 사용할 수 있습니다.
> React 프로젝트의 `create-react-app --template typescript`, Next.js 기본 설정 등 모두 TypeScript 우선입니다.

---

<a id="part6"></a>

## 6️⃣ 정리 [↑](#toc)

### 핵심 개념 요약

| 개념 | 설명 | 비유 |
|------|------|------|
| TypeScript | JavaScript에 타입을 추가한 언어 | 라벨이 붙은 상자 시스템 |
| 컴파일 타임 에러 | 코드 저장 시 발견하는 에러 | 출발 전 지도 확인 |
| 런타임 에러 | 코드 실행 중 발생하는 에러 | 길 잃고 나서 지도 꺼내기 |
| 타입 주석 | `: string` 형태로 타입을 명시 | 상자의 라벨 |
| 타입 추론 | 값으로부터 타입을 자동 파악 | 내용물로 라벨을 자동 생성 |
| 컴파일 | `.ts` → `.js` 변환 과정 | TypeScript를 브라우저가 읽을 수 있게 번역 |

---

### 다음 장 미리보기

| 장 | 내용 |
|---|---|
| 2장 | 개발 환경 설정 — Playground, tsx, tsconfig.json |
| 3장 | 기본 타입과 타입 추론 — string, number, boolean |
| 4장 | 함수와 타입 — 매개변수와 반환 타입 |

---

### 실습 과제

**기본**: [TypeScript Playground](https://www.typescriptlang.org/play)에서 아래 코드를 입력하고 Errors 탭에서 에러 메시지를 확인해보세요.

```typescript
function add(a: number, b: number): number {
  return a + b;
}
add("1", "2"); // 에러가 발생합니다 — 어떤 에러인가요?
```

**중급**: JS 02장에서 배운 변수 선언 코드에 타입 주석을 추가해보세요. `let name: string = "홍길동"` 형태로 3개 이상 작성해보세요.

**심화**: TypeScript Playground에서 `strict` 옵션을 켜고 끄면서 `let x = null; x.toString();` 코드가 어떻게 달라지는지 확인해보세요.

{% endraw %}
