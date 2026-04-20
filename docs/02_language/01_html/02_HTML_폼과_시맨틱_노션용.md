---
nav_exclude: true
---

## 학습 목표

- 폼(Form) 요소로 사용자 입력을 받는 페이지를 만들 수 있다
- 시맨틱 태그로 의미 있는 HTML 구조를 작성할 수 있다

## 진행 순서

1. 폼(Form) 기초 — `<form>`, `<input>`, `<label>`, `<button>`
2. 폼 요소 심화 — `<select>`, `<textarea>`, `<fieldset>`
3. 시맨틱 태그 — `<header>`, `<main>`, `<footer>` 등
4. 유용한 HTML 요소들 — `<details>`, `<dialog>`, `<mark>`, `<progress>`
5. 실습: 회원가입 페이지 (시맨틱 구조) — 전체 코드
6. 정리 — 요약 표, 실습 과제

---

# 02장. HTML 폼과 시맨틱 태그

## 1️⃣ 폼(Form) 기초

### 종이 설문지 비유

> 폼(Form)은 **종이 설문지**와 같습니다.
> `<input>`은 응답자가 채우는 **빈칸**, `<button>`은 맨 아래의 **제출 버튼**,
> `<label>`은 각 빈칸 옆의 **질문 문구**입니다.

### 기본 폼 구조

```html
<form action="/login" method="post">
    <label for="username">아이디:</label>
    <input type="text" id="username" name="username" placeholder="아이디를 입력하세요">

    <label for="password">비밀번호:</label>
    <input type="password" id="password" name="password" placeholder="비밀번호를 입력하세요">

    <button type="submit">로그인</button>
</form>
```

**각 속성(attribute) 설명:**

| 속성 | 역할 |
|------|------|
| `action` | 폼 데이터를 전송할 서버 주소 |
| `method` | 전송 방식 (`get`: URL에 데이터 포함, `post`: 숨겨서 전송) |
| `for` | label과 input을 연결 (label의 `for` = input의 `id`) |
| `placeholder` | input이 비어있을 때 표시되는 안내 문구 |
| `required` | 비워두면 제출 불가 (필수 입력) |

### input 타입 종류

| `type` 값 | 설명 | 표시 형태 |
|-----------|------|-----------|
| `text` | 일반 텍스트 입력 | 일반 텍스트 박스 |
| `password` | 비밀번호 (입력 내용 숨김) | ●●●● 형태 |
| `email` | 이메일 형식 검증 포함 | 텍스트 박스 (@ 필요) |
| `number` | 숫자만 입력 | 위아래 화살표 포함 |
| `date` | 날짜 선택 | 달력 UI |
| `checkbox` | 다중 선택 가능한 체크박스 | □ |
| `radio` | 단일 선택만 가능한 라디오 버튼 | ○ |
| `file` | 파일 업로드 | "파일 선택" 버튼 |
| `range` | 슬라이더 | ————● |
| `color` | 색상 선택기 | 색상 팔레트 |
| `hidden` | 사용자에게 안 보이는 값 | 화면에 없음 |

### 실습: 간단한 로그인 폼

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>로그인</title>
</head>
<body>
    <h1>로그인</h1>

    <form action="#" method="post">
        <p>
            <label for="email">이메일:</label><br>
            <input type="email" id="email" name="email"
                   placeholder="example@email.com" required>
        </p>
        <p>
            <label for="pw">비밀번호:</label><br>
            <input type="password" id="pw" name="pw"
                   placeholder="비밀번호 8자 이상" required>
        </p>
        <p>
            <input type="checkbox" id="remember" name="remember">
            <label for="remember">로그인 상태 유지</label>
        </p>
        <button type="submit">로그인</button>
        <button type="reset">초기화</button>
    </form>
