---
nav_exclude: true
---
# 01장. HTML 시작하기

## 학습 목표

- HTML이 무엇이고 웹에서 어떤 역할을 하는지 설명할 수 있다
- 기본 HTML 문서를 작성하고 브라우저에서 확인할 수 있다

## 진행 순서

1. HTML이란? — 웹에서의 역할과 HTML·CSS·JS 비교
2. 첫 HTML 파일 만들기 — VSCode, Live Server, 기본 구조
3. 텍스트 태그 — 제목, 문단, 강조
4. 링크와 이미지 — `<a>`, `<img>`, alt 속성
5. 목록 — 순서 있는 목록, 순서 없는 목록, 중첩
6. 실습: 나의 첫 웹페이지 완성 — 배운 태그 전부 활용
7. 정리 — 태그 요약 표, 다음 장 미리보기, 실습 과제

---

## 1️⃣ HTML이란?

**HTML**(HyperText Markup Language)은 웹페이지의 **구조와 내용**을 정의하는 마크업 언어입니다.

### 건물 설계도 비유

> HTML은 "여기에 제목, 여기에 문단, 여기에 이미지"처럼 웹페이지의 구조를 정하는 **건물 설계도**입니다.
> CSS가 외관 디자인을 담당하고, JavaScript가 엘리베이터·자동문처럼 움직임을 담당한다면,
> **HTML은 그 건물이 어디에 무엇이 있는지 뼈대를 잡아줍니다.**

### HTML의 핵심 개념

- **HyperText** — 링크(`<a>`)를 통해 다른 페이지로 이동할 수 있는 텍스트
- **Markup** — `<태그>`로 텍스트에 의미와 역할을 부여하는 방식
- **Language** — 브라우저(Chrome, Safari 등)가 읽고 해석하는 언어

### HTML · CSS · JavaScript 역할 비교

| 기술 | 역할 | 비유 |
|------|------|------|
| **HTML** | 웹페이지의 구조와 내용 | 건물의 뼈대 |
| CSS | 색상, 폰트, 레이아웃 등 시각적 스타일 | 건물의 외관 디자인 |
| JavaScript | 버튼 클릭, 데이터 처리, 애니메이션 등 동작 | 엘리베이터, 자동문, 조명 센서 |

> 이 세 가지는 함께 동작합니다. 이번 장에서는 HTML 뼈대를 탄탄히 잡습니다.

---

## 2️⃣ 첫 HTML 파일 만들기

### 작업 환경 준비

1. **VSCode** 실행 후 `html` 폴더 생성
2. 폴더 안에 `index.html` 파일 생성
3. VSCode 확장 프로그램 **Live Server** 설치 (처음 한 번만)
4. `index.html`에서 우클릭 → **"Open with Live Server"** 클릭
5. 브라우저가 자동으로 열리며, 파일을 저장할 때마다 브라우저가 새로고침됩니다

### Emmet 단축키로 기본 구조 자동 생성

VSCode에서 `index.html`을 열고 `!`를 입력한 뒤 `Tab`을 누르면 아래 구조가 자동으로 생성됩니다.

### HTML 기본 구조

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>나의 첫 웹페이지</title>
</head>
<body>
    <h1>안녕하세요!</h1>
    <p>나의 첫 번째 웹페이지입니다.</p>
