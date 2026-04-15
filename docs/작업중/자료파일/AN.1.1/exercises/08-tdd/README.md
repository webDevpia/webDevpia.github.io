# 08. TDD 에이전트 실습

## 목표

TDD(Test-Driven Development)의 Red → Green → Refactor 사이클을
세 개의 에이전트로 분리해 자동으로 실행되는 흐름을 완성합니다.

이번 실습 완료 기준:

1. `TDD Red`, `TDD Green`, `TDD Refactor` 에이전트 파일 작성 완료
2. `handoffs` 체인 연결 완료
3. Red(실패) → Green(통과) → Refactor(개선) 순서 검증 완료

---

## 배경 지식

이번 실습의 핵심은 "기능을 빨리 많이 구현"하는 것이 아니라,
작은 변경을 안전하게 반복하는 개발 루프를 체득하는 것입니다.

### 1) 용어 이해하기

> **TDD(Test-Driven Development, 테스트 주도 개발)**
> 구현 코드를 먼저 작성하지 않고, 테스트를 먼저 작성한 뒤 최소 구현과 개선을 반복하는 개발 방식입니다.
>
> **Red(레드 단계)**
> 실패하는 테스트를 먼저 작성해 "아직 구현되지 않은 요구사항"을 명확히 드러내는 단계입니다.
>
> **Green(그린 단계)**
> 방금 작성한 테스트를 통과시키는 데 필요한 최소한의 구현만 추가하는 단계입니다.
>
> **Refactor(리팩터 단계)**
> 테스트 통과 상태를 유지한 채 코드 구조와 가독성을 개선하는 단계입니다.
>
> **Handoff(핸드오프)**
> 현재 에이전트가 끝난 뒤 다음 에이전트로 제어를 넘기는 연결 규칙입니다.

### 2) 왜 Red(실패 테스트)부터 시작하나

Red를 먼저 만들면 "무엇을 구현해야 하는지"가 테스트 형태로 고정됩니다.
이렇게 하면 구현이 흔들려도 목표가 유지됩니다.

1. 요구사항을 실행 가능한 형태로 명확히 표현할 수 있습니다.
2. 과도한 구현(미리 최적화, 불필요한 분기)을 줄일 수 있습니다.
3. 완료 기준이 분명해져 팀/에이전트 간 의사결정 비용이 줄어듭니다.

예시(요구사항): "빈 문자열 제목이면 `ValueError`를 발생시킨다"

1. Red: 해당 동작을 검증하는 테스트를 먼저 추가합니다.
2. Green: 예외를 발생시키는 최소 코드만 구현합니다.
3. Refactor: 중복 제거, 이름 개선, 구조 개선을 수행합니다.

### 3) 단계별 진입/종료 조건

| 단계 | 진입 조건 | 해야 할 일 | 종료 조건 |
|------|-----------|------------|-----------|
| Red | 새 요구사항이 생김 | 실패하는 테스트 작성 | 새 테스트가 실제로 실패함 |
| Green | 실패 테스트가 존재함 | 최소 구현 작성 | 전체 테스트 통과 |
| Refactor | 테스트가 모두 통과함 | 구조/가독성 개선 | 테스트 통과 유지 |

실습에서 가장 중요한 원칙:

1. Red에서는 구현 코드를 수정하지 않습니다.
2. Green에서는 테스트를 통과시키는 데 필요한 코드만 작성합니다.
3. Refactor에서는 동작을 바꾸지 않습니다.

### 4) 에이전트를 3개로 분리하는 이유

에이전트를 분리하면 각 단계의 의사결정이 섞이지 않습니다.

1. Red 에이전트: "무엇이 아직 안 되는가"에만 집중
2. Green 에이전트: "어떻게 최소로 통과시킬까"에만 집중
3. Refactor 에이전트: "동작 유지 + 품질 개선"에만 집중

즉, 역할 분리를 통해 TDD 사이클 자체를 강제하고,
한 단계에서 자주 발생하는 실수가 다음 단계로 번지는 것을 줄입니다.

### 5) `handoffs`란 무엇인가

`handoffs`는 현재 에이전트 작업이 끝난 뒤 다음 에이전트로 제어를 넘기는 설정입니다.

```yaml
handoffs:
	- label: "TDD Green으로 전달"
	  agent: "TDD Green"
	  prompt: "Red 단계가 끝났습니다. 방금 추가된 실패 테스트를 통과시키는 최소 구현을 진행하세요."
```

주의점:

