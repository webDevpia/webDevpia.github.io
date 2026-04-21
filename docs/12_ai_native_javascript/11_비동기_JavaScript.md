---
title: 10. 비동기 JavaScript
layout: default
parent: AI-Native JavaScript
nav_order: 11
permalink: /ai-native-js/async
---

# 10장. 비동기 JavaScript — 데이터 가져오기
{: .no_toc }

> **Phase 2**

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 생성 + 검증 모드**
> AI(Copilot)가 코드를 생성할 수 있습니다.
> 단, 반드시 생성된 코드를 **읽고, 이해하고, 테스트로 검증**해야 합니다.
> AI 코드를 이해 없이 복붙하는 것은 금지입니다.

## 학습 목표

- 동기와 비동기의 차이를 설명할 수 있다
- `fetch`로 외부 API에서 데이터를 가져올 수 있다
- `async/await`을 사용할 수 있다
- AI가 생성한 비동기 코드를 Vitest로 테스트할 수 있다

<a id="toc"></a>

## 진행 순서

1. [비동기란?](#part1) — 식당 주문 비유
2. [콜백 함수](#part2) — 이미 쓰고 있었다!
3. [Promise](#part3) — "약속" 패턴
4. [async/await](#part4) — 더 깔끔한 방법
5. [fetch로 데이터 가져오기](#part5) — JSONPlaceholder API
6. [AI + 테스트로 검증하기](#part6) — Vitest로 비동기 테스트
7. [실습 과제](#part7) — 기본 / 도전
8. [정리](#part8) — 핵심 요약 및 다음 장

---

<a id="part1"></a>

## 1️⃣ ⭐ **핵심** — 비동기란? [↑](#toc)

> 강사와 함께 동기와 비동기의 차이를 알아봅시다

지금까지 배운 코드는 **위에서 아래로 순서대로** 실행됐습니다. 이것을 **동기(synchronous)** 방식이라고 합니다.

하지만 현실에서는 시간이 걸리는 작업이 있습니다. 서버에서 데이터를 받아오는 것, 파일을 읽는 것이 그 예입니다. 이런 작업을 동기로 처리하면 작업이 끝날 때까지 다른 모든 것이 멈춥니다.

> 식당에서 주문을 받는 방식을 상상해보세요.
>
> **동기 방식**: 1번 손님이 주문하면, 음식이 나올 때까지 2번 손님은 기다려야 합니다.
> 주방에서 파스타 15분을 조리하는 동안 식당 전체가 멈춥니다.
>
> **비동기 방식**: 1번 손님이 주문하면 번호표를 받고 자리로 돌아갑니다.
> 직원은 바로 2번 손님의 주문을 받을 수 있습니다.
> 음식이 다 되면 "37번 손님!" 하고 알려줍니다.

JavaScript는 기본적으로 **싱글 스레드**(한 번에 한 가지 일만)이지만, 비동기 방식으로 시간이 걸리는 작업을 "기다리는 동안 다른 일 처리"할 수 있습니다.

### setTimeout으로 비동기 체험하기

```javascript
console.log('1: 시작');

setTimeout(() => {
  console.log('2: 1초 후 실행됨');
}, 1000); // 1000밀리초 = 1초

console.log('3: 바로 실행됨');

// 출력 순서:
// 1: 시작
// 3: 바로 실행됨
// 2: 1초 후 실행됨  ← 나중에 실행!
```

`setTimeout` 안의 함수는 1초 뒤에 실행됩니다. 그 동안 나머지 코드는 계속 진행됩니다. 예상과 다른 순서가 당황스럽다면 정상입니다. 비동기를 처음 배울 때 누구나 혼란을 느낍니다.

---

<a id="part2"></a>

## 2️⃣ 📖 **더 알아보기** — 콜백 함수 [↑](#toc)

사실 여러분은 이미 비동기 코드를 써왔습니다. `addEventListener`에 전달하는 함수가 바로 **콜백 함수**입니다.

> 콜백(callback): "나중에 불러줘(call back)"라는 뜻입니다.
> "클릭이 일어나면 이 함수를 불러줘"라고 등록해두는 것입니다.

```javascript
// addEventListener의 두 번째 인자가 콜백 함수입니다
btn.addEventListener('click', () => {
  console.log('클릭됨!');
  // ↑ 이 함수는 나중에, 클릭이 일어날 때 실행됩니다
});

// setTimeout의 첫 번째 인자도 콜백 함수입니다
setTimeout(() => {
  console.log('1초 뒤 실행');
}, 1000);
```

### 콜백 지옥 (왜 Promise가 필요한가)

콜백 안에서 또 비동기 작업을 하면 코드가 계속 안으로 들어갑니다.

```javascript
// 사용자 가져오기 → 그 사용자의 게시물 가져오기 → 게시물의 댓글 가져오기
getUser(1, (user) => {
  getPosts(user.id, (posts) => {
    getComments(posts[0].id, (comments) => {
      // 점점 깊어지는 구조 → 가독성, 에러 처리가 매우 어려워집니다
      console.log(comments);
    });
  });
});
```

이처럼 콜백이 중첩되는 것을 **콜백 지옥(Callback Hell)**이라고 합니다. 이 문제를 해결하기 위해 **Promise**가 도입됐습니다.

---

<a id="part3"></a>

## 3️⃣ 📖 **더 알아보기** — Promise [↑](#toc)

Promise는 "지금은 없지만 나중에 값이 생길 것이라는 약속"입니다.

> 온라인 쇼핑 영수증을 상상해보세요.
> 주문하면 바로 택배가 오지 않습니다.
> 하지만 "이 주문 번호로 나중에 받을 수 있다"는 **약속(Promise)**을 받습니다.
> 약속은 세 가지 상태입니다:
> - **대기(pending)**: 택배가 이동 중
> - **이행(fulfilled)**: 택배가 도착했음 → `.then()` 실행
> - **거부(rejected)**: 배송 실패 → `.catch()` 실행

```javascript
// Promise 직접 만들기 (이해를 위한 예시, 실제로는 잘 안 씁니다)
const myPromise = new Promise((resolve, reject) => {
  const success = true;

  if (success) {
    resolve('성공!'); // 이행: then이 실행됨
  } else {
    reject('실패!'); // 거부: catch가 실행됨
  }
});

myPromise
  .then((result) => {
    console.log('결과:', result); // "결과: 성공!"
  })
  .catch((error) => {
    console.log('에러:', error);
  });
```

### .then() 체이닝

Promise의 `.then()`은 연결해서 쓸 수 있습니다:

```javascript
fetch('https://jsonplaceholder.typicode.com/users/1')
  .then((response) => response.json())   // 응답을 JSON으로 변환
  .then((user) => {
    console.log(user.name);              // 변환된 데이터 사용
    return user.name;
  })
  .then((name) => {
    console.log(`${name}님 안녕하세요!`);
  })
  .catch((error) => {
    console.error('에러 발생:', error);  // 어디서 에러가 나든 여기서 잡힘
  });
```

콜백 지옥보다는 낫지만, 여전히 복잡합니다. 이보다 더 읽기 쉬운 방법이 `async/await`입니다.

---

<a id="part4"></a>

## 4️⃣ 🚀 **도전** — async/await [↑](#toc)

`async/await`는 Promise를 더 읽기 쉽게 쓰는 문법입니다. "기다려!(await)"라는 이름처럼, 비동기 작업이 끝날 때까지 기다렸다가 다음 줄로 넘어갑니다.

> `await`은 "이 작업 끝날 때까지 잠깐 기다려"라는 표지판입니다.
> 전체 함수를 멈추는 것이 아니라, 그 함수 내부의 흐름을 잠깐 멈춥니다.

### 규칙: async 함수 안에서만 await 사용 가능

```javascript
// async 키워드를 함수 앞에 붙여야 그 안에서 await를 쓸 수 있습니다
async function fetchUser(id) {
  const response = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
  const user = await response.json();
  return user;
}
```

### Promise .then() 체인과 async/await 비교

```javascript
// Promise .then() 방식
function getUserName_promise(id) {
  return fetch(`https://jsonplaceholder.typicode.com/users/${id}`)
    .then((res) => res.json())
    .then((user) => user.name)
    .catch((err) => console.error(err));
}

// async/await 방식 — 훨씬 읽기 쉽습니다
async function getUserName_async(id) {
  try {
    const res = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
    const user = await res.json();
    return user.name;
  } catch (err) {
    console.error(err);
  }
}
```

### try/catch로 에러 처리

`async/await`에서는 `try/catch`로 에러를 처리합니다.

```javascript
async function fetchData(url) {
  try {
    const res = await fetch(url);

    // HTTP 에러 확인 (fetch는 4xx, 5xx도 에러로 처리하지 않음)
    if (!res.ok) {
      throw new Error(`HTTP 에러: ${res.status}`);
    }

    const data = await res.json();
    return data;
  } catch (err) {
    // 네트워크 에러, JSON 파싱 에러, 우리가 직접 throw한 에러 모두 잡힘
    console.error('데이터 로드 실패:', err.message);
    return null; // 실패 시 null 반환
  }
}
```

---

<a id="part5"></a>

## 5️⃣ ⭐ **핵심** — fetch로 데이터 가져오기 [↑](#toc)

> 강사 시연을 보면서 따라하세요

`fetch`는 브라우저에 내장된 함수로, HTTP 요청을 보내고 응답을 받습니다.

### JSONPlaceholder — 실습용 무료 API

[JSONPlaceholder](https://jsonplaceholder.typicode.com)는 개발 연습용 무료 가짜 API입니다. 회원가입이나 API 키 없이 바로 사용할 수 있습니다.

| 주소 | 내용 |
|------|------|
| `/users` | 사용자 10명 목록 |
| `/users/1` | ID가 1인 사용자 |
| `/posts` | 게시물 100개 목록 |
| `/posts/1` | ID가 1인 게시물 |
| `/posts?userId=1` | 사용자 1의 게시물만 |

### 사용자 목록 가져오기

```javascript
async function loadUsers() {
  const res = await fetch('https://jsonplaceholder.typicode.com/users');
  const users = await res.json();
  return users;
}

// 사용 예
loadUsers().then((users) => {
  users.forEach((user) => {
    console.log(`${user.name} (${user.email})`);
  });
});

// 출력 예:
// Leanne Graham (Sincere@april.biz)
// Ervin Howell (Shanna@melissa.tv)
// ...
```

### DOM에 데이터 표시하기

```html
<!-- index.html -->
<button id="loadBtn">사용자 불러오기</button>
<ul id="userList"></ul>
<p id="status"></p>
```

```javascript
// app.js
async function loadAndDisplayUsers() {
  const status = document.querySelector('#status');
  const list = document.querySelector('#userList');

  status.textContent = '불러오는 중...';
  list.innerHTML = '';

  try {
    const res = await fetch('https://jsonplaceholder.typicode.com/users');

    if (!res.ok) {
      throw new Error(`서버 에러: ${res.status}`);
    }

    const users = await res.json();

    users.forEach((user) => {
      const li = document.createElement('li');
      li.textContent = `${user.name} — ${user.email}`;
      list.appendChild(li);
    });

    status.textContent = `${users.length}명을 불러왔습니다.`;
  } catch (err) {
    status.textContent = `에러: ${err.message}`;
  }
}

document.querySelector('#loadBtn').addEventListener('click', loadAndDisplayUsers);
```

### 에러 처리: 네트워크 실패 시

```javascript
async function safeFetch(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    return await res.json();
  } catch (err) {
    if (err.name === 'TypeError') {
      // fetch 자체가 실패한 경우 (네트워크 없음, URL 오류 등)
      console.error('네트워크 연결을 확인해주세요');
    } else {
      console.error('데이터 요청 실패:', err.message);
    }
    return null;
  }
}
```

> **참고**: `safeFetch`는 `fetch`를 감싸는 래퍼 함수입니다. 반복되는 에러 처리 패턴을 하나로 모아두면 코드가 간결해집니다.

---

<a id="part6"></a>

## 6️⃣ 📖 **더 알아보기** — AI + 테스트로 검증하기 [↑](#toc)

비동기 코드는 직접 실행해보기 전에 테스트로 확인하는 것이 좋습니다. 특히 API 응답 처리 로직은 네트워크 없이 테스트할 수 있어야 합니다.

### Copilot에게 fetch 함수 요청하기

```
JSONPlaceholder API에서 특정 사용자의 게시물 제목 목록을 가져오는
fetchPostTitles(userId) 함수를 만들어줘.
에러 처리도 포함해줘.
```

Copilot이 생성한 코드 예시:

```javascript
// src/api.js
export async function fetchPostTitles(userId) {
  const res = await fetch(
    `https://jsonplaceholder.typicode.com/posts?userId=${userId}`
  );

  if (!res.ok) {
    throw new Error(`Failed to fetch posts: ${res.status}`);
  }

  const posts = await res.json();
  return posts.map((post) => post.title);
}
```

### 테스트 작성 전략 — 로직과 네트워크 분리

`fetch`를 직접 테스트하는 것보다, **데이터 처리 로직**을 순수 함수로 분리해서 테스트하는 것이 더 쉽습니다.

```javascript
// src/postUtils.js — 순수 함수, 테스트하기 쉬움
export function extractTitles(posts) {
  return posts.map((post) => post.title);
}

export function filterByUserId(posts, userId) {
  return posts.filter((post) => post.userId === userId);
}
```

```javascript
// tests/postUtils.test.js
import { describe, it, expect } from 'vitest';
import { extractTitles, filterByUserId } from '../src/postUtils.js';

describe('extractTitles', () => {
  it('게시물 배열에서 제목만 추출한다', () => {
    const posts = [
      { id: 1, userId: 1, title: '첫 번째 게시물', body: '...' },
      { id: 2, userId: 1, title: '두 번째 게시물', body: '...' },
    ];

    expect(extractTitles(posts)).toEqual(['첫 번째 게시물', '두 번째 게시물']);
  });

  it('빈 배열이 들어오면 빈 배열을 반환한다', () => {
    expect(extractTitles([])).toEqual([]);
  });
});

describe('filterByUserId', () => {
  it('특정 userId의 게시물만 반환한다', () => {
    const posts = [
      { id: 1, userId: 1, title: '게시물 1' },
      { id: 2, userId: 2, title: '게시물 2' },
      { id: 3, userId: 1, title: '게시물 3' },
    ];

    const result = filterByUserId(posts, 1);
    expect(result).toHaveLength(2);
    expect(result[0].title).toBe('게시물 1');
    expect(result[1].title).toBe('게시물 3');
  });
});
```

### Vitest로 테스트 실행

```bash
npx vitest run
```

```
✓ tests/postUtils.test.js (3 tests)
  ✓ extractTitles > 게시물 배열에서 제목만 추출한다
  ✓ extractTitles > 빈 배열이 들어오면 빈 배열을 반환한다
  ✓ filterByUserId > 특정 userId의 게시물만 반환한다

Test Files  1 passed (1)
Tests       3 passed (3)
```

### vi.fn()으로 fetch 모킹하기 (심화)

실제 fetch를 테스트하고 싶다면 `vi.fn()`으로 모의 함수를 만들 수 있습니다.

```javascript
// tests/api.test.js
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchPostTitles } from '../src/api.js';

// fetch를 전역 모의 함수로 교체
beforeEach(() => {
  global.fetch = vi.fn();
});

it('fetchPostTitles가 게시물 제목 배열을 반환한다', async () => {
  // fetch가 이 응답을 반환하도록 설정
  global.fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => [
      { id: 1, userId: 1, title: '테스트 제목 1' },
      { id: 2, userId: 1, title: '테스트 제목 2' },
    ],
  });

  const titles = await fetchPostTitles(1);
  expect(titles).toEqual(['테스트 제목 1', '테스트 제목 2']);
});
```

> 모킹은 처음에 복잡해 보입니다. 지금은 "로직을 순수 함수로 분리해서 테스트"하는 방법에 집중하세요. 모킹은 11장 미니 프로젝트에서 더 연습합니다.

---

<a id="part7"></a>

## 7️⃣ 실습 과제 [↑](#toc)

### 기본 과제 — 게시물 목록 가져와 제목 출력

JSONPlaceholder API를 사용해서 다음을 구현하세요:

1. 페이지 로드 시 `https://jsonplaceholder.typicode.com/posts` 에서 게시물 목록을 가져온다
2. 각 게시물의 제목을 `<li>` 요소로 목록에 표시한다
3. 로딩 중에는 "불러오는 중..." 텍스트를 표시한다
4. 에러가 발생하면 "데이터를 불러올 수 없습니다" 메시지를 표시한다

```html
<!-- 제공된 HTML 구조 -->
<p id="status">불러오는 중...</p>
<ul id="postList"></ul>
```

### 도전 과제 — 사용자 선택 → 해당 게시물만 표시

다음 기능을 추가하세요:

1. 페이지 로드 시 사용자 목록(`/users`)을 `<select>` 드롭다운에 표시한다
2. 사용자를 선택하면 해당 사용자의 게시물만(`/posts?userId=N`) 아래에 표시된다
3. `extractTitles`와 `filterByUserId` 함수를 별도 파일로 분리하고 Vitest 테스트를 작성한다

```html
<!-- 제공된 HTML 구조 -->
<select id="userSelect">
  <option value="">사용자를 선택하세요</option>
</select>
<ul id="postList"></ul>
```

---

<a id="part8"></a>

## 8️⃣ 정리 [↑](#toc)

이 장에서 배운 핵심을 정리합니다.

| 개념 | 핵심 내용 |
|------|-----------|
| 동기 vs 비동기 | 동기: 순서대로 기다림. 비동기: 기다리는 동안 다른 일 처리 |
| 콜백 | 나중에 실행될 함수. `addEventListener`, `setTimeout`에서 이미 사용 |
| Promise | 미래 값을 나타내는 객체. `.then()/.catch()`로 처리 |
| `async/await` | Promise를 동기 코드처럼 읽기 쉽게 쓰는 문법. `try/catch`로 에러 처리 |
| `fetch` | HTTP 요청 내장 함수. `res.ok` 확인 필수 |
| 테스트 전략 | 로직을 순수 함수로 분리해서 테스트. 네트워크 없이도 확인 가능 |

### Phase 2 핵심 원칙 복습

비동기 코드는 AI가 자주 실수하는 영역입니다. `await` 누락, 에러 처리 부재, 비동기 함수에서 `return` 누락 — 이 세 가지가 가장 흔한 버그입니다. AI가 생성한 비동기 코드는 항상 이 세 가지를 먼저 확인하세요.

### 다음 장 미리보기

**11장: 미니 프로젝트 — AI 협업 ToDo 앱**

지금까지 배운 모든 것을 합칩니다. DOM 조작, 이벤트, 비동기, 테스트를 결합한 ToDo 앱을 AI와 협업해서 만듭니다. 이것이 Phase 2의 최종 관문입니다.


→ **다음 내용으로 넘어갑시다**: [11. 미니 프로젝트 — AI 협업 ToDo 앱](/ai-native-js/todo-app)
