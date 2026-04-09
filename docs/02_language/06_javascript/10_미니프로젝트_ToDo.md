---
title: 10. 미니 프로젝트 - To-Do 앱
layout: default
grand_parent: Language
parent: JavaScript
nav_order: 10
permalink: /language/javascript/todo-project
---


## 학습 목표

- 1~9장에서 배운 개념을 하나의 프로젝트에 통합하여 실습할 수 있다
- HTML+CSS+JavaScript로 동작하는 웹 앱을 완성할 수 있다

<a id="toc"></a>

## 진행 순서

1. [프로젝트 개요](#part1) - 어떤 앱을 만드는지, 1~9장 개념 매핑
2. [HTML 구조](#part2) - 기본 마크업 작성
3. [CSS 스타일](#part3) - 레이아웃과 완료 표시 스타일
4. [JavaScript 핵심 로직](#part4) - 단계별 함수 구현
5. [전체 코드](#part5) - 복사해서 바로 실행 가능한 완성본
6. [정리](#part6) - 핵심 개념 총정리 및 실습 과제

---

# 10장. 미니 프로젝트 - To-Do 앱

<a id="part1"></a>

## 1️⃣ 프로젝트 개요 [↑](#toc)

### 만들 앱 소개

> 할 일을 **추가·완료·삭제**하는 To-Do 앱을 만들어 봅니다.
> 입력창에 할 일을 적고 Enter를 누르면 목록에 추가되고,
> 항목을 클릭하면 완료(취소선), 삭제 버튼을 누르면 목록에서 지워집니다.
> 하단에는 남은 할 일 개수가 실시간으로 표시됩니다.

```
┌─────────────────────────────────────┐
│          📝 To-Do 앱                 │
│  ┌──────────────────────┐ [추가]     │
│  │ 할 일을 입력하세요    │            │
│  └──────────────────────┘            │
│                                      │
│  ○ 자바스크립트 공부하기   [삭제]    │
│  ✓ ~~운동하기~~            [삭제]    │
│  ○ 책 읽기                 [삭제]    │
│                                      │
│  남은 할 일: 2개                     │
└─────────────────────────────────────┘
```

### 1~9장 개념 매핑 표

| 기능 | 사용 개념 | 해당 장 |
|------|-----------|---------|
| 할 일 데이터 저장 | 배열, 객체 | 4장, 7장 |
| 추가/삭제 버튼 | 이벤트 리스너, DOM 조작 | 9장 |
| 완료 표시 (취소선) | `classList.toggle` | 9장 |
| 입력값 검증 | 조건문, 문자열 메서드 | 3장, 2장 |
| 남은 할 일 개수 | 배열 `filter`, 템플릿 리터럴 | 7장, 2장 |
| 함수 분리 | 함수 선언, 매개변수 | 5장 |
| 고유 ID 생성 | `Date.now()`, 변수 | 2장 |

---

<a id="part2"></a>

## 2️⃣ HTML 구조 [↑](#toc)

### 파일 구조

이 장은 `todo.html` **한 파일**에 HTML·CSS·JS를 모두 작성합니다.
VSCode에서 `todo.html`을 만들고 **Live Server**로 실행하거나, 브라우저에 파일을 직접 열어도 됩니다.

### 기본 마크업

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>To-Do 앱</title>
  <!-- CSS는 3️⃣ 섹션에서 추가 -->
</head>
<body>

  <div class="container">
    <h1>📝 To-Do 앱</h1>

    <!-- 입력 영역 -->
    <div class="input-area">
      <input
        type="text"
        id="todo-input"
        placeholder="할 일을 입력하세요"
      />
      <button id="add-btn">추가</button>
    </div>

    <!-- 할 일 목록 -->
    <ul id="todo-list"></ul>

    <!-- 하단 요약 -->
    <footer id="footer">남은 할 일: 0개</footer>
  </div>

  <!-- JS는 4️⃣ 섹션에서 추가 -->
</body>
</html>
```

### 주요 요소 설명

| 요소 | id | 역할 |
|------|----|------|
| `<input>` | `todo-input` | 할 일 텍스트 입력 |
| `<button>` | `add-btn` | 추가 버튼 |
| `<ul>` | `todo-list` | 할 일 목록 컨테이너 |
| `<footer>` | `footer` | 남은 할 일 개수 표시 |

---

<a id="part3"></a>

## 3️⃣ CSS 스타일 [↑](#toc)

`<head>` 안에 `<style>` 태그를 추가합니다.

```html
<style>
  /* 전체 레이아웃 — 중앙 정렬 */
  body {
    font-family: 'Segoe UI', sans-serif;
    background: #f0f4f8;
    display: flex;
    justify-content: center;
    padding: 40px 16px;
    margin: 0;
  }

  .container {
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    padding: 32px;
    width: 100%;
    max-width: 480px;
  }

  h1 {
    margin: 0 0 24px;
    font-size: 1.6rem;
    color: #2d3748;
    text-align: center;
  }

  /* 입력 영역 */
  .input-area {
    display: flex;
    gap: 8px;
    margin-bottom: 24px;
  }

  #todo-input {
    flex: 1;
    padding: 10px 14px;
    border: 2px solid #cbd5e0;
    border-radius: 8px;
    font-size: 1rem;
    outline: none;
    transition: border-color 0.2s;
  }

  #todo-input:focus {
    border-color: #667eea;
  }

  #add-btn {
    padding: 10px 18px;
    background: #667eea;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.2s;
  }

  #add-btn:hover {
    background: #5a67d8;
  }

  /* 할 일 목록 */
  #todo-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  #todo-list li {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 14px;
    border-radius: 8px;
    margin-bottom: 8px;
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    transition: background 0.15s;
  }

  #todo-list li:hover {
    background: #edf2f7;
  }

  /* 할 일 텍스트 — 클릭 가능 */
  .todo-text {
    flex: 1;
    font-size: 1rem;
    color: #2d3748;
    cursor: pointer;
    user-select: none;
  }

  /* 완료 상태 — 취소선 (9장 classList.toggle) */
  .todo-text.completed {
    text-decoration: line-through;
    color: #a0aec0;
  }

  /* 삭제 버튼 — 빨간색 */
  .delete-btn {
    padding: 4px 10px;
    background: #fc8181;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: background 0.2s;
  }

  .delete-btn:hover {
    background: #e53e3e;
  }

  /* 하단 요약 */
  #footer {
    margin-top: 20px;
    text-align: right;
    font-size: 0.9rem;
    color: #718096;
  }
