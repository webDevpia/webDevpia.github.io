---
title: 03. Tailwind 미니 프로젝트
layout: default
grand_parent: Language
parent: Tailwind CSS
nav_order: 3
permalink: /language/tailwind/project
---

# 03장. Tailwind 미니 프로젝트
{: .no_toc }

## 학습 목표

- Tailwind의 반응형 접두사(sm, md, lg)로 모바일/데스크톱 대응 페이지를 만들 수 있다
- HTML/CSS/Tailwind를 종합하여 완성도 있는 랜딩 페이지를 만들 수 있다

> **사전 준비:** 01장(Tailwind 시작하기)과 02장(핵심 패턴)을 완료한 상태에서 진행합니다.

<a id="toc"></a>

## 진행 순서

1. [Tailwind 반응형 디자인](#part1) — 미디어 쿼리를 한 줄로
2. [자주 쓰는 레이아웃 패턴](#part2) — 실무에서 반복되는 구조
3. [프로젝트 소개: 랜딩 페이지](#part3) — 완성 화면 미리보기
4. [단계별 구현](#part4) — 내비게이션부터 푸터까지
5. [전체 코드](#part5) — 복사해서 바로 실행
6. [정리 및 다음 단계](#part6) — 3일 총정리와 JavaScript로 넘어가기

---

<a id="part1"></a>

## 1️⃣ Tailwind 반응형 디자인 [↑](#toc)

CSS 03장에서 배운 **미디어 쿼리**를 Tailwind에서는 접두사로 처리합니다.

### 모바일 퍼스트 원칙

Tailwind는 **모바일 퍼스트(Mobile First)** 방식입니다.

- **접두사 없음** = 모든 화면 (모바일 포함)
- **`sm:`** = 640px 이상의 화면
- **`md:`** = 768px 이상의 화면
- **`lg:`** = 1024px 이상의 화면
- **`xl:`** = 1280px 이상의 화면
- **`2xl:`** = 1536px 이상의 화면

> **핵심 주의사항:** `sm:`은 '스몰에서만'이 아니라 **'스몰 이상 모두'에 적용**됩니다!
> `sm:text-lg`는 "640px 이상에서 text-lg를 적용"이지, "640px에서만"이 아닙니다.

### 브레이크포인트 표

| 접두사 | 최소 너비 | 해당 기기 |
|--------|----------|---------|
| (없음) | 0px | 모든 화면 (모바일) |
| `sm:` | 640px | 큰 모바일, 작은 태블릿 |
| `md:` | 768px | 태블릿 |
| `lg:` | 1024px | 노트북, 데스크톱 |
| `xl:` | 1280px | 큰 데스크톱 |
| `2xl:` | 1536px | 매우 큰 화면 |

### CSS 미디어 쿼리 vs Tailwind 반응형

**CSS 미디어 쿼리 방식 (3줄 + CSS 파일):**

```css
/* style.css */
.grid {
    display: grid;
    grid-template-columns: 1fr;          /* 모바일: 1열 */
}
@media (min-width: 768px) {
    .grid {
        grid-template-columns: repeat(2, 1fr);  /* 태블릿: 2열 */
    }
}
@media (min-width: 1024px) {
    .grid {
        grid-template-columns: repeat(4, 1fr);  /* 데스크톱: 4열 */
    }
}
```

**Tailwind 방식 (HTML 한 줄):**

```html
<!-- 모바일: 1열 / 태블릿: 2열 / 데스크톱: 4열 -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <!-- 카드들 -->
</div>
```

CSS 파일 없이 HTML 클래스 하나로 세 가지 화면 크기를 처리합니다.

### 반응형 텍스트 크기

```html
<!-- 모바일: 작게, 태블릿: 중간, 데스크톱: 크게 -->
<h1 class="text-2xl md:text-4xl lg:text-6xl font-bold">
    반응형 제목
</h1>

<!-- 모바일: 세로 배치, 데스크톱: 가로 배치 -->
<div class="flex flex-col md:flex-row gap-4">
    <div>왼쪽 콘텐츠</div>
    <div>오른쪽 콘텐츠</div>
</div>
```

CSS로 작성하면:
```css
h1 { font-size: 1.5rem; }
@media (min-width: 768px) { h1 { font-size: 2.25rem; } }
@media (min-width: 1024px) { h1 { font-size: 3.75rem; } }

.content { flex-direction: column; }
@media (min-width: 768px) { .content { flex-direction: row; } }
```

### 반응형 표시/숨기기

```html
<!-- 모바일에서는 숨기고, md 이상에서 표시 -->
<nav class="hidden md:flex gap-6">
    <a href="#">메뉴1</a>
    <a href="#">메뉴2</a>
</nav>

<!-- 모바일에서만 표시되는 햄버거 메뉴 버튼 -->
<button class="md:hidden p-2">
    ☰
</button>
```

---

<a id="part2"></a>

## 2️⃣ 자주 쓰는 Tailwind 레이아웃 패턴 [↑](#toc)

실무에서 반복적으로 사용하는 Tailwind 구조입니다. 외우기보다는 패턴을 익혀두면 됩니다.

### 가운데 정렬 컨테이너

```html
<!-- max-w-screen-xl: 최대 너비 1280px -->
<!-- mx-auto: 좌우 마진 auto = 가운데 정렬 -->
<!-- px-4: 좌우 여백 1rem (작은 화면에서 여백 확보) -->
<div class="max-w-screen-xl mx-auto px-4">
    페이지 내용
</div>
```

CSS 대응:
```css
.container {
    max-width: 1280px;
    margin-left: auto;
    margin-right: auto;
    padding-left: 1rem;
    padding-right: 1rem;
}
```

### 내비게이션 바

```html
<nav class="bg-white shadow-sm">
    <div class="max-w-screen-xl mx-auto px-4 py-4 flex justify-between items-center">
        <!-- 로고 -->
        <a href="#" class="text-xl font-bold text-blue-600">로고</a>

        <!-- 데스크톱 메뉴 (모바일에서 숨김) -->
        <div class="hidden md:flex gap-6">
            <a href="#" class="text-gray-600 hover:text-blue-600 transition">메뉴1</a>
            <a href="#" class="text-gray-600 hover:text-blue-600 transition">메뉴2</a>
            <a href="#" class="text-gray-600 hover:text-blue-600 transition">메뉴3</a>
        </div>

        <!-- 버튼 -->
        <button class="bg-blue-600 text-white px-4 py-2 rounded-lg
                       hover:bg-blue-700 transition duration-200">
            시작하기
        </button>
    </div>
</nav>
```

### 히어로 섹션

```html
<!-- min-h-screen: 최소 높이를 화면 전체로 -->
<!-- flex items-center justify-center: 내용을 화면 정중앙에 -->
<section class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="text-center px-4">
        <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            큰 제목입니다
        </h1>
        <p class="text-lg md:text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            부제목 설명 텍스트가 들어갑니다. 최대 너비를 제한해서 읽기 편하게 합니다.
        </p>
        <button class="bg-blue-600 text-white px-8 py-4 rounded-xl text-lg font-semibold
                       hover:bg-blue-700 transition duration-300 shadow-lg hover:shadow-xl">
            CTA 버튼
        </button>
    </div>
</section>
```

### 카드 그리드

```html
<!-- 모바일: 1열 / 태블릿: 2열(md:) / 데스크톱: 3열(lg:) -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition duration-300">
        카드 1
    </div>
    <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition duration-300">
        카드 2
    </div>
    <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition duration-300">
        카드 3
    </div>
</div>
```

### 폼(Form) 입력창

```html
<div class="space-y-4">
    <!-- space-y-4: 자식 요소 사이 상하 여백 1rem -->
    <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">이름</label>
        <input
            type="text"
            class="w-full border border-gray-300 rounded-lg px-4 py-2
                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                   transition duration-200"
            placeholder="홍길동"
        />
    </div>
    <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">이메일</label>
        <input
            type="email"
            class="w-full border border-gray-300 rounded-lg px-4 py-2
                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                   transition duration-200"
            placeholder="example@email.com"
        />
    </div>
</div>
```

### 푸터

```html
<footer class="bg-gray-800 text-white py-12">
    <div class="max-w-screen-xl mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
                <h3 class="font-bold text-lg mb-4">회사</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#" class="hover:text-white transition">소개</a></li>
                    <li><a href="#" class="hover:text-white transition">채용</a></li>
                </ul>
            </div>
            <div>
                <h3 class="font-bold text-lg mb-4">서비스</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#" class="hover:text-white transition">기능1</a></li>
                    <li><a href="#" class="hover:text-white transition">기능2</a></li>
                </ul>
            </div>
            <div>
                <h3 class="font-bold text-lg mb-4">연락처</h3>
                <p class="text-gray-400">contact@example.com</p>
            </div>
        </div>
        <div class="border-t border-gray-700 pt-8 text-center text-gray-400 text-sm">
            © 2025 회사명. All rights reserved.
        </div>
    </div>
</footer>
```

---

<a id="part3"></a>

## 3️⃣ 프로젝트 소개: 랜딩 페이지 [↑](#toc)

내비게이션, 히어로, 특징 카드, 연락처 폼, 푸터 5개 섹션으로 구성된 1페이지 랜딩 사이트를 만듭니다.

### 완성 화면 구조

```
+----------------------------------------------------------+
|  내비게이션 바                                             |
|  [로고]               [메뉴1 메뉴2 메뉴3]  [시작하기]      |
+----------------------------------------------------------+
|                                                          |
|                  히어로 섹션                               |
|            큰 제목 (텍스트 중앙 정렬)                      |
|          부제목 설명 텍스트 (연한 회색)                     |
|            [ 무료로 시작하기 ] 버튼                         |
|                                                          |
+----------------------------------------------------------+
|                                                          |
|  특징 카드 (모바일: 1열, 데스크톱: 3열)                     |
|  +--------------+ +--------------+ +--------------+      |
|  | 빠른 속도     | | 강력 보안     | | 스마트 AI    |      |
|  | 설명 텍스트   | | 설명 텍스트   | | 설명 텍스트   |      |
|  +--------------+ +--------------+ +--------------+      |
|                                                          |
+----------------------------------------------------------+
|                                                          |
|                  연락처 폼                                 |
|        이름 입력창  /  이메일 입력창                         |
|           메시지 텍스트에어리어                              |
|              [ 보내기 ] 버튼                                |
|                                                          |
+----------------------------------------------------------+
|  푸터                                                     |
|  [회사]  [서비스]  [연락처]  (3열)                          |
|  ----------------------------------------                |
|  (c) 2025 회사명. All rights reserved.                    |
+----------------------------------------------------------+
```

### 사용 기술 정리

| 섹션 | 사용 패턴 | 핵심 클래스 |
|------|----------|-----------|
| 내비게이션 | flex + justify-between | `flex justify-between items-center` |
| 히어로 | min-h-screen + 중앙 정렬 | `min-h-screen flex items-center justify-center` |
| 카드 그리드 | 반응형 grid | `grid grid-cols-1 md:grid-cols-3` |
| 연락처 폼 | 폼 스타일링 | `focus:ring-2 focus:ring-blue-500` |
| 푸터 | 어두운 배경 + grid | `bg-gray-800 grid md:grid-cols-3` |

---

<a id="part4"></a>

## 4️⃣ 단계별 구현 [↑](#toc)

### Step 1: 내비게이션 바

로고 + 데스크톱 메뉴(모바일 숨김) + CTA 버튼으로 구성합니다.

```html
<nav class="bg-white shadow-sm sticky top-0 z-50">
    <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">

            <!-- 로고 -->
            <a href="#" class="text-2xl font-bold text-blue-600">MyApp</a>

            <!-- 데스크톱 메뉴: md 이상에서만 표시 -->
            <div class="hidden md:flex items-center gap-8">
                <a href="#features" class="text-gray-600 hover:text-blue-600 transition duration-200">특징</a>
                <a href="#contact" class="text-gray-600 hover:text-blue-600 transition duration-200">연락처</a>
                <a href="#about" class="text-gray-600 hover:text-blue-600 transition duration-200">소개</a>
            </div>

            <!-- CTA 버튼 -->
            <button class="bg-blue-600 text-white px-5 py-2 rounded-lg font-medium
                           hover:bg-blue-700 transition duration-200 shadow-sm">
                무료로 시작하기
            </button>

        </div>
    </div>
</nav>
```

**순수 CSS 비교:**

```css
nav { background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 50; }
.nav-inner { max-width: 1280px; margin: 0 auto; padding: 0 1rem; display: flex; justify-content: space-between; align-items: center; height: 4rem; }
.nav-menu { display: none; }
@media (min-width: 768px) { .nav-menu { display: flex; gap: 2rem; } }
```

Tailwind는 `hidden md:flex`로 이를 2단어로 표현합니다.

> **이 코드에서 처음 등장하는 클래스:**
> - `sticky top-0`: 스크롤 시 화면 상단에 고정 (02장 Position 참조)
> - `z-50`: 다른 요소 위에 표시 (02장 Z-index 참조)
> - `backdrop-blur-sm`: 뒤 배경을 약간 흐리게 (유리 효과)

**브라우저에서 이렇게 보입니다:** 화면 상단에 좌측 'MyApp' 로고, 우측 '특징/연락처/소개' 메뉴가 가로로 배치됩니다. 스크롤하면 내비게이션이 상단에 고정됩니다(sticky).

### Step 2: 히어로 섹션

화면 전체를 채우는 배경에 텍스트와 버튼을 정중앙에 배치합니다.

```html
<section class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50
                flex items-center justify-center" id="hero">
    <div class="text-center px-4 max-w-4xl mx-auto">

        <!-- 배지 -->
        <span class="inline-block bg-blue-100 text-blue-700 text-sm font-medium
                     px-4 py-1.5 rounded-full mb-6">
            2025년 새로운 버전 출시 🎉
        </span>

        <!-- 메인 제목: 모바일(text-4xl) → 데스크톱(text-6xl) -->
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            더 빠르고 스마트한<br>
            <span class="text-blue-600">웹 경험</span>을 만드세요
        </h1>

        <!-- 부제목 -->
        <p class="text-lg md:text-xl text-gray-500 mb-10 max-w-2xl mx-auto leading-relaxed">
            Tailwind CSS로 아름다운 UI를 HTML 파일 하나로 완성하세요.
            복잡한 CSS 파일 없이도 전문적인 디자인이 가능합니다.
        </p>

        <!-- CTA 버튼 그룹 -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button class="bg-blue-600 text-white px-8 py-4 rounded-xl text-lg font-semibold
                           hover:bg-blue-700 transition duration-300 shadow-lg hover:shadow-xl
                           hover:-translate-y-0.5">
                무료로 시작하기
            </button>
            <button class="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl text-lg font-semibold
                           hover:border-blue-500 hover:text-blue-600 transition duration-300">
                데모 보기
            </button>
        </div>

    </div>
</section>
```

> **이 코드에서 처음 등장하는 클래스:**
> - `bg-gradient-to-br from-blue-50 via-white to-indigo-50`: 왼쪽 위→오른쪽 아래 방향 그라디언트
> - `min-h-screen`: 최소 높이를 화면 전체로
> - `inline-block`: 배지를 인라인 블록으로 (너비는 내용만큼)

**브라우저에서 이렇게 보입니다:** 파란~흰~보라 그라디언트 배경 위에 큰 흰 글씨로 제목과 부제목, '무료로 시작하기' 버튼이 중앙에 표시됩니다.

### Step 3: 특징 카드 3개

반응형 그리드로 모바일에서 1열, 데스크톱에서 3열이 됩니다.

```html
<section class="py-20 bg-white" id="features">
    <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">

        <!-- 섹션 헤더 -->
        <div class="text-center mb-16">
            <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">왜 선택해야 할까요?</h2>
            <p class="text-gray-500 text-lg max-w-xl mx-auto">세 가지 핵심 장점을 확인하세요.</p>
        </div>

        <!-- 카드 그리드: 모바일 1열, md 이상 3열 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">

            <!-- 카드 1 -->
            <div class="bg-gray-50 rounded-2xl p-8 text-center
                        transition duration-300 hover:shadow-xl hover:-translate-y-2 cursor-pointer">
                <div class="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center
                            mx-auto mb-6 text-3xl">
                    🚀
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3">빠른 속도</h3>
                <p class="text-gray-500 leading-relaxed">
                    사용한 클래스만 포함하는 빌드 최적화로 CSS 파일 크기가 매우 작아집니다.
                </p>
            </div>

            <!-- 카드 2 -->
            <div class="bg-gray-50 rounded-2xl p-8 text-center
                        transition duration-300 hover:shadow-xl hover:-translate-y-2 cursor-pointer">
                <div class="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center
                            mx-auto mb-6 text-3xl">
                    🔒
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3">강력한 보안</h3>
                <p class="text-gray-500 leading-relaxed">
                    검증된 오픈소스 프레임워크로, 수백만 개의 프로젝트에서 안전하게 사용됩니다.
                </p>
            </div>

            <!-- 카드 3 -->
            <div class="bg-gray-50 rounded-2xl p-8 text-center
                        transition duration-300 hover:shadow-xl hover:-translate-y-2 cursor-pointer">
                <div class="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center
                            mx-auto mb-6 text-3xl">
                    💡
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3">스마트 AI 지원</h3>
                <p class="text-gray-500 leading-relaxed">
                    GitHub Copilot, Claude 등 AI 도구와 완벽하게 호환되어 개발 속도가 2배 빨라집니다.
                </p>
            </div>

        </div>
    </div>
</section>
```

**브라우저에서 이렇게 보입니다:** 3개의 흰 카드가 가로로 나란히 배치됩니다. 각 카드에 마우스를 올리면 위로 살짝 떠오르는 효과가 있습니다. 모바일에서는 1열로 세로 배치됩니다.

### Step 4: 연락처 폼

```html
<section class="py-20 bg-gray-50" id="contact">
    <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="max-w-2xl mx-auto">

            <!-- 섹션 헤더 -->
            <div class="text-center mb-12">
                <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">연락하기</h2>
                <p class="text-gray-500 text-lg">문의사항이 있으시면 언제든지 연락주세요.</p>
            </div>

            <!-- 폼 -->
            <form class="bg-white rounded-2xl p-8 shadow-md space-y-6">

                <!-- 이름 + 이메일 (sm 이상에서 2열) -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">이름</label>
                        <input
                            type="text"
                            placeholder="홍길동"
                            class="w-full border border-gray-300 rounded-lg px-4 py-3
                                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                                   transition duration-200 text-gray-900 placeholder-gray-400"
                        />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">이메일</label>
                        <input
                            type="email"
                            placeholder="example@email.com"
                            class="w-full border border-gray-300 rounded-lg px-4 py-3
                                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                                   transition duration-200 text-gray-900 placeholder-gray-400"
                        />
                    </div>
                </div>

                <!-- 메시지 -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">메시지</label>
                    <textarea
                        rows="5"
                        placeholder="문의 내용을 입력해주세요..."
                        class="w-full border border-gray-300 rounded-lg px-4 py-3
                               focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                               transition duration-200 text-gray-900 placeholder-gray-400 resize-none"
                    ></textarea>
                </div>

                <!-- 제출 버튼 -->
                <button
                    type="submit"
                    class="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold text-lg
                           hover:bg-blue-700 transition duration-300 shadow-md hover:shadow-lg"
                >
                    보내기
                </button>

            </form>

        </div>
    </div>
</section>
```

> **이 코드에서 처음 등장하는 클래스:**
> - `space-y-6`: 자식 요소 사이에 1.5rem 간격 자동 추가
> - `focus:ring-2 focus:ring-blue-500`: 포커스 시 파란 링 표시 (02장 Ring 참조)
> - `resize-none`: textarea 크기 조절 비활성화
> - `placeholder-gray-400`: 빈 입력 필드의 안내 텍스트 색상

**브라우저에서 이렇게 보입니다:** 이름, 이메일, 메시지 입력 필드가 세로로 배치됩니다. 입력 필드를 클릭하면 파란 ring 효과가 나타납니다.

### Step 5: 푸터

```html
<footer class="bg-gray-900 text-white py-16">
    <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">

        <!-- 3열 그리드: 모바일 1열, md 이상 3열 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10 mb-12">

            <!-- 브랜드 소개 -->
            <div>
                <h3 class="text-2xl font-bold text-white mb-4">MyApp</h3>
                <p class="text-gray-400 leading-relaxed">
                    Tailwind CSS로 만든 아름다운 웹 경험.
                    HTML 파일 하나로 전문적인 UI를 완성하세요.
                </p>
            </div>

            <!-- 링크 -->
            <div>
                <h4 class="font-bold text-white mb-4">서비스</h4>
                <ul class="space-y-2">
                    <li><a href="#" class="text-gray-400 hover:text-white transition duration-200">기능 소개</a></li>
                    <li><a href="#" class="text-gray-400 hover:text-white transition duration-200">요금제</a></li>
                    <li><a href="#" class="text-gray-400 hover:text-white transition duration-200">사용 사례</a></li>
                    <li><a href="#" class="text-gray-400 hover:text-white transition duration-200">블로그</a></li>
                </ul>
            </div>

            <!-- 연락처 -->
            <div>
                <h4 class="font-bold text-white mb-4">연락처</h4>
                <ul class="space-y-2 text-gray-400">
                    <li>contact@myapp.com</li>
                    <li>서울특별시 강남구</li>
                    <li>월-금 09:00 ~ 18:00</li>
                </ul>
            </div>

        </div>

        <!-- 구분선 + 저작권 -->
        <div class="border-t border-gray-700 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <p class="text-gray-400 text-sm">© 2025 MyApp. All rights reserved.</p>
            <div class="flex gap-6 text-sm text-gray-400">
                <a href="#" class="hover:text-white transition">개인정보처리방침</a>
                <a href="#" class="hover:text-white transition">이용약관</a>
            </div>
        </div>

    </div>
</footer>
```

**브라우저에서 이렇게 보입니다:** 어두운 회색 배경에 흰 글씨로 MyApp 브랜드 소개, 서비스 링크, 연락처가 3열로 배치됩니다. 하단에 저작권 문구와 개인정보처리방침 링크가 중앙 정렬로 표시됩니다.

---

<a id="part5"></a>

## 5️⃣ 전체 코드 [↑](#toc)

아래 코드를 `landing.html`로 저장하고 Live Server로 열면 완성된 랜딩 페이지를 확인할 수 있습니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyApp - 더 빠르고 스마트한 웹 경험</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="font-sans antialiased">

    <!-- ============================
         1. 내비게이션 바
    ============================= -->
    <nav class="bg-white shadow-sm sticky top-0 z-50">
        <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <a href="#" class="text-2xl font-bold text-blue-600">MyApp</a>
                <div class="hidden md:flex items-center gap-8">
                    <a href="#features" class="text-gray-600 hover:text-blue-600 transition duration-200">특징</a>
                    <a href="#contact" class="text-gray-600 hover:text-blue-600 transition duration-200">연락처</a>
                    <a href="#about" class="text-gray-600 hover:text-blue-600 transition duration-200">소개</a>
                </div>
                <button class="bg-blue-600 text-white px-5 py-2 rounded-lg font-medium
                               hover:bg-blue-700 transition duration-200">
                    무료로 시작하기
                </button>
            </div>
        </div>
    </nav>

    <!-- ============================
         2. 히어로 섹션
    ============================= -->
    <section class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50
                    flex items-center justify-center">
        <div class="text-center px-4 max-w-4xl mx-auto">
            <span class="inline-block bg-blue-100 text-blue-700 text-sm font-medium
                         px-4 py-1.5 rounded-full mb-6">
                2025년 새로운 버전 출시 🎉
            </span>
            <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
                더 빠르고 스마트한<br>
                <span class="text-blue-600">웹 경험</span>을 만드세요
            </h1>
            <p class="text-lg md:text-xl text-gray-500 mb-10 max-w-2xl mx-auto leading-relaxed">
                Tailwind CSS로 아름다운 UI를 HTML 파일 하나로 완성하세요.
                복잡한 CSS 파일 없이도 전문적인 디자인이 가능합니다.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <button class="bg-blue-600 text-white px-8 py-4 rounded-xl text-lg font-semibold
                               hover:bg-blue-700 transition duration-300 shadow-lg hover:shadow-xl">
                    무료로 시작하기
                </button>
                <button class="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl text-lg font-semibold
                               hover:border-blue-500 hover:text-blue-600 transition duration-300">
                    데모 보기
                </button>
            </div>
        </div>
    </section>

    <!-- ============================
         3. 특징 카드 섹션
    ============================= -->
    <section class="py-20 bg-white" id="features">
        <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16">
                <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">왜 선택해야 할까요?</h2>
                <p class="text-gray-500 text-lg max-w-xl mx-auto">세 가지 핵심 장점을 확인하세요.</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="bg-gray-50 rounded-2xl p-8 text-center
                            transition duration-300 hover:shadow-xl hover:-translate-y-2 cursor-pointer">
                    <div class="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center
                                mx-auto mb-6 text-3xl">🚀</div>
                    <h3 class="text-xl font-bold text-gray-900 mb-3">빠른 속도</h3>
                    <p class="text-gray-500 leading-relaxed">
                        사용한 클래스만 포함하는 빌드 최적화로 CSS 파일 크기가 매우 작아집니다.
                    </p>
                </div>
                <div class="bg-gray-50 rounded-2xl p-8 text-center
                            transition duration-300 hover:shadow-xl hover:-translate-y-2 cursor-pointer">
                    <div class="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center
                                mx-auto mb-6 text-3xl">🔒</div>
                    <h3 class="text-xl font-bold text-gray-900 mb-3">강력한 보안</h3>
                    <p class="text-gray-500 leading-relaxed">
                        검증된 오픈소스 프레임워크로, 수백만 개의 프로젝트에서 안전하게 사용됩니다.
                    </p>
                </div>
                <div class="bg-gray-50 rounded-2xl p-8 text-center
                            transition duration-300 hover:shadow-xl hover:-translate-y-2 cursor-pointer">
                    <div class="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center
                                mx-auto mb-6 text-3xl">💡</div>
                    <h3 class="text-xl font-bold text-gray-900 mb-3">스마트 AI 지원</h3>
                    <p class="text-gray-500 leading-relaxed">
                        GitHub Copilot, Claude 등 AI 도구와 완벽하게 호환되어 개발 속도가 2배 빨라집니다.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- ============================
         4. 연락처 폼
    ============================= -->
    <section class="py-20 bg-gray-50" id="contact">
        <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="max-w-2xl mx-auto">
                <div class="text-center mb-12">
                    <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">연락하기</h2>
                    <p class="text-gray-500 text-lg">문의사항이 있으시면 언제든지 연락주세요.</p>
                </div>
                <form class="bg-white rounded-2xl p-8 shadow-md space-y-6">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">이름</label>
                            <input type="text" placeholder="홍길동"
                                class="w-full border border-gray-300 rounded-lg px-4 py-3
                                       focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                                       transition duration-200" />
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">이메일</label>
                            <input type="email" placeholder="example@email.com"
                                class="w-full border border-gray-300 rounded-lg px-4 py-3
                                       focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                                       transition duration-200" />
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">메시지</label>
                        <textarea rows="5" placeholder="문의 내용을 입력해주세요..."
                            class="w-full border border-gray-300 rounded-lg px-4 py-3
                                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                                   transition duration-200 resize-none"></textarea>
                    </div>
                    <button type="submit"
                        class="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold text-lg
                               hover:bg-blue-700 transition duration-300 shadow-md hover:shadow-lg">
                        보내기
                    </button>
                </form>
            </div>
        </div>
    </section>

    <!-- ============================
         5. 푸터
    ============================= -->
    <footer class="bg-gray-900 text-white py-16">
        <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 mb-12">
                <div>
                    <h3 class="text-2xl font-bold text-white mb-4">MyApp</h3>
                    <p class="text-gray-400 leading-relaxed">
                        Tailwind CSS로 만든 아름다운 웹 경험.
                        HTML 파일 하나로 전문적인 UI를 완성하세요.
                    </p>
                </div>
                <div>
                    <h4 class="font-bold text-white mb-4">서비스</h4>
                    <ul class="space-y-2">
                        <li><a href="#" class="text-gray-400 hover:text-white transition duration-200">기능 소개</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-white transition duration-200">요금제</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-white transition duration-200">사용 사례</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-white transition duration-200">블로그</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-bold text-white mb-4">연락처</h4>
                    <ul class="space-y-2 text-gray-400">
                        <li>contact@myapp.com</li>
                        <li>서울특별시 강남구</li>
                        <li>월-금 09:00 ~ 18:00</li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-700 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
                <p class="text-gray-400 text-sm">© 2025 MyApp. All rights reserved.</p>
                <div class="flex gap-6 text-sm text-gray-400">
                    <a href="#" class="hover:text-white transition">개인정보처리방침</a>
                    <a href="#" class="hover:text-white transition">이용약관</a>
                </div>
            </div>
        </div>
    </footer>

</body>
</html>
```

---

<a id="part6"></a>

## 6️⃣ 정리 및 다음 단계 [↑](#toc)

### HTML / CSS / Tailwind 3일 총정리

| Day | 주제 | 핵심 키워드 | 결과물 |
|-----|------|------------|--------|
| 1 | HTML | 태그, 구조, 시맨틱, 폼 | 포트폴리오 페이지 (구조만) |
| 2 | CSS | 선택자, 박스 모델, Flexbox, 반응형 | 반응형 포트폴리오 (스타일 완성) |
| 3 | Tailwind | 유틸리티 클래스, CSS 대응, 반응형 접두사 | 반응형 랜딩 페이지 (Tailwind) |

### 3일간의 성장 흐름

```
Day 1 (HTML만)        Day 2 (+ CSS)         Day 3 (+ Tailwind)
+--------------+    +--------------+     +-----------------+
| 심선조        |    | # 심선조      |     | * MyApp          |
|              |    | ------------ |     | ================|
| 안녕하세요    |    | 안녕하세요    |     |  멋진 서비스     |
| - 취미1      |    | [카드][카드]  |     | [카드][카드][카드]|
| - 취미2      |    |              |     |                 |
| 연락처       |    | (c) 2026     |     | [시작하기]       |
+--------------+    +--------------+     +-----------------+
  투박한 텍스트       색상+레이아웃        프로 수준 UI
```

### 이 랜딩 페이지에 사용된 3일간의 개념

| 랜딩 페이지 구성 | 사용된 기술 | 배운 날 |
|-----------------|------------|--------|
| `<header>`, `<nav>`, `<main>`, `<footer>` | HTML 시맨틱 태그 | Day 1 (HTML 02장) |
| `<input>`, `<button>`, `<form>` | HTML 폼 요소 | Day 1 (HTML 02장) |
| `flex`, `justify-between`, `items-center` | Flexbox 정렬 | Day 2 (CSS 02장) |
| `grid grid-cols-1 md:grid-cols-3` | 반응형 그리드 | Day 2 (CSS 03장) → Day 3 Tailwind 변환 |
| `bg-blue-600`, `text-white`, `rounded-lg` | Tailwind 유틸리티 | Day 3 (Tailwind 01장) |
| `hover:bg-blue-700`, `transition` | 상태 클래스 + 전환 | Day 3 (Tailwind 01장) |
| `md:grid-cols-3`, `lg:text-6xl` | Tailwind 반응형 접두사 | Day 3 (Tailwind 02장) |

### CSS ↔ Tailwind 반응형 최종 정리

```
/* CSS 미디어 쿼리 */              /* Tailwind 반응형 */
@media (min-width: 640px)  →   sm:
@media (min-width: 768px)  →   md:
@media (min-width: 1024px) →   lg:
@media (min-width: 1280px) →   xl:

/* 예시 */
@media (min-width: 768px) {         md:grid-cols-3
    .grid { grid-cols: 3; }
}
@media (min-width: 768px) {         md:hidden
    .mobile-menu { display: none; }
}
@media (min-width: 1024px) {        lg:text-6xl
    h1 { font-size: 3.75rem; }
}
```

### JavaScript로 넘어가기

이제 HTML로 **구조**를, CSS/Tailwind로 **스타일**을 만들 수 있습니다.

> 다음은 JavaScript로 **'동작'** 을 추가합니다!
> 버튼 클릭 → 팝업 열기, 데이터 가져오기, 화면 전환 등 웹페이지가 살아 움직이게 됩니다.

| 기술 | 역할 | 비유 |
|------|------|------|
| HTML | 구조와 내용 | 건물의 뼈대 |
| CSS / Tailwind | 시각적 스타일 | 건물의 외관 |
| **JavaScript** | 동작과 상호작용 | 엘리베이터, 자동문 |

### 실습 과제

**기본** — 랜딩 페이지의 색상을 자신이 좋아하는 색으로 변경하기
- `blue-600`을 모두 `green-600`으로 바꾸어 초록 테마 완성
- 히어로 배경 그라디언트도 함께 변경

**중급** — 카드 섹션을 4개로 늘리고 lg에서 4열 배치
- 카드 하나 추가: 내용은 자유롭게
- `grid-cols-1 md:grid-cols-2 lg:grid-cols-4`로 변경

**심화** — 다크모드 토글 구현 (Tailwind의 `dark:` 접두사 활용)
- `<html class="dark">` 추가 시 어두운 테마 적용
- `dark:bg-gray-900`, `dark:text-white` 등 dark 접두사 추가
- JavaScript 버튼으로 `document.documentElement.classList.toggle('dark')` 구현

**심화+** — CSS 03장의 포트폴리오를 Tailwind로 재구현하기
- CSS 03장(반응형 디자인)에서 만든 포트폴리오 HTML을 복사합니다
- `<link rel="stylesheet" href="style.css">`를 제거하고 `<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>`로 교체합니다
- `style.css`에 작성한 모든 CSS를 Tailwind 클래스로 변환합니다
- 01장의 **CSS ↔ Tailwind 대응표**를 참고하세요

> 💡 이 과제를 완료하면 **"같은 페이지를 순수 CSS와 Tailwind 두 가지 방식으로 만든 경험"**이 됩니다. 면접에서 "CSS와 Tailwind의 차이를 설명해주세요"라는 질문에 실제 경험을 바탕으로 답할 수 있습니다!
