---
title: 15. TDD — 요구사항으로 테스트하고 AI가 구현한다
layout: default
parent: AI-Native JavaScript
nav_order: 16
permalink: /ai-native-js/tdd
---

# 15장. TDD — 요구사항으로 테스트하고 AI가 구현한다
{: .no_toc }

> **Phase 3**

> 🚀 **도전 챕터** — TDD의 개념을 이해하는 것이 목표입니다. 전체 실습은 수업 후에 천천히 해도 좋습니다.

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 완전 페어 프로그래밍**
>
> AI(Copilot)와 완전한 협업이 가능합니다.
>
> 내가 설계하고 AI가 구현합니다. 테스트로 검증합니다.
>
> "신뢰하되 검증한다(Trust but verify)"가 원칙입니다.

---

## 학습 목표

- TDD(테스트 주도 개발)의 Red-Green-Refactor 사이클을 설명할 수 있다
- 요구사항을 작성하면 AI가 테스트와 구현을 생성하는 워크플로우를 수행할 수 있다
- 14장에서 만든 tdd-agent를 활용할 수 있다

<a id="toc"></a>

## 진행 순서

1. [TDD란?](#part1) — "시험 문제를 먼저 만들기" 비유
2. [TDD 실습 1: 문자열 유틸리티](#part2) — 요구사항 → AI가 테스트+구현
3. [TDD 실습 2: 팁 계산기](#part3) — tdd-agent 활용
4. [실습 과제](#part4) — 기본 / 도전
5. [정리](#part5) — 핵심 요약 및 다음 장

---

<a id="part1"></a>

## 1. ⭐ **핵심** — TDD란? [↑](#toc)

> 강사와 함께 TDD의 개념을 알아봅시다

> 선생님이 시험 문제를 먼저 만들고, 학생이 공부해서 답을 쓰는 것처럼,
> 개발자가 테스트(시험 문제)를 먼저 만들고, AI가 코드(답)를 작성하게 하는 방법입니다.

### 일반 개발 vs TDD

```
일반 개발: 코드 먼저 → 나중에 테스트 (또는 테스트 안 함)
TDD:      테스트 먼저 → 코드를 나중에
```

순서가 반대라서 처음에는 이상하게 느껴질 수 있습니다. 하지만 테스트를 먼저 쓰면 무엇을 만들어야 하는지 명확해집니다.

### Red-Green-Refactor 사이클

TDD는 세 단계의 짧은 사이클을 반복합니다.

```
🔴 Red:       실패하는 테스트가 먼저 준비된다
              (아직 코드가 없으니 당연히 실패)

🟢 Green:     테스트를 통과하는 코드를 만든다
              (AI에게 맡깁니다!)

🔵 Refactor:  코드를 깔끔하게 정리한다
              (동작은 바꾸지 않고 코드 품질만 개선)
```

### 11장 워크플로우와의 관계

11장(ToDo 프로젝트)에서 이미 TDD의 핵심을 경험했습니다:

```
11장: 요구사항 작성 → AI가 테스트 생성 → AI가 구현 → 테스트 통과 확인
TDD:  요구사항 정의 → 테스트 준비(Red) → 구현(Green) → 리팩터링(Refactor)
```

같은 흐름입니다! TDD는 이것을 **더 짧은 사이클로 반복**하는 방법론입니다.

### 기존 방식 vs TDD + AI 방식

| | 기존 방식 | TDD + AI 방식 |
|--|---------|-------------|
| 순서 | 코드 → 테스트 | 테스트 → 코드 |
| 목표 명확도 | 모호할 수 있음 | 테스트가 명확한 목표 역할 |
| AI 활용 | 코드 생성 | 테스트 + 구현 모두 생성 |
| 검증 | 직접 실행해봄 | 테스트가 자동 검증 |

---

<a id="part2"></a>

## 2. 🚀 **도전** — TDD 실습 1: 문자열 유틸리티 [↑](#toc)

요구사항을 작성하고, AI가 테스트와 구현을 모두 생성하는 전체 사이클을 경험합니다.

### Step 1: 요구사항 작성

아래 요구사항을 직접 작성하세요.

> 💡 11장에서는 `requirements.md` 파일을, 16~17장에서는 `.github/copilot-instructions.md`를 사용합니다. TDD 미니 실습에서는 프롬프트에 요구사항을 직접 전달합니다.

```markdown
# 문자열 유틸리티 요구사항

## 기능
- capitalize(str): 첫 글자를 대문자로 변환
  - "hello" → "Hello"
  - 빈 문자열 → 빈 문자열
- truncate(str, maxLength): 글자 수 제한, 초과 시 "..." 추가
  - "안녕하세요 세계", 5 → "안녕하세요..."
  - 짧은 문자열은 그대로 반환
- slugify(str): 공백을 -로, 대문자를 소문자로 변환 (URL용)
  - "Hello World" → "hello-world"
  - 연속 공백은 -로 치환

## 제약 조건
- ESM export, Vitest 테스트
- 빈 문자열, null, undefined 입력 시 안전 처리

## 금지 사항
- 외부 라이브러리 금지
- var 금지
```

### Step 2: 🔴 Red — AI에게 테스트 생성 요청

```
아래 요구사항을 기반으로 tests/utils.test.js를 작성해줘.
각 함수별 정상 케이스 + 엣지 케이스(빈 문자열, null) 포함.

요구사항:
- capitalize(str): 첫 글자를 대문자로. "hello"→"Hello", 빈 문자열→빈 문자열
- truncate(str, maxLength): 초과 시 "..." 추가. 짧으면 그대로
- slugify(str): 공백→-, 대문자→소문자. "Hello World"→"hello-world"
- 빈 문자열, null, undefined 안전 처리
- ESM export, Vitest, var 금지
```

AI가 생성한 테스트를 **검토**하세요:
- 요구사항의 모든 기능이 테스트에 포함되어 있는가?
- 빈 문자열, null 등 엣지 케이스가 있는가?
- 누락된 항목이 있으면 요구사항을 보완한 뒤 AI에게 재생성 요청

테스트를 저장하고 실행합니다:

```bash
npx vitest --run
```

```
FAIL  tests/utils.test.js
  Cannot find module '../src/utils.js'
```

구현이 없으니 실패합니다. 이것이 🔴 **Red** 상태입니다.

### Step 3: 🟢 Green — AI에게 구현 요청

```
tests/utils.test.js의 모든 테스트를 통과하는 src/utils.js를 작성해줘.

#file:tests/utils.test.js

규칙:
- ESM export
- 빈 문자열/null 안전 처리
- 한국어 JSDoc 주석
```

```bash
npx vitest --run
```

모든 테스트가 통과하면 🟢 **Green** 상태입니다.

### Step 4: 🔵 Refactor — 코드 개선

AI에게 리팩터링을 요청합니다:

```
src/utils.js를 리뷰하고 개선해줘. 동작은 변경하지 말고 코드 품질만 개선.

#file:src/utils.js
#file:tests/utils.test.js
```

리팩터링 후 다시 테스트를 실행하여 통과 확인:

```bash
npx vitest --run
```

> **TDD 사이클 완료!**
> 요구사항 작성 → 🔴 AI가 테스트 생성 → 🟢 AI가 구현 → 🔵 AI가 리팩터링
> 학생은 각 단계에서 **검토**하는 역할입니다.

---

<a id="part3"></a>

## 3. 📖 **더 알아보기** — TDD 실습 2: 팁 계산기 (tdd-agent 활용) [↑](#toc)

14장에서 만든 `tdd-agent`를 활용해서 전체 사이클을 한 번에 실행해봅니다.

### Agent에게 요구사항 전달

```
@tdd-agent
레스토랑 팁 계산기를 만들어줘.

요구사항:
- calculateTip(amount, tipPercent): 팁 금액 계산
  - amount: 음식 금액, tipPercent: 팁 비율 (0-100)
  - 반환: 팁 금액 (소수점 반올림)
  - 음수 금액이나 100 초과 팁은 에러 처리
- splitBill(amount, tipPercent, people): 인원별 금액 계산
  - 반환: 1인당 금액 (음식+팁, 소수점 반올림)
  - 0명이면 에러 처리

기대 동작:
calculateTip(10000, 10)   → 1000
calculateTip(10000, 15)   → 1500
splitBill(30000, 10, 3)   → 11000
splitBill(30000, 10, 4)   → 8250
```

Agent가 자동으로 Red → Green → Refactor를 수행합니다.

### Agent 실행 결과 검토

Agent가 완료되면 확인할 것:
- 테스트가 요구사항을 모두 커버하는가?
- 에러 처리(음수 금액, 0명)가 포함되어 있는가?
- `npx vitest --run`으로 모든 테스트가 통과하는가?

> 💡 **핵심**: Agent는 TDD 사이클을 자동화합니다. 여러분은 **요구사항을 잘 작성하고, 결과를 검증**하는 데 집중합니다.

---

<a id="part4"></a>

## 4. 실습 과제 [↑](#toc)

### 기본 과제: TDD로 온도 변환기

요구사항을 작성하고 AI에게 TDD 사이클을 요청하세요.

**요구사항 힌트:**
- `celsiusToFahrenheit(celsius)`: 섭씨 → 화씨
- `fahrenheitToCelsius(fahrenheit)`: 화씨 → 섭씨
- 소수점 첫째 자리까지 반올림
- null/undefined 입력 시 에러 처리

### 도전 과제: tdd-agent로 장바구니 기능 구현 — 요구사항 추가 체험

14장에서 만든 `@tdd-agent`를 사용하세요. 이 과제의 핵심은 **처음 요구사항으로 TDD 사이클을 완료한 뒤, 새 요구사항을 추가하고 기존 테스트를 깨뜨리지 않으면서 확장하는 것**입니다.

**1단계 요구사항:**
- `addItem(cart, item)`: 장바구니에 상품 추가 (이름, 가격, 수량)
- `removeItem(cart, itemName)`: 이름으로 상품 제거
- `getTotal(cart)`: 전체 금액 합계 반환
- 빈 장바구니는 빈 배열, 금액은 0
- 원본 배열 불변성 유지

**2단계 — 요구사항 추가 (1단계 테스트 통과 후):**
- `applyDiscount(cart, percent)`: 전체 금액에서 할인 적용
- 할인율은 0~100 사이, 범위 밖이면 에러
- 기존 addItem, removeItem, getTotal **테스트가 깨지지 않아야** 한다

> 💡 이것이 실무 TDD의 핵심입니다 — 기존 기능을 보호하면서 새 기능을 추가하는 것.

---

<a id="part5"></a>

## 5. 정리 [↑](#toc)

### TDD + AI-Native 워크플로우

```
1. 요구사항 작성           ← 내가 설계
2. AI가 테스트 생성 (Red)   ← AI가 구현, 내가 검토
3. AI가 코드 구현 (Green)   ← AI가 구현, 테스트가 검증
4. AI가 리팩터링 (Refactor) ← AI가 개선, 테스트가 보호
```

### 12~15장 전체 흐름 정리

| 장 | 배운 것 | 역할 |
|----|--------|------|
| 12장 | Custom Instructions | AI에게 프로젝트 규칙 알려주기 |
| 13장 | Prompt Files | 반복 작업을 템플릿으로 자동화 |
| 14장 | Custom Agent | AI에게 전문가 역할 부여 |
| **15장** | **TDD** | **위 도구들을 활용한 개발 방법론** |

> 💡 12~14장은 **도구**, 15장은 **방법론**입니다. 도구를 배운 후 방법론을 익히면 실전 프로젝트에 바로 적용할 수 있습니다.

### 다음 장 미리보기

지금까지 배운 모든 것을 하나로 합칩니다. Custom Instructions, Prompt Files, Agent, TDD를 모두 활용해서 실제 외부 API와 연동하는 날씨 앱을 처음부터 완성합니다.

---

→ **다음 장**: [16. 통합 프로젝트 — 날씨 앱](/ai-native-js/weather-app)
