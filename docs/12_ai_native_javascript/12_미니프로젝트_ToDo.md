---
title: 11. 미니 프로젝트 — AI 협업 ToDo 앱
layout: default
parent: AI-Native JavaScript
nav_order: 12
permalink: /ai-native-js/todo-app
---

# 11장. 미니 프로젝트 — AI 협업 ToDo 앱
{: .no_toc }

> **Phase 2**

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 생성 + 검증 모드**
> AI(Copilot)가 코드를 생성할 수 있습니다.
> 단, 반드시 생성된 코드를 **읽고, 이해하고, 테스트로 검증**해야 합니다.
> AI 코드를 이해 없이 복붙하는 것은 금지입니다.

## 학습 목표

- 요구사항 파일을 작성하여 AI에게 코드 생성을 지시할 수 있다
- AI가 생성한 코드(테스트, 로직, UI)를 검증하고 수정할 수 있다
- 요구사항 → AI 생성 → 테스트 검증 → Bug Hunt의 전체 사이클을 경험한다

<a id="toc"></a>

## 진행 순서

1. [프로젝트 소개](#part1) — 무엇을 만드는가
2. [요구사항 파일 작성하기](#part2) — 모든 것의 시작
3. [프로젝트 구조 만들기](#part3) — 폴더와 파일 준비
4. [AI에게 테스트 코드 생성 요청](#part4) — 요구사항 → 테스트
5. [AI에게 핵심 로직 구현 요청](#part5) — 테스트를 통과하는 코드
6. [AI에게 UI + DOM 연결 요청](#part6) — 화면 만들기
7. [Bug Hunt — 생성된 코드 검증](#part7) — 보안 문제 찾기
8. [Phase 2 관문](#part8) — 자기 점검 체크리스트
9. [정리](#part9) — Phase 2 완주 축하

---

<a id="part1"></a>

## 1️⃣ 프로젝트 소개 [↑](#toc)

이 장은 Phase 2의 **최종 관문**입니다. 지금까지 배운 모든 것을 하나의 프로젝트에서 사용합니다.

- DOM 조작 (08장)
- AI 코드 평가 체크리스트 및 Bug Hunt (09장)
- async/await 및 API 호출 (10장)
- Vitest 테스트 (07장)

### 우리가 만들 것: 브라우저 ToDo 앱

![ToDo 앱 완성 화면](/docs/12_ai_native_javascript/img/todo-app-mockup.png)

### 이 프로젝트의 핵심 — 요구사항이 모든 코드를 만든다

이 프로젝트에서 여러분은 **코드를 직접 작성하지 않습니다.** 대신:

| 여러분이 하는 것 | AI가 하는 것 |
|-----------------|-------------|
| 요구사항 파일 작성 | 테스트 코드 생성 |
| AI가 만든 테스트 검토 | 핵심 로직 구현 |
| 테스트 실행 + 결과 확인 | HTML/UI 생성 |
| Bug Hunt로 코드 검증 | DOM 연결 코드 생성 |
| 보안 문제 발견 + 수정 요청 | 수정 코드 생성 |

> **핵심 원칙**: 내가 "무엇을 만들지" 정의하면, AI가 "어떻게 만들지" 구현한다.
> 내 역할은 **설계자이자 검증자**이다.

---

<a id="part2"></a>

## 2️⃣ ⭐ **핵심** — 요구사항 파일 작성하기 [↑](#toc)

> 강사와 함께 요구사항을 작성해 봅시다

AI-Native 개발의 첫 단계는 **요구사항 파일을 작성하는 것**입니다. 이 파일이 이후 모든 코드 생성의 기준이 됩니다.

> 건축가가 설계도 없이 집을 짓지 않듯이,
> AI-Native 개발자는 요구사항 없이 AI에게 코드를 요청하지 않습니다.

### 나쁜 요구사항 vs 좋은 요구사항

**나쁜 요구사항**:
```
할 일 앱 만들어줘
```
AI가 무엇을 만들지, 어떻게 동작해야 할지 알 수 없습니다.

**좋은 요구사항**: 기능, 제약 조건, 파일 구조를 명확하게 정의합니다. 아래처럼요.

### requirements.md 작성하기

프로젝트 폴더에 `requirements.md` 파일을 만들고 아래 내용을 **직접 작성**하세요. 이것이 이 프로젝트에서 여러분이 작성하는 **가장 중요한 파일**입니다.

```markdown
# ToDo 앱 요구사항

## 기능 요구사항
1. 할 일을 텍스트로 입력하고 "추가" 버튼 또는 Enter 키로 추가할 수 있다
2. 각 할 일 항목을 클릭하면 완료/미완료가 토글된다
3. 각 항목에 "삭제" 버튼이 있고, 클릭하면 삭제된다
4. "전체/완료/미완료" 필터 탭으로 목록을 걸러볼 수 있다
5. 완료 개수와 전체 개수가 표시된다

## 제약 조건
- 핵심 로직(추가, 토글, 삭제, 필터)은 순수 함수로 구현한다 (todo.js)
- DOM 조작 코드는 별도 파일에 분리한다 (app.js)
- 외부 라이브러리 없이 순수 JavaScript만 사용한다
- 빈 텍스트는 추가할 수 없다 (공백만 있는 경우 포함)
- 원본 배열을 변경하지 않는다 (불변성 유지)

## 파일 구조
- src/todo.js: 순수 함수 (addTodo, toggleTodo, deleteTodo, filterTodos)
- src/app.js: DOM 연결 코드
- tests/todo.test.js: Vitest 테스트
- index.html: 사용자 인터페이스

## 범위 밖 (Out of Scope) — 구현하지 않을 것
- localStorage 저장 (새로고침 시 데이터 유지 불필요)
- 할 일 수정(편집) 기능
- 드래그앤드롭 정렬
- 날짜/시간 표시
- 카테고리/태그 분류
- 애니메이션/트랜지션 효과
- 반응형 디자인

## 금지 사항 (Don'ts)
- var 사용 금지 (let/const만 사용)
- 전역 변수 사용 금지
- eval() 사용 금지
- jQuery 등 외부 라이브러리 사용 금지
- console.log 디버깅 코드를 최종 코드에 남기지 않는다
- innerHTML에 사용자 입력을 직접 넣지 않는다 (XSS 방지)

## 기술 스택
- JavaScript ES2022+ (ESM import/export)
- Vitest 테스트 프레임워크
- HTML5 + CSS
```

> 💡 이 파일이 이후 AI에게 모든 코드를 요청할 때의 **기준 문서**가 됩니다.
> 요구사항이 명확할수록 AI가 더 좋은 코드를 생성합니다.

### 왜 이런 항목들이 요구사항에 들어가는가?

#### "범위 밖"이 필요한 이유

AI는 "좋은 앱"을 만들려고 **요청하지 않은 기능을 추가하는 경향**이 있습니다.

```
여러분: "할 일 앱 만들어줘"
AI: (localStorage 저장 + 드래그앤드롭 + 애니메이션 + 반응형 CSS를 포함한 300줄 코드 생성)
여러분: "...이게 다 뭐지?"
```

"범위 밖"을 명시하면 AI가 **딱 요청한 것만** 만듭니다. 실무에서도 프로젝트 기획서(PRD)에는 항상 "Out of Scope" 섹션이 있습니다.

| 명시하지 않으면 | 명시하면 |
|---------------|---------|
| AI가 localStorage 저장을 추가함 | 추가하지 않음 → 코드가 간결 |
| 드래그앤드롭까지 구현됨 | 핵심 기능에만 집중 |
| 코드 200줄 → 500줄로 부풀어남 | 읽고 검증 가능한 크기 유지 |

#### "금지 사항"이 필요한 이유

AI는 때때로 **안전하지 않거나 오래된 패턴**을 사용합니다.

| 금지 항목 | 왜 금지하는가 |
|----------|-------------|
| `var` | `let`/`const`가 더 안전 — `var`는 함수 스코프라 예측하기 어려움 |
| 전역 변수 | 다른 코드와 충돌 위험 — 모든 변수는 함수/모듈 안에 |
| `eval()` | 보안 취약점 — 사용자 입력을 코드로 실행하면 위험 |
| 외부 라이브러리 | 이 프로젝트는 순수 JS 학습이 목적 |
| `innerHTML` + 사용자 입력 | XSS 공격 — `<script>` 태그가 실행될 수 있음 |
| `console.log` 남기기 | 디버깅용이므로 최종 코드에서는 제거해야 깔끔 |

> 💡 **핵심**: "하지 말 것"을 정의하는 것은 "할 것"을 정의하는 것만큼 중요합니다.
> 이 습관이 Phase 3의 Custom Instructions(12장)로 자연스럽게 이어집니다.

---

<a id="part3"></a>

## 3️⃣ 프로젝트 구조 만들기 [↑](#toc)

터미널에서 다음 명령어를 실행하세요:

```bash
# 프로젝트 폴더 만들기
mkdir todo-app
cd todo-app

# Node.js 프로젝트 초기화
npm init -y

# Vitest 설치
npm install -D vitest

# 폴더 구조 만들기
mkdir src tests
```

### package.json 수정

```json
{
  "name": "todo-app",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "devDependencies": {
    "vitest": "^3.0.0"
  }
}
```

### 최종 파일 구조

```
todo-app/
├── requirements.md     ← 요구사항 (내가 작성)
├── index.html          ← AI가 생성
├── src/
│   ├── todo.js         ← AI가 생성 (핵심 로직)
│   └── app.js          ← AI가 생성 (DOM 연결)
├── tests/
│   └── todo.test.js    ← AI가 생성 → 내가 검토
├── package.json
└── style.css           ← AI가 생성 (선택)
```

> **포인트**: `requirements.md`만 내가 작성하고, 나머지 코드는 전부 AI가 생성합니다.

---

<a id="part4"></a>

## 4️⃣ ⭐ **핵심** — AI에게 테스트 코드 생성 요청 [↑](#toc)

> 강사 시연을 보면서 따라하세요

### AI에게 요청하기

Copilot Chat에 다음과 같이 요청합니다:

```
아래 요구사항을 기반으로 tests/todo.test.js를 작성해줘.

#file:requirements.md

규칙:
- Vitest 사용 (import { describe, it, expect } from 'vitest')
- ESM import 사용
- 각 함수별로 describe 그룹
- 정상 동작 + 엣지 케이스(빈 문자열, 공백, 존재하지 않는 id) 테스트 포함
- 불변성 테스트 포함 (원본 배열이 변경되지 않는지)
- 한국어 테스트 설명
```

### AI가 생성한 테스트 검토하기

AI가 생성한 테스트 코드를 `tests/todo.test.js`에 붙여넣기 전에, **각 테스트가 요구사항과 맞는지** 확인하세요.

**검토 체크리스트:**

| 요구사항 | 테스트에 있는가? |
|----------|:---:|
| 할 일 추가 | ☐ |
| 빈 텍스트 추가 방지 | ☐ |
| 공백만 있는 텍스트 추가 방지 | ☐ |
| 완료/미완료 토글 | ☐ |
| 존재하지 않는 id 토글 시 안전 처리 | ☐ |
| 할 일 삭제 | ☐ |
| 필터링 (전체/완료/미완료) | ☐ |
| 원본 배열 불변성 | ☐ |

누락된 테스트가 있다면 **먼저 requirements.md를 수정**하고, 수정된 요구사항을 기반으로 AI에게 재생성을 요청하세요.

예시: "빈 배열에 필터를 적용하면 빈 배열을 반환한다"가 누락된 경우

**Step 1.** requirements.md의 기능 요구사항에 추가:
```markdown
5. 빈 배열에 필터를 적용하면 빈 배열을 반환한다
```

**Step 2.** AI에게 요청:
```
requirements.md가 업데이트되었습니다. 추가된 요구사항을 반영하여 
tests/todo.test.js에 테스트를 추가해줘.

#file:requirements.md
#file:tests/todo.test.js
```

> 💡 **핵심 원칙**: 코드를 바꾸고 싶으면 **먼저 요구사항을 바꾸세요.**
> requirements.md가 항상 최신 상태여야 "기준 문서" 역할을 합니다.
> 요구사항 없이 AI에게 직접 "이것도 추가해줘"라고 하면, 문서와 코드가 불일치하게 됩니다.

### 테스트 실행 — 당연히 실패합니다

```bash
npm test
```

```
FAIL  tests/todo.test.js
  Cannot find module '../src/todo.js'
```

구현 파일이 없으니 당연히 실패합니다. 이것이 정상입니다!

---

<a id="part5"></a>

## 5️⃣ ⭐ **핵심** — AI에게 핵심 로직 구현 요청 [↑](#toc)

> 강사 시연을 보면서 따라하세요

### AI에게 요청하기

Copilot Chat에 요청합니다:

```
tests/todo.test.js의 모든 테스트를 통과하는 src/todo.js를 작성해줘.

#file:requirements.md
#file:tests/todo.test.js

규칙:
- ESM export 사용
- 각 함수는 원본 배열을 변경하지 않고 새 배열을 반환
- 한국어 JSDoc 주석 포함
```

### 생성된 코드 읽기

AI가 생성한 코드를 바로 붙여넣지 말고, **먼저 읽으세요.** 각 함수가 무엇을 하는지 이해할 수 있어야 합니다.

읽으면서 확인할 것:
- `addTodo`: text를 trim하고, 빈 문자열이면 원본 반환, 아니면 새 배열 반환하는가?
- `toggleTodo`: map으로 새 배열을 만들고, id가 일치하는 항목만 completed를 반전하는가?
- `deleteTodo`: filter로 해당 id를 제외한 새 배열을 반환하는가?
- `filterTodos`: 필터 조건에 따라 적절히 걸러내는가?

### 테스트 실행 — 통과 확인

```bash
npm test
```

모든 테스트가 통과하면 핵심 로직이 요구사항대로 구현된 것입니다.

> **이것이 AI-Native 개발의 핵심 사이클입니다:**
> 요구사항 작성 → AI가 테스트 생성 → AI가 구현 → 테스트로 검증

---

<a id="part6"></a>

## 6️⃣ ⭐ **핵심** — AI에게 UI + DOM 연결 요청 [↑](#toc)

### AI에게 HTML 요청하기

```
requirements.md를 기반으로 index.html을 작성해줘.

#file:requirements.md

규칙:
- 한국어 UI
- id 속성: #todoForm, #todoInput, #todoList, .filter-btn[data-filter], #counter
- <script type="module" src="src/app.js"></script> 포함
- 간단한 인라인 CSS 또는 style.css 링크
```

생성된 HTML을 `index.html`에 저장하세요.

### AI에게 DOM 연결 요청하기

```
requirements.md와 index.html을 기반으로 src/app.js를 작성해줘.
todo.js의 순수 함수들을 HTML UI와 연결하는 코드야.

#file:requirements.md
#file:index.html
#file:src/todo.js

규칙:
- ESM import 사용
- async/await + try/catch
- 에러 메시지는 한국어
- 추가, 완료 토글, 삭제, 필터링, 개수 표시 기능 구현
```

---

<a id="part7"></a>

## 7️⃣ ⭐ **핵심** — Bug Hunt — 생성된 코드 검증 [↑](#toc)

AI가 생성한 app.js에 09장에서 배운 Bug Hunt 체크리스트를 적용합니다.

```
□ 실행되는가?
  → index.html을 브라우저에서 열어서 직접 확인하세요

□ 예상대로 동작하는가?
  → 추가, 토글, 삭제, 필터 각각 테스트해보세요
  → 빈 입력은 어떻게 처리되나요?

□ 모르는 메서드/문법이 있는가?
  → e.stopPropagation()이 무엇인지 AI에게 물어보세요
  → innerHTML에 todo.text를 직접 넣는 것이 안전한가요?

□ 보안 문제는 없는가?
  → innerHTML = `... ${todo.text} ...` 부분을 확인하세요
  → todo.text에 <script> 태그가 들어오면 어떻게 될까요?

□ 더 간단한 방법이 있는가?
  → render 함수가 하는 일이 명확한가요?
```

### 보안 문제 발견 시 — AI에게 수정 요청

만약 `innerHTML`에 사용자 입력을 직접 넣는 코드를 발견했다면:

```
app.js에서 innerHTML에 todo.text를 직접 넣는 부분이 XSS 취약점입니다.
textContent와 createElement를 사용하도록 수정해줘.

#file:src/app.js
```

AI가 수정한 코드를 확인하세요:

```javascript
// 수정 전 (보안 취약)
li.innerHTML = `
  <span class="todo-text">${todo.text}</span>
  <button class="delete-btn">삭제</button>
`;

// 수정 후 (안전) — textContent 사용으로 XSS 방지
const span = document.createElement('span');
span.className = 'todo-text';
span.textContent = todo.text; // HTML 태그를 문자 그대로 표시

const deleteBtn = document.createElement('button');
deleteBtn.className = 'delete-btn';
deleteBtn.textContent = '삭제';

li.appendChild(span);
li.appendChild(deleteBtn);
```

> **이것이 Phase 2의 핵심 역량입니다:**
> AI가 만든 코드에서 문제를 **발견**하고, AI에게 **수정을 지시**하는 것.

---

<a id="part8"></a>

## 8️⃣ Phase 2 관문 — 자기 점검 [↑](#toc)

다음 4가지를 모두 체크할 수 있으면 Phase 3으로 진행합니다.

```
□ 요구사항 파일을 작성하여 AI에게 코드를 생성시킬 수 있다
  → requirements.md가 명확하게 작성되었나요?
  → AI에게 요청할 때 요구사항 파일을 참조했나요?

□ AI가 생성한 코드를 한 줄씩 설명할 수 있다
  → todo.js의 각 함수를 보고 무엇을 하는지 설명해보세요
  → app.js의 이벤트 처리 흐름을 설명해보세요

□ AI 생성 코드에서 버그 2개 이상을 찾을 수 있다
  → Bug Hunt 체크리스트를 app.js 전체에 적용했나요?
  → 보안 문제(XSS)를 발견하고 수정을 요청했나요?

□ 테스트를 실행하고 결과를 해석할 수 있다
  → npm test로 모든 테스트가 통과하나요?
  → 테스트가 실패하면 어떤 기능에 문제가 있는지 판단할 수 있나요?
```

**위 4개를 모두 체크하면 Phase 3으로 진행합니다!**
{: .label .label-green }

### Phase 2 돌아보기

Phase 2에서 여러분이 배운 것:

| 08장 | DOM과 이벤트 | AI 생성 코드를 한 줄씩 읽고 설명하는 "Explain It Back" |
| 09장 | AI 출력 평가법 | AI 코드의 버그를 발견하는 체크리스트와 Bug Hunt |
| 10장 | 비동기 JavaScript | fetch, async/await, 테스트로 비동기 로직 검증 |
| 11장 | 미니 프로젝트 | **요구사항 파일 → AI 생성 → 테스트 검증 → Bug Hunt** |

---

<a id="part9"></a>

## 9️⃣ 정리 [↑](#toc)

Phase 2를 완주했습니다!

Phase 0-1에서 여러분은 "코드가 무엇인지, 어떻게 쓰는지"를 배웠습니다.
Phase 2에서는 "요구사항을 쓰고, AI가 만든 코드를 읽고, 평가하고, 고치는 방법"을 배웠습니다.

이 능력은 AI 시대의 개발자에게 가장 중요한 역량 중 하나입니다. AI는 빠르게 초안을 만들지만, 그 초안이 올바른지 판단하는 것은 언제나 사람의 몫입니다.

### 완료한 것들

- 요구사항 파일(requirements.md)을 작성하여 AI에게 코드 생성을 지시
- AI가 생성한 테스트 코드를 검토하고 누락된 케이스를 확인
- AI가 생성한 핵심 로직을 테스트로 검증
- AI가 생성한 UI/DOM 코드에서 보안 문제를 발견하고 수정 요청
- 브라우저에서 동작하는 ToDo 앱 완성

### 이 프로젝트의 전체 흐름 — 기억해두세요

```
1. requirements.md 작성        ← 내가 설계
2. AI에게 테스트 생성 요청      ← AI가 구현
3. 테스트 검토                  ← 내가 검증
4. AI에게 핵심 로직 구현 요청   ← AI가 구현
5. 테스트 실행 → 통과 확인      ← 내가 검증
6. AI에게 UI + DOM 요청        ← AI가 구현
7. Bug Hunt → 문제 발견        ← 내가 검증
8. AI에게 수정 요청            ← AI가 수정
9. 최종 확인                    ← 내가 승인
```

> 이 흐름이 Phase 3(날씨 앱, 영화 앱)에서도 동일하게 반복됩니다.

### 다음 장 미리보기

**Phase 3: AI-Native 개발**

이제부터는 AI를 단순한 코드 생성기가 아닌 **진정한 협업 파트너**로 활용합니다.

```
12장: Custom Instructions — AI에게 프로젝트 규칙 알려주기
13장: Prompt Files + Context Engineering — 반복 작업 템플릿
14장: Custom Agent — AI에게 전문가 역할 부여
15장: TDD — 요구사항으로 테스트하고 AI가 구현
16장: 통합 프로젝트: 날씨 앱 — 전체 AI-Native 파이프라인
17장: 통합 프로젝트: 영화 앱 — 독립 AI-Native 실행
```

Phase 3에서는 여러분이 **설계**하고, AI가 **구현**하고, 테스트로 **검증**하는 완전한 AI-Native 워크플로우를 경험하게 됩니다.

---

*Phase 2를 완주한 것을 축하합니다. 이제 AI와 함께 진짜 개발을 시작할 준비가 됐습니다.*


→ **다음 내용으로 넘어갑시다**: [12. Custom Instructions](/ai-native-js/instructions)
