---
title: 4. 신규 기능을 위한 완전한 Spec Driven Development 사이클
layout: default
grand_parent: SDD
parent: speckit
nav_order: 4
permalink: /sdd/speckit/lab04
# nav_exclude: true
# search_exclude: true
--- 
# Lab 04: 신규 기능을 위한 완전한 Spec Driven Development 사이클

## 🎯 학습 목표

이 실습에서는 기존 애플리케이션에 신규 기능(할일 편집)을 추가하면서 Spec Kit의 전체 워크플로우를 처음부터 끝까지 경험합니다:

- 신규 기능 스펙 작성 (`/speckit.specify`)
- 명확화를 통한 의사결정 (`/speckit.clarify`)
- 구현 계획 수립 (`/speckit.plan`)
- 작업 목록 생성 (`/speckit.tasks`)
- TDD 기반 구현 (`/speckit.implement`)
- 품질 검증 및 완료

## 📋 사전 준비사항

- Node.js 20+
- Git 설치 및 이 저장소 클론
- Lab 01, Lab 02 완료
- 기본 애플리케이션(001-todo-webapp) 실행 가능 상태

## 🎬 실습 시나리오

**상황**: 사용자가 "할일 목록 앱에 편집 기능을 추가해주세요"라고 요청했습니다.

**목표**: Spec Kit 워크플로우를 따라 편집 기능을 완전히 구현하고 배포 가능한 상태로 만듭니다.

## 🚀 실습 단계

### 0단계: 기준선 확인

**목표**: 기존 애플리케이션이 정상 동작하는지 확인합니다.

```bash
# 개발 서버 실행
npm run dev

# 브라우저에서 http://localhost:3000 접속
# ✅ 할일 추가/완료/삭제 기능 정상 동작 확인
```

**확인 포인트**
- [ ] 할일 추가 기능 동작
- [ ] 완료 토글 기능 동작
- [ ] 삭제 기능 동작
- [ ] 새로고침 후 데이터 유지

---

### 1단계: /speckit.specify — 신규 기능 스펙 작성

**목표**: "할일 편집 기능"을 명확한 스펙 문서로 작성합니다.

**실행 방법**
```
Copilot Chat에서:
/speckit.specify 사용자가 기존 할일의 제목과 설명을 편집할 수 있는 기능 추가
```

**생성되는 파일**
- 스펙: `/specs/002-edit-todo/spec.md`
- 요구사항 체크리스트: `/specs/002-edit-todo/checklists/requirements.md`

**핵심 확인 포인트**
- [ ] User Story가 우선순위별(P1~P3)로 정의되어 있는가
  - **US1 (P1)**: 기존 할일 편집 (인라인 편집, 저장/취소)
  - **US2 (P2)**: 편집 중 유효성 검증 (빈 제목, 길이 초과 차단)
  - **US3 (P3)**: 편집 중 다른 작업 방지 (버튼 비활성화)
- [ ] Functional Requirements가 테스트 가능한가
  - FR-001: 편집 버튼 표시
  - FR-002: 편집 모드에서 현재 값 표시
  - FR-005: 제목 1~100자, 설명 0~500자 검증
  - FR-011: 편집 중 다른 버튼 비활성화
- [ ] Edge Cases가 명시되어 있는가
  - ESC 키로 취소
  - Enter 키로 저장 (제목 필드)
  - textarea에서 Enter는 줄바꿈
  - 완료된 항목도 편집 가능
  - 필터 상태 유지
- [ ] 구현 세부사항이 배제되어 있는가 (React, hooks, state 등 미언급)

**실습 활동**
```bash
# 생성된 스펙 문서 확인
code specs/002-edit-todo/spec.md

# 체크리스트 확인
code specs/002-edit-todo/checklists/requirements.md
```

---

### 2단계: /speckit.clarify — 핵심 질문으로 명확화

**목표**: 스펙의 모호한 부분을 질문을 통해 명확히 합니다.

**실행 방법**
```
Copilot Chat에서:
/speckit.clarify
```

