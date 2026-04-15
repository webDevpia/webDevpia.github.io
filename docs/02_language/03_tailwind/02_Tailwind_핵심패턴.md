---
title: 02. Tailwind 핵심 패턴
layout: default
grand_parent: Language
parent: Tailwind CSS
nav_order: 2
permalink: /language/tailwind/patterns
---

# 02장. Tailwind 핵심 패턴
{: .no_toc }

## 학습 목표

- position, z-index, overflow 등 레이아웃 심화 클래스를 활용할 수 있다
- group hover, transition, 다크모드 등 인터랙티브 패턴을 적용할 수 있다
- Tailwind 공식 문서를 활용하여 필요한 클래스를 스스로 찾을 수 있다

> **사전 준비:** 01장에서 유틸리티 클래스 개념, Flexbox, 반응형 접두어(sm/md/lg)를 이해한 상태에서 진행합니다.

<a id="toc"></a>

## 진행 순서

1. [Position과 Z-index](#part1) — 무대 위 배우처럼 위치 제어
2. [Display와 Visibility](#part2) — 가구를 없애거나 투명 망토 씌우기
3. [테두리, 그림자, Ring](#part3) — 액자와 그림자로 요소 강조
4. [Group Hover와 Peer](#part4) — 부모가 반응하면 자식도 따라 반응
5. [Transition과 Animation](#part5) — 부드러운 움직임 만들기
6. [임의값과 공식 문서 활용](#part6) — 스케일 밖의 값, 문서 검색법
7. [정리](#part7) — 핵심 요약과 실습 과제

---

<a id="part1"></a>

## 1️⃣ Position과 Z-index [↑](#toc)

> **비유:** 무대 위의 배우와 조명
> - `relative` — "무대 위에서 자기 자리에 서 있는 배우"
> - `absolute` — "무대 위 특정 좌표로 이동한 배우 (기준점은 가장 가까운 relative 조상)"
> - `fixed` — "스크롤해도 움직이지 않는 관객석 안내판"
> - `sticky` — "스크롤하면 따라오다가 특정 위치에 붙는 자막"

### position 4종 비교표

| CSS 값 | Tailwind 클래스 | 기준점 | 스크롤 영향 |
|---|---|---|---|
| `position: relative` | `relative` | 자기 원래 자리 | 함께 스크롤 |
| `position: absolute` | `absolute` | 가장 가까운 `relative` 조상 | 함께 스크롤 |
| `position: fixed` | `fixed` | 뷰포트(화면) | 고정, 스크롤 무관 |
| `position: sticky` | `sticky` | 스크롤 컨테이너 | 임계점까지 함께, 이후 고정 |

### CSS vs Tailwind 대응

```css
/* CSS */
.nav { position: sticky; top: 0; z-index: 50; }
.badge { position: absolute; top: 8px; right: 8px; }
```

```html
<!-- Tailwind: CSS 속성을 클래스 이름으로 그대로 표현 -->
<nav class="sticky top-0 z-50">...</nav>
<span class="absolute top-2 right-2">...</span>
```

### 실용 예시 1: sticky 내비게이션

```html
<!-- 스크롤해도 상단에 고정되는 내비게이션 -->
<nav class="sticky top-0 z-50 bg-white shadow-md px-6 py-4">
  <div class="flex justify-between items-center">
    <span class="font-bold text-lg">Logo</span>
    <ul class="flex gap-6 text-gray-600">
      <li><a href="#" class="hover:text-blue-600">Home</a></li>
      <li><a href="#" class="hover:text-blue-600">About</a></li>
    </ul>
  </div>
</nav>
```

**브라우저에서 이렇게 보입니다:** 페이지를 아래로 스크롤하면 내비게이션이 화면 상단에 붙어 따라옵니다. `z-50`은 z-index: 50으로, 다른 요소들(z-10, z-20 등) 위에 렌더링되어 내용이 겹쳐도 내비게이션이 항상 앞에 표시됩니다.

### 실용 예시 2: 배지가 붙은 카드

```html
<!-- 카드 오른쪽 위에 "NEW" 배지 -->
<div class="relative w-64">
  <img src="product.jpg" class="rounded-lg w-full">
  <span class="absolute top-2 right-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">
    NEW
  </span>
</div>
```

**브라우저에서 이렇게 보입니다:** 이미지 오른쪽 상단 모서리에 빨간 원형 배지가 떠 있습니다. `relative`가 없으면 배지의 `absolute` 기준이 페이지 전체가 되어 카드에서 분리됩니다.

### z-index 레이어 순서

```html
<!-- 레이어가 겹칠 때 위에 표시할 요소에 더 높은 z-index를 부여 -->
<div class="relative z-10 bg-white">콘텐츠 (z-index: 10)</div>
<div class="relative z-20 bg-yellow-100">팝업 (z-index: 20)</div>
<div class="fixed z-50 bg-black/50">모달 오버레이 (z-index: 50)</div>
```

Tailwind의 z-index 스케일: `z-0`(0) · `z-10`(10) · `z-20`(20) · `z-30`(30) · `z-40`(40) · `z-50`(50) · `z-auto`

### overflow 제어

| 클래스 | CSS | 언제 사용 |
|---|---|---|
| `overflow-hidden` | `overflow: hidden` | 삐져나온 콘텐츠 자르기, 둥근 이미지 클리핑 |
| `overflow-auto` | `overflow: auto` | 내용이 많을 때만 스크롤바 표시 |
| `overflow-scroll` | `overflow: scroll` | 항상 스크롤바 표시 |
| `overflow-visible` | `overflow: visible` | 기본값, 삐져나와도 그대로 표시 |

```html
<!-- 카드 이미지를 둥글게 클리핑 — overflow-hidden이 없으면 모서리가 튀어나옴 -->
<div class="rounded-lg overflow-hidden w-64">
  <img src="photo.jpg" class="w-full scale-110">
</div>
```

**브라우저에서 이렇게 보입니다:** 이미지가 110%로 확대되어 있지만 카드 테두리 밖으로 나오는 부분은 잘려서 깔끔한 둥근 모서리가 유지됩니다.

---

<a id="part2"></a>

## 2️⃣ Display와 Visibility [↑](#toc)

> **비유:** 가구 치우기
> - `hidden` (`display: none`) — "가구를 방에서 완전히 내보낸 것" → 공간도 사라짐
> - `invisible` (`visibility: hidden`) — "가구에 투명 망토를 씌운 것" → 보이지 않지만 공간은 남음

### display 클래스 정리

| 클래스 | CSS | 특징 |
|---|---|---|
| `block` | `display: block` | 줄 전체 차지, 위아래 쌓임 |
| `inline` | `display: inline` | 텍스트 흐름대로, width/height 무시 |
| `inline-block` | `display: inline-block` | 줄 흐름 + width/height 설정 가능 |
| `flex` | `display: flex` | Flexbox 컨테이너 |
| `grid` | `display: grid` | Grid 컨테이너 |
| `hidden` | `display: none` | 화면에서 완전 제거, 공간 없음 |
| `invisible` | `visibility: hidden` | 투명, 공간은 유지 |

### hidden vs invisible 비교

```html
<!-- hidden: 공간 사라짐 -->
<div class="flex gap-4 items-center">
  <div class="w-16 h-16 bg-blue-500 rounded">A</div>
  <div class="hidden w-16 h-16 bg-red-500 rounded">B (사라짐)</div>
  <div class="w-16 h-16 bg-green-500 rounded">C</div>
</div>
<!-- 결과: A와 C가 붙어서 표시 -->

<!-- invisible: 공간 유지 -->
<div class="flex gap-4 items-center">
  <div class="w-16 h-16 bg-blue-500 rounded">A</div>
  <div class="invisible w-16 h-16 bg-red-500 rounded">B (투명)</div>
  <div class="w-16 h-16 bg-green-500 rounded">C</div>
</div>
<!-- 결과: A와 C 사이에 빈 공간이 유지됨 -->
```

**브라우저에서 이렇게 보입니다:** `hidden`에서는 B가 없는 것처럼 A-C가 붙고, `invisible`에서는 B 자리가 비어 A와 C 사이에 간격이 생깁니다.

### 반응형 숨기기

```html
<!-- 모바일에서 숨기고, md(768px) 이상에서 표시 -->
<aside class="hidden md:block w-64 bg-gray-50 p-6">
  사이드바 콘텐츠
</aside>

<!-- 모바일에서만 표시, md 이상에서 숨기기 -->
<button class="block md:hidden p-2">
  ☰ 메뉴
</button>
```

**브라우저에서 이렇게 보입니다:** 화면 너비가 768px 미만이면 사이드바가 사라지고 햄버거 메뉴 버튼이 나타납니다. 768px 이상이면 반대로 사이드바가 표시되고 버튼이 숨겨집니다.

```html
<!-- 실용 예시: 모바일 반응형 레이아웃 -->
<div class="flex">
  <!-- 사이드바: 모바일 숨김, 데스크톱 표시 -->
  <aside class="hidden lg:block w-64 shrink-0 border-r p-4">
    <nav class="space-y-2">
      <a href="#" class="block px-3 py-2 rounded hover:bg-gray-100">메뉴 1</a>
      <a href="#" class="block px-3 py-2 rounded hover:bg-gray-100">메뉴 2</a>
    </nav>
  </aside>
  <!-- 메인 콘텐츠: 항상 표시 -->
  <main class="flex-1 p-6">본문 내용</main>
</div>
```

---

<a id="part3"></a>

## 3️⃣ 테두리, 그림자, Ring [↑](#toc)

> **비유:** 액자
> - `border` — "액자 틀 (요소를 둘러싸는 선)"
> - `shadow` — "벽에 비친 그림자 (깊이감 표현)"
> - `ring` — "강조용 형광 테두리 (포커스 표시에 최적)"

### border: 테두리

```html
<!-- 두께: border(1px) / border-2(2px) / border-4(4px) / border-8(8px) -->
<!-- 색상: border-gray-200 / border-blue-500 / border-red-400 -->
<!-- 모서리: rounded-sm / rounded / rounded-lg / rounded-xl / rounded-full -->

<div class="border border-gray-200 rounded-lg p-4">기본 카드</div>
<div class="border-2 border-blue-500 rounded-xl p-4">강조 카드</div>
<div class="border-0">테두리 없음</div>
```

**브라우저에서 이렇게 보입니다:** 첫 번째 카드는 얇은 회색 테두리, 두 번째 카드는 두꺼운 파란 테두리와 더 둥근 모서리를 갖습니다.

### shadow: 그림자

```html
<!-- 그림자 크기: sm → 기본 → md → lg → xl → 2xl -->
<div class="shadow-sm p-4 rounded-lg">작은 그림자</div>
<div class="shadow p-4 rounded-lg">기본 그림자</div>
<div class="shadow-md p-4 rounded-lg">중간 그림자</div>
<div class="shadow-lg p-4 rounded-lg">큰 그림자</div>
<div class="shadow-xl p-4 rounded-lg">더 큰 그림자</div>
<div class="shadow-none p-4 rounded-lg border">그림자 없음</div>
```

**브라우저에서 이렇게 보입니다:** `shadow-sm`은 살짝 띄워진 느낌, `shadow-xl`은 카드가 페이지 위로 높이 떠 있는 것처럼 깊은 그림자가 생깁니다.

### ring: 포커스 테두리

**`ring`** 은 `box-shadow`를 이용해 테두리 *바깥*에 그리는 강조선입니다. `border`와 달리 레이아웃 크기에 영향을 주지 않아 포커스 표시에 주로 사용합니다.

```html
<!-- 포커스 시 ring이 나타나는 input 필드 -->
<input
  type="email"
  placeholder="이메일 주소"
  class="border border-gray-300 rounded-lg px-4 py-2
         focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
         w-full"
>
```

**브라우저에서 이렇게 보입니다:** 평소에는 회색 테두리만 있다가, 클릭해서 포커스가 생기면 파란색 2px ring이 테두리 바깥을 감쌉니다. `outline-none`으로 브라우저 기본 아웃라인을 제거하고 ring으로 대체한 패턴입니다.

### border vs outline vs ring 차이

| 속성 | Tailwind | 위치 | 레이아웃 영향 | 주 용도 |
|---|---|---|---|---|
| `border` | `border` | 테두리 안쪽 | 있음 (박스 크기에 포함) | 카드, 입력 필드 외곽선 |
| `outline` | `outline` | 테두리 바깥 | 없음 | 브라우저 기본 포커스 |
| `ring` | `ring-{n}` | 테두리 바깥 | 없음 | 커스텀 포커스 강조 |

---

<a id="part4"></a>

## 4️⃣ Group Hover와 Peer [↑](#toc)

> **비유:** 부모가 손님을 맞으면 자식이 인사하는 것
> - `group` + `group-hover:` — 부모 요소에 마우스가 올라가면 자식 요소의 스타일이 바뀜
> - `peer` + `peer-focus:` — 형제 요소에 이벤트가 발생하면 다른 형제 요소가 반응함

### group + group-hover

```html
<!-- 카드에 hover하면 제목과 설명 색상이 함께 변경 -->
<div class="group bg-white rounded-lg p-6 hover:bg-blue-50 transition cursor-pointer shadow">
  <h3 class="text-gray-800 group-hover:text-blue-600 font-semibold text-lg">
    Tailwind 핵심 패턴
  </h3>
  <p class="text-gray-500 group-hover:text-blue-400 mt-2 text-sm">
    레이아웃 심화 클래스부터 인터랙티브 패턴까지 알아봅니다.
  </p>
  <span class="inline-block mt-4 text-sm text-gray-400 group-hover:text-blue-500 group-hover:translate-x-1 transition">
    더 보기 →
  </span>
</div>
```

**브라우저에서 이렇게 보입니다:** 카드에 마우스를 올리면 배경이 파란빛으로 변하고, 제목·설명·화살표가 동시에 파란색으로 바뀝니다. 부모 div 하나에만 마우스를 올렸을 뿐인데 세 자식 요소가 함께 반응합니다.

**CSS 없이 JavaScript 없이** 이 효과를 구현할 수 있다는 점이 Tailwind `group` 패턴의 핵심입니다.

### peer + peer-focus

**`peer`** 는 HTML에서 형제 요소(같은 부모의 자식)를 연결합니다. 먼저 오는 형제에 `peer`를 붙이고, 뒤에 오는 형제에서 `peer-focus:`, `peer-checked:` 등으로 반응합니다.

```html
<!-- input에 포커스가 생기면 안내 문구가 나타남 -->
<div class="space-y-1">
  <input
    type="email"
    class="peer border border-gray-300 rounded-lg px-3 py-2 w-full
           focus:outline-none focus:ring-2 focus:ring-blue-500"
    placeholder="이메일"
  >
  <!-- peer보다 뒤에 위치해야 CSS 선택자가 작동함 -->
  <p class="hidden peer-focus:block text-sm text-blue-500">
    이메일 주소를 입력하세요
  </p>
</div>
```

**브라우저에서 이렇게 보입니다:** input을 클릭하기 전에는 안내 문구가 숨겨져 있다가, 클릭해서 포커스가 생기는 순간 파란 안내 문구가 아래에 나타납니다.

> **주의:** `peer`와 `peer-*:` 클래스는 **HTML 순서**가 중요합니다. `peer`가 먼저, 반응하는 요소가 나중에 와야 합니다. CSS의 형제 선택자(`~`) 방향이 앞→뒤이기 때문입니다.

---

<a id="part5"></a>

## 5️⃣ Transition과 Animation [↑](#toc)

### transition: 부드러운 상태 전환

```html
<!-- transition 없음 → 색이 즉시 바뀜 -->
<button class="bg-blue-500 hover:bg-blue-700 text-white px-4 py-2 rounded">
  즉시 변경
</button>

<!-- transition 있음 → 0.3초 동안 부드럽게 전환 -->
<button class="bg-blue-500 hover:bg-blue-700 text-white px-4 py-2 rounded
               transition duration-300">
  부드러운 변경
</button>
```

**브라우저에서 이렇게 보입니다:** 첫 번째 버튼은 마우스를 올리면 색이 즉시 바뀌고, 두 번째 버튼은 300ms 동안 서서히 진해집니다.

### 속성 지정 transition

```html
<!-- transition: 모든 속성을 부드럽게 (성능 부담 있음) -->
<div class="transition-all duration-300">...</div>

<!-- transition-colors: 색상 관련만 (배경, 텍스트, 테두리) -->
<div class="transition-colors duration-200">...</div>

<!-- transition-transform: 이동/크기/회전만 (GPU 가속, 성능 좋음) -->
<div class="transition-transform duration-300">...</div>
```

### 이징 함수 (easing)

| 클래스 | CSS | 느낌 |
|---|---|---|
| `ease-linear` | `linear` | 일정한 속도 |
| `ease-in` | `ease-in` | 천천히 시작, 빠르게 끝 |
| `ease-out` | `ease-out` | 빠르게 시작, 천천히 끝 (자연스러운 감속) |
| `ease-in-out` | `ease-in-out` | 천천히 시작, 중간에 빠르고, 천천히 끝 |

### transform: 이동과 확대

```html
<!-- hover 시 1.05배 확대 -->
<div class="transition-transform duration-300 hover:scale-105">...</div>

<!-- hover 시 위로 4px 이동 (떠오르는 카드 효과) -->
<div class="transition-transform duration-300 hover:-translate-y-1">...</div>

<!-- 두 효과 조합 -->
<div class="transition-all duration-300 hover:scale-105 hover:-translate-y-1 hover:shadow-xl
            bg-white rounded-lg p-6 shadow cursor-pointer">
  인터랙티브 카드
</div>
```

**브라우저에서 이렇게 보입니다:** 카드에 마우스를 올리면 5% 커지면서 4px 위로 떠오르고 그림자도 깊어집니다. 마우스를 내리면 원래 위치로 부드럽게 돌아옵니다.

### 내장 애니메이션

Tailwind는 자주 쓰는 애니메이션 4종을 제공합니다.

```html
<!-- animate-spin: 360도 계속 회전 (로딩 스피너) -->
<div class="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full">
</div>

<!-- animate-ping: 퍼지는 효과 (알림 뱃지) -->
<span class="relative flex h-3 w-3">
  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
  <span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
</span>

<!-- animate-pulse: 밝아졌다 어두워지기 반복 (스켈레톤 로딩) -->
<div class="animate-pulse flex space-x-4">
  <div class="rounded-full bg-gray-200 h-12 w-12"></div>
  <div class="flex-1 space-y-3 py-1">
    <div class="h-3 bg-gray-200 rounded w-3/4"></div>
    <div class="h-3 bg-gray-200 rounded w-1/2"></div>
  </div>
</div>

<!-- animate-bounce: 위아래 튕기기 (스크롤 유도 화살표) -->
<div class="animate-bounce text-2xl">↓</div>
```

**브라우저에서 이렇게 보입니다:**
- `animate-spin`: 파란 원형 스피너가 계속 돌아갑니다.
- `animate-ping`: 빨간 점 주변에 파동이 퍼져나갑니다.
- `animate-pulse`: 회색 블록들이 서서히 밝아졌다 어두워지며 콘텐츠 로딩 중임을 표시합니다.
- `animate-bounce`: 화살표가 위아래로 통통 튀어 스크롤을 유도합니다.

---

<a id="part6"></a>

## 6️⃣ 임의값과 공식 문서 활용 [↑](#toc)

### 임의값 (Arbitrary Values)

Tailwind의 스케일에 없는 정확한 값이 필요할 때 `[값]` 형태로 직접 지정합니다.

```html
<!-- w-[200px]: 정확히 200px 너비 -->
<div class="w-[200px]">정확한 너비</div>

<!-- bg-[#1da1f2]: 트위터 브랜드 컬러 -->
<button class="bg-[#1da1f2] text-white px-4 py-2 rounded">
  Twitter 색상
</button>

<!-- text-[22px]: 스케일에 없는 폰트 크기 -->
<p class="text-[22px] leading-[1.8]">커스텀 텍스트 크기</p>

<!-- grid-cols-[200px_1fr_200px]: 사이드바-메인-사이드바 레이아웃 -->
<div class="grid grid-cols-[200px_1fr_200px] gap-4">
  <aside>왼쪽 사이드바</aside>
  <main>메인 콘텐츠</main>
  <aside>오른쪽 사이드바</aside>
</div>
```

> **임의값 사용 원칙:** 스케일에 없는 정확한 값이 필요할 때만 사용하세요. 남용하면 Tailwind의 디자인 일관성이 깨지고 코드 가독성도 떨어집니다. `w-64`(256px)가 충분하면 `w-[256px]`은 쓰지 않는 것이 좋습니다.

### Tailwind v4 주요 변경사항

수업에서 CDN 방식으로 사용하므로 이 내용은 참고 수준으로 이해합니다.

| 항목 | v3 | v4 |
|---|---|---|
| 설정 파일 | `tailwind.config.js` | CSS 내 `@theme` 지시어 |
| 초기화 | `@tailwind base/components/utilities` 3줄 | `@import "tailwindcss"` 1줄 |
| 빌드 엔진 | Node.js | Rust 기반 (5~100배 빠름) |
| CDN | 별도 설치 필요 | `<script src="cdn.tailwindcss.com">` 1줄 |

```html
<!-- v4 CDN 사용 (수업 방식) — 설정 파일 불필요 -->
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  <div class="bg-blue-500 text-white p-4">v4 CDN으로 바로 사용</div>
</body>
</html>
```

### 공식 문서 활용법

**공식 문서:** [https://tailwindcss.com](https://tailwindcss.com)

```
활용 방법:
1. 사이트 상단 검색창에 CSS 속성명 입력
   예: "padding" 검색 → p-1, p-2, pt-4, px-6 등 모든 패딩 클래스 확인

2. 각 클래스 옆에 실제 CSS 출력값이 표시됨
   예: p-6 → padding: 1.5rem

3. 예시 코드와 인터랙티브 미리보기 제공
```

**DevTools로 Tailwind 클래스 확인하기:**

```
1. 브라우저에서 F12 (또는 Command+Option+I) → DevTools 열기
2. Elements 탭에서 HTML 요소 클릭
3. Styles 패널에서 각 Tailwind 클래스가 어떤 CSS로 변환되었는지 확인 가능

예시: class="p-6 bg-blue-500" 요소를 클릭하면
  .p-6 { padding: 1.5rem; }
  .bg-blue-500 { background-color: rgb(59 130 246); }
  이 표시됨
```

이 방법을 활용하면 "이 클래스가 정확히 어떤 CSS인지" 항상 검증할 수 있습니다.

---

<a id="part7"></a>

## 7️⃣ 정리 [↑](#toc)

### 핵심 패턴 요약

| 개념 | 대표 Tailwind 클래스 | 비유 |
|---|---|---|
| sticky 헤더 | `sticky top-0 z-50` | 스크롤해도 따라오는 자막 |
| 오버레이 배지 | `relative` + `absolute top-2 right-2` | 액자 위에 붙인 스티커 |
| 요소 숨기기 | `hidden` / `invisible` | 가구 없애기 / 투명 망토 |
| 반응형 숨기기 | `hidden md:block` | 화면 크기에 따라 보이기/숨기기 |
| 포커스 ring | `focus:ring-2 focus:ring-blue-500` | 형광 테두리 강조 |
| 그룹 hover | `group` + `group-hover:text-blue-600` | 부모 hover → 자식 반응 |
| peer 연동 | `peer` + `peer-focus:block` | 형제 포커스 → 다른 형제 반응 |
| 부드러운 전환 | `transition duration-300` | 즉시 → 서서히 변화 |
| 카드 떠오름 | `hover:scale-105 hover:-translate-y-1` | 마우스 오면 카드가 뜨는 효과 |
| 로딩 스피너 | `animate-spin` | 계속 도는 원형 아이콘 |
| 스켈레톤 UI | `animate-pulse` | 밝아졌다 어두워지며 로딩 표시 |
| 임의값 | `w-[200px]` `bg-[#1da1f2]` | 스케일 밖의 정확한 값 |

### 다음 장 미리보기

**03장: 미니 프로젝트** — 지금까지 배운 모든 패턴을 활용해 실제 페이지를 만들어 봅니다.
- 반응형 랜딩 페이지 (Hero 섹션 + 카드 그리드 + 푸터)
- sticky 내비게이션 + 모바일 메뉴 토글
- group-hover 카드 + 로딩 스켈레톤 UI

---

### 실습 과제

#### 기본: sticky 내비게이션 + absolute 배지

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen">
  <!-- sticky 내비게이션 -->
  <nav class="sticky top-0 z-50 bg-white shadow-md px-6 py-4 flex justify-between items-center">
    <span class="font-bold text-xl">MyShop</span>
    <div class="flex gap-4 text-gray-600">
      <a href="#" class="hover:text-blue-600 transition-colors">홈</a>
      <a href="#" class="hover:text-blue-600 transition-colors">상품</a>
      <a href="#" class="hover:text-blue-600 transition-colors">장바구니</a>
    </div>
  </nav>

  <!-- 배지가 붙은 상품 카드 -->
  <div class="p-8">
    <div class="relative w-48">
      <div class="bg-gray-200 h-48 rounded-lg flex items-center justify-center text-gray-500">
        상품 이미지
      </div>
      <span class="absolute top-2 right-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">
        NEW
      </span>
    </div>
  </div>

  <!-- 스크롤 테스트용 공간 -->
  <div class="h-screen bg-gray-50 flex items-center justify-center text-gray-400">
    스크롤하면 내비게이션이 상단에 고정됩니다
  </div>
</body>
</html>
```

#### 중급: group-hover로 카드 3개 인터랙티브 효과 구현

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="p-8 bg-gray-100 min-h-screen">
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <!-- 카드 1 -->
    <div class="group bg-white rounded-xl p-6 shadow transition-all duration-300
                hover:shadow-xl hover:-translate-y-1 cursor-pointer">
      <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4
                  group-hover:bg-blue-500 transition-colors duration-300">
        <span class="text-blue-600 group-hover:text-white text-xl transition-colors duration-300">📘</span>
      </div>
      <h3 class="font-bold text-gray-800 group-hover:text-blue-600 transition-colors duration-300">
        학습 자료
      </h3>
      <p class="text-gray-500 text-sm mt-2 group-hover:text-gray-600 transition-colors duration-300">
        Tailwind CSS 핵심 패턴 모음
      </p>
      <span class="inline-block mt-4 text-blue-500 text-sm font-medium opacity-0 group-hover:opacity-100
                   transition-opacity duration-300">
        자세히 보기 →
      </span>
    </div>

    <!-- 카드 2, 3은 동일 구조로 색상만 변경 (green, purple) -->
    <div class="group bg-white rounded-xl p-6 shadow transition-all duration-300
                hover:shadow-xl hover:-translate-y-1 cursor-pointer">
      <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4
                  group-hover:bg-green-500 transition-colors duration-300">
        <span class="text-green-600 group-hover:text-white text-xl transition-colors duration-300">📗</span>
      </div>
      <h3 class="font-bold text-gray-800 group-hover:text-green-600 transition-colors duration-300">실습 과제</h3>
      <p class="text-gray-500 text-sm mt-2">직접 만들어보는 미니 프로젝트</p>
      <span class="inline-block mt-4 text-green-500 text-sm font-medium opacity-0 group-hover:opacity-100
                   transition-opacity duration-300">자세히 보기 →</span>
    </div>

    <div class="group bg-white rounded-xl p-6 shadow transition-all duration-300
                hover:shadow-xl hover:-translate-y-1 cursor-pointer">
      <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4
                  group-hover:bg-purple-500 transition-colors duration-300">
        <span class="text-purple-600 group-hover:text-white text-xl transition-colors duration-300">📙</span>
      </div>
      <h3 class="font-bold text-gray-800 group-hover:text-purple-600 transition-colors duration-300">참고 문서</h3>
      <p class="text-gray-500 text-sm mt-2">Tailwind 공식 문서 바로가기</p>
      <span class="inline-block mt-4 text-purple-500 text-sm font-medium opacity-0 group-hover:opacity-100
                   transition-opacity duration-300">자세히 보기 →</span>
    </div>
  </div>
</body>
</html>
```

#### 심화: animate-pulse로 로딩 스켈레톤 UI 만들기

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="p-8 bg-gray-50">
  <p class="text-gray-500 text-sm mb-4">콘텐츠를 불러오는 동안 표시되는 스켈레톤 UI</p>

  <div class="space-y-4">
    <!-- 스켈레톤 카드 반복 -->
    <div class="bg-white rounded-xl p-5 shadow flex gap-4 animate-pulse">
      <!-- 아바타 자리 -->
      <div class="rounded-full bg-gray-200 h-12 w-12 shrink-0"></div>
      <!-- 텍스트 자리 -->
      <div class="flex-1 space-y-3 py-1">
        <div class="h-3 bg-gray-200 rounded w-1/3"></div>
        <div class="h-3 bg-gray-200 rounded w-3/4"></div>
        <div class="h-3 bg-gray-200 rounded w-1/2"></div>
      </div>
    </div>

    <div class="bg-white rounded-xl p-5 shadow flex gap-4 animate-pulse">
      <div class="rounded-full bg-gray-200 h-12 w-12 shrink-0"></div>
      <div class="flex-1 space-y-3 py-1">
        <div class="h-3 bg-gray-200 rounded w-2/5"></div>
        <div class="h-3 bg-gray-200 rounded w-4/5"></div>
        <div class="h-3 bg-gray-200 rounded w-2/3"></div>
      </div>
    </div>

    <div class="bg-white rounded-xl p-5 shadow flex gap-4 animate-pulse">
      <div class="rounded-full bg-gray-200 h-12 w-12 shrink-0"></div>
      <div class="flex-1 space-y-3 py-1">
        <div class="h-3 bg-gray-200 rounded w-1/4"></div>
        <div class="h-3 bg-gray-200 rounded w-2/3"></div>
        <div class="h-3 bg-gray-200 rounded w-1/3"></div>
      </div>
    </div>
  </div>
</body>
</html>
```

**브라우저에서 이렇게 보입니다:** 아바타와 텍스트 자리가 회색 블록으로 표시되며 서서히 밝아졌다 어두워지기를 반복합니다. 실제 콘텐츠가 로드되기 전 SNS 피드, 상품 목록 등에서 자주 볼 수 있는 패턴입니다.
