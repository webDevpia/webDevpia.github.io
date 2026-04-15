---
title: 12. 미니 프로젝트 — ToDo 앱
layout: default
parent: React (리뉴얼)
nav_order: 13
permalink: /language/react-new/todo-app
---

{% raw %}

# 12장. 미니 프로젝트 — ToDo 앱

## 학습 목표

- 지금까지 배운 모든 개념(컴포넌트, props, state, 이벤트, 폼, 리스트, 조건부 렌더링, Lifting State)을 하나의 앱으로 통합한다
- 실제 프로젝트처럼 컴포넌트 트리를 설계하고 구현한다
- 추가, 완료 토글, 삭제, 필터 기능을 단계별로 완성한다
- Tailwind CSS로 완성도 높은 UI를 만든다

---

<a id="toc"></a>

## 진행 순서

1. [프로젝트 소개](#1)
2. [프로젝트 구조 설계](#2)
3. [Step 1: TodoForm — 할 일 추가](#3)
4. [Step 2: TodoList + TodoItem — 목록 렌더링](#4)
5. [Step 3: 완료 토글](#5)
6. [Step 4: 삭제](#6)
7. [Step 5: 필터](#7)
8. [Step 6: 스타일링 완성](#8)
9. [완성 코드 전체](#9)
10. [도전 과제](#10)
11. [정리 + 브릿지](#11)

---

<a id="1"></a>
## 1️⃣ 프로젝트 소개 [↑](#toc)

### 무엇을 만드는가

할 일 관리 앱(ToDo App)은 모든 프레임워크 학습의 전통적인 통합 프로젝트입니다. 간단해 보이지만, 실제 앱에 필요한 **상태 관리, 사용자 입력, 목록 렌더링, 이벤트 처리**가 모두 담겨 있습니다.

### 최종 완성 모습

```
┌─────────────────────────────────────┐
│          나의 할 일 목록              │
│                                     │
│  [할 일을 입력하세요...      ] [추가] │
│                                     │
│  [전체] [진행중] [완료]              │
│                                     │
│  ☐  React 공부하기          [삭제]  │
│  ☑  운동하기                [삭제]  │
│  ☐  책 읽기                 [삭제]  │
│                                     │
│  총 3개 중 1개 완료                  │
└─────────────────────────────────────┘
```

### 구현할 기능

| 기능 | 관련 개념 |
|------|----------|
| 할 일 입력 및 추가 | 폼, controlled input, 배열 상태 |
| 목록 렌더링 | map, key |
| 완료 토글 | 객체 배열 업데이트, map + spread |
| 삭제 | filter |
| 필터 (전체/진행중/완료) | Lifting State, 조건부 렌더링 |
| 스타일링 | Tailwind CSS |

---

<a id="2"></a>
## 2️⃣ 프로젝트 구조 설계 [↑](#toc)

코드를 짜기 전에 **무엇을 어디에 둘지** 먼저 설계합니다. 이것이 실력 있는 개발자와 그렇지 않은 개발자의 차이입니다.

### 컴포넌트 트리

```
App
├── TodoForm         (할 일 추가 입력창)
├── FilterButtons    (전체/진행중/완료 필터)
└── TodoList
    └── TodoItem     (개별 할 일 항목)
```

### 상태 설계

어떤 상태가 필요하고, 어디에 두어야 할까요?

| 상태 | 타입 | 위치 | 이유 |
|------|------|------|------|
| `todos` | `Array` | `App` | TodoList, FilterButtons 모두 필요 |
| `filter` | `string` | `App` | FilterButtons가 변경, TodoList가 사용 |

```jsx
// App의 상태
const [todos, setTodos] = useState([]);
const [filter, setFilter] = useState('all'); // 'all' | 'active' | 'done'
```

### 데이터 구조

개별 todo 항목은 어떤 모양일까요?

```js
{
  id: 1,        // 고유 식별자 (Date.now() 사용)
  text: '리액트 공부하기', // 내용
  done: false,  // 완료 여부
}
```

---

<a id="3"></a>
## 3️⃣ Step 1: TodoForm — 할 일 추가 [↑](#toc)

새 프로젝트를 만들고 시작합니다.

```bash
npm create vite@latest todo-app -- --template react
cd todo-app
npm install
npm install -D tailwindcss @tailwindcss/vite
```

`vite.config.js`에 Tailwind 플러그인을 추가하고, `index.css`에 `@import "tailwindcss";`를 입력합니다.

이제 `TodoForm` 컴포넌트를 만듭니다.

```jsx
// src/components/TodoForm.jsx
import { useState } from 'react';

function TodoForm({ onAdd }) {
  const [text, setText] = useState('');

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed) return; // 빈 입력 무시
    onAdd(trimmed);
    setText(''); // 입력창 초기화
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mb-6">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="할 일을 입력하세요..."
        className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        type="submit"
        className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium transition-colors"
      >
        추가
      </button>
    </form>
  );
}

export default TodoForm;
```

App에서 `onAdd` 핸들러를 만들어 연결합니다.

```jsx
// src/App.jsx
import { useState } from 'react';
import TodoForm from './components/TodoForm';

function App() {
  const [todos, setTodos] = useState([]);

  function handleAdd(text) {
    const newTodo = {
      id: Date.now(),
      text,
      done: false,
    };
    setTodos((prev) => [...prev, newTodo]);
  }

  return (
    <div className="min-h-screen bg-gray-50 py-10">
      <div className="max-w-md mx-auto bg-white rounded-2xl shadow-lg p-6">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">
          나의 할 일 목록
        </h1>
        <TodoForm onAdd={handleAdd} />
        {/* 다음 단계에서 추가 예정 */}
      </div>
    </div>
  );
}

export default App;
```

---

<a id="4"></a>
## 4️⃣ Step 2: TodoList + TodoItem — 목록 렌더링 [↑](#toc)

```jsx
// src/components/TodoItem.jsx
function TodoItem({ todo, onToggle, onDelete }) {
  return (
    <li className="flex items-center gap-3 p-3 border-b border-gray-100 last:border-0 group">
      <input
        type="checkbox"
        checked={todo.done}
        onChange={() => onToggle(todo.id)}
        className="w-5 h-5 accent-blue-500 cursor-pointer"
      />
      <span
        className={`flex-1 ${
          todo.done ? 'line-through text-gray-400' : 'text-gray-700'
        }`}
      >
        {todo.text}
      </span>
      <button
        onClick={() => onDelete(todo.id)}
        className="text-gray-300 hover:text-red-400 transition-colors opacity-0 group-hover:opacity-100"
      >
        삭제
      </button>
    </li>
  );
}

export default TodoItem;
```

```jsx
// src/components/TodoList.jsx
import TodoItem from './TodoItem';

function TodoList({ todos, onToggle, onDelete }) {
  if (todos.length === 0) {
    return (
      <p className="text-center text-gray-400 py-8">
        할 일이 없습니다. 추가해 보세요!
      </p>
    );
  }

  return (
    <ul className="border border-gray-100 rounded-lg overflow-hidden">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
}

export default TodoList;
```

---

<a id="5"></a>
## 5️⃣ Step 3: 완료 토글 [↑](#toc)

`done` 속성을 뒤집어야 합니다. **배열을 직접 수정하지 않고** `map`과 스프레드 연산자로 새 배열을 만듭니다.

```jsx
// App.jsx에 추가
function handleToggle(id) {
  setTodos((prev) =>
    prev.map((todo) =>
      todo.id === id
        ? { ...todo, done: !todo.done } // 해당 항목만 done 반전
        : todo                           // 나머지는 그대로
    )
  );
}
```

**왜 이렇게 하는가?**

```js
// ❌ 직접 수정 (React가 변경을 감지 못함)
todos[0].done = true;
setTodos(todos);

// ✅ 새 배열 생성 (React가 변경을 감지함)
setTodos(prev => prev.map(todo =>
  todo.id === id ? { ...todo, done: true } : todo
));
```

---

<a id="6"></a>
## 6️⃣ Step 4: 삭제 [↑](#toc)

해당 id를 제외한 새 배열을 `filter`로 만듭니다.

```jsx
// App.jsx에 추가
function handleDelete(id) {
  setTodos((prev) => prev.filter((todo) => todo.id !== id));
}
```

`filter`는 조건을 만족하는 항목만 남긴 새 배열을 반환합니다. `id !== id`이므로 삭제 대상은 제외됩니다.

---

<a id="7"></a>
## 7️⃣ Step 5: 필터 [↑](#toc)

`filter` 상태를 App에 추가하고 (Lifting State 적용), `FilterButtons`와 `TodoList`가 공유합니다.

```jsx
// src/components/FilterButtons.jsx
const FILTERS = [
  { value: 'all', label: '전체' },
  { value: 'active', label: '진행중' },
  { value: 'done', label: '완료' },
];

function FilterButtons({ current, onChange }) {
  return (
    <div className="flex gap-2 mb-4">
      {FILTERS.map(({ value, label }) => (
        <button
          key={value}
          onClick={() => onChange(value)}
          className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
            current === value
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          {label}
        </button>
      ))}
    </div>
  );
}

export default FilterButtons;
```

App에서 필터링 로직을 처리합니다.

```jsx
// App.jsx에 추가
const [filter, setFilter] = useState('all');

const filteredTodos = todos.filter((todo) => {
  if (filter === 'active') return !todo.done;
  if (filter === 'done') return todo.done;
  return true; // 'all'
});

// JSX
<FilterButtons current={filter} onChange={setFilter} />
<TodoList todos={filteredTodos} onToggle={handleToggle} onDelete={handleDelete} />
```

---

<a id="8"></a>
## 8️⃣ Step 6: 스타일링 완성 [↑](#toc)

통계 정보와 완성도 높은 UI를 추가합니다.

```jsx
// App.jsx 하단에 통계 추가
const doneCount = todos.filter((t) => t.done).length;
const totalCount = todos.length;

// JSX
{totalCount > 0 && (
  <div className="mt-4 pt-4 border-t border-gray-100">
    <p className="text-sm text-gray-400 text-center">
      총 {totalCount}개 중{' '}
      <span className="text-blue-500 font-medium">{doneCount}개</span> 완료
    </p>
    <div className="mt-2 h-1.5 bg-gray-100 rounded-full overflow-hidden">
      <div
        className="h-full bg-blue-400 rounded-full transition-all duration-300"
        style={{ width: `${(doneCount / totalCount) * 100}%` }}
      />
    </div>
  </div>
)}
```

---

<a id="9"></a>
## 9️⃣ 완성 코드 전체 [↑](#toc)

```jsx
// src/App.jsx — 완성본
import { useState } from 'react';
import TodoForm from './components/TodoForm';
import FilterButtons from './components/FilterButtons';
import TodoList from './components/TodoList';

function App() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'React 공부하기', done: false },
    { id: 2, text: '운동하기', done: true },
  ]);
  const [filter, setFilter] = useState('all');

  function handleAdd(text) {
    setTodos((prev) => [
      ...prev,
      { id: Date.now(), text, done: false },
    ]);
  }

  function handleToggle(id) {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, done: !todo.done } : todo
      )
    );
  }

  function handleDelete(id) {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  }

  const filteredTodos = todos.filter((todo) => {
    if (filter === 'active') return !todo.done;
    if (filter === 'done') return todo.done;
    return true;
  });

  const doneCount = todos.filter((t) => t.done).length;
  const totalCount = todos.length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 py-10">
      <div className="max-w-md mx-auto bg-white rounded-2xl shadow-lg p-6">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">
          📋 나의 할 일 목록
        </h1>

        <TodoForm onAdd={handleAdd} />
        <FilterButtons current={filter} onChange={setFilter} />
        <TodoList
          todos={filteredTodos}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />

        {totalCount > 0 && (
          <div className="mt-4 pt-4 border-t border-gray-100">
            <p className="text-sm text-gray-400 text-center">
              총 {totalCount}개 중{' '}
              <span className="text-blue-500 font-medium">{doneCount}개</span>{' '}
              완료
            </p>
            <div className="mt-2 h-1.5 bg-gray-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-400 rounded-full transition-all duration-300"
                style={{ width: `${(doneCount / totalCount) * 100}%` }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
```

---

<a id="10"></a>
## 🔟 도전 과제 [↑](#toc)

### 기본 도전

1. **빈 목록 메시지 개선:** 필터별로 다른 안내 메시지 표시
   - 전체(빈 목록): "할 일을 추가해 보세요!"
   - 진행중(없음): "모든 할 일을 완료했습니다! 🎉"
   - 완료(없음): "아직 완료한 항목이 없습니다."

2. **완료 항목 일괄 삭제:** "완료 항목 삭제" 버튼 추가

### 고급 도전

3. **할 일 텍스트 수정:** 항목을 더블클릭하면 인라인 편집 가능
4. **드래그로 순서 변경:** HTML5 드래그 앤 드롭 API 활용
5. **localStorage 저장 (미리보기):**

```jsx
// 지금은 이렇게만 봐두세요 — 다음 파트에서 배웁니다
useEffect(() => {
  localStorage.setItem('todos', JSON.stringify(todos));
}, [todos]);
```

---

<a id="11"></a>
## 정리 + 브릿지 [↑](#toc)

### 이번 장에서 만든 것

| 기능 | 사용한 기술 |
|------|------------|
| 할 일 추가 | controlled input, 배열 spread |
| 목록 렌더링 | map, key |
| 완료 토글 | map + 객체 spread |
| 삭제 | filter |
| 필터링 | Lifting State, 조건부 렌더링 |
| 진행 바 | 파생 값 계산, inline style |

### Part 3가 끝났습니다

지금까지 React의 가장 핵심적인 개념들을 모두 익혔습니다. 컴포넌트, props, state, 이벤트, 폼, 리스트, 조건부 렌더링, 그리고 컴포넌트 간 데이터 공유까지.

하지만 지금 만든 앱에는 한 가지 문제가 있습니다. **새로고침하면 데이터가 사라집니다.**

다음 파트에서는 `useEffect`를 배워 타이머를 관리하고, API와 통신하고, 데이터를 localStorage에 저장하는 방법을 익힙니다. React가 렌더링 바깥 세계와 대화하는 방법을 배울 시간입니다!

{% endraw %}
