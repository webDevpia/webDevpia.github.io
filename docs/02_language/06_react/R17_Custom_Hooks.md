---
title: 16. Custom Hooks — 로직 재사용
layout: default
parent: React
nav_order: 17
permalink: /language/react/custom-hooks
---

{% raw %}

# 16장. Custom Hooks — 로직 재사용

## 학습 목표

- Custom Hook이 왜 필요한지 이해한다
- `use`로 시작하는 함수에서 다른 Hook을 조합하는 패턴을 익힌다
- `useToggle`, `useLocalStorage`, `useFetch` 등 실용적인 Hook을 직접 만든다
- ToDo 앱의 CRUD 로직을 Custom Hook으로 리팩터링한다

---

<a id="toc"></a>

## 진행 순서

1. [왜 Custom Hook인가?](#1)
2. [Custom Hook 규칙](#2)
3. [실전: useToggle](#3)
4. [실전: useLocalStorage](#4)
5. [실전: useFetch](#5)
6. [Custom Hook으로 ToDo 앱 리팩터링](#6)
7. [실습: useWindowSize Hook 만들기](#7)
8. [정리 + 브릿지](#8)

---

<a id="1"></a>
## 1️⃣ 왜 Custom Hook인가? [↑](#toc)

### 나만의 레시피

자주 해먹는 요리가 있다면, 그 레시피를 따로 적어두면 편합니다. 다음에 만들 때 처음부터 생각할 필요가 없고, 다른 사람에게 알려줄 때도 레시피 한 장이면 됩니다.

Custom Hook이 바로 이것입니다. **자주 쓰는 로직을 레시피(함수)로 정리해두면 누구나 쉽게 재사용할 수 있습니다.**

### 문제: 중복 로직

두 컴포넌트가 똑같은 데이터 로딩 로직을 가지고 있습니다.

```jsx
// UserProfile.jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then((res) => res.json())
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  if (loading) return <p>로딩 중...</p>;
  if (error) return <p>에러 발생</p>;
  return <p>{user?.name}</p>;
}

// PostList.jsx — 똑같은 로직이 반복됩니다 😢
function PostList() {
  const [posts, setPosts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/posts')
      .then((res) => res.json())
      .then(setPosts)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>로딩 중...</p>;
  if (error) return <p>에러 발생</p>;
  return <ul>{posts?.map(/* ... */)}</ul>;
}
```

두 컴포넌트에서 `useState` 3개와 `useEffect`가 완전히 같은 패턴으로 반복됩니다. 이 로직을 재사용할 방법이 없을까요?

**Custom Hook이 해결합니다.**

---

<a id="2"></a>
## 2️⃣ Custom Hook 규칙 [↑](#toc)

Custom Hook은 일반 JavaScript 함수와 거의 같습니다. 단, 세 가지 규칙이 있습니다.

### 규칙 1: 이름은 반드시 `use`로 시작

```jsx
// ✅ 올바른 이름
function useToggle() {}
function useLocalStorage() {}
function useFetch() {}
function useWindowSize() {}

// ❌ 잘못된 이름 — React가 Hook 규칙을 적용하지 않습니다
function toggle() {}
function fetchData() {}
```

### 규칙 2: 다른 Hook을 내부에서 호출할 수 있습니다

```jsx
function useMyHook() {
  const [value, setValue] = useState(0); // useState 사용 가능
  useEffect(() => { /* ... */ }, [value]); // useEffect 사용 가능
  return { value, setValue };
}
```

### 규칙 3: 반환 값은 자유롭게 설계

```jsx
// 배열 반환 (useState 스타일)
return [value, toggle];

// 객체 반환 (이름으로 구조 분해)
return { data, loading, error };

// 값만 반환
return windowSize;
```

---

<a id="3"></a>
## 3️⃣ 실전: useToggle [↑](#toc)

`true`/`false`를 토글하는 가장 단순한 Custom Hook입니다. 모달, 드롭다운, 아코디언 등에 매우 자주 씁니다.

```jsx
// src/hooks/useToggle.js
import { useState } from 'react';

function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue);

  const toggle = () => setValue((prev) => !prev);
  const setTrue = () => setValue(true);
  const setFalse = () => setValue(false);

  return [value, toggle, { setTrue, setFalse }];
}

export default useToggle;
```

```jsx
// 사용 예시
import useToggle from '../hooks/useToggle';

function Modal() {
  const [isOpen, toggleModal] = useToggle(false);

  return (
    <div className="p-4">
      <button
        onClick={toggleModal}
        className="bg-blue-500 text-white px-4 py-2 rounded-lg"
      >
        {isOpen ? '닫기' : '열기'}
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <div className="bg-white rounded-xl p-6 shadow-xl max-w-sm w-full mx-4">
            <h2 className="text-lg font-bold mb-3">모달 제목</h2>
            <p className="text-gray-600 mb-4">모달 내용입니다.</p>
            <button
              onClick={toggleModal}
              className="bg-gray-200 px-4 py-2 rounded-lg"
            >
              닫기
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

// 다크 모드 토글에도 사용
function ThemeToggle() {
  const [isDark, toggle] = useToggle(false);

  return (
    <button
      onClick={toggle}
      className={`px-4 py-2 rounded-full font-medium transition-colors ${
        isDark ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-800'
      }`}
    >
      {isDark ? '☀️ 라이트 모드' : '🌙 다크 모드'}
    </button>
  );
}
```

---

<a id="4"></a>
## 4️⃣ 실전: useLocalStorage [↑](#toc)

상태를 localStorage에 자동으로 저장하고 불러오는 Hook입니다. 새로고침해도 데이터가 유지됩니다.

```jsx
// src/hooks/useLocalStorage.js
import { useState, useEffect } from 'react';

function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    // 초기화 함수 — 컴포넌트 처음 마운트 시 한 번만 실행
    try {
      const saved = localStorage.getItem(key);
      return saved ? JSON.parse(saved) : initialValue;
    } catch {
      return initialValue;
    }
  });

  useEffect(() => {
    // value가 바뀔 때마다 localStorage 업데이트
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch {
      // localStorage 사용 불가 환경(시크릿 모드 등) 무시
    }
  }, [key, value]);

  return [value, setValue];
}

export default useLocalStorage;
```

```jsx
// 사용 예시 — useState와 완전히 같은 방식으로 씁니다
import useLocalStorage from '../hooks/useLocalStorage';

function Settings() {
  const [name, setName] = useLocalStorage('username', '');
  const [theme, setTheme] = useLocalStorage('theme', 'light');

  return (
    <div className="p-6 space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">이름</label>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="이름을 입력하세요"
          className="border rounded px-3 py-2 w-full"
        />
      </div>
      <div>
        <p className="text-sm font-medium mb-1">테마</p>
        <div className="flex gap-2">
          {['light', 'dark'].map((t) => (
            <button
              key={t}
              onClick={() => setTheme(t)}
              className={`px-3 py-1 rounded text-sm ${
                theme === t ? 'bg-blue-500 text-white' : 'bg-gray-100'
              }`}
            >
              {t === 'light' ? '라이트' : '다크'}
            </button>
          ))}
        </div>
      </div>
      <p className="text-xs text-gray-400">
        새로고침해도 설정이 유지됩니다.
      </p>
    </div>
  );
}
```

---

<a id="5"></a>
## 5️⃣ 실전: useFetch [↑](#toc)

API 데이터를 불러오는 로직을 재사용 가능하게 만듭니다. loading, error 상태를 포함합니다.

```jsx
// src/hooks/useFetch.js
import { useState, useEffect } from 'react';

function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // url이 없으면 실행하지 않습니다
    if (!url) return;

    setLoading(true);
    setData(null);
    setError(null);

    const controller = new AbortController(); // 컴포넌트 언마운트 시 요청 취소

    fetch(url, { signal: controller.signal })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP 오류: ${res.status}`);
        return res.json();
      })
      .then(setData)
      .catch((err) => {
        if (err.name !== 'AbortError') setError(err.message);
      })
      .finally(() => setLoading(false));

    return () => controller.abort(); // 클린업: 요청 취소
  }, [url]);

  return { data, loading, error };
}

export default useFetch;
```

```jsx
// 사용 예시 — 어디서든 동일한 패턴으로
import useFetch from '../hooks/useFetch';

function UserList() {
  const { data: users, loading, error } = useFetch(
    'https://jsonplaceholder.typicode.com/users'
  );

  if (loading) {
    return (
      <div className="flex justify-center py-10">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-10 text-red-500">
        오류: {error}
      </div>
    );
  }

  return (
    <ul className="space-y-2 p-4">
      {users?.map((user) => (
        <li key={user.id} className="p-3 border rounded-lg hover:bg-gray-50">
          <p className="font-medium">{user.name}</p>
          <p className="text-sm text-gray-500">{user.email}</p>
        </li>
      ))}
    </ul>
  );
}

// PostList도 같은 Hook을 씁니다 — 로직 중복 없음 ✅
function PostList() {
  const { data: posts, loading, error } = useFetch(
    'https://jsonplaceholder.typicode.com/posts?_limit=5'
  );

  if (loading) return <p className="text-center">로딩 중...</p>;
  if (error) return <p className="text-red-500">에러: {error}</p>;

  return (
    <ul className="space-y-2 p-4">
      {posts?.map((post) => (
        <li key={post.id} className="p-3 border rounded-lg">
          <p className="font-medium">{post.title}</p>
          <p className="text-sm text-gray-500 line-clamp-2">{post.body}</p>
        </li>
      ))}
    </ul>
  );
}
```

---

<a id="6"></a>
## 6️⃣ Custom Hook으로 ToDo 앱 리팩터링 [↑](#toc)

12장에서 만든 ToDo 앱의 CRUD 로직을 Custom Hook으로 분리합니다. 컴포넌트는 UI에만 집중하고, Hook이 로직을 담당합니다.

```jsx
// src/hooks/useTodos.js
import useLocalStorage from './useLocalStorage';

function useTodos() {
  const [todos, setTodos] = useLocalStorage('todos', []);

  function addTodo(text) {
    setTodos((prev) => [
      ...prev,
      { id: Date.now(), text, done: false },
    ]);
  }

  function toggleTodo(id) {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, done: !todo.done } : todo
      )
    );
  }

  function deleteTodo(id) {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  }

  function clearDone() {
    setTodos((prev) => prev.filter((todo) => !todo.done));
  }

  const stats = {
    total: todos.length,
    done: todos.filter((t) => t.done).length,
    active: todos.filter((t) => !t.done).length,
  };

  return { todos, addTodo, toggleTodo, deleteTodo, clearDone, stats };
}

