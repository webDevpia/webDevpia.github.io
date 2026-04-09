---
title: 09. DOM 조작과 이벤트
layout: default
grand_parent: Language
parent: JavaScript
nav_order: 9
permalink: /language/javascript/dom-events
---


## 학습 목표

- DOM으로 HTML 요소를 선택, 생성, 수정, 삭제할 수 있다
- 이벤트 리스너를 등록하여 사용자 상호작용에 반응할 수 있다

> **사전 안내:** 이 장부터는 **HTML 파일 + 브라우저**에서 실습합니다.
> VSCode에서 HTML 파일을 만들고 **Live Server** 확장으로 실행하세요.

<a id="toc"></a>

## 진행 순서

1. [DOM이란?](#part1) - HTML을 조작하는 리모컨
2. [요소 선택하기](#part2) - getElementById, querySelector
3. [요소 수정하기](#part3) - textContent, style, classList
4. [요소 생성과 삭제](#part4) - createElement, appendChild, remove
5. [이벤트(Event)](#part5) - addEventListener로 사용자 반응 처리
6. [실용 예제: 간단한 카운터 앱](#part6) - HTML + CSS + JS 통합
7. [정리](#part7) - 핵심 개념 요약 및 다음 장 미리보기

---

# 09장. DOM 조작과 이벤트

<a id="part1"></a>

## 1️⃣ DOM이란? [↑](#toc)

### 리모컨 비유

> TV 리모컨은 TV 화면의 각 채널, 볼륨, 밝기를 **선택해서 조작**합니다.
> **JavaScript가 리모컨**이고, **DOM이 TV 화면의 각 부분**입니다.
> DOM을 이용하면 JavaScript로 HTML 요소를 마음대로 선택하고 바꿀 수 있습니다.

**DOM(Document Object Model)**은 HTML 문서를 **트리(tree) 구조**로 표현한 것입니다.
브라우저가 HTML 파일을 읽으면 아래처럼 DOM 트리를 만듭니다.

```
HTML 파일                       DOM 트리
─────────────────               ─────────────────────
<html>                          document
  <body>                        └── html
    <h1>제목</h1>                    └── body
    <p>내용</p>                          ├── h1 ("제목")
  </body>                               └── p ("내용")
</html>
```

### document 객체

`document`는 DOM 트리의 **최상위 진입점**입니다.
`document.body`, `document.title` 등으로 HTML 전체에 접근할 수 있습니다.

### 실습용 HTML 기본 템플릿

이 장 전체에서 아래 파일(`index.html`)을 기준으로 실습합니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>DOM 실습</title>
</head>
<body>

  <h1 id="title">안녕하세요!</h1>
  <button id="btn">클릭하세요</button>

  <ul id="list">
    <li class="item">사과</li>
    <li class="item">바나나</li>
    <li class="item">체리</li>
  </ul>

  <script src="app.js"></script>
</body>
</html>
```

> `<script>` 태그는 `</body>` 바로 앞에 두세요. HTML이 모두 로드된 뒤 JS가 실행됩니다.

---

<a id="part2"></a>

## 2️⃣ 요소 선택하기 [↑](#toc)

DOM을 조작하려면 먼저 **원하는 HTML 요소를 선택**해야 합니다.

### getElementById — ID로 단일 요소 선택

```javascript
// id="title" 인 요소를 선택
const title = document.getElementById("title");
console.log(title); // <h1 id="title">안녕하세요!</h1>
```

### querySelector — CSS 선택자로 단일 요소 선택

CSS 선택자(`#id`, `.class`, `태그명`) 문법을 그대로 사용합니다.
조건에 맞는 요소 중 **첫 번째 하나만** 반환합니다.

```javascript
// id 선택자로 버튼 선택
const btn = document.querySelector("#btn");

// 클래스 선택자로 첫 번째 li 선택
const firstItem = document.querySelector(".item");

// 태그명으로 h1 선택
const heading = document.querySelector("h1");
```

### querySelectorAll — CSS 선택자로 여러 요소 선택

조건에 맞는 **모든 요소를 NodeList(배열과 유사)**로 반환합니다.

```javascript
// class="item" 인 모든 li 선택
const items = document.querySelectorAll(".item");

// forEach로 순회
items.forEach((item) => {
    console.log(item.textContent); // 사과, 바나나, 체리
});
```

실행 결과:
```
사과
바나나
체리
```

### 비교 표

| 메서드 | 선택 기준 | 반환값 | 여러 개 선택 |
|---|---|---|---|
| `getElementById("id")` | ID | 요소 1개 | 불가 |
| `querySelector("선택자")` | CSS 선택자 | 요소 1개 (첫 번째) | 불가 |
| `querySelectorAll("선택자")` | CSS 선택자 | NodeList (배열 유사) | 가능 |

> **실무 팁:** 현재는 `querySelector` / `querySelectorAll`을 가장 많이 씁니다.
> CSS 선택자를 이미 알고 있다면 별도로 배울 문법이 없습니다.

---

<a id="part3"></a>

## 3️⃣ 요소 수정하기 [↑](#toc)

요소를 선택했다면, 내용이나 스타일을 바꿀 수 있습니다.

### textContent — 텍스트 변경

```javascript
const title = document.querySelector("#title");

// 텍스트 읽기
console.log(title.textContent); // 안녕하세요!

// 텍스트 쓰기
title.textContent = "반갑습니다!";
// 화면의 h1이 "반갑습니다!"로 바뀜
```

### innerHTML — HTML 태그 포함 삽입

```javascript
const title = document.querySelector("#title");

// HTML 태그까지 포함해서 넣기
title.innerHTML = "<strong>굵은</strong> 제목";
// 화면: 굵은 제목 (굵게 표시됨)
```

> **주의 — XSS(Cross-Site Scripting) 위험:**
> 사용자가 입력한 값을 그대로 `innerHTML`에 넣으면 악성 스크립트가 실행될 수 있습니다.
> 사용자 입력 값은 `textContent`를 사용하세요.

### style — 인라인 스타일 변경

CSS 속성명에서 하이픈(`-`)을 빼고 **카멜케이스(camelCase)**로 씁니다.
예: `background-color` → `backgroundColor`

```javascript
const title = document.querySelector("#title");

title.style.color = "red";            // 글자색 빨간색
title.style.fontSize = "32px";        // 글자 크기
title.style.backgroundColor = "#eee"; // 배경색
```

### classList — CSS 클래스 조작

인라인 스타일 대신 **CSS 클래스를 추가/제거**하는 방법이 더 권장됩니다.

```javascript
const title = document.querySelector("#title");

title.classList.add("highlight");    // 클래스 추가
title.classList.remove("highlight"); // 클래스 제거
title.classList.toggle("highlight"); // 있으면 제거, 없으면 추가
title.classList.contains("highlight"); // 포함 여부 확인 (true/false)
```

### setAttribute / getAttribute — 속성 제어

```javascript
const btn = document.querySelector("#btn");

btn.setAttribute("disabled", "true");   // disabled 속성 추가
btn.getAttribute("id");                 // "btn" 반환
btn.removeAttribute("disabled");        // disabled 속성 제거
```

### 실용 예시: 버튼 클릭 시 텍스트 색상 변경

```javascript
// app.js
const btn   = document.querySelector("#btn");
const title = document.querySelector("#title");

btn.addEventListener("click", () => {
    // 클래스 토글로 색상 전환
    title.classList.toggle("red-text");
});
```

```css
/* style.css */
.red-text {
    color: red;
}
```

> 버튼을 클릭할 때마다 제목이 빨간색 ↔ 기본색으로 전환됩니다.

---

<a id="part4"></a>

## 4️⃣ 요소 생성과 삭제 [↑](#toc)

### createElement — 새 요소 생성

```javascript
// <li> 요소를 새로 만들기
const newItem = document.createElement("li");
newItem.textContent = "망고";
```

### appendChild / prepend — 자식으로 추가

```javascript
const list = document.querySelector("#list");

// 마지막 자식으로 추가
list.appendChild(newItem);

// 첫 번째 자식으로 추가
const firstItem = document.createElement("li");
firstItem.textContent = "딸기";
list.prepend(firstItem);
```

### remove — 요소 삭제

```javascript
// 특정 요소 직접 삭제
const firstLi = document.querySelector(".item");
firstLi.remove();
```

### 실용 예시: 동적 리스트 항목 추가/삭제

```html
<!-- index.html 추가 부분 -->
<input id="input" placeholder="과일 이름 입력">
<button id="add-btn">추가</button>
<ul id="fruit-list"></ul>
```

```javascript
// app.js
const input    = document.querySelector("#input");
const addBtn   = document.querySelector("#add-btn");
const fruitList = document.querySelector("#fruit-list");

addBtn.addEventListener("click", () => {
    const text = input.value.trim(); // 앞뒤 공백 제거

    if (text === "") return; // 빈 입력 무시

    // 새 li 요소 생성
    const li = document.createElement("li");
    li.textContent = text;

    // 삭제 버튼도 함께 추가
    const delBtn = document.createElement("button");
    delBtn.textContent = "삭제";
    delBtn.addEventListener("click", () => li.remove());

    li.appendChild(delBtn);
    fruitList.appendChild(li);

    input.value = ""; // 입력창 초기화
});
```

실행 결과 (화면 모습):
```
[망고 입력창] [추가]

• 사과 [삭제]
• 바나나 [삭제]
```

---

<a id="part5"></a>

## 5️⃣ 이벤트(Event) [↑](#toc)

### 초인종 비유

> 누군가 **초인종(이벤트)**을 누르면, 집주인이 **문을 열러 갑니다(이벤트 핸들러)**.
> 이벤트는 "무언가 발생했다"는 신호이고,
> 이벤트 핸들러(handler)는 그 신호를 받아 실행되는 함수입니다.

### addEventListener 기본 구조

```javascript
요소.addEventListener("이벤트종류", 핸들러함수);
```

```javascript
const btn = document.querySelector("#btn");

btn.addEventListener("click", () => {
    console.log("버튼이 클릭됐습니다!");
});
```

실행 결과 (버튼 클릭 시):
```
버튼이 클릭됐습니다!
```

### 주요 이벤트 종류

| 이벤트 | 발생 시점 | 주 사용 요소 |
|---|---|---|
| `click` | 마우스 클릭 | 버튼, 링크 |
| `input` | 입력값 변경 (실시간) | input, textarea |
| `submit` | 폼 제출 | form |
| `keydown` | 키보드 키를 누를 때 | input, document |
| `mouseover` | 마우스 포인터가 올라올 때 | 모든 요소 |
| `load` | 페이지/이미지 로드 완료 | window, img |

### 이벤트 객체 (event parameter)

핸들러 함수의 첫 번째 매개변수로 **이벤트 정보**가 자동으로 전달됩니다.

```javascript
const btn = document.querySelector("#btn");

btn.addEventListener("click", (event) => {
    console.log(event.type);   // "click" — 이벤트 종류
    console.log(event.target); // <button id="btn"> — 이벤트가 발생한 요소
});
```

키보드 이벤트에서는 어떤 키를 눌렀는지 확인할 수 있습니다.

```javascript
const input = document.querySelector("#input");

input.addEventListener("keydown", (event) => {
    console.log(event.key); // "Enter", "a", "Backspace" 등
});
```

### event.preventDefault() — 기본 동작 막기

브라우저에는 요소마다 **기본 동작**이 있습니다.
예: `<form>` 제출 시 페이지 새로고침, `<a>` 클릭 시 링크 이동.
`event.preventDefault()`로 이 기본 동작을 막을 수 있습니다.

```html
<form id="my-form">
  <input id="name-input" placeholder="이름">
  <button type="submit">제출</button>
</form>
<p id="result"></p>
```

```javascript
const form   = document.querySelector("#my-form");
const result = document.querySelector("#result");

form.addEventListener("submit", (event) => {
    event.preventDefault(); // 페이지 새로고침 방지

    const name = document.querySelector("#name-input").value;
    result.textContent = `안녕하세요, ${name}님!`;
});
```

실행 결과 (이름 입력 후 제출 클릭):
```
안녕하세요, 김철수님!
```

### 실용 예시: 입력 필드 실시간 글자수 카운터

```html
<textarea id="message" maxlength="100" placeholder="메시지 입력"></textarea>
<p id="counter">0 / 100</p>
```

```javascript
const message = document.querySelector("#message");
const counter = document.querySelector("#counter");

message.addEventListener("input", () => {
    const len = message.value.length; // 현재 입력 글자수
    counter.textContent = `${len} / 100`;

    // 80자 이상이면 경고색 표시
    if (len >= 80) {
        counter.style.color = "red";
    } else {
        counter.style.color = "black";
    }
});
```

실행 결과 (타이핑 중):
```
안녕하세요 반갑습니다
                         10 / 100
```

---

<a id="part6"></a>

## 6️⃣ 실용 예제: 간단한 카운터 앱 [↑](#toc)

지금까지 배운 DOM 선택, 수정, 이벤트를 모두 합쳐 **카운터 앱**을 만들어 봅니다.

### 전체 코드

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>카운터 앱</title>
  <style>
    body {
      font-family: sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding-top: 60px;
    }

    #count {
      font-size: 80px;
      font-weight: bold;
      margin: 20px 0;
    }

    .btn-group {
      display: flex;
      gap: 12px;
    }

    button {
      font-size: 20px;
      padding: 10px 24px;
      cursor: pointer;
      border: none;
      border-radius: 8px;
    }

    #plus-btn  { background-color: #4caf50; color: white; }
    #minus-btn { background-color: #f44336; color: white; }
    #reset-btn { background-color: #9e9e9e; color: white; }
  </style>
</head>
<body>

  <h2>카운터</h2>
  <div id="count">0</div>

  <div class="btn-group">
    <button id="minus-btn">-1</button>
    <button id="reset-btn">리셋</button>
    <button id="plus-btn">+1</button>
  </div>

  <script>
    // 현재 카운트 값을 변수로 관리
    let count = 0;

    // 요소 선택
    const countDisplay = document.querySelector("#count");
    const plusBtn      = document.querySelector("#plus-btn");
    const minusBtn     = document.querySelector("#minus-btn");
    const resetBtn     = document.querySelector("#reset-btn");

    // 화면 업데이트 함수
    function updateDisplay() {
        countDisplay.textContent = count;

        // 양수면 초록, 음수면 빨강, 0이면 검정
        if (count > 0) {
            countDisplay.style.color = "#4caf50";
        } else if (count < 0) {
            countDisplay.style.color = "#f44336";
        } else {
            countDisplay.style.color = "#333";
        }
    }

    // +1 버튼
    plusBtn.addEventListener("click", () => {
        count++;
        updateDisplay();
    });

    // -1 버튼
    minusBtn.addEventListener("click", () => {
        count--;
        updateDisplay();
    });

    // 리셋 버튼
    resetBtn.addEventListener("click", () => {
        count = 0;
        updateDisplay();
    });
  </script>

</body>
</html>
```

### 실행 결과 (화면 모습)

```
          카운터

             3        ← 초록색으로 표시

    [ -1 ]  [ 리셋 ]  [ +1 ]
```

| 동작 | 결과 |
|---|---|
| +1 버튼 클릭 | 숫자 1 증가, 양수면 초록색 |
| -1 버튼 클릭 | 숫자 1 감소, 음수면 빨간색 |
| 리셋 버튼 클릭 | 0으로 초기화, 검정색 |

---

<a id="part7"></a>

## 7️⃣ 정리 [↑](#toc)

### 핵심 개념 요약

| 분류 | 문법 | 역할 |
|---|---|---|
| 요소 선택 | `document.getElementById("id")` | ID로 요소 1개 선택 |
| 요소 선택 | `document.querySelector("선택자")` | CSS 선택자로 요소 1개 |
| 요소 선택 | `document.querySelectorAll("선택자")` | CSS 선택자로 여러 요소 |
| 내용 수정 | `element.textContent = "..."` | 텍스트 변경 |
| 내용 수정 | `element.innerHTML = "..."` | HTML 포함 변경 |
| 스타일 | `element.style.color = "red"` | 인라인 스타일 |
| 클래스 | `element.classList.toggle("cls")` | 클래스 추가/제거 |
| 요소 생성 | `document.createElement("태그")` | 새 요소 만들기 |
| 요소 추가 | `parent.appendChild(child)` | 마지막 자식으로 추가 |
| 요소 삭제 | `element.remove()` | 요소 삭제 |
| 이벤트 | `element.addEventListener("click", fn)` | 이벤트 리스너 등록 |
| 기본동작 | `event.preventDefault()` | 기본 동작 방지 |

### 다음 장 미리보기

**10장: 실전 프로젝트 — To-Do 앱**
이 장에서 배운 DOM 조작과 이벤트를 활용해 실제 할 일 목록 앱을 만들어 봅니다.
항목 추가, 완료 체크, 삭제 기능을 갖춘 완성도 있는 프로젝트입니다.

---

### 실습 과제

**기본 — 버튼 클릭 시 배경색 변경**

버튼을 클릭할 때마다 `document.body`의 배경색이 무작위로 바뀌도록 만들어 보세요.

```javascript
// 힌트: Math.random()으로 임의의 색상값 생성
const randomColor = () =>
    "#" + Math.floor(Math.random() * 0xFFFFFF).toString(16).padStart(6, "0");
```

---

**중급 — 이름 입력 후 Enter → 리스트에 추가**

입력 필드에 이름을 입력하고 Enter 키를 누르면 아래 `<ul>`에 `<li>`로 추가되도록 만들어 보세요.

```javascript
// 힌트: keydown 이벤트에서 event.key === "Enter" 확인
input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        // 리스트에 추가하는 코드 작성
    }
});
```

---

**심화 — 카운터 앱에 최대값/최소값 제한 추가**

6절의 카운터 앱을 수정하여, 숫자가 **0 미만으로 내려가거나 10을 초과하지 않도록** 제한하세요.
한계에 도달하면 해당 버튼이 비활성화(disabled)되도록 구현해 보세요.

```javascript
// 힌트: setAttribute("disabled", "") / removeAttribute("disabled")
```
