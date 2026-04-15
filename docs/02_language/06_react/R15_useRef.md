---
title: 14. useRef — DOM 접근
layout: default
parent: React
nav_order: 15
permalink: /language/react/useref
---

{% raw %}

# 14장. useRef — DOM 접근과 값 보존

## 학습 목표

- `useRef`가 state, 일반 변수와 어떻게 다른지 이해한다
- ref로 DOM 요소에 직접 접근하는 방법을 익힌다
- 리렌더 없이 값을 보존하는 ref의 활용법을 배운다
- React 19의 ref-as-prop 문법을 이해한다

---

<a id="toc"></a>

## 진행 순서

1. [useRef란?](#1)
2. [DOM 접근 — 자동으로 커서 놓기](#2)
3. [렌더링 횟수 세기](#3)
4. [이전 값 기억하기](#4)
5. [state vs ref vs 일반 변수 비교](#5)
6. [React 19: ref as prop](#6)
7. [실습: 스톱워치 개선](#7)
8. [정리 + 브릿지](#8)

---

<a id="1"></a>
## 1️⃣ useRef란? [↑](#toc)

### 메모장

useRef는 **메모장**과 같습니다. 값을 적어두지만, 무언가를 적어도 화면이 다시 그려지지 않습니다. 중요한 정보를 적어두되, 그것 때문에 화면을 새로 그리고 싶지 않을 때 사용합니다.

### 기본 구조

```jsx
import { useRef } from 'react';

const ref = useRef(초기값);
// ref = { current: 초기값 }
```

`useRef`는 `{ current: 값 }` 형태의 객체를 반환합니다.

- `ref.current`로 값을 읽고 씁니다
- 값이 바뀌어도 **리렌더를 일으키지 않습니다**
- 컴포넌트가 다시 렌더링되어도 **값이 유지됩니다**

```jsx
function Example() {
  const countRef = useRef(0);

  function handleClick() {
    countRef.current = countRef.current + 1;
    console.log('클릭 횟수:', countRef.current);
    // 콘솔에는 출력되지만 화면은 바뀌지 않습니다
  }

  return (
    <button onClick={handleClick} className="px-4 py-2 bg-blue-500 text-white rounded">
      클릭 (화면은 안 바뀜)
    </button>
  );
}
```

---

<a id="2"></a>
## 2️⃣ DOM 접근 — 자동으로 커서 놓기 [↑](#toc)

### ref를 DOM에 연결하기

ref의 가장 흔한 사용법은 **DOM 요소에 직접 접근**하는 것입니다. `ref` prop에 ref 객체를 전달하면 React가 `ref.current`에 해당 DOM 요소를 자동으로 할당합니다.

```jsx
import { useRef, useEffect } from 'react';

function AutoFocusInput() {
  const inputRef = useRef(null); // 처음엔 null

  useEffect(() => {
    // 마운트 후 ref.current에 input DOM 요소가 담깁니다
    inputRef.current.focus(); // 자동으로 커서 이동
  }, []);

  return (
    <input
      ref={inputRef}          {/* ref 연결 */}
      type="text"
      placeholder="자동으로 포커스됩니다"
      className="border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
    />
  );
}
```

페이지가 로드되자마자 input에 자동으로 커서가 이동합니다.

### 실전: 검색창 단축키

```jsx
import { useRef, useEffect } from 'react';

function SearchWithShortcut() {
  const inputRef = useRef(null);

  useEffect(() => {
    function handleKeyDown(e) {
      // Ctrl+K 또는 Cmd+K 누르면 검색창 포커스
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        inputRef.current?.focus();
      }
    }

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="relative">
      <input
        ref={inputRef}
        type="text"
        placeholder="검색... (Ctrl+K)"
        className="w-64 border rounded-lg px-4 py-2 pr-16 focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400 bg-gray-100 px-1.5 py-0.5 rounded">
        ⌘K
      </span>
    </div>
  );
}
```

### ref로 할 수 있는 DOM 조작

```jsx
// 스크롤
ref.current.scrollIntoView({ behavior: 'smooth' });

// 동영상 제어
videoRef.current.play();
videoRef.current.pause();

// 캔버스
const ctx = canvasRef.current.getContext('2d');
ctx.fillRect(0, 0, 100, 100);

// 크기 측정
const { width, height } = ref.current.getBoundingClientRect();
```

---

<a id="3"></a>
## 3️⃣ 렌더링 횟수 세기 [↑](#toc)

state로 렌더링 횟수를 세면 순환이 발생합니다. (카운트 올리기 → 리렌더 → 카운트 올리기...) ref를 사용하면 리렌더 없이 셀 수 있습니다.

```jsx
import { useState, useRef, useEffect } from 'react';

function RenderCounter() {
  const [count, setCount] = useState(0);
  const renderCount = useRef(0);

  useEffect(() => {
    // 렌더링이 끝날 때마다 ref 값 증가 (리렌더 안 일어남)
    renderCount.current += 1;
  });

  return (
    <div className="p-6 text-center space-y-4">
      <p className="text-3xl font-bold">{count}</p>
      <p className="text-sm text-gray-500">
        렌더링 횟수: <span className="text-blue-500 font-bold">{renderCount.current}</span>
      </p>
      <button
        onClick={() => setCount((c) => c + 1)}
        className="bg-blue-500 text-white px-4 py-2 rounded-lg"
      >
        증가
      </button>
    </div>
  );
}
```

---

<a id="4"></a>
## 4️⃣ 이전 값 기억하기 [↑](#toc)

이전 렌더링의 값을 기억하는 데 ref가 유용합니다. "이전 값과 현재 값을 비교해서 무언가 표시하고 싶을 때" 자주 쓰입니다.

```jsx
import { useState, useRef, useEffect } from 'react';

function PriceTracker() {
  const [price, setPrice] = useState(50000);
  const prevPriceRef = useRef(price);

  useEffect(() => {
    // 렌더링 후에 이전 값을 현재 값으로 업데이트
    prevPriceRef.current = price;
  });

  const prevPrice = prevPriceRef.current;
  const diff = price - prevPrice;

  return (
    <div className="p-6 max-w-xs mx-auto">
      <h2 className="text-lg font-bold mb-4">주식 가격 추적기</h2>
      <div className="bg-white border rounded-xl p-4 text-center mb-4">
        <p className="text-3xl font-bold">{price.toLocaleString()}원</p>
        {diff !== 0 && (
          <p className={`text-sm mt-1 font-medium ${diff > 0 ? 'text-red-500' : 'text-blue-500'}`}>
            {diff > 0 ? '▲' : '▼'} {Math.abs(diff).toLocaleString()}원
          </p>
        )}
        <p className="text-xs text-gray-400 mt-1">
          이전: {prevPrice.toLocaleString()}원
        </p>
      </div>
      <div className="flex gap-2">
        <button
          onClick={() => setPrice((p) => p + Math.floor(Math.random() * 1000))}
          className="flex-1 bg-red-500 text-white py-2 rounded-lg text-sm"
        >
          상승
        </button>
        <button
          onClick={() => setPrice((p) => p - Math.floor(Math.random() * 1000))}
          className="flex-1 bg-blue-500 text-white py-2 rounded-lg text-sm"
        >
          하락
        </button>
      </div>
    </div>
  );
}
```

---

<a id="5"></a>
## 5️⃣ state vs ref vs 일반 변수 비교 [↑](#toc)

세 가지를 언제 쓸지 헷갈릴 때 이 표를 참고하세요.

| 구분 | 리렌더 발생 | 렌더 간 유지 | 화면 반영 |
|------|:---------:|:---------:|:--------:|
| state | O | O | O |
| ref | X | O | X |
| 변수 | X | X | X |

### 각각의 특징

```jsx
function ComparisonDemo() {
  // 1. state: 바뀌면 리렌더, 화면에 반영됨
  const [stateVal, setStateVal] = useState(0);

  // 2. ref: 바뀌어도 리렌더 없음, 값은 유지됨
  const refVal = useRef(0);

  // 3. 일반 변수: 리렌더될 때마다 초기화됨
  let localVar = 0;

  function handleClick() {
    setStateVal((v) => v + 1);  // 리렌더 발생 → 화면 업데이트
    refVal.current += 1;         // 리렌더 없음, 값 유지
    localVar += 1;               // 리렌더 없음, 다음 렌더에서 0으로 초기화
    console.log({ stateVal, ref: refVal.current, local: localVar });
  }

  return (
    <div className="p-4 space-y-2">
      <p>state: {stateVal} (화면에 반영됨)</p>
      <p>ref: {refVal.current} (클릭해야 최신값 확인 가능)</p>
      <p>변수: {localVar} (항상 0)</p>
      <button onClick={handleClick} className="bg-blue-500 text-white px-4 py-2 rounded">
        클릭
      </button>
    </div>
  );
}
```

### 선택 기준

```
값이 바뀔 때 화면이 업데이트되어야 한다 → state
값을 기억해야 하지만 화면 업데이트는 필요 없다 → ref
렌더링마다 새로 계산해도 되는 임시 값 → 일반 변수
```

---

<a id="6"></a>
## 6️⃣ React 19: ref as prop [↑](#toc)

### 이전의 문제

React 18까지는 ref를 자식 컴포넌트에 전달하려면 `forwardRef`라는 복잡한 패턴이 필요했습니다.

```jsx
// React 18 이하 — forwardRef 필요 (복잡!)
const MyInput = forwardRef(function MyInput(props, ref) {
  return <input ref={ref} {...props} />;
});
```

### React 19의 개선

React 19부터는 `forwardRef` 없이 **ref를 일반 props처럼** 전달할 수 있습니다.

```jsx
// React 19 — ref를 그냥 props처럼 전달합니다 ✅
function MyInput({ ref, ...props }) {
  return (
    <input
      ref={ref}
      className="border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
      {...props}
    />
  );
}

// 사용하는 쪽
function Form() {
  const inputRef = useRef(null);

  function handleFocus() {
    inputRef.current?.focus();
  }

  return (
    <div className="p-4">
      <MyInput ref={inputRef} placeholder="이름을 입력하세요" />
      <button
        onClick={handleFocus}
        className="mt-2 bg-blue-500 text-white px-4 py-2 rounded"
      >
        포커스
      </button>
    </div>
  );
}
```

이 변화로 ref 전달이 훨씬 직관적으로 되었습니다.

---

<a id="7"></a>
## 7️⃣ 실습: 스톱워치 개선 [↑](#toc)

지난 장에서 만든 스톱워치를 개선합니다. `setInterval` ID를 **state가 아닌 ref**에 저장하는 것이 올바른 패턴입니다.

### 왜 ref에 저장해야 하는가?

```jsx
// ❌ 타이머 ID를 state로 관리하면...
const [timerId, setTimerId] = useState(null);
// timerId를 setTimerId로 바꾸면 리렌더가 발생합니다.
// 리렌더가 발생하면 새로운 setInterval이 실행될 수 있습니다.
// 타이머 ID는 화면에 표시되지 않으므로 state가 아닌 ref가 맞습니다.

// ✅ 타이머 ID를 ref로 관리하면...
const timerIdRef = useRef(null);
// 값이 바뀌어도 리렌더가 발생하지 않습니다.
```

### 개선된 스톱워치

```jsx
import { useState, useRef } from 'react';

function ImprovedStopwatch() {
  const [elapsed, setElapsed] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const timerIdRef = useRef(null); // 타이머 ID를 ref에 저장

  function handleStart() {
    if (isRunning) return;
    setIsRunning(true);
    timerIdRef.current = setInterval(() => {
      setElapsed((prev) => prev + 100);
    }, 100);
  }

  function handleStop() {
    if (!isRunning) return;
    setIsRunning(false);
    clearInterval(timerIdRef.current); // ref에서 ID를 꺼내 정리
    timerIdRef.current = null;
  }

  function handleReset() {
    handleStop();
    setElapsed(0);
  }

  const seconds = Math.floor(elapsed / 1000);
  const milliseconds = Math.floor((elapsed % 1000) / 100);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-slate-900">
      <div className="bg-slate-800 rounded-3xl p-10 text-center shadow-2xl">
        <p className="text-7xl font-mono font-bold text-white tracking-wider">
          {String(seconds).padStart(2, '0')}.
          <span className="text-4xl text-slate-400">{milliseconds}</span>
        </p>
        <p className="text-slate-500 text-sm mt-2">
          {isRunning ? '⏱ 측정 중...' : '정지'}
        </p>
        <div className="flex gap-3 mt-8 justify-center">
          <button
            onClick={isRunning ? handleStop : handleStart}
            className={`w-24 py-3 rounded-xl font-semibold text-white transition-colors ${
              isRunning
                ? 'bg-yellow-500 hover:bg-yellow-400'
                : 'bg-green-500 hover:bg-green-400'
            }`}
          >
            {isRunning ? '정지' : '시작'}
          </button>
          <button
            onClick={handleReset}
            className="w-24 py-3 rounded-xl font-semibold bg-slate-700 text-slate-300 hover:bg-slate-600 transition-colors"
          >
            초기화
          </button>
        </div>
      </div>
    </div>
  );
}

export default ImprovedStopwatch;
```

이전 버전과 비교했을 때 `useEffect` 없이 더 명확하게 타이머를 제어할 수 있습니다. 시작과 정지가 각각 독립적인 함수로 분리되어 로직이 더 읽기 쉽습니다.

### 도전 과제

1. 랩(Lap) 기능 추가 — 측정 중 "랩" 버튼을 누르면 현재 시간이 목록에 기록
2. 가장 빠른 랩은 초록색, 가장 느린 랩은 빨간색으로 표시

---

<a id="8"></a>
## 8️⃣ 정리 + 브릿지 [↑](#toc)

### 이번 장에서 배운 것

| 개념 | 내용 |
|------|------|
| `useRef` 기본 | `{ current: 값 }` 객체, 변경해도 리렌더 없음 |
| DOM 접근 | `ref` prop에 연결 → `ref.current`가 DOM 요소 |
| 값 보존 | 타이머 ID, 이전 값 등 리렌더 없이 유지 |
| React 19 ref | `forwardRef` 없이 props처럼 전달 가능 |

### state vs ref 선택 기준

> 이 값이 바뀔 때 화면이 다시 그려져야 한다 → **state**
> 이 값은 내부적으로 쓰이고 화면에 바로 반영될 필요가 없다 → **ref**

### 다음 장 예고

개별 컴포넌트 내의 데이터를 잘 관리할 수 있게 되었습니다. `useState`, `useEffect`, `useRef`로 컴포넌트 안을 완전히 제어할 수 있습니다.

하지만 앱 전체에서 공유해야 하는 데이터가 있습니다. 로그인한 사용자 정보, 다크모드 설정, 언어 설정 같은 것들은 여러 컴포넌트에서 동시에 필요합니다. 이때마다 props로 계속 전달하면 어떻게 될까요? 다음 장에서 `useContext`가 이 문제를 해결합니다.

{% endraw %}
