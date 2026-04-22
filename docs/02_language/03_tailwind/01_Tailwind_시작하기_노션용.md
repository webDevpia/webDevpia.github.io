---
nav_exclude: true
---

# 01장. Tailwind CSS 시작하기

## 학습 목표

- Tailwind CSS의 개념과 장점을 이해하고 CDN으로 바로 사용할 수 있다
- CSS 속성과 Tailwind 클래스의 1:1 대응 관계를 이해하고 활용할 수 있다

> **사전 준비:** CSS 01~03장에서 박스 모델, Flexbox, 미디어 쿼리를 이해한 상태에서 진행합니다.

## 진행 순서

1. Tailwind CSS란? — 유틸리티 클래스 개념과 등장 배경
2. CDN으로 시작하기 — v4 CDN 설정과 첫 실습
3. CSS ↔ Tailwind 대응표 — 핵심 클래스 1:1 매핑
4. 색상 시스템 — 팔레트와 농도 체계
5. hover, focus, 상태 클래스 — 인터랙티브 스타일링
6. 실용 예제: 카드 레이아웃 변환 — Before/After 비교
7. 정리 — 치트시트와 실습 과제

---

## 1️⃣ Tailwind CSS란?

**Tailwind CSS**는 **유틸리티 클래스**(Utility Class) 기반의 CSS 프레임워크입니다.

### CSS 속성의 축약어 사전

> `padding: 1.5rem`을 `p-6`이라는 짧은 코드로 쓸 수 있는 클래스를 미리 모아놓은 것입니다.
> 즉, Tailwind는 CSS를 새로 배우는 것이 아니라, **이미 알고 있는 CSS를 더 짧게 쓰는 방법**입니다.

> **비유: 레고 블록** — 각 클래스가 레고 한 조각입니다. `bg-blue-500`(파란 배경), `text-white`(흰 글씨), `px-4`(좌우 여백), `py-2`(상하 여백), `rounded`(모서리)를 하나씩 조합하면 원하는 버튼이 완성됩니다. 조각 하나하나는 단순하지만, 조합하면 무엇이든 만들 수 있습니다.

CSS를 직접 작성하는 대신, 미리 정의된 클래스를 HTML에 바로 붙여서 스타일을 적용합니다.

```html
<!-- 순수 CSS 방식: 별도 CSS 파일 필요 -->
<div class="card">내용</div>

<!-- Tailwind 방식: HTML에 바로 클래스를 붙임 -->
<div class="bg-white rounded-lg p-6 shadow-md">내용</div>
```

### 왜 인기인가?

2025년 기준 CSS 프레임워크 사용률 **1위**(37%) 를 차지하고 있습니다. 인기 이유는 다음과 같습니다.

- **CSS 파일을 따로 관리하지 않아도 됩니다** — HTML 하나로 구조와 스타일을 동시에
- **디자인 일관성** — 정해진 간격(4, 8, 12px...)과 색상 팔레트를 사용하므로 디자인이 통일됩니다
- **빠른 프로토타이핑** — 클래스 이름만 붙이면 바로 결과 확인

### CSS 10줄 vs Tailwind 1줄

**순수 CSS로 버튼 만들기 (CSS 파일 필요):**

```css
.btn {
    background-color: #3b82f6;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    font-weight: 600;
    border: none;
    cursor: pointer;
}
.btn:hover {
    background-color: #2563eb;
}
```

**Tailwind로 같은 버튼 (CSS 파일 불필요):**

```html
<button class="bg-blue-500 text-white px-4 py-2 rounded-md font-semibold hover:bg-blue-600">
  버튼
</button>
```

> CSS 파일을 왔다갔다 할 필요 없이, HTML에서 바로 스타일을 완성할 수 있습니다.
>
> 브라우저에서 이렇게 보입니다: 파란 배경에 흰 글씨 버튼이 나타나고, 마우스를 올리면 약간 진한 파란색으로 변합니다.

### 순수 CSS vs Bootstrap vs Tailwind 비교

| | 순수 CSS | Bootstrap | Tailwind |
|---|---------|-----------|----------|
| 접근 방식 | 직접 작성 | 미리 만든 컴포넌트 | 유틸리티 클래스 조합 |
| 디자인 자유도 | 최고 | 중간 | 최고 |
| 초보 진입장벽 | 낮음 | 낮음 | CSS 기초 필요 |
| 파일 구조 | HTML + CSS 파일 분리 | HTML + Bootstrap CSS | HTML 하나로 완결 |
| 코드 예시 | `class="card"` + CSS 파일 | `class="btn btn-primary"` | `class="bg-blue-500 text-white px-4 py-2 rounded"` |