</body>
</html>
```

### 각 줄 설명

| 코드 | 역할 |
|------|------|
| `<!DOCTYPE html>` | "이 파일은 HTML5 문서입니다"라고 브라우저에 알려줌 |
| `<html lang="ko">` | HTML 문서의 시작. `lang="ko"`는 한국어 페이지임을 표시 |
| `<head>` | **보이지 않는 메타 정보** — 문자셋, 뷰포트, 제목 등 |
| `<meta charset="UTF-8">` | 한글이 깨지지 않도록 UTF-8 인코딩 지정 |
| `<meta name="viewport" ...>` | 모바일에서 화면 크기를 올바르게 조정 |
| `<title>` | 브라우저 탭에 표시되는 제목 |
| `</head>` | head 영역 끝 |
| `<body>` | **눈에 보이는 내용** — 제목, 문단, 이미지 등이 모두 여기에 |
| `</body>` | body 영역 끝 |
| `</html>` | HTML 문서 끝 |

> **비유**: `<head>`는 책의 표지 뒤 저작권 페이지(독자 눈에 안 보이지만 중요한 정보),
> `<body>`는 책의 본문(독자가 실제로 읽는 내용)입니다.

---

## 3️⃣ 텍스트 태그

### 제목 태그: `<h1>` ~ `<h6>`

`h`는 Heading(제목)의 약자입니다. 숫자가 작을수록 글자가 크고 중요합니다.

```html
<h1>가장 큰 제목 (페이지 제목)</h1>
<h2>두 번째 제목 (대단원)</h2>
<h3>세 번째 제목 (소단원)</h3>
<h4>네 번째 제목</h4>
<h5>다섯 번째 제목</h5>
<h6>가장 작은 제목</h6>
```

> 💡 **Emmet 팁**: `h1` 입력 후 `Tab` → `<h1></h1>` 자동 생성. `h2`, `h3`도 동일

**브라우저 결과:**
- h1: 가장 굵고 크게 표시
- h2 ~ h6: 순서대로 작아짐
- 보통 페이지당 `<h1>`은 하나만 사용 (SEO와 접근성에 유리)

### 문단 태그: `<p>`

`p`는 Paragraph(문단)의 약자입니다. 앞뒤에 자동으로 여백이 생깁니다.

```html
<p>첫 번째 문단입니다. 긴 텍스트도 자동으로 줄바꿈됩니다.</p>
<p>두 번째 문단입니다. 문단 사이에는 자동으로 간격이 생깁니다.</p>
```

> 💡 **Emmet 팁**: `p` 입력 후 `Tab` → `<p></p>` 자동 생성. `p*3`으로 3개 한번에 생성 가능

### 줄바꿈과 수평선

```html
<p>첫 번째 줄<br>두 번째 줄 (강제 줄바꿈)</p>
<hr>
<!-- hr은 시각적 구분선 (Horizontal Rule) -->
<p>구분선 아래 내용</p>
```

> `<br>`과 `<hr>`은 닫는 태그가 없는 **빈 요소(void element)**입니다.

### 강조 태그

```html
<p>이 부분은 <strong>매우 중요합니다</strong> (굵게 표시).</p>
<p>이 부분은 <em>기울임체로 강조</em>됩니다 (Emphasis).</p>
<p><strong>굵게</strong>와 <em>기울임</em>을 <strong><em>함께</em></strong> 쓸 수 있습니다.</p>
```

> 💡 **Emmet 팁**: `p>strong` + `Tab` → `<p><strong></strong></p>` 자동 생성

**브라우저 결과:**
- `<strong>` → **굵은 글씨** (의미: 중요한 내용)
- `<em>` → *기울임꼴* (의미: 강조)

> `<b>` (굵게), `<i>` (기울임)도 있지만, **의미 없이 스타일만** 바꿉니다.
> 의미 있는 강조에는 `<strong>`, `<em>`을 권장합니다.

---

## 4️⃣ 링크와 이미지

### 링크: `<a>`

`a`는 Anchor(닻)의 약자입니다. `href` 속성(attribute)에 이동할 주소를 씁니다.

```html
<!-- 기본 링크 -->
<a href="https://www.google.com">구글로 이동</a>

<!-- 새 탭에서 열기 -->
<a href="https://www.naver.com" target="_blank">네이버 (새 탭)</a>

<!-- 같은 페이지 내 이동 -->