1. 각 `handoff` 항목은 `label`, `agent`, `prompt` 필드를 포함한 객체여야 합니다.
2. `handoffs[].agent` 값은 대상 에이전트의 `name`과 정확히 일치해야 합니다.
3. 공백/대소문자 차이도 불일치로 처리될 수 있습니다.
4. 파일 저장 후에도 반영이 안 되면 Chat 세션을 재시작해 캐시를 초기화합니다.

`description`은 어떤 상황에서 이 에이전트를 사용할지 설명하는 문구이므로 한글로 분명하게 작성하고,
`name`은 handoff 대상이 되는 표시 이름이므로 예시 값과 정확히 맞춰 유지하는 것이 안전합니다.

### 6) 테스트 작성 기본기(pytest + AAA)

이번 실습의 테스트는 [테스트 지침](../../.github/instructions/testing.instructions.md)을 따릅니다.

1. pytest를 사용합니다.
2. 테스트 함수명은 `test_`로 시작합니다.
3. 각 테스트는 `# Arrange`, `# Act`, `# Assert`를 명확히 분리합니다.
4. 한 테스트 함수는 한 가지 동작만 검증합니다.

간단한 형태 예시:

```python
def test_add_with_empty_title_raises_value_error() -> None:
    # Arrange
    manager = TodoManager()

    # Act / Assert
    with pytest.raises(ValueError):
        manager.add("")
```

### 7) Green 단계에서 자주 발생하는 실수

1. 실패 테스트를 통과시키기도 전에 구조를 크게 바꾸는 경우
2. 아직 필요하지 않은 일반화 코드(옵션, 확장 포인트)를 미리 추가하는 경우
3. 테스트를 바꿔서 통과시키는 방향으로 문제를 우회하는 경우

Green에서는 "테스트를 통과시키는 최소 구현"에만 집중하는 것이 정답입니다.

### 8) Refactor 단계 체크리스트

1. 중복 코드가 줄었는가
2. 변수/함수 이름이 역할을 분명하게 설명하는가
3. 함수가 한 가지 책임만 갖는가
4. 리팩터링 전후로 테스트 결과가 동일한가

Refactor의 품질 기준은 "코드는 더 좋아지고, 동작은 그대로"입니다.

### 9) 실습에서 주로 다루는 파일

| 파일 | 역할 | 주로 수정하는 단계 |
|------|------|---------------------|
| `tests/test_manager.py` | 요구사항을 테스트로 표현 | Red |
| `src/todo/manager.py` | 테스트를 통과시키는 구현 | Green, Refactor |

### 10) 한 사이클 실행 예시

1. Red 요청
	- "`TodoManager.add()` 메서드가 빈 문자열을 받으면 `ValueError`를 발생시키는 테스트를 작성해줘"
2. Red 검증
	- `uv run pytest -v` 실행 시 새 테스트가 실패해야 정상입니다.
3. Green 구현
	- 예외를 발생시키는 최소 코드만 추가합니다.
4. Green 검증
	- `uv run pytest -v` 실행 시 전체 테스트가 통과해야 합니다.
5. Refactor
	- 중복 제거/이름 개선/구조 개선 후 다시 테스트를 실행합니다.

이 흐름을 반복하면 기능 추가 속도보다 "변경 안정성"이 올라가고,
결과적으로 유지보수 비용이 크게 줄어듭니다.

---

## 실습 단계

### 0단계: 사전 준비

1. `.github/agents/` 폴더가 있는지 확인합니다.
2. `.github/instructions/general.instructions.md`, `.github/instructions/testing.instructions.md`가 있는지 확인합니다.
3. 프로젝트 루트에서 `uv sync`가 완료되었는지 확인합니다.

### 1단계: 템플릿 복사

아래 템플릿 3개를 복사합니다.

```text
starter/TDD-red.agent.md.template       →  .github/agents/TDD-red.agent.md
starter/TDD-green.agent.md.template     →  .github/agents/TDD-green.agent.md
starter/TDD-refactor.agent.md.template  →  .github/agents/TDD-refactor.agent.md
```

frontmatter 작성 기준:

1. `description`은 한글로 작성합니다.
	- 이 값은 "언제 이 에이전트를 써야 하는가"를 설명하는 문구입니다.
	- 검색 키워드 역할도 하므로, `실패 테스트`, `최소 구현`, `리팩터링`처럼 상황이 드러나는 표현을 넣는 것이 좋습니다.
2. `name`은 handoff에서 참조되므로 예시 값을 그대로 사용합니다.
	- 예를 들어 `agent: "TDD Green"` 이라고 썼다면, 대상 파일의 `name`도 반드시 `"TDD Green"` 이어야 합니다.
	- 공백, 대소문자, 철자 하나라도 다르면 다른 에이전트로 인식되지 않습니다.
