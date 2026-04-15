---
title: 15. useContext — 전역 상태
layout: default
parent: React (리뉴얼)
nav_order: 16
permalink: /language/react-new/usecontext
---

{% raw %}

# 15장. useContext — 전역 상태 공유

## 학습 목표

- Prop Drilling이 무엇이고 왜 문제인지 이해한다
- `createContext`, `Provider`, `useContext`의 흐름을 익힌다
- React 19의 새로운 Provider 문법(`<Context value={}>`)을 사용한다
- Context를 언제 써야 하고 언제 쓰지 말아야 하는지 판단한다

---

<a id="toc"></a>

## 진행 순서

1. [문제: Prop Drilling](#1)
2. [해결: Context](#2)
3. [Step-by-step: 테마 전환](#3)
4. [Step-by-step: 사용자 인증](#4)
5. [Context vs Props vs Zustand](#5)
6. [주의: Context는 만능이 아닙니다](#6)
7. [실습: 다국어 지원](#7)
8. [정리 + 브릿지](#8)

---

<a id="1"></a>
## 1️⃣ 문제: Prop Drilling [↑](#toc)

### 와인잔 탑

식당에서 와인을 따를 때 탑처럼 쌓인 와인잔에 하나씩 차례로 채우는 퍼포먼스를 본 적 있나요? 1층 잔에서 넘쳐야 2층으로, 2층에서 넘쳐야 3층으로 전달됩니다. 원하는 층까지 가려면 그 위의 모든 잔을 거쳐야 합니다.

Props도 마찬가지입니다. **최상위 컴포넌트의 데이터를 깊은 곳의 자식에게 전달하려면 중간의 모든 컴포넌트를 거쳐야 합니다.** 이것이 **Prop Drilling(프롭 드릴링)**입니다.

### 고통: 실제 상황

로그인한 사용자 정보(`user`)를 여러 컴포넌트에서 필요로 합니다.

```jsx
// App.jsx — user를 가지고 있습니다
function App() {
  const [user, setUser] = useState({ name: '김리액트', role: 'admin' });
  return <Layout user={user} />;  // Layout은 user가 필요 없는데 전달해야 함
}

// Layout — user 사용 안 함. 그냥 통과시킵니다
function Layout({ user }) {
  return (
    <div>
      <Header user={user} />  {/* Header에 전달하기 위해 */}
      <Sidebar user={user} /> {/* Sidebar에 전달하기 위해 */}
      <main>...</main>
    </div>
  );
}

// Header — user 사용 안 함. 또 통과
function Header({ user }) {
  return (
    <header>
      <Nav user={user} />  {/* Nav에 전달하기 위해 */}
    </header>
  );
}

// Nav — 드디어 user를 씁니다 (하지만 3단계를 거쳤습니다)
function Nav({ user }) {
  return <span>안녕하세요, {user.name}님!</span>;
}
```

`Layout`과 `Header`는 `user`를 **전혀 사용하지 않으면서도** 전달 통로 역할을 해야 합니다. 컴포넌트가 깊어질수록 고통은 커집니다.

이게 고통입니다.

---

<a id="2"></a>
## 2️⃣ 해결: Context [↑](#toc)

### 도서관 게시판

도서관에 공지사항 게시판이 있습니다. 선생님이 게시판에 공지를 붙이면, **누구든 직접 와서 읽을 수 있습니다.** 1층 → 2층 → 3층을 거칠 필요가 없습니다.

Context는 이 게시판과 같습니다. 데이터를 "공중에" 걸어두면, 어떤 자식 컴포넌트든 직접 가져다 읽을 수 있습니다.

### Context의 3단계

```
1. createContext  — 게시판 만들기
2. Provider       — 게시판에 내용 붙이기 (데이터 제공)
3. useContext      — 게시판 읽기 (데이터 소비)
```

```jsx
import { createContext, useContext, useState } from 'react';

// 1단계: Context 생성 (기본값은 선택사항)
const UserContext = createContext(null);

// 2단계: Provider로 하위 트리 감싸기 (React 19 문법)
function App() {
  const [user] = useState({ name: '김리액트', role: 'admin' });

  return (
    // React 19: <UserContext value={user}> (Provider 키워드 불필요)
    <UserContext value={user}>
      <Layout />
    </UserContext>
  );
}

// Layout, Header는 user를 전달할 필요 없습니다 ✅
function Layout() {
  return (
    <div>
      <Header />
      <main>...</main>
    </div>
  );
}

function Header() {
  return <header><Nav /></header>;
}

// 3단계: 필요한 곳에서 직접 꺼내 씁니다
function Nav() {
  const user = useContext(UserContext); // 게시판에서 직접 읽기
  return <span>안녕하세요, {user.name}님!</span>;
}
```

`Layout`, `Header`는 `user`에 대해 아무것도 알 필요가 없어졌습니다.

---

<a id="3"></a>
## 3️⃣ Step-by-step: 테마 전환 [↑](#toc)

다크/라이트 테마 전환 기능을 Context로 구현합니다.

### 1단계: ThemeContext 파일 생성

```jsx
// src/contexts/ThemeContext.jsx
import { createContext, useContext, useState } from 'react';

// Context 생성
export const ThemeContext = createContext('light');

// Context와 변경 함수를 함께 제공하는 커스텀 컴포넌트
export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  function toggleTheme() {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  }

  return (
    // React 19: <ThemeContext value={...}> 사용
    <ThemeContext value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext>
  );
}

// 편리하게 쓸 수 있는 커스텀 훅
export function useTheme() {
  return useContext(ThemeContext);
}
```

### 2단계: App 감싸기

```jsx
// src/main.jsx
import { ThemeProvider } from './contexts/ThemeContext';
import App from './App';

createRoot(document.getElementById('root')).render(
  <ThemeProvider>
    <App />
  </ThemeProvider>
);
```

### 3단계: 어디서든 사용

```jsx
// 어떤 컴포넌트에서든 props 없이 테마를 읽고 변경할 수 있습니다
import { useTheme } from '../contexts/ThemeContext';

function ThemedCard() {
  const { theme, toggleTheme } = useTheme();

  return (
    <div
      className={`p-6 rounded-xl shadow transition-colors duration-300 ${
        theme === 'dark'
          ? 'bg-gray-800 text-white'
          : 'bg-white text-gray-800'
      }`}
    >
      <p className="mb-4">현재 테마: {theme === 'dark' ? '다크 모드' : '라이트 모드'}</p>
      <button
        onClick={toggleTheme}
        className={`px-4 py-2 rounded-lg font-medium transition-colors ${
          theme === 'dark'
            ? 'bg-white text-gray-800 hover:bg-gray-100'
            : 'bg-gray-800 text-white hover:bg-gray-700'
        }`}
      >
        {theme === 'dark' ? '☀️ 라이트 모드' : '🌙 다크 모드'}
      </button>
    </div>
  );
}
```

---

<a id="4"></a>
## 4️⃣ Step-by-step: 사용자 인증 [↑](#toc)

로그인/로그아웃 상태를 앱 전체에서 공유하는 패턴입니다. 실무에서 가장 자주 쓰는 Context 사용법입니다.

```jsx
// src/contexts/AuthContext.jsx
import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null); // null = 비로그인

  function login(username) {
    // 실제 앱에서는 API 호출 후 받은 사용자 정보를 저장합니다
    setUser({ name: username, role: 'user' });
  }

  function logout() {
    setUser(null);
  }

  return (
    <AuthContext value={{ user, login, logout }}>
      {children}
    </AuthContext>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth는 AuthProvider 안에서 사용해야 합니다');
  }
  return context;
}
```

```jsx
// 로그인 폼
function LoginForm() {
  const { login } = useAuth();
  const [name, setName] = useState('');

  function handleSubmit(e) {
    e.preventDefault();
    if (name.trim()) login(name.trim());
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 p-4">
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="이름을 입력하세요"
        className="flex-1 border rounded px-3 py-2"
      />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
        로그인
      </button>
    </form>
  );
}

// 헤더에서 사용자 정보 표시
function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white shadow px-6 py-4 flex justify-between items-center">
      <h1 className="font-bold text-xl">나의 앱</h1>
      {user ? (
        <div className="flex items-center gap-3">
          <span className="text-gray-600">{user.name}님</span>
          <button
            onClick={logout}
            className="text-sm bg-gray-100 hover:bg-gray-200 px-3 py-1 rounded"
          >
            로그아웃
          </button>
        </div>
      ) : (
        <span className="text-gray-400">비로그인</span>
      )}
    </header>
  );
}

// 로그인 여부에 따라 다른 화면 보여주기
function App() {
  const { user } = useAuth();

  return (
    <div>
      <Header />
      <main className="p-6">
        {user ? (
          <p>{user.name}님, 환영합니다!</p>
        ) : (
          <LoginForm />
        )}
      </main>
    </div>
  );
}
```

---

<a id="5"></a>
## 5️⃣ Context vs Props vs Zustand [↑](#toc)

상황에 맞는 도구를 선택하는 것이 중요합니다.

| | Props | Context | Zustand |
|----|-------|---------|---------|
| 적합한 경우 | 부모→자식, 1-2단계 | 앱 전체, 변경이 적은 데이터 | 복잡한 상태, 빈번한 업데이트 |
| 예시 | 버튼 스타일, 콜백 | 테마, 인증, 언어 | 장바구니, 필터, 폼 |
| 설정 복잡도 | 없음 | 낮음 | 설치 필요 |
| 성능 | 최적 | 주의 필요 | 최적화됨 |

### 언제 무엇을 쓸까?

```
데이터를 1-2단계만 내려보내면 된다
    → Props

앱 전체에서 필요하고 자주 바뀌지 않는다 (테마, 로그인, 언어)
    → Context

여러 컴포넌트에서 복잡하게 변경하고 성능이 중요하다 (쇼핑카트, 필터)
    → Zustand 등 외부 라이브러리
```

---

<a id="6"></a>
## 6️⃣ 주의: Context는 만능이 아닙니다 [↑](#toc)

### 리렌더 문제

Context 값이 바뀌면 **그 Context를 사용하는 모든 컴포넌트가 리렌더됩니다.** 값이 자주 바뀌는 데이터를 Context에 넣으면 성능 문제가 발생합니다.

```jsx
// ❌ 나쁜 예: 자주 바뀌는 값을 하나의 Context에
const AppContext = createContext({
  user: null,         // 거의 안 바뀜 ✅
  theme: 'light',     // 가끔 바뀜 ✅
  cartItems: [],      // 자주 바뀜 ❌ → Context에 부적합
  mousePosition: {},  // 매우 자주 바뀜 ❌ → Context에 절대 불가
});

// ✅ 좋은 예: 용도별로 Context를 분리
const AuthContext = createContext(null);   // 로그인 정보
const ThemeContext = createContext('light'); // 테마
// cartItems는 Zustand 등으로 관리
```

### Context를 분리해야 하는 이유

```jsx
// ThemeContext 값이 바뀌면 AuthContext 소비자는 리렌더 안 됩니다 ✅
<AuthContext value={authValue}>
  <ThemeContext value={themeValue}>
    <App />
  </ThemeContext>
</AuthContext>
```

### Context에 적합한 데이터

| 적합 | 부적합 |
|------|--------|
| 로그인 사용자 정보 | 마우스 위치 |
| 언어 설정 | 애니메이션 진행도 |
| 테마 (다크/라이트) | 실시간으로 바뀌는 타이머 |
| 접근성 설정 | 장바구니 (Zustand가 더 적합) |

---

<a id="7"></a>
## 7️⃣ 실습: 다국어 지원 [↑](#toc)

한국어/영어를 토글하는 언어 Context를 만들어 봅시다.

### 기본 과제

```jsx
// src/contexts/LanguageContext.jsx
import { createContext, useContext, useState } from 'react';

const translations = {
  ko: {
    greeting: '안녕하세요!',
    button: '언어 변경',
    description: '한국어로 표시 중입니다.',
  },
  en: {
    greeting: 'Hello!',
    button: 'Change Language',
    description: 'Displaying in English.',
  },
};

const LanguageContext = createContext('ko');

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState('ko');

  function toggleLanguage() {
    setLang((prev) => (prev === 'ko' ? 'en' : 'ko'));
  }

  return (
    <LanguageContext value={{ lang, toggleLanguage, t: translations[lang] }}>
      {children}
    </LanguageContext>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
```

```jsx
// 사용 예시
function WelcomePage() {
  const { t, toggleLanguage, lang } = useLanguage();

  return (
    <div className="text-center p-8">
      <p className="text-3xl font-bold mb-4">{t.greeting}</p>
      <p className="text-gray-600 mb-6">{t.description}</p>
      <button
        onClick={toggleLanguage}
        className="bg-indigo-500 text-white px-6 py-2 rounded-lg hover:bg-indigo-600 transition-colors"
      >
        {t.button} ({lang === 'ko' ? 'EN' : '한국어'})
      </button>
    </div>
  );
}
```

### 도전 과제

1. 일본어(ja)를 세 번째 언어로 추가
2. 선택된 언어를 localStorage에 저장해서 새로고침 후에도 유지
3. 날짜 형식도 언어에 맞게 변환 (`new Date().toLocaleDateString('ko-KR')`)

---

<a id="8"></a>
## 8️⃣ 정리 + 브릿지 [↑](#toc)

### 이번 장에서 배운 것

| 개념 | 내용 |
|------|------|
| Prop Drilling | 중간 컴포넌트가 불필요하게 props를 전달하는 문제 |
| `createContext` | Context 객체 생성 |
| `<Context value={}>` | React 19의 Provider 문법 |
| `useContext` | 어느 자식에서든 Context 값 읽기 |
| Context 분리 | 업데이트 빈도가 다른 데이터는 다른 Context로 |

### 핵심 흐름

```
createContext()     → 게시판 만들기
<Context value={}>  → 게시판에 내용 붙이기
useContext()        → 게시판 읽기
```

### React 19 주의사항

```jsx
// React 18 이하 (여전히 작동하지만 구식)
<ThemeContext.Provider value={theme}>

// React 19 (권장)
<ThemeContext value={theme}>
```

### 다음 장 예고

React의 내장 Hook(`useState`, `useEffect`, `useRef`, `useContext`)을 모두 배웠습니다. 이 Hook들을 조합해서 **나만의 Custom Hook**을 만드는 방법을 배울 차례입니다. 같은 로직을 두 곳에서 반복한다면, Custom Hook으로 깔끔하게 재사용할 수 있습니다.

{% endraw %}
