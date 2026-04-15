---
title: 03. Copilot 커스터마이징과 Custom Instructions
layout: default
parent: AI-Native Development
nav_order: 3
permalink: /ai-native/instructions
---

# 03장. Copilot 커스터마이징과 Custom Instructions
{: .no_toc }

## 학습 목표

- Copilot의 3가지 커스터마이징 요소를 구분하고 선택 기준을 설명할 수 있다
- Custom Instructions 파일을 작성하여 Copilot의 코드 생성 품질을 높일 수 있다

<a id="toc"></a>

## 진행 순서

1. [Copilot을 "우리 프로젝트에 맞게" 바꾸기](#part1) — 커스터마이징 3요소 소개
2. [YAML Frontmatter 기초](#part2) — 파일 설정 블록 이해
3. [실습: copilot-instructions.md 작성](#part3) — 프로젝트 공통 규칙
4. [실습: *.instructions.md 작성](#part4) — 파일별 세부 규칙
5. [동작 확인](#part5) — Copilot이 규칙을 따르는지 검증
6. [슬래시 명령으로 자동 생성하기](#part6) — `/create-instructions`, `/init`
7. [여기까지 되셨나요?](#part7) — 체크리스트
8. [정리](#part8) — 핵심 요약 및 다음 장

---

<a id="part1"></a>

## 1️⃣ Copilot을 "우리 프로젝트에 맞게" 바꾸기 [↑](#toc)

> 새 팀원에게 "우리 팀은 이렇게 합니다"라고 알려주지 않으면,
> 그 팀원은 자기 방식대로 일합니다.
> Copilot도 마찬가지입니다. 규칙을 알려주지 않으면 제멋대로 코드를 작성합니다.

GitHub Copilot을 프로젝트에 맞게 커스터마이징하는 방법은 3가지입니다.

### 커스터마이징 3요소

| 요소 | 비유 | 파일 위치 | 적용 시점 |
|------|------|-----------|----------|
| **Custom Instructions** | 팀 규칙서 | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md` | 항상 자동 적용 |
| **Prompt Files** | 업무 양식 | `.github/prompts/*.prompt.md` | Chat에서 `/명령` 실행 시 |
| **Custom Agents** | 전문 역할 직원 | `.github/agents/*.agent.md` | 에이전트 선택 시 |

### 어떤 것을 써야 할까?

```
이 설정이 모든 작업에 항상 적용되어야 하는가?
    YES → .github/copilot-instructions.md

특정 파일 유형/경로에만 규칙을 적용해야 하는가?
    YES → *.instructions.md (applyTo 설정)

특정 반복 작업을 템플릿화하고 싶은가?
    YES → Prompt Files (*.prompt.md)

특정 역할을 가진 전용 에이전트가 필요한가?
    YES → Custom Agents (*.agent.md)
```

### 컨텍스트 레이어 이해

Copilot은 여러 레이어의 지시문을 합쳐서 동작합니다.

| 레이어 | 예시 | 배치 시점 |
|--------|------|----------|
| 시스템 레이어 (비공개) | 안전 정책, 기본 지시문 | 모든 요청에 항상 포함 |
| 공통 지침 | `.github/copilot-instructions.md` | 대부분의 채팅 요청 |
| 조건부 지침 | `.github/instructions/*.instructions.md` | 파일 패턴이 맞을 때 |
| 실행형 템플릿 | `.github/prompts/*.prompt.md` | `/명령` 실행 시 |
| 역할/도구 제약 | `.github/agents/*.agent.md` | 에이전트 선택 시 |
| 사용자 입력 | Chat 메시지 | 메시지 전송 시 |

이 장에서는 **Custom Instructions**를 중심으로 실습합니다.

---

<a id="part2"></a>

## 2️⃣ YAML Frontmatter 기초 [↑](#toc)

`.instructions.md`, `.prompt.md`, `.agent.md` 파일의 맨 위에는 `---`로 감싸인 설정 블록이 있습니다. 이것을 **YAML frontmatter**라고 합니다.

```yaml
---
description: "파이썬 코드 작성 시 사용한다."
applyTo: "**/*.py"
---
```

YAML frontmatter는 본문 내용이 아닙니다. Copilot에게 "이 파일을 **언제**, **어떻게** 사용할지"를 알려주는 설정입니다.

### 자주 사용하는 항목

| 항목 | 의미 | 어디서 쓰나 |
|------|------|------------|
| `description` | 언제 이 파일을 써야 하는지 설명 | instructions, prompts, agents 공통 |
| `applyTo` | 어떤 파일 패턴에 규칙을 적용할지 | instructions |
| `name` | Chat 목록에 보이는 이름 | prompts, agents |
| `agent` | 어떤 실행 모드로 실행할지 | prompts |
| `tools` | 허용할 도구 목록 | agents |

### YAML 작성 기본 규칙

1. `key: value` 형태가 기본 구조입니다.
2. 목록은 `-` 기호로 씁니다.
3. 들여쓰기로 구조를 표현합니다.
4. **탭(Tab)이 아닌 공백(Space)을 사용합니다.**
5. 값 안에 `:` 같은 특수문자가 있으면 따옴표로 감쌉니다.

> 🤔 **들여쓰기 오류가 나면?**
> YAML은 탭(Tab) 문자를 허용하지 않습니다. VS Code에서 탭이 입력되지 않도록 설정하거나, 공백(Space) 2~4칸으로 직접 입력하세요.

> 🤔 **frontmatter가 인식되지 않으면?**
> 파일의 **첫 번째 줄**이 `---`로 시작해야 합니다. 빈 줄이 `---`보다 앞에 오면 frontmatter로 인식되지 않습니다.

이 과정의 규칙: `description`과 본문은 한국어, `name`은 영문으로 작성합니다.

---

<a id="part3"></a>

## 3️⃣ 실습: copilot-instructions.md 작성 [↑](#toc)

`copilot-instructions.md`는 프로젝트 **전체에 항상 적용**되는 공통 규칙입니다. 커밋 메시지 스타일, 예외 처리 원칙 같은 내용이 여기에 들어갑니다.

### 폴더 생성

터미널에서 프로젝트 루트 위치를 확인하고 실행합니다.

**Windows**:
```powershell
mkdir .github
```

**macOS / Linux**:
```bash
mkdir -p .github
```

### 파일 생성 및 내용 작성

`.github/copilot-instructions.md` 파일을 만들고 아래 내용을 붙여넣습니다.

```markdown
# Todo Manager Copilot 공통 지침

## 적용 범위

- 이 파일은 워크스페이스 전체에 항상 적용되는 공통 규칙이다.
- 파일 유형별 세부 규칙은 `.github/instructions/*.instructions.md`에서 관리한다.

## 커밋 메시지 스타일

- 형식은 `type(scope): summary`를 사용한다.
- `type`은 `feat`, `fix`, `refactor`, `test`, `docs`, `chore` 중 하나를 사용한다.
- `summary`는 50자 내외로 핵심 변경점을 명확히 작성한다.

## 예외 처리 공통 원칙

- 입력값 검증 실패에는 `ValueError` 또는 `TypeError`를 우선 사용한다.
- `except Exception` 같은 광범위 예외 처리는 특별한 이유가 없으면 사용하지 않는다.
- 예외 메시지에는 실패 원인과 조건을 함께 포함한다.

## 문서 및 주석 원칙

- 공개 함수와 클래스에는 한국어 docstring을 작성한다.
- 복잡한 분기나 비즈니스 규칙에는 의도를 설명하는 짧은 주석을 작성한다.
- 동작이 바뀌면 README와 관련 문서도 함께 갱신한다.

## 변경 품질 기준

- 기능 추가/버그 수정 시 관련 테스트를 반드시 추가하거나 갱신한다.
- 리팩터링은 동작 변경 없이 수행하고, 필요한 경우 테스트로 동일 동작을 보증한다.
```

이 파일은 `.github/` 폴더에 위치하며, frontmatter 없이 일반 Markdown으로 작성합니다.

---

<a id="part4"></a>

## 4️⃣ 실습: *.instructions.md 작성 [↑](#toc)

`*.instructions.md`는 **특정 파일 유형에만 조건부로 적용**되는 세부 규칙입니다. `applyTo` 필드로 적용 대상을 지정합니다.

### 폴더 생성

```bash
mkdir -p .github/instructions
```

### general.instructions.md — Python 코딩 규칙

`.github/instructions/general.instructions.md` 파일을 만들고 아래 내용을 붙여넣습니다.

```markdown
---
description: "파이썬 코드 작성 또는 리뷰 시 사용한다. 이 프로젝트의 네이밍 규칙, 타입 힌트, 코드 구조 규칙을 포함한다."
applyTo: "**/*.py"
---

# Todo Manager 파이썬 코딩 지침

## 언어 규칙

- 변수명, 함수명, 클래스명은 영어로 작성한다.
- 함수명과 변수명은 snake_case, 클래스명은 PascalCase를 사용한다.
- 코드 주석과 docstring은 한국어로 작성한다.

## 타입 힌트

- 모든 함수 시그니처에 타입 힌트를 포함한다.
- 반환 타입도 반드시 명시한다 (`-> None` 포함).

## 함수 설계

- 함수는 단일 책임 원칙을 따른다.
- 중첩 깊이는 3 이하로 유지한다.
- 모든 공개 메서드에 한국어 docstring을 작성한다.
```

`applyTo: "**/*.py"` 가 핵심입니다. Python 파일을 작업할 때만 이 규칙이 자동으로 적용됩니다.

> 🤔 **`applyTo: "**"` 와 `applyTo: "**/*.py"` 의 차이가 뭔가요?**
> `applyTo: "**"` 는 모든 파일, 모든 작업에 지침을 불러옵니다. 불필요한 컨텍스트가 늘어나 응답이 느려질 수 있습니다. 특정 파일 유형의 규칙은 해당 패턴만 지정하세요.

### testing.instructions.md — 테스트 작성 규칙

`.github/instructions/testing.instructions.md` 파일을 만들고 아래 내용을 붙여넣습니다.

```markdown
---
description: "테스트 작성, 리뷰, 수정 시 사용한다. pytest 규칙, AAA(Arrange-Act-Assert) 패턴, 테스트 네이밍 규칙을 포함한다."
applyTo: "tests/**"
---

# Todo Manager 테스트 작성 지침

## 테스트 프레임워크

- pytest를 사용한다.

## 테스트 명명 규칙

- 테스트 함수명은 `test_`로 시작한다.
- 이름은 `test_메서드명_조건_기대결과` 형식을 권장한다.
  - 예: `test_add_with_empty_title_raises_value_error`

## 테스트 구조

- Arrange-Act-Assert 패턴을 따른다.
- 한 테스트 함수는 한 가지 동작만 검증한다.
- 각 단계를 `# Arrange`, `# Act`, `# Assert` 주석으로 구분한다.
```

### AAA 패턴이란?

Arrange-Act-Assert는 테스트를 세 단계로 나눠 읽기 쉽게 만드는 방식입니다.

```python
def test_add_with_empty_title_raises_value_error():
    # Arrange — 테스트에 필요한 객체와 입력값 준비
    manager = TodoManager()

    # Act + Assert — 실행과 동시에 예외 검증
    with pytest.raises(ValueError):
        manager.add("")
```

| 단계 | 역할 | 비유 |
|------|------|------|
| Arrange (준비) | 객체, 입력값, 사전 상태 준비 | 실험 준비 |
| Act (실행) | 검증하려는 동작 1회 실행 | 실험 수행 |
| Assert (검증) | 결과가 기대값과 같은지 확인 | 결과 측정 |

> 🤔 **Copilot이 이 규칙들을 안 따르면?**
> 다음 순서로 확인해보세요.
> 1. 파일이 올바른 경로에 있는지: `.github/instructions/` 폴더 안
> 2. frontmatter의 `---` 가 파일 첫 줄에 있는지
> 3. `applyTo` 값이 현재 작업하는 파일 경로와 맞는지
> 4. Copilot Chat 새 대화를 시작한 뒤 다시 요청해보세요.

---

<a id="part5"></a>

## 5️⃣ 동작 확인 [↑](#toc)

지침 파일을 모두 작성했으면, Copilot이 실제로 규칙을 따르는지 확인합니다.

### 확인 방법

Copilot Chat에서 새 대화를 시작하고, Agent 모드로 전환한 뒤 아래 요청을 순서대로 입력합니다.

**1번 요청 — Python 코딩 규칙 확인**:

```
TodoManager에 title이 빈 문자열일 때 ValueError를 발생시키는 검증 로직을 add() 메서드에 추가해줘.
```

확인 포인트:
- 함수 시그니처에 타입 힌트가 있는가? (`def add(self, title: str) -> Todo:`)
- snake_case 네이밍을 따르는가?
- 한국어 docstring이 포함되는가?
- 예외 처리에 `ValueError`를 쓰는가?

**2번 요청 — 테스트 규칙 확인**:

```
위에서 추가한 검증 로직에 대한 테스트를 tests/ 폴더에 작성해줘.
```

확인 포인트:
- 테스트 함수명이 `test_add_조건_기대결과` 형식인가?
- `# Arrange`, `# Act`, `# Assert` 주석 구조가 있는가?
- 한 함수에서 한 가지 동작만 검증하는가?

**규칙이 반영되지 않았을 때 재요청 예시**:

```
방금 생성한 코드를 프로젝트 지침에 맞게 다시 수정해줘.
- 공통 지침: 예외 처리 원칙, 한국어 docstring 반영
- 테스트 지침: AAA 패턴, test_메서드명_조건_기대결과 네이밍 반영
```

---

<a id="part6"></a>

## 6️⃣ 슬래시 명령으로 자동 생성하기 [↑](#toc)

VS Code 최신 버전에서는 Copilot이 Instructions 파일을 자동으로 만들어주는 슬래시 명령을 지원합니다.

### `/create-instructions` — 지침 파일 자동 생성

```
/create-instructions
pytest 테스트는 Arrange-Act-Assert 패턴을 사용하고,
테스트 함수 이름은 test_메서드명_조건_기대결과 형식으로 작성하도록 규칙을 만들어줘.
```

생성 후 확인 포인트:
- 저장 위치가 `.github/instructions/` 폴더인가?
- `applyTo`가 `tests/**` 로 올바르게 설정되었는가?
- `description`에 "테스트", "pytest", "AAA" 같은 키워드가 포함되었는가?

### `/init` — 공통 지침 초안 자동 생성

```
/init
```

현재 프로젝트를 분석해 `.github/copilot-instructions.md` 초안을 만들어줍니다. 생성 후에는 반드시 검토하고, 앞서 작성한 내용과 중복되지 않도록 정리합니다.

> 🤔 **슬래시 명령이 목록에 안 보이면?**
> VS Code와 GitHub Copilot Chat 확장이 최신 버전인지 확인하세요.
> Chat이 Agent 모드로 설정되어 있는지도 확인하세요.
> 이 기능이 없어도 3번~5번 실습을 직접 완료하면 학습 목표를 달성할 수 있습니다.

---

<a id="part7"></a>

## 7️⃣ 여기까지 되셨나요? [↑](#toc)

| 항목 | 확인 |
|------|:------:|
| `.github/copilot-instructions.md` 생성 완료 | ☐ |
| `.github/instructions/general.instructions.md` 생성 완료 | ☐ |
| `.github/instructions/testing.instructions.md` 생성 완료 | ☐ |
| `description` 필드에 검색 키워드 포함 | ☐ |
| `applyTo` 가 각각 `**/*.py`, `tests/**` 로 설정 | ☐ |
| 공통 지침과 파일별 지침 역할이 분리됨 | ☐ |
| Python 코드 생성 요청 시 타입 힌트, snake_case, docstring 반영 확인 | ☐ |
| 테스트 코드 생성 요청 시 AAA 패턴, 네이밍 규칙 반영 확인 | ☐ |

---

<a id="part8"></a>

## 8️⃣ 정리 [↑](#toc)

이번 장에서 만든 파일과 각각의 역할을 정리합니다.

| 파일 | 역할 | 적용 방식 |
|------|------|----------|
| `.github/copilot-instructions.md` | 프로젝트 전체 공통 규칙 | 모든 채팅 요청에 자동 적용 |
| `general.instructions.md` | Python 파일 코딩 규칙 | `.py` 파일 작업 시 자동 적용 |
| `testing.instructions.md` | 테스트 파일 작성 규칙 | `tests/` 경로 파일 작업 시 자동 적용 |

**Custom Instructions의 핵심 원칙:**
- 공통 규칙은 `copilot-instructions.md`에, 파일 유형별 규칙은 `*.instructions.md`에 분리
- 같은 규칙을 여러 파일에 중복 작성하면 결과가 불안정해질 수 있음
- `description`에는 "언제 쓸지", "핵심 키워드", "포함 범위"를 구체적으로 작성

### 다음 장 미리보기

Custom Instructions가 "항상 적용되는 규칙"이라면, Prompt Files는 "필요할 때 직접 실행하는 작업 템플릿"입니다. 반복되는 작업 요청을 파일로 저장해두고, 한 번에 실행하는 방법을 실습합니다.

→ **04장**: [Prompt Files](/ai-native/prompt-files)