3. `handoffs`는 객체 배열 형식으로 작성합니다.
	- 각 항목은 최소한 `label`, `agent`, `prompt` 세 속성을 가져야 합니다.
4. `handoffs`의 필수 속성은 아래 의미로 이해하면 됩니다.

| 속성 | 필수 여부 | 역할 | 작성 기준 |
|------|-----------|------|-----------|
| `label` | 필수 | Chat UI에서 보이는 handoff 버튼/동작 이름 | 사람이 읽었을 때 다음 단계가 바로 드러나게 작성합니다. 예: `"TDD Green으로 전달"` |
| `agent` | 필수 | 실제로 넘길 대상 에이전트 이름 | 대상 에이전트의 `name` 값과 정확히 같아야 합니다. 예: `"TDD Green"` |
| `prompt` | 필수 | 다음 에이전트에게 자동으로 전달할 작업 지시문 | 방금 끝난 단계, 현재 상태, 다음 단계에서 해야 할 일을 1~2문장으로 분명히 적습니다. |
| `send` | 선택 | 추가 컨텍스트 전달 방식 제어 | 이번 실습에서는 필수가 아니므로 생략해도 됩니다. |

필수 속성 예시:

```yaml
handoffs:
  - label: "TDD Green으로 전달"
	agent: "TDD Green"
	prompt: "Red 단계가 끝났습니다. 방금 추가된 실패 테스트를 통과시키는 최소 구현을 진행하세요."
```

실수하기 쉬운 포인트:

1. `label`은 설명용 이름이지, 실제 대상 에이전트 식별자가 아닙니다.
2. 실제 연결은 `agent` 값으로 이루어지므로 반드시 대상의 `name`과 일치해야 합니다.
3. `prompt`가 너무 짧거나 모호하면 다음 에이전트가 현재 상태를 정확히 이해하지 못할 수 있습니다.
4. YAML에서는 들여쓰기에 탭 대신 공백을 사용해야 합니다.
5. `handoffs:` 아래의 `- label:` 과 그 하위 속성(`agent`, `prompt`)은 같은 객체에 속하므로 들여쓰기 깊이를 유지해야 합니다.

### 2단계: `TDD-red.agent.md` 작성 (복붙용)

```md
---
description: "새 기능이나 동작에 대해 먼저 실패하는 테스트를 작성할 때 사용한다. TDD의 Red 단계로, 구현 없이 테스트만 작성한다."
name: "TDD Red"
tools: [read, edit, search, execute]
handoffs:
  - label: "TDD Green으로 전달"
	agent: "TDD Green"
	prompt: "Red 단계가 끝났습니다. 방금 추가된 실패 테스트를 통과시키는 최소 구현을 진행하세요."
---

당신은 테스트 작성 전문가입니다. TDD의 Red 단계를 담당합니다.

## 역할

- 주어진 기능 명세에 대해 실패하는 pytest 테스트를 `tests/test_manager.py` 에 작성한다.
- 구현 코드(`src/todo/manager.py`)는 절대 작성하거나 수정하지 않는다.
- 테스트 작성 후 `uv run pytest` 를 실행하여 테스트가 실패(Red)인지 확인한다.

## 테스트 작성 규칙

- `.github/instructions/testing.instructions.md` 파일의 지침을 따른다.
- 한 번에 하나의 기능에 대한 테스트만 작성한다.
- 정상 케이스와 예외 케이스를 모두 포함한다.

## 완료 조건

- 테스트가 실패(Red) 상태임을 확인한 후 TDD Green 에이전트에게 넘긴다.
```

### 3단계: `TDD-green.agent.md` 작성 (복붙용)

```md
---
description: "실패한 테스트를 통과시키는 최소 구현이 필요할 때 사용한다. TDD의 Green 단계로, 테스트를 통과시키는 데 필요한 코드만 작성한다."
name: "TDD Green"
tools: [read, edit, search, execute]
handoffs:
  - label: "TDD Refactor로 전달"
    agent: "TDD Refactor"
    prompt: "Green 단계가 끝났습니다. 현재 테스트 통과 상태를 유지하면서 코드 품질을 개선하세요."
---

당신은 구현 전문가입니다. TDD의 Green 단계를 담당합니다.

## 역할

- 현재 실패하는 테스트를 통과시키는 최소한의 코드를 `src/todo/manager.py` 에 작성한다.
- 구현 후 `uv run pytest` 를 실행하여 모든 테스트가 통과(Green)하는지 확인한다.

## 구현 원칙

- 테스트를 통과하는 데 필요한 코드만 작성한다.
- 과도한 최적화나 불필요한 기능 추가를 피한다.
- `.github/instructions/general.instructions.md` 파일의 지침을 따른다.

## 완료 조건

- 모든 테스트가 통과(Green)하면 TDD Refactor 에이전트에게 넘긴다.
```

