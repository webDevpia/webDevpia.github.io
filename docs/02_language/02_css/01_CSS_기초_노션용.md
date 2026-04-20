---
nav_exclude: true
---

# 01장. CSS 기초

## 학습 목표

- CSS를 HTML에 연결하는 3가지 방법을 이해하고 외부 파일 방식을 사용할 수 있다
- 선택자로 요소를 지정하고 박스 모델을 이해하여 여백과 크기를 조절할 수 있다

## 진행 순서

1. CSS란? - 스타일시트 언어 소개
2. CSS 연결 방법 3가지 - 인라인, 내부, 외부 스타일
3. 선택자(Selector) - 요소, 클래스, ID 선택자
4. 색상과 텍스트 스타일링 - 색상 표기법, 폰트 속성
5. 박스 모델(Box Model) - content, padding, border, margin
6. display 속성 - block, inline, inline-block
7. position과 transition 기초 - 위치 제어, 부드러운 전환 효과
8. 정리 - 핵심 개념 요약 및 실습 과제

---

## 1️⃣ CSS란?

**CSS(Cascading Style Sheets)**는 HTML로 작성된 웹페이지의 시각적 표현을 담당하는 스타일시트 언어입니다.

### 인테리어 비유

> HTML이 건물의 뼈대라면,
> **CSS는 인테리어 — 벽지 색, 가구 배치, 조명을 결정**합니다.

| 기술 | 역할 | 비유 |
|------|------|------|
| HTML | 웹페이지의 구조와 내용 | 건물의 뼈대 |
| **CSS** | 색상, 폰트, 레이아웃 등 시각적 스타일 | 인테리어 디자인 |
| JavaScript | 버튼 클릭, 데이터 처리 등 동작 | 엘리베이터, 자동문 |

### 캐스케이드(Cascade)의 의미

**캐스케이드(Cascade)**는 '폭포처럼 위에서 아래로 흐른다'는 뜻입니다. CSS 스타일은 여러 곳에서 선언될 수 있고, 더 구체적인 규칙이 일반적인 규칙보다 우선 적용됩니다.

```css
/* 일반 규칙: 모든 p 태그에 적용 */
p { color: black; }

/* 더 구체적인 규칙: .warning 클래스가 있는 p 태그에 적용 → 우선 */
p.warning { color: red; }
```

### CSS가 없는 웹 vs CSS가 있는 웹

CSS 없이 HTML만 있으면 브라우저 기본 스타일만 적용됩니다. 모든 텍스트가 흑백으로 나열되고, 링크는 파란색 밑줄, 헤딩은 굵은 텍스트로만 표시됩니다. CSS를 적용하면 브랜드 색상, 깔끔한 레이아웃, 읽기 좋은 폰트를 갖춘 현대적인 웹페이지가 됩니다.

---

## 2️⃣ CSS 연결 방법 3가지

### 방법 1: 인라인 스타일

HTML 태그의 `style` 속성에 직접 작성합니다.

```html
<h1 style="color: blue; font-size: 32px;">안녕하세요</h1>
<p style="color: gray; margin: 16px 0;">본문 텍스트입니다.</p>
```

### 방법 2: 내부 스타일

HTML 파일의 `<head>` 안에 `<style>` 태그로 작성합니다.

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    h1 { color: blue; }
    p  { color: gray; }
  </style>
</head>
<body>
  <h1>안녕하세요</h1>
  <p>본문 텍스트입니다.</p>
</body>
</html>
```

### 방법 3: 외부 스타일 (권장)

별도의 `.css` 파일을 만들고 HTML에서 `<link>` 태그로 연결합니다.

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>안녕하세요</h1>
  <p>본문 텍스트입니다.</p>
</body>
</html>
```

```css
/* style.css */
h1 { color: blue; }
p  { color: gray; }
```

### 비교 표