<!-- 다른 HTML 파일로 이동 -->
<a href="about.html">소개 페이지</a>
```

> 💡 **Emmet 팁**: `a` + `Tab` → `<a href=""></a>` 자동 생성. `a[target=_blank]` + `Tab`으로 새 탭 링크도 가능

> **비유**: `<a>` 태그는 다른 페이지로 가는 **문**입니다.
> `href`는 그 문이 어디로 연결되는지 알려주는 **주소판**이고,
> `target="_blank"`는 **새 방(탭)으로 들어가는 문**입니다.

### 이미지: `<img>`

```html
<!-- 인터넷 이미지 -->
<img src="https://via.placeholder.com/300x200" alt="300x200 플레이스홀더 이미지">

<!-- 로컬 이미지 (같은 폴더에 cat.jpg가 있을 때) -->
<img src="cat.jpg" alt="귀여운 고양이 사진">

<!-- 크기 지정 -->
<img src="logo.png" alt="회사 로고" width="200" height="100">
```

> 💡 **Emmet 팁**: `img` + `Tab` → `<img src="" alt="">` 자동 생성. src와 alt 사이를 `Tab`으로 이동

**`alt` 속성이 중요한 이유:**

| 상황 | alt 없을 때 | alt 있을 때 |
|------|-------------|-------------|
| 이미지 로딩 실패 | 빈 공간 또는 깨진 아이콘 | "귀여운 고양이 사진" 텍스트 표시 |
| 시각 장애인 스크린 리더 | 내용 파악 불가 | alt 텍스트를 음성으로 읽어줌 |
| 검색엔진(SEO) | 이미지 내용 파악 불가 | 이미지 내용을 인식하여 검색 노출 향상 |

> **비유**: `<img>`는 벽에 사진을 거는 것이고,
> `alt`는 사진 밑에 붙이는 **캡션(설명문)**입니다. 캡션이 있으면 모두가 이해할 수 있습니다.

### 실습: 링크 + 이미지 함께 쓰기

```html
<!-- 이미지를 클릭하면 링크로 이동 -->
<a href="https://www.google.com" target="_blank">
    <img src="https://via.placeholder.com/150" alt="구글로 이동">
</a>
```

---

## 5️⃣ 목록

### 순서 없는 목록: `<ul>` + `<li>`

`ul`은 Unordered List, `li`는 List Item의 약자입니다. 각 항목 앞에 점(•)이 붙습니다.

```html
<h2>좋아하는 음식</h2>
<ul>
    <li>삼겹살</li>
    <li>파스타</li>
    <li>초밥</li>
</ul>
```

> 💡 **Emmet 팁**: `ul>li*3` + `Tab` → `<ul>` 안에 `<li>` 3개 자동 생성

**브라우저 결과:**
- • 삼겹살
- • 파스타
- • 초밥

### 순서 있는 목록: `<ol>` + `<li>`

`ol`은 Ordered List의 약자입니다. 각 항목 앞에 번호(1, 2, 3...)가 붙습니다.

```html
<h2>오늘 할 일</h2>
<ol>
    <li>HTML 공부하기</li>
    <li>실습 과제 완성하기</li>
    <li>커피 마시기</li>
</ol>
```

> 💡 **Emmet 팁**: `ol>li*3` + `Tab` → 순서 있는 목록도 동일하게 생성

**브라우저 결과:**
1. HTML 공부하기
2. 실습 과제 완성하기
3. 커피 마시기

### 중첩 목록

목록 안에 목록을 넣을 수 있습니다.

```html
<ul>
    <li>프론트엔드
        <ul>
            <li>HTML</li>
            <li>CSS</li>
            <li>JavaScript</li>
        </ul>
    </li>
    <li>백엔드
        <ul>
            <li>Python</li>
            <li>Java</li>
        </ul>
    </li>
