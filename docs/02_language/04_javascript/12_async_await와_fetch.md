---
title: 12. async/await와 fetch API
layout: default
grand_parent: Language
parent: JavaScript
nav_order: 12
permalink: /language/javascript/async-fetch
---

## 학습 목표

- async/await로 비동기 코드를 동기 코드처럼 읽기 쉽게 작성할 수 있다
- fetch API로 외부 데이터를 가져오고 화면에 표시할 수 있다

<a id="toc"></a>

## 진행 순서

1. [async/await란?](#part1) - Promise를 더 읽기 쉽게 쓰는 문법
2. [try/catch로 에러 처리](#part2) - 비동기 에러를 안전하게 잡는 법
3. [fetch API 기본](#part3) - URL로 데이터를 가져오는 내장 함수
4. [fetch 활용: GET 요청](#part4) - 데이터 읽어오기
5. [fetch 활용: POST 요청](#part5) - 데이터 보내기
6. [실용 예제: 유저 정보 카드](#part6) - HTML + fetch + DOM 조합
7. [정리](#part7) - 핵심 개념 요약 및 다음 장 미리보기

---

# 12장. async/await와 fetch API

<a id="part1"></a>

## 1️⃣ async/await란? [↑](#toc)

### 번호표 vs 직원 서비스 비유

> **11장의 Promise가 '번호표 시스템'**이었다면,
> **async/await는 '직원이 직접 가져다주는 서비스'**입니다.
> 코드가 위에서 아래로 순서대로 읽히지만, 내부적으로는 여전히 비동기로 동작합니다.

Promise를 사용하면 `.then().then().then()` 체이닝이 길어질수록 읽기 어려워집니다.
`async/await`는 이 문제를 해결하기 위해 ES2017에 추가된 문법입니다.

---

### async 함수 선언

`async` 키워드를 함수 앞에 붙이면 그 함수는 **자동으로 Promise를 반환**하는 비동기 함수가 됩니다.

```js
// async 키워드를 붙인 함수 — 항상 Promise를 반환한다
async function greet() {
  return "안녕하세요"; // 내부적으로 Promise.resolve("안녕하세요")와 동일
}

greet().then((msg) => console.log(msg));
// 출력: 안녕하세요
```

---

### await 키워드

`await`는 **Promise 앞에 붙이면** 그 Promise가 완료될 때까지 기다린 뒤 결과값을 반환합니다.
`await`는 반드시 `async` 함수 안에서만 사용할 수 있습니다.

```js
// 1초 후에 완료되는 Promise를 흉내 낸 함수
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function run() {
  console.log("시작");
  await delay(1000); // 1초 기다린다
  console.log("1초 후");
  await delay(1000); // 다시 1초 기다린다
  console.log("2초 후");
}

run();
// 출력:
// 시작
// (1초 후) 1초 후
// (2초 후) 2초 후
```

---

### Promise 체이닝 → async/await 변환

```js
// 500ms 후 완료되는 비동기 함수들
function getUserName() {
  return new Promise((resolve) => setTimeout(() => resolve("홍길동"), 500));
}
function getTodo(user) {
  return new Promise((resolve) => setTimeout(() => resolve(`${user}의 할 일: 공부하기`), 500));
}

// Before: Promise 체이닝 — .then()이 쌓일수록 읽기 어렵다
getUserName()
  .then((user) => getTodo(user))
  .then((todo) => console.log(todo))
  .catch((err) => console.log("에러:", err.message));

// After: async/await — 위에서 아래로 자연스럽게 읽힌다
async function run() {
  const user = await getUserName(); // 결과가 올 때까지 기다림
  const todo = await getTodo(user); // 앞 결과를 바로 사용
  console.log(todo);
}
run();
// 출력: 홍길동의 할 일: 공부하기
```

---

<a id="part2"></a>

## 2️⃣ try/catch로 에러 처리 [↑](#toc)

### 안전망 비유

> **곡예사가 공중에서 실수해도 안전망(catch)이 받아줍니다.**
> async/await에서는 `try/catch`가 그 안전망 역할을 합니다.
> Promise의 `.catch()`를 대체하는 더 읽기 쉬운 방법입니다.

---

### try/catch/finally 구조

```js
async function riskyTask() {
  try {
    // 위험할 수 있는 코드를 여기에 둔다
    const result = await someAsyncOperation();
    console.log("성공:", result);
  } catch (error) {
    // 에러가 발생하면 여기서 잡는다
    console.log("에러 이름:", error.name);
    console.log("에러 메시지:", error.message);
  } finally {
    // 성공이든 실패든 항상 실행된다 (선택 사항)
    console.log("작업 완료 (성공/실패 무관)");
  }
}
```

---

### Promise의 .catch()를 try/catch로 대체

```js
async function getUser() {
  throw new Error("서버 연결 실패");
}

// Before: .catch()로 에러 처리
getUser()
  .then((user) => console.log(user))
  .catch((err) => console.log("에러:", err.message));

// After: try/catch — 동기 코드와 동일한 패턴이라 읽기 쉽다
async function run() {
  try {
    const user = await getUser();
    console.log(user);
  } catch (err) {
    console.log("에러:", err.message); // 에러: 서버 연결 실패
  }
}
run();
```

---

### 에러 객체의 주요 속성

| 속성 | 설명 | 예시 |
|------|------|------|
| `error.message` | 에러 설명 문자열 | `"서버 연결 실패"` |
| `error.name` | 에러 종류 | `"Error"`, `"TypeError"`, `"SyntaxError"` |
| `error.stack` | 에러 발생 위치 (디버깅용) | 파일명과 줄 번호 포함 |

---

<a id="part3"></a>

## 3️⃣ fetch API 기본 [↑](#toc)

### 우체부 비유

> **fetch는 우체부입니다.**
> 주소(URL)를 주면 그 주소로 가서 편지(데이터)를 받아 옵니다.
> 우체부가 갔다 오는 동안 우리는 다른 일을 할 수 있습니다 — 비동기!

`fetch()`는 브라우저와 Node.js 18+ 에 내장된 함수로, **HTTP 요청(네트워크 통신)**을 보내고
Promise를 반환합니다. 외부 라이브러리 없이도 API 서버와 통신할 수 있습니다.

---

### fetch()의 기본 흐름

```js
// fetch()는 Promise를 반환한다 — await로 기다린다
const response = await fetch("https://jsonplaceholder.typicode.com/users/1");

// response는 Response 객체 — 아직 데이터가 아니다
// .json()을 호출해야 실제 데이터(JavaScript 객체)로 변환된다
const user = await response.json();

console.log(user.name); // Leanne Graham
```

> **Response 객체(응답 객체)란?**
> 서버가 보내준 응답 전체를 담은 객체입니다. 상태 코드, 헤더, 본문 등을 포함합니다.
> 실제 데이터를 꺼내려면 `.json()`, `.text()` 등의 메서드를 추가로 호출해야 합니다.

---

### 실습용 무료 API: JSONPlaceholder

이 장에서는 **JSONPlaceholder**(https://jsonplaceholder.typicode.com/)를 실습에 사용합니다.
가입 없이 바로 사용할 수 있는 가짜 REST API로, 게시글, 유저, 댓글 등의 데이터를 제공합니다.

| 엔드포인트(endpoint) | 설명 |
|---------------------|------|
| `/users` | 유저 10명 목록 |
| `/users/1` | ID가 1인 유저 정보 |
| `/posts` | 게시글 100개 목록 |
| `/posts/1` | ID가 1인 게시글 |

> **엔드포인트(endpoint)란?**
> API 서버에서 특정 데이터를 가져오는 URL 경로입니다.

---

### 첫 번째 fetch 실습

```js
async function firstFetch() {
  // 유저 1번의 정보를 가져온다
  const response = await fetch("https://jsonplaceholder.typicode.com/users/1");
  const user = await response.json();

  console.log(user.name);    // Leanne Graham
  console.log(user.email);   // Sincere@april.biz
  console.log(user.address.city); // Gwenborough
}

firstFetch();
```

**실행 결과:**
```
Leanne Graham
Sincere@april.biz
Gwenborough
```

---

<a id="part4"></a>

## 4️⃣ fetch 활용: GET 요청 [↑](#toc)

**GET 요청**은 서버에서 데이터를 **읽어오는** 가장 기본적인 HTTP 방식입니다.
`fetch(url)`의 기본 동작이 GET 요청입니다.

---

### 유저 목록 가져오기

```js
async function getUserList() {
  const response = await fetch("https://jsonplaceholder.typicode.com/users");
  const users = await response.json();

  // 유저 10명의 이름과 이메일 출력
  users.forEach((user) => {
    console.log(`${user.name} (${user.email})`);
  });
}

getUserList();
```

**실행 결과:**
```
Leanne Graham (Sincere@april.biz)
Ervin Howell (Shanna@melissa.tv)
Clementine Bauch (Nathan@yesenia.net)
... (10명)
```

---

### 에러 처리: response.ok 체크

`fetch()`는 404(페이지 없음), 500(서버 오류) 같은 HTTP 오류가 발생해도
**Promise 자체는 실패하지 않습니다.** 네트워크 자체가 끊길 때만 reject됩니다.
따라서 `response.ok`를 직접 확인해야 합니다.

```js
async function safeGetUser(id) {
  try {
    const response = await fetch(
      `https://jsonplaceholder.typicode.com/users/${id}`
    );

    // response.ok: 상태 코드가 200~299 사이일 때 true
    if (!response.ok) {
      throw new Error(`HTTP 오류: 상태 코드 ${response.status}`);
    }

    const user = await response.json();
    return user;
  } catch (error) {
    // 네트워크 단절, HTTP 오류 등 모든 에러를 여기서 처리
    console.log("데이터를 가져오지 못했습니다:", error.message);
    return null; // 에러가 나도 null을 반환해 프로그램이 멈추지 않게 한다
  }
}

// 존재하는 유저
safeGetUser(1).then((user) => console.log(user?.name)); // Leanne Graham

// 존재하지 않는 유저 (404)
safeGetUser(9999).then((user) => console.log(user));
// 출력: 데이터를 가져오지 못했습니다: HTTP 오류: 상태 코드 404
//        null
```

> **`response.status`란?**
> 서버가 응답할 때 함께 보내는 숫자 코드입니다.
> 200은 성공, 404는 찾을 수 없음, 500은 서버 내부 오류를 의미합니다.

---

### 실용 예시: 게시글 목록에서 제목만 출력

```js
async function showPostTitles() {
  try {
    // ?_limit=5 — 쿼리 파라미터로 5개만 요청한다
    const response = await fetch("https://jsonplaceholder.typicode.com/posts?_limit=5");
    if (!response.ok) throw new Error(`요청 실패: ${response.status}`);
    const posts = await response.json();
    posts.forEach((post, i) => console.log(`${i + 1}. ${post.title}`));
  } catch (error) {
    console.log("게시글을 불러올 수 없습니다:", error.message);
  }
}
showPostTitles();
// 출력: 1. sunt aut facere... / 2. qui est esse / ...
```

---

<a id="part5"></a>

## 5️⃣ fetch 활용: POST 요청 [↑](#toc)

**POST 요청**은 서버로 데이터를 **보내는** HTTP 방식입니다.
게시글 작성, 회원가입, 로그인 등에 사용됩니다.

---

### fetch options (방법, 헤더, 본문)

POST 요청은 `fetch(url, options)` 형태로 두 번째 인자에 옵션을 넘깁니다.

```js
const response = await fetch("https://example.com/api/posts", {
  method: "POST",           // HTTP 메서드 지정 (기본값은 "GET")
  headers: {
    "Content-Type": "application/json", // 보내는 데이터가 JSON임을 알린다
  },
  body: JSON.stringify({    // JavaScript 객체를 JSON 문자열로 변환
    title: "새 게시글",
    content: "본문 내용",
  }),
});
```

> **`JSON.stringify()`란?**
> JavaScript 객체 `{ name: "홍길동" }`를 JSON 문자열 `'{"name":"홍길동"}'`으로 변환합니다.
> 네트워크로 데이터를 보낼 때는 문자열 형태여야 하므로 반드시 변환이 필요합니다.

---

### 실용 예시: 새 게시글 작성

```js
async function createPost(title, body, userId) {
  try {
    const response = await fetch(
      "https://jsonplaceholder.typicode.com/posts",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: title,
          body: body,
          userId: userId,
        }),
      }
    );

    if (!response.ok) {
      throw new Error(`게시글 작성 실패: ${response.status}`);
    }

    // 서버가 생성된 게시글 정보를 반환한다
    const newPost = await response.json();
    console.log("게시글이 작성되었습니다!");
    console.log("ID:", newPost.id);
    console.log("제목:", newPost.title);
    return newPost;
  } catch (error) {
    console.log("오류 발생:", error.message);
    return null;
  }
}

createPost("오늘의 공부 기록", "async/await를 배웠다.", 1);
```

**실행 결과:**
```
게시글이 작성되었습니다!
ID: 101
제목: 오늘의 공부 기록
```

> JSONPlaceholder는 실제로 데이터를 저장하지 않습니다.
> 하지만 요청을 받은 것처럼 응답을 돌려줘서 실습에 활용할 수 있습니다.

---

<a id="part6"></a>

## 6️⃣ 실용 예제: 유저 정보 카드 [↑](#toc)

버튼을 클릭하면 무작위 유저 정보를 가져와 카드로 표시하는 예제입니다.
HTML, CSS, JavaScript를 하나의 파일에 작성합니다.

---

### HTML 구조 (user-card.html)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <title>유저 카드</title>
  <!-- 스타일: body(flex, 중앙정렬), button(보라색), #card(흰 카드+그림자, display:none),
       #error(빨간색, display:none), #loading(회색, display:none) -->
</head>
<body>
  <h1>무작위 유저 카드</h1>
  <button id="btn">유저 불러오기</button>
  <p id="loading">불러오는 중...</p>
  <p id="error"></p>
  <div id="card">
    <h2 id="name"></h2>
    <p id="email"></p>
    <p id="phone"></p>
    <p id="company"></p>
  </div>
  <script src="user-card.js"></script>
</body>
</html>
```

### JavaScript (user-card.js)

```js
const btn     = document.getElementById("btn");
const card    = document.getElementById("card");
const loading = document.getElementById("loading");
const errorEl = document.getElementById("error");

// 1~10 사이 무작위 ID를 반환한다
function randomId() {
  return Math.floor(Math.random() * 10) + 1;
}

// 유저 정보를 카드 요소에 채워 넣는다
function showCard(user) {
  document.getElementById("name").textContent    = user.name;
  document.getElementById("email").textContent   = "이메일: " + user.email;
  document.getElementById("phone").textContent   = "전화: " + user.phone;
  document.getElementById("company").textContent = "회사: " + user.company.name;
  card.style.display = "block";
}

btn.addEventListener("click", async () => {
  // UI 초기화
  errorEl.style.display = "none";
  card.style.display    = "none";
  loading.style.display = "block";
  btn.disabled          = true;
  btn.textContent       = "불러오는 중...";

  try {
    const response = await fetch(
      `https://jsonplaceholder.typicode.com/users/${randomId()}`
    );
    if (!response.ok) throw new Error(`오류 코드: ${response.status}`);
    const user = await response.json();
    showCard(user);
  } catch (error) {
    errorEl.textContent   = "오류: " + error.message;
    errorEl.style.display = "block";
  } finally {
    // 성공/실패 관계없이 로딩 상태를 항상 해제한다
    loading.style.display = "none";
    btn.disabled          = false;
    btn.textContent       = "유저 불러오기";
  }
});
```

---

### 동작 흐름 요약

| 단계 | 동작 |
|------|------|
| 1. 버튼 클릭 | 버튼 비활성화, "불러오는 중..." 표시 |
| 2. fetch 실행 | 무작위 ID로 유저 정보 요청 |
| 3. 성공 | 카드에 이름, 이메일, 전화번호, 회사 표시 |
| 4. 실패 | 에러 메시지를 빨간 글씨로 표시 |
| 5. finally | 버튼 복구, 로딩 메시지 제거 |

---

<a id="part7"></a>

## 7️⃣ 정리 [↑](#toc)

### Promise vs async/await 비교

| 항목 | Promise 체이닝 | async/await |
|------|---------------|-------------|
| 가독성 | 들여쓰기 깊어짐 | 위→아래 자연스럽게 읽힘 |
| 에러 처리 | `.catch()` | `try/catch` |
| 디버깅 | 스택 추적 어려움 | 동기 코드처럼 디버깅 가능 |
| 내부 동작 | Promise | Promise (async/await는 문법 설탕) |

> **문법 설탕(Syntactic Sugar)이란?**
> 기능은 동일하지만 더 읽기 쉽게 만든 문법입니다.
> async/await는 Promise를 더 쉽게 쓰는 방법일 뿐, 내부적으로는 Promise로 동작합니다.

---

### fetch API 요약

| 상황 | 코드 |
|------|------|
| GET 요청 | `fetch(url)` |
| POST 요청 | `fetch(url, { method: "POST", headers: {...}, body: JSON.stringify(data) })` |
| 응답 JSON 변환 | `await response.json()` |
| 응답 성공 확인 | `response.ok` (200~299이면 true) |
| HTTP 상태 코드 | `response.status` |

---

### 핵심 패턴 정리

```js
// 권장 패턴: async/await + try/catch + response.ok 체크
async function getData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP 오류: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.log("오류:", error.message);
    return null;
  }
}
```

---

### 다음 장 미리보기

> **13장: Node.js와 npm** — 브라우저 밖에서 JavaScript 실행하기
> fetch로 API를 다루는 법을 배웠으니, 이제 Node.js 서버에서 직접 API를 만들어 봅시다.

---

### 실습 과제

**기본** — JSONPlaceholder에서 게시글 10개 가져와서 제목 출력하기

```js
// 힌트: ?_limit=10 쿼리 파라미터를 사용하세요
// https://jsonplaceholder.typicode.com/posts?_limit=10
async function showTenPosts() {
  // 여기에 코드를 작성하세요
}
```

**중급** — async/await + try/catch로 에러가 나도 앱이 멈추지 않게 처리하기

```js
// 힌트: 존재하지 않는 ID (예: 9999)로 요청해서 에러 처리를 확인해보세요
async function robustFetch(id) {
  // response.ok도 확인하고, catch에서 null을 반환해 보세요
}
```

**심화** — "더 보기" 버튼을 누르면 다음 10개 게시글을 추가로 불러오기 (페이지네이션)

```js
// 힌트: _page와 _limit 파라미터를 활용하세요
// https://jsonplaceholder.typicode.com/posts?_page=1&_limit=10
// https://jsonplaceholder.typicode.com/posts?_page=2&_limit=10

let currentPage = 1;

async function loadMore() {
  // currentPage를 사용해 다음 페이지를 불러오고
  // currentPage를 1 증가시키세요
}
```

---

[↑ 목차로](#toc)
