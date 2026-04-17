---
title: 14. TDD + AI 에이전트
layout: default
parent: AI-Native JavaScript
nav_order: 15
permalink: /ai-native-js/tdd-agent
---

# 14장. TDD + AI 에이전트 — 테스트 먼저, 코드는 AI가
{: .no_toc }

> **Day 4** · Phase 3 · 예상 시간: 40분 (시간 여유 시)

> 🚀 **도전 챕터** — TDD의 개념을 이해하는 것이 목표입니다. 전체 실습은 수업 후에 천천히 해도 좋습니다.

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 완전 페어 프로그래밍**
> AI(Copilot)와 완전한 협업이 가능합니다.
> 내가 설계하고 AI가 구현합니다. 테스트로 검증합니다.
> "신뢰하되 검증한다(Trust but verify)"가 원칙입니다.

## 학습 목표

- TDD(테스트 주도 개발)의 Red-Green-Refactor 사이클을 설명할 수 있다
- 테스트를 먼저 작성하고 AI에게 구현을 맡길 수 있다
- Custom Agent 파일을 만들 수 있다

<a id="toc"></a>

## 진행 순서

1. [TDD란?](#part1) — "시험 문제를 먼저 만들기" 비유
2. [TDD 실습 1: 문자열 유틸리티](#part2) — Red-Green-Refactor 첫 경험
3. [TDD 실습 2: 장바구니 기능](#part3) — 복잡한 로직에 TDD 적용
4. [Custom Agent란?](#part4) — 전문가 역할 부여하기
5. [Agent 사용하기](#part5) — 실전 워크플로우
6. [실습 과제](#part6) — 기본 / 도전
7. [정리](#part7) — 핵심 요약 및 다음 장

---

<a id="part1"></a>

## 1️⃣ ⭐ **핵심** — TDD란? [↑](#toc)

> 강사와 함께 TDD의 개념을 알아봅시다

> 선생님이 시험 문제를 먼저 만들고, 학생이 공부해서 답을 쓰는 것처럼,
> 개발자가 테스트(시험 문제)를 먼저 만들고, AI가 코드(답)를 작성하게 하는 방법입니다.

### TDD = Test-Driven Development

TDD(테스트 주도 개발)는 코드를 먼저 작성하는 것이 아니라, **테스트를 먼저 작성**하는 개발 방법입니다.

순서가 반대라서 처음에는 이상하게 느껴질 수 있습니다. 하지만 테스트를 먼저 쓰면 무엇을 만들어야 하는지 명확해집니다.

### Red-Green-Refactor 사이클

TDD는 세 단계의 짧은 사이클을 반복합니다.

```
🔴 Red:       실패하는 테스트를 먼저 작성한다
              (아직 코드가 없으니 당연히 실패)

🟢 Green:     테스트를 통과하는 코드를 만든다
              (AI에게 맡깁니다!)

🔵 Refactor:  코드를 깔끔하게 정리한다
              (동작은 바꾸지 않고 코드 품질만 개선)
```

이 사이클을 빠르게 반복하면서 기능을 하나씩 완성합니다.

### TDD + AI가 완벽한 이유

```
테스트 = 명확한 목표
AI = 목표를 달성하는 코드를 만드는 도구
```

테스트를 먼저 작성하면 AI에게 **무엇을 만들어야 하는지** 정확히 전달할 수 있습니다. "이 테스트들을 모두 통과하는 코드를 만들어줘"라고 하면, AI는 명확한 목표를 가지고 코드를 작성합니다.

### 기존 방식 vs TDD + AI 방식

| | 기존 방식 | TDD + AI 방식 |
|--|---------|-------------|
| 순서 | 코드 → 테스트 | 테스트 → 코드 |
| 목표 명확도 | 모호할 수 있음 | 테스트가 명확한 목표 역할 |
| AI 활용 | 코드 생성 | 테스트를 보고 구현 생성 |
| 검증 | 직접 실행해봄 | 테스트가 자동 검증 |

---

<a id="part2"></a>

## 2️⃣ 🚀 **도전** — TDD 실습 1: 문자열 유틸리티 [↑](#toc)

간단한 문자열 처리 함수 3개를 TDD로 만들어봅시다.

### 만들 함수들

- `capitalize(str)`: 첫 글자를 대문자로 변환
- `truncate(str, maxLength)`: 글자 수 제한, 초과 시 `...` 추가
- `slugify(str)`: 공백을 `-`로, 대문자를 소문자로 변환 (URL용)

### Step 1: 🔴 Red — 테스트 먼저 작성하기

`tests/utils.test.js` 파일을 직접 만들고 아래 내용을 작성합니다.

```javascript
import { describe, it, expect } from 'vitest';
import { capitalize, truncate, slugify } from '../src/utils.js';

describe('capitalize', () => {
  it('첫 글자를 대문자로 변환한다', () => {
    // Arrange
    const input = 'hello';

    // Act
    const result = capitalize(input);

    // Assert
    expect(result).toBe('Hello');
  });

  it('이미 대문자이면 그대로 반환한다', () => {
    expect(capitalize('Hello')).toBe('Hello');
  });

  it('빈 문자열이면 빈 문자열을 반환한다', () => {
    expect(capitalize('')).toBe('');
  });
});

describe('truncate', () => {
  it('글자 수가 maxLength 이하이면 그대로 반환한다', () => {
    expect(truncate('안녕', 10)).toBe('안녕');
  });

  it('글자 수가 maxLength를 초과하면 잘라서 ...을 붙인다', () => {
    expect(truncate('안녕하세요', 3)).toBe('안녕하...');
  });

  it('maxLength가 0이면 ...만 반환한다', () => {
    expect(truncate('안녕', 0)).toBe('...');
  });
});

describe('slugify', () => {
  it('공백을 하이픈으로 변환한다', () => {
    expect(slugify('hello world')).toBe('hello-world');
  });

  it('대문자를 소문자로 변환한다', () => {
    expect(slugify('Hello World')).toBe('hello-world');
  });

  it('여러 공백은 하나의 하이픈으로 변환한다', () => {
    expect(slugify('hello   world')).toBe('hello-world');
  });
});
```

테스트를 실행해봅니다.

```bash
npx vitest
```

예상 결과: **모두 실패** (아직 `src/utils.js`가 없으니까요!)

```
FAIL  tests/utils.test.js
 × capitalize > 첫 글자를 대문자로 변환한다
 × capitalize > 이미 대문자이면 그대로 반환한다
...
```

이것이 🔴 Red 상태입니다. 실패하는 테스트가 생겼습니다.

### Step 2: 🟢 Green — AI에게 구현 맡기기

Copilot Chat을 열고 아래와 같이 요청합니다.

```
tests/utils.test.js의 테스트를 모두 통과하는 src/utils.js를 작성해줘.

#file:tests/utils.test.js

규칙:
- ESM export 사용 (export const 형태)
- 각 함수에 한국어 JSDoc 주석 포함
- 간결하게 작성
```

Copilot이 생성한 코드 예시:

```javascript
/**
 * 문자열의 첫 글자를 대문자로 변환합니다.
 * @param {string} str - 변환할 문자열
 * @returns {string} 첫 글자가 대문자인 문자열
 */
export const capitalize = (str) => {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1);
};

/**
 * 문자열을 최대 길이로 자릅니다. 초과 시 '...'을 붙입니다.
 * @param {string} str - 자를 문자열
 * @param {number} maxLength - 최대 길이
 * @returns {string} 자른 문자열
 */
export const truncate = (str, maxLength) => {
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength) + '...';
};

/**
 * 문자열을 URL용 슬러그로 변환합니다.
 * @param {string} str - 변환할 문자열
 * @returns {string} 슬러그 문자열
 */
export const slugify = (str) => {
  return str
    .toLowerCase()
    .replace(/\s+/g, '-');
};
```

다시 테스트를 실행합니다.

```bash
npx vitest
```

예상 결과: **모두 통과**

```
PASS  tests/utils.test.js
 ✓ capitalize > 첫 글자를 대문자로 변환한다
 ✓ capitalize > 이미 대문자이면 그대로 반환한다
 ✓ capitalize > 빈 문자열이면 빈 문자열을 반환한다
 ... (9개 테스트 모두 통과)
```

이것이 🟢 Green 상태입니다!

### Step 3: 🔵 Refactor — 코드 정리하기

테스트가 모두 통과하는 것을 확인했으니, 이제 코드를 더 깔끔하게 정리합니다.

Copilot Chat에 요청합니다.

```
src/utils.js를 리팩터링해줘. 
동작은 바꾸지 말고, 코드 품질만 개선해줘.
개선 후 tests/utils.test.js의 모든 테스트가 통과하는지 확인해줘.

#file:src/utils.js
```

리팩터링 후 반드시 테스트를 다시 실행합니다.

```bash
npx vitest
```

여전히 모두 통과하면 성공입니다!

---

<a id="part3"></a>

## 3️⃣ 📖 **더 알아보기** — TDD 실습 2: 장바구니 기능 [↑](#toc)

더 복잡한 로직인 장바구니 기능을 TDD로 만들어봅시다.

### 만들 함수들

- `addItem(cart, item)`: 장바구니에 상품 추가
- `removeItem(cart, itemId)`: 장바구니에서 상품 제거
- `getTotal(cart)`: 총 금액 계산
- `applyDiscount(cart, percent)`: 할인 적용

### Step 1: 🔴 Red — 테스트 먼저 작성

`tests/cart.test.js` 파일을 만듭니다.

```javascript
import { describe, it, expect } from 'vitest';
import { addItem, removeItem, getTotal, applyDiscount } from '../src/cart.js';

describe('addItem', () => {
  it('빈 장바구니에 상품을 추가하면 상품 1개가 된다', () => {
    // Arrange
    const cart = [];
    const item = { id: 1, name: '사과', price: 1000, quantity: 1 };

    // Act
    const result = addItem(cart, item);

    // Assert
    expect(result).toHaveLength(1);
    expect(result[0]).toEqual(item);
  });

  it('같은 상품을 추가하면 수량이 늘어난다', () => {
    // Arrange
    const cart = [{ id: 1, name: '사과', price: 1000, quantity: 1 }];
    const item = { id: 1, name: '사과', price: 1000, quantity: 1 };

    // Act
    const result = addItem(cart, item);

    // Assert
    expect(result).toHaveLength(1);
    expect(result[0].quantity).toBe(2);
  });

  it('기존 장바구니는 변경하지 않는다 (불변성)', () => {
    // Arrange
    const cart = [];
    const item = { id: 1, name: '사과', price: 1000, quantity: 1 };

    // Act
    addItem(cart, item);

    // Assert
    expect(cart).toHaveLength(0); // 원본 배열 변경 없음
  });
});

describe('removeItem', () => {
  it('존재하는 상품을 제거하면 장바구니에서 사라진다', () => {
    // Arrange
    const cart = [
      { id: 1, name: '사과', price: 1000, quantity: 1 },
      { id: 2, name: '바나나', price: 500, quantity: 2 }
    ];

    // Act
    const result = removeItem(cart, 1);

    // Assert
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe(2);
  });

  it('존재하지 않는 id를 제거하면 장바구니가 그대로다', () => {
    const cart = [{ id: 1, name: '사과', price: 1000, quantity: 1 }];
    const result = removeItem(cart, 99);
    expect(result).toHaveLength(1);
  });
});

describe('getTotal', () => {
  it('장바구니 총 금액을 계산한다', () => {
    // Arrange
    const cart = [
      { id: 1, name: '사과', price: 1000, quantity: 2 },  // 2000
      { id: 2, name: '바나나', price: 500, quantity: 3 }  // 1500
    ];

    // Act
    const total = getTotal(cart);

    // Assert
    expect(total).toBe(3500);
  });

  it('빈 장바구니의 총 금액은 0이다', () => {
    expect(getTotal([])).toBe(0);
  });
});

describe('applyDiscount', () => {
  it('10% 할인을 적용한다', () => {
    // Arrange
    const cart = [{ id: 1, name: '사과', price: 1000, quantity: 1 }];

    // Act
    const discounted = applyDiscount(cart, 10);

    // Assert
    expect(getTotal(discounted)).toBe(900);
  });

  it('0% 할인은 금액 변화가 없다', () => {
    const cart = [{ id: 1, name: '사과', price: 1000, quantity: 1 }];
    const discounted = applyDiscount(cart, 0);
    expect(getTotal(discounted)).toBe(1000);
  });

  it('100% 할인은 모든 상품이 0원이 된다', () => {
    const cart = [{ id: 1, name: '사과', price: 1000, quantity: 1 }];
    const discounted = applyDiscount(cart, 100);
    expect(getTotal(discounted)).toBe(0);
  });
});
```

테스트 실행 → 모두 실패 확인 (🔴 Red)

### Step 2: 🟢 Green — AI에게 구현 맡기기

```
tests/cart.test.js의 모든 테스트를 통과하는 src/cart.js를 작성해줘.

#file:tests/cart.test.js

규칙:
- 배열을 직접 수정하지 말고 새 배열을 반환할 것 (불변성)
- ESM export 사용
- 각 함수에 한국어 JSDoc 주석
```

Copilot이 구현 코드를 생성합니다. 테스트 실행으로 확인합니다.

```bash
npx vitest
```

모두 통과하면 🟢 Green!

### Step 3: 🔵 Refactor — 정리

테스트가 통과하면 코드를 정리합니다. 테스트가 든든한 안전망이 되어줍니다. 리팩터링 중 실수로 동작이 바뀌면 테스트가 즉시 알려줍니다.

> **TDD의 숨은 장점**
> 리팩터링이 두렵지 않아집니다. 테스트가 있으니 코드를 마음껏 바꾸고, 테스트로 확인하면 됩니다.

---

<a id="part4"></a>

## 4️⃣ 📖 **더 알아보기** — Custom Agent란? [↑](#toc)

> 회사에서 어떤 일을 맡기고 싶을 때, "아무나"에게 맡기는 것보다 그 분야의 전문가에게 맡기는 게 낫습니다.
> "TDD 전문가에게 이 기능 구현을 맡겨봐"처럼요.
> Custom Agent는 Copilot에게 특정 역할을 부여하는 파일입니다.

### Custom Agent vs Prompt File

| 구분 | Prompt File | Custom Agent |
|------|-------------|-------------|
| **형태** | 일회성 작업 템플릿 | 지속적인 역할/페르소나 |
| **비유** | 업무 요청 양식 | 전문가 역할 직원 |
| **특징** | 한 번 실행 | 대화 내내 역할 유지 |
| **도구 제어** | 제한적 | 허용할 도구 명시 가능 |

### tdd-agent.md 작성하기

`.github/agents/tdd-agent.md` 파일을 만들어봅시다.

먼저 폴더를 생성합니다.

```bash
mkdir -p .github/agents
```

`.github/agents/tdd-agent.md`:

```markdown
---
description: "TDD 사이클(Red-Green-Refactor)로 기능을 구현하는 전문 에이전트. 테스트를 먼저 작성하고, 구현 후 리팩터링한다."
mode: "agent"
tools:
  - read_file
  - write_file
  - run_in_terminal
---

# TDD Agent

당신은 TDD(테스트 주도 개발) 전문가입니다.
모든 기능은 Red-Green-Refactor 사이클로 구현합니다.

## 작업 순서 (반드시 이 순서를 따릅니다)

### 1단계: 요구사항 분석 (Planning)
- 사용자가 요청한 기능을 분석합니다
- 구현할 함수 목록을 만듭니다
- 각 함수의 입력/출력을 명확히 정의합니다

### 2단계: 🔴 Red — 테스트 먼저 작성
- 구현 코드 없이 테스트부터 작성합니다
- `tests/` 폴더에 `*.test.js` 파일을 만듭니다
- 각 함수당 최소 3가지 케이스를 작성합니다:
  - 정상 케이스
  - 경계값 케이스
  - 에러/엣지 케이스
- `npx vitest --run`으로 테스트가 실패하는지 확인합니다

### 3단계: 🟢 Green — 최소 구현
- 테스트를 통과하는 최소한의 코드만 작성합니다
- `src/` 폴더에 구현 파일을 만듭니다
- `npx vitest --run`으로 모든 테스트가 통과하는지 확인합니다

### 4단계: 🔵 Refactor — 정리
- 동작은 유지하면서 코드 품질을 개선합니다
- 중복 제거, 명확한 이름, 주석 추가
- 리팩터링 후 다시 `npx vitest --run`으로 확인합니다

## 코드 규칙
- ESM (import/export) 사용, require 금지
- const 우선, var 금지
- async/await 사용, Promise 체이닝 금지
- 에러 처리 반드시 포함
- 한국어 JSDoc 주석

## 테스트 규칙
- Vitest 사용
- AAA 패턴 (Arrange-Act-Assert)
- describe로 함수별 그룹화
- it 설명은 한국어로 ("~하면 ~를 반환한다")

## 완료 보고
모든 단계가 완료되면 아래 형식으로 보고합니다:

```
✅ TDD 사이클 완료

📋 구현한 함수:
- [함수명]: [한 줄 설명]

🧪 테스트 결과:
- 통과: X개
- 실패: 0개

📁 생성된 파일:
- src/[파일명]
- tests/[파일명]
```
```

### Agent 파일의 구조

```yaml
---
description: "..."   ← 언제 이 에이전트를 써야 하는지 설명
mode: "agent"        ← 에이전트 모드로 실행
tools:               ← 허용할 도구 목록
  - read_file        ← 파일 읽기
  - write_file       ← 파일 쓰기
  - run_in_terminal  ← 터미널 명령 실행
---
```

`tools` 목록에 있는 것만 Agent가 사용할 수 있습니다. 불필요한 도구를 제한해서 안전하게 만들 수 있습니다.

---

<a id="part5"></a>

## 5️⃣ Agent 사용하기 [↑](#toc)

### Agent 실행 방법

Copilot Chat에서 Agent 모드로 전환하고, 에이전트를 선택합니다.

1. Copilot Chat 열기 (`Ctrl+Shift+I` / `Cmd+Shift+I`)
2. 모드를 **Agent**로 전환
3. `@tdd-agent`를 입력하거나 에이전트 목록에서 선택

### 실제 워크플로우 예시

**사용자 요청:**
```
@tdd-agent 
이메일 주소 유효성을 검사하는 validateEmail 함수를 만들어줘.
- 올바른 이메일: test@example.com → true
- @ 없음: testexample.com → false  
- 도메인 없음: test@ → false
- 빈 문자열 → false
```

**Agent 응답 (단계별 진행):**

```
📋 요구사항 분석 완료
- 함수: validateEmail(email)
- 입력: 문자열
- 출력: boolean

🔴 Red 단계 시작...
tests/validate.test.js 작성 중...
```

```javascript
// Agent가 생성한 tests/validate.test.js
import { describe, it, expect } from 'vitest';
import { validateEmail } from '../src/validate.js';

describe('validateEmail', () => {
  it('올바른 이메일 주소는 true를 반환한다', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });

  it('@가 없으면 false를 반환한다', () => {
    expect(validateEmail('testexample.com')).toBe(false);
  });

  it('도메인이 없으면 false를 반환한다', () => {
    expect(validateEmail('test@')).toBe(false);
  });

  it('빈 문자열이면 false를 반환한다', () => {
    expect(validateEmail('')).toBe(false);
  });

  it('null이면 false를 반환한다', () => {
    expect(validateEmail(null)).toBe(false);
  });
});
```

```
테스트 실행 중...
결과: 5개 실패 (구현 파일 없음) ✅ Red 확인

🟢 Green 단계 시작...
src/validate.js 작성 중...
```

```javascript
// Agent가 생성한 src/validate.js
/**
 * 이메일 주소의 유효성을 검사합니다.
 * @param {string} email - 검사할 이메일 주소
 * @returns {boolean} 유효한 이메일이면 true
 */
export const validateEmail = (email) => {
  if (!email || typeof email !== 'string') return false;

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailPattern.test(email);
};
```

```
테스트 실행 중...
결과: 5개 통과 ✅ Green 확인

🔵 Refactor 단계...
코드 검토 중: 현재 코드는 이미 간결하고 명확합니다.
주석 보완만 진행합니다.

✅ TDD 사이클 완료

📋 구현한 함수:
- validateEmail: 이메일 주소 유효성 검사

🧪 테스트 결과:
- 통과: 5개
- 실패: 0개

📁 생성된 파일:
- src/validate.js
- tests/validate.test.js
```

### Agent vs 일반 Copilot의 차이

일반 Copilot에게 같은 요청을 하면 바로 구현 코드를 줍니다. TDD Agent는 반드시 테스트를 먼저 만들고, 단계를 거칩니다. 이것이 핵심 차이입니다.

---

<a id="part6"></a>

## 6️⃣ 실습 과제 [↑](#toc)

### 기본 과제: TDD로 팁 계산기 만들기

레스토랑 팁 계산기를 TDD로 만들어보세요.

**요구사항:**
- `calculateTip(amount, tipPercent)`: 팁 금액 계산
  - `amount`: 음식 금액
  - `tipPercent`: 팁 비율 (0-100)
  - 반환: 팁 금액 (소수점 반올림)
- `splitBill(amount, tipPercent, people)`: 인원별 금액 계산
  - 반환: 1인당 내야 할 금액 (음식+팁, 소수점 반올림)

**단계:**
1. 🔴 `tests/tip.test.js` 직접 작성 (최소 6개 테스트 케이스)
2. 테스트 실행 → 실패 확인
3. 🟢 Copilot Chat에 테스트 파일을 보여주고 구현 요청
4. 테스트 실행 → 통과 확인
5. 🔵 코드 리뷰 후 개선점 있으면 수정

**기대 동작:**

```javascript
calculateTip(10000, 10);   // → 1000 (10000의 10%)
calculateTip(10000, 15);   // → 1500 (10000의 15%)
calculateTip(0, 10);       // → 0
splitBill(30000, 10, 3);   // → 11000 (33000 / 3)
splitBill(30000, 10, 4);   // → 8250 (33000 / 4, 반올림)
```

---

### 도전 과제: tdd-agent로 비밀번호 유효성 검사 구현하기

`.github/agents/tdd-agent.md`를 만들고, 이 에이전트를 사용해서 비밀번호 유효성 검사 기능을 구현해보세요.

**요구사항:**
- `validatePassword(password)`: 비밀번호 유효성 검사
  - 최소 8글자 이상
  - 대문자 1개 이상 포함
  - 숫자 1개 이상 포함
  - 특수문자 1개 이상 포함 (`!@#$%^&*`)
  - 반환: `{ valid: boolean, message: string }`

**기대 동작:**

```javascript
validatePassword('Hello1!');
// → { valid: false, message: '비밀번호는 8자 이상이어야 합니다' }

validatePassword('helloworld1!');
// → { valid: false, message: '대문자를 1개 이상 포함해야 합니다' }

validatePassword('Hello World1!');
// → { valid: true, message: '사용 가능한 비밀번호입니다' }
```

**확인 체크리스트:**

| 항목 | 확인 |
|------|:----:|
| `.github/agents/tdd-agent.md` 생성 완료 | ☐ |
| Agent가 테스트를 먼저 작성했다 | ☐ |
| Red → Green → Refactor 순서로 진행됐다 | ☐ |
| 모든 테스트가 통과한다 | ☐ |
| 엣지 케이스 테스트가 포함되어 있다 | ☐ |

---

<a id="part7"></a>

## 7️⃣ 정리 [↑](#toc)

이번 장에서 배운 내용을 정리합니다.

| 개념 | 설명 |
|------|------|
| **TDD** | 테스트를 먼저 작성하고 코드를 나중에 만드는 개발 방법 |
| **Red** | 실패하는 테스트 작성 (아직 구현 없음) |
| **Green** | 테스트를 통과하는 최소 코드 작성 |
| **Refactor** | 동작 유지하면서 코드 품질 개선 |
| **Custom Agent** | Copilot에게 특정 역할과 행동 방식을 지정하는 파일 |

**TDD + AI의 핵심:**
- 테스트가 명확한 목표를 만든다
- AI는 목표(테스트)를 보고 코드를 만든다
- 테스트가 자동으로 검증한다
- Custom Agent가 TDD 사이클을 일관되게 수행한다

```
내가 할 일: 테스트 작성 (무엇을 만들지 결정)
AI가 할 일: 테스트를 통과하는 코드 작성 (어떻게 만들지 결정)
테스트가 할 일: 코드가 올바른지 자동 검증
```

---

### 다음 장 미리보기

지금까지 배운 모든 것을 하나로 합칩니다. Custom Instructions, Prompt Files, TDD + Agent를 모두 활용해서 실제 외부 API와 연동하는 날씨 앱을 처음부터 완성합니다. 이것이 이 과정의 최종 목표입니다.

→ **다음 내용으로 넘어갑시다**: [15장. 통합 프로젝트 — 날씨 앱](/ai-native-js/weather-app)