</ul>
```

> 💡 **Emmet 팁**: `ul>li*2>ul>li*3` + `Tab` → 중첩 목록도 한 줄로 생성 가능

**브라우저 결과:**
- 프론트엔드
  - HTML
  - CSS
  - JavaScript
- 백엔드
  - Python
  - Java

---

## 6️⃣ 실습: 나의 첫 웹페이지 완성

지금까지 배운 태그를 모두 활용하여 자기소개 페이지를 만들어봅니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>나를 소개합니다</title>
</head>
<body>

    <h1>안녕하세요, 저는 김코딩입니다!</h1>
    <hr>

    <h2>자기소개</h2>
    <p>
        저는 웹 개발을 공부하고 있는 <strong>김코딩</strong>입니다.
        HTML부터 차근차근 배우고 있으며, <em>언젠가는 멋진 웹사이트를 만드는 것</em>이 목표입니다.
    </p>

    <h2>취미 목록</h2>
    <ul>
        <li>코딩</li>
        <li>독서
            <ul>
                <li>소설</li>
                <li>기술 서적</li>
            </ul>
        </li>
        <li>산책</li>
    </ul>

    <h2>좋아하는 사이트</h2>
    <ol>
        <li><a href="https://developer.mozilla.org" target="_blank">MDN Web Docs</a> - HTML 공식 문서</li>
        <li><a href="https://www.youtube.com" target="_blank">YouTube</a> - 학습 영상</li>
        <li><a href="https://github.com" target="_blank">GitHub</a> - 코드 저장소</li>
    </ol>

    <h2>프로필 이미지</h2>
    <img src="https://via.placeholder.com/200x200" alt="김코딩의 프로필 사진">

    <hr>
    <p><em>이 페이지는 HTML만으로 만들어졌습니다. CSS를 배우면 더 예쁘게 꾸밀 수 있어요!</em></p>

</body>
</html>
```

**브라우저에서 확인하면:**
- 큰 제목으로 이름이 표시됩니다
- 구분선 아래 자기소개 문단이 나옵니다
- 취미는 중첩 목록(점)으로, 좋아하는 사이트는 번호 목록으로 표시됩니다
- 링크를 클릭하면 새 탭에서 해당 사이트가 열립니다
- 플레이스홀더 이미지가 표시됩니다

---

## 7️⃣ 정리

### 01장에서 배운 태그 요약

| 태그 | 역할 | Emmet 단축키 |
|------|------|-------------|
| `<h1>` ~ `<h6>` | 제목 (크기 순) | `h1` + Tab |
| `<p>` | 문단 | `p` + Tab |
| `<br>` | 강제 줄바꿈 | `br` + Tab |
| `<hr>` | 수평 구분선 | `hr` + Tab |
| `<strong>` | 굵게 강조 | `strong` + Tab |
| `<em>` | 기울임 강조 | `em` + Tab |
| `<a>` | 링크 | `a` + Tab |
| `<img>` | 이미지 | `img` + Tab |
| `<ul>` + `<li>` | 순서 없는 목록 | `ul>li*3` + Tab |
| `<ol>` + `<li>` | 순서 있는 목록 | `ol>li*3` + Tab |

### 다음 장 미리보기

다음 장(02장)에서는 아래 내용을 배웁니다:
- **폼(Form)** — 사용자 입력을 받는 로그인·회원가입 페이지 만들기
- **시맨틱 태그** — `<header>`, `<nav>`, `<main>`, `<footer>` 등으로 구조화된 HTML 작성

### 실습 과제

**기본** — 자기소개 페이지 만들기
- 이름, 나이, 사는 곳을 제목과 문단으로 작성
- 취미를 `<ul>`로, 좋아하는 음식 순위를 `<ol>`로 작성

**중급** — 좋아하는 영화·음악 3개를 목록 + 링크 + 이미지로 소개
- 각 항목에 이미지(`<img>`)와 공식 사이트 링크(`<a>`) 추가
- `<strong>`으로 제목 강조

**심화** — 두 번째 HTML 파일 만들고 첫 페이지에서 링크로 연결
- `about.html` 파일을 새로 만들어 "저에 대해 더 알아보기" 내용 작성
- `index.html`에서 `<a href="about.html">소개 더보기</a>` 링크 추가
- `about.html`에서 다시 `index.html`로 돌아오는 링크도 추가
