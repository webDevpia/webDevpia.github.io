---
nav_exclude: true
---

# 02장. CSS Flexbox

## 학습 목표

- Flexbox로 요소를 가로/세로로 정렬하고 카드 레이아웃을 만들 수 있다
- justify-content와 align-items의 차이를 이해하고 활용할 수 있다

## 진행 순서

1. Flexbox란? - flex 컨테이너와 아이템
2. 주축과 교차축 - flex-direction, 방향 이해
3. 정렬: justify-content와 align-items - 주축과 교차축 정렬
4. flex-wrap과 gap - 줄바꿈과 간격 조절
5. 실용 예제: 카드 레이아웃 - 실제 카드 레이아웃 구현
6. 정리 - 속성 요약 및 실습 과제

---

## 1️⃣ Flexbox란?

**Flexbox(Flexible Box Layout)**는 요소들을 가로 또는 세로 방향으로 정렬하고 배치하기 위한 CSS 레이아웃 시스템입니다.

### 선반 정리 비유

> **선반 위 물건 정렬**을 생각해 보세요.
> - **선반(컨테이너)**: 물건을 올려놓는 공간 → `display: flex`가 적용된 부모 요소
> - **물건(아이템)**: 선반 위에 올라가는 개별 물건 → 자식 요소들
>
> '가운데 정렬', '양쪽 균등 배치' 같은 규칙은 **선반(컨테이너)**에 지정합니다.

### flex 컨테이너와 flex 아이템

```html
<!-- 컨테이너 (부모) -->
<div class="container">
  <!-- 아이템 (자식) -->
  <div class="item">1</div>
  <div class="item">2</div>
  <div class="item">3</div>
</div>
```

```css
/* 부모에 display: flex 한 줄이면 시작! */
.container {
  display: flex;
}
```

### flex 적용 전/후 비교

**적용 전** — div는 기본값이 `block`이므로 세로로 쌓입니다.
```
┌──────────┐
│  아이템 1 │
└──────────┘
┌──────────┐
│  아이템 2 │
└──────────┘
┌──────────┐
│  아이템 3 │
└──────────┘
```

**적용 후** — `display: flex`를 적용하면 가로로 나란히 배치됩니다.
```
┌──────────┐ ┌──────────┐ ┌──────────┐
│  아이템 1 │ │  아이템 2 │ │  아이템 3 │
└──────────┘ └──────────┘ └──────────┘
```

---

## 2️⃣ 주축과 교차축

Flexbox에서는 두 개의 축이 있습니다.

- **주축(Main Axis)**: 아이템이 배치되는 방향
- **교차축(Cross Axis)**: 주축과 수직인 방향

> 주축은 **물건을 놓는 방향**, 교차축은 **그 수직 방향**입니다.

### flex-direction

`flex-direction`으로 주축 방향을 설정합니다.

```css
.container {
  display: flex;

  /* row: 가로 방향 (기본값) → 주축: 좌→우 */
  flex-direction: row;

  /* row-reverse: 가로 역방향 → 주축: 우→좌 */
  flex-direction: row-reverse;

  /* column: 세로 방향 → 주축: 위→아래 */
  flex-direction: column;

  /* column-reverse: 세로 역방향 → 주축: 아래→위 */
  flex-direction: column-reverse;
}
```

### 방향에 따른 축 변화

**flex-direction: row (기본)**
```
주축 →
┌──────────────────────────────────────┐
│  [아이템1]  [아이템2]  [아이템3]      │ ↕ 교차축
└──────────────────────────────────────┘
```

**flex-direction: column**
```
┌──────────────────────────┐  ↔ 교차축
│  [아이템1]               │
│  [아이템2]               │  ↕ 주축
│  [아이템3]               │
└──────────────────────────┘
```

---

## 3️⃣ 정렬: justify-content와 align-items

### justify-content — 주축 정렬

주축 방향(기본: 가로)으로 아이템을 정렬합니다.

```css
.container {
  display: flex;

  /* 시작점 정렬 (기본값) */
  justify-content: flex-start;

  /* 끝점 정렬 */
  justify-content: flex-end;

  /* 가운데 정렬 */
  justify-content: center;

  /* 양 끝에 배치, 아이템 사이 균등 간격 */
  justify-content: space-between;

  /* 모든 아이템 양쪽에 균등 간격 */
  justify-content: space-around;

  /* 모든 아이템 사이와 양 끝 간격 동일 */
  justify-content: space-evenly;
}
```

