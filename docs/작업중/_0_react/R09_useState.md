---
title: 08. useState — 컴포넌트의 기억
layout: default
parent: React (리뉴얼)
nav_order: 9
permalink: /language/react-new/usestate
---

{% raw %}

# 08장. useState — 컴포넌트의 기억

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다.

- 일반 변수가 화면을 업데이트하지 못하는 이유를 설명할 수 있다
- `useState`로 상태를 선언하고 업데이트할 수 있다
- 문자열, 불리언 등 다양한 타입의 상태를 관리할 수 있다
- 상태 업데이트가 비동기임을 이해하고 함수형 업데이터를 사용할 수 있다
- React DevTools로 상태 변화를 실시간 확인할 수 있다

---

## 진행 순서

<a id="toc"></a>

1. [컴포넌트의 기억 — 비유로 시작하기](#1)
2. [왜 일반 변수가 안 되는가?](#2)
3. [useState 기본 — 드디어 화면이 바뀝니다](#3)
4. [문자열 상태 — 텍스트 토글](#4)
5. [불리언 상태 — 보이기/숨기기](#5)
6. [중요: 상태 업데이트는 비동기입니다](#6)
7. [React DevTools로 상태 확인하기](#7)
8. [실습: 카운터 앱 + 글자색 토글](#8)
9. [정리 + 브릿지](#9)

---

<a id="1"></a>
## 1️⃣ 컴포넌트의 기억 — 비유로 시작하기 [↑](#toc)

React 공식 문서는 State를 이렇게 설명합니다.

> **"State = 컴포넌트의 기억"**

쇼핑 카트를 생각해봅니다.

- 상품을 담으면 카트가 "기억"합니다
- 다음 페이지로 이동해도 카트의 내용은 유지됩니다
- "비우기" 버튼을 누르면 기억이 초기화됩니다

컴포넌트의 **State**도 같습니다.

- 버튼을 클릭하면 숫자가 "기억"됩니다 (`count`)
- 다른 상태가 바뀌어 다시 렌더링되어도 `count`는 유지됩니다
- "초기화" 버튼을 누르면 `count`가 0으로 돌아갑니다

이 장에서 배울 `useState`가 바로 컴포넌트에게 기억 능력을 부여하는 Hook입니다.

---

<a id="2"></a>
## 2️⃣ 왜 일반 변수가 안 되는가? [↑](#toc)

### 시도: 일반 변수로 카운터 만들기

```jsx
// src/App.jsx
function Counter() {
  let count = 0; // 일반 변수

  function handleClick() {
    count = count + 1;
    console.log("count:", count); // 콘솔에는 1, 2, 3... 출력됨
  }

  return (
    <div className="text-center p-8">
      <p className="text-4xl font-bold mb-4">{count}</p>
      <button
        onClick={handleClick}
        className="bg-blue-500 text-white px-6 py-2 rounded-lg"
      >
        +1
      </button>
    </div>
  );
}
// 버튼을 클릭해도 화면의 숫자는 0 그대로입니다!
// 콘솔에는 1, 2, 3이 찍히지만 화면은 바뀌지 않습니다
```

**왜 count는 바뀌는데 화면은 안 바뀔까요?**

React가 화면을 다시 그리려면(re-render) **"뭔가 바뀌었어"** 라는 신호가 필요합니다.

일반 변수가 바뀐다고 해서 React는 알 수가 없습니다. React 입장에서는 아무 일도 안 생긴 것입니다.

게다가 더 큰 문제가 있습니다. 어떤 이유로 React가 다시 렌더링된다면, `Counter` 함수가 다시 실행되면서 `let count = 0` 이 다시 실행되어 count가 0으로 초기화됩니다.

```
1. 버튼 클릭 → count = 1 (변수는 바뀌었지만)
2. React는 모름 → 화면 그대로
3. 만약 렌더링이 일어나면 → let count = 0 → 다시 초기화
```

**필요한 것은 두 가지입니다:**
1. 렌더링 간에 데이터를 기억하는 공간
2. 데이터가 바뀌면 React에게 "다시 그려!"라고 신호하는 방법

이것을 해결하는 것이 **`useState`** 입니다.

---

<a id="3"></a>
## 3️⃣ useState 기본 — 드디어 화면이 바뀝니다 [↑](#toc)

### useState 사용법

```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);
  //     ↑      ↑           ↑
  //   현재값  업데이트함수  초기값

  function handleClick() {
    setCount(count + 1); // setCount를 호출하면 React에게 "다시 그려!" 신호가 갑니다
  }

  return (
    <div className="text-center p-8">
      <p className="text-6xl font-bold mb-6 text-blue-600">{count}</p>
      <button
        onClick={handleClick}
        className="bg-blue-500 text-white px-8 py-3 rounded-xl text-lg font-medium hover:bg-blue-600 active:scale-95 transition-all"
      >
        +1
      </button>
    </div>
  );
}

export default Counter;
// 버튼 클릭 시마다 화면의 숫자가 1씩 증가합니다!
// 출력: 0 → 1 → 2 → 3 ...
```

**와! 이제 화면이 바뀝니다!**

### 해부학: useState가 하는 일

```jsx
const [count, setCount] = useState(0);
```

이 한 줄이 하는 일을 풀어서 설명합니다.

1. `useState(0)` → "0을 초기값으로 상태를 만들어줘"
2. `[count, setCount]` → 배열 구조 분해 할당으로 두 값을 꺼냄
   - `count` → 현재 상태값 (처음에는 0)
   - `setCount` → 상태를 업데이트하는 함수
3. `setCount(새값)` 호출 → React가 알림을 받고 → 컴포넌트를 다시 렌더링 → 화면이 바뀜

### 이름 규칙

`set` + 상태이름 (camelCase)이 관례입니다.

```jsx
const [count, setCount] = useState(0);
const [name, setName] = useState("");
const [isOpen, setIsOpen] = useState(false);
const [items, setItems] = useState([]);
const [user, setUser] = useState(null);
```

---

<a id="4"></a>
## 4️⃣ 문자열 상태 — 텍스트 토글 [↑](#toc)

숫자뿐만 아니라 문자열도 상태로 관리할 수 있습니다.

```jsx
import { useState } from "react";

function LikeButton() {
  const [liked, setLiked] = useState(false);

  function handleClick() {
    setLiked(!liked); // false → true → false → ...
  }

  return (
    <button
      onClick={handleClick}
      className={`px-6 py-3 rounded-full font-semibold text-lg transition-all ${
        liked
          ? "bg-red-500 text-white shadow-lg scale-105"
          : "bg-gray-100 text-gray-600 hover:bg-gray-200"
      }`}
    >
      {liked ? "❤️ 좋아요 취소" : "🤍 좋아요"}
    </button>
  );
}
// 클릭 전: 회색 "🤍 좋아요" 버튼
// 클릭 후: 빨간 "❤️ 좋아요 취소" 버튼 (크기도 살짝 커짐)
// 다시 클릭: 원래 상태로
```

### 여러 상태 함께 사용

```jsx
import { useState } from "react";

function ProfileCard() {
  const [name, setName] = useState("김철수");
  const [role, setRole] = useState("개발자");
  const [isEditing, setIsEditing] = useState(false);

  return (
    <div className="bg-white p-6 rounded-xl shadow-md max-w-sm">
      {isEditing ? (
        <div className="space-y-3">
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full border rounded px-3 py-2"
            placeholder="이름"
          />
          <input
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="w-full border rounded px-3 py-2"
            placeholder="역할"
          />
          <button
            onClick={() => setIsEditing(false)}
            className="w-full bg-blue-500 text-white py-2 rounded"
          >
            저장
          </button>
        </div>
      ) : (
        <div>
          <h2 className="text-xl font-bold">{name}</h2>
          <p className="text-gray-500">{role}</p>
          <button
            onClick={() => setIsEditing(true)}
            className="mt-4 text-blue-500 hover:underline text-sm"
          >
            수정
          </button>
        </div>
      )}
    </div>
  );
}
// 초기: "김철수 / 개발자" 와 "수정" 링크
// 수정 클릭 후: 이름/역할 입력 필드와 "저장" 버튼
// 저장 후: 변경된 이름/역할로 프로필 표시
```

---

<a id="5"></a>
## 5️⃣ 불리언 상태 — 보이기/숨기기 [↑](#toc)

불리언 상태는 "열림/닫힘", "보임/숨김" 같은 토글에 자주 사용됩니다.

```jsx
import { useState } from "react";

function Spoiler({ title, content }) {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div className="border rounded-lg overflow-hidden max-w-md">
      <button
        onClick={() => setIsVisible(!isVisible)}
        className="w-full flex justify-between items-center px-4 py-3 bg-gray-50 hover:bg-gray-100 text-left font-medium"
      >
        <span>{title}</span>
        <span className="text-gray-400 transition-transform" style={{ transform: isVisible ? "rotate(180deg)" : "rotate(0deg)" }}>
          ▼
        </span>
      </button>

      {isVisible && (
        <div className="px-4 py-3 text-gray-700 leading-relaxed">
          {content}
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <div className="p-6 space-y-3 max-w-md mx-auto">
      <Spoiler
        title="React란 무엇인가?"
        content="React는 Meta(Facebook)가 만든 JavaScript 라이브러리로, 사용자 인터페이스를 컴포넌트 기반으로 구축합니다."
      />
      <Spoiler
        title="useState를 왜 사용하나요?"
        content="일반 변수는 바뀌어도 React가 화면을 다시 그리지 않습니다. useState를 쓰면 값이 바뀔 때마다 자동으로 화면이 업데이트됩니다."
      />
    </div>
  );
}
// 각 항목을 클릭하면 내용이 접히고 펼쳐집니다
// 화살표(▼)도 펼침 시 회전합니다
```

---

<a id="6"></a>
## 6️⃣ 중요: 상태 업데이트는 비동기입니다 [↑](#toc)

이것은 많은 초보자들이 실수하는 중요한 개념입니다.

### 문제: setCount 직후의 count는 아직 바뀌지 않았습니다

```jsx
import { useState } from "react";

function BuggyCounter() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
    console.log("count:", count); // ← 이 시점의 count는 아직 이전 값!
    // 예시: 첫 클릭 시 콘솔 출력은 0 (화면은 1로 바뀌지만)
    // 출력: "count: 0" (setCount를 호출했지만 count는 아직 0)
  }

  return (
    <div className="p-8 text-center">
      <p className="text-4xl font-bold mb-4">{count}</p>
      <button onClick={handleClick} className="bg-blue-500 text-white px-6 py-2 rounded">
        +1
      </button>
    </div>
  );
}
```

`setCount(count + 1)`은 즉시 `count` 변수를 바꾸지 않습니다. **"다음 렌더링에서는 count를 이 값으로 써주세요"** 라고 React에게 예약하는 것입니다.

> **setState는 '예약'입니다. 즉시 바뀌지 않습니다.**

### 연속 클릭 시 발생하는 함정

```jsx
function BuggyTripleCounter() {
  const [count, setCount] = useState(0);

  function handleTripleClick() {
    // 셋 다 같은 count를 보고 있음!
    setCount(count + 1); // count=0 기준: 1로 예약
    setCount(count + 1); // count=0 기준: 1로 예약 (덮어씀)
    setCount(count + 1); // count=0 기준: 1로 예약 (덮어씀)
    // 결과: 3이 아니라 1만 증가합니다!
  }

  return (
    <div className="p-8 text-center">
      <p className="text-4xl font-bold mb-4">{count}</p>
      <button onClick={handleTripleClick} className="bg-red-500 text-white px-6 py-2 rounded">
        +3 (버그 있음)
      </button>
    </div>
  );
}
// 클릭해도 1씩만 증가합니다 — 3씩 증가하지 않습니다!
```

### 해결: 함수형 업데이터 `prev => prev + 1`

이전 상태를 기반으로 계산할 때는 **함수형 업데이터**를 사용하세요.

```jsx
function CorrectTripleCounter() {
  const [count, setCount] = useState(0);

  function handleTripleClick() {
    // prev는 항상 "직전의 최신 상태"를 받습니다
    setCount((prev) => prev + 1); // 0 → 1
    setCount((prev) => prev + 1); // 1 → 2
    setCount((prev) => prev + 1); // 2 → 3
    // 결과: 3씩 증가합니다!
  }

  return (
    <div className="p-8 text-center">
      <p className="text-4xl font-bold mb-4">{count}</p>
      <button onClick={handleTripleClick} className="bg-green-500 text-white px-6 py-2 rounded">
        +3 (올바름)
      </button>
    </div>
  );
}
// 클릭 시 3씩 증가합니다
// 출력: 0 → 3 → 6 → 9 ...
```

### 언제 함수형 업데이터를 써야 하나요?

| 상황 | 추천 방법 |
|------|-----------|
| 이전 값에 기반해 계산 | `setCount(prev => prev + 1)` |
| 단순히 새 값 설정 | `setCount(42)` |
| `setTimeout` 안에서 | 함수형 업데이터 필수 |
| 연속 업데이트 | 함수형 업데이터 필수 |

**좋은 습관**: `prev` 기반 계산이라면 항상 함수형 업데이터를 써서 안전하게 만드세요.

```jsx
// 추천 패턴
setCount((prev) => prev + 1);
setLiked((prev) => !prev);
setItems((prev) => [...prev, newItem]);
```

---

<a id="7"></a>
## 7️⃣ React DevTools로 상태 확인하기 [↑](#toc)

React DevTools는 컴포넌트의 상태를 실시간으로 볼 수 있는 브라우저 확장입니다.

### 설치

1. Chrome 웹 스토어에서 **"React Developer Tools"** 검색 → 설치
2. 브라우저 재시작

### 사용법

1. React 앱이 실행된 페이지에서 `F12` (DevTools 열기)
2. 상단 탭에서 **"⚛ Components"** 클릭
3. 컴포넌트 트리에서 컴포넌트 클릭
4. 오른쪽 패널에서 **Hooks** 섹션 확인

```
Counter                    ← 컴포넌트 이름
  hooks
    State: 5               ← useState의 현재 값
```

버튼을 클릭하면 DevTools에서 State 값이 실시간으로 바뀌는 것을 볼 수 있습니다!

### DevTools에서 직접 상태 수정하기

DevTools에서 State 값을 클릭해서 직접 변경할 수도 있습니다. 디버깅에 매우 유용합니다.

> **팁**: DevTools 없이 개발하는 것은 눈을 감고 운전하는 것과 같습니다. 꼭 설치하세요!

---

<a id="8"></a>
## 8️⃣ 실습: 카운터 앱 + 글자색 토글 [↑](#toc)

### 기본 과제

카운터(+/- 버튼)와 글자색 토글 버튼을 가진 앱을 만드세요.

```jsx
// src/App.jsx
import { useState } from "react";

function App() {
  const [count, setCount] = useState(0);
  const [isRed, setIsRed] = useState(false);

  function handleIncrement() {
    setCount((prev) => prev + 1);
  }

  function handleDecrement() {
    setCount((prev) => prev - 1);
  }

  function handleReset() {
    setCount(0);
  }

  function handleToggleColor() {
    setIsRed((prev) => !prev);
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow-xl p-10 text-center w-80">
        <h1 className="text-lg font-semibold text-gray-500 mb-2 uppercase tracking-widest">
          Counter
        </h1>

        {/* 숫자 표시 — isRed에 따라 색상 변경 */}
        <p
          className={`text-8xl font-bold mb-8 transition-colors ${
            isRed ? "text-red-500" : "text-blue-500"
          }`}
        >
          {count}
        </p>

        {/* +/- 버튼 */}
        <div className="flex justify-center gap-4 mb-4">
          <button
            onClick={handleDecrement}
            className="w-14 h-14 rounded-full bg-gray-100 text-2xl font-bold hover:bg-gray-200 active:scale-95 transition-all"
          >
            −
          </button>
          <button
            onClick={handleReset}
            className="px-4 py-2 rounded-lg bg-gray-100 text-sm text-gray-600 hover:bg-gray-200"
          >
            초기화
          </button>
          <button
            onClick={handleIncrement}
            className="w-14 h-14 rounded-full bg-blue-500 text-white text-2xl font-bold hover:bg-blue-600 active:scale-95 transition-all"
          >
            +
          </button>
        </div>

        {/* 글자색 토글 버튼 */}
        <button
          onClick={handleToggleColor}
          className={`mt-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            isRed
              ? "bg-red-100 text-red-600 hover:bg-red-200"
              : "bg-blue-100 text-blue-600 hover:bg-blue-200"
          }`}
        >
          {isRed ? "🔵 파란색으로" : "🔴 빨간색으로"}
        </button>
      </div>
    </div>
  );
}

export default App;
// 출력:
// +/- 버튼으로 숫자가 올라가고 내려갑니다
// 초기화 버튼으로 0으로 돌아갑니다
// 색상 토글 버튼으로 숫자 색이 파란색/빨간색으로 바뀝니다
```

### 도전 과제

1. **최솟값/최댓값 제한**: count가 0 아래로 내려가지 않도록, 10을 초과하지 않도록 제한
2. **단계 크기 선택**: 1씩 / 5씩 / 10씩 증가하는 버튼 추가
3. **히스토리**: 클릭할 때마다 이전 값들을 목록으로 보여주기 (배열 상태)

---

<a id="9"></a>
## 9️⃣ 정리 + 브릿지 [↑](#toc)

### 핵심 정리

| 개념 | 요점 |
|------|------|
| `useState` | 컴포넌트에 기억 능력 부여 |
| `const [값, set함수] = useState(초기값)` | 기본 사용법 |
| `set함수(새값)` | 상태 업데이트 + 리렌더 트리거 |
| 비동기 업데이트 | `set함수` 호출 후 즉시 값이 바뀌지 않음 |
| 함수형 업데이터 | `set함수(prev => prev + 1)` — 이전 값 기반 계산 시 |

### useState 3단계 흐름

```
1. 선언: const [count, setCount] = useState(0)
2. 표시: <p>{count}</p>
3. 업데이트: <button onClick={() => setCount(prev => prev + 1)}>
```

### 체크리스트

- [ ] 일반 변수가 화면을 못 바꾸는 이유를 설명할 수 있다
- [ ] `const [state, setState] = useState(초기값)` 을 직접 쓸 수 있다
- [ ] `setCount(prev => prev + 1)` 함수형 업데이터를 쓸 수 있다
- [ ] DevTools에서 상태 값이 실시간으로 바뀌는 것을 확인할 수 있다
- [ ] 불리언 상태로 show/hide 토글을 구현할 수 있다

---

> **브릿지**: 상태로 화면을 실시간으로 업데이트할 수 있게 되었습니다. 이제 버튼을 클릭하면 숫자가 바뀝니다! **다음 장에서는 입력 폼과 함께 `useState`를 사용하는 방법을 배웁니다.** 사용자가 텍스트를 입력할 때마다 상태가 바뀌고, 폼을 제출할 때 검증까지 — 실무에서 가장 자주 쓰는 패턴입니다.

{% endraw %}
