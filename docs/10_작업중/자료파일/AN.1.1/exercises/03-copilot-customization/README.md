# 03. Copilot 커스터마이징 구조 이해

## 목표

GitHub Copilot의 세 가지 커스터마이징 요소가 무엇인지, 각각 언제 어떻게 사용하는지 이해합니다.

---

## 배경 지식

### 1) 세 가지 커스터마이징 요소

| 요소 | 파일 형식 | 위치 | 역할 |
|------|-----------|------|------|
| **Custom Instructions** | `.github/copilot-instructions.md`, `AGENTS.md`, `*.instructions.md` | `.github/`, 워크스페이스 루트, `.github/instructions/` | AI에게 프로젝트 규칙·컨벤션을 알려주는 지침 |
| **Prompt Files** | `*.prompt.md` | `.github/prompts/` | 자주 쓰는 요청을 재사용 가능한 템플릿으로 저장 |
| **Custom Agents** | `*.agent.md` | `.github/agents/` | 특정 역할과 도구 제한을 가진 전문화된 AI 모드 |

#### 컨텍스트 레이어 한눈에 보기

Copilot 내부 시스템 프롬프트 전문은 공개되지 않았지만,
실무에서 제어 가능한 컨텍스트 레이어는 아래처럼 이해하면 됩니다.

| 레이어 | 예시 | 정의 위치 | 배치 시점 |
|------|------|-----------|-----------|
| 시스템 레이어(비공개) | 안전 정책, 제품 기본 지시문 | Copilot 서비스 내부 | 모든 요청에 항상 포함 |
| 공통 지침 | `.github/copilot-instructions.md`, `AGENTS.md` | 저장소 루트/.github | 대체로 모든 채팅 요청 |
| 조건부 지침 | `.github/instructions/*.instructions.md` + `applyTo` | `.github/instructions/` | 현재 파일/작업이 패턴과 맞을 때 |
| 실행형 템플릿 | `.github/prompts/*.prompt.md` | `.github/prompts/` | Chat에서 `/프롬프트` 실행 시 |
| 역할/도구 제약 | `.github/agents/*.agent.md` | `.github/agents/` | 해당 에이전트 모드 선택 시 |
| 사용자 입력 | Chat 메시지, `${selection}`, `#codebase` 등 | Chat 입력창 | 메시지 전송 시 |
| 세션 기록 | 같은 대화의 이전 메시지 | Chat 세션 | 연속 대화 동안 누적 |

핵심 요약:

- 시스템 레이어는 수정 불가, 나머지 레이어는 팀에서 설계 가능
- `.github/` 파일은 규칙의 정식 소스, Chat 입력은 작업 순간의 의도/범위
- 같은 규칙을 여러 위치에 중복 작성하면 결과 편차가 커짐

#### 메모리 위치 한눈에 보기

실습 에이전트 환경에서는 메모리를 아래처럼 구분해 사용합니다.

| 메모리 종류 | 경로 | 용도 |
|------------|------|------|
| 사용자 메모리 | `/memories/` | 대화 간 유지되는 개인 선호/규칙 |
| 세션 메모리 | `/memories/session/` | 현재 대화에서만 쓰는 작업 메모 |
| 저장소 메모리 | `/memories/repo/` | 현재 저장소에만 의미 있는 규칙/사실 |

오해 방지:

| 표기 | 의미 | VS Code 탐색기에서 폴더로 보이나? |
|------|------|-------------------------------|
| `/memories/...` | 에이전트 전용 메모리 네임스페이스(논리 경로) | 아니오 |
| `.github/...` | 실제 워크스페이스 파일 경로 | 예 |

중요한 구분:

- 메모리 경로는 작업 보조용 기록 저장소
- 팀 규칙의 정식 소스는 `.github/` 하위 파일
- `/memories/...`는 일반 파일 탐색 경로가 아니므로, 탐색기에서 찾을 수 없습니다.

팀 규칙 파일 예시:

