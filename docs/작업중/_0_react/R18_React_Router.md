---
title: 17. React Router
layout: default
parent: React (리뉴얼)
nav_order: 18
permalink: /language/react-new/router
---

{% raw %}

# 17장. React Router — 페이지 이동

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다.

- SPA(Single Page Application)가 무엇인지 설명할 수 있다
- React Router v7을 설치하고 기본 라우팅을 설정할 수 있다
- `<Link>`, `<NavLink>`로 페이지 간 이동을 구현할 수 있다
- `useNavigate`로 코드에서 직접 페이지를 이동할 수 있다
- URL 파라미터(`useParams`)로 동적 페이지를 만들 수 있다
- 중첩 라우트와 `<Outlet>`으로 공유 레이아웃을 만들 수 있다
- 404 페이지를 설정할 수 있다

---

## 진행 순서

<a id="toc"></a>

1. [라우터 = 건물의 엘리베이터](#1)
2. [SPA란?](#2)
3. [React Router 설치](#3)
4. [Routes 설정](#4)
5. [Link와 NavLink](#5)
6. [useNavigate — 코드로 이동하기](#6)
7. [URL 파라미터](#7)
8. [중첩 라우트 (Nested Routes)](#8)
9. [404 페이지](#9)
10. [실습: 다중 페이지 포트폴리오](#10)
11. [정리 + 브릿지](#11)

---

<a id="1"></a>
## 1️⃣ 라우터 = 건물의 엘리베이터 [↑](#toc)

웹사이트에서 "다른 페이지로 이동한다"는 것이 실제로 어떻게 동작하는지 생각해 본 적 있으신가요?

전통적인 웹사이트는 마치 **다른 건물로 이동하는 것**과 같습니다. 쇼핑몰에서 상품 목록을 보다가 상품 상세 페이지를 클릭하면 브라우저가 서버에 완전히 새로운 HTML 파일을 요청합니다. 화면 전체가 깜빡이고 새로 그려집니다.

React로 만드는 SPA는 다릅니다. **건물 엘리베이터**를 생각해 보세요.

> 엘리베이터 버튼(URL)을 누르면 해당 층(페이지)의 내용이 표시됩니다.
> 하지만 건물 자체(앱)를 나갔다가 다시 들어오는 것이 아닙니다.
> 1층 로비(네비게이션)는 항상 그 자리에 있고, 가운데 공간(컨텐츠)만 바뀝니다.

이것이 React Router가 하는 일입니다.

---

<a id="2"></a>
## 2️⃣ SPA란? [↑](#toc)

### 전통적인 웹사이트 (MPA — Multi Page Application)

```
사용자: 상품 페이지 클릭
  → 브라우저: 서버에 /products.html 요청
  → 서버: products.html 파일 전송
  → 브라우저: 화면 전체를 새로 그림 (깜빡임)
  → 사용자: 새 페이지 확인

사용자: 상품 상세 클릭
  → 브라우저: 서버에 /products/123.html 요청
  → 서버: product-123.html 파일 전송
  → 브라우저: 화면 전체를 또 새로 그림 (깜빡임)
```

**문제**: 매번 서버 왕복, 화면 깜빡임, 느린 UX.

### SPA (Single Page Application)

```
사용자: 앱 최초 접속
  → 브라우저: 서버에서 index.html + JS 번들 한 번만 받음
  → 이후 모든 "페이지 이동"은 JS가 화면을 교체
  → 서버 왕복 없음, 깜빡임 없음, 앱처럼 빠름
```

| 비교 항목 | 전통적 MPA | SPA (React + Router) |
|-----------|-----------|----------------------|
| 페이지 이동 | 서버에서 새 HTML 수신 | JS가 화면 교체 |
| 화면 깜빡임 | 있음 | 없음 |
| 초기 로딩 | 빠름 | 약간 느림 |
| 이후 이동 | 매번 느림 | 매우 빠름 |
| URL 지원 | 자연스러움 | React Router 필요 |

> **요약**: SPA는 처음에 앱 전체를 한 번 내려받고, 이후 URL에 따라 보여줄 컴포넌트만 교체합니다.

---

<a id="3"></a>
## 3️⃣ React Router 설치 [↑](#toc)

### 설치

React Router v7은 패키지 이름이 `react-router` 하나로 통합되었습니다.

```bash
npm install react-router
```

> **v7 변경사항**: 예전에는 `react-router-dom`을 설치했습니다. v7부터는 `react-router` 하나만 설치하면 됩니다.

### main.jsx에 BrowserRouter 감싸기

```jsx
// src/main.jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router';
import App from './App.jsx';
import './index.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
);
```

`<BrowserRouter>`가 앱 전체를 감싸야 React Router 기능을 어디서든 쓸 수 있습니다.

---

<a id="4"></a>
## 4️⃣ Routes 설정 [↑](#toc)

### 문제

앱이 커지면 URL마다 다른 화면을 보여줘야 합니다. 어떻게 "이 URL이면 이 컴포넌트를 보여줘"를 설정할까요?

### 고통

if/else로 URL을 직접 확인하면 코드가 난잡해집니다.

```jsx
// 이렇게 하면 안 됩니다
function App() {
  const path = window.location.pathname;
  if (path === '/') return <Home />;
  if (path === '/about') return <About />;
  // ... URL이 10개면 if가 10개
}
```

### 해결

`<Routes>`와 `<Route>`로 선언적으로 라우팅 규칙을 정의합니다.

```jsx
// src/App.jsx
import { Routes, Route } from 'react-router';
import Home from './pages/Home';
import About from './pages/About';
import Products from './pages/Products';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/products" element={<Products />} />
    </Routes>
  );
}

export default App;
```

```jsx
// src/pages/Home.jsx
function Home() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold">홈 페이지</h1>
      <p className="mt-2 text-gray-600">환영합니다!</p>
    </div>
  );
}

export default Home;
```

URL이 `/`이면 `<Home />`을, `/about`이면 `<About />`을 렌더링합니다.

---

<a id="5"></a>
## 5️⃣ Link와 NavLink [↑](#toc)

### 문제

페이지 이동에 `<a href="/about">` 를 쓰면 어떻게 될까요?

### 고통

```jsx
// 이렇게 쓰면 안 됩니다
<a href="/about">소개</a>
```

`<a>` 태그는 브라우저를 서버로 보내 새 HTML을 요청합니다. SPA의 장점이 사라집니다. 화면이 깜빡이고 React 상태(로그인 정보 등)가 초기화됩니다.

### 해결 — Link

```jsx
// src/components/Navbar.jsx
import { Link } from 'react-router';

function Navbar() {
  return (
    <nav className="bg-white shadow-md px-6 py-4">
      <div className="flex gap-6">
        <Link to="/" className="text-gray-700 hover:text-blue-600 font-medium">
          홈
        </Link>
        <Link to="/about" className="text-gray-700 hover:text-blue-600 font-medium">
          소개
        </Link>
        <Link to="/products" className="text-gray-700 hover:text-blue-600 font-medium">
          상품
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;
```

`<Link to="...">` 는 클릭해도 서버 요청 없이 화면만 교체합니다.

### NavLink — 현재 페이지 강조

`<NavLink>`는 `<Link>`와 동일하지만, **현재 URL과 일치하면 `active` 클래스를 자동으로 붙여줍니다.**

```jsx
import { NavLink } from 'react-router';

function Navbar() {
  return (
    <nav className="bg-white shadow-md px-6 py-4">
      <div className="flex gap-6">
        <NavLink
          to="/"
          className={({ isActive }) =>
            isActive
              ? 'text-blue-600 font-bold border-b-2 border-blue-600 pb-1'
              : 'text-gray-700 hover:text-blue-600 font-medium'
          }
        >
          홈
        </NavLink>
        <NavLink
          to="/about"
          className={({ isActive }) =>
            isActive
              ? 'text-blue-600 font-bold border-b-2 border-blue-600 pb-1'
              : 'text-gray-700 hover:text-blue-600 font-medium'
          }
        >
          소개
        </NavLink>
      </div>
    </nav>
  );
}
```

`className`에 함수를 넘기면 `isActive` 값에 따라 다른 클래스를 적용할 수 있습니다.

---

<a id="6"></a>
## 6️⃣ useNavigate — 코드로 이동하기 [↑](#toc)

### 문제

버튼 클릭이 아닌 **특정 로직 완료 후** 페이지를 이동해야 할 때가 있습니다. 예: 로그인 성공 → 홈으로 이동, 폼 제출 완료 → 목록 페이지로 이동.

### 해결

`useNavigate` 훅으로 코드 안에서 페이지를 이동합니다.

```jsx
// src/pages/Login.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router';

function Login() {
  const [id, setId] = useState('');
  const [pw, setPw] = useState('');
  const navigate = useNavigate();

  const handleLogin = () => {
    // 실제로는 서버 인증을 해야 합니다
    if (id === 'admin' && pw === '1234') {
      alert('로그인 성공!');
      navigate('/');          // 홈으로 이동
    } else {
      alert('아이디 또는 비밀번호가 틀렸습니다.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-xl shadow-md w-80">
        <h2 className="text-2xl font-bold mb-6 text-center">로그인</h2>
        <input
          type="text"
          placeholder="아이디"
          value={id}
          onChange={(e) => setId(e.target.value)}
          className="w-full border rounded-lg px-3 py-2 mb-3 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <input
          type="password"
          placeholder="비밀번호"
          value={pw}
          onChange={(e) => setPw(e.target.value)}
          className="w-full border rounded-lg px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition"
        >
          로그인
        </button>
      </div>
    </div>
  );
}

export default Login;
```

### navigate 주요 사용법

```jsx
navigate('/about');           // /about 으로 이동
navigate(-1);                 // 뒤로 가기 (브라우저 뒤로 버튼과 동일)
navigate(1);                  // 앞으로 가기
navigate('/home', { replace: true }); // 히스토리 교체 (뒤로 가기 방지)
```

---

<a id="7"></a>
## 7️⃣ URL 파라미터 [↑](#toc)

### 문제

상품이 100개 있다면 `<Route path="/product/1">`, `<Route path="/product/2">` ... 100개를 써야 할까요?

### 해결 — 동적 라우트와 useParams

`:id` 처럼 콜론으로 시작하는 부분이 **URL 파라미터**입니다. 어떤 값이 와도 매칭됩니다.

```jsx
// App.jsx에서 라우트 설정
<Route path="/product/:id" element={<ProductDetail />} />
```

```jsx
// src/pages/ProductDetail.jsx
import { useParams } from 'react-router';

// 더미 데이터
const products = [
  { id: '1', name: '노트북', price: 1200000, description: '고성능 노트북입니다.' },
  { id: '2', name: '마우스', price: 35000, description: '무선 마우스입니다.' },
  { id: '3', name: '키보드', price: 89000, description: '기계식 키보드입니다.' },
];

function ProductDetail() {
  const { id } = useParams();  // URL에서 :id 값을 읽음
  const product = products.find((p) => p.id === id);

  if (!product) {
    return (
      <div className="p-8 text-center">
        <p className="text-red-500 text-xl">상품을 찾을 수 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-2">{product.name}</h1>
      <p className="text-blue-600 text-xl font-semibold mb-4">
        {product.price.toLocaleString()}원
      </p>
      <p className="text-gray-600">{product.description}</p>
    </div>
  );
}

export default ProductDetail;
```

```jsx
// 상품 목록에서 링크 연결
import { Link } from 'react-router';

function ProductList() {
  const products = [
    { id: '1', name: '노트북' },
    { id: '2', name: '마우스' },
    { id: '3', name: '키보드' },
  ];

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">상품 목록</h1>
      <ul className="space-y-2">
        {products.map((product) => (
          <li key={product.id}>
            <Link
              to={`/product/${product.id}`}
              className="text-blue-600 hover:underline"
            >
              {product.name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

`/product/1`에 접속하면 `useParams()`가 `{ id: '1' }`을 반환합니다.

---

<a id="8"></a>
## 8️⃣ 중첩 라우트 (Nested Routes) [↑](#toc)

### 문제

대부분의 앱에는 **모든 페이지에 공통으로 표시되는 네비게이션 바와 푸터**가 있습니다. 각 페이지 컴포넌트에 Navbar를 반복해서 넣으면 중복이 생깁니다.

### 해결 — Layout + Outlet

**레이아웃 컴포넌트**를 만들고, 그 안에 `<Outlet />`을 배치합니다. `<Outlet />`은 "여기에 자식 라우트의 컴포넌트를 렌더링해"라는 표시입니다.

```jsx
// src/components/Layout.jsx
import { Outlet } from 'react-router';
import Navbar from './Navbar';

function Layout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-4xl mx-auto px-4 py-8">
        <Outlet />
        {/* 여기에 Home, About, Products 중 하나가 렌더링됩니다 */}
      </main>
      <footer className="text-center py-6 text-gray-400 text-sm border-t mt-8">
        © 2025 My Portfolio
      </footer>
    </div>
  );
}

export default Layout;
```

```jsx
// src/App.jsx — 중첩 라우트 설정
import { Routes, Route } from 'react-router';
import Layout from './components/Layout';
import Home from './pages/Home';
import About from './pages/About';
import Products from './pages/Products';
import ProductDetail from './pages/ProductDetail';
import NotFound from './pages/NotFound';

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        {/* Layout 안의 <Outlet />에 렌더링되는 자식들 */}
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/products" element={<Products />} />
        <Route path="/product/:id" element={<ProductDetail />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
```

이제 `Home`, `About`, `Products`는 모두 같은 `Navbar`와 `footer`를 공유합니다.

---

<a id="9"></a>
## 9️⃣ 404 페이지 [↑](#toc)

`path="*"`은 다른 모든 라우트에 매칭되지 않는 URL을 잡습니다.

```jsx
// src/pages/NotFound.jsx
import { Link } from 'react-router';

function NotFound() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center">
      <p className="text-8xl font-bold text-gray-200 mb-4">404</p>
      <h1 className="text-2xl font-bold text-gray-700 mb-2">
        페이지를 찾을 수 없습니다
      </h1>
      <p className="text-gray-500 mb-8">
        주소를 다시 확인하거나, 아래 버튼으로 홈으로 돌아가세요.
      </p>
      <Link
        to="/"
        className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition font-semibold"
      >
        홈으로 돌아가기
      </Link>
    </div>
  );
}

export default NotFound;
```

---

<a id="10"></a>
## 🔟 실습: 다중 페이지 포트폴리오 [↑](#toc)

지금까지 배운 모든 것을 합쳐서 **4개 페이지로 구성된 포트폴리오 사이트**를 만들어 봅니다.

### 프로젝트 구조

```
portfolio/
├── src/
│   ├── components/
│   │   ├── Layout.jsx
│   │   └── Navbar.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── About.jsx
│   │   ├── Projects.jsx
│   │   ├── ProjectDetail.jsx
│   │   ├── Contact.jsx
│   │   └── NotFound.jsx
│   ├── App.jsx
│   └── main.jsx
```

### App.jsx

```jsx
import { Routes, Route } from 'react-router';
import Layout from './components/Layout';
import Home from './pages/Home';
import About from './pages/About';
import Projects from './pages/Projects';
import ProjectDetail from './pages/ProjectDetail';
import Contact from './pages/Contact';
import NotFound from './pages/NotFound';

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/projects/:id" element={<ProjectDetail />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
```

### Navbar.jsx

```jsx
import { NavLink } from 'react-router';

const links = [
  { to: '/', label: '홈' },
  { to: '/about', label: '소개' },
  { to: '/projects', label: '프로젝트' },
  { to: '/contact', label: '연락처' },
];

function Navbar() {
  return (
    <header className="bg-white border-b px-6 py-4">
      <nav className="max-w-4xl mx-auto flex justify-between items-center">
        <span className="font-bold text-xl text-blue-600">My Portfolio</span>
        <div className="flex gap-6">
          {links.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                isActive
                  ? 'text-blue-600 font-semibold border-b-2 border-blue-600 pb-1'
                  : 'text-gray-600 hover:text-blue-600 transition'
              }
            >
              {label}
            </NavLink>
          ))}
        </div>
      </nav>
    </header>
  );
}

export default Navbar;
```

> `end` prop: `to="/"`일 때 하위 경로(`/about` 등)에서도 홈 링크가 active로 표시되는 것을 방지합니다.

### Projects.jsx (URL 파라미터 예시)

```jsx
import { Link } from 'react-router';

const projects = [
  { id: '1', title: 'ToDo 앱', tech: 'React + Tailwind', desc: '16장에서 만든 Todo 앱' },
  { id: '2', title: '포트폴리오', tech: 'React Router', desc: '이 장에서 만드는 포트폴리오' },
  { id: '3', title: '날씨 앱', tech: 'React + API', desc: '20장 최종 프로젝트' },
];

function Projects() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">프로젝트</h1>
      <div className="grid gap-4 sm:grid-cols-2">
        {projects.map((p) => (
          <Link
            key={p.id}
            to={`/projects/${p.id}`}
            className="block bg-white border rounded-xl p-5 hover:shadow-md transition"
          >
            <h2 className="text-lg font-semibold mb-1">{p.title}</h2>
            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-medium">
              {p.tech}
            </span>
            <p className="text-gray-500 text-sm mt-2">{p.desc}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Projects;
```

### 기본 과제

- [ ] 4개 페이지(Home, About, Projects, Contact)를 만들고 NavLink로 연결하세요.
- [ ] Projects 페이지에서 프로젝트 카드를 클릭하면 상세 페이지로 이동하세요.
- [ ] 존재하지 않는 URL 접속 시 NotFound 페이지가 나타나게 하세요.

### 도전 과제

- [ ] Contact 페이지에 폼을 만들고, 제출 시 `useNavigate`로 홈으로 이동시키세요.
- [ ] NavLink에 마우스를 올리면 부드럽게 색이 바뀌는 애니메이션을 추가하세요.
- [ ] `useSearchParams`를 조사해서 Projects 페이지에 기술 스택 필터를 추가해 보세요.

---

<a id="11"></a>
## 1️⃣1️⃣ 정리 + 브릿지 [↑](#toc)

### 이 장에서 배운 것

| 개념 | 역할 |
|------|------|
| `<BrowserRouter>` | 앱 전체에 라우터 기능 제공 |
| `<Routes>`, `<Route>` | URL → 컴포넌트 매핑 |
| `<Link>`, `<NavLink>` | 서버 요청 없이 페이지 이동 |
| `useNavigate` | 코드에서 직접 페이지 이동 |
| `useParams` | URL 파라미터 읽기 |
| `<Outlet>` | 중첩 라우트의 자식 렌더링 위치 |
| `path="*"` | 404 페이지 |

### 핵심 패턴 요약

```jsx
// main.jsx — BrowserRouter로 감싸기
<BrowserRouter><App /></BrowserRouter>

// App.jsx — 라우트 설정
<Routes>
  <Route element={<Layout />}>
    <Route path="/" element={<Home />} />
    <Route path="/item/:id" element={<ItemDetail />} />
    <Route path="*" element={<NotFound />} />
  </Route>
</Routes>

// 이동 — Link / NavLink / useNavigate
<Link to="/about">소개</Link>
navigate('/home');
```

---

> **브릿지**: 여러 페이지를 가진 앱을 만들 수 있게 되었습니다. 하지만 지금까지 데이터는 모두 코드에 직접 적었습니다. 실제 앱은 서버에서 데이터를 가져옵니다. 다음 장에서 외부 API에서 데이터를 불러오는 방법을 배웁니다.

{% endraw %}
