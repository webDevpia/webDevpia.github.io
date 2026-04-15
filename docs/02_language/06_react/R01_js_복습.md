---
title: 00. React를 위한 JavaScript 복습
layout: default
parent: React
nav_order: 1
permalink: /language/react/js-review
---

{% raw %}

# 00장. React를 위한 JavaScript 복습

> "React를 배우다가 막히는 대부분의 이유는 React가 어려워서가 아니라, 그 안에 쓰인 JavaScript 문법이 낯설어서입니다."

이 장은 React 코드에 반복적으로 등장하는 JavaScript 패턴 9가지를 빠르게 정리합니다.  
이미 알고 있다면 빠르게 훑고 넘어가세요. 처음 보는 문법이 있다면 반드시 여기서 익히고 다음 장으로 가세요.

---

## 학습 목표

- React 코드에서 자주 쓰이는 JavaScript 9가지 패턴을 이해한다
- 각 문법이 React에서 어떻게 활용되는지 연결할 수 있다
- 아래 자가 점검 목록을 모두 통과할 수 있다

---

<a id="toc"></a>
## 진행 순서
1. [화살표 함수](#1)
2. [구조분해 할당](#2)
3. [스프레드 연산자](#3)
4. [배열 메서드 (map, filter, find)](#4)
5. [템플릿 리터럴](#5)
6. [ES 모듈 (import / export)](#6)
7. [const와 let](#7)
8. [삼항 연산자와 &&](#8)
9. [비동기: Promise와 async/await](#9)
10. [자가 점검](#check)

---

<a id="1"></a>
## 1️⃣ 화살표 함수 [↑](#toc)

### 왜 알아야 하나요?

React 컴포넌트와 이벤트 핸들러는 거의 모두 화살표 함수로 작성됩니다.

### 일반 함수 vs 화살표 함수

```javascript
// 일반 함수
function greet(name) {
  return "안녕, " + name;
}

// 화살표 함수 — 완전한 형태
const greet = (name) => {
  return "안녕, " + name;
};

// 화살표 함수 — 한 줄 단축형 (return 생략)
const greet = (name) => "안녕, " + name;

// 매개변수가 하나면 괄호도 생략 가능
const greet = name => "안녕, " + name;
```

### 객체를 반환할 때는 소괄호로 감싸세요

```javascript
// 잘못된 예 — 중괄호를 함수 본문으로 인식합니다
const getUser = () => { name: "Alice" }; // undefined 반환!

// 올바른 예 — 소괄호로 감싸면 객체 리터럴로 인식합니다
const getUser = () => ({ name: "Alice" }); // { name: "Alice" } 반환
```

### 이것이 React에서 이렇게 쓰입니다

```jsx
// 컴포넌트 자체
const Hello = () => <h1>안녕하세요!</h1>;

// 이벤트 핸들러
<button onClick={() => console.log("클릭!")}>눌러보세요</button>

// map 안에서 컴포넌트 반환
items.map(item => <li key={item.id}>{item.name}</li>)
```

---

<a id="2"></a>
## 2️⃣ 구조분해 할당 [↑](#toc)

### 왜 알아야 하나요?

React 컴포넌트는 props를 구조분해로 받고, `useState`는 배열 구조분해로 사용합니다.

### 객체 구조분해

```javascript
const person = { name: "Alice", age: 25, city: "서울" };

// 구조분해 없이 사용
console.log(person.name); // "Alice"
console.log(person.age);  // 25

// 구조분해 사용 — 변수를 한 번에 꺼냅니다
const { name, age } = person;
console.log(name); // "Alice"
console.log(age);  // 25

// 다른 이름으로 꺼내기
const { name: userName } = person;
console.log(userName); // "Alice"

// 기본값 설정
const { city, country = "한국" } = person;
console.log(country); // "한국" (person에 country가 없으므로 기본값 사용)
```

### 배열 구조분해

```javascript
const colors = ["빨강", "파랑", "초록"];

// 구조분해 없이
const first = colors[0];
const second = colors[1];

// 구조분해 사용
const [first, second] = colors;
console.log(first);  // "빨강"
console.log(second); // "파랑"

// 특정 위치만 꺼내기 (콤마로 건너뜀)
const [, , third] = colors;
console.log(third); // "초록"
```

### 이것이 React에서 이렇게 쓰입니다

```jsx
// Props 구조분해 — 매개변수에서 바로 꺼냅니다
function UserCard({ name, age, city = "미입력" }) {
  return (
    <div>
      <h2>{name}</h2>
      <p>나이: {age}</p>
      <p>도시: {city}</p>
    </div>
  );
}

// useState — 배열 구조분해
const [count, setCount] = useState(0);
//     ↑ 현재값    ↑ 업데이트 함수
```

---

<a id="3"></a>
## 3️⃣ 스프레드 연산자 [↑](#toc)

### 왜 알아야 하나요?

React에서 상태(state)를 업데이트할 때 **원본을 직접 수정하지 않고** 새 객체/배열을 만들어야 합니다. 스프레드 연산자가 핵심 도구입니다.

### 배열 스프레드

```javascript
const fruits = ["사과", "바나나"];

// 새 배열 만들기 (원본 유지)
const moreFruits = [...fruits, "딸기"];
console.log(fruits);     // ["사과", "바나나"] — 원본 그대로
console.log(moreFruits); // ["사과", "바나나", "딸기"]

// 배열 합치기
const a = [1, 2, 3];
const b = [4, 5, 6];
const combined = [...a, ...b]; // [1, 2, 3, 4, 5, 6]
```

### 객체 스프레드

```javascript
const user = { name: "Alice", age: 25 };

// 속성 추가한 새 객체 만들기
const updatedUser = { ...user, city: "서울" };
// { name: "Alice", age: 25, city: "서울" }

// 속성 수정 — 뒤에 오는 값이 우선합니다
const olderUser = { ...user, age: 26 };
// { name: "Alice", age: 26 }
```

### 이것이 React에서 이렇게 쓰입니다

```jsx
// 배열 상태에 항목 추가
const [todos, setTodos] = useState(["운동", "독서"]);
setTodos([...todos, "코딩"]);

// 객체 상태의 특정 필드만 업데이트
const [user, setUser] = useState({ name: "Alice", age: 25 });
setUser({ ...user, age: 26 }); // age만 바꾸고 나머지는 유지
```

---

<a id="4"></a>
## 4️⃣ 배열 메서드 (map, filter, find) [↑](#toc)

### 왜 알아야 하나요?

`map`은 React에서 목록을 화면에 그릴 때 매일 사용합니다. `filter`는 특정 조건의 항목만 보여줄 때, `find`는 특정 항목을 찾을 때 씁니다.

### map — 모든 항목 변환

```javascript
const numbers = [1, 2, 3, 4, 5];

// 각 숫자를 2배로 만든 새 배열
const doubled = numbers.map(n => n * 2);
console.log(doubled); // [2, 4, 6, 8, 10]

// 객체 배열을 다른 형태로 변환
const students = [
  { id: 1, name: "Alice", score: 90 },
  { id: 2, name: "Bob",   score: 75 },
];
const names = students.map(s => s.name);
console.log(names); // ["Alice", "Bob"]
```

### filter — 조건에 맞는 항목만

```javascript
const scores = [45, 80, 92, 61, 38, 77];

// 60점 이상만 필터링
const passed = scores.filter(score => score >= 60);
console.log(passed); // [80, 92, 61, 77]
```

### find — 조건에 맞는 첫 번째 항목

```javascript
const users = [
  { id: 1, name: "Alice" },
  { id: 2, name: "Bob" },
  { id: 3, name: "Charlie" },
];

const found = users.find(u => u.id === 2);
console.log(found); // { id: 2, name: "Bob" }
```

### 이것이 React에서 이렇게 쓰입니다

```jsx
const students = [
  { id: 1, name: "Alice", score: 90 },
  { id: 2, name: "Bob",   score: 55 },
  { id: 3, name: "Carol", score: 80 },
];

function StudentList() {
  // 60점 이상만 표시
  const passed = students.filter(s => s.score >= 60);

  return (
    <ul>
      {passed.map(student => (
        <li key={student.id}>
          {student.name}: {student.score}점
        </li>
      ))}
    </ul>
  );
}
```

---

<a id="5"></a>
## 5️⃣ 템플릿 리터럴 [↑](#toc)

### 왜 알아야 하나요?

클래스명을 동적으로 만들거나, 문자열 안에 변수를 넣을 때 자주 씁니다.

```javascript
const name = "Alice";
const age = 25;

// 기존 방식 (문자열 연결)
console.log("이름: " + name + ", 나이: " + age);

// 템플릿 리터럴 (백틱 사용)
console.log(`이름: ${name}, 나이: ${age}`);

// 표현식도 사용 가능
console.log(`내년에는 ${age + 1}살이 됩니다.`);

// 여러 줄 문자열
const message = `
  안녕하세요, ${name}님.
  오늘도 좋은 하루 되세요!
`;
```

### 이것이 React에서 이렇게 쓰입니다

```jsx
function Badge({ score }) {
  // 점수에 따라 Tailwind 클래스를 동적으로 결정
  const color = score >= 60 ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800";

  return (
    <span className={`px-2 py-1 rounded ${color}`}>
      {score}점
    </span>
  );
}
```

---

<a id="6"></a>
## 6️⃣ ES 모듈 (import / export) [↑](#toc)

### 왜 알아야 하나요?

React 앱은 여러 파일로 나뉩니다. 파일 사이에 컴포넌트와 함수를 주고받는 방법이 모듈 시스템입니다.

### named export / import

```javascript
// utils.js — 여러 항목을 내보낼 때
export function add(a, b) {
  return a + b;
}

export function subtract(a, b) {
  return a - b;
}

export const PI = 3.14159;
```

```javascript
// main.js — 가져올 때 (중괄호 사용)
import { add, PI } from "./utils.js";

console.log(add(2, 3)); // 5
console.log(PI);        // 3.14159
```

### default export / import

```javascript
// Button.jsx — 파일당 하나의 기본 내보내기
function Button({ label }) {
  return <button>{label}</button>;
}

export default Button;
```

```javascript
// App.jsx — 중괄호 없이 가져옴, 이름도 자유롭게
import Button from "./Button";
import MyButton from "./Button"; // 같은 파일, 다른 이름도 가능
```

### 이것이 React에서 이렇게 쓰입니다

```jsx
// components/Header.jsx
export default function Header() {
  return <header className="bg-blue-600 text-white p-4">My App</header>;
}

// components/Footer.jsx
export default function Footer() {
  return <footer className="bg-gray-100 p-4">© 2025</footer>;
}

// App.jsx
import Header from "./components/Header";
import Footer from "./components/Footer";

function App() {
  return (
    <>
      <Header />
      <main>본문 내용</main>
      <Footer />
    </>
  );
}
```

---

<a id="7"></a>
## 7️⃣ const와 let [↑](#toc)

### 왜 알아야 하나요?

React 코드에서는 `var`를 거의 사용하지 않습니다. `const`와 `let`의 차이를 알아야 합니다.

```javascript
// const — 재할당 불가 (React에서 기본값으로 사용)
const name = "Alice";
name = "Bob"; // 에러! 재할당 불가

// 단, 객체/배열의 내부는 변경 가능
const user = { name: "Alice" };
user.name = "Bob";    // 가능 (객체 내부 수정)
user = { name: "Bob" }; // 에러! (재할당 자체는 불가)

// let — 재할당 가능 (반복문, 조건에 따라 값이 달라질 때)
let count = 0;
count = 1; // 가능
count++;   // 가능
```

### 언제 무엇을 쓰나요?

```javascript
// const를 기본으로 — 바뀌지 않는 것들
const PI = 3.14;
const userName = "Alice";
const fetchData = async () => { /* ... */ };

// let을 쓰는 경우 — 나중에 값이 바뀌는 것들
let isLoading = false;
isLoading = true; // 나중에 변경

// React에서 상태는 let이 아니라 useState를 씁니다
// let count = 0;           ← 이렇게 하면 화면이 안 바뀝니다
// const [count, setCount] = useState(0); ← 이렇게 해야 합니다
```

---

<a id="8"></a>
## 8️⃣ 삼항 연산자와 && [↑](#toc)

### 왜 알아야 하나요?

React의 JSX 안에서는 `if` 문을 직접 쓸 수 없습니다. 대신 삼항 연산자와 `&&`로 조건부 렌더링을 합니다.

### 삼항 연산자

```javascript
// 형식: 조건 ? 참일 때 값 : 거짓일 때 값
const age = 20;
const status = age >= 18 ? "성인" : "미성년자";
console.log(status); // "성인"

// 중첩도 가능하지만 읽기 어려워집니다
const grade =
  score >= 90 ? "A" :
  score >= 80 ? "B" :
  score >= 70 ? "C" : "F";
```

### && 연산자

```javascript
// 조건이 참일 때만 오른쪽 값을 반환
const isLoggedIn = true;
const message = isLoggedIn && "환영합니다!";
console.log(message); // "환영합니다!"

const isLoggedOut = false;
const msg2 = isLoggedOut && "환영합니다!";
console.log(msg2); // false (아무것도 출력 안 됨)
```

### 이것이 React에서 이렇게 쓰입니다

```jsx
function UserStatus({ isLoggedIn, userName, cartCount }) {
  return (
    <div>
      {/* 삼항 연산자 — 두 가지 중 하나를 보여줄 때 */}
      {isLoggedIn ? (
        <p>안녕하세요, {userName}님!</p>
      ) : (
        <p>로그인해 주세요.</p>
      )}

      {/* && — 조건이 참일 때만 보여줄 때 */}
      {cartCount > 0 && (
        <span className="badge">{cartCount}개</span>
      )}
    </div>
  );
}
```

---

<a id="9"></a>
## 9️⃣ 비동기: Promise와 async/await [↑](#toc)

### 왜 알아야 하나요?

날씨 앱에서 서버에서 데이터를 가져올 때 비동기 처리를 사용합니다. 깊은 이해보다는 패턴을 익히는 게 목표입니다.

### Promise란?

```javascript
// Promise = "나중에 결과를 줄게요"라는 약속
// 인터넷에서 데이터를 가져오는 건 시간이 걸립니다

fetch("https://api.example.com/data") // 요청 시작 (즉시 Promise 반환)
  .then(response => response.json())   // 응답이 오면 JSON으로 변환
  .then(data => console.log(data))     // 변환된 데이터 사용
  .catch(error => console.error(error)); // 에러 처리
```

### async/await — 더 읽기 쉬운 방식

```javascript
// async 함수 안에서 await을 쓰면 완료될 때까지 기다립니다
async function fetchWeather(city) {
  try {
    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("날씨 데이터를 가져오지 못했습니다:", error);
  }
}
```

### 이것이 React에서 이렇게 쓰입니다

```jsx
import { useState, useEffect } from "react";

function WeatherCard({ city }) {
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    async function load() {
      const response = await fetch(`/api/weather?city=${city}`);
      const data = await response.json();
      setWeather(data);
    }
    load();
  }, [city]);

  if (!weather) return <p>로딩 중...</p>;

  return <p>{city}의 날씨: {weather.description}</p>;
}
```

> 자세한 내용은 09장(useEffect)과 16장(API 연동)에서 다룹니다.

---

<a id="check"></a>
## ✅ 자가 점검 [↑](#toc)

아래 9개를 모두 이해하면 React 학습을 시작할 수 있습니다.

| # | 개념 | 확인 질문 |
|---|------|-----------|
| 1 | 화살표 함수 | `const fn = x => x * 2`를 일반 함수로 바꿀 수 있다 |
| 2 | 구조분해 할당 | `const { name, age } = user`가 뭘 하는지 안다 |
| 3 | 스프레드 연산자 | `{ ...user, age: 26 }`이 원본을 바꾸지 않음을 안다 |
| 4 | 배열 메서드 | `map`, `filter`, `find`의 차이를 설명할 수 있다 |
| 5 | 템플릿 리터럴 | `` `안녕, ${name}` ``을 쓸 수 있다 |
| 6 | ES 모듈 | `export default`와 `export`의 차이를 안다 |
| 7 | const / let | 언제 `const`를 쓰고 언제 `let`을 쓰는지 안다 |
| 8 | 삼항 / && | JSX 안에서 조건에 따라 다른 내용을 보여줄 수 있다 |
| 9 | async/await | `await fetch(url)`이 뭘 기다리는지 안다 |

---

## 정리

이 장에서 배운 9가지 패턴은 React 코드 어디에서나 반복해서 나타납니다. 처음부터 완벽하게 외울 필요는 없습니다. React를 배우면서 이 장으로 돌아오면 됩니다.

**다음 장 미리보기:**  
환경이 아직 준비되지 않았다면, 지금 바로 01장으로 가서 Node.js와 Vite를 설치하고 첫 React 앱을 실행해 봅시다. 설치하는 과정 자체가 React의 첫 번째 실습입니다.

**[→ 01장: 환경 구축 + 첫 React 앱](/language/react-new/setup)**

{% endraw %}