- `.github/copilot-instructions.md`
- `.github/instructions/*.instructions.md`
- `.github/prompts/*.prompt.md`
- `.github/agents/*.agent.md`

확인 방법(실습 환경):

- `/memories/` 경로는 에이전트의 memory 조회 기능으로 확인합니다.
- 반대로 `.github/` 파일은 VS Code 탐색기에서 직접 열어 확인합니다.

### 2) 결정 기준

```
이 설정이 모든 작업에 항상 적용되어야 하는가?
    YES → `.github/copilot-instructions.md` (기본) 또는 `AGENTS.md` (여러 에이전트/모노레포)

특정 파일 유형/경로에만 규칙을 적용해야 하는가?
    YES → `*.instructions.md`

특정 반복 작업을 템플릿화하고 싶은가?
    YES → Prompt Files (`*.prompt.md`)

특정 역할을 가진 전용 에이전트가 필요한가?
    YES → Custom Agents (`*.agent.md`)
```

### 3) `copilot-instructions.md`, `*.instructions.md`, `AGENTS.md` 차이

교육생이 가장 많이 헷갈리는 부분은 "모두 지침 파일처럼 보이는데 뭐가 다른가?" 입니다.

핵심부터 정리하면:

- `.github/copilot-instructions.md` = **프로젝트 전체에 항상 적용되는 기본 지침**
- `*.instructions.md` = **특정 파일/폴더/언어에만 조건부로 적용되는 지침**
- `AGENTS.md` = **여러 AI 에이전트가 함께 볼 수 있는 항상 적용 지침**

#### 비교 표

| 파일 | 형식 | 적용 방식 | 위치 | 언제 쓰면 좋은가 |
|------|------|-----------|------|------------------|
| `.github/copilot-instructions.md` | 일반 Markdown | 워크스페이스의 모든 채팅 요청에 자동 적용 | `.github/` 폴더 | 프로젝트 전체 공통 규칙 1장을 만들고 싶을 때 |
| `*.instructions.md` | Markdown + 선택적 YAML frontmatter | `applyTo` 패턴이 맞는 파일에만 자동 적용, 또는 설명 기준으로 선택 적용 | `.github/instructions/` | 언어별/프레임워크별/폴더별 세부 규칙이 필요할 때 |
| `AGENTS.md` | 일반 Markdown | 워크스페이스 전체에 자동 적용, 하위 폴더별 파일도 실험적으로 가능 | 워크스페이스 루트 또는 하위 폴더 | 여러 AI 에이전트가 공통 규칙을 함께 보게 하고 싶을 때 |

#### 쉽게 구분하면

1. `copilot-instructions.md`
    - "이 프로젝트에서는 항상 이렇게 일해라"를 적는 파일입니다.
    - 예: 네이밍 규칙, 기본 라이브러리, 아키텍처 원칙, 에러 처리 원칙

2. `*.instructions.md`
    - "이 파일 종류에서는 이렇게 해라"를 적는 파일입니다.
    - 예: Python 파일에는 타입 힌트 강제, 테스트 파일에는 AAA 패턴 강제

3. `AGENTS.md`
    - "이 저장소에서 동작하는 여러 AI 에이전트가 공통으로 지켜야 할 규칙"을 적는 파일입니다.
    - VS Code 공식 문서 기준으로, 여러 AI 에이전트를 함께 쓸 때 공통 지침 파일로 적합합니다.

#### 실무 권장 방식

1. 먼저 `.github/copilot-instructions.md` 하나로 프로젝트 공통 규칙을 정리합니다.
2. 그다음 `*.instructions.md`를 추가해 언어별/폴더별 세부 규칙을 나눕니다.
3. 여러 에이전트나 모노레포(monorepo) 구조를 운영한다면 `AGENTS.md`를 검토합니다.

