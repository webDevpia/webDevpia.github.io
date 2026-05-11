---
title: 14. Custom Agent
layout: default
parent: AI-Native JavaScript
nav_order: 15
permalink: /ai-native-js/agent
---
{% raw %}

# 14장. Custom Agent — AI에게 전문가 역할 부여하기
{: .no_toc }

> **Phase 3**

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

- Custom Agent가 무엇이고 Prompt File과 어떻게 다른지 설명할 수 있다
- Agent 파일의 구조(description, mode, tools)를 이해하고 작성할 수 있다
- TDD Agent를 만들고 실행할 수 있다

<a id="toc"></a>

## 진행 순서

1. [Custom Agent란?](#part1) — 전문가 역할 부여하기
2. [Agent 파일 작성하기](#part2) — tdd-agent.md 만들기
3. [Agent 사용하기](#part3) — 실전 워크플로우
4. [실습 과제](#part4) — 기본 / 도전
5. [정리](#part5) — 핵심 요약 및 다음 장

---

<a id="part1"></a>

## 1. ⭐ **핵심** — Custom Agent란? [↑](#toc)

> 강사와 함께 Custom Agent의 개념을 알아봅시다

> 회사에서 어떤 일을 맡기고 싶을 때, "아무나"에게 맡기는 것보다 그 분야의 전문가에게 맡기는 게 낫습니다.
> "TDD 전문가에게 이 기능 구현을 맡겨봐"처럼요.
> Custom Agent는 Copilot에게 특정 역할을 부여하는 파일입니다.

### AI-Native 도구 3종 세트 정리

12~14장에서 배우는 도구를 정리합니다:

| 도구 | 파일 위치 | 비유 | 역할 |
|------|----------|------|------|
| **Custom Instructions** (12장) | `.github/copilot-instructions.md` | 회사 규칙 | 모든 요청에 자동 적용되는 규칙 |
| **Prompt Files** (13장) | `.github/prompts/*.prompt.md` | 업무 요청 양식 | 반복 작업을 템플릿으로 자동화 |
| **Custom Agent** (14장) | `.github/agents/*.md` | 전문가 직원 | AI에게 특정 역할과 행동 방식 부여 |

### Custom Agent vs Prompt File

| 구분 | Prompt File | Custom Agent |
|------|-------------|-------------|
| **형태** | 일회성 작업 템플릿 | 지속적인 역할/페르소나 |
| **비유** | 업무 요청서 | 전문가 역할 직원 |
| **특징** | 한 번 실행 | 대화 내내 역할 유지 |
| **도구 제어** | 제한적 | 허용할 도구 명시 가능 |

> 💡 **비유**: Prompt File은 "이 양식대로 보고서 써줘"이고, Agent는 "너는 TDD 전문가야. 앞으로 내가 요청하는 모든 기능을 TDD로 구현해"입니다.

---

<a id="part2"></a>

## 2. ⭐ **핵심** — Agent 파일 작성하기 [↑](#toc)

### Agent 파일 작성 전에 — 3가지 질문

11장에서 4가지, 12장에서 5가지, 13장에서 2가지 질문을 던졌습니다. 이제 이 패턴이 익숙해졌을 것입니다. Agent 파일을 만들기 전에 3가지만 생각합니다.

**질문 1. 이 Agent는 어떤 전문가인가?**

> 어떤 역할을 맡길지 정합니다. "TDD 전문가"라면:

- 테스트를 먼저 쓰고, 구현하고, 리팩터링한다
- Red → Green → Refactor 순서를 반드시 따른다

→ 이것이 **description**과 **역할 정의**(작업 순서)가 됩니다.

**질문 2. 이 Agent가 쓸 수 있는 도구는 무엇인가?**

> 필요한 권한만 주고, 불필요한 권한은 빼서 안전하게 만듭니다.

- 파일을 읽고 쓸 수 있어야 한다 (read_file, write_file)
- 테스트를 실행해야 한다 (run_in_terminal)
- 코드를 삭제하거나 Git을 조작할 필요는 없다 → 빼기

→ 이것이 **tools** 목록이 됩니다. 불필요한 도구를 빼면 실수를 방지할 수 있습니다.

**질문 3. 반드시 지켜야 할 코드 규칙은 무엇인가?**

> 12장에서 만든 copilot-instructions.md의 규칙을 Agent에도 적용합니다.

- ESM, const 우선, var 금지
- 한국어 JSDoc 주석
- Vitest AAA 패턴

→ 이것이 **코드 규칙**과 **테스트 규칙** 섹션이 됩니다.

> 💡 이 3가지 질문에 답하면, 아래 tdd-agent.md의 구조가 자연스럽게 나옵니다.

### tdd-agent.md 작성하기

`.github/agents/tdd-agent.md` 파일을 만들어봅시다.

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

### 2단계: Red — 테스트 먼저 작성
- 구현 코드 없이 테스트부터 작성합니다
- tests/ 폴더에 *.test.js 파일을 만듭니다
- 각 함수당 최소 3가지 케이스: 정상, 경계값, 에러
- npx vitest --run으로 실패 확인

### 3단계: Green — 최소 구현
- 테스트를 통과하는 최소한의 코드만 작성합니다
- npx vitest --run으로 통과 확인

### 4단계: Refactor — 정리
- 동작은 유지하면서 코드 품질 개선
- 리팩터링 후 다시 테스트 통과 확인

## 코드 규칙
- ESM (import/export) 사용, require 금지
- const 우선, var 금지
- 에러 처리 반드시 포함
- 한국어 JSDoc 주석

## 테스트 규칙
- Vitest 사용
- AAA 패턴 (Arrange-Act-Assert)
- describe로 함수별 그룹화
- it 설명은 한국어로

## 완료 보고
모든 단계가 완료되면 보고합니다:
- 구현한 함수 목록
- 테스트 결과 (통과/실패)
- 생성된 파일 목록
```

### Agent 파일의 구조

```yaml
---
description: "..."   # 언제 이 에이전트를 써야 하는지 설명
mode: "agent"        # 에이전트 모드로 실행
tools:               # 허용할 도구 목록
  - read_file        # 파일 읽기
  - write_file       # 파일 쓰기
  - run_in_terminal  # 터미널 명령 실행
---
```

`tools` 목록에 있는 것만 Agent가 사용할 수 있습니다. 불필요한 도구를 제한해서 안전하게 만들 수 있습니다.

---

<a id="part3"></a>

## 3. ⭐ **핵심** — Agent 사용하기 [↑](#toc)

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

✅ TDD 사이클 완료
📋 구현한 함수: validateEmail
🧪 테스트 결과: 통과 5개, 실패 0개
📁 생성된 파일: src/validate.js, tests/validate.test.js
```

### Agent vs 일반 Copilot의 차이

일반 Copilot에게 같은 요청을 하면 바로 구현 코드를 줍니다. TDD Agent는 반드시 테스트를 먼저 만들고, 단계를 거칩니다. 이것이 핵심 차이입니다.

---

<a id="part4"></a>

## 4. 실습 과제 [↑](#toc)

### 기본 과제: 코드 리뷰 Agent 만들기

`.github/agents/review-agent.md`를 만들어보세요.

요구사항:
- description: "코드 리뷰 전문가. 코드를 분석하고 개선점을 제안한다."
- 보안 취약점, 성능 문제, 코딩 컨벤션 위반을 찾도록 지시
- read_file 도구만 허용 (코드를 수정하지 않고 읽기만)

**확인 체크리스트:**

| 항목 | 확인 |
|------|:----:|
| `.github/agents/review-agent.md` 생성 완료 | ☐ |
| description이 역할을 명확히 설명하는가? | ☐ |
| tools에 read_file만 포함되어 있는가? | ☐ |
| 보안/성능/컨벤션 검토 지시가 본문에 있는가? | ☐ |

{::nomarkdown}
<details>
<summary>예시 답안 보기 (먼저 직접 작성한 뒤 비교하세요)</summary>
{:/nomarkdown}

```markdown
---
description: "코드 리뷰 전문가. 코드를 분석하고 보안 취약점, 성능 문제, 코딩 컨벤션 위반을 찾아 개선점을 제안한다."
mode: "agent"
tools:
  - read_file
---

# Code Review Agent

당신은 코드 리뷰 전문가입니다.
코드를 수정하지 않고, 분석과 개선 제안만 합니다.

## 리뷰 항목

### 1. 보안 취약점
- innerHTML에 사용자 입력을 직접 넣는 XSS 취약점
- eval() 사용 여부
- 하드코딩된 API 키나 비밀번호

### 2. 성능 문제
- 불필요한 반복문 중첩
- 매번 재계산하는 값 (캐싱 가능 여부)
- DOM 접근 최소화 여부

### 3. 코딩 컨벤션
- var 대신 const/let 사용 여부
- 함수가 20줄 이하인가
- 변수명이 의미 있는가 (x, temp, data 같은 이름 금지)
- ESM import/export 사용 여부

## 출력 형식
- 발견한 문제를 심각도(높음/중간/낮음)로 분류
- 각 문제에 대해 개선된 코드 예시 제시
- 전체 코드 품질을 A/B/C로 평가하고 총평을 한국어로 작성
```

> 💡 tdd-agent.md와 비교해보세요. 구조는 같지만 **역할**(리뷰 vs TDD), **도구**(read_file만 vs read+write+terminal), **작업 내용**(분석 vs 구현)이 다릅니다.

{::nomarkdown}
</details>
{:/nomarkdown}

### 도전 과제: tdd-agent로 비밀번호 유효성 검사 구현

tdd-agent를 사용해서 비밀번호 유효성 검사 기능을 구현해보세요.

**요구사항:**
- `validatePassword(password)`: 비밀번호 유효성 검사
  - 최소 8글자 이상
  - 대문자 1개 이상 포함
  - 숫자 1개 이상 포함
  - 특수문자 1개 이상 포함
  - 반환: `{ valid: boolean, message: string }`

**확인 체크리스트:**

| 항목 | 확인 |
|------|:----:|
| `.github/agents/tdd-agent.md` 생성 완료 | ☐ |
| Agent가 테스트를 먼저 작성했다 | ☐ |
| Red → Green → Refactor 순서로 진행됐다 | ☐ |
| 모든 테스트가 통과한다 | ☐ |

{::nomarkdown}
<details>
<summary>예시 답안 보기 (먼저 tdd-agent로 직접 구현한 뒤 비교하세요)</summary>
{:/nomarkdown}

**Agent가 생성할 tests/password.test.js:**

```javascript
import { describe, it, expect } from 'vitest';
import { validatePassword } from '../src/password.js';

describe('validatePassword', () => {
  it('모든 조건을 만족하면 valid: true를 반환한다', () => {
    const result = validatePassword('Abcd123!');
    expect(result.valid).toBe(true);
  });

  it('8글자 미만이면 valid: false와 메시지를 반환한다', () => {
    const result = validatePassword('Ab1!');
    expect(result.valid).toBe(false);
    expect(result.message).toContain('8글자');
  });

  it('대문자가 없으면 valid: false를 반환한다', () => {
    const result = validatePassword('abcd1234!');
    expect(result.valid).toBe(false);
    expect(result.message).toContain('대문자');
  });

  it('숫자가 없으면 valid: false를 반환한다', () => {
    const result = validatePassword('Abcdefgh!');
    expect(result.valid).toBe(false);
    expect(result.message).toContain('숫자');
  });

  it('특수문자가 없으면 valid: false를 반환한다', () => {
    const result = validatePassword('Abcdefg1');
    expect(result.valid).toBe(false);
    expect(result.message).toContain('특수문자');
  });

  it('빈 문자열이면 valid: false를 반환한다', () => {
    const result = validatePassword('');
    expect(result.valid).toBe(false);
  });
});
```

**Agent가 생성할 src/password.js:**

```javascript
/**
 * 비밀번호 유효성을 검사합니다.
 * @param {string} password - 검사할 비밀번호
 * @returns {{ valid: boolean, message: string }}
 */
export const validatePassword = (password) => {
  if (!password || password.length < 8) {
    return { valid: false, message: '비밀번호는 최소 8글자 이상이어야 합니다' };
  }
  if (!/[A-Z]/.test(password)) {
    return { valid: false, message: '대문자가 1개 이상 포함되어야 합니다' };
  }
  if (!/[0-9]/.test(password)) {
    return { valid: false, message: '숫자가 1개 이상 포함되어야 합니다' };
  }
  if (!/[!@#$%^&*()_+\-=\[\]{}|;:',.<>?/`~]/.test(password)) {
    return { valid: false, message: '특수문자가 1개 이상 포함되어야 합니다' };
  }
  return { valid: true, message: '유효한 비밀번호입니다' };
};
```

> 💡 AI가 생성한 코드와 다를 수 있습니다. 중요한 것은 **모든 테스트가 통과하는지**입니다. 정규식 패턴이나 메시지 문구는 달라도 괜찮습니다.

{::nomarkdown}
</details>
{:/nomarkdown}

---

<a id="part5"></a>

## 5. 정리 [↑](#toc)

### AI-Native 도구 3종 세트 완성

| 장 | 도구 | 파일 | 핵심 |
|----|------|------|------|
| 12장 | Custom Instructions | `copilot-instructions.md` | 항상 적용되는 규칙 |
| 13장 | Prompt Files | `*.prompt.md` | 반복 작업 템플릿 |
| **14장** | **Custom Agent** | `*.md` (agents/) | **전문가 역할 부여** |

이 3가지 도구를 프로젝트에 세팅하면 AI와의 협업 품질이 크게 향상됩니다.

### 다음 장 미리보기

14장까지 AI-Native 도구 3종을 모두 배웠습니다. 다음 장에서는 이 도구들을 활용하여 **TDD(테스트 주도 개발)** 방법론을 실습합니다. 요구사항을 작성하면 AI가 테스트를 생성하고, 구현하고, 검증하는 전체 사이클을 경험합니다.

---

→ **다음 장**: [15. TDD — 요구사항으로 테스트하고 AI가 구현한다](/ai-native-js/tdd)
{% endraw %}
