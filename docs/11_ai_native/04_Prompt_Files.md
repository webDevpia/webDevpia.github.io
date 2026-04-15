---
title: 04. Prompt Files
layout: default
parent: AI-Native Development
nav_order: 4
permalink: /ai-native/prompt-files
---

# 04장. Prompt Files
{: .no_toc }

## 학습 목표

- Prompt File로 반복 작업을 템플릿화하여 일관된 품질로 실행할 수 있다
- 변수(`${input:...}`, `${selection}`)를 활용한 동적 프롬프트를 작성할 수 있다

<a id="toc"></a>

## 진행 순서

1. [Prompt File이란?](#part1) — Custom Instructions와의 차이
2. [Prompt File 구조와 문법](#part2) — frontmatter + 변수 문법
3. [실습: new-feature.prompt.md](#part3) — 새 기능 추가 템플릿
4. [실습: write-tests.prompt.md](#part4) — 테스트 작성 템플릿
5. [실습: code-review.prompt.md](#part5) — 코드 리뷰 템플릿
6. [여기까지 되셨나요?](#part6) — 체크리스트
7. [정리](#part7) — 활용 팁 및 다음 장

---

<a id="part1"></a>

## 1️⃣ Prompt File이란? [↑](#toc)

> 자주 쓰는 업무 양식을 상상해보세요.
> 매번 처음부터 작성하는 대신, 양식을 만들어두고 빈칸만 채우는 방식입니다.
> Prompt Files는 Copilot에게 보내는 요청을 파일로 저장해두고, 필요할 때 한 번에 실행하는 기능입니다.

### Custom Instructions와 Prompt Files의 차이

| | Custom Instructions | Prompt Files |
|--|---------------------|--------------|
| 역할 | "이 프로젝트에서는 항상 이렇게 해라" | "이 작업을 이렇게 실행해라" |
| 적용 시점 | 자동, 항상 | 수동, 필요할 때 |
| 비유 | 팀 규칙서 | 업무 양식 |
| 파일 위치 | `.github/copilot-instructions.md`, `.github/instructions/` | `.github/prompts/` |
| 실행 방법 | 없음 (자동 적용) | Chat에서 `/` 입력 후 선택 |

### 왜 Prompt Files를 쓰는가?

- **품질**: 모호한 즉흥 요청보다 구조화된 템플릿이 더 일관된 결과를 만듭니다.
- **재사용**: 팀원 모두가 같은 요청 패턴을 공유할 수 있습니다.
- **속도**: 반복 작업을 슬래시 명령 하나로 실행합니다.
- **리뷰**: 요청 자체를 코드처럼 검토하고 개선할 수 있습니다.

---

<a id="part2"></a>

## 2️⃣ Prompt File 구조와 문법 [↑](#toc)

Prompt File은 YAML frontmatter + 본문으로 구성됩니다.

```yaml
---
description: "Todo Manager에 새 기능을 구현하고 테스트를 추가할 때 사용"
name: "New Feature"
agent: "agent"
---
# 프롬프트 본문

기능명: ${input:featureName:구현할 기능명을 입력하세요}
```

### frontmatter 주요 항목

| 항목 | 역할 | 예시 |
|------|------|------|
| `description` | 언제 쓰는 프롬프트인지 설명 | `"새 기능 구현 시 사용"` |
| `name` | Chat `/` 목록에 보이는 이름 | `"New Feature"` |
| `agent` | 실행 모드 | `"agent"` |
| `tools` (선택) | 허용 도구 목록 | `[read, search]` |
| `argument-hint` (선택) | 실행 전 입력창 안내 문구 | `"기능명을 입력하세요"` |

### 본문에서 자주 쓰는 변수 문법

| 문법 | 역할 | 예시 |
|------|------|------|
| `${input:변수명}` | 실행 시 사용자 입력을 받음 | `${input:featureName}` |
| `${input:변수명:힌트}` | 입력창에 안내 문구 포함 | `${input:featureName:구현할 기능명}` |
| `${selection}` | 에디터에서 선택한 코드를 전달 | 코드 리뷰, 테스트 작성 시 |
| `#codebase` | 워크스페이스 전체에서 관련 파일 탐색 | 후속 메시지에서 `#codebase` |
| `#problems` | VS Code 오류/경고 정보 포함 | 오류 기반 수정 요청 시 |

### 본문 권장 구조

```
작업 목표
입력 변수
제약 조건
출력 형식
완료 기준
```

> 🤔 **프롬프트 이름이 Chat 목록에 안 보이면?**
> 파일이 `.github/prompts/` 폴더에 있는지, 파일 확장자가 `.prompt.md`인지 확인하세요.
> 그래도 안 보이면 VS Code를 재시작해보세요.

---

<a id="part3"></a>

## 3️⃣ 실습: new-feature.prompt.md [↑](#toc)

"새 기능 추가" 요청을 표준화하는 템플릿입니다.

### 폴더 생성

```bash
mkdir -p .github/prompts
```

### 파일 생성

`.github/prompts/new-feature.prompt.md` 파일을 만들고 아래 내용을 붙여넣습니다.

```markdown
---
description: "Todo Manager에 새 기능을 구현하고 테스트를 추가할 때 사용"
name: "New Feature"
agent: "agent"
---

다음 기능을 Todo Manager에 추가해주세요.

기능명: ${input:featureName:구현할 기능명을 입력하세요}

요구사항:
${input:requirements:기능 요구사항을 입력하세요}

다음을 포함해주세요:
1. `src/todo/manager.py` 에 메서드 추가 (한국어 docstring 포함)
2. `tests/test_manager.py` 에 테스트 추가 (Arrange-Act-Assert 패턴)
3. 모든 기존 테스트가 계속 통과하는지 확인
4. 프로젝트 코딩 지침 준수
```

### 실행 방법

1. Copilot Chat을 Agent 모드로 열기
2. 입력창에 `/` 입력
3. 목록에서 `New Feature` 선택
4. 변수 입력:
   - `featureName`: `완료된 할 일 개수 조회`
   - `requirements`: `완료 상태인 todo만 개수로 반환하고, 테스트 2개 이상 작성`
5. Enter로 실행

### 결과 확인 포인트

- `src/todo/manager.py` 수정 제안이 포함되었는가?
- `tests/test_manager.py` 테스트 제안이 포함되었는가?
- 타입 힌트, snake_case, 한국어 docstring이 적용되었는가?
- AAA 패턴 테스트가 생성되었는가?

---

<a id="part4"></a>

## 4️⃣ 실습: write-tests.prompt.md [↑](#toc)

에디터에서 선택한 코드를 기반으로 테스트를 작성하는 템플릿입니다. `${selection}` 변수를 사용합니다.

### 파일 생성

`.github/prompts/write-tests.prompt.md` 파일을 만들고 아래 내용을 붙여넣습니다.

```markdown
---
description: "선택된 코드에 AAA 패턴과 프로젝트 규칙을 따라 pytest 테스트를 작성할 때 사용"
name: "Write Tests"
agent: "agent"
---

다음 코드에 대한 pytest 테스트를 작성해주세요:

${selection}

요구사항:
- Arrange-Act-Assert 패턴을 사용한다.
- 정상 케이스와 예외 케이스를 모두 포함한다.
- 각 테스트 함수에 한국어 주석으로 테스트 의도를 설명한다.
- 테스트 함수명은 `test_메서드명_조건_기대결과` 형식을 따른다.
```

### `${selection}` 사용 방법

`${selection}`은 에디터에서 선택한 텍스트를 프롬프트에 자동으로 삽입합니다.

**실행 순서:**

1. VS Code 에디터에서 `src/todo/manager.py` 파일 열기
2. 테스트를 생성할 메서드를 마우스로 선택. 예시:

```python
def add(self, title: str) -> Todo:
    """새 Todo를 추가하고 반환한다"""
    raise NotImplementedError
```

3. 코드가 선택된 상태에서 Copilot Chat 창 열기
4. 입력창에 `/` 입력 → `Write Tests` 선택 → Enter

> 🤔 **코드를 선택하지 않고 실행하면?**
> `${selection}`이 빈 값으로 전달되어 Copilot이 어떤 코드를 테스트할지 알 수 없습니다.
> 반드시 코드를 먼저 선택한 후 프롬프트를 실행하세요.

### 결과 확인

| 확인 항목 | 기대 결과 |
|----------|----------|
| 선택 코드 반영 | 선택한 메서드 기준으로 테스트 생성 |
| 정상 케이스 | 정상 입력 시 결과 반환 테스트 포함 |
| 예외 케이스 | 빈 문자열 등 이상 입력 테스트 포함 |
| AAA 패턴 | `# Arrange`, `# Act`, `# Assert` 주석 존재 |
| 함수명 형식 | `test_add_정상입력_todo반환` 형식 |

### 생성된 테스트 실행 (선택)

생성된 코드를 `tests/test_manager.py`에 붙여넣은 뒤 실행합니다.

```bash
uv run pytest tests/test_manager.py -v
```

---

<a id="part5"></a>

## 5️⃣ 실습: code-review.prompt.md [↑](#toc)

코드를 수정하지 않고 리뷰 피드백만 제공하는 읽기 전용 템플릿입니다. `tools: [read, search]`로 수정 도구를 제한합니다.

### 파일 생성

`.github/prompts/code-review.prompt.md` 파일을 만들고 아래 내용을 붙여넣습니다.

```markdown
---
description: "Python 코드의 품질, 네이밍, 구조를 검토하고 실행 가능한 피드백을 제공할 때 사용"
name: "Code Review"
agent: "agent"
tools: [read, search]
---

다음 코드를 리뷰해주세요:

${selection}

다음 관점으로 검토하고 개선 제안을 제공해주세요:

1. **명명 규칙**: 변수명, 함수명이 역할을 명확히 나타내는가?
2. **단일 책임**: 함수/클래스가 하나의 일만 하는가?
3. **타입 힌트**: 모든 시그니처에 타입이 명시되어 있는가?
4. **코드 중복**: 반복되는 로직이 있는가?
5. **테스트 가능성**: 단위 테스트하기 쉬운 구조인가?

## 출력 형식

각 항목에 대해 **현재 상태** → **개선 방향** 으로 작성해주세요.
코드를 직접 수정하지 말고, 피드백만 제공해주세요.
```

### `tools: [read, search]` 의 의미

이 프롬프트의 목적은 수정이 아닌 리뷰 피드백입니다. `tools`를 읽기 중심으로 제한하면 의도치 않은 수정 제안이나 과도한 작업 흐름을 줄일 수 있습니다.

| 도구 | 역할 | 이 실습에서 필요한 이유 |
|------|------|-----------------------|
| `read` | 파일 내용 읽기 | 선택한 코드와 주변 구조를 정확히 이해하기 위해 |
| `search` | 워크스페이스 키워드/심볼 검색 | 관련 함수, 테스트, 호출부를 찾아 리뷰 정확도를 높이기 위해 |

> 리뷰 전용 프롬프트는 읽기 도구만, 코드 수정 프롬프트는 별도 파일로 분리하는 것이 안전합니다.

### 실행 방법

1. 리뷰할 메서드 1개를 에디터에서 선택
2. Copilot Chat에서 `/` → `Code Review` 선택 → Enter
3. 수정 없이 피드백 목록이 나오는지 확인

### 선택 범위에 따른 문법 가이드

| 리뷰 목표 | 권장 방법 |
|-----------|---------|
| 선택한 코드 자체 리뷰 | `${selection}` (기본) |
| 호출부나 연관 코드까지 함께 검토 | 후속 메시지에서 `#codebase` 추가 |
| 현재 오류/경고까지 함께 검토 | 후속 메시지에서 `#problems` 추가 |
| 최근 변경 코드 기준 리뷰 | 후속 메시지에서 `#changes` 추가 |

---

<a id="part6"></a>

## 6️⃣ 여기까지 되셨나요? [↑](#toc)

`.github/prompts/` 폴더에 3개 파일이 있는지 확인합니다.

```
.github/prompts/
├── new-feature.prompt.md     ☐
├── write-tests.prompt.md     ☐
└── code-review.prompt.md     ☐
```

| 항목 | 확인 |
|------|------|
| `.github/prompts/` 폴더 생성 | ☐ |
| `new-feature.prompt.md` 생성 | ☐ |
| `write-tests.prompt.md` 생성 | ☐ |
| `code-review.prompt.md` 생성 | ☐ |
| Chat에서 `/` 입력 시 3개 프롬프트 목록에 보임 | ☐ |
| `New Feature` 실행 시 기능 코드 + 테스트 동시 생성 | ☐ |
| `Write Tests` 실행 시 선택 코드 기반 AAA 테스트 생성 | ☐ |
| `Code Review` 실행 시 코드 수정 없이 피드백만 반환 | ☐ |

---

<a id="part7"></a>

## 7️⃣ 정리 [↑](#toc)

이번 장에서 만든 3개 프롬프트를 정리합니다.

| 파일 | 주요 문법 | 용도 |
|------|-----------|------|
| `new-feature.prompt.md` | `${input:변수명:힌트}` | 기능명과 요구사항을 입력받아 코드 + 테스트 동시 생성 |
| `write-tests.prompt.md` | `${selection}` | 선택한 코드를 기반으로 AAA 패턴 테스트 작성 |
| `code-review.prompt.md` | `${selection}` + `tools: [read, search]` | 읽기 전용으로 코드 리뷰 피드백 제공 |

### Prompt Files 활용 팁

1. **목적을 하나로**: 하나의 프롬프트에 너무 많은 역할을 담으면 결과가 불안정해집니다.
2. **구조를 명확히**: 목표, 제약, 출력 형식을 분리해서 작성합니다.
3. **`description`에 키워드**: 나중에 검색하기 쉽도록 키워드를 포함합니다.
4. **팀과 공유**: `.github/prompts/` 폴더는 Git에 커밋해 팀원 모두가 사용하도록 합니다.
5. **버전 관리**: 프롬프트도 코드처럼 수정 이력을 남기세요.

### 이제 갖춰진 것

```
.github/
├── copilot-instructions.md       # 프로젝트 공통 규칙 (03장)
├── instructions/
│   ├── general.instructions.md   # Python 코딩 규칙 (03장)
│   └── testing.instructions.md   # pytest + AAA 패턴 (03장)
└── prompts/
    ├── new-feature.prompt.md     # 새 기능 추가 템플릿 (04장)
    ├── write-tests.prompt.md     # 테스트 작성 템플릿 (04장)
    └── code-review.prompt.md     # 코드 리뷰 템플릿 (04장)
```

Copilot은 이제 여러분의 프로젝트 규칙을 알고 있고, 반복 작업을 슬래시 명령 하나로 실행할 수 있습니다.

### 다음 장 미리보기

Prompt Files가 "작업 템플릿"이라면, Custom Agents는 "역할이 고정된 전문 팀원"입니다. 예를 들어 코드 리뷰만 담당하고 절대 수정하지 않는 에이전트, 또는 테스트 작성 전문 에이전트를 만드는 방법을 다음 과정에서 배웁니다.

→ 다음 과정: Custom Agents


→ **다음 장**: [05. Custom Agents와 Context Engineering](/ai-native/agents-context)
