---
title: 13. Prompt Files + Context Engineering
layout: default
parent: AI-Native JavaScript
nav_order: 14
permalink: /ai-native-js/prompts
---
{% raw %}

# 13장. Prompt Files + Context Engineering

{: .no_toc }

> **Phase 3**

> 🚀 **도전 챕터** — 여유가 있다면 도전해 보세요! 핵심 개념만 알아도 충분합니다.

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

- Prompt File(`.prompt.md`)을 만들고 사용할 수 있다
- 동적 변수(`{{variable}}`)를 활용할 수 있다
- Context Packet(맥락 꾸러미)을 구성할 수 있다

`<a id="toc"></a>`

## 진행 순서

1. [Prompt File이란?](#part1) — "단골 주문서" 비유
2. [첫 Prompt File 만들기](#part2) — new-feature.prompt.md
3. [더 많은 Prompt Files](#part3) — 테스트, 디버그, 리뷰 템플릿
4. [Context Engineering](#part4) — AI에게 맥락 꾸러미 전달하기
5. [좋은 프롬프트 vs 나쁜 프롬프트](#part5) — 비교와 개선
6. [실습 과제](#part6) — 기본 / 도전
7. [정리](#part7) — 핵심 요약 및 다음 장

---

`<a id="part1"></a>`

## 1. ⭐ **핵심** — Prompt File이란? [↑](#toc)

> 카페를 자주 가는 단골손님을 생각해보세요.
> 매번 "아이스 아메리카노 큰 걸로, 샷 추가하고, 시럽은 빼주세요"를 말하는 대신,
> 단골 주문서를 만들어두면 어떨까요? "항상 먹던 걸로요" 한 마디면 끝입니다.

**Prompt File**이 바로 그 단골 주문서입니다.

### Prompt File vs Custom Instructions

| 구분             | Custom Instructions                 | Prompt File                     |
| ---------------- | ----------------------------------- | ------------------------------- |
| **형태**   | 항상 자동 적용되는 규칙             | 필요할 때 직접 실행하는 템플릿  |
| **비유**   | 회사 규칙서                         | 업무 요청 양식                  |
| **위치**   | `.github/copilot-instructions.md` | `.github/prompts/*.prompt.md` |
| **사용법** | 자동                                | Chat에서 `/파일명` 입력       |

### Prompt File로 무엇을 할 수 있나?

Prompt File은 자주 반복하는 요청을 파일로 저장해두는 것입니다.

```
반복 요청의 예:
- "이 파일에 대한 테스트를 Vitest로 작성해줘"
- "이 함수에 어떤 버그가 있는지 리뷰해줘"  
- "새 기능을 추가해줘. 구현 코드와 테스트 코드를 같이 만들어줘"
```

이런 요청을 매번 타이핑하는 대신, 파일로 만들어두고 `/new-feature`, `/write-tests`, `/debug-code`처럼 간단히 호출합니다.

---

`<a id="part2"></a>`

## 2. 🚀 **도전** — 첫 Prompt File 만들기 [↑](#toc)

> 강사 시연을 보면서 따라하세요

가장 자주 쓰는 요청인 "새 기능 추가"를 Prompt File로 만들어봅시다.

### Prompt File 작성 전에 — 2가지 질문

11장에서 4가지 질문, 12장에서 5가지 질문을 던졌습니다. Prompt File을 만들기 전에도 2가지를 먼저 생각합니다.

**질문 1. 어떤 요청을 자주 반복하는가?**

> Copilot Chat에서 같은 말을 여러 번 타이핑한 적이 있나요?

- "새 기능 추가해줘" (구현 + 테스트)
- "이 파일 테스트 작성해줘"
- "이 코드 디버깅해줘"
- "이 코드 리뷰해줘"

→ 이것이 Prompt File의 **후보 목록**이 됩니다. 자주 반복하는 요청이 곧 템플릿이 될 파일입니다.

**질문 2. 그 요청에 매번 포함되는 정보는 무엇인가?**

> 요청할 때 매번 적어야 하는 내용을 정리합니다.

- 어떤 파일을 참고하나? → `#file:` 참조
- 어떤 규칙을 따라야 하나? → 작업 규칙 섹션
- 어떻게 되면 끝인가? → 완료 기준
- 매번 달라지는 값은? → `{{변수}}`로 처리

→ 이것이 Prompt File의 **섹션 구조**가 됩니다.

> 💡 이 2가지 질문에 답하면, 아래 Prompt File의 구조가 자연스럽게 나옵니다.
> 섹션 4에서 배울 "Context Packet"은 이 구조를 더 체계적으로 정리하는 프레임워크입니다.

### 폴더 생성

```bash
mkdir -p .github/prompts
```

### new-feature.prompt.md 작성

`.github/prompts/new-feature.prompt.md` 파일을 만들고 아래 내용을 작성합니다.

```markdown
---
description: "새 기능을 추가할 때 사용한다. 구현 코드와 Vitest 테스트를 함께 생성한다."
mode: "agent"
---

# 새 기능 추가 요청

## 기능 이름
{{feature_name}}

## 요구사항
{{requirements}}

## 작업 규칙
- `src/` 폴더에 구현 코드를 작성한다
- `tests/` 폴더에 Vitest 테스트 코드를 작성한다
- 기존 코드 스타일을 반드시 따른다
- 한국어 주석을 사용한다
- 함수는 하나의 일만 한다
- 에러 처리를 반드시 포함한다

## 참고 파일
#file:src/todo.js

## 완료 기준
- 구현 코드가 동작한다
- 모든 테스트가 통과한다
- 기존 테스트가 깨지지 않는다
```

### Frontmatter 설명

```yaml
---
description: "..."   ← Copilot이 이 파일이 무엇인지 이해하는 설명
mode: "agent"        ← Agent 모드로 실행 (파일 생성, 편집 가능)
---
```

`mode: "agent"`로 설정하면 Copilot이 실제로 파일을 만들고 편집할 수 있습니다. 단순히 답변만 하는 것이 아니라 코드를 직접 작성해줍니다.

> **혼동 주의**: 여기서 `mode: "agent"`는 Prompt File의 **실행 권한 설정**이지, 14장에서 배울 **Custom Agent**와는 다른 개념입니다.
>
> |                     | Prompt File의 `mode: "agent"`           | 14장 Custom Agent                  |
> | ------------------- | ----------------------------------------- | ---------------------------------- |
> | **파일 위치** | `.github/prompts/`                      | `.github/agents/`                |
> | **의미**      | "이 프롬프트 실행 시 파일 생성/편집 허용" | "AI에게 지속적인 전문가 역할 부여" |
> | **지속성**    | 1회 실행 후 끝                            | 대화 내내 역할 유지                |
> | **비유**      | 업무 요청서에 "파일 수정 권한 포함" 도장  | "너는 TDD 전문가야"                |

### `{{변수}}` 문법

Prompt File의 특별한 기능은 **동적 변수**입니다.

```markdown
## 기능 이름
{{feature_name}}    ← 실행 시 직접 입력하는 값
```

이 파일을 실행하면 Copilot이 `{{feature_name}}`과 `{{requirements}}`에 무엇을 넣을지 물어봅니다.

```
예시:
feature_name = "검색 기능"
requirements = "키워드로 할 일을 검색하는 searchTodos 함수, 대소문자 구분 없이 검색"
```

### 사용 방법

Copilot Chat을 열고 (단축키: `Ctrl+Shift+I` 또는 `Cmd+Shift+I`) Agent 모드로 전환한 뒤:

```
/new-feature
```

를 입력하거나, 프롬프트 파일 목록에서 선택합니다.

> **`#file:src/todo.js` 는 무엇인가요?**
> Copilot Chat에서 `#file:경로` 형식으로 특정 파일을 맥락으로 포함시킬 수 있습니다. AI가 기존 코드의 스타일과 구조를 참고하여 일관된 코드를 생성합니다.

---

`<a id="part3"></a>`

## 3. 📖 **더 알아보기** — 더 많은 Prompt Files [↑](#toc)

자주 쓰는 작업들을 Prompt File로 만들어봅시다.

### write-tests.prompt.md — 테스트 작성 템플릿

`.github/prompts/write-tests.prompt.md`:

```markdown
---
description: "기존 코드에 대한 Vitest 테스트를 작성할 때 사용한다."
mode: "agent"
---

# 테스트 작성 요청

## 테스트할 파일
#file:{{file_path}}

## 작업 지시
위 파일의 모든 함수에 대한 Vitest 테스트를 작성해줘.

## 테스트 작성 규칙
- AAA 패턴 사용 (Arrange, Act, Assert)
- 각 함수당 최소 3가지 케이스: 정상, 경계값, 에러
- 테스트 설명은 한국어로 ("~하면 ~를 반환한다")
- `describe`로 함수별로 그룹화
- 파일명은 원본 파일명 + `.test.js`

## 테스트 파일 위치
`tests/` 폴더에 저장한다.
```

**사용 예:**

```
/write-tests
file_path = src/storage.js
```

### debug-code.prompt.md — 디버깅 템플릿

`.github/prompts/debug-code.prompt.md`:

```markdown
---
description: "코드가 예상대로 동작하지 않을 때 원인을 찾고 수정하기 위해 사용한다."
mode: "agent"
---

# 디버깅 요청

## 문제 파일
#file:{{file_path}}

## 예상 동작
{{expected_behavior}}

## 실제 동작
{{actual_behavior}}

## 에러 메시지 (있으면)
{{error_message}}

## 요청 사항
1. 위 파일에서 문제의 원인을 찾아줘
2. 원인을 한국어로 설명해줘
3. 수정된 코드를 제시해줘
4. 수정 후 테스트 방법도 알려줘
```

**사용 예:**

```
/debug-code
file_path = src/api.js
expected_behavior = fetchTodos 함수가 할 일 배열을 반환해야 한다
actual_behavior = undefined를 반환한다
error_message = TypeError: Cannot read properties of undefined
```

### code-review.prompt.md — 코드 리뷰 템플릿

`.github/prompts/code-review.prompt.md`:

```markdown
---
description: "작성한 코드의 품질을 리뷰받고 개선점을 찾을 때 사용한다."
mode: "chat"
---

# 코드 리뷰 요청

## 리뷰할 파일
#file:{{file_path}}

## 리뷰 기준
아래 항목들을 기준으로 코드를 리뷰해줘:

### 코드 품질
- 함수가 너무 길지 않은가? (20줄 이하 권장)
- 변수명이 의미 있는가?
- 중복 코드가 있는가?

### 안전성
- 에러 처리가 되어 있는가?
- 예상치 못한 입력에도 동작하는가?
- 보안 문제가 있는가?

### 테스트 가능성
- 함수를 쉽게 테스트할 수 있는가?
- 의존성이 너무 많지 않은가?

## 출력 형식
- 발견한 문제점을 번호로 정리해줘
- 각 문제에 대해 개선된 코드 예시를 보여줘
- 전체 평가(A/B/C)와 총평을 한국어로 작성해줘
```

### 완성된 Prompt Files 구조

```
.github/
└── prompts/
    ├── new-feature.prompt.md    ← 새 기능 추가
    ├── write-tests.prompt.md    ← 테스트 작성
    ├── debug-code.prompt.md     ← 디버깅
    └── code-review.prompt.md    ← 코드 리뷰
```

---

`<a id="part4"></a>`

## 4. 📖 **더 알아보기** — Context Engineering [↑](#toc)

> 형사가 사건을 수사할 때를 생각해보세요.
> "범인을 잡아줘"라고만 하면 어디서 시작해야 할지 모릅니다.
> 하지만 "이 장소에서, 이 시간에, 이런 증거가 있고, 용의자는 이 사람들입니다"라고 맥락을 제공하면 훨씬 빠르게 수사를 진행할 수 있죠.
> AI도 마찬가지입니다. 맥락을 많이 줄수록 더 좋은 결과를 냅니다.

### Context Packet — 맥락 꾸러미

좋은 AI 요청에는 5가지 요소가 있습니다. 이를 **Context Packet(맥락 꾸러미)**이라고 합니다.

> 💡 11장에서 작성한 `requirements.md`를 떠올려보세요. 기능 요구사항, 제약 조건, 범위 밖, 금지 사항 — 이것이 바로 Context Packet의 요소들입니다. requirements.md는 프로젝트 전체의 맥락이고, Context Packet은 개별 요청마다의 맥락입니다.

```
1. 목표 (Goal)
   무엇을 만들 것인가?
   "searchTodos 함수를 만들어줘"

2. 참고 파일 (References)
   어떤 기존 코드를 참고할 것인가?
   "#file:src/todo.js — 기존 todos 배열 구조 참고"

3. 제약 조건 (Constraints)
   무엇을 지켜야 하는가?
   "filter 메서드 사용, 대소문자 구분 없이 검색"

4. 완료 기준 (Done Criteria)
   어떻게 되면 끝인가?
   "Vitest 테스트 3개가 모두 통과하면 완료"

5. 제외 사항 (Exclusions)
   무엇을 건드리지 말 것인가?
   "기존 addTodo, deleteTodo 함수는 수정하지 말 것"
```

### 실제 Context Packet 예시: ToDo 앱에 검색 기능 추가

**맥락 꾸러미 없는 요청:**

```
검색 기능 만들어줘
```

결과: AI가 어떤 구조로 만들지, 어디에 추가할지, 테스트는 어떻게 작성할지 알 수 없어서 엉뚱한 코드가 나올 수 있습니다.

**맥락 꾸러미가 있는 요청:**

```
[목표]
todo.js의 todos 배열에서 키워드로 할 일을 검색하는 searchTodos 함수를 추가해줘.

[참고 파일]
#file:src/todo.js — todos 배열과 기존 함수 구조 참고

[제약 조건]
- Array.filter 메서드를 사용할 것
- 대소문자 구분 없이 검색 (toLowerCase 사용)
- 검색어가 빈 문자열이면 전체 목록 반환

[완료 기준]
- searchTodos('밥') → '밥' 포함된 할 일만 반환
- searchTodos('') → 전체 할 일 반환
- searchTodos('없는것') → 빈 배열 반환
- 위 3가지 Vitest 테스트가 모두 통과

[제외 사항]
- 기존 addTodo, deleteTodo, getTodos 함수 수정 금지
```

훨씬 구체적이고 명확합니다. AI가 정확히 무엇을 만들어야 하는지 알 수 있습니다.

### Context Packet을 Prompt File에 넣기

앞서 만든 `new-feature.prompt.md`가 바로 Context Packet 구조를 가지고 있습니다.

```markdown
## 기능 이름         ← 목표 (Goal)
{{feature_name}}

## 요구사항          ← 제약 조건 (Constraints)
{{requirements}}

## 참고 파일         ← 참고 파일 (References)
#file:src/todo.js

## 완료 기준         ← 완료 기준 (Done Criteria)
- 구현 코드가 동작한다
- 모든 테스트가 통과한다
- 기존 테스트가 깨지지 않는다

## 작업 규칙         ← 제외 사항 포함 (Exclusions)
- 기존 코드 스타일을 반드시 따른다
```

---

`<a id="part5"></a>`

## 5. 좋은 프롬프트 vs 나쁜 프롬프트 [↑](#toc)

### 비교 1: 검색 기능 요청

| 나쁜 프롬프트           | 좋은 프롬프트                                                                                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ❌ "검색 기능 만들어줘" | ✅ "todo.js의 todos 배열에서 키워드로 할 일을 검색하는 searchTodos 함수를 만들어줘. Vitest 테스트도 포함. filter 메서드 사용. 대소문자 구분 없이 검색." |

### 비교 2: 테스트 요청

| 나쁜 프롬프트        | 좋은 프롬프트                                                                                                                                                                       |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ❌ "테스트 작성해줘" | ✅ "src/storage.js의 saveSearch와 getHistory 함수에 대한 Vitest 테스트를 tests/storage.test.js에 작성해줘. 각 함수당 정상 케이스, 빈 값 케이스, 에러 케이스를 포함. AAA 패턴 사용." |

### 비교 3: 버그 수정 요청

| 나쁜 프롬프트    | 좋은 프롬프트                                                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ❌ "버그 고쳐줘" | ✅ "src/api.js의 fetchWeather 함수에서 도시명이 한국어일 때 undefined를 반환하는 버그가 있어. encodeURIComponent를 사용해서 수정해줘. 기존 테스트는 깨지면 안 돼." |

### 좋은 프롬프트의 공통점

1. **무엇을**: 함수명, 파일명, 기능을 구체적으로 명시
2. **어디서**: 파일 경로, 위치를 명시
3. **어떻게**: 사용할 방법, 패턴, 도구를 명시
4. **언제 끝**: 성공 기준을 명시
5. **무엇이 아닌지**: 건드리지 말 것을 명시

### 프롬프트 개선 연습

아래 나쁜 프롬프트를 좋은 프롬프트로 바꿔보세요.

```
❌ "정렬 기능 추가해줘"

↓ 직접 개선해보세요:
✅ "..."
```

**힌트:**

- 어떤 배열을 정렬하나요?
- 어떤 기준으로 정렬하나요? (날짜, 이름, 중요도?)
- 어떤 파일에 추가하나요?
- 정렬 전/후 결과가 어떻게 달라야 하나요?

---

`<a id="part6"></a>`

## 6. 실습 과제 [↑](#toc)

### 기본 과제: write-tests.prompt.md 만들고 실제 사용하기

1. `.github/prompts/write-tests.prompt.md` 파일을 이번 장의 예시를 참고하여 만드세요.
2. ToDo 앱의 `src/todo.js` 파일에 대한 테스트를 이 Prompt File을 사용해서 요청하세요.
3. 생성된 테스트를 실행해보세요.

```bash
npx vitest
```

**확인 체크리스트:**

| 항목                                                | 확인 |
| --------------------------------------------------- | :--: |
| `.github/prompts/write-tests.prompt.md` 생성 완료 |  ☐  |
| Prompt File에 `{{file_path}}` 변수 포함           |  ☐  |
| AAA 패턴 규칙이 Prompt File에 명시됨                |  ☐  |
| 생성된 테스트가 실제로 실행됨                       |  ☐  |
| 최소 3개 테스트가 통과함                            |  ☐  |

---

### 도전 과제: Context Packet으로 검색 기능 구현하기

Context Packet 5요소를 모두 포함한 요청으로 ToDo 앱에 검색 기능을 추가해보세요.

**요구사항:**

- 함수명: `searchTodos(keyword)`
- 위치: `src/todo.js`
- 동작: `keyword`를 포함하는 할 일만 반환
- 대소문자 구분 없이 검색
- `keyword`가 빈 문자열이면 전체 반환

**단계:**

1. Context Packet 작성 (5가지 요소 모두 포함)
2. Copilot Chat에 요청
3. 생성된 코드 확인 및 검증
4. 테스트 실행

```javascript
// 예상 동작 예시
const todos = [
  { id: 1, text: '밥 먹기', done: false },
  { id: 2, text: '운동하기', done: false },
  { id: 3, text: '밥상 차리기', done: true }
];

searchTodos('밥');
// → [{ id: 1, text: '밥 먹기', done: false }, { id: 3, text: '밥상 차리기', done: true }]

searchTodos('');
// → (todos 전체 배열)

searchTodos('없는것');
// → []
```

---

`<a id="part7"></a>`

## 7. 정리 [↑](#toc)

이번 장에서 배운 내용을 정리합니다.

| 개념                        | 설명                                                   |
| --------------------------- | ------------------------------------------------------ |
| **Prompt File**       | 자주 쓰는 AI 요청을 파일로 저장한 템플릿               |
| **`{{변수}}`**      | 실행 시 값을 입력받는 동적 변수                        |
| **`mode: "agent"`** | Copilot이 파일을 직접 만들고 수정하는 모드             |
| **`#file:경로`**    | 특정 파일을 맥락으로 포함시키는 참조 문법              |
| **Context Packet**    | 목표, 참고 파일, 제약 조건, 완료 기준, 제외 사항 5요소 |

**핵심 원칙:**

- Prompt File은 반복 작업의 자동화 도구
- 좋은 프롬프트 = 구체적인 목표 + 참고 파일 + 제약 조건 + 완료 기준
- Context가 많을수록 AI 출력의 품질이 높아짐

---

### 📖 더 알아보기: 다른 AI 도구의 작업 템플릿

12장에서 Custom Instructions를 비교했듯이, Prompt Files도 도구마다 이름이 다릅니다.

| 개념                  | GitHub Copilot                  | Claude Code                     | Codex (OpenAI)       |
| --------------------- | ------------------------------- | ------------------------------- | -------------------- |
| **작업 템플릿** | `.github/prompts/*.prompt.md` | `.claude/commands/*.md`       | — (직접 프롬프트)   |
| **실행 방법**   | Copilot Chat에서 파일 참조      | `/명령어` 슬래시 커맨드       | 프롬프트에 직접 작성 |
| **변수 지원**   | 이중 중괄호 변수 문법           | `$ARGUMENTS`                  | —                   |
| **AI 에이전트** | `.github/agents/*.md`         | 에이전트 시스템 내장 (subagent) | 에이전트 시스템 내장 |

> 💡 **공통 원칙**: "자주 하는 요청을 파일로 저장하고 재사용한다."
> 도구가 바뀌어도 이 원칙은 동일합니다.

---

### 다음 장 미리보기

Custom Instructions로 규칙을 알려주고, Prompt Files로 반복 작업을 자동화했습니다. 다음 장에서는 AI-Native 도구의 마지막 퍼즐 — **Custom Agent**를 배웁니다. AI에게 "TDD 전문가" 같은 역할을 부여하는 방법입니다.

→ **다음 장**: [14. Custom Agent — AI에게 전문가 역할 부여](/ai-native-js/agent)
{% endraw %}
