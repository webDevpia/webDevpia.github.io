---
title: 03. CSS 반응형 디자인
layout: default
grand_parent: Language
parent: CSS
nav_order: 3
permalink: /language/css/responsive
---

# 03장. CSS 반응형 디자인

## 학습 목표

- 미디어 쿼리로 화면 크기에 따라 다른 스타일을 적용할 수 있다
- 모바일 퍼스트 접근법으로 반응형 웹페이지를 만들 수 있다

<a id="toc"></a>

## 진행 순서

1. [반응형 디자인이란?](#part1) - 개념과 viewport 설정
2. [미디어 쿼리 기초](#part2) - @media 문법과 브레이크포인트
3. [모바일 퍼스트](#part3) - min-width vs max-width 접근법
4. [반응형 유닛](#part4) - px, %, rem, vw/vh
5. [실용 예제: 반응형 포트폴리오](#part5) - 전체 코드 구현
6. [정리](#part6) - 체크리스트, Tailwind 연결 안내, 실습 과제

---

<a id="part1"></a>

## 1️⃣ 반응형 디자인이란? [↑](#toc)

**반응형 웹 디자인(Responsive Web Design)**은 화면 크기에 따라 레이아웃과 스타일이 유연하게 변하는 웹 디자인 방식입니다.

### 접이식 가구 비유

> **접이식 가구**를 생각해 보세요.
> - 넓은 거실에서는 소파로, 좁은 방에서는 침대로 변하는 가구처럼
> - 웹페이지도 **데스크톱에서는 3열 카드**, **스마트폰에서는 1열**로 자동 변합니다.

### 왜 필요한가?

2024년 기준으로 전 세계 웹 트래픽의 약 60% 이상이 모바일에서 발생합니다. 하나의 웹사이트가 스마트폰, 태블릿, 데스크톱 등 모든 화면에서 잘 보여야 합니다.

| 기기 | 화면 너비 | 특징 |
|------|-----------|------|
| 스마트폰 | ~480px | 세로로 길고 좁음 |
| 태블릿 | 481px~1024px | 가로 세로 전환 가능 |
| 데스크톱 | 1025px~ | 넓은 화면 |
| 와이드 모니터 | 1440px~ | 매우 넓은 화면 |

### viewport 메타 태그

모바일 브라우저는 기본적으로 데스크톱 크기(약 980px)로 페이지를 렌더링한 뒤 축소합니다. 이를 방지하기 위해 모든 HTML 파일의 `<head>`에 다음 태그를 반드시 추가해야 합니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <!-- 반응형 웹의 필수 설정 -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>반응형 웹</title>
</head>
```

- `width=device-width`: 뷰포트(viewport, 실제 화면 영역)를 기기의 실제 너비로 설정
- `initial-scale=1.0`: 초기 확대/축소 비율을 1배(원본 크기)로 설정

---

<a id="part2"></a>

## 2️⃣ 미디어 쿼리 기초 [↑](#toc)

**미디어 쿼리(Media Query)**는 특정 조건(화면 너비, 방향 등)이 충족될 때만 적용되는 CSS 규칙을 작성하는 문법입니다.

### 기본 문법

```css
/* 기본 스타일 */
.cards {
  display: flex;
  gap: 24px;
}

/* 화면 너비가 768px 이하일 때 (태블릿/모바일) */
@media (max-width: 768px) {
  .cards {
    flex-direction: column; /* 가로 → 세로 배치로 변경 */
  }
}

/* 화면 너비가 480px 이하일 때 (스마트폰) */
@media (max-width: 480px) {
  body {
    font-size: 14px; /* 작은 화면에서 글자 크기 줄이기 */
  }
}
```

### @media 문법 설명

```css
@media (조건) {
  /* 조건이 참일 때만 적용되는 CSS */
}

/* 자주 쓰는 조건들 */
@media (max-width: 768px)   { /* 768px 이하 */ }
@media (min-width: 769px)   { /* 769px 이상 */ }
@media (orientation: portrait)  { /* 세로 방향 */ }
@media (orientation: landscape) { /* 가로 방향 */ }
```

### 주요 브레이크포인트(Breakpoint)

**브레이크포인트**는 레이아웃이 변하는 기준 너비입니다.

| 이름 | 너비 | 대상 기기 |
|------|------|-----------|
| 스마트폰 | ~480px | 모바일 |
| 태블릿 | 481px~768px | 소형 태블릿 |
| 태블릿 가로 | 769px~1024px | 대형 태블릿, 소형 노트북 |
| 데스크톱 | 1025px~1440px | 노트북, 데스크톱 |
| 와이드 | 1441px~ | 대형 모니터 |

> 실무에서는 프레임워크나 팀 컨벤션에 따라 브레이크포인트가 달라집니다. Tailwind CSS는 `sm(640px)`, `md(768px)`, `lg(1024px)`, `xl(1280px)` 등을 사용합니다.

### 실습: 카드가 데스크톱은 3열, 모바일은 1열

```html
<div class="cards">
  <div class="card">카드 1</div>
  <div class="card">카드 2</div>
  <div class="card">카드 3</div>
</div>
```

```css
* { box-sizing: border-box; }

/* 기본(데스크톱): 3열 */
.cards {
  display: flex;
  gap: 20px;
}

.card {
  flex: 1;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
}

/* 태블릿 이하: 2열 */
@media (max-width: 768px) {
  .card {
    flex: 0 0 calc(50% - 10px);
  }
}

/* 모바일: 1열 */
@media (max-width: 480px) {
  .cards {
    flex-direction: column;
  }
  .card {
    flex: none;
  }
}
```

---

<a id="part3"></a>

## 3️⃣ 모바일 퍼스트 [↑](#toc)

### 작은 방에서 큰 방으로 비유

> **작은 방을 꾸민 다음 큰 방으로 확장하는 것**이,
> 큰 방에서 시작해서 작은 방에 맞게 줄이는 것보다 쉽습니다.
>
> 모바일 퍼스트도 마찬가지입니다 — 모바일에서 시작해 큰 화면으로 확장합니다.

### max-width (데스크톱 퍼스트) vs min-width (모바일 퍼스트)

**데스크톱 퍼스트** — 데스크톱 기준으로 작성 후, `max-width`로 줄여나감

```css
/* 기본: 데스크톱 스타일 */
.container { display: flex; }

/* 768px 이하일 때 변경 */
@media (max-width: 768px) {
  .container { flex-direction: column; }
}

/* 480px 이하일 때 추가 변경 */
@media (max-width: 480px) {
  .container { padding: 10px; }
}
```

**모바일 퍼스트** — 모바일 기준으로 작성 후, `min-width`로 확장

```css
/* 기본: 모바일 스타일 */
.container { padding: 10px; }

/* 481px 이상(태블릿)일 때 확장 */
@media (min-width: 481px) {
  .container { padding: 20px; }
}

/* 769px 이상(데스크톱)일 때 확장 */
@media (min-width: 769px) {
  .container {
    display: flex;
    padding: 40px;
  }
}
```

### 실무 권장: 모바일 퍼스트

| 방식 | 장점 | 단점 |
|------|------|------|
| 데스크톱 퍼스트 | 기존 방식에 익숙함 | 모바일 최적화가 뒤늦게 됨 |
| **모바일 퍼스트** | **성능 우수, 점진적 향상** | **새로운 사고방식 필요** |

모바일 퍼스트가 권장되는 이유:
1. **성능**: 모바일에서 불필요한 CSS를 로드하지 않음
2. **점진적 향상(Progressive Enhancement)**: 핵심 내용을 먼저 확보, 이후 기능 추가
3. **트렌드**: Tailwind CSS, Bootstrap 5 모두 모바일 퍼스트 방식을 사용

---

<a id="part4"></a>

## 4️⃣ 반응형 유닛 [↑](#toc)

고정 픽셀(px) 대신 상대적인 단위를 사용하면 다양한 화면 크기에 유연하게 대응할 수 있습니다.

### 단위 비교

| 단위 | 기준 | 예시 | 특징 |
|------|------|------|------|
| `px` | 절대값 | `font-size: 16px` | 고정 크기, 정확하지만 유연하지 않음 |
| `%` | 부모 요소 | `width: 50%` | 부모 크기에 상대적 |
| `em` | 현재 요소의 font-size | `padding: 1.5em` | 중첩 시 복잡해질 수 있음 |
| `rem` | 루트(html) font-size | `font-size: 1.25rem` | **일관성 높음, 권장** |
| `vw` | 뷰포트 너비 | `width: 100vw` | 화면 너비 기준 |
| `vh` | 뷰포트 높이 | `height: 100vh` | 화면 높이 기준 |

### rem 권장 이유

```css
/* html의 font-size가 16px이면 */
html { font-size: 16px; } /* 브라우저 기본값 */

h1 { font-size: 2rem; }   /* 32px = 16px × 2 */
p  { font-size: 1rem; }   /* 16px = 16px × 1 */
small { font-size: 0.875rem; } /* 14px = 16px × 0.875 */

/* 큰 화면에서 전체 글자 크기를 키우려면 html만 변경 */
@media (min-width: 1200px) {
  html { font-size: 18px; }
  /* h1은 자동으로 36px, p는 18px으로 조정됨 */
}
```

`rem`을 사용하면 루트 font-size 하나만 변경해도 모든 요소가 일관되게 조정됩니다.

### max-width로 컨테이너 제한

화면이 매우 넓어질 때 콘텐츠가 지나치게 늘어나지 않도록 최대 너비를 제한합니다.

```css
.container {
  width: 100%;          /* 화면 너비에 맞게 */
  max-width: 1200px;    /* 최대 1200px을 넘지 않음 */
  margin: 0 auto;       /* 가운데 정렬 */
  padding: 0 20px;      /* 좌우 여백 (모바일에서 중요) */
}
```

---

<a id="part5"></a>

## 5️⃣ 실용 예제: 반응형 포트폴리오 [↑](#toc)

HTML 03장의 포트폴리오 페이지에 CSS 01~02장 스타일과 반응형을 추가한 전체 예제입니다.

- **데스크톱**: 왼쪽 사이드바 + 오른쪽 메인 콘텐츠 2단 레이아웃
- **모바일**: 헤더 + 메인 콘텐츠 1단 레이아웃

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>반응형 포트폴리오</title>
  <link rel="stylesheet" href="portfolio.css">
</head>
<body>

  <!-- 헤더 -->
  <header class="site-header">
    <div class="container header-inner">
      <div class="logo">포트폴리오</div>
      <nav class="nav">
        <a href="#about">소개</a>
        <a href="#projects">프로젝트</a>
        <a href="#contact">연락처</a>
      </nav>
    </div>
  </header>

  <!-- 메인 레이아웃 -->
  <main class="container main-layout">

    <!-- 사이드바 -->
    <aside class="sidebar" id="about">
      <div class="profile">
        <div class="profile-avatar">👤</div>
        <h2 class="profile-name">홍길동</h2>
        <p class="profile-role">프론트엔드 개발자</p>
        <ul class="profile-skills">
          <li>HTML / CSS</li>
          <li>JavaScript</li>
          <li>React</li>
        </ul>
      </div>
    </aside>

    <!-- 메인 콘텐츠 -->
    <section class="main-content">

      <div id="projects">
        <h2 class="section-title">프로젝트</h2>
        <div class="project-cards">
          <article class="project-card">
            <h3>날씨 앱</h3>
            <p>OpenWeather API를 활용한 실시간 날씨 정보 앱</p>
            <div class="card-tags">
              <span class="tag">HTML</span>
              <span class="tag">CSS</span>
              <span class="tag">JavaScript</span>
            </div>
          </article>
          <article class="project-card">
            <h3>할 일 목록</h3>
            <p>로컬 스토리지를 활용한 할 일 관리 앱</p>
            <div class="card-tags">
              <span class="tag">React</span>
              <span class="tag">CSS</span>
            </div>
          </article>
        </div>
      </div>

    </section>
  </main>

  <!-- 푸터 -->
  <footer class="site-footer">
    <div class="container">
      <p>© 2024 홍길동. All rights reserved.</p>
    </div>
  </footer>

</body>
</html>
```

```css
/* portfolio.css */

/* ============================================
   기본 설정 (모바일 퍼스트)
   ============================================ */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html { font-size: 16px; }

body {
  font-family: 'Noto Sans KR', sans-serif;
  line-height: 1.7;
  color: #333;
  background-color: #f5f5f5;
}

/* 컨테이너 */
.container {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px;
}

/* ============================================
   헤더
   ============================================ */
.site-header {
  background-color: #1a1a2e;
  padding: 16px 0;
  position: sticky; /* 스크롤 시 상단 고정 */
  top: 0;
  z-index: 100;
}

.header-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.25rem;
  font-weight: 700;
  color: #ffffff;
}

.nav {
  display: flex;
  gap: 24px;
}

.nav a {
  color: #ccc;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.nav a:hover {
  color: #ffffff;
}

/* ============================================
   메인 레이아웃 — 모바일: 1단
   ============================================ */
.main-layout {
  padding-top: 40px;
  padding-bottom: 60px;
  display: flex;
  flex-direction: column; /* 모바일: 세로 쌓기 */
  gap: 32px;
}

/* ============================================
   사이드바
   ============================================ */
.sidebar {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 32px 24px;
  border: 1px solid #e8e8e8;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.profile-avatar {
  font-size: 4rem;
  margin-bottom: 16px;
}

.profile-name {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.profile-role {
  color: #3498db;
  font-size: 0.9rem;
  margin-bottom: 20px;
}

.profile-skills {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.profile-skills li {
  background-color: #f0f4ff;
  color: #3498db;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
}

/* ============================================
   메인 콘텐츠
   ============================================ */
.main-content {
  flex: 1;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e8e8e8;
}

/* 프로젝트 카드 — 모바일: 1열 */
.project-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.project-card {
  background-color: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s, box-shadow 0.2s;
}

.project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.project-card h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.project-card p {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 16px;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  background-color: #f0f4ff;
  color: #3498db;
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
}

/* ============================================
   푸터
   ============================================ */
.site-footer {
  background-color: #1a1a2e;
  color: #999;
  padding: 24px 0;
  text-align: center;
  font-size: 0.9rem;
}

/* ============================================
   태블릿 이상 (min-width: 768px)
   ============================================ */
@media (min-width: 768px) {
  /* 프로젝트 카드 2열 */
  .project-cards {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .project-card {
    flex: 0 0 calc(50% - 8px);
  }
}

/* ============================================
   데스크톱 이상 (min-width: 1024px)
   ============================================ */
@media (min-width: 1024px) {
  /* 메인 레이아웃: 2단 (사이드바 + 메인) */
  .main-layout {
    flex-direction: row;
    align-items: flex-start;
    gap: 40px;
  }

  /* 사이드바: 고정 너비 */
  .sidebar {
    flex: 0 0 260px;
    position: sticky; /* 스크롤 시 사이드바 고정 */
    top: 80px;
  }

  /* 메인 콘텐츠: 나머지 공간 */
  .main-content {
    flex: 1;
  }
}
```

---

<a id="part6"></a>

## 6️⃣ 정리 [↑](#toc)

### 미디어 쿼리 요약

```css
/* 모바일 퍼스트 브레이크포인트 */
/* 기본: 모바일 (0px~) */

@media (min-width: 480px) { /* 스마트폰 가로 */ }
@media (min-width: 768px) { /* 태블릿 */ }
@media (min-width: 1024px) { /* 데스크톱 */ }
@media (min-width: 1440px) { /* 와이드 */ }
```

### 반응형 체크리스트

- `<meta name="viewport" content="width=device-width, initial-scale=1.0">` 추가했는가?
- `box-sizing: border-box` 전역 적용했는가?
- 고정 너비(`px`) 대신 `%`, `rem`, `max-width` 사용했는가?
- 모바일에서 먼저 확인했는가? (Chrome DevTools F12 → 모바일 아이콘)
- 가로 스크롤이 생기지 않는가?
- 텍스트 크기가 모바일에서 읽기 편한가? (최소 14px)
- 버튼/링크 크기가 터치하기 충분한가? (최소 44px × 44px)

### Tailwind CSS와의 연결

이 장에서 직접 작성한 미디어 쿼리를, 다음 과정에서는 **Tailwind CSS**로 훨씬 간결하게 표현합니다.

| 직접 CSS | Tailwind CSS |
|----------|--------------|
| `@media (min-width: 768px) { .cards { flex-direction: row; } }` | `class="flex-col md:flex-row"` |
| `@media (min-width: 1024px) { .sidebar { display: block; } }` | `class="hidden lg:block"` |

> Tailwind CSS 과정에서는 새로운 프로젝트(랜딩 페이지)를 Tailwind로 만들면서, 직접 작성한 CSS와 유틸리티 클래스의 차이를 체감합니다. 실습 과제에서 이 포트폴리오를 Tailwind로 재구현하는 도전도 있습니다!

### 실습 과제

**기본** — 카드 레이아웃 반응형으로 만들기
- 데스크톱: 3열, 태블릿: 2열, 모바일: 1열
- 모바일 퍼스트로 작성 (`min-width` 미디어 쿼리 사용)

**중급** — 02장의 카드 레이아웃에 반응형 내비게이션 추가
- 데스크톱: 가로 내비게이션
- 모바일: 내비게이션 숨기기 (`display: none`) 또는 세로로 전환

**심화** — 반응형 포트폴리오 완성하기
- 위 예제 코드를 직접 입력하고 실행
- Chrome DevTools(F12)에서 모바일 모드로 전환하며 레이아웃 확인
- 브레이크포인트를 조정해 보고 어떻게 달라지는지 관찰