```
flex-start:    [1] [2] [3] _ _ _ _
flex-end:      _ _ _ _ [1] [2] [3]
center:        _ _ [1] [2] [3] _ _
space-between: [1] _ _ [2] _ _ [3]
space-around:  _ [1] _ _ [2] _ _ [3] _
space-evenly:  _ [1] _ [2] _ [3] _
```

### align-items — 교차축 정렬

교차축 방향(기본: 세로)으로 아이템을 정렬합니다.

```css
.container {
  display: flex;
  height: 200px; /* 교차축 정렬을 보려면 높이가 필요 */

  /* 교차축 시작점 정렬 */
  align-items: flex-start;

  /* 교차축 끝점 정렬 */
  align-items: flex-end;

  /* 교차축 가운데 정렬 */
  align-items: center;

  /* 교차축 전체를 채움 (기본값) */
  align-items: stretch;
}
```

### 핵심 조합: 완벽한 가운데 정렬

```css
.centered-box {
  display: flex;
  justify-content: center; /* 주축(가로) 가운데 */
  align-items: center;     /* 교차축(세로) 가운데 */
  height: 300px;
  background-color: #f0f4ff;
}
```

```html
<div class="centered-box">
  <p>완벽하게 가운데 정렬된 텍스트</p>
</div>
```

이 조합은 **히어로 섹션, 버튼, 카드 내용 정렬** 등 실무에서 매우 자주 사용됩니다.

---

## 4️⃣ flex-wrap과 gap

### flex-wrap — 줄바꿈

기본적으로 flex 아이템은 한 줄에 모두 배치되려 합니다. 화면이 좁아지면 아이템이 찌그러집니다. `flex-wrap: wrap`을 사용하면 공간이 부족할 때 자동으로 다음 줄로 넘어갑니다.

```css
.container {
  display: flex;

  /* 기본값: 한 줄에 모두 배치 (넘쳐도 한 줄 유지) */
  flex-wrap: nowrap;

  /* 공간 부족 시 다음 줄로 자동 이동 */
  flex-wrap: wrap;
}
```

```
flex-wrap: nowrap (화면이 좁을 때):
[아이템1][아이템2][아이템3][아이템4][아이템5] → 찌그러짐

flex-wrap: wrap (화면이 좁을 때):
[아이템1] [아이템2] [아이템3]
[아이템4] [아이템5]
```

### gap — 아이템 사이 간격

`margin` 대신 `gap`을 사용하면 아이템 사이 간격을 간편하게 설정할 수 있습니다.

```css
.container {
  display: flex;
  flex-wrap: wrap;

  /* 모든 방향 간격 동일 */
  gap: 16px;

  /* 행 간격 16px, 열 간격 24px */
  gap: 16px 24px;
}
```

`margin`을 사용하면 첫/마지막 요소에도 여백이 생겨 복잡해지지만, `gap`은 **아이템 사이에만** 간격을 적용합니다.

### 실습: 카드 3개를 한 줄에 배치

```html
<div class="card-container">
  <div class="card">카드 1</div>
  <div class="card">카드 2</div>
  <div class="card">카드 3</div>
  <div class="card">카드 4</div>
  <div class="card">카드 5</div>
</div>
```

```css
.card-container {
  display: flex;
  flex-wrap: wrap;  /* 화면이 좁으면 자동 줄바꿈 */
  gap: 16px;
}

.card {
  /* 3개가 한 줄에 배치되도록 너비 설정 */
  /* (100% - gap 2개) / 3개 = 약 31% */
  flex: 0 0 calc(33.33% - 11px);
  padding: 20px;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}
```

---

## 5️⃣ 실용 예제: 카드 레이아웃

3개의 카드를 Flexbox로 가로 배치하고, 카드 안에서도 Flexbox로 내용을 정렬하는 예제입니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>카드 레이아웃</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <section class="card-section">
    <h2 class="section-title">서비스 소개</h2>

    <div class="card-container">
      <!-- 카드 1 -->
      <article class="card">
        <div class="card-icon">🎨</div>
        <h3 class="card-title">디자인</h3>
        <p class="card-text">사용자 경험을 고려한 아름다운 디자인을 제공합니다.</p>
        <a href="#" class="card-link">더 알아보기</a>
      </article>

      <!-- 카드 2 -->
      <article class="card">
        <div class="card-icon">⚡</div>
        <h3 class="card-title">개발</h3>
        <p class="card-text">최신 기술로 빠르고 안정적인 웹 서비스를 구축합니다.</p>
        <a href="#" class="card-link">더 알아보기</a>
      </article>

      <!-- 카드 3 -->
      <article class="card">
        <div class="card-icon">📊</div>
        <h3 class="card-title">분석</h3>
        <p class="card-text">데이터 기반의 인사이트로 비즈니스 성장을 돕습니다.</p>
        <a href="#" class="card-link">더 알아보기</a>
      </article>
    </div>
  </section>
