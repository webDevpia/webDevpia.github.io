---
title: 03. HTML 미니 프로젝트
layout: default
grand_parent: Language
parent: HTML
nav_order: 3
permalink: /language/html/mini-project
---

## 학습 목표

- 1~2장에서 배운 모든 태그를 활용하여 완성도 있는 웹페이지를 만들 수 있다

<a id="toc"></a>

## 진행 순서

1. [프로젝트 소개](#part1) — 완성 화면 미리보기, 개념 매핑
2. [페이지 구조 설계](#part2) — 시맨틱 뼈대 잡기
3. [섹션별 구현](#part3) — 단계별 코드 작성
4. [전체 코드](#part4) — 복사해서 바로 실행 가능한 완성본
5. [정리](#part5) — 전체 태그 요약, CSS로 넘어가기

---

# 03장. HTML 미니 프로젝트

<a id="part1"></a>

## 1️⃣ 프로젝트 소개 [↑](#toc)

### 나만의 포트폴리오 페이지 (CSS 없이 HTML 구조만)

이번 프로젝트의 목표는 **CSS 없이 HTML 태그만으로** 자신을 소개하는 포트폴리오 페이지를 완성하는 것입니다. 지금은 스타일이 없어 투박하게 보이지만, 이 HTML 구조가 CSS를 배우면 멋진 페이지로 변신하는 **뼈대**가 됩니다.

### 완성 화면 미리보기 (ASCII 다이어그램)

```
+--------------------------------------------------+
| [나의 포트폴리오]  홈 | 소개 | 기술 | 프로젝트 | 연락 |
+--------------------------------------------------+
|                                                  |
|  안녕하세요, 저는 김코딩입니다!                     |
|  웹 개발을 공부하고 있습니다.                       |
|  [사진]                                           |
|                                                  |
+------ 소개 ----------------------------------------+
|  저는 HTML부터 차근차근 배우는 중입니다...            |
|                                                  |
+------ 기술 스택 ------------------------------------+
|  • HTML   • CSS   • JavaScript                   |
|                                                  |
+------ 프로젝트 -------------------------------------+
|  [이미지] 자기소개 페이지       → 보러가기           |
|  [이미지] 회원가입 폼            → 보러가기           |
|                                                  |
+------ 연락처 ---------------------------------------+
|  이름: [         ]   이메일: [              ]     |
|  메시지: [                              ]        |
|  [보내기]                                         |
|                                                  |
+--------------------------------------------------+
|  © 2025 김코딩 포트폴리오. All rights reserved.   |
+--------------------------------------------------+
```

### 1~2장 개념 매핑표

| 페이지 영역 | 사용하는 태그 | 배운 장 |
|-------------|---------------|---------|
| 헤더 + 내비게이션 | `<header>`, `<nav>`, `<ul>`, `<li>`, `<a>` | 01장 + 02장 |
| 자기소개 섹션 | `<section>`, `<h2>`, `<p>`, `<strong>`, `<em>`, `<img>` | 01장 |
| 기술 스택 섹션 | `<section>`, `<ul>`, `<li>` | 01장 |
| 프로젝트 섹션 | `<section>`, `<article>`, `<img>`, `<a>` | 01장 + 02장 |
| 연락처 폼 | `<section>`, `<form>`, `<input>`, `<textarea>`, `<button>` | 02장 |
| 푸터 | `<footer>`, `<p>` | 02장 |

---

<a id="part2"></a>

## 2️⃣ 페이지 구조 설계 [↑](#toc)

시맨틱 태그로 뼈대를 먼저 잡습니다. 빈 뼈대를 만들고 섹션별로 내용을 채워나가는 방식입니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>김코딩 포트폴리오</title>
</head>
<body>

    <!-- 1. 헤더: 이름 + 내비게이션 -->
    <header>
        <!-- 여기에 내용 -->
    </header>

    <!-- 2. 메인 콘텐츠 -->
    <main>

        <!-- 2-1. 자기소개 -->
        <section id="about">
            <!-- 여기에 내용 -->
        </section>

        <!-- 2-2. 기술 스택 -->
        <section id="skills">
            <!-- 여기에 내용 -->
        </section>

        <!-- 2-3. 프로젝트 -->
        <section id="projects">
            <!-- 여기에 내용 -->
        </section>

        <!-- 2-4. 연락처 폼 -->
        <section id="contact">
            <!-- 여기에 내용 -->
        </section>

    </main>

    <!-- 3. 푸터 -->
    <footer>
        <!-- 여기에 내용 -->
    </footer>

</body>
</html>
```

> 구조를 먼저 잡고 내용을 채우는 이 방식을 **"뼈대 우선(Structure First)"** 접근이라고 합니다. 큰 프로젝트에서도 이 순서를 지키면 복잡도가 줄어듭니다.

---

<a id="part3"></a>

## 3️⃣ 섹션별 구현 [↑](#toc)

### Step 1. 헤더 + 내비게이션

```html
<header>
    <h1>나의 포트폴리오</h1>
    <nav>
        <ul>
            <li><a href="#about">소개</a></li>
            <li><a href="#skills">기술</a></li>
            <li><a href="#projects">프로젝트</a></li>
            <li><a href="#contact">연락처</a></li>
        </ul>
    </nav>
</header>
```

**포인트:**
- `href="#about"`처럼 `#`으로 시작하면 같은 페이지 내 해당 `id`로 이동합니다
- `<nav>` 안의 링크 목록은 `<ul>` + `<li>`로 감싸는 것이 시맨틱하게 올바릅니다

### Step 2. 자기소개 섹션

```html
<section id="about">
    <h2>안녕하세요!</h2>
    <p>
        저는 <strong>웹 개발</strong>을 공부하고 있는 <strong>김코딩</strong>입니다.<br>
        <em>언젠가는 멋진 웹사이트를 만드는 것</em>이 목표입니다.
    </p>
    <img src="https://via.placeholder.com/150x150" alt="김코딩 프로필 사진">
</section>
```

### Step 3. 기술 스택 섹션

```html
<section id="skills">
    <h2>기술 스택</h2>
    <ul>
        <li>HTML — 웹페이지 구조</li>
        <li>CSS — 스타일 및 레이아웃 (학습 중)</li>
        <li>JavaScript — 인터랙션 (예정)</li>
    </ul>
    <details>
        <summary>더 배우고 싶은 기술</summary>
        <ul>
            <li>React</li>
            <li>Node.js</li>
            <li>Python</li>
        </ul>
    </details>
</section>
```

**포인트:** `<details>` + `<summary>`를 활용해 클릭 전까지는 숨겨두는 콘텐츠를 구현합니다.

### Step 4. 프로젝트 섹션

```html
<section id="projects">
    <h2>프로젝트</h2>

    <article>
        <h3>자기소개 페이지</h3>
        <img src="https://via.placeholder.com/200x120" alt="자기소개 페이지 스크린샷">
        <p>HTML 01장에서 만든 자기소개 페이지입니다. 제목, 목록, 링크, 이미지를 활용했습니다.</p>
        <p><a href="index.html" target="_blank">페이지 보기</a></p>
    </article>

    <hr>

    <article>
        <h3>회원가입 폼</h3>
        <img src="https://via.placeholder.com/200x120" alt="회원가입 폼 스크린샷">
        <p>HTML 02장에서 만든 회원가입 폼입니다. 시맨틱 태그와 다양한 input 타입을 활용했습니다.</p>
        <p><a href="signup.html" target="_blank">페이지 보기</a></p>
    </article>
</section>
```

**포인트:**
- 각 프로젝트는 `<article>` 태그로 감쌉니다 (독립적으로 의미 있는 콘텐츠)
- `<hr>`로 프로젝트 사이에 구분선을 넣습니다

### Step 5. 연락처 폼 섹션

```html
<section id="contact">
    <h2>연락처</h2>
    <p>궁금한 점이 있으시면 아래 폼으로 메시지를 보내주세요.</p>

    <form action="#" method="post">
        <p>
            <label for="contact-name">이름:</label><br>
            <input type="text" id="contact-name" name="name"
                   placeholder="홍길동" required>
        </p>
        <p>
            <label for="contact-email">이메일:</label><br>
            <input type="email" id="contact-email" name="email"
                   placeholder="example@email.com" required>
        </p>
        <p>
            <label for="message">메시지:</label><br>
            <textarea id="message" name="message" rows="5" cols="40"
                      placeholder="메시지를 입력하세요" required></textarea>
        </p>
        <button type="submit">보내기</button>
    </form>
</section>
```

### Step 6. 푸터

```html
<footer>
    <p>&copy; 2025 김코딩 포트폴리오. All rights reserved.</p>
    <p>
        <a href="https://github.com" target="_blank">GitHub</a> |
        <a href="mailto:kimcoding@example.com">이메일</a>
    </p>
</footer>
```

**포인트:** `mailto:` 링크는 클릭 시 기본 이메일 앱이 열립니다.

---

<a id="part4"></a>

## 4️⃣ 전체 코드 [↑](#toc)

아래 코드를 `portfolio.html`로 저장하고 브라우저에서 바로 확인할 수 있습니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>김코딩 포트폴리오</title>
</head>
<body>

    <!-- 헤더 -->
    <header>
        <h1>나의 포트폴리오</h1>
        <nav>
            <ul>
                <li><a href="#about">소개</a></li>
                <li><a href="#skills">기술</a></li>
                <li><a href="#projects">프로젝트</a></li>
                <li><a href="#contact">연락처</a></li>
            </ul>
        </nav>
    </header>

    <main>

        <!-- 자기소개 -->
        <section id="about">
            <h2>안녕하세요!</h2>
            <p>
                저는 <strong>웹 개발</strong>을 공부하고 있는 <strong>김코딩</strong>입니다.<br>
                <em>언젠가는 멋진 웹사이트를 만드는 것</em>이 목표입니다.
            </p>
            <img src="https://via.placeholder.com/150x150" alt="김코딩 프로필 사진">
        </section>

        <hr>

        <!-- 기술 스택 -->
        <section id="skills">
            <h2>기술 스택</h2>
            <ul>
                <li>HTML — 웹페이지 구조</li>
                <li>CSS — 스타일 및 레이아웃 (학습 중)</li>
                <li>JavaScript — 인터랙션 (예정)</li>
            </ul>
            <details>
                <summary>더 배우고 싶은 기술</summary>
                <ul>
                    <li>React</li>
                    <li>Node.js</li>
                    <li>Python</li>
                </ul>
            </details>
        </section>

        <hr>

        <!-- 프로젝트 -->
        <section id="projects">
            <h2>프로젝트</h2>

            <article>
                <h3>자기소개 페이지</h3>
                <img src="https://via.placeholder.com/200x120" alt="자기소개 페이지 스크린샷">
                <p>HTML 01장에서 만든 자기소개 페이지입니다. 제목, 목록, 링크, 이미지를 활용했습니다.</p>
                <p><a href="index.html">페이지 보기</a></p>
            </article>

            <hr>

            <article>
                <h3>회원가입 폼</h3>
                <img src="https://via.placeholder.com/200x120" alt="회원가입 폼 스크린샷">
                <p>HTML 02장에서 만든 회원가입 폼입니다. 시맨틱 태그와 다양한 input 타입을 활용했습니다.</p>
                <p><a href="signup.html">페이지 보기</a></p>
            </article>
        </section>

        <hr>

        <!-- 연락처 폼 -->
        <section id="contact">
            <h2>연락처</h2>
            <p>궁금한 점이 있으시면 아래 폼으로 메시지를 보내주세요.</p>

            <form action="#" method="post">
                <p>
                    <label for="contact-name">이름:</label><br>
                    <input type="text" id="contact-name" name="name"
                           placeholder="홍길동" required>
                </p>
                <p>
                    <label for="contact-email">이메일:</label><br>
                    <input type="email" id="contact-email" name="email"
                           placeholder="example@email.com" required>
                </p>
                <p>
                    <label for="message">메시지:</label><br>
                    <textarea id="message" name="message" rows="5" cols="40"
                              placeholder="메시지를 입력하세요" required></textarea>
                </p>
                <button type="submit">보내기</button>
            </form>
        </section>

    </main>

    <!-- 푸터 -->
    <footer>
        <hr>
        <p>&copy; 2025 김코딩 포트폴리오. All rights reserved.</p>
        <p>
            <a href="https://github.com" target="_blank">GitHub</a> |
            <a href="mailto:kimcoding@example.com">이메일</a>
        </p>
    </footer>

</body>
</html>
```

---

<a id="part5"></a>

## 5️⃣ 정리 [↑](#toc)

### HTML 전체 태그 총정리

| 분류 | 태그 | 역할 |
|------|------|------|
| **문서 구조** | `<!DOCTYPE html>` | HTML5 문서 선언 |
| | `<html>`, `<head>`, `<body>` | 문서 기본 구조 |
| | `<meta>`, `<title>` | 메타 정보, 제목 |
| **텍스트** | `<h1>` ~ `<h6>` | 제목 (크기 순) |
| | `<p>` | 문단 |
| | `<br>` | 강제 줄바꿈 |
| | `<hr>` | 수평 구분선 |
| | `<strong>`, `<em>` | 굵게, 기울임 강조 |
| | `<mark>` | 텍스트 하이라이트 |
| **링크/미디어** | `<a>` | 링크 |
| | `<img>` | 이미지 |
| **목록** | `<ul>`, `<ol>`, `<li>` | 순서없는/있는 목록 |
| **폼** | `<form>`, `<input>`, `<label>` | 폼 기본 구조 |
| | `<select>`, `<option>` | 드롭다운 |
| | `<textarea>` | 여러 줄 텍스트 |
| | `<fieldset>`, `<legend>` | 폼 그룹화 |
| | `<button>` | 버튼 |
| **시맨틱** | `<header>`, `<nav>` | 헤더, 내비게이션 |
| | `<main>`, `<section>` | 메인, 섹션 |
| | `<article>`, `<aside>` | 독립 콘텐츠, 사이드바 |
| | `<footer>` | 푸터 |
| **유틸리티** | `<details>`, `<summary>` | 접이식 콘텐츠 |
| | `<progress>`, `<meter>` | 진행/측정 바 |
| | `<dialog>` | 모달 팝업 |
| | `<div>`, `<span>` | 비시맨틱 묶음 (스타일 용) |

### CSS로 넘어가기

> 지금은 투박한 모습이지만, **CSS를 배우면 이 페이지가 깔끔하게 변신합니다!**
>
> - 지금: 흑백, 기본 폰트, 정렬 없음
> - CSS 배운 후: 컬러 테마, 예쁜 폰트, 카드 레이아웃, 반응형 디자인

HTML이 "무엇이 있는가"를 정의했다면, CSS는 "어떻게 보이는가"를 정의합니다.
이 포트폴리오 HTML 구조를 그대로 유지하면서 CSS만 추가하면 됩니다.

### 실습 과제

**기본** — 전체 코드를 그대로 실행하고, 이름/소개/프로젝트 내용을 자신의 것으로 교체하기

**중급** — 프로젝트 섹션에 항목 하나 더 추가하기
- 실제 자신이 만든 HTML 파일(01장, 02장 실습)을 프로젝트로 소개
- `<article>` 구조 그대로 복사하여 내용만 변경

**심화** — 포트폴리오를 여러 파일로 분리하기
- `portfolio.html` — 메인 포트폴리오
- `about.html` — 자기소개 상세
- `projects.html` — 프로젝트 목록
- 각 파일에서 서로 링크로 연결 (`<a href="about.html">`)
- 모든 파일에 동일한 `<header>` + `<nav>` + `<footer>` 구조 적용