> 모노레포(monorepo)
> - 한 줄 정의: 여러 프로젝트, 패키지, 서비스를 하나의 저장소(repo)에서 함께 관리하는 방식입니다.
> - 반대 개념: 멀티레포(polyrepo), 프로젝트마다 저장소를 나누어 관리하는 방식입니다.
> - 이 수업 연결: `AGENTS.md` 또는 `*.instructions.md`를 경로 기준으로 나누어 운영할 때 자주 등장합니다.

#### 주의할 점

- VS Code는 여러 지침 파일을 함께 읽어 문맥에 넣을 수 있습니다.
- 같은 저장소 안에 서로 충돌하는 규칙을 넣으면 결과가 불안정해질 수 있습니다.
- 따라서 `copilot-instructions.md`에는 공통 규칙만, `*.instructions.md`에는 세부 규칙만 넣는 식으로 역할을 분리하는 것이 좋습니다.

### 4) YAML frontmatter 기초

Copilot 커스터마이징 파일을 처음 보면 맨 위에 아래와 비슷한 블록이 먼저 나옵니다.

참고:

- 여기서 설명하는 `YAML frontmatter`는 주로 `*.instructions.md`, `*.prompt.md`, `*.agent.md` 파일에서 자주 봅니다.
- `.github/copilot-instructions.md`와 `AGENTS.md`는 일반 Markdown 본문으로 사용하는 경우가 많습니다.

```yaml
---
description: "이 프롬프트는 새 기능 구현에 사용합니다."
name: "New Feature"
agent: "agent"
---
```

이 부분이 바로 `YAML frontmatter` 입니다.

#### YAML이란?

YAML은 사람이 읽기 쉽게 만든 설정 형식입니다.

- 프로그램 옵션이나 메타데이터를 적을 때 자주 사용합니다.
- `key: value` 형태로 정보를 적습니다.
- 들여쓰기가 구조를 결정합니다.
- JSON보다 사람이 읽고 수정하기 쉽다는 장점이 있습니다.

```yaml
description: "파이썬 코드 작성 시 사용"
applyTo: "**/*.py"
tools:
    - read
    - search
```

#### YAML을 읽을 때 알아야 할 기본 규칙

1. `key: value`가 기본 구조입니다.
2. 목록은 `-` 기호로 씁니다.
3. 들여쓰기는 매우 중요합니다. 보통 공백 2칸 또는 4칸을 사용합니다.
4. 탭(tab)보다 공백(space)을 쓰는 것이 안전합니다.
5. 값 안에 `:` 같은 문자가 들어가면 따옴표로 감싸는 것이 안전합니다.

#### YAML frontmatter란?

`frontmatter`는 문서의 **맨 앞(front)** 에 들어가는 **메타데이터 영역(matter)** 입니다.

- Markdown 본문 앞에 위치합니다.
- 보통 `---` 로 시작하고 `---` 로 끝납니다.
- 본문 내용 자체가 아니라, 이 문서를 Copilot이 어떻게 이해하고 사용할지 알려주는 설정입니다.

즉, 커스터마이징 파일은 크게 2부분으로 나뉩니다.

1. `YAML frontmatter`: 호출 조건, 이름, 적용 범위, 도구 같은 설정
2. 본문(body): 실제 지시문, 프롬프트 내용, 역할 설명

#### Copilot 커스터마이징에서 frontmatter가 중요한 이유

Copilot은 본문만 보는 것이 아니라, 맨 위의 YAML frontmatter를 보고 이 파일을 어떻게 다룰지 판단합니다.

- 이 파일을 언제 불러와야 하는지
- 어떤 파일에 자동 적용해야 하는지
- Chat `/` 목록에 어떤 이름으로 보여줄지
- 어떤 도구만 허용할지

즉, frontmatter가 잘못되면 본문을 잘 써도 기대한 방식으로 동작하지 않을 수 있습니다.

#### 자주 보는 항목 설명