</body>
</html>
```

```css
/* style.css */
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Noto Sans KR', sans-serif;
  background-color: #f5f5f5;
  color: #333;
  padding: 40px 20px;
}

/* 섹션 */
.card-section {
  max-width: 1000px;
  margin: 0 auto; /* 가운데 정렬 */
}

.section-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 40px;
  color: #1a1a1a;
}

/* 카드 컨테이너 — Flexbox로 가로 배치 */
.card-container {
  display: flex;
  gap: 24px;
}

/* 카드 — Flexbox로 내용 세로 배치 */
.card {
  display: flex;
  flex-direction: column; /* 세로로 쌓기 */
  flex: 1;                /* 3개가 균등 분배 */
  padding: 32px 24px;
  background-color: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-4px); /* 호버 시 살짝 위로 */
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* 카드 아이콘 */
.card-icon {
  font-size: 2.5rem;
  margin-bottom: 16px;
}

/* 카드 제목 */
.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #1a1a1a;
}

/* 카드 본문 */
.card-text {
  font-size: 0.95rem;
  line-height: 1.7;
  color: #666;
  flex: 1; /* 남은 공간 채우기 → 버튼이 항상 아래에 위치 */
  margin-bottom: 20px;
}

/* 카드 링크 버튼 */
.card-link {
  display: inline-block;
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  text-align: center;
  transition: background-color 0.2s;
}

.card-link:hover {
  background-color: #2980b9;
}
```

**포인트**: 카드 안에서 `flex-direction: column`과 `flex: 1`을 카드 본문에 적용하면, 카드들의 높이가 달라도 버튼이 항상 카드 하단에 고정됩니다.

---

## 6️⃣ 정리

### Flexbox 속성 요약

| 속성 | 대상 | 설명 |
|------|------|------|
| `display: flex` | 컨테이너 | Flexbox 활성화 |
| `flex-direction` | 컨테이너 | 주축 방향 (row / column) |
| `justify-content` | 컨테이너 | 주축 정렬 |
| `align-items` | 컨테이너 | 교차축 정렬 |
| `flex-wrap` | 컨테이너 | 줄바꿈 여부 |
| `gap` | 컨테이너 | 아이템 사이 간격 |
| `flex` | 아이템 | 크기 비율 (flex-grow, flex-shrink, flex-basis 단축) |

### 자주 쓰는 조합

| 목적 | 코드 |
|------|------|
| 가로 나란히 배치 | `display: flex;` |
| 세로 나란히 배치 | `display: flex; flex-direction: column;` |
| 가운데 정렬 | `justify-content: center; align-items: center;` |
| 양쪽 끝 정렬 (내비게이션) | `justify-content: space-between;` |
| 균등 간격 카드 | `display: flex; flex-wrap: wrap; gap: 16px;` |

### 다음 장 미리보기

**03장 CSS 반응형 디자인** — 카드 레이아웃이 완성됐다면, 이제 **스마트폰에서는 1열, 데스크톱에서는 3열**로 자동으로 바뀌도록 만들어봅니다. 미디어 쿼리를 사용한 반응형 웹을 배웁니다.

### 실습 과제

**기본** — 3개의 카드를 가로로 나란히 배치하기
- `display: flex`와 `gap` 활용
- 카드 내용: 이미지, 제목, 설명, 버튼

**중급** — 내비게이션 바 만들기
- 로고는 왼쪽, 메뉴 링크는 오른쪽에 배치
- `justify-content: space-between` 활용
- 세로 가운데 정렬: `align-items: center`

**심화** — 사진 갤러리 (flex-wrap으로 4열 그리드처럼 배치)
- `flex-wrap: wrap` 활용
- 각 이미지의 `flex: 0 0 calc(25% - gap)` 설정
- 화면이 좁아지면 2열로 변경 (미디어 쿼리 예습)
