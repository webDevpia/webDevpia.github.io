# 04. Custom Instructions 실습

## 목표

Todo Manager 프로젝트에 맞는 Custom Instructions 파일을 직접 작성하고, Copilot이 이 지침을 따르는지 확인합니다.

이번 교시는 다음 순서로 실습을 발전시킵니다.

1. `*.instructions.md`만으로 시작
2. `.github/copilot-instructions.md` + `*.instructions.md`로 역할 분리
3. `/create-instructions`, `/init` 명령으로 자동 생성 흐름 체험

---

## 배경 지식

**Custom Instructions**는 Copilot에게 프로젝트 규칙을 알려주는 지침 파일입니다.

- 파일 기반 지침: `.github/instructions/*.instructions.md`
- 워크스페이스 공통 지침: `.github/copilot-instructions.md`

운영 방식 비교:

| 방식 | 파일 | 적용 범위 | 추천 상황 |
|------|------|-----------|-----------|
| 기초 | `*.instructions.md` | `applyTo` 패턴이 맞는 파일/작업 | 처음 규칙 설계를 배울 때 |
| 발전 | `.github/copilot-instructions.md` + `*.instructions.md` | 공통 규칙 + 파일별 세부 규칙 동시 적용 | 팀 프로젝트로 확장할 때 |

### 메모리 경로 오해 방지

실습 중 `/memories/...` 표기를 보더라도, 이것은 VS Code 탐색기에서 보이는 실제 폴더 경로가 아닙니다.

| 표기 | 의미 | VS Code 탐색기에서 폴더로 보이나? |
|------|------|-------------------------------|
| `/memories/...` | 에이전트 전용 메모리 네임스페이스(논리 경로) | 아니오 |
| `.github/...` | 실제 워크스페이스 파일 경로 | 예 |

확인 방법:

- `/memories/...`는 에이전트의 memory 조회 기능으로 확인
- `.github/...`는 VS Code 탐색기에서 파일로 확인

메모리 조회 요청 예시(복붙용):

1. "사용자 메모리 목록을 보여줘."
2. "세션 메모리 파일 목록을 보여줘."
3. "저장소 메모리(`/memories/repo/`)에 어떤 항목이 있는지 보여줘."

핵심 필드:

- `description`: 이 지침을 언제 쓸지 설명 (키워드 포함 권장)
- `applyTo`: 특정 파일 패턴에 자동 적용 (예: `**/*.py`)

```yaml
---
description: "파이썬 코드 작성 시 사용"
applyTo: "**/*.py"
---
```

> **주의**: `applyTo: "**"` 는 모든 요청마다 지침을 불러오므로, 꼭 필요한 경우에만 사용합니다.

---

## 실습 단계

### 1단계: 기초 실습 (`*.instructions.md`만 사용)

#### 1-1. 폴더 생성
`.github/instructions/` 폴더를 만듭니다.

#### 1-2. 템플릿 복사
`starter/` 폴더의 `.template` 파일을 `.github/instructions/` 에 복사하고, `.template` 확장자를 제거합니다.

```
starter/general.instructions.md.template  →  .github/instructions/general.instructions.md
starter/testing.instructions.md.template  →  .github/instructions/testing.instructions.md
```

#### 1-3. 내용 작성
각 파일을 열어 Todo Manager 프로젝트에 맞게 내용을 채웁니다.

아래 예시는 그대로 따라 입력해도 동작하도록 구성한 최소 완성본입니다.

1) `.github/instructions/general.instructions.md` 작성

```md
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

2) `.github/instructions/testing.instructions.md` 작성

```md
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

3) 작성 후 빠른 점검

- 파일 맨 위에 `---`로 감싼 frontmatter 블록이 있는지 확인
- `description`, `applyTo` 값이 따옴표로 감싸져 있는지 확인
- `[프로젝트명]` 같은 템플릿 문구가 남아 있지 않은지 확인
- Copilot Chat에 1-4 예시 요청을 넣었을 때 위 규칙(네이밍, 타입 힌트, AAA 등)이 반영되는지 확인

### 참고: Arrange-Act-Assert(AAA) 패턴