| 방식 | 재사용 | 유지보수 | 사용 상황 |
|------|--------|----------|-----------|
| 인라인 | 불가능 | 매우 어려움 | 긴급 테스트, JavaScript로 동적 적용 |
| 내부 스타일 | 같은 파일 내 | 어려움 | 단일 페이지, 이메일 템플릿 |
| **외부 스타일** | **여러 파일 공유** | **쉬움** | **실무 표준 방식** |

외부 파일 방식을 권장하는 이유는 **여러 HTML 파일이 하나의 CSS 파일을 공유**할 수 있어, 스타일을 한 곳에서 수정하면 모든 페이지에 반영되기 때문입니다.

### 실습: 외부 CSS 파일 연결하기

```
프로젝트 폴더/
├── index.html
└── style.css
```

`style.css` 파일을 만들고 `index.html`에서 연결해 보세요.

---

## 3️⃣ 선택자(Selector)

**선택자(Selector)**는 CSS 스타일을 적용할 HTML 요소를 지정하는 방법입니다.

### 요소 선택자

태그 이름으로 선택합니다. 해당 태그 전체에 적용됩니다.

```css
/* 모든 h1 태그의 색상을 빨간색으로 */
h1 { color: red; }

/* 모든 p 태그의 글자 크기를 16px로 */
p { font-size: 16px; }
```

### 클래스 선택자

`.클래스명` 형태로 선택합니다. 여러 요소에 같은 클래스를 적용할 수 있습니다.

```html
<p class="highlight">이 문장은 강조됩니다.</p>
<span class="highlight">이 텍스트도 강조됩니다.</span>
```

```css
/* .highlight 클래스가 있는 모든 요소 */
.highlight { background-color: yellow; }
```

### ID 선택자

`#아이디명` 형태로 선택합니다. 페이지에서 **하나의 요소**에만 사용합니다.

```html
<h1 id="main-title">메인 제목</h1>
```

```css
/* #main-title 아이디를 가진 요소 */
#main-title { font-size: 48px; color: navy; }
```

### 자손 선택자

특정 요소 안에 있는 자손 요소를 선택합니다.

```html
<nav>
  
  
</nav>
```

```css
/* nav 안의 모든 a 태그 */
nav a { color: white; text-decoration: none; }
```

### 언제 무엇을 사용하나?

| 선택자 | 형태 | 재사용 | 우선순위 | 사용 상황 |
|--------|------|--------|----------|-----------|
| 요소 | `h1` | 해당 태그 전체 | 낮음 | 기본 스타일 설정 |
| 클래스 | `.box` | 여러 요소 | 중간 | **실무에서 가장 많이 사용** |
| ID | `#header` | 단 하나 | 높음 | 페이지에서 유일한 요소 |

### 특이성(Specificity) 간단 소개

같은 요소에 여러 규칙이 충돌할 때, **더 구체적인 선택자가 우선** 적용됩니다.

```
ID(100점) > 클래스(10점) > 요소(1점)
```

```css
h1 { color: black; }        /* 1점 */
.title { color: blue; }     /* 10점 → 이 규칙이 적용 */
#main-title { color: red; } /* 100점 → 이 규칙이 적용 */
```

---

## 4️⃣ 색상과 텍스트 스타일링

### 색상 표기법

CSS에서 색상을 표현하는 방법은 4가지입니다.

```css
/* 1. 색상 이름 */
h1 { color: red; }
p  { color: gray; }

/* 2. HEX(16진수) — #RRGGBB */
h1 { color: #ff0000; } /* 빨간색 */
h2 { color: #333333; } /* 진한 회색 */
h3 { color: #4a90d9; } /* 파란색 계열 */

/* 3. RGB */
h1 { color: rgb(255, 0, 0); }   /* 빨간색 */
h2 { color: rgb(51, 51, 51); }  /* 진한 회색 */

/* 4. RGBA — 투명도 포함 (0 = 완전 투명, 1 = 완전 불투명) */
.overlay { background-color: rgba(0, 0, 0, 0.5); }
```

실무에서는 **HEX 코드**를 가장 많이 사용합니다. 디자이너로부터 `#3498db` 같은 HEX 코드를 전달받는 경우가 많습니다.

### 텍스트 스타일링 속성