**이번 실습에서 반영된 결정사항**
1. **Q: 편집 모드 진입 방식은?**
   - A: 각 항목에 별도 "편집" 버튼 추가 (명시적 액션)

2. **Q: 다중 줄 설명 편집 시 Enter 키 동작은?**
   - A: 설명은 textarea, Enter는 줄바꿈, 저장은 버튼만

3. **Q: 편집 중 변경사항 유실 방지 정책은?**
   - A: ESC/취소만 변경 무시, 다른 동작은 자유롭게 허용

**확인 포인트**
- [ ] spec.md의 Clarifications 섹션에 결정사항이 기록되었는가
- [ ] 모든 [NEEDS CLARIFICATION] 마커가 제거되었는가
- [ ] 결정사항이 User Story와 Requirements에 반영되었는가

**실습 활동**
```bash
# 명확화 결과 확인
code specs/002-edit-todo/spec.md
# Clarifications 섹션 확인
```

---

### 3단계: /speckit.plan — 구현 계획 및 설계

**목표**: 기술 스택, 아키텍처, 설계 산출물을 작성합니다.

**실행 방법**
```
Copilot Chat에서:
/speckit.plan
```

**생성되는 파일**
- 계획: `/specs/002-edit-todo/plan.md`
- 리서치: `/specs/002-edit-todo/research.md`
- 데이터 모델: `/specs/002-edit-todo/data-model.md`
- 계약: `/specs/002-edit-todo/contracts/ui-actions.md`
- 퀵스타트: `/specs/002-edit-todo/quickstart.md`

**핵심 확인 포인트**

**plan.md**
- [ ] 기술 스택이 기존 애플리케이션과 일치하는가
  - Next.js 16, React 19, TypeScript 5, Tailwind CSS 4
- [ ] 구현 전략이 명확한가
  - 인라인 편집 (별도 페이지/모달 아님)
  - 기존 validation.ts 재사용
  - editingId 상태로 동시 편집 방지
- [ ] 성능 예산이 정의되어 있는가
  - 편집 모드 전환: 100ms 이내
  - 저장 후 UI 업데이트: 50ms 이내

**data-model.md**
- [ ] 기존 TodoItem 타입에 updatedAt 필드가 추가되었는가
- [ ] EditingState 관리 방식이 명시되어 있는가

**contracts/ui-actions.md**
- [ ] updateTodo 동작이 명확히 정의되어 있는가
  - 입력: id, title, description
  - 출력: updatedAt 갱신, 로컬 스토리지 저장

**quickstart.md**
- [ ] 개발 환경 설정 방법이 명시되어 있는가
- [ ] TDD 구현 순서가 제시되어 있는가
- [ ] 수동 테스트 체크리스트가 포함되어 있는가

**실습 활동**
```bash
# 계획 문서 확인
code specs/002-edit-todo/plan.md
code specs/002-edit-todo/data-model.md
code specs/002-edit-todo/contracts/ui-actions.md

# 퀵스타트 가이드 확인
code specs/002-edit-todo/quickstart.md
```

---

### 4단계: /speckit.tasks — 실행 가능한 작업 목록 생성

**목표**: 구현 가능한 단위 작업으로 분해하고 TDD 순서를 정의합니다.

**실행 방법**
```
Copilot Chat에서:
/speckit.tasks
```

**생성되는 파일**
- 작업 목록: `/specs/002-edit-todo/tasks.md`

**핵심 확인 포인트**

**Phase 구조**
- [ ] Phase 1-2: Setup & Foundational
- [ ] Phase 3: User Story 1 (P1 - MVP)
- [ ] Phase 4: User Story 2 (P2)
- [ ] Phase 5: User Story 3 (P3)
- [ ] Phase 6: Polish & Cross-Cutting

**TDD 패턴**
- [ ] 각 Phase마다 "테스트 작성(Red) → 구현(Green)" 순서인가
  - 예: T007-T009(테스트) → T010-T017(구현)