</body>
</html>
```

> `type="reset"` 버튼은 폼의 모든 입력값을 초기 상태로 되돌립니다.

---

## 2️⃣ 폼 요소 심화

### 드롭다운 선택: `<select>` + `<option>`

```html
<label for="country">국가 선택:</label>
<select id="country" name="country">
    <option value="">-- 선택하세요 --</option>
    <option value="kr">대한민국</option>
    <option value="us">미국</option>
    <option value="jp">일본</option>
</select>
```

**브라우저 결과:** 클릭하면 목록이 펼쳐지는 드롭다운 메뉴가 표시됩니다.

### 여러 줄 텍스트 입력: `<textarea>`

```html
<label for="bio">자기소개:</label><br>
<textarea id="bio" name="bio" rows="5" cols="40"
          placeholder="자기소개를 입력하세요 (최대 200자)"></textarea>
```

- `rows`: 세로 줄 수 (높이)
- `cols`: 가로 글자 수 (너비)
- 오른쪽 아래 모서리를 드래그하여 크기 조절 가능

### 입력 그룹화: `<fieldset>` + `<legend>`

```html
<fieldset>
    <legend>성별 선택</legend>

    <input type="radio" id="male" name="gender" value="male">
    <label for="male">남성</label>

    <input type="radio" id="female" name="gender" value="female">
    <label for="female">여성</label>

    <input type="radio" id="other" name="gender" value="other">
    <label for="other">기타</label>
</fieldset>
```

> `radio` 버튼은 `name` 속성이 같은 것끼리 묶입니다. 같은 그룹에서 하나만 선택됩니다.

### 실습: 회원가입 폼

```html
<form action="#" method="post">
    <fieldset>
        <legend>기본 정보</legend>
        <p>
            <label for="name">이름:</label><br>
            <input type="text" id="name" name="name" required>
        </p>
        <p>
            <label for="reg-email">이메일:</label><br>
            <input type="email" id="reg-email" name="email" required>
        </p>
        <p>
            <label for="reg-pw">비밀번호:</label><br>
            <input type="password" id="reg-pw" name="password" required>
        </p>
    </fieldset>

    <fieldset>
        <legend>추가 정보</legend>
        <p>성별:</p>
        <input type="radio" id="m" name="gender" value="m">
        <label for="m">남성</label>
        <input type="radio" id="f" name="gender" value="f">
        <label for="f">여성</label>

        <p>
            <label for="intro">자기소개:</label><br>
            <textarea id="intro" name="intro" rows="4" cols="40"
                      placeholder="간단히 소개해주세요"></textarea>
        </p>
    </fieldset>

    <button type="submit">가입하기</button>
</form>
```

---

## 3️⃣ 시맨틱 태그

### 방에 이름표 붙이기 비유

> `<div>`만 사용하면 집 안의 모든 방이 "방"이라는 이름만 가집니다.
> 하지만 `<header>`, `<nav>`, `<main>`, `<footer>` 등 **시맨틱(Semantic) 태그**로 이름을 붙이면
> "이 방은 현관, 이 방은 거실, 이 방은 부엌"처럼 **각 공간의 역할이 명확해집니다.**

### 주요 시맨틱 태그

| 태그 | 역할 |
|------|------|
| `<header>` | 페이지 상단 — 로고, 사이트 제목, 대표 내비게이션 |
| `<nav>` | 내비게이션(Navigation) — 메뉴 링크 모음 |
| `<main>` | 페이지의 핵심 콘텐츠 (페이지당 하나만) |
| `<section>` | 주제별 콘텐츠 묶음 (제목 포함 권장) |
| `<article>` | 독립적으로 배포 가능한 콘텐츠 (블로그 글, 뉴스 기사) |
| `<aside>` | 부가 정보 — 사이드바, 광고, 관련 링크 |
| `<footer>` | 페이지 하단 — 저작권, 연락처, 사이트맵 |

### 시맨틱 vs 비시맨틱 비교

```html
<!-- 비시맨틱: 의미 없는 div만 사용 -->
<div id="header">로고</div>
<div id="nav">메뉴</div>
<div id="content">내용</div>
<div id="footer">저작권</div>