</style>
```

---

<a id="part4"></a>

## 4️⃣ JavaScript 핵심 로직 [↑](#toc)

`</body>` 바로 앞에 `<script>` 태그를 추가합니다.
각 함수마다 **어느 장에서 배운 개념인지 주석**을 달아 두었습니다.

### 4-1. 데이터: todos 배열

```javascript
// [4장 배열] [7장 객체 배열]
// 각 할 일은 { id, text, completed } 형태의 객체입니다.
let todos = [];
```

| 프로퍼티 | 타입 | 설명 |
|----------|------|------|
| `id` | number | 고유 식별자 (`Date.now()` 사용) |
| `text` | string | 할 일 내용 |
| `completed` | boolean | 완료 여부 |

### 4-2. renderTodos() — 화면 다시 그리기

```javascript
// [9장 DOM 조작] [7장 배열 메서드] [2장 템플릿 리터럴]
// todos 배열을 기준으로 <ul> 목록을 처음부터 다시 그립니다.
function renderTodos() {
  const list = document.getElementById('todo-list');

  // 기존 목록을 지우고 새로 그립니다 (9장 innerHTML)
  list.innerHTML = '';

  // [4장 반복문] todos 배열을 순회하며 <li> 요소를 생성합니다
  todos.forEach(function(todo) {
    const li = document.createElement('li'); // 9장 createElement

    // [2장 템플릿 리터럴] 완료 여부에 따라 클래스를 다르게 줍니다
    li.innerHTML = `
      <span
        class="todo-text ${todo.completed ? 'completed' : ''}"
        onclick="toggleTodo(${todo.id})"
      >${todo.text}</span>
      <button class="delete-btn" onclick="deleteTodo(${todo.id})">삭제</button>
    `;

    list.appendChild(li); // 9장 appendChild
  });

  // [7장 filter] [2장 템플릿 리터럴] 남은 할 일 개수를 계산해서 표시합니다
  const remaining = todos.filter(function(todo) {
    return !todo.completed;
  }).length;

  document.getElementById('footer').textContent = `남은 할 일: ${remaining}개`;
}
```

> `renderTodos()`는 매번 목록을 처음부터 다시 그립니다.
> 이 "상태 → 화면 반영" 패턴은 React 등 현대 프레임워크의 핵심 원리이기도 합니다.

### 4-3. addTodo() — 할 일 추가

```javascript
// [3장 조건문] [2장 문자열 메서드] [4장 배열 push]
// 입력값을 검증하고 todos 배열에 새 객체를 추가합니다.
function addTodo() {
  const input = document.getElementById('todo-input');
  const text = input.value.trim(); // 2장: 앞뒤 공백 제거

  // [3장 조건문] 빈 문자열이면 추가하지 않습니다
  if (text === '') {
    alert('할 일을 입력해 주세요!');
    return;
  }

  // [7장 객체] 새 할 일 객체를 만들고 배열에 추가합니다
  const newTodo = {
    id: Date.now(),    // 2장: 고유 숫자 ID
    text: text,        // 입력한 텍스트
    completed: false   // 처음에는 미완료 상태
  };

  todos.push(newTodo); // 4장: 배열 맨 뒤에 추가

  input.value = '';    // 입력창 초기화
  input.focus();       // 커서를 다시 입력창으로

  renderTodos(); // 변경된 배열로 화면을 다시 그립니다
}
```

### 4-4. toggleTodo(id) — 완료 상태 전환

```javascript
// [7장 배열 find] [9장 classList] [3장 논리 연산자]
// 클릭한 할 일의 completed 값을 true ↔ false로 전환합니다.
function toggleTodo(id) {
  // [7장 find] id가 일치하는 객체를 찾습니다
  const todo = todos.find(function(t) {
    return t.id === id;
  });

  if (todo) {
    // [3장 논리 NOT 연산자] true이면 false, false이면 true
    todo.completed = !todo.completed;
  }

  renderTodos();
}
```

### 4-5. deleteTodo(id) — 할 일 삭제

```javascript
// [7장 배열 filter] 클릭한 할 일을 배열에서 제거합니다.
function deleteTodo(id) {
  // filter: id가 다른 항목만 남기면 해당 항목이 삭제됩니다 (7장)
  todos = todos.filter(function(t) {
    return t.id !== id;
  });

  renderTodos();
}
```

### 4-6. 이벤트 리스너 등록

```javascript
// [9장 이벤트 리스너]
// 페이지가 로드된 뒤 버튼과 Enter 키 이벤트를 등록합니다.
document.addEventListener('DOMContentLoaded', function() {

  // "추가" 버튼 클릭 시 addTodo() 실행
  document.getElementById('add-btn').addEventListener('click', addTodo);

  // 입력창에서 Enter 키를 누르면 addTodo() 실행 (9장 keydown 이벤트)
  document.getElementById('todo-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      addTodo();
    }
  });

  // 초기 화면 렌더링
  renderTodos();
});
```

---

<a id="part5"></a>

## 5️⃣ 전체 코드 [↑](#toc)

아래 코드를 `todo.html`로 저장하고 브라우저에서 열면 바로 실행됩니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>To-Do 앱</title>
  <style>
    /* 전체 레이아웃 — 중앙 정렬 */
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #f0f4f8;
      display: flex;
      justify-content: center;
      padding: 40px 16px;
      margin: 0;
    }

    .container {
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
      padding: 32px;
      width: 100%;
      max-width: 480px;
    }

    h1 {
      margin: 0 0 24px;
      font-size: 1.6rem;
      color: #2d3748;
      text-align: center;
    }

    /* 입력 영역 */
    .input-area {
      display: flex;
      gap: 8px;
      margin-bottom: 24px;
    }

    #todo-input {
      flex: 1;
      padding: 10px 14px;
      border: 2px solid #cbd5e0;
      border-radius: 8px;
      font-size: 1rem;
      outline: none;
      transition: border-color 0.2s;
    }

    #todo-input:focus {
      border-color: #667eea;
    }

    #add-btn {
      padding: 10px 18px;
      background: #667eea;
      color: #fff;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      cursor: pointer;
      transition: background 0.2s;
    }

    #add-btn:hover {
      background: #5a67d8;
    }

    /* 할 일 목록 */
    #todo-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }

    #todo-list li {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 12px 14px;
      border-radius: 8px;
      margin-bottom: 8px;
      background: #f7fafc;
      border: 1px solid #e2e8f0;
      transition: background 0.15s;
    }

    #todo-list li:hover {
      background: #edf2f7;
    }

    /* 할 일 텍스트 */
    .todo-text {
      flex: 1;
      font-size: 1rem;
      color: #2d3748;
      cursor: pointer;
      user-select: none;
    }

    /* 완료 상태 — 취소선 */
    .todo-text.completed {
      text-decoration: line-through;
      color: #a0aec0;
    }

    /* 삭제 버튼 — 빨간색 */
    .delete-btn {
      padding: 4px 10px;
      background: #fc8181;
      color: #fff;
      border: none;
      border-radius: 6px;
      font-size: 0.85rem;
      cursor: pointer;
      transition: background 0.2s;
    }

    .delete-btn:hover {
      background: #e53e3e;
    }

    /* 하단 요약 */
    #footer {
      margin-top: 20px;
      text-align: right;
      font-size: 0.9rem;
      color: #718096;
    }
  </style>
</head>
<body>

  <div class="container">
    <h1>📝 To-Do 앱</h1>

    <div class="input-area">
      <input
        type="text"
        id="todo-input"
        placeholder="할 일을 입력하세요"
      />
      <button id="add-btn">추가</button>
    </div>

    <ul id="todo-list"></ul>

    <footer id="footer">남은 할 일: 0개</footer>
  </div>

  <script>
    // ─────────────────────────────────────────
    // [4장 배열] [7장 객체 배열]
    // todos: 할 일 목록을 저장하는 배열
    // 각 항목은 { id, text, completed } 객체입니다.
    // ─────────────────────────────────────────
    let todos = [];

    // ─────────────────────────────────────────
    // renderTodos() — 화면 다시 그리기
    // [9장 DOM 조작] [7장 배열 메서드] [2장 템플릿 리터럴]
    // ─────────────────────────────────────────
    function renderTodos() {
      const list = document.getElementById('todo-list');
      list.innerHTML = ''; // 기존 목록 초기화 (9장 innerHTML)

      // [4장 반복문] 배열을 순회하며 <li> 요소를 생성합니다
      todos.forEach(function(todo) {
        const li = document.createElement('li'); // 9장 createElement

        // [2장 템플릿 리터럴] 완료 여부에 따라 클래스 적용
        li.innerHTML = `
          <span
            class="todo-text ${todo.completed ? 'completed' : ''}"
            onclick="toggleTodo(${todo.id})"
          >${todo.text}</span>
          <button class="delete-btn" onclick="deleteTodo(${todo.id})">삭제</button>
        `;

        list.appendChild(li); // 9장 appendChild
      });

      // [7장 filter] [2장 템플릿 리터럴] 남은 할 일 개수 계산
      const remaining = todos.filter(function(todo) {
        return !todo.completed;
      }).length;

      document.getElementById('footer').textContent = `남은 할 일: ${remaining}개`;
    }

    // ─────────────────────────────────────────
    // addTodo() — 할 일 추가
    // [3장 조건문] [2장 문자열 메서드] [4장 배열 push]
    // ─────────────────────────────────────────
    function addTodo() {
      const input = document.getElementById('todo-input');
      const text = input.value.trim(); // 2장: 앞뒤 공백 제거

      // [3장 조건문] 빈 문자열 검증
      if (text === '') {
        alert('할 일을 입력해 주세요!');
        return;
      }

      // [7장 객체] 새 할 일 객체 생성
      const newTodo = {
        id: Date.now(),  // 2장: 고유 숫자 ID
        text: text,
        completed: false
      };

      todos.push(newTodo); // 4장: 배열에 추가

      input.value = '';
      input.focus();

      renderTodos();
    }

    // ─────────────────────────────────────────
    // toggleTodo(id) — 완료 상태 전환
    // [7장 배열 find] [3장 논리 NOT 연산자]
    // ─────────────────────────────────────────
    function toggleTodo(id) {
      // [7장 find] id가 일치하는 객체를 찾습니다
      const todo = todos.find(function(t) {
        return t.id === id;
      });

      if (todo) {
        // [3장 논리 NOT] true ↔ false 전환
        todo.completed = !todo.completed;
      }

      renderTodos();
    }

    // ─────────────────────────────────────────
    // deleteTodo(id) — 할 일 삭제
    // [7장 배열 filter]
    // ─────────────────────────────────────────
    function deleteTodo(id) {
      // id가 다른 항목만 남기면 해당 항목이 삭제됩니다
      todos = todos.filter(function(t) {
        return t.id !== id;
      });

      renderTodos();
    }

    // ─────────────────────────────────────────
    // 이벤트 리스너 등록
    // [9장 addEventListener] [9장 keydown 이벤트]
    // ─────────────────────────────────────────
    document.addEventListener('DOMContentLoaded', function() {

      // "추가" 버튼 클릭
      document.getElementById('add-btn').addEventListener('click', addTodo);

      // Enter 키로 추가
      document.getElementById('todo-input').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
          addTodo();
        }
      });

      renderTodos(); // 초기 화면 렌더링
    });
  </script>

</body>
</html>
```