| 항목 | 의미 | 어디서 자주 쓰나 |
|------|------|------------------|
| `description` | 이 파일을 언제 써야 하는지 설명 | instructions, prompts, agents 공통 |
| `applyTo` | 어떤 파일 패턴에 규칙을 적용할지 지정 | instructions |
| `name` | UI나 목록에서 보여줄 이름 | prompts, agents |
| `agent` | 어떤 실행 모드/에이전트로 실행할지 지정 | prompts |
| `tools` | 사용할 수 있는 도구를 제한 | agents |

이 과정에서의 운영 규칙:
- `description`와 본문은 한글로 작성
- `name`은 영문으로 작성
- `applyTo`, `agent`, `tools` 같은 키 이름은 그대로 유지

#### 예시로 보는 frontmatter 해석

**Instructions 예시**

```yaml
---
description: "이 프로젝트에서 파이썬 코드를 작성할 때 사용합니다."
applyTo: "**/*.py"
---
```

해석:

- 파이썬 파일 작업일 때 이 지침을 참고하라는 뜻입니다.
- 모든 파일이 아니라 `**/*.py` 패턴에만 적용됩니다.

**Prompt 예시**

```yaml
---
description: "Todo Manager 프로젝트에 새 기능과 테스트를 함께 추가할 때 사용합니다."
name: "New Feature"
agent: "agent"
---
```

해석:

- 새 기능 구현용 프롬프트입니다.
- 목록에는 `New Feature` 라는 이름으로 보입니다.
- 실행 시 `agent` 모드로 동작합니다.

**Agent 예시**

```yaml
---
description: "코드 품질, 명명, 구조를 검토할 때 사용합니다."
name: "Code Reviewer"
tools: [read, search]
---
```

해석:

- 코드 리뷰 전용 에이전트입니다.
- 이름은 `Code Reviewer` 로 표시됩니다.
- 수정 도구 없이 `read`, `search`만 사용하도록 제한됩니다.

#### 한 줄로 기억하기

- YAML = 설정을 적는 형식
- YAML frontmatter = 문서 맨 위의 설정 블록
- 본문 = 실제로 Copilot에게 전달할 규칙/요청/역할 설명

---

## 실습 단계

### 0단계: 예시 파일 탐색 준비

1. 이 실습 폴더의 `examples/` 디렉토리를 확인합니다.

   ```text
   exercises/03-copilot-customization/examples/
   ├── sample.instructions.md
   ├── sample.prompt.md
   └── sample.agent.md
   ```

2. VS Code 탐색기에서 각 파일이 존재하는지 확인합니다.
3. 각 파일을 순서대로 열어 `frontmatter`와 본문 구조를 파악할 준비를 합니다.

### 1단계: 예시 파일 읽기와 분석

아래 3개 파일을 순서대로 읽고, 각 파일의 역할을 확인합니다.

| 파일 | 형식(구조) | 핵심 내용 | 용도(언제 쓰나) | 사용 사례 |
|------|------------|-----------|------------------|-----------|
| [sample.instructions.md](examples/sample.instructions.md) | `YAML frontmatter` + 지침 본문 (`description`, `applyTo`) | Python 네이밍, 타입 힌트, 함수 설계 규칙 | 특정 파일 패턴(`**/*.py`)에 상시 규칙 적용 | 팀 Python 컨벤션을 자동 반영해 코드 생성/수정 일관성 확보 |
| [sample.prompt.md](examples/sample.prompt.md) | `YAML frontmatter` + 재사용 프롬프트 템플릿 (`name`, `agent`, `${input:...}`) | "New Feature" 요청 템플릿과 입력 변수(기능명/요구사항) | 반복되는 요청을 표준화해 동일한 출력 품질 유지 | 기능 추가 시 `/New Feature` 호출 → 메서드/테스트 생성 흐름 재사용 |
| [sample.agent.md](examples/sample.agent.md) | `YAML frontmatter` + 역할 지시문 + 제약 (`tools: [read, search]`) | 코드 리뷰 관점(명명/단일책임/테스트/중복)과 "수정 금지" 제약 | 역할 기반 전용 에이전트로 작업 모드 분리 | 구현 전에 Code Reviewer 에이전트로 품질 점검 후 개선 항목 도출 |