**작업 세부사항**
- [ ] 모든 작업에 정확한 파일 경로가 명시되어 있는가
  - 예: `T010 [US1] updateTodo 함수 구현 in lib/hooks/useTodos.ts`
- [ ] 검증 방법이 명시되어 있는가
  - 예: `npm run test:unit -- useTodos.test.tsx`
- [ ] 병렬 실행 가능한 작업에 [P] 마킹이 있는가

**Phase 3 (US1 - MVP) 상세 확인**
```
테스트:
- T007: useTodos 훅 테스트 (updateTodo 함수)
- T008: TodoItem 컴포넌트 테스트 (편집 모드)
- T009: 편집 흐름 통합 테스트

구현:
- T010: updateTodo 함수 구현
- T011: TodoItem 편집 모드 상태 추가
- T012: TodoItem 편집 모드 UI 구현
- T013: 편집 버튼 추가
- T014: 저장 로직 구현
- T015: 취소 로직 구현
- T016: TodoList editingId 상태 관리
- T017: E2E 테스트
```

**실습 활동**
```bash
# 작업 목록 확인
code specs/002-edit-todo/tasks.md

# Phase 구조와 의존성 그래프 확인
# 병렬 실행 가능 작업([P]) 식별
```

---

### 5단계: /speckit.implement — TDD 기반 구현

**목표**: tasks.md의 작업 순서대로 TDD를 따라 구현합니다.

**실행 방법**
```
Copilot Chat에서:
/speckit.implement 진행
```

#### Phase 3: User Story 1 - 기본 편집 기능 (MVP)

**Step 1: 테스트 작성 (Red)**

**T007: useTodos 훅 테스트**
```bash
# Copilot Chat에 요청
T007 작업 진행해줘

# 생성된 파일 확인
code tests/unit/hooks/useTodos.test.tsx

# Red 확인 (테스트 실패)
npm run test:unit -- useTodos.test.tsx
```

**확인 포인트**
- [ ] updateTodo 함수 테스트가 추가되었는가
- [ ] 제목/설명 업데이트 검증
- [ ] updatedAt 타임스탬프 갱신 검증
- [ ] 로컬 스토리지 저장 검증
- [ ] 테스트가 실패(Red)하는가

**T008: TodoItem 컴포넌트 테스트**
```bash
# Copilot Chat에 요청
T008 작업 진행해줘

# Red 확인
npm run test:component -- TodoItem.test.tsx
```

**확인 포인트**
- [ ] 편집 버튼 클릭 시 편집 모드 전환 테스트
- [ ] 저장 버튼 클릭 시 onEdit 호출 테스트
- [ ] 취소 버튼 클릭 시 onCancelEdit 호출 테스트
- [ ] Enter/ESC 키 동작 테스트
- [ ] 테스트가 실패(Red)하는가

**T009: 통합 테스트**
```bash
# Copilot Chat에 요청
T009 작업 진행해줘

# Red 확인
npm run test:integration -- todo-flow.test.tsx
```

**확인 포인트**
- [ ] 편집 → 저장 → 목록 반영 검증
- [ ] 편집 → 취소 → 원래 내용 유지 검증
- [ ] 편집 → 저장 → 로컬 스토리지 지속성 검증
- [ ] 테스트가 실패(Red)하는가

---

**Step 2: 구현 (Green)**

**T010: updateTodo 함수 구현**
```bash
# Copilot Chat에 요청
T010 작업 진행해줘

# 생성된 코드 확인
code lib/hooks/useTodos.ts

# Green 확인
npm run test:unit -- useTodos.test.tsx
```

**확인 포인트**
- [ ] updateTodo 함수가 추가되었는가
- [ ] todos 배열에서 id로 항목 찾아 업데이트
- [ ] updatedAt 현재 시각(ISO-8601)으로 갱신
- [ ] saveTodos() 호출
- [ ] useTodos 반환값에 updateTodo 추가
- [ ] **T007 테스트가 통과(Green)하는가**

