---
title: 19. Zustand — 상태 관리
layout: default
parent: React
nav_order: 20
permalink: /language/react/zustand
---

{% raw %}

# 19장. Zustand — 상태 관리 라이브러리

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다.

- Prop Drilling 문제가 무엇인지 설명할 수 있다
- Zustand를 설치하고 첫 스토어를 만들 수 있다
- 셀렉터 패턴으로 필요한 상태만 구독할 수 있다
- ToDo 앱의 상태를 Zustand 스토어로 마이그레이션할 수 있다
- 도메인별로 스토어를 나눠 관리할 수 있다
- Context와 Zustand의 차이를 상황에 맞게 선택할 수 있다

---

## 진행 순서

<a id="toc"></a>

1. [Zustand = 중앙 창고](#1)
2. [왜 Zustand인가? — Prop Drilling 문제](#2)
3. [설치 및 첫 스토어 만들기](#3)
4. [스토어 사용하기 — 셀렉터 패턴](#4)
5. [실전: ToDo 스토어로 마이그레이션](#5)
6. [여러 스토어 나누기](#6)
7. [Context vs Zustand 비교](#7)
8. [실습: 장바구니 with Zustand](#8)
9. [정리 + 브릿지](#9)

---

<a id="1"></a>
## 1️⃣ Zustand = 중앙 창고 [↑](#toc)

React로 앱을 만들다 보면 이런 상황이 생깁니다.

> A 컴포넌트에서 로그인한 사용자 정보를 B 컴포넌트와 C 컴포넌트에서도 써야 합니다. 그런데 B와 C는 A의 자식이 아닌, 완전히 다른 위치에 있습니다.

**택배 비유로 이해하기**

Props는 마치 **택배**와 같습니다. A에서 B로, B에서 C로, C에서 D로 전달해야 한다면 중간 B, C는 그 데이터가 필요 없어도 "중간 전달자" 역할을 해야 합니다. 택배를 4번 옮겨야 합니다.

**Zustand는 중앙 창고입니다.**

> 모든 컴포넌트가 창고에 직접 찾아가서 필요한 물건을 가져옵니다.
> 중간에 택배를 거치지 않아도 됩니다.
> 창고에 물건을 넣을 수도 있습니다.
> A가 창고에 새 물건을 넣으면, 창고를 구독 중인 D가 즉시 알아챕니다.

---

<a id="2"></a>
## 2️⃣ 왜 Zustand인가? — Prop Drilling 문제 [↑](#toc)

### 문제: Prop Drilling

컴포넌트 트리가 깊어지면 props를 여러 단계로 내려보내야 합니다. 이를 **Prop Drilling**이라고 합니다.

```
App (user 상태 보유)
  └── Header (user 필요 → props로 받음)
       └── UserAvatar (user 필요 → props로 받음)
            └── UserMenu (user 필요 → props로 받음)  ← 실제 쓰는 곳
```

```jsx
// 모든 중간 컴포넌트가 user를 전달해야 합니다
function App() {
  const [user, setUser] = useState({ name: '김철수' });
  return <Header user={user} />;          // Header는 user를 써야 할까요?
}

function Header({ user }) {              // Header는 user가 필요 없지만
  return <UserAvatar user={user} />;    // 전달만 합니다
}

function UserAvatar({ user }) {         // UserAvatar도 전달만 합니다
  return <UserMenu user={user} />;
}

function UserMenu({ user }) {           // 실제로 쓰는 곳
  return <p>안녕하세요, {user.name}!</p>;
}
```

Header와 UserAvatar는 `user`를 직접 쓰지도 않는데 props로 받아서 전달하기만 합니다.

### Context로 해결할 수 있지만...

Context는 Provider 안의 모든 컴포넌트를 **리렌더링**시킵니다. `user` 객체 안의 단 하나의 값이 바뀌어도, Provider 하위의 모든 컴포넌트가 다시 렌더됩니다. 성능에 영향을 줄 수 있습니다.

### Zustand의 장점

- **Prop Drilling 없음**: 어느 컴포넌트에서든 스토어에 직접 접근
- **선택적 구독**: 필요한 값만 구독해서 그 값이 바뀔 때만 리렌더
- **간단한 문법**: Context보다 훨씬 적은 코드
- **Redux보다 가벼움**: 보일러플레이트(반복 코드) 거의 없음

---

<a id="3"></a>
## 3️⃣ 설치 및 첫 스토어 만들기 [↑](#toc)

### 설치

```bash
npm install zustand
```

### 카운터 스토어 만들기

```jsx
// src/stores/useCounterStore.js
import { create } from 'zustand';

const useCounterStore = create((set) => ({
  // 상태 (State)
  count: 0,

  // 액션 (Actions) — 상태를 바꾸는 함수들
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
  incrementBy: (amount) => set((state) => ({ count: state.count + amount })),
}));

export default useCounterStore;
```

### 구조 이해하기

```
create((set) => ({...}))
  ↑                ↑
  Zustand 함수     set = 상태를 업데이트하는 함수 (React의 setState와 유사)

set((state) => ({ count: state.count + 1 }))
  ↑
  이전 상태(state)를 받아 새 상태를 반환하는 함수 형태 (불변성 자동 처리)

set({ count: 0 })
  ↑
  값을 바로 넣어도 됩니다 (이전 상태가 필요 없을 때)
```

---

<a id="4"></a>
## 4️⃣ 스토어 사용하기 — 셀렉터 패턴 [↑](#toc)

### 기본 사용

```jsx
// src/components/Counter.jsx
import useCounterStore from '../stores/useCounterStore';

function Counter() {
  // 스토어에서 필요한 것만 꺼내기 (셀렉터)
  const count = useCounterStore((state) => state.count);
  const increment = useCounterStore((state) => state.increment);
  const decrement = useCounterStore((state) => state.decrement);
  const reset = useCounterStore((state) => state.reset);

  return (
    <div className="flex flex-col items-center gap-4 p-8">
      <p className="text-5xl font-bold tabular-nums">{count}</p>
      <div className="flex gap-3">
        <button
          onClick={decrement}
          className="w-12 h-12 bg-red-100 text-red-700 rounded-full text-xl font-bold hover:bg-red-200 transition"
        >
          −
        </button>
        <button
          onClick={reset}
          className="px-4 h-12 bg-gray-100 text-gray-700 rounded-full font-medium hover:bg-gray-200 transition"
        >
          리셋
        </button>
        <button
          onClick={increment}
          className="w-12 h-12 bg-blue-100 text-blue-700 rounded-full text-xl font-bold hover:bg-blue-200 transition"
        >
          +
        </button>
      </div>
    </div>
  );
}

export default Counter;
```

### 셀렉터(Selector)가 중요한 이유

```jsx
// 스토어 전체를 구독 — 어떤 값이 바뀌어도 리렌더됩니다 (비효율)
const store = useCounterStore();

// 셀렉터로 필요한 값만 구독 — count가 바뀔 때만 리렌더됩니다 (효율적)
const count = useCounterStore((state) => state.count);
```

스토어에 값이 10개 있어도, 셀렉터로 1개만 구독하면 그 1개가 바뀔 때만 해당 컴포넌트가 리렌더됩니다.

### 멀리 있는 컴포넌트에서도 바로 접근

```jsx
// 완전히 다른 파일에 있는 컴포넌트도 스토어에 바로 접근합니다
// props 전달이 전혀 필요 없습니다

// src/pages/Header.jsx
import useCounterStore from '../stores/useCounterStore';

function Header() {
  const count = useCounterStore((state) => state.count);
  return (
    <header className="bg-white border-b px-6 py-3">
      <span className="text-sm text-gray-500">현재 카운트: {count}</span>
    </header>
  );
}
```

---

<a id="5"></a>
## 5️⃣ 실전: ToDo 스토어로 마이그레이션 [↑](#toc)

이전 과정에서 만든 ToDo 앱을 Zustand로 옮겨봅니다. Before/After를 비교해 보세요.

### Before — useState 사용 (기존)

```jsx
// App.jsx — 모든 상태와 로직이 여기 있습니다
function App() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  const addTodo = () => {
    if (!input.trim()) return;
    setTodos([...todos, { id: Date.now(), text: input, done: false }]);
    setInput('');
  };

  const toggleTodo = (id) => {
    setTodos(todos.map(t => t.id === id ? { ...t, done: !t.done } : t));
  };

  const deleteTodo = (id) => {
    setTodos(todos.filter(t => t.id !== id));
  };

  return (
    // props로 전달해야 합니다
    <>
      <TodoInput value={input} onChange={setInput} onAdd={addTodo} />
      <TodoList todos={todos} onToggle={toggleTodo} onDelete={deleteTodo} />
    </>
  );
}
```

### After — Zustand 사용

**스토어 정의**

```jsx
// src/stores/useTodoStore.js
import { create } from 'zustand';

const useTodoStore = create((set) => ({
  todos: [],

  addTodo: (text) =>
    set((state) => ({
      todos: [
        ...state.todos,
        { id: Date.now(), text: text.trim(), done: false },
      ],
    })),

  toggleTodo: (id) =>
    set((state) => ({
      todos: state.todos.map((t) =>
        t.id === id ? { ...t, done: !t.done } : t
      ),
    })),

  deleteTodo: (id) =>
    set((state) => ({
      todos: state.todos.filter((t) => t.id !== id),
    })),

  clearCompleted: () =>
    set((state) => ({
      todos: state.todos.filter((t) => !t.done),
    })),
}));

export default useTodoStore;
```

**컴포넌트 — props 없이 직접 접근**

```jsx
// src/components/TodoInput.jsx
import { useState } from 'react';
import useTodoStore from '../stores/useTodoStore';

function TodoInput() {
  const [input, setInput] = useState('');
  const addTodo = useTodoStore((state) => state.addTodo); // 스토어에서 직접

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    addTodo(input);
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mb-4">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="할 일을 입력하세요..."
        className="flex-1 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
      >
        추가
      </button>
    </form>
  );
}

export default TodoInput;
```

```jsx
// src/components/TodoList.jsx
import useTodoStore from '../stores/useTodoStore';

function TodoList() {
  // props 없이 스토어에서 직접 꺼냅니다
  const todos = useTodoStore((state) => state.todos);
  const toggleTodo = useTodoStore((state) => state.toggleTodo);
  const deleteTodo = useTodoStore((state) => state.deleteTodo);
  const clearCompleted = useTodoStore((state) => state.clearCompleted);

  const doneCount = todos.filter((t) => t.done).length;

  return (
    <div>
      <p className="text-sm text-gray-500 mb-3">
        완료: {doneCount} / 전체: {todos.length}
      </p>
      <ul className="space-y-2">
        {todos.map((todo) => (
          <li
            key={todo.id}
            className="flex items-center gap-3 bg-white border rounded-lg px-4 py-3"
          >
            <input
              type="checkbox"
              checked={todo.done}
              onChange={() => toggleTodo(todo.id)}
              className="w-4 h-4 accent-blue-600 cursor-pointer"
            />
            <span
              className={`flex-1 ${todo.done ? 'line-through text-gray-400' : 'text-gray-800'}`}
            >
              {todo.text}
            </span>
            <button
              onClick={() => deleteTodo(todo.id)}
              className="text-red-400 hover:text-red-600 transition text-sm"
            >
              삭제
            </button>
          </li>
        ))}
      </ul>
      {doneCount > 0 && (
        <button
          onClick={clearCompleted}
          className="mt-3 text-sm text-gray-400 hover:text-red-500 transition"
        >
          완료된 항목 모두 삭제
        </button>
      )}
    </div>
  );
}

export default TodoList;
```

```jsx
// src/App.jsx — 이제 매우 간단합니다
import TodoInput from './components/TodoInput';
import TodoList from './components/TodoList';

function App() {
  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">할 일 목록</h1>
      <TodoInput />   {/* props 없음 */}
      <TodoList />    {/* props 없음 */}
    </div>
  );
}

export default App;
```

props가 완전히 사라졌습니다. 각 컴포넌트가 스토어에서 필요한 것만 가져갑니다.

---

<a id="6"></a>
## 6️⃣ 여러 스토어 나누기 [↑](#toc)

하나의 스토어에 모든 것을 넣으면 스토어가 거대해집니다. **도메인별로 스토어를 나눕니다.**

```
src/stores/
  useUserStore.js     → 로그인/로그아웃, 사용자 정보
  useTodoStore.js     → ToDo 목록 CRUD
  useThemeStore.js    → 다크모드 등 UI 테마
  useCartStore.js     → 장바구니
```

```jsx
// src/stores/useUserStore.js
import { create } from 'zustand';

const useUserStore = create((set) => ({
  user: null,
  isLoggedIn: false,

  login: (userData) => set({ user: userData, isLoggedIn: true }),
  logout: () => set({ user: null, isLoggedIn: false }),
  updateProfile: (updates) =>
    set((state) => ({ user: { ...state.user, ...updates } })),
}));

export default useUserStore;
```

```jsx
// src/stores/useThemeStore.js
import { create } from 'zustand';

const useThemeStore = create((set) => ({
  isDark: false,
  toggleTheme: () => set((state) => ({ isDark: !state.isDark })),
}));

export default useThemeStore;
```

여러 스토어를 동시에 사용할 수 있습니다.

```jsx
// 한 컴포넌트에서 여러 스토어 사용
import useUserStore from '../stores/useUserStore';
import useThemeStore from '../stores/useThemeStore';

function Header() {
  const user = useUserStore((state) => state.user);
  const isLoggedIn = useUserStore((state) => state.isLoggedIn);
  const isDark = useThemeStore((state) => state.isDark);
  const toggleTheme = useThemeStore((state) => state.toggleTheme);
  const logout = useUserStore((state) => state.logout);

  return (
    <header className={`px-6 py-4 border-b ${isDark ? 'bg-gray-900 text-white' : 'bg-white text-gray-800'}`}>
      <div className="flex justify-between items-center">
        <span className="font-bold">My App</span>
        <div className="flex gap-3 items-center">
          <button
            onClick={toggleTheme}
            className="text-sm px-3 py-1 rounded-full border hover:bg-gray-100 dark:hover:bg-gray-700 transition"
          >
            {isDark ? '라이트 모드' : '다크 모드'}
          </button>
          {isLoggedIn ? (
            <>
              <span className="text-sm">{user.name}</span>
              <button
                onClick={logout}
                className="text-sm text-red-500 hover:underline"
              >
                로그아웃
              </button>
            </>
          ) : (
            <span className="text-sm text-gray-400">로그인이 필요합니다</span>
          )}
        </div>
      </div>
    </header>
  );
}
```

---

<a id="7"></a>
## 7️⃣ Context vs Zustand 비교 [↑](#toc)

언제 Context를 쓰고, 언제 Zustand를 써야 할까요?

| 기준 | Context | Zustand |
|------|---------|---------|
| 설치 | 불필요 (React 내장) | `npm install zustand` |
| 보일러플레이트 | 많음 (createContext, Provider, useContext) | 적음 (`create` 하나) |
| 리렌더 최적화 | 어려움 (모든 소비자 리렌더) | 셀렉터로 자동 최적화 |
| 학습 곡선 | 보통 | 낮음 |
| 번들 크기 | 0 (내장) | ~1KB (매우 작음) |
| 적합 용도 | 테마, 다국어, 인증 정보 | 복잡한 비즈니스 로직, 자주 바뀌는 데이터 |

### 가이드라인

```
거의 바뀌지 않는 전역 값 (테마 색상, 언어 설정)
  → Context 충분합니다

자주 바뀌고 여러 컴포넌트가 쓰는 데이터 (장바구니, 알림, ToDo)
  → Zustand를 쓰세요

두 경우 모두 해당 (예: 인증 상태는 자주 안 바뀌지만 앱 전체가 씀)
  → 취향에 따라, 팀 규칙에 따라 선택
```

---

<a id="8"></a>
## 8️⃣ 실습: 장바구니 with Zustand [↑](#toc)

Zustand로 쇼핑 장바구니를 만들어 봅니다.

### 장바구니 스토어

```jsx
// src/stores/useCartStore.js
import { create } from 'zustand';

const useCartStore = create((set, get) => ({
  items: [],  // [{ id, name, price, quantity }]

  addItem: (product) =>
    set((state) => {
      const existing = state.items.find((item) => item.id === product.id);
      if (existing) {
        // 이미 있으면 수량 증가
        return {
          items: state.items.map((item) =>
            item.id === product.id
              ? { ...item, quantity: item.quantity + 1 }
              : item
          ),
        };
      }
      // 없으면 새로 추가
      return { items: [...state.items, { ...product, quantity: 1 }] };
    }),

  removeItem: (id) =>
    set((state) => ({
      items: state.items.filter((item) => item.id !== id),
    })),

  updateQuantity: (id, quantity) =>
    set((state) => ({
      items: quantity <= 0
        ? state.items.filter((item) => item.id !== id)
        : state.items.map((item) =>
            item.id === id ? { ...item, quantity } : item
          ),
    })),

  clearCart: () => set({ items: [] }),

  // get()으로 스토어의 현재 상태를 읽는 파생 값
  getTotal: () => {
    const { items } = get();
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  },

  getItemCount: () => {
    const { items } = get();
    return items.reduce((sum, item) => sum + item.quantity, 0);
  },
}));

export default useCartStore;
```

### 상품 목록 컴포넌트

```jsx
// src/components/ProductGrid.jsx
import useCartStore from '../stores/useCartStore';

const products = [
  { id: 1, name: '무선 마우스', price: 35000 },
  { id: 2, name: '기계식 키보드', price: 89000 },
  { id: 3, name: '27인치 모니터', price: 320000 },
  { id: 4, name: 'USB 허브', price: 24000 },
];

function ProductGrid() {
  const addItem = useCartStore((state) => state.addItem);
  const cartItems = useCartStore((state) => state.items);

  const isInCart = (id) => cartItems.some((item) => item.id === id);

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">상품 목록</h2>
      <div className="grid grid-cols-2 gap-4">
        {products.map((product) => (
          <div key={product.id} className="bg-white border rounded-xl p-4 shadow-sm">
            <div className="w-full h-24 bg-gray-100 rounded-lg mb-3 flex items-center justify-center text-3xl">
              🖥️
            </div>
            <p className="font-semibold text-gray-800">{product.name}</p>
            <p className="text-blue-600 font-bold mt-1">
              {product.price.toLocaleString()}원
            </p>
            <button
              onClick={() => addItem(product)}
              className={`w-full mt-3 py-2 rounded-lg text-sm font-medium transition ${
                isInCart(product.id)
                  ? 'bg-green-100 text-green-700'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              {isInCart(product.id) ? '장바구니에 있음 (+1)' : '장바구니 담기'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProductGrid;
```

### 장바구니 컴포넌트

```jsx
// src/components/Cart.jsx
import useCartStore from '../stores/useCartStore';

function Cart() {
  const items = useCartStore((state) => state.items);
  const removeItem = useCartStore((state) => state.removeItem);
  const updateQuantity = useCartStore((state) => state.updateQuantity);
  const clearCart = useCartStore((state) => state.clearCart);
  const getTotal = useCartStore((state) => state.getTotal);
  const getItemCount = useCartStore((state) => state.getItemCount);

  if (items.length === 0) {
    return (
      <div className="bg-gray-50 border-2 border-dashed border-gray-200 rounded-xl p-8 text-center text-gray-400">
        장바구니가 비어 있습니다
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">장바구니 ({getItemCount()}개)</h2>
        <button
          onClick={clearCart}
          className="text-sm text-red-400 hover:text-red-600 transition"
        >
          전체 삭제
        </button>
      </div>

      <ul className="space-y-3 mb-4">
        {items.map((item) => (
          <li
            key={item.id}
            className="bg-white border rounded-xl px-4 py-3 flex items-center gap-3"
          >
            <div className="flex-1">
              <p className="font-medium text-gray-800">{item.name}</p>
              <p className="text-sm text-blue-600">{item.price.toLocaleString()}원</p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => updateQuantity(item.id, item.quantity - 1)}
                className="w-7 h-7 rounded-full bg-gray-100 hover:bg-gray-200 transition flex items-center justify-center text-gray-700 font-bold"
              >
                −
              </button>
              <span className="w-5 text-center font-semibold tabular-nums">
                {item.quantity}
              </span>
              <button
                onClick={() => updateQuantity(item.id, item.quantity + 1)}
                className="w-7 h-7 rounded-full bg-gray-100 hover:bg-gray-200 transition flex items-center justify-center text-gray-700 font-bold"
              >
                +
              </button>
            </div>
            <button
              onClick={() => removeItem(item.id)}
              className="text-red-400 hover:text-red-600 transition ml-2"
            >
              ✕
            </button>
          </li>
        ))}
      </ul>

      <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 flex justify-between items-center">
        <span className="font-semibold text-gray-700">총 금액</span>
        <span className="text-xl font-bold text-blue-700">
          {getTotal().toLocaleString()}원
        </span>
      </div>
    </div>
  );
}

export default Cart;
```

### 기본 과제

- [ ] 위 코드를 구현하고 상품 담기 / 수량 변경 / 삭제 / 전체 삭제를 동작시키세요.
- [ ] 헤더에 장바구니 아이템 수를 표시하는 배지를 추가하세요.

### 도전 과제

- [ ] 장바구니 데이터를 `localStorage`에 저장하세요. 페이지를 새로고침해도 데이터가 유지되어야 합니다. (힌트: Zustand `persist` 미들웨어를 검색해 보세요)
- [ ] 같은 상품을 장바구니에 담을 수 있는 최대 수량을 10개로 제한하세요.
- [ ] 장바구니 총 금액이 50,000원 이상이면 "무료배송" 배지를 표시하세요.

---

<a id="9"></a>
## 9️⃣ 정리 + 브릿지 [↑](#toc)

### 이 장에서 배운 것

| 개념 | 내용 |
|------|------|
| Prop Drilling | 불필요한 props 전달 연쇄 문제 |
| `create` | Zustand 스토어 생성 함수 |
| `set` | 스토어 상태 업데이트 함수 |
| `get` | 스토어의 현재 상태를 읽는 함수 |
| 셀렉터 | 필요한 상태만 구독해 불필요한 리렌더 방지 |
| 도메인 분리 | 스토어를 역할별로 파일 나누기 |

### 핵심 패턴 요약

```jsx
// 스토어 정의
import { create } from 'zustand';

const useMyStore = create((set, get) => ({
  value: 0,
  setValue: (v) => set({ value: v }),
  increment: () => set((state) => ({ value: state.value + 1 })),
  getDouble: () => get().value * 2,
}));

// 컴포넌트에서 사용
const value = useMyStore((state) => state.value);       // 구독
const increment = useMyStore((state) => state.increment); // 액션
```

### 지금까지 배운 상태 관리 도구 정리

| 도구 | 범위 | 쓸 때 |
|------|------|-------|
| `useState` | 컴포넌트 내부 | 해당 컴포넌트에서만 쓰는 값 |
| `useContext` | Provider 하위 전체 | 테마, 언어, 간단한 전역 값 |
| `Zustand` | 앱 전체 | 복잡한 상태, 자주 업데이트되는 공유 데이터 |

---

> **브릿지**: 모든 핵심 도구를 배웠습니다! React Router로 여러 페이지를 만들고, fetch API로 외부 데이터를 불러오고, Zustand로 전역 상태를 관리할 수 있게 되었습니다. 마지막 장에서 지금까지 배운 모든 것을 합쳐서 실제 날씨 앱을 완성합니다.

{% endraw %}