**파일별 읽는 순서:**

1. `frontmatter`를 먼저 본다: 이 파일이 언제 호출되는지(`description`), 어디에 적용되는지(`applyTo`), 어떤 실행 모드인지(`agent`, `tools`)를 결정한다.
2. 본문 지시를 본다: 실제 행동 규칙(무엇을 하고, 무엇을 하지 않는지)이 들어 있다.
3. 산출물을 예상해 본다: 이 파일을 적용했을 때 결과가 "규칙 적용"인지, "요청 템플릿 실행"인지, "역할 분리"인지 구분한다.

**실습 적용 예시:**

1. `sample.instructions.md`
    - 상황: Python 파일을 생성할 때마다 타입 힌트를 강제하고 싶다.
    - 적용: `.github/instructions/`로 옮겨 적용 후 Python 코드 생성을 요청한다.
    - 확인: 함수 시그니처와 반환 타입이 자동으로 포함되는지 본다.

2. `sample.prompt.md`
    - 상황: "새 기능 + 테스트" 요청을 매번 같은 형식으로 실행하고 싶다.
    - 적용: `.github/prompts/`에 두고 Chat의 `/` 메뉴에서 `New Feature`를 호출한다.
    - 확인: `src/todo/manager.py`, `tests/test_manager.py` 수정 제안이 일관되게 나오는지 본다.

3. `sample.agent.md`
    - 상황: 코드 수정 없이 리뷰 피드백만 받고 싶다.
    - 적용: `.github/agents/`에 두고 해당 에이전트 모드로 실행한다.
    - 확인: 도구 제한(`read`, `search`)을 지키며 실행 가능한 개선 제안이 나오는지 본다.

### 2단계: 3요소 적용 판단 연습

아래 상황에서 어떤 요소를 사용할지 결정 기준을 적용해 판단합니다.

| 상황 | 적합한 요소 |
|------|------------|
| 프로젝트에서 모든 Python 파일에 타입 힌트를 강제하고 싶다 | |
| 매번 비슷한 방식으로 새 기능을 추가 요청하고 싶다 | |
| 코드 리뷰할 때만 사용하는 읽기 전용 AI 모드가 필요하다 | |
| 프로젝트 전체에 항상 적용되는 코딩 규칙이 있다 | |
| 여러 AI 에이전트가 공통 지침을 함께 보게 하고 싶다 | |

정답 확인:

| 상황 | 적합한 요소 |
|------|------------|
| 프로젝트에서 모든 Python 파일에 타입 힌트를 강제하고 싶다 | `*.instructions.md` (`applyTo: "**/*.py"`) |
| 매번 비슷한 방식으로 새 기능을 추가 요청하고 싶다 | Prompt Files (`*.prompt.md`) |
| 코드 리뷰할 때만 사용하는 읽기 전용 AI 모드가 필요하다 | Custom Agents (`*.agent.md`) |
| 프로젝트 전체에 항상 적용되는 코딩 규칙이 있다 | `.github/copilot-instructions.md` |
| 여러 AI 에이전트가 공통 지침을 함께 보게 하고 싶다 | `AGENTS.md` |

---

## 체크리스트

- [ ] 3요소(Custom Instructions, Prompt Files, Custom Agents)의 역할 차이를 설명할 수 있다
- [ ] `copilot-instructions.md` vs `*.instructions.md` vs `AGENTS.md` 차이를 구분할 수 있다
- [ ] YAML frontmatter의 `description`, `applyTo`, `name`, `tools` 항목이 무엇인지 알 수 있다
- [ ] `examples/` 폴더의 3개 파일을 읽고 각각의 역할을 설명할 수 있다
- [ ] 주어진 상황에서 어떤 요소를 써야 할지 결정 기준을 적용할 수 있다

---

## 자주 발생하는 문제와 해결