<!-- 시맨틱: 역할이 명확한 태그 사용 -->
<header>로고</header>
<nav>메뉴</nav>
<main>내용</main>
<footer>저작권</footer>
```

두 코드의 브라우저 표시는 동일합니다. 하지만 시맨틱 태그를 쓰는 이유는:

| 이유 | 설명 |
|------|------|
| **접근성** | 스크린 리더(시각 장애인용 도구)가 "이곳은 내비게이션입니다"라고 올바르게 안내 |
| **SEO** | 검색엔진이 페이지 구조를 더 잘 이해하여 검색 순위 향상 |
| **유지보수** | 코드를 처음 보는 사람도 각 영역의 역할을 즉시 파악 |

### 페이지 레이아웃 예시 (ASCII 다이어그램)

```
+------------------------------------------+
|              <header>                    |
|  로고       내비게이션 메뉴               |
+------------------------------------------+
|   <nav> (선택적으로 별도 영역으로)        |
+------------------------------------------+
|  <main>                                  |
|  +--------------------+  +----------+   |
|  | <section>          |  | <aside>  |   |
|  | 주요 콘텐츠         |  | 사이드바  |   |
|  +--------------------+  +----------+   |
|  | <article>          |                  |
|  | 블로그 글 1         |                  |
|  +--------------------+                  |
+------------------------------------------+
|              <footer>                    |
|  저작권 © 2025 · 이메일: xxx@xxx.com     |
+------------------------------------------+
```

### 기본 시맨틱 구조 코드

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>시맨틱 HTML 예시</title>
</head>
<body>

    <header>
        <h1>나의 블로그</h1>
        <nav>
            <ul>
                <li></li>
                <li></li>
                <li></li>
            </ul>
        </nav>
    </header>

    <main>
        <section id="about">
            <h2>소개</h2>
            <p>웹 개발을 공부하는 블로그입니다.</p>
        </section>

        <section id="posts">
            <h2>최신 글</h2>
            <article>
                <h3>HTML 배우기</h3>
                <p>오늘부터 HTML을 공부했습니다...</p>
            </article>
            <article>
                <h3>CSS 입문</h3>
                <p>HTML 다음에는 CSS를 배웠습니다...</p>
            </article>
        </section>

        <aside>
            <h3>관련 링크</h3>
            <ul>
                <li><a href="https://developer.mozilla.org" target="_blank">MDN</a></li>
            </ul>
        </aside>
    </main>

    <footer>
        <p>&copy; 2025 나의 블로그. All rights reserved.</p>
    </footer>

</body>
</html>
```

---

## 4️⃣ 유용한 HTML 요소들

### 접이식 FAQ: `<details>` + `<summary>`

JavaScript 없이도 클릭하면 펼쳐지는 아코디언을 만들 수 있습니다.

```html
<details>
    <summary>HTML이 어렵지 않나요?</summary>
    <p>처음에는 낯설 수 있지만, 태그 구조를 익히면 금방 쉬워집니다.
    핵심은 태그의 '의미'를 기억하는 것입니다.</p>
</details>

<details>
    <summary>CSS와 HTML 중 무엇을 먼저 배워야 하나요?</summary>
    <p>HTML을 먼저 배우는 것이 일반적입니다.
    HTML로 구조를 만들고, 그 위에 CSS로 스타일을 입힙니다.</p>
</details>
```

**브라우저 결과:** `<summary>` 텍스트 옆에 ▶ 화살표가 생기며, 클릭하면 내용이 펼쳐집니다.

### 텍스트 하이라이트: `<mark>`

```html
<p>HTML에서 가장 중요한 개념은 <mark>시맨틱 태그</mark>입니다.</p>
```