```css
body {
  /* 글자 크기 (기본값: 16px) */
  font-size: 16px;

  /* 글꼴 — 여러 개를 쓰면 순서대로 폴백(fallback) */
  font-family: 'Noto Sans KR', Arial, sans-serif;

  /* 글자 굵기 (400=기본, 700=굵게) */
  font-weight: 400;

  /* 줄 높이 (가독성을 위해 1.5~1.8 권장) */
  line-height: 1.6;

  /* 글자 색상 */
  color: #333333;
}

h1 {
  /* 텍스트 정렬: left | center | right | justify */
  text-align: center;
}

a {
  /* 밑줄 제거 */
  text-decoration: none;
}

p.intro {
  /* 대소문자 변환: uppercase | lowercase | capitalize */
  text-transform: uppercase;

  /* 글자 간격 */
  letter-spacing: 0.05em;
}
```

### CSS 단위 미리보기

글자 크기나 여백을 지정할 때 숫자 뒤에 붙는 단위입니다.

| 단위 | 의미 | 예시 | 특징 |
|------|------|------|------|
| `px` | 픽셀 (고정 크기) | `font-size: 16px;` | 화면 해상도에 따라 고정 |
| `rem` | 루트 글자 크기 기준 (상대 크기) | `font-size: 2rem;` | 브라우저 기본 16px 기준 → 2rem = 32px |
| `%` | 부모 요소 기준 비율 | `width: 50%;` | 부모의 절반 |

> 💡 `rem`은 "root em"의 약자입니다. `2rem`은 "기본 글자 크기의 2배"라는 뜻입니다.
> 반응형 디자인에서는 `px`보다 `rem`을 권장합니다. 더 자세한 단위는 CSS 03장에서 다룹니다.

### 실용 예시: 본문 텍스트 스타일링

```css
/* style.css */

/* 전체 기본 설정 */
body {
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 16px;
  line-height: 1.7;
  color: #333;
  background-color: #fafafa;
}

/* 제목 */
h1 { font-size: 2rem; color: #1a1a1a; }
h2 { font-size: 1.5rem; color: #2c2c2c; }

/* 링크 */
a { color: #3498db; text-decoration: none; }
a:hover { text-decoration: underline; }
```

---

## 5️⃣ 박스 모델(Box Model)

### 택배 상자 비유

> **택배 상자**를 생각해 보세요.
> - **내용물(content)**: 실제 물건
> - **완충재(padding)**: 내용물 보호를 위한 스티로폼
> - **상자 테두리(border)**: 상자 겉면
> - **상자 간 거리(margin)**: 상자와 상자 사이 공간

### 박스 모델 구조

```
┌─────────────────────────────────┐
│            margin               │
│  ┌───────────────────────────┐  │
│  │          border           │  │
│  │  ┌─────────────────────┐  │  │
│  │  │       padding       │  │  │
│  │  │  ┌───────────────┐  │  │  │
│  │  │  │    content    │  │  │  │
│  │  │  │  (width/height│  │  │  │
│  │  │  └───────────────┘  │  │  │
│  │  └─────────────────────┘  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

```css
.box {
  /* 내용 영역 크기 */
  width: 300px;
  height: 200px;

  /* 안쪽 여백 (내용과 테두리 사이) */
  padding: 20px;           /* 상하좌우 모두 20px */
  padding: 10px 20px;      /* 상하 10px, 좌우 20px */
  padding: 10px 20px 15px 20px; /* 상 우 하 좌 (시계 방향) */

  /* 테두리 */
  border: 1px solid #ddd;  /* 두께 스타일 색상 */

  /* 바깥 여백 (다른 요소와의 거리) */
  margin: 16px;
  margin: 0 auto;          /* 상하 0, 좌우 auto → 가운데 정렬 */
}
```

### box-sizing: border-box

기본값인 `content-box`에서는 `width`가 **내용 영역만**을 의미합니다. padding과 border가 추가되면 실제 크기가 더 커집니다.

```css
/* 문제: width: 300px 이지만 실제 크기는 342px */
.box {
  width: 300px;
  padding: 20px;   /* 좌우 40px 추가 */
  border: 1px solid; /* 좌우 2px 추가 */
  /* 실제 너비 = 300 + 40 + 2 = 342px */
}

