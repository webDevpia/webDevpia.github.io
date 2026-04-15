---
title: 11. Lifting State Up
layout: default
parent: React
nav_order: 12
permalink: /language/react/lifting-state
---

{% raw %}

# 11장. 컴포넌트 간 상태 공유 — Lifting State Up

## 학습 목표

- 형제 컴포넌트 사이에서 데이터를 공유해야 할 때 발생하는 문제를 이해한다
- 상태를 공통 부모로 올리는(Lifting State Up) 패턴을 익힌다
- "데이터는 아래로, 이벤트는 위로"라는 React의 단방향 데이터 흐름을 이해한다
- 언제 상태를 올려야 하는지 판단 기준을 세울 수 있다

---

<a id="toc"></a>

## 진행 순서

1. [문제: 형제 컴포넌트가 데이터를 공유하려면?](#1)
2. [해결: 상태를 부모로 올리기](#2)
3. [단방향 데이터 흐름](#3)
4. [실전 예제: 온도 변환기](#4)
5. [실전 예제: 검색 + 필터](#5)
6. [언제 Lifting State를 사용하는가?](#6)
7. [실습: 탭 네비게이션](#7)
8. [정리 + 브릿지](#8)

---

<a id="1"></a>
## 1️⃣ 문제: 형제 컴포넌트가 데이터를 공유하려면? [↑](#toc)

### 형제에게 메모 전달하기

학교 교실을 상상해 보세요. 짝꿍에게 메모를 전달하고 싶은데, 선생님(부모)을 통해서만 전달할 수 있는 규칙이 있습니다. 형제끼리 직접 대화하는 통로는 없습니다. React 컴포넌트도 마찬가지입니다. **형제 컴포넌트는 서로 직접 데이터를 주고받을 수 없습니다.**

### 고통: 실제 상황

쇼핑몰 페이지를 만들고 있습니다. 검색창(`SearchBar`)에 키워드를 입력하면 상품 목록(`ProductList`)이 필터링되어야 합니다.

```jsx
// SearchBar가 query 상태를 혼자 가지고 있습니다
function SearchBar() {
  const [query, setQuery] = useState('');

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="상품 검색..."
      className="border rounded px-3 py-2 w-full"
    />
  );
}

// ProductList는 query를 알 수 없습니다 😢
function ProductList() {
  const products = ['사과', '바나나', '오렌지', '포도', '망고'];

  return (
    <ul className="mt-4 space-y-2">
      {products.map((product) => (
        <li key={product} className="p-2 border rounded">
          {product}
        </li>
      ))}
    </ul>
  );
}

// 부모는 두 컴포넌트를 나란히 렌더링합니다
function App() {
  return (
    <div className="p-4">
      <SearchBar />
      <ProductList />
    </div>
  );
}
```

**문제:** `SearchBar`의 `query` 상태가 `ProductList`와 완전히 분리되어 있습니다. 형제끼리 서로의 상태를 읽을 방법이 없습니다.

이것이 바로 **Lifting State Up(상태 올리기)**이 필요한 순간입니다.

---

<a id="2"></a>
## 2️⃣ 해결: 상태를 부모로 올리기 [↑](#toc)

### 원리

**두 컴포넌트가 같은 데이터를 필요로 한다면, 그 데이터를 두 컴포넌트의 공통 부모에 올려야 합니다.**

```
       App (상태 보관소)
      ↙ query    ↘ query
 SearchBar    ProductList
 (query 표시)  (query로 필터링)
```

부모가 상태를 가지고, 자식들에게는 두 가지를 내려줍니다.

- **데이터(props):** `query` 값 → 자식이 화면에 표시하거나 사용
- **콜백(callbacks):** `setQuery` 함수 → 자식이 상태 변경을 요청

```jsx
// 상태를 부모로 올렸습니다 ✅
function App() {
  const [query, setQuery] = useState('');

  return (
    <div className="p-4">
      {/* 자식에게 값과 변경 함수를 내려줍니다 */}
      <SearchBar query={query} onQueryChange={setQuery} />
      <ProductList query={query} />
    </div>
  );
}

// SearchBar는 이제 상태를 직접 갖지 않습니다
function SearchBar({ query, onQueryChange }) {
  return (
    <input
      value={query}
      onChange={(e) => onQueryChange(e.target.value)}
      placeholder="상품 검색..."
      className="border rounded px-3 py-2 w-full"
    />
  );
}

// ProductList는 query를 받아서 필터링합니다
function ProductList({ query }) {
  const products = ['사과', '바나나', '오렌지', '포도', '망고'];
  const filtered = products.filter((p) =>
    p.includes(query)
  );

  return (
    <ul className="mt-4 space-y-2">
      {filtered.map((product) => (
        <li key={product} className="p-2 border rounded">
          {product}
        </li>
      ))}
    </ul>
  );
}
```

이제 `SearchBar`에서 입력하면 → `App`의 `query`가 바뀌고 → `ProductList`가 새 `query`로 다시 필터링합니다.

---

<a id="3"></a>
## 3️⃣ 단방향 데이터 흐름 [↑](#toc)

이것이 React의 핵심 철학입니다.

```
┌─────────────────────────────────┐
│              App                │
│         (상태 보관소)            │
│    const [query, setQuery]      │
└──────────┬──────────┬───────────┘
           │ props    │ props
     (데이터 아래로)   (콜백 아래로)
           ↓          ↓
    ┌──────────┐ ┌────────────┐
    │SearchBar │ │ProductList │
    │(이벤트   │ │(query 사용)│
    │ 위로 ↑)  │ │            │
    └──────────┘ └────────────┘
```

| 방향 | 무엇 | 방법 |
|------|------|------|
| 아래로 ↓ | 데이터 | props |
| 위로 ↑ | 이벤트/요청 | callback 함수 |

React에서 데이터는 **항상 부모 → 자식** 방향으로만 흐릅니다. 자식이 데이터를 변경하고 싶을 때는 부모가 내려준 **콜백 함수를 호출**하는 방식으로 "요청"합니다. 실제 상태 변경은 항상 상태를 소유한 부모가 합니다.

이 단방향 흐름 덕분에 데이터가 어디서 어떻게 바뀌는지 **추적하기 쉬워집니다.**

---

<a id="4"></a>
## 4️⃣ 실전 예제: 온도 변환기 [↑](#toc)

섭씨 입력창과 화씨 입력창이 서로 동기화되는 고전적인 예제입니다. 하나를 바꾸면 다른 하나도 자동으로 바뀝니다.

```jsx
// 변환 유틸리티 함수
function toFahrenheit(celsius) {
  return (celsius * 9) / 5 + 32;
}

function toCelsius(fahrenheit) {
  return ((fahrenheit - 32) * 5) / 9;
}

// 재사용 가능한 온도 입력 컴포넌트
function TemperatureInput({ scale, value, onValueChange }) {
  const label = scale === 'c' ? '섭씨 (°C)' : '화씨 (°F)';

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      <input
        type="number"
        value={value}
        onChange={(e) => onValueChange(e.target.value)}
        className="border rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
    </div>
  );
}

// 상태는 부모가 보관합니다
function Calculator() {
  const [celsius, setCelsius] = useState('');

  // 파생 값은 렌더링 중에 계산합니다 (useEffect 불필요)
  const fahrenheit = celsius !== '' ? toFahrenheit(Number(celsius)) : '';

  function handleCelsiusChange(value) {
    setCelsius(value);
  }

  function handleFahrenheitChange(value) {
    if (value === '') {
      setCelsius('');
    } else {
      setCelsius(String(toCelsius(Number(value))));
    }
  }

  return (
    <div className="max-w-sm mx-auto p-6 bg-white rounded-xl shadow">
      <h2 className="text-xl font-bold mb-4 text-center">온도 변환기</h2>
      <TemperatureInput
        scale="c"
        value={celsius}
        onValueChange={handleCelsiusChange}
      />
      <TemperatureInput
        scale="f"
        value={fahrenheit}
        onValueChange={handleFahrenheitChange}
      />
      {celsius !== '' && (
        <p className="text-center text-gray-600 mt-2">
          {celsius}°C = {Number(fahrenheit).toFixed(2)}°F
        </p>
      )}
    </div>
  );
}
```

**핵심 포인트:** 상태는 섭씨(`celsius`) 하나만 저장합니다. 화씨는 렌더링 중에 계산하는 **파생 값(derived value)**입니다. 두 값을 별도 상태로 관리하면 동기화 문제가 생깁니다.

---

<a id="5"></a>
## 5️⃣ 실전 예제: 검색 + 필터 [↑](#toc)

앞서 보았던 문제를 완전히 해결합니다. 이번에는 실제 상품 데이터와 함께 구현합니다.

```jsx
const PRODUCTS = [
  { id: 1, name: '맥북 프로', category: '노트북', price: 2500000 },
  { id: 2, name: '아이패드', category: '태블릿', price: 900000 },
  { id: 3, name: '아이폰 15', category: '스마트폰', price: 1200000 },
  { id: 4, name: '갤럭시 S24', category: '스마트폰', price: 1100000 },
  { id: 5, name: '갤럭시 탭', category: '태블릿', price: 700000 },
];

function SearchBar({ query, onQueryChange }) {
  return (
    <div className="mb-4">
      <input
        type="text"
        value={query}
        onChange={(e) => onQueryChange(e.target.value)}
        placeholder="상품명 검색..."
        className="border rounded-lg px-4 py-2 w-full shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
    </div>
  );
}

function ProductList({ products }) {
  if (products.length === 0) {
    return (
      <p className="text-center text-gray-400 py-8">
        검색 결과가 없습니다.
      </p>
    );
  }

  return (
    <ul className="space-y-2">
      {products.map((product) => (
        <li
          key={product.id}
          className="flex justify-between items-center p-3 border rounded-lg hover:bg-gray-50"
        >
          <div>
            <span className="font-medium">{product.name}</span>
            <span className="ml-2 text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded">
              {product.category}
            </span>
          </div>
          <span className="text-indigo-600 font-semibold">
            {product.price.toLocaleString()}원
          </span>
        </li>
      ))}
    </ul>
  );
}

// 부모가 상태를 보관합니다
function ProductPage() {
  const [query, setQuery] = useState('');

  const filteredProducts = PRODUCTS.filter((p) =>
    p.name.includes(query) || p.category.includes(query)
  );

  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">상품 목록</h1>
      <SearchBar query={query} onQueryChange={setQuery} />
      <p className="text-sm text-gray-500 mb-2">
        {filteredProducts.length}개 상품
      </p>
      <ProductList products={filteredProducts} />
    </div>
  );
}
```

---

<a id="6"></a>
## 6️⃣ 언제 Lifting State를 사용하는가? [↑](#toc)

### 판단 기준

다음 질문에 "예"가 하나라도 있다면 상태를 올려야 합니다.

| 질문 | 예 → 올리기 |
|------|------------|
| 두 컴포넌트가 같은 데이터를 보여주는가? | ✅ |
| 한 컴포넌트의 변경이 다른 컴포넌트에 영향을 주는가? | ✅ |
| 여러 컴포넌트가 같은 데이터를 기반으로 계산하는가? | ✅ |

### 어디까지 올려야 하나?

**공통 부모 중 가장 가까운 곳**까지만 올립니다. 필요 이상으로 올리면 코드가 복잡해집니다.

```
App
├── Header
├── Main
│   ├── SearchBar  ← query 필요
│   └── ProductList ← query 필요
└── Footer

→ query 상태는 Main에 두면 됩니다 (App까지 올릴 필요 없음)
```

### 올리지 않아도 되는 경우

- 상태가 한 컴포넌트에서만 사용될 때
- 부모/조상 중 누구도 해당 상태를 필요로 하지 않을 때

```jsx
// 이 경우 isOpen은 Modal 내부에만 있으면 충분합니다
function Modal() {
  const [isOpen, setIsOpen] = useState(false);
  // ...
}
```

---

<a id="7"></a>
## 7️⃣ 실습: 탭 네비게이션 [↑](#toc)

탭 버튼과 콘텐츠 패널이 `activeTab` 상태를 공유하는 컴포넌트를 만들어 봅시다.

### 요구사항

- 탭: 홈, 프로필, 설정 (3개)
- 탭 버튼 클릭 → 해당 탭 콘텐츠 표시
- 활성 탭은 파란색으로 강조

### 기본 과제

```jsx
const TABS = [
  { id: 'home', label: '홈', content: '홈 화면입니다. 최신 소식을 확인하세요.' },
  { id: 'profile', label: '프로필', content: '프로필 화면입니다. 내 정보를 수정할 수 있습니다.' },
  { id: 'settings', label: '설정', content: '설정 화면입니다. 앱 환경을 변경하세요.' },
];

function TabButtons({ activeTab, onTabChange }) {
  return (
    <div className="flex border-b">
      {TABS.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === tab.id
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}

function TabContent({ activeTab }) {
  const current = TABS.find((tab) => tab.id === activeTab);
  return (
    <div className="p-4 text-gray-700">
      {current?.content}
    </div>
  );
}

// TODO: TabContainer 컴포넌트를 완성하세요
// activeTab 상태를 여기서 관리하고
// TabButtons와 TabContent에 전달하세요
function TabContainer() {
  // 여기를 완성하세요
}
```

### 도전 과제

1. 탭에 숫자 배지 추가하기 (예: "알림 (3)")
2. 탭 전환 시 페이드 애니메이션 추가 (Tailwind `transition-opacity`)
3. URL 해시(`#home`, `#profile`)와 탭 상태 동기화하기

---

<a id="8"></a>
## 8️⃣ 정리 + 브릿지 [↑](#toc)

### 이번 장에서 배운 것

| 개념 | 내용 |
|------|------|
| Lifting State Up | 공통 부모로 상태를 올려 자식들이 공유 |
| 단방향 데이터 흐름 | 데이터는 아래로(props), 이벤트는 위로(callbacks) |
| 공통 부모 찾기 | 두 컴포넌트 모두 접근할 수 있는 가장 가까운 조상 |
| 파생 값 | 상태에서 계산 가능한 값은 별도 상태로 관리하지 않음 |

### 핵심 원칙

> 두 컴포넌트가 같은 데이터를 보여주거나 영향을 주면, 그 데이터는 공통 부모에 있어야 합니다.

### 다음 장 예고

컴포넌트 간 데이터 공유를 배웠습니다. 이제 배운 모든 것(JSX, 컴포넌트, props, state, 이벤트, 폼, 리스트, 조건부 렌더링, Lifting State)을 합쳐서 **실전 ToDo 앱 프로젝트**를 만들어 봅시다. 지금까지의 학습을 하나의 완성된 애플리케이션으로 통합하는 시간입니다!

{% endraw %}