### 4단계: `TDD-refactor.agent.md` 작성 (복붙용)

```md
---
description: "테스트가 모두 통과한 뒤 코드 품질을 개선할 때 사용한다. TDD의 Refactor 단계로, 테스트를 유지한 채 구조를 개선한다."
name: "TDD Refactor"
tools: [read, edit, search, execute]
handoffs:
  - label: "TDD Red로 전달"
    agent: "TDD Red"
    prompt: "Refactor 단계가 끝났습니다. 다음 요구사항에 대해 다시 실패하는 테스트부터 시작하세요."
---

당신은 리팩터링 전문가입니다. TDD의 Refactor 단계를 담당합니다.

## 역할

- 모든 테스트가 통과하는 상태를 유지하면서 코드 품질을 개선한다.
- 리팩터링 후 `uv run pytest` 를 실행하여 모든 테스트가 여전히 통과하는지 확인한다.

## 리팩터링 기준

- 중복 코드를 제거한다.
- 변수명, 함수명이 역할을 명확히 나타내도록 개선한다.
- 함수가 단일 책임 원칙을 따르도록 구조를 개선한다.

## 완료 조건

- 모든 테스트가 여전히 통과하면 TDD Red 에이전트에게 넘겨 다음 기능 사이클을 시작한다.
```

### 5단계: handoff 연결 검증

아래 값이 정확히 맞는지 확인합니다.

| 현재 에이전트 | handoff 대상 |
|---------------|--------------|
| `TDD Red` | `TDD Green` |
| `TDD Green` | `TDD Refactor` |
| `TDD Refactor` | `TDD Red` |

검증 포인트:

1. `handoffs`의 각 항목에 `label`, `agent`, `prompt`가 모두 있는지
2. `handoffs[].agent` 값과 대상 에이전트의 `name` 값이 정확히 일치하는지
3. 공백/대소문자 오타가 없는지

### 6단계: TDD 사이클 실행

1. Chat에서 `TDD Red` 에이전트를 선택합니다.
2. 아래 요청을 입력합니다.

```text
TodoManager.add() 메서드가 빈 문자열을 받으면 ValueError를 발생시키는 테스트를 작성해줘.
```

3. Red → Green → Refactor 순서로 전환되는지 확인합니다.

### 7단계: 실행 결과 확인

각 단계에서 아래를 확인합니다.

| 단계 | 기대 결과 |
|------|----------|
| Red | 실패하는 테스트가 먼저 추가됨 |
| Green | 최소 구현으로 테스트가 통과함 |
| Refactor | 동작 유지 상태에서 코드 품질이 개선됨 |

최종 검증 명령:

```powershell
uv run pytest -v
```

### 8단계: 자주 발생하는 문제와 해결

1. Red 단계에서 구현 코드를 함께 수정할 때
	- `TDD Red` 역할에 "구현 코드 수정 금지"가 있는지 확인
	- 요청에 "테스트만 작성"을 다시 명시

2. Green 단계에서 과도한 리팩터링을 할 때
	- "최소 구현만" 원칙을 재요청
	- 불필요한 구조 변경을 제외 범위로 지정

3. 자동 handoff가 되지 않을 때
	- `handoffs`를 문자열이 아닌 객체 형식으로 작성했는지 확인
	- `handoffs[].agent` 값과 `name` 문자열 일치 여부 확인
	- 에이전트 파일 저장 후 Chat 세션 재시작

4. 테스트 명령 실패 시
	- `uv sync` 실행 여부 확인
	- 프로젝트 루트에서 `uv run pytest -v` 실행했는지 확인

---

## 체크리스트

- [ ] `.github/agents/TDD-red.agent.md` 생성 완료
- [ ] `.github/agents/TDD-green.agent.md` 생성 완료
- [ ] `.github/agents/TDD-refactor.agent.md` 생성 완료
- [ ] `handoffs` 체인 Red → Green → Refactor → Red 연결 확인
- [ ] Red 단계에서 실패 테스트 작성 확인
- [ ] Green 단계에서 테스트 통과 확인
- [ ] Refactor 단계 후에도 전체 테스트 통과 확인

---

## 참고

막히면 `solution/` 폴더의 완성 예시를 참고하세요.
통합 실습은 `../09-integration/`에서 진행합니다.