**T011-T015: TodoItem 컴포넌트 구현**
```bash
# 순차적으로 진행
T011 작업 진행해줘  # 편집 모드 상태 추가
T012 작업 진행해줘  # 편집 모드 UI 구현
T013 작업 진행해줘  # 편집 버튼 추가
T014 작업 진행해줘  # 저장 로직
T015 작업 진행해줘  # 취소 로직

# 중간 검증
npm run test:component -- TodoItem.test.tsx
```

**확인 포인트 (T011-T015 완료 후)**
- [ ] isEditing, editTitle, editDescription 상태 추가
- [ ] 편집 모드일 때 input/textarea 렌더링
- [ ] 표시 모드일 때 편집 버튼 표시
- [ ] handleSave: onEdit 호출 후 편집 모드 종료
- [ ] handleCancel: 원래 값 복원 후 편집 모드 종료
- [ ] Enter/ESC 키 핸들러 구현
- [ ] **T008 테스트가 통과(Green)하는가**

**T016: TodoList editingId 상태 관리**
```bash
# Copilot Chat에 요청
T016 작업 진행해줘

# 코드 확인
code components/TodoList.tsx

# 통합 테스트 검증
npm run test:integration -- todo-flow.test.tsx
```

**확인 포인트**
- [ ] editingId 상태 추가 (useState<string | null>)
- [ ] handleStartEdit, handleCancelEdit, handleEdit 구현
- [ ] TodoItem에 props 전달
  - isEditing={editingId === todo.id}
  - disabled={editingId !== null && editingId !== todo.id}
  - onStartEdit, onCancelEdit, onEdit
- [ ] **T009 통합 테스트가 통과(Green)하는가**

**T017: E2E 테스트**
```bash
# Copilot Chat에 요청
T017 작업 진행해줘

# E2E 테스트 실행
npm run test:e2e -- todo-core.spec.ts
```

**확인 포인트**
- [ ] 편집 시나리오 추가 (편집 버튼 → 수정 → 저장 → 새로고침 → 확인)
- [ ] **E2E 테스트가 통과(Green)하는가**

**✅ Checkpoint: User Story 1 완료**
```bash
# 편집 기능 관련 모든 테스트 실행
npm run test -- TodoItem useTodos todo-flow
# 결과: 모두 통과해야 함
```

---

#### Phase 4: User Story 2 - 유효성 검증

**Step 1: 테스트 작성 (Red)**

**T018-T019: 유효성 검증 테스트**
```bash
# Copilot Chat에 요청
T018, T019 작업을 순차적으로 진행해줘

# Red 확인
npm run test:component -- TodoItem.test.tsx
npm run test:integration -- todo-flow.test.tsx
```

**확인 포인트**
- [ ] 빈 제목 저장 시도 테스트
- [ ] 100자 초과 제목 테스트
- [ ] 500자 초과 설명 테스트
- [ ] 오류 발생 시 onEdit 호출 안 됨 검증
- [ ] 테스트가 실패(Red)하는가

**Step 2: 구현 (Green)**

**T020-T022: 유효성 검증 구현**
```bash
# Copilot Chat에 요청
T020, T021, T022 작업을 순차적으로 진행해줘

# Green 확인
npm run test:component -- TodoItem.test.tsx
npm run test:integration -- todo-flow.test.tsx
```

**확인 포인트**
- [ ] titleError, descriptionError 상태 추가
- [ ] handleSave에 validateTodoTitle, validateTodoDescription 추가
- [ ] 오류 시 저장 차단 (return)
- [ ] 오류 메시지 UI 표시 (text-red-500)
- [ ] 오류 시 입력 필드 테두리 red-500
- [ ] **유효성 검증 테스트가 통과(Green)하는가**

**T023: E2E 테스트**
```bash
# Copilot Chat에 요청
T023 작업 진행해줘

# E2E 테스트 실행
npm run test:e2e -- todo-core.spec.ts
```

**✅ Checkpoint: User Story 1 AND 2 완료**

---

