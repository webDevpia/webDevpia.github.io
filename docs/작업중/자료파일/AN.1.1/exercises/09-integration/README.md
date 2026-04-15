# 09. 통합 실습: 프로젝트 기반 적용

## 목표

앞서 만든 커스터마이징 산출물(Custom Instructions, Prompt Files, Custom Agents)을
Todo Manager 프로젝트에 한 번에 연결해 실제 기능 구현 흐름을 경험합니다.

이번 시간에는 다음 흐름을 하나의 개발 사이클로 묶습니다.

1. 선행 산출물 점검
2. Planner로 구현 계획 수립
3. `docs/PRODUCT.md` 요구사항 갱신
4. TDD Red → Green → Refactor 실행
5. `uv run pytest -v` 로 최종 검증

---

## 배경 지식

### 1) 통합 실습이란 무엇인가

통합 실습은 개별 시간에 따로 배운 커스터마이징 요소를 실제 프로젝트 작업 흐름으로 연결하는 단계입니다.

- Custom Instructions: 항상 적용되는 공통 규칙
- Prompt Files: 반복 작업을 실행하는 표준 템플릿
- Planner Agent: 구현 전에 계획을 세우는 읽기 전용 에이전트
- Context Engineering 문서: 요구사항과 제약 조건을 명확히 제공하는 문맥
- TDD Agents: Red → Green → Refactor 사이클 자동화

즉, 이번 시간의 핵심은 "새 파일 하나를 만드는 것"이 아니라,
"AI가 일관된 규칙과 문맥 속에서 기능 구현을 끝까지 수행하게 만드는 것"입니다.

### 2) 이번 실습에서 결합되는 요소

| 요소 | 위치 | 이번 실습에서 하는 역할 |
|------|------|-------------------------|
| 공통 지침 | `.github/copilot-instructions.md` | 예외 처리, 문서화, 품질 기준 적용 |
| 파일별 지침 | `.github/instructions/*.instructions.md` | Python/pytest 규칙 적용 |
| 프롬프트 파일 | `.github/prompts/*.prompt.md` | 반복 요청 템플릿 제공 |
| Planner 에이전트 | `.github/agents/planner.agent.md` | 구현 계획 수립 |
| TDD 에이전트 | `.github/agents/TDD-*.agent.md` | Red → Green → Refactor 자동 진행 |
| 제품 요구사항 문서 | `docs/PRODUCT.md` | 기능 요구사항의 기준 문서 |

### 3) 왜 `PRODUCT.md`를 먼저 갱신하는가

통합 실습에서는 "무엇을 구현할지"를 먼저 문서로 고정해야 Planner와 TDD 에이전트가 같은 기준으로 동작합니다.

- Planner는 요구사항을 기반으로 계획을 세웁니다.
- TDD Red는 요구사항을 기반으로 실패하는 테스트를 작성합니다.
- TDD Green/Refactor는 그 테스트를 통과시키는 방향으로 구현합니다.

요구사항 문서가 없거나 모호하면, 에이전트마다 다른 가정을 하게 되어 결과가 흔들립니다.

### 4) 이번 실습의 성공 기준

아래 4가지가 모두 만족되면 통합 실습이 완료된 것입니다.

1. Planner가 구현 순서와 검증 기준을 제시한다.
2. `docs/PRODUCT.md`에 새 기능 요구사항이 반영된다.
3. TDD Red → Green → Refactor 흐름이 실제 코드와 테스트에 반영된다.
4. `uv run pytest -v` 실행 결과 전체 테스트가 통과한다.

---

## 실습 단계

### 0단계: 선행 산출물 점검

13교시를 시작하기 전 `.github/` 폴더가 최소한 아래 구조를 갖추고 있는지 확인합니다.

```text
.github/
├── copilot-instructions.md
├── instructions/
│   ├── general.instructions.md
│   └── testing.instructions.md
├── prompts/
│   ├── new-feature.prompt.md
│   └── write-tests.prompt.md
└── agents/
    ├── planner.agent.md
    ├── TDD-red.agent.md
    ├── TDD-green.agent.md
    └── TDD-refactor.agent.md
```

파일이 없다면 아래 완성본을 참고하거나 복사해 채웁니다.

```text
exercises/04-custom-instructions/solution/copilot-instructions.md      →  .github/copilot-instructions.md
exercises/04-custom-instructions/solution/general.instructions.md      →  .github/instructions/general.instructions.md
exercises/04-custom-instructions/solution/testing.instructions.md      →  .github/instructions/testing.instructions.md
exercises/05-prompt-files/solution/new-feature.prompt.md              →  .github/prompts/new-feature.prompt.md
exercises/05-prompt-files/solution/write-tests.prompt.md              →  .github/prompts/write-tests.prompt.md
exercises/06-custom-agents/solution/planner.agent.md                  →  .github/agents/planner.agent.md
exercises/08-tdd/solution/TDD-red.agent.md                            →  .github/agents/TDD-red.agent.md
exercises/08-tdd/solution/TDD-green.agent.md                          →  .github/agents/TDD-green.agent.md
exercises/08-tdd/solution/TDD-refactor.agent.md                       →  .github/agents/TDD-refactor.agent.md
```