**브라우저 결과:** "시맨틱 태그" 부분이 형광펜으로 칠한 것처럼 **노란 배경**으로 강조됩니다.

### 진행 상태 표시: `<progress>` + `<meter>`

```html
<!-- 작업 진행률 (0~100%) -->
<p>HTML 학습 진행률:</p>
<progress value="60" max="100">60%</progress>

<!-- 범위 내 측정값 (온도, 점수 등) -->
<p>현재 만족도:</p>
<meter value="7" min="0" max="10" low="3" high="8" optimum="9">7/10</meter>
```

**`<progress>`** — 완료율처럼 진행 중인 작업에 사용
**`<meter>`** — 온도, 점수처럼 특정 범위 내의 측정값에 사용

### 모달 팝업: `<dialog>`

```html
<button onclick="document.getElementById('myDialog').showModal()">
    팝업 열기
</button>

<dialog id="myDialog">
    <h2>공지사항</h2>
    <p>HTML 02장 학습을 완료했습니다!</p>
    <button onclick="document.getElementById('myDialog').close()">
        닫기
    </button>
</dialog>
```

**브라우저 결과:** "팝업 열기" 버튼을 클릭하면 화면 중앙에 대화상자가 나타납니다.

> `<dialog>`는 JavaScript를 최소한으로 사용합니다(`showModal()`, `close()`만). 순수 HTML에 가깝게 모달을 구현할 수 있습니다.

---

## 5️⃣ 실습: 회원가입 페이지 (시맨틱 구조)

시맨틱 태그로 구조를 잡고, 폼으로 사용자 입력을 받는 회원가입 페이지 전체 코드입니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>회원가입 - 코딩학교</title>
</head>
<body>

    <!-- 헤더: 로고 + 내비게이션 -->
    <header>
        <h1>코딩학교</h1>
        <nav>
            <ul>
                <li></li>
                <li></li>
                <li></li>
            </ul>
        </nav>
    </header>

    <!-- 메인: 핵심 콘텐츠 (회원가입 폼) -->
    <main>
        <section>
            <h2>회원가입</h2>
            <p>코딩학교와 함께 웹 개발을 시작해보세요!</p>

            <form action="#" method="post">

                <fieldset>
                    <legend>기본 정보</legend>

                    <p>
                        <label for="fullname">이름 <span>(필수)</span>:</label><br>
                        <input type="text" id="fullname" name="fullname"
                               placeholder="홍길동" required>
                    </p>

                    <p>
                        <label for="signup-email">이메일 <span>(필수)</span>:</label><br>
                        <input type="email" id="signup-email" name="email"
                               placeholder="example@email.com" required>
                    </p>

                    <p>
                        <label for="signup-pw">비밀번호 <span>(필수)</span>:</label><br>
                        <input type="password" id="signup-pw" name="password"
                               placeholder="8자 이상 입력" required>
                    </p>
                </fieldset>

                <fieldset>
                    <legend>추가 정보</legend>

                    <p>성별:</p>
                    <input type="radio" id="gender-m" name="gender" value="male">
                    <label for="gender-m">남성</label>
                    <input type="radio" id="gender-f" name="gender" value="female">
                    <label for="gender-f">여성</label>
                    <input type="radio" id="gender-n" name="gender" value="none">
                    <label for="gender-n">선택 안 함</label>

                    <p>
                        <label for="level">관심 분야:</label><br>
                        <select id="level" name="level">
                            <option value="">-- 선택하세요 --</option>
                            <option value="html">HTML/CSS</option>
                            <option value="js">JavaScript</option>
                            <option value="py">Python</option>
                            <option value="etc">기타</option>
                        </select>
                    </p>

                    <p>
                        <label for="self-intro">자기소개:</label><br>
                        <textarea id="self-intro" name="intro" rows="4" cols="40"
                                  placeholder="간단한 자기소개를 적어주세요"></textarea>
                    </p>
                </fieldset>

                <p>
                    <input type="checkbox" id="agree" name="agree" required>
                    <label for="agree">이용약관에 동의합니다 (필수)</label>
                </p>

                <button type="submit">가입하기</button>
                <button type="reset">초기화</button>

            </form>
        </section>
    </main>

    <!-- 푸터: 저작권 등 부가 정보 -->
    <footer>
        <p>&copy; 2025 코딩학교. All rights reserved.</p>
        <p>
             |
             |
            
        </p>
    </footer>