Bootstrap은 `btn btn-primary`처럼 **미리 만들어진 컴포넌트**를 사용하므로 빠르지만 디자인이 비슷비슷해집니다. Tailwind는 블록처럼 조합하기 때문에 자유도가 높습니다.

---

## 2️⃣ CDN으로 시작하기 (v4)

**CDN**(Content Delivery Network) 이란 인터넷에서 파일을 가져오는 방법입니다. npm으로 설치하지 않고도 `<script>` 태그 하나로 Tailwind를 바로 사용할 수 있습니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tailwind 시작하기</title>
    <!-- Tailwind CSS v4 CDN -->
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-gray-50 p-8">
    <h1 class="text-3xl font-bold text-blue-600">Hello Tailwind!</h1>
    <p class="mt-4 text-gray-600">유틸리티 클래스로 스타일링합니다.</p>
</body>
</html>
```

> 브라우저에서 이렇게 보입니다: 파란색 굵은 큰 글자로 'Hello Tailwind!'가 표시되고, 그 아래 회색 본문 텍스트가 위쪽 여백과 함께 나타납니다.

위 파일을 `index.html`로 저장하고 Live Server로 열면 바로 결과를 확인할 수 있습니다.

### CDN vs npm 차이

| | CDN | npm (Vite/Next.js 등) |
|---|-----|----------------------|
| 설정 복잡도 | `<script>` 태그 1줄 | 패키지 설치 + 설정 파일 |
| 사용 목적 | 학습, 빠른 프로토타입 | 실무 프로젝트 |
| 빌드 최적화 | 없음 (전체 CSS 로드) | 사용한 클래스만 포함 |
| 이 수업 | ✅ CDN 사용 | — |

> **수업에서는 CDN을 사용합니다.** 실무에서는 npm + Vite 환경을 사용하지만, 지금은 HTML 파일 하나로 바로 실습합니다.

### 첫 번째 실습: 텍스트 스타일링

복사-붙여넣기로 바로 실행하세요.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>텍스트 스타일링</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-gray-100 p-10">
    <!-- text-3xl: font-size: 1.875rem -->
    <!-- font-bold: font-weight: 700 -->
    <!-- text-blue-600: color: #2563eb -->
    <h1 class="text-3xl font-bold text-blue-600">제목입니다</h1>

    <!-- mt-4: margin-top: 1rem -->
    <!-- text-gray-500: color: #6b7280 -->
    <p class="mt-4 text-gray-500">본문 텍스트입니다.</p>
</body>
</html>
```

> 브라우저에서 이렇게 보입니다: 연한 회색 배경 위에 파란 굵은 제목이 크게 표시되고, 아래에 회색(연한) 본문 텍스트가 위쪽 간격을 두고 나타납니다.

---

## 3️⃣ CSS ↔ Tailwind 대응표

이 섹션이 Tailwind 학습의 핵심입니다. **새로운 언어를 배우는 것이 아니라, CSS를 짧게 쓰는 법**을 익히는 것입니다.

### Tailwind 숫자 체계 (Spacing Scale)

> **비유: 눈금자** — Tailwind의 숫자는 0.25rem(4px) 간격의 눈금입니다. `p-4`는 "눈금 4칸 = 1rem = 16px"입니다. 눈금자를 보듯이 숫자가 커질수록 간격이 일정하게 늘어납니다.

Tailwind의 간격(padding, margin, gap, width, height 등)은 모두 동일한 숫자 체계를 사용합니다.

| 숫자 | rem | px | 예시 |
|------|-----|-----|------|
| 0 | 0 | 0px | `p-0` (여백 없음) |
| 0.5 | 0.125rem | 2px | `p-0.5` |
| 1 | 0.25rem | 4px | `p-1` |
| 2 | 0.5rem | 8px | `p-2` |
| 3 | 0.75rem | 12px | `p-3` |
| 4 | 1rem | 16px | `p-4` |
| 6 | 1.5rem | 24px | `p-6` |
| 8 | 2rem | 32px | `p-8` |
| 12 | 3rem | 48px | `p-12` |
| 16 | 4rem | 64px | `p-16` |
| 20 | 5rem | 80px | `p-20` |
| 24 | 6rem | 96px | `p-24` |