AAA 패턴은 테스트 코드를 준비(Arrange) - 실행(Act) - 검증(Assert)으로 나눠
가독성과 유지보수성을 높이는 대표적인 테스트 작성 방식입니다.

- Arrange(준비): 테스트에 필요한 객체, 입력값, 사전 상태를 준비합니다.
- Act(실행): 검증하려는 동작을 한 번 실행합니다.
- Assert(검증): 실행 결과가 기대값과 같은지 확인합니다.

간단 예시:

```python
def test_add_with_empty_title_raises_value_error():
	# Arrange
	manager = TodoManager()

	# Act + Assert
	with pytest.raises(ValueError):
		manager.add("")
```

실무 팁:

- 한 테스트 함수에는 보통 Act를 1개만 둡니다.
- Arrange 코드가 길어지면 fixture로 분리해 중복을 줄입니다.

### 참고: Given-When-Then(GWT) 패턴

GWT 패턴은 테스트를 시나리오 문장처럼 표현하는 방식입니다.
테스트 의도를 먼저 읽기 쉽게 만들고 싶을 때 유용합니다.

- Given(상황): 테스트가 시작되는 전제 조건
- When(행동): 검증하려는 동작
- Then(결과): 기대하는 결과

간단 예시:

```text
Given 제목이 빈 문자열인 입력값이 있다.
When add("")를 호출한다.
Then ValueError가 발생한다.
```

AAA와 GWT는 의미가 거의 동일하며, 아래처럼 대응됩니다.

| AAA | GWT |
|-----|-----|
| Arrange | Given |
| Act | When |
| Assert | Then |

#### 1-4. 동작 확인
Copilot Chat에 다음 요청을 입력하고 지침이 반영되는지 확인합니다:

```
TodoManager에 title이 빈 문자열일 때 ValueError를 발생시키는 검증 로직을 add() 메서드에 추가해줘.
```

### 2단계: 발전 실습 (`copilot-instructions.md` + `*.instructions.md` 분리)

#### 2-1. 공통 지침 파일 추가
`starter/copilot-instructions.md.template`를 `.github/copilot-instructions.md`로 복사한 뒤,
프로젝트 전반 공통 규칙을 작성합니다.

```
starter/copilot-instructions.md.template  →  .github/copilot-instructions.md
```

아래 예시는 그대로 붙여 넣어도 동작하는 2단계 기준 완성본입니다.

```md
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

#### 2-2. 파일별 지침과 역할 분리
기존 `*.instructions.md`에는 파일 유형별 세부 규칙만 남깁니다.

예시(세부 규칙):

- `general.instructions.md`: Python 네이밍/타입 힌트
- `testing.instructions.md`: 테스트 구조, AAA 패턴

아래는 역할 분리 후 최종 예시입니다.
1단계에서 만든 두 파일은 아래 내용으로 덮어써도 됩니다.

1) `.github/instructions/general.instructions.md`

```md
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

2) `.github/instructions/testing.instructions.md`

