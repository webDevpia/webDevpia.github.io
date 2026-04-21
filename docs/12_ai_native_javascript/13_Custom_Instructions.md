---
title: 12. Custom Instructions
layout: default
parent: AI-Native JavaScript
nav_order: 13
permalink: /ai-native-js/instructions
---

# 12장. Custom Instructions — AI에게 규칙 알려주기
{: .no_toc }

> **Phase 3**

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 완전 페어 프로그래밍**
> AI(Copilot)와 완전한 협업이 가능합니다.
> 내가 설계하고 AI가 구현합니다. 테스트로 검증합니다.
> "신뢰하되 검증한다(Trust but verify)"가 원칙입니다.

## 학습 목표

- `copilot-instructions.md` 파일을 작성할 수 있다
- JavaScript 프로젝트용 코딩 규칙을 Instructions 파일로 만들 수 있다
- Instructions 적용 전후의 AI 출력 차이를 확인할 수 있다

<a id="toc"></a>

## 진행 순서

1. [Custom Instructions란?](#part1) — "신입사원 교육 매뉴얼" 비유
2. [copilot-instructions.md 작성하기](#part2) — 프로젝트 공통 규칙 파일
3. [범위 지정 Instructions](#part3) — 파일 유형별 세부 규칙
4. [Instructions가 만드는 차이](#part4) — 적용 전후 비교
5. [좋은 Instructions 작성 팁](#part5) — 더 나은 규칙 만들기
6. [실습 과제](#part6) — 기본 / 도전
7. [정리](#part7) — 핵심 요약 및 다음 장

---

<a id="part1"></a>

## 1️⃣ ⭐ **핵심** — Custom Instructions란? [↑](#toc)

> 새 직원이 첫 출근을 했습니다. 회사 규칙을 아무것도 알려주지 않으면 어떻게 될까요?
> 그 직원은 자기 이전 회사의 방식대로 일할 겁니다. 어쩌면 우리 팀과는 전혀 다른 스타일로요.
> GitHub Copilot도 똑같습니다.

### AI에게 "우리 팀 규칙"을 알려줘야 한다

Copilot은 수백만 개의 오픈소스 코드를 학습했습니다. 그래서 기본 설정으로 쓰면, 어떤 프로젝트에서는 `var`를 쓰고, 어떤 프로젝트에서는 `require`를 쓰고, 에러 처리를 아예 빠뜨리기도 합니다.

**Custom Instructions**는 AI에게 우리 프로젝트의 규칙을 미리 알려주는 파일입니다.

```
📋 신입사원 교육 매뉴얼 = Custom Instructions
"우리 팀은 이렇게 코드를 씁니다. 이것은 하면 안 됩니다. 이 형식을 따르세요."
```

### Custom Instructions의 두 가지 형태

| 종류 | 파일 위치 | 적용 방식 |
|------|-----------|----------|
| **공통 규칙** | `.github/copilot-instructions.md` | 모든 작업에 항상 자동 적용 |
| **범위 지정 규칙** | `.github/instructions/*.instructions.md` | 특정 파일 유형 작업 시 자동 적용 |

### 왜 `.github/` 폴더인가?

`.github/` 폴더는 GitHub와 관련된 설정 파일들을 보관하는 곳입니다. GitHub Copilot은 이 위치를 자동으로 인식하여 Instructions 파일을 읽어들입니다. 별도의 설정 없이 파일을 만들기만 하면 됩니다.

---

<a id="part2"></a>

## 2️⃣ ⭐ **핵심** — copilot-instructions.md 작성하기 [↑](#toc)

> 강사 시연을 보면서 따라하세요

프로젝트 전체에 적용되는 공통 규칙을 만들어봅시다.

### 폴더와 파일 생성

터미널에서 프로젝트 루트 폴더로 이동한 뒤 아래 명령을 실행합니다.

**macOS / Linux:**
```bash
mkdir -p .github
```

**Windows (PowerShell):**
```powershell
mkdir .github
```

그리고 `.github/copilot-instructions.md` 파일을 만들고 아래 내용을 붙여넣습니다.

```markdown
# 프로젝트 규칙

## 언어 및 런타임
- JavaScript (ES2022+), Node.js 20
- ESM (import/export) 사용, require 금지
- 파일 확장자는 .js 사용

## 코딩 컨벤션
- 변수명: camelCase (예: todoList, userName)
- 상수: UPPER_SNAKE_CASE (예: MAX_ITEMS, API_URL)
- 함수: 한 가지 일만 하는 작은 함수 (20줄 이하 권장)
- const 우선, let은 필요할 때만, var 금지
- 화살표 함수 우선 사용

## 에러 처리
- fetch 호출은 반드시 try/catch로 감싸기
- 사용자에게 보여주는 에러 메시지는 한국어로
- 에러 메시지에 원인 정보를 포함할 것

## 테스트
- 테스트 프레임워크: Vitest
- 파일명: *.test.js
- AAA 패턴 사용: Arrange, Act, Assert
- 각 테스트 함수는 하나의 동작만 검증

## 주석
- 복잡한 로직에는 한국어 주석 작성
- 함수 위에 JSDoc 형식의 설명 작성 권장
```

> **왜 frontmatter(---블록)가 없나요?**
> `copilot-instructions.md`는 특별한 파일입니다. 항상 전체에 적용되므로 별도의 설정 블록이 필요 없습니다. 다음 절에서 만들 `.instructions.md` 파일에는 frontmatter가 필요합니다.

---

<a id="part3"></a>

## 3️⃣ 🚀 **도전** — 범위 지정 Instructions [↑](#toc)

공통 규칙 외에, **특정 파일 유형에만** 적용되는 세부 규칙을 만들 수 있습니다. 마치 "JavaScript 코드를 작성할 때만", "테스트 코드를 작성할 때만" 적용되는 별도의 규칙집입니다.

### 폴더 생성

```bash
mkdir -p .github/instructions
```

### javascript.instructions.md — JavaScript 전용 규칙

`.github/instructions/javascript.instructions.md` 파일을 만들고 아래 내용을 붙여넣습니다.

```markdown
---
description: "JavaScript 코드 작성 또는 리뷰 시 사용한다. 네이밍 규칙, 함수 설계, 비동기 처리 규칙을 포함한다."
applyTo: "**/*.js"
---

# JavaScript 코딩 지침

## 변수와 함수 설계
- 변수명은 의미 있게 작성 (x, temp, data 같은 이름 금지)
- 함수는 동사로 시작 (예: getTodo, addItem, validateInput)
- 매개변수가 3개 이상이면 객체로 묶기

## 비동기 처리
- Promise 대신 async/await 사용
- await 사용 시 반드시 try/catch로 감싸기
- 에러 변수명은 err 또는 error 사용

## 모듈 시스템
- import/export 사용 (require/module.exports 금지)
- 명명된 내보내기(named export) 우선

## 코드 품질
- 중첩 if-else는 3단계 이하로 유지
- 매직 넘버 금지: 숫자는 상수에 저장
- 불필요한 console.log 제거
```

`applyTo: "**/*.js"` 부분이 핵심입니다. `.js` 파일을 작업할 때만 이 규칙이 자동으로 적용됩니다.

### testing.instructions.md — 테스트 전용 규칙

`.github/instructions/testing.instructions.md` 파일을 만들고 아래 내용을 붙여넣습니다.

```markdown
---
description: "Vitest 테스트 작성 또는 리뷰 시 사용한다. AAA 패턴, 테스트 네이밍, 엣지 케이스 처리 규칙을 포함한다."
applyTo: "**/*.test.js"
---

# Vitest 테스트 작성 지침

## 테스트 프레임워크
- Vitest를 사용한다
- import는 파일 맨 위에서 한 번만

## 테스트 명명 규칙
- describe 블록: 테스트 대상 함수/모듈 이름
- it/test 설명: "~하면 ~를 반환한다" 형식 (한국어)

## 테스트 구조 (AAA 패턴)
- Arrange: 테스트에 필요한 데이터 준비
- Act: 테스트 대상 함수 실행
- Assert: 결과 검증 (expect)
- 각 단계를 빈 줄로 구분

## 엣지 케이스
- 빈 값(null, undefined, 빈 문자열) 처리 테스트 포함
- 경계값(0, 최대값) 테스트 포함
- 에러 케이스 테스트 포함 (rejects, toThrow)
```

### YAML Frontmatter란?

파일 맨 위의 `---`로 감싼 블록이 **YAML frontmatter**입니다. Copilot에게 "이 파일을 언제, 어떻게 사용할지"를 알려주는 설정입니다.

```yaml
---
description: "언제 이 규칙을 쓸지 설명"   ← Copilot이 참고하는 설명
applyTo: "**/*.js"                        ← 어떤 파일에 적용할지 패턴
---
```

| 항목 | 의미 |
|------|------|
| `description` | 이 규칙 파일이 언제 쓰이는지 설명 |
| `applyTo` | 적용할 파일 패턴 (`**/*.js`, `**/*.test.js` 등) |

---

<a id="part4"></a>

## 4️⃣ ⭐ **핵심** — Instructions가 만드는 차이 [↑](#toc)

> 강사와 함께 적용 전후를 비교해 봅시다

Instructions를 적용하기 전후로 AI 출력이 어떻게 달라지는지 직접 비교해봅시다.

### 같은 질문, 다른 결과

**요청한 내용:**
```
할 일 목록을 가져오는 함수를 만들어줘. 서버에서 JSON으로 받아온다.
```

**Instructions 적용 전 (기본 Copilot):**

```javascript
// AI가 생성한 코드 — 문제가 많습니다!
var BASE_URL = 'https://api.example.com';

function getTodos(callback) {
  fetch(BASE_URL + '/todos')
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      callback(data);
    });
}
```

문제점:
- `var` 사용 (금지됨)
- `require` 대신 전역 `fetch` (ESM 환경 고려 없음)
- 에러 처리 없음
- 콜백 패턴 사용 (구식)

**Instructions 적용 후 (우리 규칙을 따른 Copilot):**

```javascript
// AI가 생성한 코드 — 규칙을 잘 따릅니다!
const BASE_URL = 'https://api.example.com';

/**
 * 서버에서 할 일 목록을 가져옵니다.
 * @returns {Promise<Array>} 할 일 목록 배열
 */
export const getTodos = async () => {
  try {
    const response = await fetch(`${BASE_URL}/todos`);

    if (!response.ok) {
      throw new Error(`서버 오류: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    throw new Error(`할 일 목록을 불러오는 데 실패했습니다: ${error.message}`);
  }
};
```

개선된 점:
- `const` 사용
- `async/await` 패턴
- `try/catch` 에러 처리 포함
- 한국어 에러 메시지
- ESM `export` 사용
- JSDoc 주석 포함

같은 질문인데 결과가 완전히 달라졌습니다!

### 확인 방법

Instructions 파일을 만든 뒤 Copilot Chat에서 새 대화를 시작하고 아래 요청을 해보세요.

```
fetch로 사용자 목록을 가져오는 함수를 작성해줘.
에러 처리도 포함해줘.
```

확인 포인트:
- `var` 대신 `const`/`let`을 쓰는가?
- `async/await` 패턴을 쓰는가?
- `try/catch`가 포함되어 있는가?
- 에러 메시지가 한국어인가?
- `export`로 내보내는가?

> **Copilot이 규칙을 안 따를 때**
> 1. 파일 경로 확인: `.github/copilot-instructions.md` (앞에 점이 붙습니다)
> 2. Copilot Chat 새 대화를 시작해보세요
> 3. 아래처럼 직접 명시하면 더 확실합니다:
> ```
> 프로젝트 지침을 따라서 fetch로 사용자 목록을 가져오는 함수를 작성해줘.
> ```

---

<a id="part5"></a>

## 5️⃣ 좋은 Instructions 작성 팁 [↑](#toc)

Instructions가 잘 동작하려면 **구체적이고 명확하게** 작성해야 합니다.

### 원칙 1: 구체적으로 작성하기

| 나쁜 예 | 좋은 예 |
|---------|---------|
| ❌ "좋은 코드를 써라" | ✅ "함수는 20줄 이하로 작성한다" |
| ❌ "에러를 처리해라" | ✅ "fetch 호출은 반드시 try/catch로 감싼다" |
| ❌ "명확한 이름을 써라" | ✅ "변수명은 x, temp 같은 약어 금지" |

### 원칙 2: 예시를 포함하기

```markdown
## 함수 네이밍
- 동사로 시작한다
- 좋은 예: getTodo, addItem, deleteUser, validateInput
- 나쁜 예: todo, item, data, process
```

예시를 보여주면 AI가 의도를 더 잘 이해합니다.

### 원칙 3: 금지 사항을 명시하기

```markdown
## 절대 하면 안 되는 것
- var 사용 금지
- require() 사용 금지
- 에러 처리 없는 fetch 금지
- 하드코딩된 URL 금지 (상수로 분리할 것)
```

"하면 안 된다"를 명시적으로 적는 것이 "이렇게 해라"보다 효과적일 때가 많습니다.

### 원칙 4: 너무 많이 쓰지 않기

Instructions 파일이 너무 길면 AI가 중요한 규칙을 놓칠 수 있습니다. 핵심적인 규칙 10-15개를 선별해서 작성하세요.

```
❌ 너무 긴 Instructions (50줄+)
   → AI가 어떤 규칙이 중요한지 판단하기 어려워짐

✅ 핵심만 담은 Instructions (20-30줄)
   → AI가 규칙을 더 잘 따름
```

### 원칙 5: 팀과 함께 만들기

Instructions 파일은 팀 전체가 동의한 규칙이어야 합니다. 혼자 만들어서 팀원에게 강요하면 반발이 생길 수 있습니다. 팀원들과 논의하고, 가장 중요한 규칙부터 시작하세요.

---

<a id="part6"></a>

## 6️⃣ 실습 과제 [↑](#toc)

### 기본 과제: 나만의 copilot-instructions.md 완성하기

이번 장에서 만든 파일을 자신의 ToDo 앱 프로젝트에 적용해보세요.

**단계:**
1. ToDo 앱 프로젝트 폴더에 `.github/` 폴더 생성
2. `.github/copilot-instructions.md` 파일 생성
3. 이번 장의 예시를 기반으로 자신의 프로젝트에 맞게 수정
4. `.github/instructions/javascript.instructions.md` 생성
5. `.github/instructions/testing.instructions.md` 생성
6. Copilot Chat에서 간단한 함수 작성을 요청해보고 규칙이 반영됐는지 확인

**확인 체크리스트:**

| 항목 | 확인 |
|------|:----:|
| `.github/copilot-instructions.md` 생성 완료 | ☐ |
| `.github/instructions/javascript.instructions.md` 생성 완료 | ☐ |
| `.github/instructions/testing.instructions.md` 생성 완료 | ☐ |
| `applyTo` 패턴이 올바르게 설정됨 (`**/*.js`, `**/*.test.js`) | ☐ |
| Copilot이 `const`를 사용하는지 확인 | ☐ |
| Copilot이 `async/await` + `try/catch`를 사용하는지 확인 | ☐ |

---

### 도전 과제: Instructions 적용 전후 비교 보고서 작성

같은 요청을 Instructions 적용 전과 후에 각각 Copilot에게 해보고, 결과를 비교하는 짧은 보고서를 작성해보세요.

**비교 요청 예시:**
```
localStorage에 데이터를 저장하고 불러오는 함수를 만들어줘.
저장할 때는 JSON.stringify, 불러올 때는 JSON.parse를 써줘.
에러 처리도 포함해줘.
```

**보고서 형식:**

```markdown
# Instructions 적용 전후 비교

## 요청 내용
[어떤 요청을 했는지]

## 적용 전 출력
[Copilot이 생성한 코드]

## 적용 후 출력
[Copilot이 생성한 코드]

## 비교 분석
- 개선된 점: [예: var → const, 에러 처리 추가 등]
- 여전히 아쉬운 점: [예: 주석이 영어로 나옴 등]
- Instructions 수정이 필요한 부분: [예: 주석을 한국어로 쓰도록 명시 추가]
```

---

<a id="part7"></a>

## 7️⃣ 정리 [↑](#toc)

이번 장에서 만든 파일과 각각의 역할을 정리합니다.

| 파일 | 역할 | 적용 방식 |
|------|------|----------|
| `.github/copilot-instructions.md` | 프로젝트 전체 공통 규칙 | 모든 채팅 요청에 자동 적용 |
| `.github/instructions/javascript.instructions.md` | JS 파일 코딩 규칙 | `.js` 파일 작업 시 자동 적용 |
| `.github/instructions/testing.instructions.md` | Vitest 테스트 작성 규칙 | `.test.js` 파일 작업 시 자동 적용 |

**Custom Instructions의 핵심 원칙:**
- 공통 규칙은 `copilot-instructions.md`에, 파일 유형별 규칙은 `*.instructions.md`에 분리
- 구체적이고 명확하게 작성해야 AI가 잘 따름
- 너무 긴 Instructions보다 핵심 규칙 10-15개가 효과적
- 금지 사항을 명시적으로 적는 것이 중요

---

### 다음 장 미리보기

Custom Instructions가 "항상 적용되는 규칙"이라면, Prompt Files는 "필요할 때 꺼내 쓰는 작업 템플릿"입니다. 카페의 단골 주문서처럼, 자주 하는 요청을 파일로 저장해두고 한 번에 실행하는 방법을 배웁니다.

→ **다음 내용으로 넘어갑시다**: [13장. Prompt Files + Context Engineering](/ai-native-js/prompts)