### 실행 결과 (화면 텍스트)

"자바스크립트 공부하기"를 추가하고, "운동하기"를 추가한 뒤 완료로 표시하면:

```
┌─────────────────────────────────────┐
│          📝 To-Do 앱                 │
│  ┌──────────────────────┐ [추가]     │
│  │                      │            │
│  └──────────────────────┘            │
│                                      │
│  자바스크립트 공부하기       [삭제]  │
│  ~~운동하기~~                [삭제]  │
│                                      │
│                      남은 할 일: 1개 │
└─────────────────────────────────────┘
```

---

<a id="part6"></a>

## 6️⃣ 정리 [↑](#toc)

### 사용한 개념 총정리

| 함수/기능 | 핵심 개념 | 장 |
|-----------|-----------|-----|
| `todos` 배열 선언 | 배열, 객체 리터럴 | 4장, 7장 |
| `addTodo()` 검증 | `trim()`, 조건문, `return` | 2장, 3장, 5장 |
| `todos.push()` | 배열 추가 메서드 | 4장 |
| `renderTodos()` 순회 | `forEach` 반복 | 4장 |
| 취소선 표시 | 삼항 연산자, `classList` | 3장, 9장 |
| `toggleTodo()` | `find`, 논리 NOT `!` | 7장, 3장 |
| `deleteTodo()` | `filter` | 7장 |
| `remaining` 계산 | `filter`, 템플릿 리터럴 | 7장, 2장 |
| 버튼·Enter 이벤트 | `addEventListener`, `keydown` | 9장 |
| DOM 업데이트 | `innerHTML`, `createElement`, `appendChild` | 9장 |

