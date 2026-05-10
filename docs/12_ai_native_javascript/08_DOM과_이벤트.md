---
title: 08. DOM과 이벤트
layout: default
parent: AI-Native JavaScript
nav_order: 9
permalink: /ai-native-js/dom
---
# 08장. DOM과 이벤트 — AI가 쓴 코드 읽기

{: .no_toc }

> **Phase 2**

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 생성 + 검증 모드**
>
> AI(Copilot)가 코드를 생성할 수 있습니다.
>
> 단, 반드시 생성된 코드를 **읽고, 이해하고, 테스트로 검증**해야 합니다.
>
> AI 코드를 이해 없이 복붙하는 것은 금지입니다.

---

## 학습 목표

- DOM이 무엇인지 설명할 수 있다
- `querySelector`, `getElementById`로 HTML 요소를 선택할 수 있다
- 이벤트 리스너를 등록하고 사용자 입력에 반응할 수 있다
- AI가 생성한 DOM 코드를 한 줄씩 읽고 설명할 수 있다

`<a id="toc"></a>`

## 진행 순서

1. [DOM이란?](#part1) — HTML의 가계도(트리)
2. [요소 선택하기](#part2) — getElementById, querySelector, querySelectorAll
3. [요소 변경하기](#part3) — textContent, innerHTML, style, classList
4. [이벤트 리스너](#part4) — addEventListener 패턴
5. [AI가 생성한 DOM 코드 읽기](#part5) — 한 줄씩 설명하기
6. [실습 과제](#part6) — 기본 / 도전
7. [정리](#part7) — 핵심 요약 및 다음 장

---

`<a id="part1"></a>`

## 1. 📖 **더 알아보기** — DOM이란? [↑](#toc)

브라우저는 HTML 파일을 읽을 때 단순한 텍스트로 보관하지 않습니다. 마치 조직도를 그리듯이, HTML 태그 하나하나를 **나무(트리) 구조**로 변환합니다. 이 구조를 **DOM(Document Object Model)**이라고 부릅니다.

> 가계도를 상상해보세요.
> 할아버지 → 아버지/삼촌 → 나/형제 순으로 이어지는 구조입니다.
> HTML에서 `<html>`은 최상위 조상이고, `<body>` 안의 태그들은 자식과 손자입니다.
> JavaScript는 이 가계도를 보며 "세 번째 손자 요소의 글자를 바꿔줘"라고 명령합니다.

### HTML이 DOM 트리로 변환되는 과정

아래 HTML 코드를 보면:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>나의 페이지</title>
  </head>
  <body>
    <h1 id="title">안녕하세요</h1>
    <p class="intro">반갑습니다</p>
    <button id="btn">클릭</button>
  </body>
</html>
```

브라우저는 이것을 다음과 같은 트리로 읽습니다:

```
document
└── html
    ├── head
    │   └── title ("나의 페이지")
    └── body
        ├── h1#title ("안녕하세요")
        ├── p.intro ("반갑습니다")
        └── button#btn ("클릭")
```

### document 객체

JavaScript에서 이 트리 전체를 `document`라는 객체로 접근합니다. `document`는 브라우저가 자동으로 만들어주는 특별한 객체입니다.

```javascript
// 브라우저 콘솔에서 실행해보세요
console.log(document);           // 전체 HTML 문서 객체
console.log(document.title);     // "나의 페이지"
console.log(document.body);      // <body> 요소 전체
```

---

`<a id="part2"></a>`

## 2. ⭐ **핵심** — 요소 선택하기 [↑](#toc)

DOM 트리에서 원하는 요소를 꺼내오는 방법은 여러 가지입니다. 마치 도서관에서 책을 찾는 방법이 "책 번호로 찾기", "제목으로 찾기", "분류별 찾기"처럼 다양한 것과 같습니다.

> 강사 시연을 보면서 따라하세요

### getElementById — ID로 요소 하나 선택

```html
<h1 id="title">안녕하세요</h1>
```

```javascript
const titleEl = document.getElementById('title');
console.log(titleEl);          // <h1 id="title">안녕하세요</h1>
console.log(titleEl.textContent); // "안녕하세요"
```

- `id`는 페이지 안에서 **유일**해야 합니다.
- 없는 id를 입력하면 `null`을 반환합니다.

### querySelector — CSS 선택자로 요소 하나 선택

CSS에서 쓰던 선택자 문법을 그대로 사용할 수 있습니다.

```html
<p class="intro">반갑습니다</p>
<button id="btn">클릭</button>
<input type="text" placeholder="이름 입력">
```

```javascript
// id 선택: # 사용
const btn = document.querySelector('#btn');

// class 선택: . 사용
const intro = document.querySelector('.intro');

// 태그 선택
const input = document.querySelector('input');

// 조합 선택: div 안의 p
const p = document.querySelector('div p');
```

`querySelector`는 조건에 맞는 **첫 번째 요소**만 반환합니다.

### querySelectorAll — 여러 요소를 한꺼번에 선택

```html
<ul>
  <li class="item">사과</li>
  <li class="item">바나나</li>
  <li class="item">딸기</li>
</ul>
```

```javascript
const items = document.querySelectorAll('.item');
console.log(items.length); // 3

// forEach로 순회
items.forEach((item) => {
  console.log(item.textContent);
});
// 출력:
// 사과
// 바나나
// 딸기
```

### 세 가지 선택 방법 비교

| 메서드               | 선택 기준  | 반환값                 | 여러 개 선택 |
| -------------------- | ---------- | ---------------------- | ------------ |
| `getElementById`   | id 속성    | 요소 하나 또는 null    | 불가         |
| `querySelector`    | CSS 선택자 | 첫 번째 요소 또는 null | 불가         |
| `querySelectorAll` | CSS 선택자 | NodeList (배열과 유사) | 가능         |

> 실무에서는 `querySelector`와 `querySelectorAll`을 가장 많이 씁니다.
> CSS 선택자를 이미 알고 있다면 배울 것이 거의 없습니다.

---

`<a id="part3"></a>`

## 3. 요소 변경하기 [↑](#toc)

요소를 선택했다면 이제 내용이나 스타일을 바꿀 수 있습니다.

### textContent — 텍스트 바꾸기

```javascript
const title = document.querySelector('#title');

// 읽기
console.log(title.textContent); // "안녕하세요"

// 쓰기
title.textContent = '반가워요!';
// 페이지에 "반가워요!"가 표시됩니다
```

### innerHTML — HTML 태그 포함해서 바꾸기

```javascript
const container = document.querySelector('#container');

container.innerHTML = '<strong>굵은 글씨</strong>입니다';
// 페이지에 굵은 글씨가 표시됩니다
```

> **주의**: `innerHTML`에 사용자가 직접 입력한 값을 넣으면 보안 문제가 생길 수 있습니다.
> 이 문제는 09장 Bug Hunt에서 자세히 다룹니다.

### style — CSS 스타일 바꾸기

```javascript
const box = document.querySelector('#box');

box.style.color = 'red';
box.style.backgroundColor = 'yellow'; // CSS의 background-color를 camelCase로!
box.style.fontSize = '20px';
```

### classList — CSS 클래스 추가/제거/토글

CSS 파일에 미리 클래스를 정의해두고, JavaScript로 클래스를 붙이고 떼는 방식이 더 깔끔합니다.

```css
/* style.css */
.highlight {
  background-color: yellow;
  font-weight: bold;
}
.hidden {
  display: none;
}
```

```javascript
const el = document.querySelector('#message');

el.classList.add('highlight');    // 클래스 추가
el.classList.remove('highlight'); // 클래스 제거
el.classList.toggle('hidden');    // 있으면 제거, 없으면 추가
el.classList.contains('highlight'); // true 또는 false 반환
```

### 실습: 색상 변경 버튼 만들기

> 💡 `index.html`과 `app.js` 두 파일을 만드세요. HTML 파일의 `</body>` 앞에 `<script src="app.js"></script>`를 추가하세요.

```html
<!-- index.html -->
<div id="box" style="width:200px; height:200px; background:blue;"></div>
<button id="changeBtn">색상 바꾸기</button>
<script src="app.js"></script>
```

```javascript
// app.js
const box = document.querySelector('#box');
const btn = document.querySelector('#changeBtn');

const colors = ['blue', 'red', 'green', 'orange', 'purple'];
let currentIndex = 0;

btn.addEventListener('click', () => {
  currentIndex = (currentIndex + 1) % colors.length;
  box.style.backgroundColor = colors[currentIndex];
});
```

버튼을 클릭할 때마다 박스 색상이 blue → red → green → orange → purple → blue 순으로 바뀝니다.

---

`<a id="part4"></a>`

## 4. ⭐ **핵심** — 이벤트 리스너 [↑](#toc)

> 강사 시연을 보면서 따라하세요

사용자가 버튼을 클릭하거나, 키보드를 누르거나, 폼을 제출하면 브라우저는 **이벤트**를 발생시킵니다. JavaScript는 이 이벤트를 듣고(listen) 반응합니다.

> 카페에서 번호 알림판을 상상해보세요.
> 직원이 "37번 손님!"이라고 외칠 때(이벤트 발생),
> 37번 손님이 일어나 음료를 받으러 갑니다(이벤트 핸들러 실행).
> `addEventListener`는 "나는 이 이벤트를 기다리겠다"고 등록하는 것입니다.

### addEventListener 기본 패턴

```javascript
요소.addEventListener('이벤트종류', 실행할함수);
```

```javascript
const btn = document.querySelector('#btn');

btn.addEventListener('click', () => {
  console.log('버튼이 클릭되었습니다!');
});
```

### onclick vs addEventListener

```javascript
// 방법 1: onclick 속성 (옛날 방식)
btn.onclick = () => {
  console.log('클릭!');
};

// 방법 2: addEventListener (권장)
btn.addEventListener('click', () => {
  console.log('클릭!');
});
```

`addEventListener`가 더 나은 이유:

- 같은 요소에 여러 핸들러를 등록할 수 있습니다
- `removeEventListener`로 나중에 제거할 수 있습니다
- 현대 JavaScript 프로젝트에서 표준으로 쓰입니다

### 자주 쓰는 이벤트 종류

```javascript
// click: 클릭했을 때
btn.addEventListener('click', () => { ... });

// input: input 값이 바뀔 때마다 (타이핑 중)
const inputEl = document.querySelector('input');
inputEl.addEventListener('input', (e) => {
  console.log(e.target.value); // 현재 입력값
});

// keydown: 키보드 키를 눌렀을 때
document.addEventListener('keydown', (e) => {
  console.log(e.key); // 눌린 키 이름: "Enter", "a", "ArrowUp" 등
});

// submit: 폼이 제출될 때
const form = document.querySelector('form');
form.addEventListener('submit', (e) => {
  e.preventDefault(); // 페이지 새로고침 방지
  console.log('폼이 제출됐습니다');
});
```

### 이벤트 객체 (e)

이벤트 핸들러 함수는 **이벤트 객체**를 매개변수로 받습니다. 보통 `e` 또는 `event`라고 이름 붙입니다.

```javascript
inputEl.addEventListener('input', (e) => {
  // e.target: 이벤트가 발생한 요소
  // e.target.value: 그 요소의 현재 값
  const text = e.target.value;
  console.log('입력값:', text);
});
```

### 실습: 인터랙티브 폼

```html
<!-- index.html -->
<form id="greetForm">
  <input type="text" id="nameInput" placeholder="이름을 입력하세요">
  <button type="submit">인사하기</button>
</form>
<p id="result"></p>
```

```javascript
// app.js
const form = document.querySelector('#greetForm');
const nameInput = document.querySelector('#nameInput');
const result = document.querySelector('#result');

form.addEventListener('submit', (e) => {
  e.preventDefault(); // 폼 제출 시 페이지 새로고침 막기

  const name = nameInput.value.trim();

  if (name === '') {
    result.textContent = '이름을 입력해주세요.';
    return;
  }

  result.textContent = `안녕하세요, ${name}님!`;
  nameInput.value = ''; // 입력 필드 초기화
});
```

---

`<a id="part5"></a>`

## 5. ⭐ **핵심** — AI가 생성한 DOM 코드 읽기 [↑](#toc)

> 강사 시연을 보면서 따라하세요

이제 Phase 2의 핵심 스킬을 연습합니다. AI가 생성한 코드를 **한 줄씩 읽고 설명**하는 것입니다.

"이해 없이 복붙"과 "읽고 설명할 수 있는 사용"은 완전히 다릅니다. AI 코드를 진정으로 내 것으로 만드는 방법은 각 줄이 무엇을 하는지 설명할 수 있어야 합니다.

### Copilot이 생성한 코드 예시 — 탭 컴포넌트

아래 코드는 "탭 버튼을 클릭하면 해당 탭 내용이 보이는 컴포넌트를 만들어줘"라고 요청했을 때 Copilot이 생성한 코드입니다.

**HTML:**

```html
<div class="tabs">
  <div class="tab-buttons">
    <button class="tab-btn active" data-tab="tab1">소개</button>
    <button class="tab-btn" data-tab="tab2">경험</button>
    <button class="tab-btn" data-tab="tab3">연락처</button>
  </div>
  <div class="tab-contents">
    <div id="tab1" class="tab-content active">
      <p>안녕하세요! 저는 JavaScript를 배우고 있습니다.</p>
    </div>
    <div id="tab2" class="tab-content">
      <p>6개월째 프론트엔드를 공부 중입니다.</p>
    </div>
    <div id="tab3" class="tab-content">
      <p>이메일: hello@example.com</p>
    </div>
  </div>
</div>
```

**CSS:**

```css
.tab-content { display: none; }
.tab-content.active { display: block; }
.tab-btn.active { background: #333; color: white; }
```

**JavaScript (Copilot 생성):**

```javascript
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach((btn) => {
  btn.addEventListener('click', () => {
    const targetId = btn.dataset.tab;

    tabBtns.forEach((b) => b.classList.remove('active'));
    tabContents.forEach((c) => c.classList.remove('active'));

    btn.classList.add('active');
    document.getElementById(targetId).classList.add('active');
  });
});
```

### "Explain It Back" 연습

이 코드를 읽고, 아래 빈칸을 한국어로 채워보세요. 직접 손으로 써보는 것을 권장합니다.

```javascript
// 1번 줄:
const tabBtns = document.querySelectorAll('.tab-btn');
// → 이 줄은: ___________________________________________

// 2번 줄:
const tabContents = document.querySelectorAll('.tab-content');
// → 이 줄은: ___________________________________________

// 3번 줄:
tabBtns.forEach((btn) => {
// → 이 줄은: ___________________________________________

// 4번 줄:
  btn.addEventListener('click', () => {
// → 이 줄은: ___________________________________________

// 5번 줄:
    const targetId = btn.dataset.tab;
// → 이 줄은: ___________________________________________
// → btn.dataset.tab이 무엇인지 HTML을 다시 보고 확인하세요

// 6번 줄:
    tabBtns.forEach((b) => b.classList.remove('active'));
// → 이 줄은: ___________________________________________

// 7번 줄:
    tabContents.forEach((c) => c.classList.remove('active'));
// → 이 줄은: ___________________________________________

// 8번 줄:
    btn.classList.add('active');
// → 이 줄은: ___________________________________________

// 9번 줄:
    document.getElementById(targetId).classList.add('active');
// → 이 줄은: ___________________________________________
```

### 정답 예시

```javascript
const tabBtns = document.querySelectorAll('.tab-btn');
// → CSS 클래스 .tab-btn을 가진 모든 버튼 요소를 선택해서 tabBtns에 저장한다

const tabContents = document.querySelectorAll('.tab-content');
// → CSS 클래스 .tab-content를 가진 모든 콘텐츠 영역을 선택해서 tabContents에 저장한다

tabBtns.forEach((btn) => {
// → tabBtns 배열의 각 버튼에 대해 반복한다. 각 버튼을 btn이라고 부른다

  btn.addEventListener('click', () => {
// → 이 버튼이 클릭될 때 실행할 함수를 등록한다

    const targetId = btn.dataset.tab;
// → 클릭된 버튼의 data-tab 속성값을 읽어온다. 예: "tab1", "tab2", "tab3"

    tabBtns.forEach((b) => b.classList.remove('active'));
// → 모든 탭 버튼에서 active 클래스를 제거한다 (선택된 상태 초기화)

    tabContents.forEach((c) => c.classList.remove('active'));
// → 모든 탭 콘텐츠에서 active 클래스를 제거한다 (보이는 상태 초기화)

    btn.classList.add('active');
// → 방금 클릭한 버튼에 active 클래스를 추가한다 (선택된 버튼 강조)

    document.getElementById(targetId).classList.add('active');
// → targetId에 해당하는 콘텐츠 요소를 찾아서 active 클래스를 추가한다 (내용 표시)
  });
});
```

> AI가 생성한 코드라도 이렇게 한 줄씩 설명할 수 있으면, 그 코드는 이제 내 코드입니다.
> 설명할 수 없는 코드는 아직 내 것이 아닙니다.

---

`<a id="part6"></a>`

## 6. 실습 과제 [↑](#toc)

### 기본 과제 — 할 일 입력 폼

다음 HTML을 기반으로 JavaScript를 직접 작성하세요. (AI를 쓰지 말고 직접 먼저 도전하세요!)

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>할 일 목록</title>
</head>
<body>
  <h1>할 일 목록</h1>
  <form id="todoForm">
    <input type="text" id="todoInput" placeholder="할 일을 입력하세요">
    <button type="submit">추가</button>
  </form>
  <ul id="todoList"></ul>

  <script src="app.js"></script>
</body>
</html>
```

구현해야 할 기능:

1. 텍스트를 입력하고 "추가" 버튼을 누르면 `<ul>` 목록에 `<li>`로 추가된다
2. 빈 텍스트는 추가되지 않는다
3. 추가 후 입력 필드가 비워진다

### 도전 과제 — AI 협업 이미지 갤러리

1. Copilot에게 다음과 같이 요청하세요:

   ```
   HTML, CSS, JavaScript로 이미지 갤러리를 만들어줘.
   이미지 배열이 있고, 클릭하면 크게 보이는 모달 창이 뜨고,
   모달 창 밖을 클릭하면 닫히는 기능이 있어야 해.
   ```
2. 생성된 JavaScript 코드 전체에 대해 "Explain It Back" 연습을 수행하세요.
   각 줄마다 한국어 주석으로 무엇을 하는지 설명하세요.
3. 설명이 안 되는 줄이 있다면:

   - MDN Web Docs에서 해당 메서드를 검색하세요
   - 그래도 모르겠으면 Copilot Chat에 "이 줄이 정확히 무엇을 하는지 설명해줘"라고 질문하세요

---

`<a id="part7"></a>`

## 7. 정리 [↑](#toc)

이 장에서 배운 핵심을 정리합니다.

| 개념                 | 핵심 내용                                                   |
| -------------------- | ----------------------------------------------------------- |
| DOM                  | 브라우저가 HTML을 트리 구조로 변환한 것.`document`로 접근 |
| `querySelector`    | CSS 선택자로 첫 번째 요소 선택                              |
| `querySelectorAll` | CSS 선택자로 모든 요소 선택 (NodeList 반환)                 |
| `textContent`      | 요소의 텍스트 내용 읽기/쓰기                                |
| `classList`        | 클래스 추가/제거/토글                                       |
| `addEventListener` | 이벤트 발생 시 실행할 함수 등록                             |
| "Explain It Back"    | AI 생성 코드를 한 줄씩 한국어로 설명하는 학습법             |

### Phase 2 핵심 원칙 복습

AI가 DOM 코드를 생성해줄 수 있습니다. 하지만 그 코드를 여러분이 설명할 수 있어야 진짜 배운 것입니다. 설명할 수 없는 코드는 복사한 것이지, 배운 것이 아닙니다.

### 다음 장 미리보기

**09장: AI 출력 평가법 — Bug Hunt**

AI가 항상 올바른 코드를 생성하지는 않습니다. 다음 장에서는 AI가 의도적으로 잘못 생성한 코드에서 버그를 찾는 실습을 합니다. 이것이 Phase 2의 가장 중요한 스킬입니다.

→ **다음 장**: [09. AI 출력 평가법 — Bug Hunt](/ai-native-js/bug-hunt)