```md
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

3) 2단계 작성 후 빠른 점검

- `.github/copilot-instructions.md`에 공통 규칙(커밋/예외/문서/품질)이 들어있는지 확인
- `general.instructions.md`, `testing.instructions.md`에 공통 규칙이 중복되지 않았는지 확인
- `applyTo`가 각각 `**/*.py`, `tests/**`로 유지되는지 확인
- Copilot이 요청별로 공통 규칙 + 파일별 규칙을 함께 반영하는지 확인

#### 2-3. 분리 적용 확인
Copilot Chat에서 아래 순서대로 입력하면서 공통 규칙 + 세부 규칙이 함께 반영되는지 확인합니다.

실습 목표:

- 요청 종류에 따라 파일별 지침이 다르게 적용되는지 확인
- 동시에 공통 지침(`.github/copilot-instructions.md`)이 항상 함께 적용되는지 확인

실습 순서:

1) Copilot Chat에서 새 대화를 시작합니다.
2) 아래 1번 요청을 입력합니다.
3) 생성/수정된 코드에서 테스트 전용 규칙이 반영됐는지 확인합니다.
4) 이어서 아래 2번 요청을 입력합니다.
5) 생성/수정된 코드에서 Python 코딩 규칙 + 공통 규칙이 반영됐는지 확인합니다.

```text
1) 테스트 파일에 맞는 테스트 코드를 작성해줘.
2) 서비스 로직 메서드를 추가해줘.
```

확인 포인트:

- 1번 요청(테스트 코드)
	- 테스트 함수명이 `test_메서드명_조건_기대결과` 형식에 가깝다.
	- `# Arrange`, `# Act`, `# Assert` 구조가 보인다.
	- 한 테스트에서 한 가지 동작만 검증한다.

- 2번 요청(서비스 로직)
	- 함수 시그니처와 반환 타입 힌트가 포함된다.
	- snake_case 네이밍을 따른다.
	- 한국어 docstring/주석 규칙이 반영된다.
	- 예외 처리 시 `ValueError`/`TypeError` 우선 원칙이 반영된다.

문제가 있을 때 재요청 예시:

```text
방금 생성한 코드를 프로젝트 지침에 맞게 다시 수정해줘.
- 공통 지침: 예외 처리 원칙, 문서/주석 원칙 반영
- 테스트 지침: AAA 패턴, test_메서드명_조건_기대결과 네이밍 반영
```

완료 기준:

- 같은 대화에서 테스트 요청과 서비스 요청을 각각 실행했을 때,
	두 결과 모두 공통 규칙 + 해당 파일 유형 규칙이 함께 반영되면 완료입니다.



### 3단계: 슬래시 명령 실습 (`/create-instructions`, `/init`)

최신 VS Code 기준으로 이 단계는 `/create-instructions`와 `/init`을 사용해 자동 생성 결과를 점검하는 실습입니다.

#### 3-1. `/create-instructions` 따라하기

실습 목표:

- 테스트 지침 파일을 자동 생성해 생산성을 높인다.
- 자동 생성 결과를 프로젝트 규칙에 맞게 검토/보정한다.

실습 순서:

1) Copilot Chat에서 새 대화를 시작합니다.
2) 아래 입력을 실행합니다.

```text
/create-instructions
pytest 테스트는 Arrange-Act-Assert 패턴을 사용하고, 테스트 함수 이름은 test_메서드명_조건_기대결과 형식으로 작성하도록 규칙을 만들어줘.
```

3) 생성된 instructions 파일을 열어 저장 위치를 확인합니다.
4) frontmatter의 `description`, `applyTo`가 의도와 맞는지 확인합니다.
5) 필요하면 본문 규칙(네이밍, AAA, 주석 규칙)을 직접 보완합니다.

생성 후 확인 포인트:

- `applyTo`가 테스트 파일 범위(`tests/**`)에 맞는지 확인
- `description`에 테스트/pytest/AAA 같은 검색 키워드가 포함됐는지 확인
- 테스트 함수 네이밍 규칙이 빠지지 않았는지 확인

#### 3-2. `/init` 따라하기

실습 목표:

- 워크스페이스 공통 지침 초안을 자동 생성한다.
- 파일별 지침과 역할이 겹치지 않도록 분리한다.

실습 순서:

1) Copilot Chat에서 아래 명령을 실행합니다.

```text
/init
```

2) 생성된 공통 지침 파일(보통 `.github/copilot-instructions.md`)을 엽니다.
3) 아래 항목이 공통 규칙으로 들어가 있는지 확인합니다.
	- 커밋 메시지 스타일
	- 예외 처리 공통 원칙
	- 문서/주석 원칙
4) 파일별 지침(`general.instructions.md`, `testing.instructions.md`)과 중복되는 문장이 있으면
	공통 규칙은 `copilot-instructions.md`에만 남기고, 파일별 지침에는 세부 규칙만 남깁니다.

생성 후 확인 포인트:

- 공통 지침: 프로젝트 전반 규칙 중심
- 파일별 지침: 파일 타입별 세부 규칙 중심
- 중복/충돌 문장 최소화

#### 3-3. 자동 생성 후 통합 검증

아래 요청을 다시 실행해 자동 생성한 지침이 실제 코드 생성에 반영되는지 확인합니다.

```text
1) 테스트 파일에 맞는 테스트 코드를 작성해줘.
2) 서비스 로직 메서드를 추가해줘.
```

완료 기준:

- 1번 요청 결과: 테스트 네이밍 + AAA 구조 반영
- 2번 요청 결과: 타입 힌트/네이밍/docstring + 공통 예외 처리 원칙 반영
- 두 요청 모두에서 공통 지침과 파일별 지침이 함께 적용됨

---

## 자주 발생하는 문제와 해결

### 1) Copilot이 지침을 따르지 않을 때

**증상:** 코드 생성 요청을 했는데 지침의 네이밍, 타입 힌트, 주석 규칙이 반영되지 않음

**원인 확인 순서:**

1. 지침 파일 존재 확인
   - `.github/instructions/general.instructions.md` 존재하는가?
   - `.github/copilot-instructions.md` 존재하는가?
   
2. frontmatter 확인
   - `applyTo` 값이 현재 작업 파일과 일치하는가?
   - 예: Python 파일 작업 중이면 `applyTo: "**/*.py"`
   