/* 해결: box-sizing: border-box 적용 */
.box {
  box-sizing: border-box;
  width: 300px;
  padding: 20px;
  border: 1px solid;
  /* 실제 너비 = 300px (padding, border 포함) */
}
```

```css
/* 모든 요소에 box-sizing 적용 (실무 필수) */
* {
  box-sizing: border-box;
}
```

이 한 줄이 없으면 `width`가 예상과 다르게 동작하는 경우가 많습니다. 모든 프로젝트의 CSS 최상단에 추가하는 것을 권장합니다.

### 개발자 도구(F12)에서 박스 모델 확인하기

1. F12 키를 눌러 개발자 도구를 엽니다
2. Elements 탭에서 원하는 요소를 클릭합니다
3. Styles 패널 하단에서 박스 모델 다이어그램을 확인합니다
4. 각 영역(content, padding, border, margin)의 크기가 색상별로 표시됩니다

### 실습: 카드 만들기

```html
<!-- index.html -->
<div class="card">
  <h2 class="card-title">카드 제목</h2>
  <p class="card-text">카드 내용입니다. 박스 모델을 활용해 여백을 조절합니다.</p>
</div>
```

```css
/* style.css */
* { box-sizing: border-box; }

.card {
  width: 320px;
  padding: 24px;           /* 내부 여백 */
  border: 1px solid #e0e0e0; /* 테두리 */
  border-radius: 8px;      /* 모서리 둥글게 */
  margin: 16px;            /* 외부 여백 */
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 그림자 */
}

.card-title {
  font-size: 1.25rem;
  margin-bottom: 12px;
  color: #1a1a1a;
}

.card-text {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.6;
}
```

---

## 6️⃣ display 속성

**display** 속성은 요소가 화면에서 차지하는 공간의 방식을 결정합니다.

### block

한 줄 전체를 차지합니다. 다음 요소는 항상 새 줄에서 시작합니다.

```html
<div>첫 번째 div</div>
<div>두 번째 div</div>
```

기본값이 block인 태그: `div`, `h1`~`h6`, `p`, `ul`, `li`, `section`, `header`, `footer`

### inline

내용만큼만 차지합니다. 같은 줄에 여러 요소가 나란히 배치됩니다. **width/height 설정 불가**.

```html
<span>텍스트</span>

<strong>굵은 텍스트</strong>
```

기본값이 inline인 태그: `span`, `a`, `strong`, `em`, `img`, `button`

### inline-block

내용만큼 차지하면서도 **width/height 설정이 가능**합니다.

```css
.badge {
  display: inline-block;
  width: 80px;
  height: 28px;
  background-color: #3498db;
  color: white;
  text-align: center;
  border-radius: 4px;
}
```

### none

요소를 완전히 숨깁니다. 공간도 차지하지 않습니다.

```css
/* 모바일에서 사이드바 숨기기 */
.sidebar {
  display: none;
}
```

### 비교 표

| 값 | 공간 차지 | width/height 설정 | 줄바꿈 | 대표 태그 |
|----|-----------|-------------------|--------|-----------|
| `block` | 한 줄 전체 | 가능 | 발생 | div, p, h1 |
| `inline` | 내용만큼 | **불가능** | 미발생 | span, a |
| `inline-block` | 내용만큼 | **가능** | 미발생 | — |
| `none` | 0 | — | — | — |

```css
/* 예시: 인라인 요소에 크기를 주고 싶을 때 */
a.button {
  display: inline-block; /* inline에서는 width/height 적용 안 됨 */
  width: 120px;
  height: 40px;
  background-color: #3498db;
  color: white;
  text-align: center;
  line-height: 40px; /* 세로 가운데 정렬 트릭 */
  border-radius: 4px;
}
```

---

## 7️⃣ position과 transition 기초

### position — 요소의 위치 제어

**position** 속성은 요소를 문서 흐름에서 어떻게 배치할지 결정합니다.

| 값 | 의미 | 사용 예 |
|----|------|---------|
| `static` | 기본값 — 문서 흐름대로 배치 | 대부분의 요소 |
| `relative` | 원래 위치 기준으로 이동 | 미세 조정, absolute의 기준점 |
| `absolute` | 가장 가까운 relative 부모 기준으로 배치 | 배지, 드롭다운, 오버레이 |
| `fixed` | 화면(뷰포트) 기준 고정 | 상단 고정 네비게이션 |
| `sticky` | 스크롤 시 특정 위치에 붙음 | 스크롤 따라가는 헤더 |

```css
/* 상단 고정 네비게이션 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;  /* 다른 요소 위에 표시 (숫자가 클수록 위) */
}