### `applyTo`를 너무 넓게 잡아 모든 파일에 불필요하게 적용될 때

- `applyTo: "**"` 대신 `applyTo: "**/*.py"`처럼 파일 패턴을 구체적으로 지정한다.
- 관련 파일에만 적용해야 불필요한 컨텍스트 낭비를 줄일 수 있다.

### `description`이 너무 짧아 언제 써야 할지 불분명할 때

- "파이썬 규칙" 대신 "Todo Manager 프로젝트에서 Python 파일을 작성할 때 적용할 네이밍/타입 힌트 규칙"처럼 구체적으로 작성한다.

### `:` 뒤 값이 없거나 들여쓰기가 혼용될 때

- YAML은 들여쓰기가 구조를 결정한다. 탭 대신 공백(2칸 또는 4칸)만 사용한다.
- 값 안에 `:` 같은 특수문자가 있으면 따옴표로 감싼다.

### `name`을 한글/영문 기준 없이 섞어 UI 이름이 들쭉날쭉할 때

- 이 과정 규칙: `name`은 영문으로 작성한다.
- Chat `/` 목록에서 일관된 이름이 표시되어야 프롬프트를 빠르게 찾을 수 있다.

### frontmatter `---`가 누락되어 파일이 지침으로 인식되지 않을 때

- 파일 맨 첫 줄이 `---`로 시작하고, frontmatter 블록이 `---`로 끝나야 한다.
- 빈 줄이 `---`보다 앞에 오면 frontmatter로 인식되지 않는다.

---

## 참고

### 에이전트 스킬 (다음 과정)

이 과정에서는 Custom Instructions, Prompt Files, Custom Agents 3요소를 중심으로 실습합니다.  
Agent Skills는 특정 도메인의 지식과 절차를 하나의 스킬 단위로 패키징하여, 에이전트가 필요할 때 불러 쓰도록 설계하는 방식입니다.

| 비교 항목 | 이 과정의 3요소 | Agent Skills (다음 과정) |
|------|------|------|
| 목적 | Copilot 동작 규칙/요청/역할을 프로젝트 단위로 설계 | 도메인별 작업 능력을 재사용 가능한 "스킬"로 제공 |
| 적용 범위 | 현재 워크스페이스와 과제 중심 | 여러 프로젝트/업무에서 재사용 가능한 전문 역량 단위 |
| 학습 시점 | 본 과정에서 실습 | 다음 과정에서 실습 |

> Agent Skills는 본 과정 범위를 넘어서는 확장 주제이며, 후속 과정에서 별도로 다룹니다.

### YAML 이해 확인 (미니 퀴즈)

**1번.** YAML frontmatter와 본문의 차이를 한 문장으로 설명해보세요.

**2번.** 아래 frontmatter에서 `description`, `name`, `tools`는 각각 어떤 역할을 하나요?

```yaml
---
description: "코드 리뷰용 에이전트입니다."
name: "Code Reviewer"
tools: [read, search]
---
```

**3번.** 다음 두 `applyTo` 중 파이썬 프로젝트 규칙에 더 적절한 것은 무엇인가요? 이유도 함께 말해보세요.

```yaml
applyTo: "**"
```

```yaml
applyTo: "**/*.py"
```

**정답 확인 포인트:**

- frontmatter는 문서 맨 위의 설정 블록이고, 본문은 실제 지시/요청/역할 설명이다.
- `description`은 언제 쓰는지 설명하고, `name`은 목록에 보이는 이름이며, `tools`는 사용할 수 있는 도구를 제한한다.
- 파이썬 규칙이라면 `applyTo: "**/*.py"`가 더 적절하다. 관련 파일에만 적용되어 불필요한 컨텍스트 낭비를 줄일 수 있기 때문이다.

---

## 다음 단계

3교시 이후 각 요소를 Todo Manager 프로젝트에 직접 적용합니다.  
→ **4교시**: `../04-custom-instructions/` 에서 실습 시작