3. Chat 새로고침
   - Copilot Chat을 완전히 닫았다가 다시 오기
   - 또는 Chat에서 "Settings" → "Reload window"

**해결책:**

```bash
# 파일 존재 확인
ls -la .github/instructions/
ls -la .github/copilot-instructions.md

# 파일이 존재하면 내용 검증
cat .github/instructions/general.instructions.md | head -10
```

파일이 존재하면 VS Code에서 열어 frontmatter를 다시 확인합니다.

**재검증:** Chat에서 새 대화를 시작한 후 코드 생성 요청을 다시 합니다.

---

### 2) `applyTo` 패턴이 너무 넓을 때

**증상:** `applyTo: "**"` 로 설정해서 모든 요청마다 지침이 불려와, 불필요한 컨텍스트가 과다 해짐

**원인:**

- `applyTo: "**"`는 모든 파일과 모든 작업에 지침을 적용
- 이로 인해 Chat 응답이 느려지거나 컨텍스트 초과 오류 발생 가능

**해결책:**

파일 유형별로 제한합니다:

| 지침 파일 | 적절한 applyTo | 설명 |
|---------|---------------|------|
| general.instructions.md | `**/*.py` | Python 파일만 |
| testing.instructions.md | `tests/**` | 테스트 폴더만 |
| copilot-instructions.md | (frontmatter 불필요) | 공통 지침은 자동 적용 |

**수정 예시:**

❌ 잘못된 예:
```yaml
applyTo: "**"
```

✓ 올바른 예:
```yaml
applyTo: "**/*.py"
```

---

### 3) 공통 지침과 파일별 지침 역할이 겹칠 때

**증상:** 같은 규칙이 `copilot-instructions.md`와 `*.instructions.md` 모두에 들어가 있음

**원인:**

- 어느 파일에 뭘 넣을지 기준이 불명확
- 지침을 작성할 때 역할 분리를 제대로 하지 않음

**기준을 다시 정리하면:**

| 파일 | 들어갈 내용 | 예시 |
|------|-----------|------|
| `.github/copilot-instructions.md` | 모든 파일에 항상 적용되는 공통 규칙 | 커밋 메시지 스타일, 예외 처리 원칙, 일반 문서화 원칙 |
| `.github/instructions/general.instructions.md` | Python 파일만 적용되는 규칙 | Python 네이밍, 타입 힌트, docstring 포맷 |
| `.github/instructions/testing.instructions.md` | 테스트 파일만 적용되는 규칙 | pytest 문법, AAA 패턴, 테스트 함수 네이밍 |

**해결책:**

1. `copilot-instructions.md`에서 언어/프레임워크 특화 규칙 제거
   - ❌ "Python 타입 힌트는..." → ✓ `general.instructions.md`로 이동
   
2. `*.instructions.md`에서 공통 규칙 제거
   - ❌ "커밋 메시지는 type(scope): summary" → ✓ `copilot-instructions.md`로 이동

3. 수정 후 Chat 새로고침

**재검증:** 2-2 예시 코드와 비교해 역할이 제대로 분리되었는지 확인