#### Phase 5: User Story 3 - 동시 편집 방지

**Step 1: 테스트 작성 (Red)**

**T024-T025: disabled 상태 테스트**
```bash
# Copilot Chat에 요청
T024, T025 작업을 순차적으로 진행해줘

# Red 확인
npm run test:component -- TodoItem.test.tsx
npm run test:integration -- todo-flow.test.tsx
```

**확인 포인트**
- [ ] disabled prop 전달 시 버튼 비활성화 테스트
- [ ] 편집 중 다른 항목 버튼 비활성화 테스트
- [ ] 편집 완료 후 버튼 재활성화 테스트
- [ ] 테스트가 실패(Red)하는가

**Step 2: 구현 (Green)**

**T026-T028: disabled 상태 구현 및 접근성**
```bash
# Copilot Chat에 요청
T026, T027, T028 작업을 순차적으로 진행해줘

# Green 확인
npm run test:component -- TodoItem.test.tsx
npm run test:integration -- todo-flow.test.tsx
```

**확인 포인트**
- [ ] TodoItem에 disabled prop 추가
- [ ] 편집/삭제 버튼에 disabled 속성 추가
- [ ] disabled 시 시각적 피드백 (opacity-50, cursor-not-allowed)
- [ ] ARIA 라벨 추가
  - 편집 버튼: `aria-label="Edit {todo.title}"`
  - 저장 버튼: `aria-label="Save changes"`
  - 취소 버튼: `aria-label="Cancel editing"`
  - 제목 입력: `aria-label="Edit title"`
  - 설명 입력: `aria-label="Edit description"`
- [ ] 편집 모드 진입 시 제목 필드 자동 포커스 (autoFocus)
- [ ] **모든 테스트가 통과(Green)하는가**

**✅ Checkpoint: 모든 User Story 완료**

---

#### Phase 6: Polish & Quality

**T029: Lint 및 Typecheck**
```bash
# Lint 실행
npm run lint

# 오류가 있으면 수정
# Copilot Chat에 lint 오류 해결 요청

# TypeScript 타입 체크
npx tsc --noEmit

# 오류가 있으면 수정
```

**확인 포인트**
- [ ] lint 오류 없음
- [ ] TypeScript 타입 오류 없음

**T030: 전체 테스트 스위트 실행**
```bash
# 편집 기능 관련 모든 테스트 실행
npm run test -- TodoItem TodoForm useTodos todo-flow filtering --run

# 결과 확인
# ✅ TodoItem: 18/18 passed
# ✅ TodoForm: 3/3 passed
# ✅ useTodos: 8/8 passed
# ✅ todo-flow: 6/6 passed
# ✅ filtering: 1/1 passed
# ✅ Total: 39/39 passed
```

**확인 포인트**
- [ ] 편집 기능 핵심 테스트 39/39 통과

**T031-T034: 수동 테스트, 성능, 문서**

수동 테스트 체크리스트 (quickstart.md 참조):
- [ ] 편집 버튼 클릭 → 편집 모드 전환
- [ ] 제목/설명 수정 → 저장 → 반영 확인
- [ ] Enter 키로 저장 (제목 필드)
- [ ] ESC 키로 취소
- [ ] 빈 제목 저장 시도 → 오류 메시지
- [ ] 편집 중 다른 항목 버튼 비활성화
- [ ] 편집 완료 후 버튼 재활성화

성능 확인:
- [ ] 편집 모드 전환이 즉시 반응하는가
- [ ] 저장 후 UI 업데이트가 부드러운가

**✅ 최종 확인: 모든 Phase 완료**

---

### 6단계: 실습 종합 확인

**기능 동작 확인**
```bash
# 개발 서버 실행
npm run dev

# 브라우저에서 테스트
```

**수동 테스트 시나리오**
1. 할일 추가 → 편집 버튼 클릭 → 제목 변경 → 저장 → 확인
2. 편집 → ESC 키 → 변경사항 취소 확인
3. 편집 → 제목을 빈 값으로 → 저장 시도 → 오류 메시지 확인
4. 한 항목 편집 중 → 다른 항목의 편집/삭제 버튼 비활성화 확인
5. 편집 완료 → 새로고침 → 변경사항 유지 확인