추가 확인:

1. `docs/PRODUCT.md` 파일이 있는지 확인합니다.
2. Chat 드롭다운에서 `Planner`, `TDD Red`, `TDD Green`, `TDD Refactor`가 보이는지 확인합니다.
3. `/` 목록에서 `New Feature`, `Write Tests` 프롬프트가 보이는지 확인합니다.

### 1단계: 실습 시나리오 이해

이번 통합 실습에서는 Todo Manager에 **상태별 필터링** 기능을 추가합니다.

기능 목표:

- `pending` 상태인 할일만 조회할 수 있어야 합니다.
- `done` 상태인 할일만 조회할 수 있어야 합니다.
- 기존 기능(추가, 전체 조회, 완료 처리, 삭제)은 깨지지 않아야 합니다.

이 단계에서는 메서드명보다 동작 정의가 더 중요합니다.
구체적인 구현 방식은 Planner 계획과 TDD 사이클에서 확정합니다.

### 2단계: Planner로 구현 계획 수립

#### 2-1. 에이전트 선택

Copilot Chat에서 **Planner** 에이전트를 선택합니다.

#### 2-2. 계획 요청

아래 요청을 그대로 입력합니다.

```text
TodoManager에 상태(pending/done)로 할일을 필터링하는 기능을 구현할 계획을 세워줘.

다음 항목을 포함해줘:
1. 수정할 파일 목록
2. TDD Red → Green → Refactor 순서
3. 각 단계의 완료 기준
4. 테스트해야 할 핵심 시나리오
```

#### 2-3. 결과 확인

Planner 결과에서 아래 항목을 확인합니다.

| 확인 항목 | 기대 결과 |
|----------|----------|
| 파일 목록 | `docs/PRODUCT.md`, `src/todo/manager.py`, `tests/test_manager.py` 등이 언급됨 |
| TDD 순서 | Red → Green → Refactor 순서가 분리되어 제시됨 |
| 테스트 시나리오 | pending/done 필터링, 회귀 테스트 등이 포함됨 |
| 구현 범위 | 불필요한 대규모 리팩터링 없이 현재 기능에 필요한 범위로 제한됨 |

> **팁**: Planner가 코드를 직접 작성하려 하면, 다시 요청해 "구현하지 말고 계획만 제시"라고 고정합니다.

### 3단계: `docs/PRODUCT.md` 업데이트

#### 3-1. 업데이트할 위치 확인

`docs/PRODUCT.md`를 열고 현재 기능 목록 아래에 새 기능 요구사항을 추가합니다.

#### 3-2. 복붙용 예시 추가

아래 블록 중 하나를 현재 문서 구조에 맞게 반영합니다.

옵션 A: 기능 표에 바로 추가

```md
| 상태별 필터링 | 상태(pending/done)로 할일 목록을 필터링한다 |
```

옵션 B: 별도 섹션으로 추가

```md
## 추가 예정 기능 (13교시 통합 실습)

| 기능 | 설명 | 상태 |
|------|------|------|
| 상태별 필터링 | 상태(pending/done)로 할일 목록을 필터링한다 | 🔲 미구현 |
```

#### 3-3. 문서 갱신 확인

아래를 확인합니다.

1. 기능 설명이 "상태(pending/done)"를 명확히 포함하는지 확인
2. 기존 비기능 요구사항/제약 사항과 충돌하지 않는지 확인
3. 이후 TDD 에이전트가 참조할 수 있도록 문서가 저장되어 있는지 확인

### 4단계: TDD Red 실행

#### 4-1. 에이전트 선택

Copilot Chat에서 **TDD Red** 에이전트를 선택합니다.

#### 4-2. 실행 입력

아래 텍스트를 입력합니다. Planner 출력은 실제 생성된 계획으로 바꿔 붙여넣습니다.

```text
상태별 필터링 기능에 대한 실패하는 pytest 테스트부터 작성해줘.

참조 문서:
- docs/PRODUCT.md

대상 파일:
- src/todo/manager.py
- tests/test_manager.py

Planner 계획:
[여기에 Planner가 만든 계획을 붙여넣기]
```

#### 4-3. Red 단계 확인

아래 항목을 확인합니다.

| 확인 항목 | 기대 결과 |
|----------|----------|
| 테스트 추가 | `tests/test_manager.py`에 새 테스트가 생김 |
| 실패 상태 | 새 테스트가 현재 구현 미완성 때문에 실패함 |
| 구조 | AAA 패턴, 테스트 네이밍 규칙이 반영됨 |

