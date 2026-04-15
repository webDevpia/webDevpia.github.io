---
title: 08. Enum과 상수
layout: default
grand_parent: Language
parent: TypeScript
nav_order: 8
permalink: /language/typescript/enum
---

{% raw %}

## 학습 목표

- Enum이 필요한 이유와 숫자/문자열 Enum의 차이를 설명할 수 있다
- `const enum`으로 성능을 개선하는 방법을 이해한다
- Enum과 유니언 리터럴 타입의 장단점을 비교해 적절히 선택할 수 있다
- `as const`로 배열·객체를 읽기 전용 상수로 만들 수 있다

<a id="toc"></a>

## 진행 순서

1. [왜 Enum이 필요한가?](#part1) - 마법의 숫자·문자열 문제
2. [숫자 Enum](#part2) - 자동 증가 값, 역방향 매핑
3. [문자열 Enum](#part3) - 가독성 높은 권장 방식
4. [const enum](#part4) - 컴파일 타임 인라인, 번들 크기 최적화
5. [Enum vs 유니언 리터럴](#part5) - 언제 무엇을 쓸지
6. [as const](#part6) - 배열·객체를 상수로 만들기
7. [정리](#part7) - 핵심 요약, 실습 과제 3단계

---

# 08장. Enum과 상수

<a id="part1"></a>

## 1️⃣ 왜 Enum이 필요한가? [↑](#toc)

### 교통 신호등 비유

> 교통 신호등은 **빨강, 노랑, 초록** 세 가지 상태만 가집니다.
> 다른 색은 의미가 없습니다. 이처럼 **정해진 값의 집합**만 허용해야 하는 경우가 있습니다.
> Enum은 이런 "허용 가능한 값의 집합"을 명확하게 정의하는 방법입니다.

### 고통 — 마법의 숫자·문자열 문제

```typescript
// ❌ 숫자만 보면 의미를 알 수 없음
function setUserStatus(status: number) {
  if (status === 1) {
    console.log("활성 계정");
  } else if (status === 2) {
    console.log("정지된 계정");
  } else if (status === 3) {
    console.log("삭제된 계정");
  }
  // 1, 2, 3이 무엇을 의미하는지 코드만 봐서는 모름
}

setUserStatus(2); // 2가 무슨 상태인지?
```

```typescript
// ❌ 문자열도 오타가 나면 컴파일러가 잡지 못함
function setDirection(dir: string) {
  if (dir === "north") { /* ... */ }
  if (dir === "norht") { /* ... */ }  // 오타! 하지만 컴파일 통과
}
```

### 해결 — Enum으로 의미 있는 이름 부여

```typescript
// ✅ 값의 의미가 코드에서 바로 보임
enum UserStatus {
  Active   = 1,
  Suspended = 2,
  Deleted  = 3
}

function setUserStatus(status: UserStatus) {
  if (status === UserStatus.Active) {
    console.log("활성 계정");
  }
}

setUserStatus(UserStatus.Active);   // 의미가 명확함
setUserStatus(UserStatus.Suspended);
// setUserStatus(99);  // ❌ 컴파일 오류: 허용되지 않은 값
```

---

<a id="part2"></a>

## 2️⃣ 숫자 Enum [↑](#toc)

`enum` 키워드로 선언하면 멤버에 **자동으로 0부터 숫자**가 할당됩니다.

```typescript
enum Direction {
  Up,    // 0
  Down,  // 1
  Left,  // 2
  Right  // 3
}

console.log(Direction.Up);    // 0
console.log(Direction.Right); // 3
console.log(Direction[0]);    // "Up"  ← 역방향 매핑
```

실행 결과:
```
0
3
Up
```

### 시작값 지정

첫 번째 멤버에 값을 지정하면 이후 멤버는 그 값부터 자동 증가합니다.

```typescript
enum HttpStatus {
  OK          = 200,
  Created     = 201,
  BadRequest  = 400,
  Unauthorized = 401,
  NotFound    = 404,
  ServerError = 500
}

function handleResponse(status: HttpStatus): string {
  if (status === HttpStatus.OK || status === HttpStatus.Created) {
    return "성공";
  } else if (status >= 400 && status < 500) {
    return "클라이언트 오류";
  }
  return "서버 오류";
}

console.log(handleResponse(HttpStatus.OK));         // 성공
console.log(handleResponse(HttpStatus.NotFound));   // 클라이언트 오류
console.log(handleResponse(HttpStatus.ServerError)); // 서버 오류
```

실행 결과:
```
성공
클라이언트 오류
서버 오류
```

### 역방향 매핑 (Reverse Mapping)

숫자 Enum은 값으로 이름을 조회할 수 있습니다. (문자열 Enum은 불가)

```typescript
enum Color {
  Red,   // 0
  Green, // 1
  Blue   // 2
}

console.log(Color[1]);       // "Green"
console.log(Color["Green"]); // 1
```

> 역방향 매핑이 필요한 경우가 Enum을 선택하는 주요 이유 중 하나입니다.
> 숫자 코드를 사람이 읽을 수 있는 이름으로 변환할 때 유용합니다.

---

<a id="part3"></a>

## 3️⃣ 문자열 Enum [↑](#toc)

문자열 Enum은 각 멤버에 **명시적으로 문자열 값**을 지정합니다.

```typescript
enum Status {
  Loading = "LOADING",
  Success = "SUCCESS",
  Error   = "ERROR"
}

console.log(Status.Loading); // "LOADING"
console.log(Status.Success); // "SUCCESS"
```

실행 결과:
```
LOADING
SUCCESS
```

### 왜 문자열 Enum이 권장되는가?

```typescript
// 숫자 Enum: 로그에서 보면 의미 없는 숫자
enum NumStatus { Loading = 0, Success = 1, Error = 2 }
console.log(NumStatus.Loading); // 0 → 의미를 모름

// 문자열 Enum: 로그에서 바로 의미를 알 수 있음
enum StrStatus { Loading = "LOADING", Success = "SUCCESS", Error = "ERROR" }
console.log(StrStatus.Loading); // "LOADING" → 한눈에 이해
```

### 실용 예제: 주문 상태 관리

```typescript
enum OrderStatus {
  Pending   = "PENDING",
  Confirmed = "CONFIRMED",
  Shipped   = "SHIPPED",
  Delivered = "DELIVERED",
  Cancelled = "CANCELLED"
}

interface Order {
  id: number;
  product: string;
  status: OrderStatus;
}

function getStatusLabel(status: OrderStatus): string {
  const labels: Record<OrderStatus, string> = {
    [OrderStatus.Pending]:   "결제 대기",
    [OrderStatus.Confirmed]: "주문 확인",
    [OrderStatus.Shipped]:   "배송 중",
    [OrderStatus.Delivered]: "배송 완료",
    [OrderStatus.Cancelled]: "주문 취소"
  };
  return labels[status];
}

const order: Order = {
  id: 1001,
  product: "노트북",
  status: OrderStatus.Shipped
};

console.log(`주문 #${order.id}: ${getStatusLabel(order.status)}`);
// 주문 #1001: 배송 중
```

실행 결과:
```
주문 #1001: 배송 중
```

---

<a id="part4"></a>

## 4️⃣ const enum [↑](#toc)

`const enum`은 컴파일 시점에 **값이 인라인(inline)으로 대체**됩니다.
런타임에 Enum 객체가 생성되지 않아 번들 크기를 줄일 수 있습니다.

```typescript
const enum Weekday {
  Mon = 1,
  Tue,
  Wed,
  Thu,
  Fri,
  Sat,
  Sun
}

const today = Weekday.Wed;
console.log(today); // 3
```

컴파일된 JavaScript를 보면 Enum 객체 없이 숫자가 직접 들어갑니다:

```javascript
// 컴파일 결과 (const enum은 사라지고 값이 직접 삽입됨)
const today = 3; /* Weekday.Wed */
console.log(today);
```

### 일반 enum vs const enum 비교

```typescript
// 일반 enum: 런타임 객체 생성 (약간의 메모리 사용)
enum RegularDirection { Up = 0, Down = 1 }
// 컴파일 결과: var RegularDirection = { Up: 0, Down: 1, 0: "Up", 1: "Down" }

// const enum: 런타임 객체 없음, 값만 인라인
const enum ConstDirection { Up = 0, Down = 1 }
// 컴파일 결과: 사용 부분에 0, 1 숫자가 직접 삽입됨
```

> **주의**: `const enum`은 선언 파일(`.d.ts`)에서 사용할 때 제약이 있습니다.
> 일반 라이브러리 코드에서는 일반 `enum`이나 유니언 리터럴을 권장합니다.

---

<a id="part5"></a>

## 5️⃣ Enum vs 유니언 리터럴 [↑](#toc)

TypeScript에서 관련 상수를 표현하는 방법이 두 가지 있습니다.
언제 무엇을 써야 할지 비교합니다.

### 나란히 비교

```typescript
// ─── Enum 방식 ───
enum Color {
  Red   = "RED",
  Green = "GREEN",
  Blue  = "BLUE"
}

function paintEnum(color: Color): void {
  console.log(`색상: ${color}`);
}

paintEnum(Color.Red);        // ✅
// paintEnum("RED");         // ❌ 컴파일 오류: string은 Color가 아님

// ─── 유니언 리터럴 방식 ───
type ColorLiteral = "red" | "green" | "blue";

function paintLiteral(color: ColorLiteral): void {
  console.log(`색상: ${color}`);
}

paintLiteral("red");         // ✅
paintLiteral("green");       // ✅
// paintLiteral("yellow");   // ❌ 컴파일 오류
```

### 장단점 비교표

| 항목 | Enum | 유니언 리터럴 |
|------|------|--------------|
| 문법 간결성 | 보통 | 간단 (`"a" \| "b"`) |
| 역방향 매핑 | 숫자 Enum만 지원 | 없음 |
| 런타임 객체 | 존재 (const enum 제외) | 없음 (타입만) |
| 확장성 | 선언 병합 가능 | 새 타입 별칭 필요 |
| JSON 호환 | 문자열 Enum만 자연스러움 | 완전 호환 |
| 외부 API 값 | 어색함 | 자연스러움 |

### 권장 기준

```typescript
// ✅ 유니언 리터럴을 사용하세요 — 대부분의 경우
type Theme = "light" | "dark" | "system";
type Locale = "ko" | "en" | "ja";

// ✅ Enum을 사용하세요 — 이 경우만
// 1) 숫자 코드 ↔ 문자 이름 역방향 매핑이 필요할 때
// 2) 선언 병합으로 외부 라이브러리 Enum을 확장할 때
// 3) 기존 코드베이스가 Enum을 표준으로 사용할 때
```

> 일반적으로 **유니언 리터럴이 더 간단하고 JS와 자연스럽게 어울립니다.**
> Enum은 역방향 매핑이 필요하거나 팀 표준이 Enum을 쓸 때 선택합니다.

---

<a id="part6"></a>

## 6️⃣ as const [↑](#toc)

`as const`는 배열이나 객체를 **읽기 전용 리터럴 타입**으로 만들어줍니다.
Enum 없이도 상수 집합을 안전하게 관리할 수 있습니다.

### 배열에 as const 적용

```typescript
// ❌ as const 없이 — 타입이 string[]로 추론됨
const COLORS_MUTABLE = ["red", "green", "blue"];
// 타입: string[]  → 어떤 문자열이든 들어올 수 있음

// ✅ as const — 읽기 전용 튜플 + 리터럴 타입으로 추론됨
const COLORS = ["red", "green", "blue"] as const;
// 타입: readonly ["red", "green", "blue"]

type Color = typeof COLORS[number]; // "red" | "green" | "blue"

function setColor(color: Color): void {
  console.log(`색상 설정: ${color}`);
}

setColor("red");    // ✅
setColor("green");  // ✅
// setColor("yellow"); // ❌ 컴파일 오류
// COLORS.push("yellow"); // ❌ 컴파일 오류: readonly
```

### 객체에 as const 적용

```typescript
const HTTP_STATUS = {
  OK:          200,
  CREATED:     201,
  BAD_REQUEST: 400,
  NOT_FOUND:   404,
  SERVER_ERROR: 500
} as const;

// 타입: { readonly OK: 200; readonly CREATED: 201; ... }

type StatusCode = typeof HTTP_STATUS[keyof typeof HTTP_STATUS];
// 200 | 201 | 400 | 404 | 500

function isSuccess(code: StatusCode): boolean {
  return code === HTTP_STATUS.OK || code === HTTP_STATUS.CREATED;
}

console.log(isSuccess(HTTP_STATUS.OK));         // true
console.log(isSuccess(HTTP_STATUS.NOT_FOUND));  // false
// HTTP_STATUS.OK = 999; // ❌ 컴파일 오류: readonly
```

실행 결과:
```
true
false
```

### as const vs Enum 비교

```typescript
// Enum 방식
enum HttpMethod {
  GET    = "GET",
  POST   = "POST",
  PUT    = "PUT",
  DELETE = "DELETE"
}

// as const 방식 — 더 간결, 런타임 객체 없음
const HTTP_METHODS = ["GET", "POST", "PUT", "DELETE"] as const;
type HttpMethod2 = typeof HTTP_METHODS[number];
// "GET" | "POST" | "PUT" | "DELETE"
```

---

<a id="part7"></a>

## 7️⃣ 정리 [↑](#toc)

### 핵심 개념 요약

| 개념 | 문법 | 특징 |
|------|------|------|
| 숫자 Enum | `enum Dir { Up, Down }` | 자동 증가, 역방향 매핑 |
| 문자열 Enum | `enum S { A = "A" }` | 가독성 우수, 권장 방식 |
| const enum | `const enum E { A = 1 }` | 컴파일 타임 인라인, 객체 없음 |
| 유니언 리터럴 | `type T = "a" \| "b"` | 간단, 런타임 없음, 대부분 권장 |
| as const (배열) | `["a", "b"] as const` | readonly 튜플, 리터럴 타입 |
| as const (객체) | `{ A: 1 } as const` | readonly 객체, 정확한 타입 |
| typeof + keyof | `typeof OBJ[keyof typeof OBJ]` | as const 객체에서 값 타입 추출 |

### 다음 장 미리보기 — 9장: 클래스와 타입

- TypeScript 클래스에서 속성 타입 선언하는 방법
- `public`, `private`, `protected` 접근 제어자
- `readonly` 속성과 `implements` 키워드
- 추상 클래스(abstract class)로 설계 지침서 만들기

---

### 실습 과제

#### 기본 — 문자열 Enum으로 월(Month) 열거형 만들기

```typescript
// 12개월을 문자열 Enum으로 정의하세요
// enum Month { Jan = "JAN", Feb = "FEB", ... }
// getKoreanMonth(month: Month): string 함수를 만들어
// Month.Jan → "1월", Month.Feb → "2월" 형태로 반환하세요

enum Month {
  // 직접 채워보세요
}

function getKoreanMonth(month: Month): string {
  // switch 또는 Record를 사용하세요
}

console.log(getKoreanMonth(Month.Jan)); // 1월
console.log(getKoreanMonth(Month.Dec)); // 12월
```

#### 중급 — as const로 권한(permissions) 상수 테이블 만들기

```typescript
// 아래 PERMISSIONS 객체를 as const로 선언하고
// Role 타입과 Permission 타입을 typeof/keyof로 추출하세요
const PERMISSIONS = {
  admin:  ["read", "write", "delete", "manage"],
  editor: ["read", "write"],
  viewer: ["read"]
} as const;

// type Role = ...       (PERMISSIONS의 키: "admin" | "editor" | "viewer")
// type Permission = ... (배열 요소: "read" | "write" | "delete" | "manage")

// hasPermission(role: Role, permission: Permission): boolean 함수를 작성하세요
```

#### 심화 — HttpStatus Enum + 판별 유니언 조합

```typescript
// 7장의 판별 유니언 패턴과 Enum을 조합하세요
enum HttpStatus {
  OK      = 200,
  Created = 201,
  NotFound = 404,
  ServerError = 500
}

type ApiResult<T> =
  | { status: HttpStatus.OK | HttpStatus.Created; data: T }
  | { status: HttpStatus.NotFound;   message: string }
  | { status: HttpStatus.ServerError; message: string; retry: boolean };

// handleResult<T>(result: ApiResult<T>): void 함수를 작성하고
// 각 케이스를 처리한 뒤, never 완전성 체크도 추가하세요
```

{% endraw %}