**산출물 확인**
```bash
# 스펙 문서
code specs/002-edit-todo/spec.md
code specs/002-edit-todo/plan.md
code specs/002-edit-todo/tasks.md

# 구현 파일
code lib/hooks/useTodos.ts        # updateTodo 함수
code components/TodoItem.tsx       # 편집 모드
code components/TodoList.tsx       # editingId 상태

# 테스트 파일
code tests/unit/hooks/useTodos.test.tsx
code tests/component/TodoItem.test.tsx
code tests/integration/todo-flow.test.tsx
code tests/e2e/todo-core.spec.ts
```

---

## 📊 실습 결과 확인

### 완료 체크리스트

**Phase 1-2: Setup**
- [ ] 기존 validation 유틸 확인 완료
- [ ] 기존 useTodos 훅 구조 분석 완료
- [ ] 기존 TodoItem 컴포넌트 구조 분석 완료

**Phase 3: US1 (MVP)**
- [ ] T007-T009: 테스트 작성 완료 (Red 확인)
- [ ] T010: updateTodo 함수 구현 완료
- [ ] T011-T015: TodoItem 편집 모드 구현 완료
- [ ] T016: TodoList editingId 상태 관리 완료
- [ ] T017: E2E 테스트 통과
- [ ] **US1 단독 테스트 가능 확인**

**Phase 4: US2**
- [ ] T018-T019: 유효성 검증 테스트 작성 완료 (Red 확인)
- [ ] T020-T022: 유효성 검증 구현 완료
- [ ] T023: E2E 테스트 통과
- [ ] **US1 AND US2 동시 동작 확인**

**Phase 5: US3**
- [ ] T024-T025: disabled 상태 테스트 작성 완료 (Red 확인)
- [ ] T026-T028: disabled 상태 구현 및 접근성 개선 완료
- [ ] **모든 US 동시 동작 확인**

**Phase 6: Polish**
- [ ] T029: Lint/Typecheck 통과
- [ ] T030: 전체 테스트 스위트 통과 (39/39)
- [ ] T031-T034: 수동 테스트, 성능, 문서 완료

### 테스트 결과 요약

```
편집 기능 테스트 결과:
✅ TodoItem: 18/18 passed
   - Edit Mode: 8 tests
   - Validation: 5 tests
   - Disabled State: 5 tests

✅ TodoForm: 3/3 passed
✅ useTodos: 8/8 passed (updateTodo 포함)
✅ todo-flow: 6/6 passed
   - 편집 흐름 테스트
   - 유효성 검증 테스트
   - disabled 상태 테스트
✅ filtering: 1/1 passed

━━━━━━━━━━━━━━━━━━━━━━
✅ Total: 39/39 passed (100%)
```

### 구현된 기능

1. **인라인 편집**: 편집 버튼 클릭으로 즉시 편집 모드 전환
2. **키보드 단축키**: 
   - Enter (제목 필드): 저장
   - ESC: 취소
   - Enter (설명 필드): 줄바꿈
3. **실시간 유효성 검증**: 
   - 빈 제목 차단
   - 제목 100자 제한
   - 설명 500자 제한
4. **동시 편집 방지**: 한 항목 편집 중 다른 항목 버튼 비활성화
5. **접근성**: 
   - 상세한 ARIA 라벨
   - 자동 포커스
   - 키보드 네비게이션
6. **데이터 지속성**: 로컬 스토리지 자동 저장

---

## 🎓 학습 포인트

### Spec Driven Development의 핵심

1. **명확성 우선**: 
   - 스펙 작성 시 구현 세부사항 배제
   - 명확화 단계에서 모호성 제거

2. **독립성 보장**:
   - 각 User Story가 독립적으로 테스트 가능
   - 우선순위별 단계적 구현 가능