> 💡 **규칙:** 숫자 × 0.25rem = 실제 크기. 예: `p-8` = 8 × 0.25rem = 2rem = 32px
>
> ⚠️ **주의:** 숫자가 연속적이지 않습니다! 4 다음에 5가 아니라 6이고, 8 다음에 10이 아니라 12입니다. 필요한 숫자를 [공식 문서](https://tailwindcss.com/docs/customizing-spacing)에서 확인하세요.
>
> 💡 **임의값:** 스케일에 없는 정확한 값이 필요하면 `p-[13px]`, `w-[200px]`처럼 대괄호로 직접 지정할 수 있습니다 (Tailwind v3+).

### 간격(Spacing) — padding, margin

Tailwind의 숫자 단위: **숫자 × 0.25rem** (기본 폰트 16px 기준)

| CSS 속성 | 값 | Tailwind | 기억법 |
|----------|-----|---------|--------|
| `padding: 0.5rem` | `8px` | `p-2` | p + 숫자 (4=1rem 기준) |
| `padding: 1rem` | `16px` | `p-4` | |
| `padding: 1.5rem` | `24px` | `p-6` | |
| `padding: 2rem` | `32px` | `p-8` | |
| `padding-left/right: 1rem` | | `px-4` | px = padding x축(좌우) |
| `padding-top/bottom: 1rem` | | `py-4` | py = padding y축(상하) |
| `padding-top: 1rem` | | `pt-4` | pt = padding-top |
| `padding-bottom: 1rem` | | `pb-4` | pb = padding-bottom |
| `margin: 1rem` | `16px` | `m-4` | m = margin |
| `margin: 0 auto` | | `mx-auto` | x축 auto = 가운데 정렬 |
| `margin-top: 1rem` | | `mt-4` | mt = margin-top |
| `margin-bottom: 1rem` | | `mb-4` | mb = margin-bottom |

```html
<!-- CSS 방식 -->
<style>
.box { padding: 1.5rem; margin: 1rem auto; }
</style>
<div class="box">내용</div>

<!-- Tailwind 방식: CSS 파일 없음 -->
<div class="p-6 mx-auto">내용</div>
```

### 간격과 여백 심화

| CSS 속성 | Tailwind | 비고 |
|----------|---------|------|
| `padding-left: 1rem` | `pl-4` | 왼쪽만 |
| `padding-right: 1rem` | `pr-4` | 오른쪽만 |
| `margin-left: 1rem` | `ml-4` | 왼쪽만 |
| `margin-right: 1rem` | `mr-4` | 오른쪽만 |
| `margin-top: -1rem` | `-mt-4` | 음수 마진 (요소를 위로 당김) |
| `margin-left: auto` | `ml-auto` | 오른쪽으로 밀기 |

### 레이아웃 — display, flexbox

| CSS 속성 | Tailwind | 기억법 |
|----------|---------|--------|
| `display: flex` | `flex` | 동일 |
| `display: grid` | `grid` | 동일 |
| `display: block` | `block` | 동일 |
| `display: none` | `hidden` | Tailwind에서는 hidden으로 표현 |
| `justify-content: center` | `justify-center` | justify + 값 |
| `justify-content: space-between` | `justify-between` | |
| `justify-content: flex-end` | `justify-end` | |
| `align-items: center` | `items-center` | items + 값 |
| `align-items: flex-start` | `items-start` | |
| `flex-direction: column` | `flex-col` | |
| `flex-wrap: wrap` | `flex-wrap` | 동일 |
| `gap: 1rem` | `gap-4` | gap + 숫자 |
| `gap: 1.5rem` | `gap-6` | |

```html
<!-- CSS Flexbox -->
<style>
.nav { display: flex; justify-content: space-between; align-items: center; }
</style>

<!-- Tailwind Flexbox -->
<nav class="flex justify-between items-center">
    <div>로고</div>
    <div>메뉴</div>
</nav>
```

### Flexbox 심화

| CSS 속성 | Tailwind | 용도 |
|----------|---------|------|
| `flex: 1 1 0%` | `flex-1` | 남은 공간 균등 분배 |
| `flex-grow: 1` | `grow` | 늘어남 허용 |
| `flex-shrink: 0` | `shrink-0` | 줄어듦 방지 |
| `align-self: center` | `self-center` | 개별 아이템 정렬 |
| `order: -1` | `order-first` | 순서 변경 (맨 앞으로) |

### 타이포그래피 — font-size, font-weight, color

| CSS 속성 | 값 | Tailwind | 기억법 |
|----------|-----|---------|--------|
| `font-size: 0.75rem` | `12px` | `text-xs` | extra small |
| `font-size: 0.875rem` | `14px` | `text-sm` | small |
| `font-size: 1rem` | `16px` | `text-base` | base(기본) |
| `font-size: 1.125rem` | `18px` | `text-lg` | large |
| `font-size: 1.25rem` | `20px` | `text-xl` | extra large |
| `font-size: 1.5rem` | `24px` | `text-2xl` | 2x extra large |
| `font-size: 1.875rem` | `30px` | `text-3xl` | |
| `font-size: 2.25rem` | `36px` | `text-4xl` | |
| `font-weight: 400` | normal | `font-normal` | |
| `font-weight: 500` | medium | `font-medium` | |
| `font-weight: 600` | semibold | `font-semibold` | |
| `font-weight: 700` | bold | `font-bold` | |
| `line-height: 1.5` | | `leading-normal` | leading = 행간 |
| `text-align: center` | | `text-center` | |

### 크기 — width, height

| CSS 속성 | 값 | Tailwind | 기억법 |
|----------|-----|---------|--------|
| `width: 100%` | | `w-full` | full = 100% |
| `width: 50%` | | `w-1/2` | 분수 표기 |
| `width: 25%` | | `w-1/4` | |
| `height: 100%` | | `h-full` | |
| `height: 100vh` | | `h-screen` | screen = vh |
| `min-height: 100vh` | | `min-h-screen` | |
| `max-width: 1280px` | | `max-w-screen-xl` | |
| `max-width: 1024px` | | `max-w-screen-lg` | |
| `max-width: 320px` | | `max-w-xs` | |
| `max-width: 28rem` | | `max-w-md` | medium |

### 색상 — color, background-color

| CSS 속성 | Tailwind | 기억법 |
|----------|---------|--------|
| `color: #3b82f6` (파랑) | `text-blue-500` | text + 색상명 + 농도 |
| `color: #ffffff` (흰색) | `text-white` | |
| `color: #111827` (거의 검정) | `text-gray-900` | |
| `background-color: #3b82f6` | `bg-blue-500` | bg + 색상명 + 농도 |
| `background-color: #ffffff` | `bg-white` | |
| `background-color: #f9fafb` | `bg-gray-50` | |

### 테두리와 그림자

| CSS 속성 | Tailwind | 기억법 |
|----------|---------|--------|
| `border-radius: 0.25rem` | `rounded` | 기본 rounded |
| `border-radius: 0.5rem` | `rounded-lg` | large |
| `border-radius: 1rem` | `rounded-2xl` | |
| `border-radius: 9999px` | `rounded-full` | 완전 원형 |
| `border: 1px solid` | `border` | 기본 테두리 |
| `border-color: #e5e7eb` | `border-gray-200` | |
| `box-shadow: 작은 그림자` | `shadow-sm` | |
| `box-shadow: 중간 그림자` | `shadow-md` | |
| `box-shadow: 큰 그림자` | `shadow-lg` | |
| `box-shadow: 매우 큰 그림자` | `shadow-xl` | |

### 테두리 상세

| CSS 속성 | Tailwind | 비고 |
|----------|---------|------|
| `border: 1px solid` | `border` | 기본 테두리 |
| `border-width: 2px` | `border-2` | 두꺼운 테두리 |
| `border-color: #e5e7eb` | `border-gray-200` | 테두리 색상 |
| `outline` | `outline` | 테두리 바깥 선 (레이아웃에 영향 없음) |
| `box-shadow (ring)` | `ring-2 ring-blue-500` | focus 시 포커스 링 (outline 대신 사용) |

> 💡 **ring vs border vs outline 차이:**
> - `border`: 요소의 실제 테두리, 레이아웃에 영향
> - `outline`: 요소 바깥 선, 레이아웃에 영향 없음 (접근성용)
> - `ring`: Tailwind 전용, box-shadow로 구현된 포커스 표시 — 두께/색상 조절이 쉬움

### 위치와 레이어 (Position / Z-index)

| CSS 속성 | Tailwind | 용도 |
|----------|---------|------|
| `position: relative` | `relative` | 기준점 설정 |
| `position: absolute` | `absolute` | 부모 기준 위치 지정 |
| `position: fixed` | `fixed` | 화면 고정 (스크롤해도 안 움직임) |
| `position: sticky` | `sticky` | 스크롤 시 상단 고정 |
| `top: 0` | `top-0` | 위쪽 0 |
| `z-index: 10` | `z-10` | 레이어 순서 (높을수록 위) |
| `z-index: 50` | `z-50` | 모달, 드롭다운에 사용 |
| `overflow: hidden` | `overflow-hidden` | 넘치는 내용 숨기기 |
| `overflow: auto` | `overflow-auto` | 넘치면 스크롤 표시 |

### 실습: CSS 카드를 Tailwind로 변환

**순수 CSS 버전 (CSS 파일 + HTML 필요):**

```css
/* style.css */
.card {
    background: white;
    border-radius: 0.5rem;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 320px;
}
.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 0.5rem;
}
.card-text {
    color: #6b7280;
    line-height: 1.6;
}
```

```html
<!-- index.html -->
<div class="card">
    <h2 class="card-title">카드 제목</h2>
    <p class="card-text">카드 내용입니다.</p>
</div>
```

**Tailwind 버전 (HTML 파일 하나로 완결):**

```html
<div class="bg-white rounded-lg p-6 shadow-md max-w-xs">
    <h2 class="text-xl font-bold text-gray-800 mb-2">카드 제목</h2>
    <p class="text-gray-500 leading-relaxed">카드 내용입니다.</p>
</div>
```

> CSS 파일이 사라지고 HTML만으로 동일한 결과를 얻습니다.
>
> 두 카드의 모양은 동일하지만, Tailwind 버전은 CSS 파일 없이 HTML만으로 완성되었습니다.

---

## 4️⃣ 색상 시스템

Tailwind는 **정해진 색상 팔레트**를 사용합니다. 임의의 16진수 색상 대신, 이름과 농도 조합으로 색상을 지정합니다.

### 농도(Shade) 체계

> **비유: 물감 농도** — 물에 물감을 타는 것을 상상하세요. 50은 물을 많이 타서 매우 연한 색, 500은 기본 색(물감 원래 색), 900은 원액에 가까운 진한 색입니다. 숫자가 클수록 진하고, 작을수록 밝습니다.

숫자가 **클수록 진하고**, **작을수록 밝습니다.**

| 농도 | 의미 | 사용 예 |
|------|------|---------|
| `50` | 매우 밝음 (거의 흰색) | 배경색 |
| `100` | 밝음 | 배경 강조 |
| `200` | 연함 | 테두리 |
| `300` | | 비활성 텍스트 |
| `400` | | 아이콘 |
| `500` | 기본색 (표준) | 버튼, 링크 |
| `600` | 진함 | 버튼 hover |
| `700` | 더 진함 | 헤더 |
| `800` | 어두움 | 타이틀 |
| `900` | 매우 어두움 | 제목, 강조 |
| `950` | 거의 검정 | |

> 💡 **실무 팁 — 색상 농도 사용 가이드:**
> - **배경색:** 50~200 (연한 색) — 눈이 편안
> - **텍스트:** 700~900 (진한 색) — 가독성 확보
> - **버튼/강조:** 500~600 (기본 색) — 눈에 띄면서 과하지 않음
> - **hover 변화:** 기본보다 100 올리기 — `bg-blue-500 hover:bg-blue-600`

### 주요 색상 종류

```
gray, slate, zinc, neutral, stone   ← 회색 계열
red, orange, amber, yellow          ← 따뜻한 계열
lime, green, emerald, teal          ← 초록 계열
cyan, sky, blue, indigo, violet     ← 파랑/보라 계열
purple, fuchsia, pink, rose         ← 분홍/보라 계열
```

### 색상 사용법

```html
<!-- 텍스트 색상: text-{색상}-{농도} -->
<p class="text-blue-500">파란 텍스트</p>
<p class="text-red-600">빨간 텍스트</p>
<p class="text-gray-400">회색 텍스트 (연함)</p>
<p class="text-gray-900">거의 검정 텍스트</p>

<!-- 배경 색상: bg-{색상}-{농도} -->
<div class="bg-blue-100">연한 파란 배경</div>
<div class="bg-green-500">초록 배경</div>
<div class="bg-gray-800 text-white">어두운 배경 + 흰 텍스트</div>

<!-- 테두리 색상: border-{색상}-{농도} -->
<div class="border border-gray-200">연한 테두리</div>
<div class="border-2 border-blue-500">파란 테두리</div>
```

### 실습: 다양한 색상의 버튼

```html
<div class="flex gap-4 p-8 flex-wrap">
    <!-- 파란 버튼 -->
    <button class="bg-blue-500 text-white px-4 py-2 rounded">파랑</button>

    <!-- 초록 버튼 -->
    <button class="bg-green-500 text-white px-4 py-2 rounded">초록</button>

    <!-- 빨간 버튼 -->
    <button class="bg-red-500 text-white px-4 py-2 rounded">빨강</button>

    <!-- 아웃라인 버튼 (배경 없이 테두리만) -->
    <button class="border-2 border-blue-500 text-blue-500 px-4 py-2 rounded">아웃라인</button>

    <!-- 회색 버튼 -->
    <button class="bg-gray-200 text-gray-700 px-4 py-2 rounded">회색</button>
</div>
```

### 전체 코드로 실행해보기 — 색상 시스템

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tailwind 색상</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-gray-50 p-8">
    <h1 class="text-2xl font-bold mb-6">색상 시스템</h1>

    <h2 class="text-lg font-semibold mb-3">텍스트 + 배경 색상</h2>
    <p class="text-blue-500 mb-1">text-blue-500: 파란 텍스트</p>
    <p class="text-red-600 mb-1">text-red-600: 빨간 텍스트</p>
    <div class="bg-gray-800 text-white p-3 rounded mb-6">bg-gray-800: 어두운 배경 + 흰 텍스트</div>

    <h2 class="text-lg font-semibold mb-3">다양한 색상의 버튼</h2>
    <div class="flex gap-4 flex-wrap">
        <button class="bg-blue-500 text-white px-4 py-2 rounded">파랑</button>
        <button class="bg-green-500 text-white px-4 py-2 rounded">초록</button>
        <button class="bg-red-500 text-white px-4 py-2 rounded">빨강</button>
        <button class="border-2 border-blue-500 text-blue-500 px-4 py-2 rounded">아웃라인</button>
        <button class="bg-gray-200 text-gray-700 px-4 py-2 rounded">회색</button>
    </div>
</body>
</html>
```

> 💡 `blue-500`을 `blue-300`이나 `blue-700`으로 바꿔보세요. 숫자가 작을수록 연하고, 클수록 진합니다.

---

## 5️⃣ hover, focus, 상태 클래스

Tailwind에서 `hover:`, `focus:` 등의 **접두사**(prefix) 를 붙이면 해당 상태일 때만 스타일이 적용됩니다.

### 기본 상태 클래스

| CSS | Tailwind | 설명 |
|-----|---------|------|
| `:hover { background: #1d4ed8 }` | `hover:bg-blue-700` | 마우스 올릴 때 |
| `:hover { color: white }` | `hover:text-white` | |
| `:focus { outline: 2px solid blue }` | `focus:ring-2 focus:ring-blue-500` | 클릭/탭 포커스 시 |
| `:active { opacity: 0.8 }` | `active:opacity-80` | 클릭하는 순간 |

> 💡 **원리**: `hover:bg-blue-700`은 CSS의 `:hover { background-color: ... }`를 Tailwind가 자동으로 만들어주는 것입니다. `focus:`, `active:` 등도 동일한 원리입니다.

### transition — 부드러운 전환

```html
<!-- transition: 모든 속성에 transition 적용 -->
<!-- duration-300: 전환 시간 300ms -->
<!-- ease-in-out: 가속/감속 곡선 -->
<button class="bg-blue-500 text-white px-6 py-3 rounded-lg
               transition duration-300 ease-in-out
               hover:bg-blue-700 hover:shadow-lg">
    호버해 보세요
</button>
```

> 브라우저에서 이렇게 보입니다: 파란 버튼에 마우스를 올리면 색상이 부드럽게 진한 파란색으로 바뀌고, 그림자가 나타납니다 (300ms 동안 서서히 전환).

CSS로 작성하면:
```css
.button {
    background-color: #3b82f6;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    transition: all 300ms ease-in-out;
}
.button:hover {
    background-color: #1d4ed8;
    box-shadow: 0 10px 15px rgba(0,0,0,0.1);
}
```

### 실습: hover 효과 있는 카드

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hover 카드</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center p-8">
    <div class="flex gap-6">
        <!-- hover 효과가 있는 카드 -->
        <div class="bg-white rounded-xl p-6 shadow-md max-w-xs
                    transition duration-300
                    hover:shadow-xl hover:-translate-y-1 cursor-pointer">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <!-- 아이콘 자리 -->
                <span class="text-blue-600 text-xl font-bold">★</span>
            </div>
            <h3 class="text-lg font-bold text-gray-800 mb-2">카드 제목</h3>
            <p class="text-gray-500 text-sm leading-relaxed">
                마우스를 올려보세요. 카드가 위로 살짝 올라갑니다.
            </p>
        </div>

        <!-- 두 번째 카드 -->
        <div class="bg-white rounded-xl p-6 shadow-md max-w-xs
                    transition duration-300
                    hover:shadow-xl hover:-translate-y-1 cursor-pointer">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <span class="text-green-600 text-xl font-bold">♥</span>
            </div>
            <h3 class="text-lg font-bold text-gray-800 mb-2">두 번째 카드</h3>
            <p class="text-gray-500 text-sm leading-relaxed">
                hover:-translate-y-1 로 위로 이동하는 효과를 줍니다.
            </p>
        </div>
    </div>
</body>
</html>
```

> 브라우저에서 이렇게 보입니다: 흰 카드 두 개가 나란히 놓여 있고, 마우스를 올리면 카드가 위로 살짝 이동하면서 그림자가 커집니다.

### focus — 폼 요소 스타일링

```html
<!-- 입력창에 포커스 시 파란 테두리 표시 -->
<input
    type="text"
    placeholder="이름을 입력하세요"
    class="border border-gray-300 rounded-lg px-4 py-2 w-full
           focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
           transition duration-200"
/>
```

> 브라우저에서 이렇게 보입니다: 기본 상태에서는 회색 테두리 입력창이고, 클릭하면 파란 링(포커스 링)이 둘레에 생깁니다.

CSS로 작성하면:
```css
input {
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    width: 100%;
    transition: all 200ms;
}
input:focus {
    outline: none;
    box-shadow: 0 0 0 2px #3b82f6;
    border-color: transparent;
}
```

### 전체 코드로 실행해보기 — hover + focus

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>hover + focus</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-gray-100 p-8 space-y-8">
    <h1 class="text-2xl font-bold">hover + focus 체험</h1>

    <h2 class="text-lg font-semibold">hover 카드 (마우스를 올려보세요)</h2>
    <div class="flex gap-6">
        <div class="bg-white rounded-xl p-6 shadow-md max-w-xs
                    transition duration-300 hover:shadow-xl hover:-translate-y-1 cursor-pointer">
            <h3 class="text-lg font-bold text-gray-800 mb-2">카드 1</h3>
            <p class="text-gray-500 text-sm">hover 시 위로 올라갑니다</p>
        </div>
        <div class="bg-white rounded-xl p-6 shadow-md max-w-xs
                    transition duration-300 hover:shadow-xl hover:-translate-y-1 cursor-pointer">
            <h3 class="text-lg font-bold text-gray-800 mb-2">카드 2</h3>
            <p class="text-gray-500 text-sm">그림자도 커집니다</p>
        </div>
    </div>

    <h2 class="text-lg font-semibold">focus 입력창 (클릭해보세요)</h2>
    <input type="text" placeholder="이름을 입력하세요"
           class="border border-gray-300 rounded-lg px-4 py-2 w-full max-w-md
                  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                  transition duration-200" />

    <input type="email" placeholder="이메일을 입력하세요"
           class="border border-gray-300 rounded-lg px-4 py-2 w-full max-w-md
                  focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent
                  transition duration-200" />
</body>
</html>
```

> 💡 `focus:ring-blue-500`을 `focus:ring-red-500`으로 바꾸면 포커스 링 색상이 변합니다.

---

## 6️⃣ 실용 예제: CSS 카드 레이아웃을 Tailwind로 변환

CSS 02장에서 만든 Flexbox 카드 레이아웃을 Tailwind로 재구현합니다.

### Before: 순수 CSS 방식

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>카드 레이아웃 - CSS 방식</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #f3f4f6; padding: 2rem; font-family: sans-serif; }
        .container { max-width: 960px; margin: 0 auto; }
        h1 { text-align: center; font-size: 2rem; color: #1f2937; margin-bottom: 2rem; }
        .card-grid {
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            justify-content: center;
        }
        .card {
            background: white;
            border-radius: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            width: 280px;
            transition: box-shadow 0.3s, transform 0.3s;
        }
        .card:hover {
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
            transform: translateY(-4px);
        }
        .card-icon {
            width: 3rem; height: 3rem;
            background: #dbeafe;
            border-radius: 0.5rem;
            display: flex; align-items: center; justify-content: center;
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }
        .card-title { font-size: 1.125rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem; }
        .card-desc { color: #6b7280; font-size: 0.875rem; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>서비스 소개</h1>
        <div class="card-grid">
            <div class="card">
                <div class="card-icon">🚀</div>
                <h2 class="card-title">빠른 속도</h2>
                <p class="card-desc">최적화된 코드로 빠른 로딩을 제공합니다.</p>
            </div>
            <div class="card">
                <div class="card-icon">🔒</div>
                <h2 class="card-title">안전한 보안</h2>
                <p class="card-desc">최신 보안 기술로 데이터를 보호합니다.</p>
            </div>
            <div class="card">
                <div class="card-icon">💡</div>
                <h2 class="card-title">스마트 기능</h2>
                <p class="card-desc">AI 기반으로 더 스마트한 서비스를 제공합니다.</p>
            </div>
        </div>
    </div>
</body>
</html>
```

### After: Tailwind 방식 (CSS 파일 없음)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>카드 레이아웃 - Tailwind 방식</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-gray-100 p-8 font-sans">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-center text-4xl font-bold text-gray-800 mb-8">서비스 소개</h1>

        <div class="flex gap-6 flex-wrap justify-center">
            <!-- 카드 1 -->
            <div class="bg-white rounded-xl p-6 shadow-sm w-72
                        transition duration-300 hover:shadow-lg hover:-translate-y-1 cursor-pointer">
                <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4 text-2xl">
                    🚀
                </div>
                <h2 class="text-lg font-bold text-gray-800 mb-2">빠른 속도</h2>
                <p class="text-gray-500 text-sm leading-relaxed">최적화된 코드로 빠른 로딩을 제공합니다.</p>
            </div>

            <!-- 카드 2 -->
            <div class="bg-white rounded-xl p-6 shadow-sm w-72
                        transition duration-300 hover:shadow-lg hover:-translate-y-1 cursor-pointer">
                <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4 text-2xl">
                    🔒
                </div>
                <h2 class="text-lg font-bold text-gray-800 mb-2">안전한 보안</h2>
                <p class="text-gray-500 text-sm leading-relaxed">최신 보안 기술로 데이터를 보호합니다.</p>
            </div>

            <!-- 카드 3 -->
            <div class="bg-white rounded-xl p-6 shadow-sm w-72
                        transition duration-300 hover:shadow-lg hover:-translate-y-1 cursor-pointer">
                <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4 text-2xl">
                    💡
                </div>
                <h2 class="text-lg font-bold text-gray-800 mb-2">스마트 기능</h2>
                <p class="text-gray-500 text-sm leading-relaxed">AI 기반으로 더 스마트한 서비스를 제공합니다.</p>
            </div>
        </div>
    </div>
</body>
</html>
```

> 두 카드의 모양은 동일하지만, Tailwind 버전은 CSS 파일 없이 HTML만으로 완성되었습니다.

### Before / After 핵심 비교

| | CSS 방식 | Tailwind 방식 |
|---|---------|--------------|
| 파일 수 | HTML + CSS (2개) | HTML 하나 |
| CSS 줄 수 | 약 45줄 | 0줄 (클래스로 대체) |
| hover 효과 | CSS `:hover` 선택자 | `hover:` 접두사 |
| 변경 방법 | CSS 파일에서 수정 | HTML 클래스만 수정 |

---

## 7️⃣ 정리

### Tailwind 핵심 클래스 치트시트

| 분류 | 클래스 예시 | CSS 대응 |
|------|-----------|---------|
| **여백** | `p-4`, `px-6`, `py-2`, `m-4`, `mx-auto` | padding, margin |
| **크기** | `w-full`, `h-screen`, `max-w-screen-xl` | width, height, max-width |
| **레이아웃** | `flex`, `grid`, `justify-center`, `items-center`, `gap-4` | flexbox, grid |
| **텍스트** | `text-xl`, `font-bold`, `text-center`, `leading-relaxed` | font, text-align |
| **색상** | `text-blue-500`, `bg-gray-100`, `border-gray-300` | color, background |
| **테두리** | `rounded-lg`, `rounded-full`, `border`, `shadow-md` | border-radius, box-shadow |
| **상태** | `hover:bg-blue-700`, `focus:ring-2`, `transition` | :hover, :focus |
| **위치** | `relative`, `absolute`, `fixed`, `sticky`, `z-10` | position, z-index |

### CSS ↔ Tailwind 대응 빠른 참고

```
padding: 1rem    →  p-4
margin: 0 auto   →  mx-auto
display: flex    →  flex
flex-direction: column  →  flex-col
justify-content: space-between  →  justify-between
align-items: center  →  items-center
font-size: 1.5rem   →  text-2xl
font-weight: bold   →  font-bold
color: blue   →  text-blue-500
background: white  →  bg-white
border-radius: 0.5rem  →  rounded-lg
box-shadow: ...  →  shadow-md
position: absolute  →  absolute
z-index: 50  →  z-50
overflow: hidden  →  overflow-hidden
```

### 다음 장 미리보기

02장에서는 **핵심 패턴**을 다룹니다.
- `position`, `z-index`로 요소 배치 제어
- `group-hover`, `peer`로 연관 요소 스타일링
- `transition`, `animate`로 부드러운 인터랙션 구현
- Tailwind 공식 문서를 활용하여 필요한 클래스를 찾는 방법

03장에서는 반응형 랜딩 페이지 프로젝트를 완성합니다.

### 실습 과제

**기본** — CSS 01장의 모든 스타일을 Tailwind 클래스로 교체하기
- 제목, 단락, 목록 스타일을 Tailwind 텍스트 클래스로
- 배경색, 여백을 bg-*, p-*, m-* 클래스로

**중급** — Tailwind로 내비게이션 바 + 카드 3개 레이아웃 만들기
- 내비게이션: `flex justify-between items-center` 구조
- 카드 3개: `flex gap-6` 또는 `grid grid-cols-3`

**심화** — hover + transition으로 인터랙티브한 카드 만들기
- 마우스 올리면 카드가 위로 이동 (`hover:-translate-y-2`)
- 그림자가 커지는 효과 (`hover:shadow-xl`)
- 색상이 부드럽게 전환 (`transition duration-300`)