### 다음 장 미리보기 — 11장 비동기 프로그래밍

지금 만든 To-Do 앱은 모든 데이터가 **메모리(변수)**에만 있습니다.
새로고침하면 데이터가 사라지고, 서버에서 데이터를 받아오려면 **기다려야** 합니다.
11장에서는 이 문제를 해결하는 **비동기(async/await)** 와 **`fetch` API**를 배웁니다.

```
10장 (지금)          11장 (다음)
─────────────        ──────────────────────────
메모리에 저장   →    서버·파일에서 가져오기
동기 실행       →    비동기 (async/await)
새로고침 시 삭제 →   fetch + localStorage로 유지
```

### 실습 과제 3단계

**기본** — 앱을 실행하고 할 일 5개를 추가·완료·삭제해 보세요.

```
목표: 앱이 정상 동작하는지 직접 확인하기
확인 포인트:
  - 추가 버튼과 Enter 키 모두 동작하는가?
  - 빈 칸 입력 시 알림이 뜨는가?
  - 완료 클릭 시 취소선이 생기는가?
  - 남은 할 일 개수가 정확히 바뀌는가?
```

**중급** — "전체 삭제" 버튼을 추가해 보세요.

```html
<!-- footer 위에 추가 -->
<button id="clear-btn">전체 삭제</button>
```

```javascript
// 힌트: todos 배열을 빈 배열로 초기화하면 됩니다
document.getElementById('clear-btn').addEventListener('click', function() {
  // 여기에 코드를 작성하세요
});
```

**심화** — `localStorage`로 새로고침 후에도 데이터를 유지해 보세요.

```javascript
// 힌트 1: 저장 — todos 배열을 문자열로 변환해서 저장합니다
localStorage.setItem('todos', JSON.stringify(todos));

// 힌트 2: 불러오기 — 페이지 로드 시 저장된 데이터를 읽습니다
const saved = localStorage.getItem('todos');
if (saved) {
  todos = JSON.parse(saved);
}

// addTodo(), toggleTodo(), deleteTodo() 안에서
// renderTodos() 호출 직전에 힌트 1 코드를 넣어 보세요.
// DOMContentLoaded 안에서 힌트 2 코드를 넣어 보세요.
```

---

> **수고하셨습니다!**
> 1장부터 9장까지 배운 개념이 하나의 앱으로 합쳐졌습니다.
> 다음 장에서는 **비동기 프로그래밍**으로 더 넓은 세계를 탐험합니다.