수동 확인 명령:

```powershell
uv run pytest -v
```

> **중요**: Red 단계에서는 실패가 정상입니다. 이 단계에서 테스트가 이미 모두 통과하면, 실패 조건이 약한지 다시 점검해야 합니다.

### 5단계: Green → Refactor 진행

#### 5-1. 자동 handoff 확인

TDD Red가 끝난 뒤 `TDD Green`으로 자동 전환되는지 확인합니다.

- 자동 전환되면 그대로 진행합니다.
- 자동 전환되지 않으면 수동으로 `TDD Green`을 선택합니다.

#### 5-2. Green 단계 확인

Green 단계에서 아래를 확인합니다.

1. 테스트를 통과시키는 최소 구현만 추가되는지 확인
2. `src/todo/manager.py`에 상태별 필터링 로직이 반영되는지 확인
3. 과도한 구조 변경 없이 현재 요구사항에 필요한 수준으로 구현되는지 확인

필요 시 수동 요청 예시:

```text
방금 작성한 실패 테스트를 통과시키는 최소 구현만 추가해줘.
불필요한 리팩터링은 하지 말아줘.
```

#### 5-3. Refactor 단계 확인

Refactor 단계에서 아래를 확인합니다.

1. 동작을 바꾸지 않고 중복 제거/가독성 개선이 이루어지는지 확인
2. 타입 힌트, docstring, 네이밍 규칙이 유지되는지 확인
3. 테스트가 계속 통과하는지 확인

필요 시 수동 요청 예시:

```text
현재 테스트를 깨지 않는 범위에서만 코드 품질을 개선해줘.
중복 제거와 가독성 개선에 집중해줘.
```

### 6단계: 최종 검증

#### 6-1. 전체 테스트 실행

```powershell
uv run pytest -v
```

#### 6-2. 최종 결과 확인

아래 항목이 모두 만족되는지 확인합니다.

| 확인 항목 | 기대 결과 |
|----------|----------|
| 전체 테스트 | `uv run pytest -v` 전체 통과 |
| 요구사항 반영 | `docs/PRODUCT.md`에 상태별 필터링 기능이 명시됨 |
| 구현 반영 | `src/todo/manager.py`에 필터링 기능이 구현됨 |
| 테스트 반영 | `tests/test_manager.py`에 새 기능 테스트가 존재함 |
| 규칙 반영 | docstring, 타입 힌트, 예외 처리 규칙이 유지됨 |

#### 6-3. 완료 후 정리

가능하면 `docs/PRODUCT.md`의 상태 값을 `✅ 구현 완료`로 갱신합니다.

### 7단계: 자주 발생하는 문제와 해결

1. Planner가 계획 대신 코드를 작성할 때
    - `planner.agent.md`의 `tools`가 읽기 전용(`read`, `search`)인지 확인
    - 다시 요청할 때 "구현하지 말고 계획만 제시"를 명시

2. TDD Red 이후 자동 전환이 안 될 때
    - `TDD-red.agent.md`의 `handoffs[].agent` 값이 `TDD Green`과 정확히 일치하는지 확인
    - `handoffs` 항목이 문자열이 아니라 `label`, `agent`, `prompt`를 포함한 객체인지 확인
    - 이름 대소문자와 공백이 맞는지 확인

3. `PRODUCT.md`를 업데이트했는데 반영이 약할 때
    - TDD 요청에 `docs/PRODUCT.md`를 다시 명시
    - Planner 출력과 제품 요구사항을 함께 붙여넣어 재실행

4. `uv run pytest -v` 실행이 안 될 때
    - 루트 README의 환경 설정대로 `uv sync`가 완료되었는지 확인
    - 프로젝트 루트에서 명령을 실행했는지 확인

5. 최종 테스트 실패가 새 기능 이전부터 존재할 때
    - 이 통합 실습은 4~12교시 산출물이 갖춰진 상태를 전제로 함
    - 선행 실습이 미완성이라면 해당 exercise의 solution 기준으로 먼저 맞춘 뒤 다시 진행

---

## 체크리스트

- [ ] `.github/` 선행 산출물 점검 완료
- [ ] Planner가 구현 계획을 마크다운으로 제시함
- [ ] `docs/PRODUCT.md`에 상태별 필터링 요구사항 추가 완료
- [ ] TDD Red: 실패하는 테스트 작성 완료
- [ ] TDD Green: 테스트 통과하는 최소 구현 완료
- [ ] TDD Refactor: 코드 품질 개선 완료
- [ ] 최종 `uv run pytest -v` 전체 통과

---

## 완성 참조본

최종 결과 확인용 자료는 `solution/` 폴더에 있습니다.

- `solution/PRODUCT.md` : 통합 실습 완료 후 요구사항 문서 예시
- `solution/.github-snapshot/` : 완성된 `.github/` 구조 참조본
