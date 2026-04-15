---
title: 02. JSX와 컴포넌트
layout: default
parent: React
nav_order: 3
permalink: /language/react/jsx-components
---

{% raw %}

# 02장. JSX와 컴포넌트

> "컴포넌트 = 레고 블록 — 작은 블록을 조합해서 큰 구조물을 만듭니다."

레고를 생각해보세요. 집 한 채를 만들 때 아무도 처음부터 끝까지 한 덩어리로 만들지 않습니다. 벽 블록, 창문 블록, 지붕 블록을 따로 만들어서 조립합니다. React의 컴포넌트도 똑같습니다. 화면을 작은 조각으로 나누고, 조합해서 완성된 UI를 만듭니다.

---

## 학습 목표

- 컴포넌트가 무엇인지, 왜 필요한지 설명할 수 있다
- JSX와 HTML의 차이를 이해하고 JSX를 올바르게 작성할 수 있다
- JSX 안에서 JavaScript 표현식을 사용할 수 있다
- 컴포넌트를 파일로 분리하고 import/export할 수 있다
- Fragment를 사용해 불필요한 감싸기 태그를 없앨 수 있다

---

<a id="toc"></a>
## 진행 순서
1. [컴포넌트란?](#1)
2. [JSX란?](#2)
3. [JSX에서 JavaScript 표현식 사용하기](#3)
4. [컴포넌트 분리하기](#4)
5. [Fragment](#5)
6. [실습: 자기소개 카드 만들기](#6)
7. [정리](#summary)

---

<a id="1"></a>
## 1️⃣ 컴포넌트란? [↑](#toc)

### 문제: 모든 코드가 한 파일에

처음 HTML을 배울 때는 파일 하나에 모든 내용을 넣었습니다. 작은 페이지라면 괜찮지만, 복잡한 앱이 되면 1,000줄이 넘는 파일을 혼자 관리하게 됩니다. 어디를 수정해야 할지 찾는 것만으로도 시간이 걸립니다.

### 고통: 같은 UI를 여러 곳에 복붙

네이버나 쿠팡의 상품 카드를 생각해보세요. 수백 개의 카드가 있는데, 카드 디자인을 바꾸려면 수백 줄을 수정해야 합니다. 하나를 놓치면 버그가 생깁니다.

### 해결: 컴포넌트

```jsx
// 한 번 만들고, 여러 곳에서 재사용
function ProductCard() {
  return (
    <div className="border rounded-lg p-4 shadow">
      <img src="product.jpg" alt="상품" className="w-full" />
      <h3 className="font-bold mt-2">상품 이름</h3>
      <p className="text-blue-600 font-bold">₩29,900</p>
    </div>
  );
}

// App에서 여러 번 사용
function App() {
  return (
    <div className="grid grid-cols-3 gap-4">
      <ProductCard />
      <ProductCard />
      <ProductCard />
    </div>
  );
}
```

나중에 카드 디자인을 바꾸려면 `ProductCard` 함수 하나만 수정하면 됩니다.

### 컴포넌트의 규칙

**1. 컴포넌트 이름은 반드시 대문자로 시작합니다 (PascalCase)**

```jsx
// 올바른 예
function UserCard() { ... }
function WeatherWidget() { ... }
function NavBar() { ... }

// 잘못된 예 — 소문자로 시작하면 React가 HTML 태그로 인식합니다
function userCard() { ... }  // ❌
```

**2. 반드시 JSX(또는 null)를 반환합니다**

```jsx
// 반환값이 있어야 합니다
function Greeting() {
  return <h1>안녕하세요!</h1>;
}

// 아무것도 표시하지 않으려면 null을 반환합니다
function Hidden() {
  return null;
}
```

**3. 함수형 컴포넌트를 사용합니다 (React 16.8 이후 표준)**

```jsx
// 함수 선언식
function MyComponent() {
  return <div>내용</div>;
}

// 화살표 함수 (같은 결과)
const MyComponent = () => {
  return <div>내용</div>;
};

// 둘 다 옳습니다. 이 강의에서는 함수 선언식을 주로 사용합니다.
```

---

<a id="2"></a>
## 2️⃣ JSX란? [↑](#toc)

### JSX = JavaScript 안의 HTML처럼 생긴 문법

JSX는 "JavaScript XML"의 약자입니다. HTML처럼 보이지만 실제로는 JavaScript입니다. 브라우저는 JSX를 직접 이해하지 못하며, Vite가 빌드할 때 일반 JavaScript로 변환해줍니다.

```jsx
// 우리가 쓰는 JSX
const element = <h1 className="title">안녕하세요</h1>;

// Vite가 변환한 실제 JavaScript
const element = React.createElement("h1", { className: "title" }, "안녕하세요");
```

직접 `React.createElement`를 쓰지 않아도 되는 이유가 JSX입니다.

### JSX와 HTML의 차이점

| HTML | JSX | 이유 |
|------|-----|------|
| `class="..."` | `className="..."` | `class`는 JavaScript 예약어 |
| `for="..."` | `htmlFor="..."` | `for`도 JavaScript 예약어 |
| `onclick="..."` | `onClick={...}` | 이벤트는 camelCase |
| `<input>` | `<input />` | 모든 태그는 반드시 닫아야 함 |
| `<img>` | `<img />` | 자기 닫기 태그도 슬래시 필요 |
| 주석: `<!-- -->` | `{/* 주석 */}` | JS 주석 방식 |

### JSX 작성 규칙

**규칙 1: 반드시 하나의 부모 태그가 있어야 합니다**

```jsx
// ❌ 에러 — 두 개의 루트 요소
function Wrong() {
  return (
    <h1>제목</h1>
    <p>내용</p>
  );
}

// ✅ 올바름 — div로 감쌈
function Right() {
  return (
    <div>
      <h1>제목</h1>
      <p>내용</p>
    </div>
  );
}
```

**규칙 2: 모든 태그는 닫아야 합니다**

```jsx
// ❌ HTML에서는 괜찮지만 JSX에서는 에러
<input type="text">
<br>
<img src="photo.jpg">

// ✅ 자기 닫기 태그 사용
<input type="text" />
<br />
<img src="photo.jpg" />
```

**규칙 3: 속성은 camelCase**

```jsx
// ❌
<div tabindex="0" maxlength="10" backgroundcolor="blue">

// ✅
<div tabIndex="0" maxLength="10" backgroundColor="blue">
```

예외: `data-` 속성과 `aria-` 속성은 그대로 사용합니다.

```jsx
<div data-testid="my-div" aria-label="설명">
```

### JSX를 예쁘게 작성하는 방법

여러 줄에 걸친 JSX는 소괄호로 감쌉니다.

```jsx
function LongComponent() {
  return (
    <div className="container">
      <header>
        <h1>제목</h1>
      </header>
      <main>
        <p>내용</p>
      </main>
    </div>
  );
}
```

---

<a id="3"></a>
## 3️⃣ JSX에서 JavaScript 표현식 사용하기 [↑](#toc)

JSX 안에서 `{중괄호}`를 사용하면 JavaScript 표현식을 넣을 수 있습니다.

### 변수 출력

```jsx
function Greeting() {
  const name = "Alice";
  const year = new Date().getFullYear();

  return (
    <div>
      <h1>안녕하세요, {name}님!</h1>
      <p>현재 연도: {year}</p>
    </div>
  );
}
```

### 계산식

```jsx
function Receipt() {
  const price = 29000;
  const quantity = 3;

  return (
    <div>
      <p>단가: {price.toLocaleString()}원</p>
      <p>수량: {quantity}개</p>
      <p>합계: {(price * quantity).toLocaleString()}원</p>
    </div>
  );
}
```

### 삼항 연산자 (조건부 내용)

```jsx
function UserBadge({ isAdmin }) {
  return (
    <span className={isAdmin ? "bg-red-500 text-white" : "bg-gray-200"}>
      {isAdmin ? "관리자" : "일반 사용자"}
    </span>
  );
}
```

### && 연산자 (조건부 렌더링)

```jsx
function Notification({ hasNewMessage, messageCount }) {
  return (
    <div>
      <h2>알림</h2>
      {hasNewMessage && (
        <p className="text-blue-600">
          새 메시지가 {messageCount}개 있습니다.
        </p>
      )}
    </div>
  );
}
```

### 함수 호출

```jsx
function formatDate(date) {
  return date.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

function DateDisplay() {
  return (
    <p>오늘: {formatDate(new Date())}</p>
  );
}
```

### 주의: 객체와 boolean은 직접 출력 불가

```jsx
// ❌ 에러 — 객체는 직접 출력할 수 없습니다
const user = { name: "Alice" };
<p>{user}</p>

// ✅ 속성을 꺼내서 출력하세요
<p>{user.name}</p>

// ❌ false, true, null은 화면에 표시되지 않습니다
<p>{false}</p>  // 아무것도 표시 안 됨

// ✅ 문자열로 변환하면 됩니다
<p>{String(false)}</p>  // "false" 표시
```

---

<a id="4"></a>
## 4️⃣ 컴포넌트 분리하기 [↑](#toc)

### 왜 파일을 분리하나요?

컴포넌트 수가 늘어나면 `App.jsx` 하나에 모두 넣기가 버거워집니다. 파일을 나누면:
- 각 파일의 역할이 명확해집니다
- 팀으로 작업할 때 충돌이 줄어듭니다
- 원하는 컴포넌트를 찾기 쉬워집니다

### 폴더 구조 만들기

```
src/
├── components/          ← 컴포넌트 파일들
│   ├── Header.jsx
│   ├── Footer.jsx
│   └── Card.jsx
├── App.jsx
└── main.jsx
```

### Header 컴포넌트 만들기

```jsx
// src/components/Header.jsx
function Header() {
  return (
    <header className="bg-blue-600 text-white px-6 py-4 flex items-center justify-between">
      <h1 className="text-xl font-bold">날씨 앱</h1>
      <nav className="flex gap-4">
        <a href="/" className="hover:underline">홈</a>
        <a href="/about" className="hover:underline">소개</a>
      </nav>
    </header>
  );
}

export default Header;
```

### Footer 컴포넌트 만들기

```jsx
// src/components/Footer.jsx
function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-gray-800 text-gray-400 text-center py-6 text-sm">
      <p>© {year} 날씨 앱. All rights reserved.</p>
    </footer>
  );
}

export default Footer;
```

### Card 컴포넌트 만들기

```jsx
// src/components/Card.jsx
function Card() {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
      <h2 className="text-lg font-semibold text-gray-800 mb-2">카드 제목</h2>
      <p className="text-gray-500">카드 내용이 여기에 들어갑니다.</p>
    </div>
  );
}

export default Card;
```

### App.jsx에서 조합하기

```jsx
// src/App.jsx
import Header from "./components/Header";
import Footer from "./components/Footer";
import Card from "./components/Card";

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />

      <main className="flex-1 container mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">오늘의 날씨</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card />
          <Card />
          <Card />
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
```

### 브라우저에서 확인

DevTools의 Components 탭을 열면 이제 트리가 깊어졌습니다.

```
App
├── Header
├── main
│   ├── Card
│   ├── Card
│   └── Card
└── Footer
```

각 컴포넌트를 클릭하면 해당 컴포넌트의 정보를 볼 수 있습니다.

---

<a id="5"></a>
## 5️⃣ Fragment [↑](#toc)

### 문제: 불필요한 div가 생깁니다

JSX는 하나의 루트 요소를 요구합니다. 그래서 의미 없는 `<div>`로 감싸는 경우가 생깁니다.

```jsx
// 의미 없는 div가 HTML에 추가됩니다
function LabeledInput() {
  return (
    <div>
      <label htmlFor="name">이름</label>
      <input id="name" type="text" />
    </div>
  );
}
```

### 해결: Fragment

Fragment는 DOM에 실제 요소를 추가하지 않는 투명한 래퍼입니다.

```jsx
// 방법 1: <Fragment> 태그 사용
import { Fragment } from "react";

function LabeledInput() {
  return (
    <Fragment>
      <label htmlFor="name">이름</label>
      <input id="name" type="text" />
    </Fragment>
  );
}

// 방법 2: 단축 문법 <> </> (더 자주 씁니다)
function LabeledInput() {
  return (
    <>
      <label htmlFor="name">이름</label>
      <input id="name" type="text" />
    </>
  );
}
```

### key가 필요할 때는 Fragment 명시 사용

`map`으로 목록을 렌더링할 때 `key`가 필요하면 단축 문법 `<>`을 쓸 수 없습니다.

```jsx
import { Fragment } from "react";

const items = [
  { id: 1, title: "항목 1", desc: "설명 1" },
  { id: 2, title: "항목 2", desc: "설명 2" },
];

function List() {
  return (
    <dl>
      {items.map(item => (
        <Fragment key={item.id}>
          <dt className="font-bold">{item.title}</dt>
          <dd className="text-gray-600 mb-2">{item.desc}</dd>
        </Fragment>
      ))}
    </dl>
  );
}
```

---

<a id="6"></a>
## 6️⃣ 실습: 자기소개 카드 만들기 [↑](#toc)

지금까지 배운 내용으로 자기소개 카드를 만들어봅시다.

### 완성 목표

- 이름, 직업, 자기소개 문구가 있는 카드
- 기술 스택 태그 목록
- 연락처 링크

### 단계별 구현

**Step 1: ProfileCard.jsx 만들기**

```jsx
// src/components/ProfileCard.jsx
function ProfileCard() {
  const profile = {
    name: "홍길동",
    role: "프론트엔드 개발자",
    bio: "React와 TypeScript를 좋아합니다. 사용자 경험을 개선하는 것에 관심이 많습니다.",
    skills: ["React", "JavaScript", "Tailwind CSS", "Git"],
    github: "https://github.com/username",
    email: "user@example.com",
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-8 max-w-sm mx-auto">
      {/* 아바타 */}
      <div className="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
        {profile.name[0]}
      </div>

      {/* 이름과 직업 */}
      <h1 className="text-2xl font-bold text-center text-gray-800">
        {profile.name}
      </h1>
      <p className="text-blue-600 text-center mt-1">{profile.role}</p>

      {/* 구분선 */}
      <hr className="my-4 border-gray-100" />

      {/* 자기소개 */}
      <p className="text-gray-600 text-sm leading-relaxed text-center">
        {profile.bio}
      </p>

      {/* 기술 스택 */}
      <div className="mt-4 flex flex-wrap gap-2 justify-center">
        {profile.skills.map(skill => (
          <span
            key={skill}
            className="bg-blue-50 text-blue-700 text-xs font-medium px-3 py-1 rounded-full"
          >
            {skill}
          </span>
        ))}
      </div>

      {/* 연락처 */}
      <div className="mt-6 flex justify-center gap-4">
        <a
          href={profile.github}
          className="text-gray-500 hover:text-gray-900 text-sm font-medium"
          target="_blank"
          rel="noopener noreferrer"
        >
          GitHub
        </a>
        <a
          href={`mailto:${profile.email}`}
          className="text-gray-500 hover:text-gray-900 text-sm font-medium"
        >
          이메일
        </a>
      </div>
    </div>
  );
}

export default ProfileCard;
```

**Step 2: App.jsx에서 사용하기**

```jsx
// src/App.jsx
import ProfileCard from "./components/ProfileCard";

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <ProfileCard />
    </div>
  );
}

export default App;
```

### 🔍 React DevTools로 확인

1. Components 탭에서 `App > ProfileCard` 트리를 확인하세요
2. `ProfileCard`를 클릭하면 내부 상태를 볼 수 있습니다
3. `<>` 단축 문법으로 감싼 부분이 트리에서 어떻게 보이는지 확인하세요

---

## 실습 과제

### 기본 과제

`profile` 객체의 정보를 자신의 정보로 바꿔보세요.
- 이름, 직업, 자기소개를 변경하세요
- skills 배열에 본인이 알고 있는 기술을 넣으세요

### 도전 과제

카드를 3개 만들고 나란히 배치해보세요. 각 카드에 다른 프로필 정보를 넣어보세요.

힌트: App.jsx에서

```jsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
  <ProfileCard />
  <ProfileCard />
  <ProfileCard />
</div>
```

문제: 3개 카드가 모두 같은 내용입니다. 이 문제를 어떻게 해결할까요? → **다음 장에서 배웁니다!**

---

<a id="summary"></a>
## 정리 [↑](#toc)

| 개념 | 핵심 내용 |
|------|-----------|
| 컴포넌트 | UI를 나누는 함수. 이름은 PascalCase |
| JSX | HTML처럼 보이지만 JavaScript. `className`, camelCase 속성 |
| 표현식 | `{변수}`, `{함수()}`, `{조건 ? A : B}` |
| 분리 | `export default` → 다른 파일에서 `import` |
| Fragment | `<>...</>` — DOM에 흔적을 남기지 않는 투명한 래퍼 |

**컴포넌트를 만들었지만 아직 밋밋합니다.**  
자기소개 카드의 3개 버전이 모두 같은 내용인 것도 눈치채셨나요? 다음 장에서는 Tailwind CSS로 더 예쁘게 꾸미고, 04장에서는 Props를 배워서 각 카드에 다른 데이터를 넣는 방법을 배웁니다. 일단 지금은 디자인부터 개선해봅시다.

**[→ 03장: 스타일링 (Tailwind CSS)](/language/react-new/styling)**

{% endraw %}