3. **TDD 패턴**:
   - Red (테스트 실패) → Green (구현) 반복
   - 테스트가 구현의 가이드 역할

4. **산출물 연결**:
   - Spec → Plan → Tasks → Implementation
   - 각 단계의 산출물이 다음 단계의 입력

5. **품질 검증**:
   - Lint/Typecheck로 코드 품질 보장
   - 테스트로 기능 정확성 보장
   - 수동 테스트로 사용자 경험 확인

### TDD 실천 패턴

1. **테스트 먼저**: 구현 전에 테스트를 작성하여 요구사항을 명확히 함
2. **작은 단위**: 각 작업을 작은 단위로 분해하여 진행
3. **빠른 피드백**: 각 단계마다 테스트 실행으로 즉시 확인
4. **리팩토링 안전망**: 테스트가 있어 리팩토링 시 회귀 방지

---

## 💡 팁

### Copilot Chat 활용법

1. **단계별 진행**: 각 Phase를 순차적으로 진행
   ```
   /speckit.specify → /speckit.clarify → /speckit.plan → /speckit.tasks → /speckit.implement
   ```

2. **작업 단위 요청**: 한 번에 1-2개 작업씩 요청
   ```
   T007 작업 진행해줘
   T010 작업 진행해줘
   ```

3. **TDD 주기 명시**: Red-Green 사이클을 명시적으로 요청
   ```
   T007 테스트 작성 후 Red 확인해줘
   T010 구현 후 Green 확인해줘
   ```

4. **중간 검증**: 각 단계마다 테스트 실행으로 확인
   ```
   npm run test:component -- TodoItem.test.tsx
   ```

### 문제 해결

**"테스트가 통과하지 않아요"**
1. 테스트 파일과 구현 파일을 모두 확인
2. 오류 메시지를 Copilot Chat에 복사하여 해결 요청
3. 필요시 캐시 클리어: `npm run test -- --no-cache`

**"Lint/Typecheck 오류가 발생해요"**
1. 오류 메시지를 확인하고 Copilot Chat에 해결 요청
2. import 누락 확인
3. 타입 정의 확인

**"개발 서버가 실행되지 않아요"**
1. 포트 충돌 확인: 3000 포트가 사용 중인지 확인
2. 의존성 재설치: `rm -rf node_modules && npm install`

---

## 🔍 심화 학습

### 추가 실습 아이디어

1. **우선순위 변경 기능**: 할일의 순서를 드래그앤드롭으로 변경
2. **카테고리 기능**: 할일에 카테고리 태그 추가
3. **검색 기능**: 제목/설명으로 할일 검색
4. **마감일 기능**: 할일에 마감일 추가 및 정렬

### Spec Kit 고급 활용

1. **성능 최적화**: 
   - React.memo 적용
   - useMemo/useCallback 활용
   - Virtual scrolling 구현

2. **접근성 강화**:
   - 스크린 리더 테스트
   - 키보드 네비게이션 개선
   - WCAG 2.1 AA 준수

3. **에러 처리**:
   - ErrorBoundary 추가
   - Toast 알림 시스템
   - 오류 로깅

---

## 📚 참고 자료

- [GitHub Spec Kit 문서](https://github.com/github/spec-kit)
- [React 19 Documentation](https://react.dev/)
- [Next.js 16 Documentation](https://nextjs.org/docs)
- [Vitest Documentation](https://vitest.dev/)
- [Playwright Documentation](https://playwright.dev/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)

---

## ✅ 최종 확인

- [ ] 편집 기능이 정상 동작한다
- [ ] 모든 테스트가 통과한다 (39/39)
- [ ] Lint/Typecheck 오류가 없다
- [ ] 수동 테스트 체크리스트를 완료했다
- [ ] 스펙 → 계획 → 작업 → 구현의 흐름을 이해했다
- [ ] TDD Red-Green 사이클을 경험했다

**축하합니다! 🎉 완전한 Spec Driven Development 사이클을 완료했습니다!**