</body>
</html>
```

**구조 요약:**
- `<header>` — 사이트 이름 + 내비게이션 링크
- `<main>` → `<section>` — 회원가입 폼 (핵심 콘텐츠)
  - `<fieldset>` 두 개로 기본 정보 / 추가 정보 분리
- `<footer>` — 저작권, 약관 링크

---

## 6️⃣ 정리

### 폼 요소 요약

| 태그/속성 | 역할 | 예시 |
|-----------|------|------|
| `<form>` | 폼 영역 정의 | `<form action="..." method="post">` |
| `<input type="text">` | 텍스트 입력 | `<input type="text" name="name">` |
| `<input type="email">` | 이메일 입력 (형식 검증) | `<input type="email">` |
| `<input type="password">` | 비밀번호 입력 | `<input type="password">` |
| `<input type="checkbox">` | 다중 선택 체크박스 | `<input type="checkbox">` |
| `<input type="radio">` | 단일 선택 라디오 | `<input type="radio" name="g">` |
| `<select>` | 드롭다운 목록 | `<select><option>항목</option></select>` |
| `<textarea>` | 여러 줄 텍스트 | `<textarea rows="4"></textarea>` |
| `<fieldset>` | 입력 요소 그룹화 | `<fieldset><legend>제목</legend>…</fieldset>` |
| `<label>` | 입력 요소 설명 | `<label for="id">이름:</label>` |
| `<button type="submit">` | 폼 제출 버튼 | `<button type="submit">제출</button>` |
| `required` | 필수 입력 강제 | `<input required>` |
| `placeholder` | 빈칸 안내 문구 | `<input placeholder="입력하세요">` |

### 시맨틱 태그 요약

| 태그 | 역할 |
|------|------|
| `<header>` | 페이지 상단 영역 (로고, 내비게이션) |
| `<nav>` | 내비게이션 메뉴 |
| `<main>` | 핵심 콘텐츠 영역 (페이지당 하나) |
| `<section>` | 주제별 콘텐츠 구분 |
| `<article>` | 독립적 콘텐츠 (블로그 글, 기사) |
| `<aside>` | 부가 콘텐츠 (사이드바) |
| `<footer>` | 페이지 하단 영역 (저작권, 연락처) |
| `<details>` + `<summary>` | JS 없는 접이식 콘텐츠 |
| `<mark>` | 텍스트 하이라이트 |
| `<progress>` | 진행률 표시 바 |
| `<dialog>` | 모달 팝업 |

### 다음 장 미리보기

03장에서는 1~2장에서 배운 **모든 태그를 합쳐서** 하나의 완성된 포트폴리오 페이지를 만듭니다.

### 실습 과제

**기본** — 자신의 취미를 소개하는 폼 만들기
- 이름, 이메일, 취미(체크박스 3개 이상), 한줄 소개(textarea)
- `<fieldset>`으로 그룹화

**중급** — 시맨틱 태그로 블로그 레이아웃 만들기
- `<header>` + `<nav>` + `<main>` + `<aside>` + `<footer>` 구조
- `<main>` 안에 `<article>` 3개 (글 제목 + 내용 요약 + 링크)

**심화** — `<details>` + `<summary>`로 FAQ 페이지 만들기
- 질문 5개 이상을 접이식으로 구성
- 시맨틱 구조(`<header>`, `<main>`, `<section>`, `<footer>`) 적용