---

### 4) `description` 필드가 너무 짧아 의도가 불명확할 때

**증상:** 프롬프트 작성할 때 어느 지침을 참고해야 할지 모호함

**원인:**

너무 짧거나 일반적인 표현

❌ 예:
```yaml
description: "파이썬 규칙"
description: "코딩 지침"
```

✓ 예:
```yaml
description: "파이썬 코드 작성 또는 리뷰 시 사용한다. 이 프로젝트의 네이밍 규칙, 타입 힌트, 코드 구조 규칙을 포함한다."
description: "테스트 작성 시 사용한다. pytest 규칙, AAA(Arrange-Act-Assert) 패턴, 테스트 네이밍 규칙을 포함한다."
```

**해결책:**

`description`에 다음 3가지를 포함시킵니다:

1. **언제 쓸지**: "파이썬 코드 작성 시", "테스트 작성 시"
2. **핵심 키워드**: "네이밍", "타입 힌트", "AAA 패턴"
3. **포함 범위**: "규칙을 포함한다"

**수정 방법:**

각 파일의 frontmatter를 열어 `description`을 위 기준에 맞게 다시 작성합니다.

---

### 5) `/create-instructions`나 `/init` 명령이 작동하지 않을 때

**증상:** 명령을 입력해도 아무 반응이 없거나 오류 메시지가 나옴

**원인:**

- VS Code 버전이 낮음 (2026-01 이후 버전 필요)
- Copilot Chat 확장이 최신 버전이 아님
- Chat이 Agent 모드가 아님

**해결책:**

1. Copilot Chat 확장 업데이트 확인
   - VS Code 좌측 "Extensions" → "Copilot Chat" → 업데이트 체크

2. Chat이 Agent 모드인지 확인
   - Chat 입력창 위쪽 드롭다운에서 "Agent" 선택

3. 명령 실행 재시도
   - Chat에서 `/create-instructions` 입력
   - 또는 `/init` 입력

**만약 여전히 작동하지 않으면:**

- 3단계는 선택 사항이고, 2단계까지 완료해도 학습 목표를 달성할 수 있습니다.
- 2-1, 2-2의 예시 파일을 참고해 지침을 직접 완성하면 됩니다.

---

### 6) Chat이 지침을 일부만 따를 때

**증상:** 코드 생성 결과에 타입 힌트는 있는데 docstring 주석이 없거나, 네이밍은 맞는데 AAA 패턴이 없는 경우

**원인:**

- 지침의 우선순위가 명확하지 않음
- 프롬프트 요청이 지침 규칙보다 강함

**해결책:**

1. 지침 파일의 규칙 순서를 명확히 합니다
   - "반드시 포함할 항목" 우선 나열
   - 그 다음 "권장 사항"

2. 프롬프트에서 명시적으로 요청합니다
   
   ❌ 약한 요청:
   ```
   코드를 작성해줘.
   ```
   
   ✓ 강한 요청:
   ```
   다음 규칙을 반드시 따르면서 코드를 작성해줘:
   - 타입 힌트 필수
   - 한국어 docstring 필수
   - AAA 패턴 필수
   ```

**재검증:** 명시적 요청 후 결과에서 모든 규칙이 반영되는지 확인

---

## 체크리스트

- [ ] `.github/instructions/general.instructions.md` 생성 완료
- [ ] `.github/instructions/testing.instructions.md` 생성 완료
- [ ] `.github/copilot-instructions.md` 생성 완료
- [ ] `description` 필드에 키워드가 포함되어 있음
- [ ] 공통 지침과 파일별 지침이 역할 분리되어 있음
- [ ] `/create-instructions` 실행 후 생성 파일을 검토/수정함
- [ ] `/init` 실행 후 공통 지침 초안을 정리함
- [ ] Copilot이 지침을 따르는 코드를 생성함

---

## 참고

막히면 `solution/` 폴더의 1~2단계 완성 예시를 참고하세요.
3단계(`/create-instructions`, `/init`)는 실행 시점에 따라 결과가 달라질 수 있으므로,
본문의 결과 확인 기준으로 검토하세요.