export default useTodos;
```

```jsx
// App.jsx — 훨씬 깔끔해졌습니다
import { useState } from 'react';
import useTodos from './hooks/useTodos';
import TodoForm from './components/TodoForm';
import FilterButtons from './components/FilterButtons';
import TodoList from './components/TodoList';

function App() {
  const { todos, addTodo, toggleTodo, deleteTodo, clearDone, stats } = useTodos();
  const [filter, setFilter] = useState('all');

  const filteredTodos = todos.filter((todo) => {
    if (filter === 'active') return !todo.done;
    if (filter === 'done') return todo.done;
    return true;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 py-10">
      <div className="max-w-md mx-auto bg-white rounded-2xl shadow-lg p-6">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">
          나의 할 일 목록
        </h1>
        <TodoForm onAdd={addTodo} />
        <FilterButtons current={filter} onChange={setFilter} />
        <TodoList
          todos={filteredTodos}
          onToggle={toggleTodo}
          onDelete={deleteTodo}
        />
        {stats.done > 0 && (
          <button
            onClick={clearDone}
            className="mt-3 w-full text-sm text-gray-400 hover:text-red-400 py-2 transition-colors"
          >
            완료 항목 삭제 ({stats.done}개)
          </button>
        )}
        {stats.total > 0 && (
          <div className="mt-3 pt-3 border-t">
            <p className="text-xs text-center text-gray-400">
              전체 {stats.total}개 · 진행중 {stats.active}개 · 완료 {stats.done}개
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
```

**변화:** App 컴포넌트에서 상태 관리 로직이 모두 사라졌습니다. `addTodo`, `toggleTodo`, `deleteTodo`가 무엇을 하는지 이름만 봐도 알 수 있습니다. localStorage 연동도 자동으로 됩니다.

---

<a id="7"></a>
## 7️⃣ 실습: useWindowSize Hook 만들기 [↑](#toc)

창 크기를 추적하는 Hook을 만들어 봅시다. 반응형 UI를 만들 때 매우 유용합니다.

### 요구사항

- `{ width, height }` 형태로 현재 창 크기를 반환
- 창 크기가 바뀔 때마다 자동으로 업데이트
- 컴포넌트 언마운트 시 이벤트 리스너 정리

### 기본 과제

```jsx
// src/hooks/useWindowSize.js
import { useState, useEffect } from 'react';

function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    function handleResize() {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return size;
}

export default useWindowSize;
```

```jsx
// 사용 예시
import useWindowSize from '../hooks/useWindowSize';

function ResponsiveDemo() {
  const { width, height } = useWindowSize();

  const breakpoint =
    width < 640 ? 'sm (모바일)' :
    width < 1024 ? 'md (태블릿)' :
    'lg (데스크탑)';

  return (
    <div className="p-6 text-center">
      <div className="inline-block bg-blue-50 rounded-xl px-6 py-4 mb-4">
        <p className="text-2xl font-mono font-bold text-blue-600">
          {width} × {height}
        </p>
        <p className="text-sm text-blue-400 mt-1">{breakpoint}</p>
      </div>
      <p className="text-gray-500 text-sm">
        창 크기를 조절해 보세요!
      </p>
    </div>
  );
}
```

### 도전 과제

1. **useDebounce Hook 만들기** — 값이 빠르게 바뀔 때 일정 시간 후에만 반영 (검색창 입력에 유용)

```jsx
// 목표 인터페이스
function useDebounce(value, delay = 300) {
  // delay ms 동안 value가 안 바뀌면 그때 업데이트
  // hint: useEffect + setTimeout + clearTimeout
}

// 사용 예시
const [query, setQuery] = useState('');
const debouncedQuery = useDebounce(query, 500);

useEffect(() => {
  // debouncedQuery가 바뀔 때만 API 호출 (타이핑할 때마다 호출 안 됨)
  if (debouncedQuery) fetchResults(debouncedQuery);
}, [debouncedQuery]);
```

2. **useOnClickOutside Hook 만들기** — 특정 요소 바깥을 클릭했을 때 감지 (드롭다운, 모달 닫기에 사용)

---

<a id="8"></a>
## 8️⃣ 정리 + 브릿지 [↑](#toc)

### 이번 장에서 배운 것

| Hook | 역할 |
|------|------|
| `useToggle` | boolean 토글 — 모달, 드롭다운, 다크모드 |
| `useLocalStorage` | 상태를 localStorage에 자동 저장 |
| `useFetch` | API 호출 + loading/error 상태 관리 |
| `useTodos` | ToDo CRUD 로직 캡슐화 |
| `useWindowSize` | 창 크기 추적 |

### Custom Hook 설계 원칙

```
1. 이름은 use로 시작
2. 한 가지 책임만 (단일 책임 원칙)
3. 반환 값은 사용하는 쪽이 편리하게 설계
4. 클린업 잊지 않기 (이벤트 리스너, 타이머)
```

### 언제 Custom Hook을 만드는가?

```
같은 Hook 로직이 두 곳 이상에서 반복된다 → Custom Hook으로 추출
컴포넌트가 UI와 관계없는 로직으로 복잡해진다 → Custom Hook으로 분리
```

### Part 4가 끝났습니다

`useEffect`, `useRef`, `useContext`, 그리고 Custom Hook까지 배웠습니다. React의 핵심 역량을 모두 갖추었습니다.

마지막 Part에서는 지금까지 배운 모든 것을 활용해 **라우팅(React Router), 외부 API 연동, 상태 관리 라이브러리(Zustand)**를 배우고 날씨 앱을 완성합니다. 실무에서 만나는 형태의 앱을 처음부터 끝까지 만들어 보는 시간입니다!

{% endraw %}
