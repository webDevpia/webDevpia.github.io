---
title: 14. 미니 프로젝트 — ToDo 앱
layout: default
grand_parent: Language
parent: TypeScript
nav_order: 14
permalink: /language/typescript/todo-project
---

{% raw %}

## 학습 목표

- JS 10장의 ToDo 앱을 TypeScript로 리팩터링하는 전 과정을 이해할 수 있다
- `interface`, `enum`, 리터럴 유니언으로 앱 데이터 구조를 타입으로 정의할 수 있다
- DOM 요소와 이벤트 핸들러에 올바른 TS 타입을 붙일 수 있다
- Before(JS)/After(TS) 비교를 통해 타입이 어떤 버그를 막아주는지 설명할 수 있다

<a id="toc"></a>

## 진행 순서

1. [JS → TS 리팩터링이란?](#part1) - "타입 입히기"의 의미
2. [타입 정의하기](#part2) - `Todo` 인터페이스, `FilterType`, `Priority` enum
3. [함수에 타입 추가](#part3) - Before/After 4개 함수 비교
4. [DOM 타입](#part4) - `HTMLInputElement`, `querySelector`, 타입 단언
5. [이벤트 핸들러 타입](#part5) - `MouseEvent`, `KeyboardEvent`, submit 핸들러
6. [완성 코드 전체](#part6) - 복사해서 바로 사용 가능한 TS 버전
7. [JS vs TS 비교표](#part7) - 무엇이 달라졌나, 어떤 버그를 막나
8. [개념 매핑표](#part8) - 사용된 TS 개념 → 학습한 장
9. [정리](#part9) - 핵심 요약과 실습 과제

---

# 14장. 미니 프로젝트 — 타입 안전한 ToDo 앱

<a id="part1"></a>

## 1️⃣ JS → TS 리팩터링이란? [↑](#toc)

> JS 10장에서 만든 ToDo 앱을 기억하시나요?
> 그 코드에 **타입을 입히겠습니다.**
> "리팩터링(Refactoring)"은 동작은 그대로 유지하면서 코드 구조를 개선하는 작업입니다.

우리가 하려는 것은 정확히 이것입니다. 버튼이 작동하고, 항목이 추가·삭제되고, 완료 표시가 되는 **동작 자체는 그대로**입니다. 달라지는 것은 **타입 안전성**입니다.

### JS 10장 코드 일부 (리팩터링 전)

```javascript
// JS 10장 — 타입이 없는 todos 배열
let todos = [];

function addTodo() {
  const input = document.getElementById('todo-input');
  const text = input.value.trim();  // input이 null일 수도? 모름

  if (text === '') {
    alert('할 일을 입력해 주세요!');
    return;
  }

  const newTodo = {
    id: Date.now(),
    text: text,
    completed: false
    // createdAt 같은 필드를 나중에 추가하면 기존 todo 객체와 불일치 발생 가능
  };

  todos.push(newTodo);
  renderTodos();
}
```

이 코드에서 발생할 수 있는 문제:

| 문제 | 발생 시점 | TypeScript라면? |
|------|-----------|----------------|
| `input`이 `null`일 때 `.value` 접근 | 런타임 TypeError | 컴파일 타임 에러 |
| `todos`에 다른 구조의 객체 삽입 | 런타임 오동작 | 컴파일 타임 에러 |
| `filterTodos("all2")` 오타 | 런타임 조건 미충족 | 컴파일 타임 에러 |
| `todo.complted` 속성 오타 | 런타임 `undefined` | 컴파일 타임 에러 |

TypeScript로 리팩터링하면 이 모든 실수를 **코드 작성 시점**에 잡을 수 있습니다.

### 리팩터링 전략

```
JS 10장 코드
    ↓
1단계: 타입 정의 (interface, enum, type)
    ↓
2단계: 함수 시그니처에 타입 추가
    ↓
3단계: DOM 접근 타입 수정
    ↓
4단계: 이벤트 핸들러 타입 추가
    ↓
타입 안전한 TS ToDo 앱 완성
```

---

<a id="part2"></a>

## 2️⃣ 타입 정의하기 [↑](#toc)

> 집을 짓기 전에 설계도를 그리듯, 코드를 작성하기 전에 타입을 먼저 정의합니다.
> 타입 정의 파일은 앱 전체의 "계약서"입니다.

### Todo 인터페이스 (06장 interface)

```typescript
// types/todo.ts

// [06장 interface] Todo 객체의 구조를 명확히 정의
interface Todo {
  id: number;
  text: string;
  completed: boolean;
  createdAt: Date;
}
```

이제 `Todo` 타입을 벗어나는 객체는 컴파일 에러가 납니다.

```typescript
// ✅ 올바른 Todo 객체
const todo: Todo = {
  id: 1,
  text: "타입스크립트 공부",
  completed: false,
  createdAt: new Date()
};

// ❌ 에러: 'text' 속성이 없음
const bad: Todo = {
  id: 2,
  completed: false,
  createdAt: new Date()
  // text 누락 → Property 'text' is missing in type
};
```

### FilterType 리터럴 유니언 (05장 유니언/리터럴)

```typescript
// [05장 리터럴 유니언] 필터 값은 세 가지 중 하나만 허용
type FilterType = "all" | "active" | "completed";
```

```typescript
// ✅ 허용된 값
const filter: FilterType = "all";
const filter2: FilterType = "active";

// ❌ 에러: 오타를 즉시 잡아줌
// const bad: FilterType = "all2";
// Type '"all2"' is not assignable to type 'FilterType'
```

### Priority enum (08장 enum)

```typescript
// [08장 enum] 우선순위는 세 단계로 제한
enum Priority {
  Low = "low",
  Medium = "medium",
  High = "high"
}
```

```typescript
// ✅ enum 값 사용
const p: Priority = Priority.High;
console.log(p); // "high"

// ❌ 임의 문자열 사용 불가
// const bad: Priority = "urgent";
// Type '"urgent"' is not assignable to type 'Priority'
```

### 세 타입을 하나 파일에 정리

```typescript
// types/todo.ts — 앱 전체에서 공유하는 타입 정의

interface Todo {
  id: number;
  text: string;
  completed: boolean;
  createdAt: Date;
}

type FilterType = "all" | "active" | "completed";

enum Priority {
  Low = "low",
  Medium = "medium",
  High = "high"
}
```

---

<a id="part3"></a>

## 3️⃣ 함수에 타입 추가 [↑](#toc)

> 함수는 타입 시스템의 핵심입니다.
> 매개변수와 반환 타입을 명시하면 잘못된 호출을 즉시 감지할 수 있습니다.

### addTodo — 할 일 추가

**Before (JS 10장)**

```javascript
// JS: 어떤 값이 들어와도 에러 없음
function addTodo() {
  const input = document.getElementById('todo-input');
  const text = input.value.trim();
  if (text === '') return;

  const newTodo = {
    id: Date.now(),
    text: text,
    completed: false
  };
  todos.push(newTodo);
  renderTodos();
}
```

**After (TS)**

```typescript
// TS: 반환 타입 void, todos 배열은 Todo[] 타입
let todos: Todo[] = [];

function addTodo(text: string): void {
  // [04장 함수 타입] 매개변수 text는 반드시 string
  if (text.trim() === "") return;

  const newTodo: Todo = {
    id: Date.now(),
    text: text.trim(),
    completed: false,
    createdAt: new Date()        // createdAt 필드 누락 시 에러
  };

  todos.push(newTodo);           // Todo 타입이 아닌 객체 push 시 에러
  renderTodos();
}
```

달라진 점:
- `text: string` → 숫자나 객체 전달 시 컴파일 에러
- `: void` → 값을 반환하려 하면 에러
- `todos: Todo[]` → 구조가 다른 객체 push 시 에러

---

### toggleTodo — 완료 상태 전환

**Before (JS 10장)**

```javascript
// JS: id가 number인지 string인지 불분명
function toggleTodo(id) {
  const todo = todos.find(t => t.id === id);
  if (todo) {
    todo.completed = !todo.completed;
  }
  renderTodos();
}
```

**After (TS)**

```typescript
// TS: id는 반드시 number
function toggleTodo(id: number): void {
  const todo: Todo | undefined = todos.find((t: Todo) => t.id === id);

  if (todo !== undefined) {
    // [07장 타입 좁히기] undefined 체크 후 접근 — 안전 보장
    todo.completed = !todo.completed;
  }

  renderTodos();
}
```

```typescript
// ❌ 문자열 id로 호출 시 즉시 에러
// toggleTodo("1");
// Argument of type 'string' is not assignable to parameter of type 'number'
```

---

### deleteTodo — 할 일 삭제

**Before (JS 10장)**

```javascript
function deleteTodo(id) {
  todos = todos.filter(t => t.id !== id);
  renderTodos();
}
```

**After (TS)**

```typescript
// TS: 매개변수·반환·배열 모두 타입 명시
function deleteTodo(id: number): void {
  todos = todos.filter((t: Todo) => t.id !== id);
  renderTodos();
}
```

---

### filterTodos — 필터 적용

JS 10장에는 없던 기능입니다. 리팩터링하면서 추가합니다.

```typescript
// [05장 리터럴 유니언] filter 값은 FilterType만 허용
function filterTodos(filter: FilterType): Todo[] {
  switch (filter) {
    case "all":
      return todos;
    case "active":
      return todos.filter((t: Todo) => !t.completed);
    case "completed":
      return todos.filter((t: Todo) => t.completed);
    // TS는 switch가 FilterType의 모든 경우를 처리했는지 자동 확인
  }
}
```

```typescript
// ✅ 정상 호출
filterTodos("all");
filterTodos("active");
filterTodos("completed");

// ❌ 에러: FilterType에 없는 값
// filterTodos("pending");
// Argument of type '"pending"' is not assignable to parameter of type 'FilterType'
```

---

<a id="part4"></a>

## 4️⃣ DOM 타입 [↑](#toc)

> DOM 요소에도 타입이 있습니다. `<input>`은 `HTMLInputElement`, `<button>`은 `HTMLButtonElement`입니다.
> TypeScript는 잘못된 DOM 접근도 컴파일 타임에 잡아줍니다.

### querySelector의 반환 타입 문제

```typescript
// querySelector는 Element | null 을 반환합니다
const input = document.querySelector("#todoInput");
// input의 타입: Element | null

// ❌ 에러: Element에는 .value 속성이 없음
// console.log(input.value);
// Property 'value' does not exist on type 'Element'
```

TypeScript는 `querySelector`가 반환하는 값이 `null`일 수도 있고, 어떤 종류의 요소인지 모른다는 점을 지적합니다.

### 해결법 — 타입 단언 (13장 타입 단언)

```typescript
// [13장 타입 단언] as를 사용해서 구체적인 타입 지정
const input = document.querySelector("#todoInput") as HTMLInputElement;
const addBtn = document.querySelector("#add-btn") as HTMLButtonElement;
const todoList = document.querySelector("#todo-list") as HTMLUListElement;
const footer = document.querySelector("#footer") as HTMLElement;
```

이제 `input.value`에 접근해도 에러가 없습니다.

```typescript
// ✅ HTMLInputElement의 속성 사용 가능
const text: string = input.value.trim();
input.focus();
input.placeholder = "할 일을 입력하세요";
```

### 주요 DOM 타입 목록

| HTML 요소 | TypeScript 타입 | 주요 속성/메서드 |
|-----------|----------------|----------------|
| `<input>` | `HTMLInputElement` | `.value`, `.checked`, `.focus()` |
| `<button>` | `HTMLButtonElement` | `.disabled`, `.textContent` |
| `<ul>`, `<ol>` | `HTMLUListElement` / `HTMLOListElement` | `.innerHTML`, `.appendChild()` |
| `<li>` | `HTMLLIElement` | `.innerHTML`, `.className` |
| `<div>` | `HTMLDivElement` | `.innerHTML`, `.style` |
| 그 외 일반 | `HTMLElement` | `.textContent`, `.style`, `.classList` |

### 안전한 DOM 접근 헬퍼 함수

매번 `as HTMLInputElement`를 쓰는 것이 번거롭다면 헬퍼 함수를 사용할 수 있습니다.

```typescript
// [10장 제네릭] — 타입 매개변수로 어떤 요소든 안전하게 가져오기
function getElement<T extends HTMLElement>(selector: string): T {
  const element = document.querySelector<T>(selector);
  if (element === null) {
    throw new Error(`요소를 찾을 수 없습니다: ${selector}`);
  }
  return element;
}

// 사용 예
const input = getElement<HTMLInputElement>("#todoInput");
const addBtn = getElement<HTMLButtonElement>("#add-btn");
```

---

<a id="part5"></a>

## 5️⃣ 이벤트 핸들러 타입 [↑](#toc)

> 이벤트 핸들러도 타입이 있습니다. 어떤 이벤트인지 명시하면 `event.key`, `event.target` 등에 안전하게 접근할 수 있습니다.

### 클릭 이벤트 핸들러

**Before (JS 10장)**

```javascript
// JS: event 매개변수의 타입 불명확
document.getElementById('add-btn').addEventListener('click', function(event) {
  addTodo();
});
```

**After (TS)**

```typescript
// TS: MouseEvent 타입으로 event 속성 자동완성 가능
addBtn.addEventListener("click", (event: MouseEvent): void => {
  event.preventDefault();  // MouseEvent에 있는 메서드 — 타입 안전
  const text = input.value;
  addTodo(text);
});
```

### 키보드 이벤트 핸들러

**Before (JS 10장)**

```javascript
// JS: event.key 접근이 안전한지 모름
document.getElementById('todo-input').addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    addTodo();
  }
});
```

**After (TS)**

```typescript
// TS: KeyboardEvent 타입 — .key, .code, .ctrlKey 등 자동완성
input.addEventListener("keydown", (event: KeyboardEvent): void => {
  if (event.key === "Enter") {
    const text = input.value;
    addTodo(text);
  }
});
```

### DOMContentLoaded 핸들러

```typescript
// TS: Event 타입 (가장 기본 이벤트 타입)
document.addEventListener("DOMContentLoaded", (event: Event): void => {
  // 초기화 코드
  renderTodos();
});
```

### 이벤트 타입 상속 구조

```
Event (최상위)
  ├── UIEvent
  │     ├── MouseEvent    (click, dblclick, mouseover...)
  │     ├── KeyboardEvent (keydown, keyup, keypress...)
  │     └── TouchEvent    (touchstart, touchend...)
  └── FocusEvent          (focus, blur...)
```

구체적인 타입일수록 더 많은 속성에 접근할 수 있습니다.

```typescript
// MouseEvent이면 좌표 정보 접근 가능
addBtn.addEventListener("click", (e: MouseEvent) => {
  console.log(e.clientX, e.clientY);  // 클릭 위치 (x, y)
});

// KeyboardEvent이면 키 정보 접근 가능
input.addEventListener("keydown", (e: KeyboardEvent) => {
  console.log(e.key, e.shiftKey);  // 눌린 키, Shift 여부
});
```

---

<a id="part6"></a>

## 6️⃣ 완성 코드 전체 [↑](#toc)

아래는 JS 10장 ToDo 앱을 TypeScript로 완전히 리팩터링한 코드입니다.  
`todo.ts`로 저장하고 `tsc todo.ts` 또는 `tsx todo.ts`로 실행합니다.  
브라우저용이므로 HTML과 함께 사용하거나 TypeScript Playground에서 확인하세요.

```typescript
// ─────────────────────────────────────────────────────────────
// types: 앱 전체 데이터 구조 정의
// ─────────────────────────────────────────────────────────────

// [06장 interface] Todo 객체의 구조
interface Todo {
  id: number;
  text: string;
  completed: boolean;
  createdAt: Date;
}

// [05장 리터럴 유니언] 필터 값은 세 가지 중 하나
type FilterType = "all" | "active" | "completed";

// [08장 enum] 우선순위 상수
enum Priority {
  Low = "low",
  Medium = "medium",
  High = "high"
}

// ─────────────────────────────────────────────────────────────
// 상태: 타입이 지정된 전역 변수
// ─────────────────────────────────────────────────────────────

let todos: Todo[] = [];
let currentFilter: FilterType = "all";

// ─────────────────────────────────────────────────────────────
// DOM 접근: 타입 단언으로 안전하게
// ─────────────────────────────────────────────────────────────

// [13장 타입 단언] querySelector + as
const input = document.querySelector("#todoInput") as HTMLInputElement;
const addBtn = document.querySelector("#add-btn") as HTMLButtonElement;
const todoList = document.querySelector("#todo-list") as HTMLUListElement;
const footer = document.querySelector("#footer") as HTMLElement;

// ─────────────────────────────────────────────────────────────
// 핵심 로직 함수 (타입 명시)
// ─────────────────────────────────────────────────────────────

// [04장 함수 타입] 반환 타입 void
function addTodo(text: string): void {
  if (text.trim() === "") {
    alert("할 일을 입력해 주세요!");
    return;
  }

  // [06장 interface] Todo 타입과 일치하지 않으면 에러
  const newTodo: Todo = {
    id: Date.now(),
    text: text.trim(),
    completed: false,
    createdAt: new Date()
  };

  todos.push(newTodo);
  input.value = "";
  input.focus();
  renderTodos();
}

// [07장 타입 좁히기] find 결과는 Todo | undefined
function toggleTodo(id: number): void {
  const todo: Todo | undefined = todos.find((t: Todo) => t.id === id);

  if (todo !== undefined) {
    todo.completed = !todo.completed;
  }

  renderTodos();
}

// [04장 함수 타입] 반환 타입 void
function deleteTodo(id: number): void {
  todos = todos.filter((t: Todo) => t.id !== id);
  renderTodos();
}

// [05장 리터럴 유니언] FilterType만 허용
function filterTodos(filter: FilterType): Todo[] {
  switch (filter) {
    case "all":
      return todos;
    case "active":
      return todos.filter((t: Todo) => !t.completed);
    case "completed":
      return todos.filter((t: Todo) => t.completed);
  }
}

// ─────────────────────────────────────────────────────────────
// 렌더링 함수
// ─────────────────────────────────────────────────────────────

function renderTodos(): void {
  const filtered: Todo[] = filterTodos(currentFilter);

  todoList.innerHTML = "";

  filtered.forEach((todo: Todo) => {
    const li: HTMLLIElement = document.createElement("li");

    li.innerHTML = `
      <span
        class="todo-text ${todo.completed ? "completed" : ""}"
        data-id="${todo.id}"
      >${todo.text}</span>
      <small class="date">${todo.createdAt.toLocaleDateString("ko-KR")}</small>
      <button class="delete-btn" data-id="${todo.id}">삭제</button>
    `;

    todoList.appendChild(li);
  });

  // 남은 할 일 개수 계산
  const remaining: number = todos.filter((t: Todo) => !t.completed).length;
  footer.textContent = `남은 할 일: ${remaining}개`;
}

// ─────────────────────────────────────────────────────────────
// 이벤트 핸들러 등록
// ─────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", (event: Event): void => {

  // [MouseEvent] 추가 버튼 클릭
  addBtn.addEventListener("click", (event: MouseEvent): void => {
    addTodo(input.value);
  });

  // [KeyboardEvent] Enter 키로 추가
  input.addEventListener("keydown", (event: KeyboardEvent): void => {
    if (event.key === "Enter") {
      addTodo(input.value);
    }
  });

  // [MouseEvent] 이벤트 위임 — 목록 클릭 (토글 + 삭제)
  todoList.addEventListener("click", (event: MouseEvent): void => {
    const target = event.target as HTMLElement;
    const idStr: string | undefined = target.dataset["id"];

    if (idStr === undefined) return;

    const id: number = Number(idStr);

    if (target.classList.contains("todo-text")) {
      toggleTodo(id);
    } else if (target.classList.contains("delete-btn")) {
      deleteTodo(id);
    }
  });

  renderTodos();
});
```

---

<a id="part7"></a>

## 7️⃣ JS vs TS 비교 [↑](#toc)

### 코드 변경 비교표

| 코드 위치 | JavaScript (JS 10장) | TypeScript (이번 장) |
|-----------|---------------------|---------------------|
| `todos` 배열 | `let todos = []` | `let todos: Todo[] = []` |
| `newTodo` 생성 | `{ id, text, completed }` | `{ id, text, completed, createdAt }` (필드 누락 불가) |
| DOM 접근 | `document.getElementById('...')` | `document.querySelector(...) as HTMLInputElement` |
| `addTodo` 매개변수 | 없음 (전역 DOM 직접 접근) | `text: string` |
| 이벤트 핸들러 | `function(event) {}` | `(event: MouseEvent): void => {}` |
| `filterTodos` | 없음 | `filter: FilterType` 매개변수로 추가 |
| `find` 반환값 | 타입 불명확 | `Todo \| undefined` 명시 |

### TypeScript가 추가로 잡아주는 버그

```typescript
// 버그 1 — 잘못된 타입의 id 전달
// toggleTodo("1");  // ❌ string은 number 자리에 못 들어감

// 버그 2 — Todo 구조 불일치
// todos.push({ id: 1, text: "공부" }); // ❌ completed, createdAt 누락

// 버그 3 — 없는 필터 값 사용
// filterTodos("pending"); // ❌ FilterType에 없는 값

// 버그 4 — null인 DOM 요소에 접근
// const x = document.querySelector("#없는요소");
// x.value; // ❌ null일 수 있음 — as 없이는 접근 불가

// 버그 5 — 속성 오타
// todo.complted = true; // ❌ Property 'complted' does not exist on type 'Todo'
```

---

<a id="part8"></a>

## 8️⃣ 개념 매핑표 [↑](#toc)

이번 프로젝트에서 사용한 모든 TypeScript 개념과, 그것을 처음 배운 장을 정리합니다.

| 사용된 개념 | 코드 예시 | 학습한 장 |
|-----------|----------|---------|
| `interface` | `interface Todo { id: number; ... }` | 06장 |
| 리터럴 유니언 | `type FilterType = "all" \| "active" \| "completed"` | 05장 |
| `enum` | `enum Priority { Low = "low", ... }` | 08장 |
| 함수 반환 타입 | `function addTodo(text: string): void` | 04장 |
| 배열 타입 | `let todos: Todo[]` | 03장 |
| 타입 좁히기 | `if (todo !== undefined)` | 07장 |
| 타입 단언 (`as`) | `querySelector(...) as HTMLInputElement` | 13장 |
| 제네릭 헬퍼 | `function getElement<T extends HTMLElement>` | 10장 |
| DOM 이벤트 타입 | `(event: MouseEvent): void` | 12장 |

---

<a id="part9"></a>

## 9️⃣ 정리 [↑](#toc)

### 핵심 개념 요약

| 개념 | 설명 | 이번 장 예시 |
|------|------|------------|
| 인터페이스로 객체 모양 정의 | `interface`로 Todo 구조 고정 | `interface Todo { id: number; ... }` |
| 리터럴 유니언으로 값 제한 | 문자열 오타를 컴파일 타임에 차단 | `type FilterType = "all" \| "active" \| "completed"` |
| 열거형으로 상수 관리 | 관련 상수를 그룹화 | `enum Priority { Low, Medium, High }` |
| DOM 타입 단언 | `HTMLElement`를 구체적 타입으로 | `querySelector(...) as HTMLInputElement` |
| 이벤트 타입 명시 | 이벤트 속성에 안전하게 접근 | `(event: KeyboardEvent) => event.key` |
| `Todo \| undefined` 좁히기 | `find` 결과 null 안전 처리 | `if (todo !== undefined) { ... }` |

---

### 실습 과제

**기본** — 위 완성 코드에서 `Priority` enum을 `Todo` 인터페이스에 추가해보세요.

```typescript
// 힌트: Todo 인터페이스에 priority 필드를 추가합니다
interface Todo {
  id: number;
  text: string;
  completed: boolean;
  createdAt: Date;
  priority: Priority; // 이 줄을 추가하면 어떤 에러가 발생하나요?
}
// → addTodo 함수에서 priority를 함께 받아야 합니다
```

**중급** — `filterTodos` 함수를 `priority`로도 필터링할 수 있도록 확장해보세요.

```typescript
// 힌트: FilterType에 priority 값을 추가하거나 별도 매개변수를 추가할 수 있습니다
type FilterType = "all" | "active" | "completed" | "high" | "medium" | "low";
```

**심화** — `localStorage`로 새로고침 후에도 데이터를 유지하도록 `saveTodos`와 `loadTodos` 함수를 TypeScript 타입과 함께 작성해보세요.

```typescript
// 힌트
function saveTodos(todos: Todo[]): void {
  localStorage.setItem("todos", JSON.stringify(todos));
}

function loadTodos(): Todo[] {
  const saved: string | null = localStorage.getItem("todos");
  if (saved === null) return [];
  // JSON.parse 결과는 any 타입 — 어떻게 Todo[]로 만들 수 있을까요?
  return JSON.parse(saved) as Todo[];
}
```

{% endraw %}
