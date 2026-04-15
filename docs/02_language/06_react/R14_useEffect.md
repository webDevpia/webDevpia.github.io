---
title: 13. useEffect — 부수 효과
layout: default
parent: React
nav_order: 14
permalink: /language/react/useeffect
---

{% raw %}

# 13장. useEffect — 부수 효과

## 학습 목표

- 부수 효과(side effect)가 무엇인지 이해한다
- `useEffect`의 기본 사용법과 실행 시점을 익힌다
- 의존성 배열(`[]`, `[value]`, 생략)의 차이를 구분한다
- 클린업 함수로 타이머와 구독을 정리하는 방법을 배운다
- `useEffect`를 남용하지 않는 판단력을 기른다

---

<a id="toc"></a>

## 진행 순서

1. [부수 효과란?](#1)
2. [useEffect 기본](#2)
3. [의존성 배열 — 가장 헷갈리는 부분](#3)
4. [클린업 함수](#4)
5. [실전: 디지털 시계](#5)
6. [실전: 문서 제목 변경](#6)
7. [useEffect 남용 주의](#7)
8. [실습: 스톱워치](#8)
9. [정리 + 브릿지](#9)

---

<a id="1"></a>
## 1️⃣ 부수 효과란? [↑](#toc)

### 저녁 먹고 나서 설거지

저녁 식사(렌더링)가 끝난 후에 설거지(부수 효과)를 합니다. 설거지는 식사 자체와 직접 관계없지만, 식사 후 반드시 해야 하는 일입니다. React도 마찬가지입니다. **렌더링이 끝난 후에 실행해야 할 작업들이 있습니다.**

### 부수 효과의 종류

React의 렌더링 과정(JSX → DOM)과 직접 관련 없는 모든 작업이 부수 효과입니다.

| 종류 | 예시 |
|------|------|
| 데이터 가져오기 | `fetch('/api/users')` |
| 타이머 | `setInterval`, `setTimeout` |
| DOM 직접 조작 | `document.title = '새 제목'` |
| 이벤트 구독 | `window.addEventListener('resize', ...)` |
| 외부 라이브러리 | 지도, 차트 초기화 |

### 왜 따로 관리하는가?

```jsx
// ❌ 렌더링 중에 직접 실행하면 안 됩니다
function Counter() {
  const [count, setCount] = useState(0);

  // 렌더링할 때마다 실행되어 무한루프 발생!
  fetch('/api/data').then(/* ... */);

  return <div>{count}</div>;
}
```

렌더링은 **순수 함수**처럼 동작해야 합니다. 같은 입력에 같은 출력, 외부 세계 변경 없음. 외부 세계와의 소통은 `useEffect`에게 맡깁니다.

> React는 UI를 그리는 데 집중하고, 나머지는 useEffect에게 맡깁니다.

---

<a id="2"></a>
## 2️⃣ useEffect 기본 [↑](#toc)

### 기본 형태

```jsx
import { useEffect } from 'react';

useEffect(() => {
  // 렌더링이 끝난 후 실행할 코드
});
```

### 간단한 예제

```jsx
import { useState, useEffect } from 'react';

function Example() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    console.log('렌더링이 끝났습니다. count:', count);
  });

  return (
    <div className="p-4 text-center">
      <p className="text-2xl font-bold mb-4">{count}</p>
      <button
        onClick={() => setCount((c) => c + 1)}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        증가
      </button>
    </div>
  );
}
```

버튼을 클릭할 때마다 콘솔에 메시지가 출력됩니다. `useEffect`는 **매 렌더링이 끝난 후** 실행됩니다.

### 실행 시점

```
1. 컴포넌트 렌더링 (JSX → DOM)
2. 화면에 표시
3. useEffect 실행  ← 여기
```

---

<a id="3"></a>
## 3️⃣ 의존성 배열 — 가장 헷갈리는 부분 [↑](#toc)

`useEffect`의 두 번째 인자로 **의존성 배열**을 전달합니다. 이 배열이 `useEffect`의 실행 시점을 제어합니다.

### 세 가지 경우

#### 빈 배열 `[]` — 마운트 시 한 번만

```jsx
useEffect(() => {
  console.log('컴포넌트가 처음 나타났습니다');
}, []);
// "입학식 때 한 번" — 학교에 처음 입학할 때만 입학식을 합니다
```

**언제 사용?** API에서 초기 데이터를 불러올 때, 외부 라이브러리를 초기화할 때

#### 값이 있는 배열 `[count]` — 해당 값이 바뀔 때마다

```jsx
useEffect(() => {
  console.log('count가 바뀌었습니다:', count);
}, [count]);
// "성적이 바뀔 때마다 부모님께 알림" — 성적이 변경될 때만 연락합니다
```

**언제 사용?** 특정 값의 변화에 반응해야 할 때

#### 배열 생략 — 매 렌더마다

```jsx
useEffect(() => {
  console.log('렌더링될 때마다 실행');
});
// "매일 아침 알람" — 무조건 매일 울립니다 (거의 사용하지 않음)
```

**언제 사용?** 거의 사용하지 않습니다. 대부분의 경우 불필요한 실행이 발생합니다.

### 비교 표

| 의존성 배열 | 실행 시점 | 비유 |
|------------|---------|------|
| `[]` | 마운트 시 한 번 | 입학식 |
| `[value]` | value가 바뀔 때마다 | 성적 변경 알림 |
| 생략 | 매 렌더마다 | 매일 아침 알람 |

### 여러 의존성

```jsx
useEffect(() => {
  // userId 또는 postId 중 하나라도 바뀌면 실행
  fetchPost(userId, postId);
}, [userId, postId]);
```

---

<a id="4"></a>
## 4️⃣ 클린업 함수 [↑](#toc)

### 퇴근할 때 컴퓨터 끄기

타이머를 시작했으면, 컴포넌트가 사라질 때 타이머를 멈춰야 합니다. 퇴근할 때 컴퓨터를 끄는 것처럼. 정리하지 않으면 **메모리 누수(memory leak)**가 발생합니다.

```jsx
useEffect(() => {
  // 효과 시작
  const timerId = setInterval(() => {
    console.log('틱!');
  }, 1000);

  // 클린업 함수 — 컴포넌트가 사라지거나 의존성이 바뀌기 전에 실행
  return () => {
    clearInterval(timerId);
    console.log('타이머 정리 완료');
  };
}, []);
```

### 클린업이 실행되는 시점

```
1. 컴포넌트 마운트 → useEffect 실행
2. 컴포넌트 언마운트 → 클린업 실행
   또는
2. 의존성 변경 → 클린업 실행 → useEffect 다시 실행
```

### 클린업이 필요한 경우

| 효과 | 클린업 |
|------|--------|
| `setInterval` | `clearInterval` |
| `setTimeout` | `clearTimeout` |
| `addEventListener` | `removeEventListener` |
| WebSocket 연결 | 연결 해제 |
| 구독(Subscription) | 구독 취소 |

---

<a id="5"></a>
## 5️⃣ 실전: 디지털 시계 [↑](#toc)

`setInterval`과 클린업을 함께 사용하는 가장 대표적인 예제입니다.

```jsx
import { useState, useEffect } from 'react';

function DigitalClock() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    // 1초마다 현재 시간으로 업데이트
    const timerId = setInterval(() => {
      setTime(new Date());
    }, 1000);

    // 클린업: 컴포넌트가 사라질 때 타이머 정리
    return () => clearInterval(timerId);
  }, []); // 마운트 시 한 번만 타이머 시작

  const hours = String(time.getHours()).padStart(2, '0');
  const minutes = String(time.getMinutes()).padStart(2, '0');
  const seconds = String(time.getSeconds()).padStart(2, '0');

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900">
      <div className="text-center">
        <p className="text-7xl font-mono font-bold text-green-400 tracking-widest">
          {hours}:{minutes}:{seconds}
        </p>
        <p className="text-gray-400 mt-4">
          {time.toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'long',
          })}
        </p>
      </div>
    </div>
  );
}

export default DigitalClock;
```

---

<a id="6"></a>
## 6️⃣ 실전: 문서 제목 변경 [↑](#toc)

`document.title`을 변경하면 브라우저 탭의 제목이 바뀝니다. 이것도 부수 효과입니다.

```jsx
import { useState, useEffect } from 'react';

function MessageCounter() {
  const [count, setCount] = useState(0);

  // count가 바뀔 때마다 탭 제목 업데이트
  useEffect(() => {
    document.title = count > 0 ? `메시지 (${count})` : '메시지함';

    // 클린업: 컴포넌트가 사라지면 제목 복원
    return () => {
      document.title = '나의 앱';
    };
  }, [count]);

  return (
    <div className="p-6 text-center">
      <p className="text-4xl font-bold mb-4">{count}</p>
      <p className="text-gray-500 mb-6">읽지 않은 메시지</p>
      <div className="flex gap-3 justify-center">
        <button
          onClick={() => setCount((c) => c + 1)}
          className="bg-red-500 text-white px-4 py-2 rounded-lg"
        >
          새 메시지
        </button>
        <button
          onClick={() => setCount(0)}
          className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg"
        >
          모두 읽음
        </button>
      </div>
    </div>
  );
}
```

브라우저 탭을 보면 버튼을 클릭할 때마다 제목이 바뀌는 것을 확인할 수 있습니다.

---

<a id="7"></a>
## 7️⃣ useEffect 남용 주의 [↑](#toc)

`useEffect`를 처음 배우면 "무언가 할 때마다" `useEffect`를 쓰고 싶어집니다. 하지만 많은 경우 `useEffect`가 필요 없습니다.

### 파생 값은 useEffect 없이 계산하세요

```jsx
// ❌ 나쁜 예: useEffect로 파생 값 계산
function BadExample() {
  const [items, setItems] = useState([1, 2, 3, 4, 5]);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    setTotal(items.reduce((sum, n) => sum + n, 0));
  }, [items]);
  // items가 바뀌면 → 리렌더 → useEffect 실행 → total 업데이트 → 리렌더
  // 두 번 렌더링됩니다!

  return <p>합계: {total}</p>;
}

// ✅ 좋은 예: 렌더링 중에 계산
function GoodExample() {
  const [items, setItems] = useState([1, 2, 3, 4, 5]);

  // 렌더링할 때마다 계산 — 한 번만 렌더링됩니다
  const total = items.reduce((sum, n) => sum + n, 0);

  return <p>합계: {total}</p>;
}
```

### useEffect가 필요한 경우 vs 아닌 경우

| 상황 | useEffect 필요? |
|------|----------------|
| 다른 state에서 값 계산 | ❌ 렌더링 중 계산 |
| props가 바뀔 때 state 초기화 | ❌ key 사용 |
| 클릭 시 API 요청 | ❌ 이벤트 핸들러에서 |
| 마운트 시 데이터 로드 | ✅ |
| 타이머 시작/정리 | ✅ |
| 외부 이벤트 구독 | ✅ |

> 규칙: "이 코드는 렌더링 때문에 실행되어야 하는가, 아니면 특정 이벤트 때문에 실행되어야 하는가?" — 특정 이벤트라면 이벤트 핸들러에 두세요.

---

<a id="8"></a>
## 8️⃣ 실습: 스톱워치 [↑](#toc)

타이머 시작/정지/초기화 기능이 있는 스톱워치를 만들어 봅시다.

### 요구사항

- **시작/정지** 버튼 (토글)
- **초기화** 버튼
- 0.1초 단위로 경과 시간 표시 (예: 12.3초)

### 기본 과제 — 뼈대 코드

```jsx
import { useState, useEffect } from 'react';

function Stopwatch() {
  const [elapsed, setElapsed] = useState(0);   // 경과 시간 (ms)
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    if (!isRunning) return; // 멈춰 있으면 아무것도 안 함

    const timerId = setInterval(() => {
      setElapsed((prev) => prev + 100); // 100ms마다 증가
    }, 100);

    return () => clearInterval(timerId); // 정지하거나 언마운트 시 정리
  }, [isRunning]); // isRunning이 바뀔 때마다 (시작/정지)

  function handleReset() {
    setIsRunning(false);
    setElapsed(0);
  }

  // TODO: elapsed를 "분:초.0" 형식으로 변환하세요
  const display = (elapsed / 1000).toFixed(1);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
        <p className="text-6xl font-mono font-bold text-gray-800 mb-8">
          {display}
          <span className="text-2xl text-gray-400 ml-1">초</span>
        </p>
        <div className="flex gap-4">
          <button
            onClick={() => setIsRunning((r) => !r)}
            className={`px-6 py-3 rounded-xl font-semibold text-white transition-colors ${
              isRunning
                ? 'bg-yellow-500 hover:bg-yellow-600'
                : 'bg-green-500 hover:bg-green-600'
            }`}
          >
            {isRunning ? '정지' : '시작'}
          </button>
          <button
            onClick={handleReset}
            className="px-6 py-3 rounded-xl font-semibold bg-gray-200 text-gray-700 hover:bg-gray-300 transition-colors"
          >
            초기화
          </button>
        </div>
      </div>
    </div>
  );
}

export default Stopwatch;
```

### 도전 과제

1. 랩(Lap) 기능 추가 — 시작 중 버튼을 누르면 현재 시간 기록
2. 경과 시간을 `분:초.밀리초` 형식으로 표시 (예: `01:23.4`)

---

<a id="9"></a>
## 9️⃣ 정리 + 브릿지 [↑](#toc)

### 이번 장에서 배운 것

| 개념 | 내용 |
|------|------|
| 부수 효과 | 렌더링 이후 React 외부 세계와 상호작용 |
| `useEffect(() => {}, [])` | 마운트 시 한 번만 실행 |
| `useEffect(() => {}, [v])` | `v`가 바뀔 때마다 실행 |
| 클린업 함수 | `return () => {}` — 언마운트/재실행 전 정리 |
| 남용 주의 | 파생 값은 렌더링 중 계산, 이벤트는 핸들러에서 |

### 핵심 기억법

```
useEffect(실행할 함수, [언제 실행할지]);
                             ↑
                    [] = 처음 한 번
                    [v] = v가 바뀔 때
                    없음 = 매번
```

### 다음 장 예고

타이머를 관리하는 법을 배웠습니다. 그런데 `setInterval` ID를 `state`로 관리하면 ID가 바뀔 때마다 리렌더가 발생합니다. 이것은 불필요합니다. 다음 장에서 `useRef`를 배우면 **리렌더 없이 값을 저장**하고 **DOM 요소에 직접 접근**하는 더 좋은 방법을 알게 됩니다.

{% endraw %}
