---
title: 11. 미니 프로젝트 — AI 협업 ToDo 앱
layout: default
parent: AI-Native JavaScript
nav_order: 12
permalink: /ai-native-js/todo-app
---

# 11장. 미니 프로젝트 — AI 협업 ToDo 앱
{: .no_toc }

> **Day 3** · Phase 2 · 예상 시간: 120분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 생성 + 검증 모드**
> AI(Copilot)가 코드를 생성할 수 있습니다.
> 단, 반드시 생성된 코드를 **읽고, 이해하고, 테스트로 검증**해야 합니다.
> AI 코드를 이해 없이 복붙하는 것은 금지입니다.

## 학습 목표

- 요구사항을 자연어로 명확하게 작성할 수 있다
- AI가 생성한 코드를 검증하고 수정할 수 있다
- Vitest로 핵심 로직을 테스트할 수 있다

<a id="toc"></a>

## 진행 순서

1. [프로젝트 소개](#part1) — 무엇을 만드는가
2. [요구사항 작성하기](#part2) — AI-Native 개발의 첫 단계
3. [프로젝트 구조 만들기](#part3) — 폴더와 파일 준비
4. [핵심 로직부터 — 테스트 먼저](#part4) — 미니 TDD 경험
5. [UI 연결하기](#part5) — DOM 코드 읽고 검증
6. [검증하고 개선하기](#part6) — 엣지 케이스 테스트
7. [Phase 2 관문](#part7) — 자기 점검 체크리스트
8. [정리](#part8) — Phase 2 완주 축하

---

<a id="part1"></a>

## 1️⃣ 프로젝트 소개 [↑](#toc)

이 장은 Phase 2의 **최종 관문**입니다. 지금까지 배운 모든 것을 하나의 프로젝트에서 사용합니다.

- DOM 조작 (08장)
- AI 코드 평가 체크리스트 및 Bug Hunt (09장)
- async/await 및 API 호출 (10장)
- Vitest 테스트 (07장)

### 우리가 만들 것: 브라우저 ToDo 앱

```
┌─────────────────────────────────────┐
│  나의 할 일 목록                     │
│                                     │
│  [ 할 일 입력                ] [추가] │
│                                     │
│  전체(5) | 완료(2) | 미완료(3)       │
│  ─────────────────────────────────  │
│  ☑ 장보기                    [삭제]  │
│  ☑ 운동하기                  [삭제]  │
│  ○ JavaScript 공부하기       [삭제]  │
│  ○ 보고서 작성               [삭제]  │
│  ○ 이메일 확인               [삭제]  │
│                                     │
│  완료: 2개 / 전체: 5개              │
└─────────────────────────────────────┘
```

### AI-Native 협업 흐름

이 프로젝트에서 여러분과 AI는 역할을 나눕니다:

| 여러분 | AI (Copilot) |
|--------|--------------|
| 요구사항 작성 | 코드 생성 |
| 테스트 작성 | 구현 코드 생성 |
| 코드 읽고 설명하기 | UI 연결 코드 생성 |
| 버그 찾고 수정하기 | 수정 제안 |

---

<a id="part2"></a>

## 2️⃣ ⭐ **핵심** — 요구사항 작성하기 [↑](#toc)

> 강사와 함께 요구사항을 작성해 봅시다

AI-Native 개발의 첫 단계는 **무엇을 만들지 명확하게 쓰는 것**입니다. 좋은 요구사항이 좋은 AI 코드를 만듭니다.

> 건축가가 설계도 없이 집을 짓지 않듯이,
> AI-Native 개발자는 요구사항 없이 AI에게 코드를 요청하지 않습니다.
> 요구사항은 내가 무엇을 원하는지 정확히 생각하게 해주는 도구입니다.

### 기능 요구사항

```
기능 요구사항:
1. 할 일을 텍스트로 입력하고 추가할 수 있다
2. 각 할 일에 완료/미완료 토글이 있다
3. 할 일을 삭제할 수 있다
4. "전체/완료/미완료" 필터로 목록을 걸러볼 수 있다
5. 할 일 개수가 표시된다
```

### 제약 조건 (Constraints)

```
제약 조건:
- 핵심 로직(추가, 토글, 삭제, 필터)은 순수 함수로 구현한다
- 외부 라이브러리 없이 순수 JavaScript만 사용한다
- 빈 텍스트는 추가할 수 없다
```

### 좋은 요구사항 vs 나쁜 요구사항

**나쁜 요구사항**:
```
할 일 앱 만들어줘
```

AI가 무엇을 만들지, 어떻게 동작해야 할지 알 수 없습니다.

---

**좋은 요구사항**:
```
다음 기능을 가진 브라우저 ToDo 앱을 만들어줘:

기능:
1. 텍스트 입력 후 "추가" 버튼 또는 Enter 키로 할 일을 추가
2. 각 항목 클릭으로 완료/미완료 토글
3. 항목마다 "삭제" 버튼
4. "전체/완료/미완료" 탭으로 필터링

제약:
- 순수 함수 (addTodo, toggleTodo, deleteTodo, filterTodos)를 todo.js에 분리
- DOM 조작 코드는 app.js에 분리
- 빈 입력은 무시
```

이제 AI가 정확히 무엇을 만들어야 하는지 알 수 있습니다.

---

<a id="part3"></a>

## 3️⃣ 프로젝트 구조 만들기 [↑](#toc)

터미널에서 다음 명령어를 실행하세요:

```bash
# 프로젝트 폴더 만들기
mkdir todo-app
cd todo-app

# Node.js 프로젝트 초기화
npm init -y

# Vitest 설치
npm install -D vitest

# 폴더 구조 만들기
mkdir src tests
```

### package.json 수정

`package.json`을 열고 `scripts` 부분을 수정하세요:

```json
{
  "name": "todo-app",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "devDependencies": {
    "vitest": "^2.0.0"
  }
}
```

### 최종 파일 구조

```
todo-app/
├── index.html          ← 사용자 인터페이스
├── src/
│   ├── todo.js         ← 핵심 로직 (순수 함수)
│   └── app.js          ← DOM 연결 코드
├── tests/
│   └── todo.test.js    ← 테스트
├── package.json
└── style.css           ← (선택) 스타일
```

### HTML 뼈대 만들기

`index.html` 파일을 만들고 다음 내용을 작성하세요. (이 부분은 직접 작성합니다!)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>나의 할 일 목록</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="container">
    <h1>나의 할 일 목록</h1>

    <form id="todoForm">
      <input
        type="text"
        id="todoInput"
        placeholder="할 일을 입력하세요"
        autocomplete="off"
      >
      <button type="submit">추가</button>
    </form>

    <div class="filters">
      <button class="filter-btn active" data-filter="all">전체</button>
      <button class="filter-btn" data-filter="completed">완료</button>
      <button class="filter-btn" data-filter="active">미완료</button>
    </div>

    <ul id="todoList"></ul>

    <p id="counter"></p>
  </div>

  <script type="module" src="src/app.js"></script>
</body>
</html>
```

---

<a id="part4"></a>

## 4️⃣ ⭐ **핵심** — 핵심 로직부터 — 테스트 먼저 [↑](#toc)

> 강사 시연을 보면서 따라하세요

AI-Native 개발에서 가장 중요한 원칙 중 하나입니다.

> **테스트를 먼저 작성하고, AI에게 구현을 요청한다.**
>
> 테스트는 "무엇이 되어야 하는지"의 명세입니다.
> AI가 코드를 만들었을 때 테스트가 통과하면 올바른 구현입니다.
> 테스트가 실패하면 AI의 코드에 문제가 있다는 신호입니다.

### Step 1: 테스트 먼저 작성하기

`tests/todo.test.js`를 만들고 다음 테스트를 작성하세요. (직접 작성하세요!)

```javascript
// tests/todo.test.js
import { describe, it, expect, beforeEach } from 'vitest';
import { addTodo, toggleTodo, deleteTodo, filterTodos } from '../src/todo.js';

describe('addTodo', () => {
  it('텍스트를 받아 새 할 일 객체를 추가한 배열을 반환한다', () => {
    const todos = [];
    const result = addTodo(todos, '공부하기');

    expect(result).toHaveLength(1);
    expect(result[0].text).toBe('공부하기');
    expect(result[0].completed).toBe(false);
    expect(result[0].id).toBeDefined();
  });

  it('빈 텍스트는 추가하지 않는다', () => {
    const todos = [];
    const result = addTodo(todos, '');
    expect(result).toHaveLength(0);
  });

  it('공백만 있는 텍스트는 추가하지 않는다', () => {
    const todos = [];
    const result = addTodo(todos, '   ');
    expect(result).toHaveLength(0);
  });

  it('원본 배열을 변경하지 않는다 (불변성)', () => {
    const todos = [];
    addTodo(todos, '공부하기');
    expect(todos).toHaveLength(0); // 원본은 그대로
  });
});

describe('toggleTodo', () => {
  it('해당 id의 completed 상태를 반전시킨다', () => {
    const todos = [
      { id: 1, text: '공부', completed: false },
    ];
    const result = toggleTodo(todos, 1);

    expect(result[0].completed).toBe(true);
  });

  it('존재하지 않는 id는 배열을 그대로 반환한다', () => {
    const todos = [
      { id: 1, text: '공부', completed: false },
    ];
    const result = toggleTodo(todos, 999);
    expect(result).toEqual(todos);
  });

  it('원본 배열을 변경하지 않는다', () => {
    const todos = [{ id: 1, text: '공부', completed: false }];
    toggleTodo(todos, 1);
    expect(todos[0].completed).toBe(false); // 원본은 그대로
  });
});

describe('deleteTodo', () => {
  it('해당 id의 할 일을 제거한 새 배열을 반환한다', () => {
    const todos = [
      { id: 1, text: '공부', completed: false },
      { id: 2, text: '운동', completed: false },
    ];
    const result = deleteTodo(todos, 1);

    expect(result).toHaveLength(1);
    expect(result[0].id).toBe(2);
  });

  it('원본 배열을 변경하지 않는다', () => {
    const todos = [{ id: 1, text: '공부', completed: false }];
    deleteTodo(todos, 1);
    expect(todos).toHaveLength(1); // 원본은 그대로
  });
});

describe('filterTodos', () => {
  let todos;

  beforeEach(() => {
    todos = [
      { id: 1, text: '공부', completed: true },
      { id: 2, text: '운동', completed: false },
      { id: 3, text: '독서', completed: false },
    ];
  });

  it('"all" 필터는 전체 배열을 반환한다', () => {
    expect(filterTodos(todos, 'all')).toHaveLength(3);
  });

  it('"completed" 필터는 완료된 항목만 반환한다', () => {
    const result = filterTodos(todos, 'completed');
    expect(result).toHaveLength(1);
    expect(result[0].text).toBe('공부');
  });

  it('"active" 필터는 미완료 항목만 반환한다', () => {
    const result = filterTodos(todos, 'active');
    expect(result).toHaveLength(2);
  });
});
```

### Step 2: 테스트 실행 — 당연히 실패합니다

```bash
npm test
```

```
FAIL  tests/todo.test.js
  Cannot find module '../src/todo.js'
```

구현 파일이 없으니 당연히 실패합니다. 이제 Copilot에게 구현을 요청합니다.

### Step 3: Copilot에게 구현 요청하기

`src/todo.js` 파일을 새로 만들고, 파일 상단에 다음 주석을 작성한 뒤 Copilot 자동완성을 기다리세요:

```javascript
// todo.js
// 할 일 목록의 핵심 로직을 순수 함수로 구현합니다.
// 각 함수는 원본 배열을 변경하지 않고 새 배열을 반환해야 합니다.
//
// addTodo(todos, text): 새 할 일을 추가한 배열 반환
// toggleTodo(todos, id): id의 completed를 반전시킨 배열 반환
// deleteTodo(todos, id): id를 제거한 배열 반환
// filterTodos(todos, filter): 'all'|'completed'|'active' 필터 적용

export function addTodo(todos, text) {
  // Copilot이 여기부터 생성할 것입니다
```

### Copilot 생성 코드 예시

Copilot이 생성한 코드가 다음과 같다고 가정합니다:

```javascript
// src/todo.js (Copilot 생성)
export function addTodo(todos, text) {
  const trimmed = text.trim();
  if (!trimmed) return todos;

  const newTodo = {
    id: Date.now(),
    text: trimmed,
    completed: false,
  };

  return [...todos, newTodo];
}

export function toggleTodo(todos, id) {
  return todos.map((todo) =>
    todo.id === id ? { ...todo, completed: !todo.completed } : todo
  );
}

export function deleteTodo(todos, id) {
  return todos.filter((todo) => todo.id !== id);
}

export function filterTodos(todos, filter) {
  if (filter === 'completed') return todos.filter((t) => t.completed);
  if (filter === 'active') return todos.filter((t) => !t.completed);
  return todos;
}
```

### Step 4: 생성된 코드 읽기

테스트를 실행하기 전에 코드를 읽으세요. 각 줄에 주석을 달아봅니다:

```javascript
export function addTodo(todos, text) {
  const trimmed = text.trim();
  // → text의 앞뒤 공백을 제거한다

  if (!trimmed) return todos;
  // → trimmed가 빈 문자열이면 (falsy이면) 원본 배열을 그대로 반환한다

  const newTodo = {
    id: Date.now(),
    // → 현재 타임스탬프(밀리초)를 id로 사용. 충분히 고유하다
    text: trimmed,
    completed: false,
  };

  return [...todos, newTodo];
  // → 스프레드 연산자로 원본 배열을 복사하고 newTodo를 끝에 추가한 새 배열 반환
}
```

### Step 5: 테스트 실행 — 통과 확인

```bash
npm test
```

```
✓ tests/todo.test.js (10 tests)
  ✓ addTodo > 텍스트를 받아 새 할 일 객체를 추가한 배열을 반환한다
  ✓ addTodo > 빈 텍스트는 추가하지 않는다
  ✓ addTodo > 공백만 있는 텍스트는 추가하지 않는다
  ✓ addTodo > 원본 배열을 변경하지 않는다 (불변성)
  ✓ toggleTodo > 해당 id의 completed 상태를 반전시킨다
  ✓ toggleTodo > 존재하지 않는 id는 배열을 그대로 반환한다
  ✓ toggleTodo > 원본 배열을 변경하지 않는다
  ✓ deleteTodo > 해당 id의 할 일을 제거한 새 배열을 반환한다
  ✓ deleteTodo > 원본 배열을 변경하지 않는다
  ✓ filterTodos > "all" 필터는 전체 배열을 반환한다
  ✓ filterTodos > "completed" 필터는 완료된 항목만 반환한다
  ✓ filterTodos > "active" 필터는 미완료 항목만 반환한다

Test Files  1 passed (1)
Tests       12 passed (12)
```

테스트가 모두 통과하면 핵심 로직이 올바르게 구현된 것입니다.

---

<a id="part5"></a>

## 5️⃣ ⭐ **핵심** — UI 연결하기 [↑](#toc)

> 강사 시연을 보면서 따라하세요

핵심 로직이 검증됐으니 이제 UI를 연결합니다. Copilot에게 DOM 연결 코드를 요청합니다.

### Copilot에게 요청하기

`src/app.js` 파일을 만들고 다음 주석을 작성하세요:

```javascript
// app.js
// todo.js의 순수 함수들을 HTML UI와 연결합니다.
// HTML 구조:
// - #todoForm: 폼
// - #todoInput: 텍스트 입력
// - #todoList: ul 목록
// - .filter-btn[data-filter]: 필터 버튼 (all, completed, active)
// - #counter: 완료/전체 개수 표시
//
// 기능: 추가, 완료 토글, 삭제, 필터링, 개수 표시

import { addTodo, toggleTodo, deleteTodo, filterTodos } from './todo.js';

// Copilot이 여기부터 생성합니다
```

### Copilot 생성 코드 예시

```javascript
// src/app.js (Copilot 생성)
import { addTodo, toggleTodo, deleteTodo, filterTodos } from './todo.js';

let todos = [];
let currentFilter = 'all';

function render() {
  const list = document.querySelector('#todoList');
  const counter = document.querySelector('#counter');

  if (!list || !counter) return;

  const filtered = filterTodos(todos, currentFilter);
  list.innerHTML = '';

  filtered.forEach((todo) => {
    const li = document.createElement('li');
    li.className = todo.completed ? 'completed' : '';

    li.innerHTML = `
      <span class="todo-text">${todo.text}</span>
      <button class="delete-btn" data-id="${todo.id}">삭제</button>
    `;

    li.querySelector('.todo-text').addEventListener('click', () => {
      todos = toggleTodo(todos, todo.id);
      render();
    });

    li.querySelector('.delete-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      todos = deleteTodo(todos, todo.id);
      render();
    });

    list.appendChild(li);
  });

  const completedCount = todos.filter((t) => t.completed).length;
  counter.textContent = `완료: ${completedCount} / 전체: ${todos.length}`;
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('#todoForm');
  const input = document.querySelector('#todoInput');
  const filterBtns = document.querySelectorAll('.filter-btn');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    todos = addTodo(todos, input.value);
    input.value = '';
    render();
  });

  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      currentFilter = btn.dataset.filter;

      filterBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');

      render();
    });
  });

  render();
});
```

### Bug Hunt 체크리스트 적용

이 코드에 09장에서 배운 체크리스트를 적용해보세요:

```
□ 실행되는가?
  → index.html을 브라우저에서 열어서 직접 확인하세요

□ 예상대로 동작하는가?
  → 추가, 토글, 삭제, 필터 각각 테스트해보세요
  → 빈 입력은 어떻게 처리되나요?

□ 모르는 메서드/문법이 있는가?
  → e.stopPropagation()이 무엇인지 찾아보세요 (힌트: 이벤트 버블링)
  → innerHTML에 todo.text를 직접 넣는 것이 안전한가요?

□ 보안 문제는 없는가?
  → li.innerHTML = `... ${todo.text} ...` 부분을 확인하세요
  → todo.text에 <script> 태그가 들어오면 어떻게 될까요?

□ 더 간단한 방법이 있는가?
  → render 함수가 하는 일이 명확한가요?
```

### 보안 문제 발견 및 수정

체크리스트에서 발견한 보안 문제를 수정해보세요:

```javascript
// 문제가 있는 코드
li.innerHTML = `
  <span class="todo-text">${todo.text}</span>
  <button class="delete-btn" data-id="${todo.id}">삭제</button>
`;

// 수정된 코드 — textContent 사용으로 XSS 방지
const span = document.createElement('span');
span.className = 'todo-text';
span.textContent = todo.text; // textContent는 HTML 태그를 문자 그대로 표시

const deleteBtn = document.createElement('button');
deleteBtn.className = 'delete-btn';
deleteBtn.dataset.id = todo.id;
deleteBtn.textContent = '삭제';

li.appendChild(span);
li.appendChild(deleteBtn);
```

---

<a id="part6"></a>

## 6️⃣ 🚀 **도전** — 검증하고 개선하기 [↑](#toc)

### 모든 테스트 다시 실행

코드를 수정했다면 테스트를 다시 실행해서 핵심 로직이 여전히 올바른지 확인합니다.

```bash
npm test
```

모든 테스트가 통과해야 합니다.

### 💪 **보너스 챌린지** — 엣지 케이스 테스트 추가

기본 테스트가 통과했다면 **예외 상황(엣지 케이스)**도 테스트해보세요.

```javascript
// tests/todo.test.js에 추가

describe('addTodo — 엣지 케이스', () => {
  it('매우 긴 텍스트도 추가할 수 있다', () => {
    const longText = 'a'.repeat(1000);
    const result = addTodo([], longText);
    expect(result[0].text).toBe(longText);
  });

  it('특수문자를 포함한 텍스트도 추가할 수 있다', () => {
    const result = addTodo([], '<script>alert("xss")</script>');
    expect(result[0].text).toBe('<script>alert("xss")</script>');
    // 텍스트로는 저장되어야 합니다 (렌더링 시 탈출 처리 필요)
  });

  it('여러 번 추가하면 id가 모두 다르다', () => {
    let todos = [];
    todos = addTodo(todos, '첫 번째');
    todos = addTodo(todos, '두 번째');
    todos = addTodo(todos, '세 번째');

    const ids = todos.map((t) => t.id);
    const uniqueIds = new Set(ids);
    expect(uniqueIds.size).toBe(3); // 모든 id가 고유해야 함
  });
});

describe('filterTodos — 엣지 케이스', () => {
  it('빈 배열에 필터를 적용하면 빈 배열을 반환한다', () => {
    expect(filterTodos([], 'all')).toEqual([]);
    expect(filterTodos([], 'completed')).toEqual([]);
    expect(filterTodos([], 'active')).toEqual([]);
  });

  it('알 수 없는 필터는 전체 배열을 반환한다', () => {
    const todos = [{ id: 1, text: '공부', completed: false }];
    expect(filterTodos(todos, 'unknown')).toHaveLength(1);
  });
});
```

### 최종 테스트 실행

```bash
npm test
```

```
✓ tests/todo.test.js (17 tests)

Test Files  1 passed (1)
Tests       17 passed (17)
```

---

<a id="part7"></a>

## 7️⃣ Phase 2 관문 — 자기 점검 [↑](#toc)

다음 4가지를 모두 체크할 수 있으면 Phase 3으로 진행합니다.

```
□ AI가 생성한 코드를 한 줄씩 설명할 수 있다
  → app.js의 각 함수를 보고 무엇을 하는지 설명해보세요
  → 설명이 안 되는 줄이 있다면 MDN에서 찾아보세요

□ AI 생성 코드에서 버그 2개 이상을 찾을 수 있다
  → 이 프로젝트에서 발견한 문제점을 기록해두세요
  → 09장 체크리스트를 app.js 전체에 적용해보세요

□ Vitest로 테스트를 작성하고 실행할 수 있다
  → todo.test.js가 12개 이상의 테스트를 통과해야 합니다
  → 엣지 케이스 테스트도 직접 작성했나요?

□ fetch로 외부 API 데이터를 가져올 수 있다
  → 10장의 기본/도전 과제를 완료했나요?
```

**위 4개를 모두 체크하면 Phase 3으로 진행합니다!**
{: .label .label-green }

### Phase 2 돌아보기

Phase 2에서 여러분이 배운 것:

| 08장 | DOM과 이벤트 | AI 생성 코드를 한 줄씩 읽고 설명하는 "Explain It Back" |
| 09장 | AI 출력 평가법 | AI 코드의 버그를 발견하는 체크리스트와 Bug Hunt |
| 10장 | 비동기 JavaScript | fetch, async/await, 테스트로 비동기 로직 검증 |
| 11장 | 미니 프로젝트 | 요구사항 → 테스트 → AI 구현 → 검증의 전체 흐름 |

---

<a id="part8"></a>

## 8️⃣ 정리 [↑](#toc)

Phase 2를 완주했습니다!

Phase 0-1에서 여러분은 "코드가 무엇인지, 어떻게 쓰는지"를 배웠습니다.
Phase 2에서는 "AI가 만든 코드를 읽고, 평가하고, 고치는 방법"을 배웠습니다.

이 능력은 AI 시대의 개발자에게 가장 중요한 역량 중 하나입니다. AI는 빠르게 초안을 만들지만, 그 초안이 올바른지 판단하는 것은 언제나 사람의 몫입니다.

### 완료한 것들

- 브라우저에서 동작하는 ToDo 앱 완성
- 핵심 로직을 순수 함수로 분리하고 테스트 작성
- AI가 생성한 DOM 코드 검증 및 보안 문제 수정
- 12개 이상의 Vitest 테스트 작성 및 통과

### 다음 장 미리보기

**Phase 3: AI-Native 개발**

이제부터는 AI를 단순한 코드 생성기가 아닌 **진정한 협업 파트너**로 활용합니다.

```
12장: Custom Instructions — AI에게 프로젝트 규칙 알려주기
13장: Prompt Files + Context Engineering — 반복 작업 템플릿
14장: TDD + AI 에이전트 — 테스트 먼저, AI가 구현
15장: 통합 프로젝트: 날씨 앱 — 전체 AI-Native 파이프라인
```

Phase 3에서는 여러분이 **설계**하고, AI가 **구현**하고, 테스트로 **검증**하는 완전한 AI-Native 워크플로우를 경험하게 됩니다.

---

*Phase 2를 완주한 것을 축하합니다. 이제 AI와 함께 진짜 개발을 시작할 준비가 됐습니다.*


→ **다음 내용으로 넘어갑시다**: [12. Custom Instructions](/ai-native-js/instructions)