/* 스크롤하면 상단에 붙는 사이드바 */
.sidebar {
  position: sticky;
  top: 80px;  /* 상단에서 80px 위치에 고정 */
}
```

> 💡 **z-index**는 요소의 쌓이는 순서를 결정합니다. 숫자가 클수록 위에 표시됩니다. `position`이 `static`이 아닌 요소에만 적용됩니다.

### transition — 부드러운 변화 효과

**transition**은 CSS 속성 값이 바뀔 때 **즉시 변하지 않고 부드럽게 전환**되도록 만듭니다.

```css
.button {
  background-color: #3498db;
  transition: background-color 0.3s;  /* 배경색을 0.3초에 걸쳐 변경 */
}

.button:hover {
  background-color: #2980b9;  /* 마우스 올리면 부드럽게 색상 전환 */
}
```

```css
/* 카드 hover 효과 — 위로 살짝 올라가면서 그림자 커짐 */
.card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-4px);     /* 위로 4px 이동 */
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
```

> **비유**: transition은 **슬로우 모션**입니다. "색상이 바뀌었다!"가 아니라 "색상이 부드럽게~ 바뀌는 중..."이 됩니다. 이후 Flexbox 챕터와 Tailwind에서 자주 사용합니다.

---

## 8️⃣ 정리

### 핵심 개념 요약

| 개념 | 설명 | 핵심 포인트 |
|------|------|-------------|
| CSS 연결 | 외부 파일 방식 권장 | `<link rel="stylesheet" href="style.css">` |
| 선택자 | 요소 / 클래스 / ID | 클래스를 가장 많이 사용 |
| 특이성 | ID > 클래스 > 요소 | 충돌 시 더 구체적인 규칙 적용 |
| 색상 | 이름, HEX, RGB | 실무에서는 HEX 많이 사용 |
| 박스 모델 | content→padding→border→margin | `box-sizing: border-box` 필수 |
| display | block / inline / inline-block / none | 레이아웃의 기초 |
| position | static / relative / absolute / fixed / sticky | 요소 배치 제어 |
| transition | 속성 변화를 부드럽게 | `transition: 속성 시간` |

### 다음 장 미리보기

**02장 CSS Flexbox** — 박스 모델을 이해했다면 이제 여러 요소를 **가로로 나란히 배치**하는 방법을 배웁니다. `display: flex` 한 줄로 시작하는 현대적인 레이아웃 기법입니다.

### 실습 과제

**기본** — HTML 03장의 포트폴리오 페이지에 CSS로 색상과 폰트 입히기
- `body`에 `font-family`, `color`, `background-color` 설정
- 제목, 본문, 링크에 각각 다른 스타일 적용

**중급** — 3개의 카드를 만들고 박스 모델로 여백/테두리 조절하기
- `padding`, `border`, `margin`, `border-radius` 활용
- `box-sizing: border-box` 적용

**심화** — 개발자 도구(F12)에서 아무 웹사이트의 박스 모델 탐색하기
- 마음에 드는 웹사이트에서 요소를 선택
- 박스 모델 다이어그램에서 각 영역의 크기 확인
- CSS 속성을 개발자 도구에서 직접 수정해 보기
