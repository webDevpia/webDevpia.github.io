---
title: 3. GitHub Spec Kit을 활용한 Spec Driven Development
layout: default
grand_parent: SDD
parent: speckit
nav_order: 3
permalink: /sdd/speckit/lab03
# nav_exclude: true
# search_exclude: true
--- 
# Lab 03: GitHub Spec Kit을 활용한 Spec Driven Development

## 🎯 학습 목표

이 실습에서는 GitHub Spec Kit 워크플로우를 단계적으로 따라가며, 스펙 기반 개발(Spec Driven Development)을 실습합니다:
- 프로젝트 헌법(Constitution) 수립 및 템플릿 동기화
- 스펙 작성 → 명확화(Clarify) → 계획(Plan) → 작업(Task) 흐름 체험
- 산출물 간 연결(스펙/리서치/데이터 모델/계약/퀵스타트/작업 목록) 확인

## 📋 사전 준비사항

- Node.js 20+
- Git 설치 및 이 저장소 클론
- Lab 01 완료(테스트 환경 구축)

## 🚀 실습 단계

> 이 실습은 이미 생성된 산출물을 참고해 같은 과정을 재현하는 흐름으로 구성됩니다. 각 단계에서 “무엇을 만들고, 어떤 파일이 생성되는지”를 확인합니다.

### 1단계: speckit.constitute — 프로젝트 헌법 수립

**목표**: 코드 품질, 테스트 기준, UX 일관성, 성능 원칙을 수립하고 프로젝트 전반의 거버넌스를 정의합니다.

**확인 파일**
- 헌법 파일: [/.specify/memory/constitution.md](/.specify/memory/constitution.md)
- 템플릿 동기화: [/.specify/templates/plan-template.md](/.specify/templates/plan-template.md), [/.specify/templates/spec-template.md](/.specify/templates/spec-template.md), [/.specify/templates/tasks-template.md](/.specify/templates/tasks-template.md)

**핵심 확인 포인트**
- 헌법 원칙(코드 품질/테스트/UX/성능)이 명시되어 있는가
- Governance 규칙과 버전 정책이 정의되어 있는가
- Plan/Spec/Tasks 템플릿에 헌법 체크가 반영되어 있는가

---

### 2단계: speckit/.specify — 기능 스펙 작성

**목표**: “할일 목록 웹앱” 기능을 스펙으로 문서화합니다.

**확인 파일**
- 스펙: [/specs/001-todo-webapp/spec.md](/specs/001-todo-webapp/spec.md)
- 요구사항 체크리스트: [/specs/001-todo-webapp/checklists/requirements.md](/specs/001-todo-webapp/checklists/requirements.md)

**핵심 확인 포인트**
- 사용자 스토리(P1~P3)가 독립적으로 테스트 가능한가
- 기능 요구사항, 엣지 케이스, 성공 기준이 명확한가
- 구현 세부사항이 과도하게 들어가지 않았는가

---

### 3단계: speckit.clarify — 핵심 질문으로 명확화

**목표**: 스펙의 모호성을 제거하기 위해 최대 5개의 질문을 통해 결정사항을 확정합니다.

**이번 실습에서 반영된 결정**
- 기본 정렬: 미완료 우선, 완료는 하단 분리
- 다크모드 기본값: 시스템 설정 → 사용자 전환 시 저장
- 완료 토글 시 이동: 상태 변경 시 섹션 이동
- 삭제 정책: 삭제 전 확인 모달
- 스토리지 실패: 경고 표시 후 세션 내 임시 상태로 동작

**확인 파일**
- 명확화 기록: [/specs/001-todo-webapp/spec.md](/specs/001-todo-webapp/spec.md)

---

### 4단계: speckit.plan — 구현 계획 및 설계 산출물 생성

**목표**: 기술 스택, 프로젝트 구조, 설계 산출물을 정리하고 구현 계획을 수립합니다.

**확인 파일**
- 구현 계획: [/specs/001-todo-webapp/plan.md](/specs/001-todo-webapp/plan.md)
- 리서치: [/specs/001-todo-webapp/research.md](/specs/001-todo-webapp/research.md)
- 데이터 모델: [/specs/001-todo-webapp/data-model.md](/specs/001-todo-webapp/data-model.md)
- 계약(로컬 스토리지/동작): [/specs/001-todo-webapp/contracts/local-storage.schema.json](/specs/001-todo-webapp/contracts/local-storage.schema.json), [/specs/001-todo-webapp/contracts/ui-actions.md](/specs/001-todo-webapp/contracts/ui-actions.md)
- 퀵스타트: [/specs/001-todo-webapp/quickstart.md](/specs/001-todo-webapp/quickstart.md)
- 에이전트 컨텍스트: [.github/agents/copilot-instructions.md](.github/agents/copilot-instructions.md)

**핵심 확인 포인트**
- 기술 스택이 요구사항과 일치하는가(Next.js, React, TS, Tailwind 등)
- 성능 예산/제약 사항이 계획에 반영되었는가
- 프로젝트 구조가 실제 코드베이스와 일치하는가

---

### 5단계: speckit.tasks — 실행 가능한 작업 목록 생성

**목표**: 사용자 스토리별로 독립 구현이 가능한 작업 리스트를 작성합니다.

**확인 파일**
- 작업 목록: [/specs/001-todo-webapp/tasks.md](/specs/001-todo-webapp/tasks.md)

**핵심 확인 포인트**
- 작업이 사용자 스토리별로 분리되어 있는가
- 테스트 작업이 먼저 정의되어 있는가(TDD)
- 파일 경로가 명시되어 있는가

---

### 6단계: speckit.analyze — 스펙/계획/작업 정합성 분석

**목표**: 스펙, 계획, 작업 목록 간의 누락/모호성/불일치를 분석하고 수정 후보를 도출합니다.

**확인 파일**
- 분석 결과는 Copilot Chat 응답으로 제공되며, 필요 시 문서를 보정합니다.

**핵심 확인 포인트**
- 요구사항 대비 작업 누락이 없는가(커버리지 100%)
- 모호한 문구/표현이 남아 있지 않은가
- 헌법 원칙(품질/테스트/UX/성능)이 작업에 반영되었는가
- typecheck/lint 기준이 명확하게 고정되어 있는가

---

### 7단계: speckit.implement — 작업 구현 및 검증

**목표**: Tasks 문서에 정의된 작업을 실제 코드/테스트로 구현하고, lint/typecheck/test 기준으로 품질을 검증합니다.

**이번 실습에서 구현된 핵심 산출물(예시)**
- 앱 조립(메인 화면): [/app/page.tsx](/app/page.tsx)
- 레이아웃/메타데이터: [/app/layout.tsx](/app/layout.tsx)
- 공통 타입: [/lib/types/todo.ts](/lib/types/todo.ts), [/lib/types/preferences.ts](/lib/types/preferences.ts)
- 유틸(검증/스토리지/필터/테마):
	- [/lib/utils/validation.ts](/lib/utils/validation.ts)
	- [/lib/utils/storage.ts](/lib/utils/storage.ts)
	- [/lib/utils/filter.ts](/lib/utils/filter.ts)
	- [/lib/utils/theme.ts](/lib/utils/theme.ts)
- 상태 훅: [/lib/hooks/useTodos.ts](/lib/hooks/useTodos.ts), [/lib/hooks/usePreferences.ts](/lib/hooks/usePreferences.ts)
- UI 컴포넌트:
	- [/components/TodoForm.tsx](/components/TodoForm.tsx)
	- [/components/TodoList.tsx](/components/TodoList.tsx)
	- [/components/TodoItem.tsx](/components/TodoItem.tsx)
	- [/components/FilterTabs.tsx](/components/FilterTabs.tsx)
	- [/components/ThemeToggle.tsx](/components/ThemeToggle.tsx)
	- [/components/ConfirmModal.tsx](/components/ConfirmModal.tsx)
	- [/components/EmptyState.tsx](/components/EmptyState.tsx)
	- [/components/StorageErrorBanner.tsx](/components/StorageErrorBanner.tsx)


- [x] T033 [US3] 테마 클래스 적용 및 시스템 동기화 in /app/layout.tsx, /lib/utils/theme.ts

**중간 버그 수정 사례 (Copilot Chat 활용)**

실습 도중 발생한 버그를 해결하는 Spec-Kit의 정석 패턴(Task Update → TDD)을 적용해 해결합니다.

1. **상황**: 다크모드 수동 전환 시 HTML 클래스는 변하지만 실제 배경색이 변경되지 않음 (테스트 누락)
2. **절차**:
   - `tasks.md`에 `[Bug] Fix: 다크모드...` 항목 추가
   - Copilot Chat에 "TDD 절차(Test 강화 → Verify (Red 확인) → Fix → Update (tasks.md 업데이트)"로 수정 요청
3. **결과**:
   - 테스트 강화: `/tests/e2e/theme-responsive.spec.ts`에 `toHaveCSS` 검증 추가
   - 구현 수정: `/app/globals.css`에 `@custom-variant dark` 추가 (Tailwind v4 대응)
   - 작업 완료: `tasks.md` 업데이트 완료

**테스트 산출물(예시)**
- Unit: [/tests/unit/utils/validation.test.ts](/tests/unit/utils/validation.test.ts), [/tests/unit/utils/storage.test.ts](/tests/unit/utils/storage.test.ts), [/tests/unit/utils/filter.test.ts](/tests/unit/utils/filter.test.ts)
- Hook Unit: [/tests/unit/hooks/useTodos.test.tsx](/tests/unit/hooks/useTodos.test.tsx)
- Component: [/tests/component/TodoForm.test.tsx](/tests/component/TodoForm.test.tsx), [/tests/component/FilterTabs.test.tsx](/tests/component/FilterTabs.test.tsx), [/tests/component/ThemeToggle.test.tsx](/tests/component/ThemeToggle.test.tsx)
- Integration: [/tests/integration/todo-flow.test.tsx](/tests/integration/todo-flow.test.tsx), [/tests/integration/filtering.test.tsx](/tests/integration/filtering.test.tsx), [/tests/integration/theme.test.tsx](/tests/integration/theme.test.tsx)
- E2E(작성 예시): [/tests/e2e/todo-core.spec.ts](/tests/e2e/todo-core.spec.ts), [/tests/e2e/filtering.spec.ts](/tests/e2e/filtering.spec.ts), [/tests/e2e/theme-responsive.spec.ts](/tests/e2e/theme-responsive.spec.ts) (버그 수정 포함)

**실행/검증 명령**
- 개발 서버: `npm run dev`
- 정적 검증: `npm run lint` / `npx tsc --noEmit`
- 테스트: `npm run test` (또는 `npx vitest run`)
- E2E: `npm run test:e2e`

**핵심 확인 포인트(스펙 ↔ 구현 매핑)**
- CreateTodo/Toggle/Delete 흐름이 정상 동작하고 새로고침 후 복원되는가
- 필터(all/active/completed) 전환 및 저장/복원이 동작하는가
- 테마(system/user) 전환, 저장/복원, 시스템 변경 동기화가 동작하는가
- 로컬 스토리지 실패 시 경고 표시 후 세션 내 상태로 동작하는가
- 정렬 규칙(미완료 우선)이 일관되게 적용되는가

> 참고: 테스트 실행 시 출력이 부족하게 보이면 `npx vitest run --reporter verbose`로 실행 로그를 더 자세히 확인할 수 있습니다.

---

## ✅ 체크리스트

- [ ] 헌법과 템플릿 동기화 파일을 확인했다
- [ ] 스펙 문서가 사용자 스토리/요구사항/성공 기준을 포함한다
- [ ] Clarify 결정이 스펙에 반영되었다
- [ ] Plan 산출물(리서치/데이터 모델/계약/퀵스타트)을 확인했다
- [ ] Tasks 문서가 사용자 스토리별 작업과 테스트를 포함한다
- [ ] Analyze 결과에서 누락/모호성/불일치를 확인하고 필요 시 보정했다
- [ ] Implement 산출물(코드/테스트)이 Tasks와 일치하는지 확인했다
- [ ] lint/typecheck/test 실행으로 품질을 검증했다

## 🧪 실습 확인 과제

다음 항목을 직접 열어 확인하세요.
- [/specs/001-todo-webapp/spec.md](/specs/001-todo-webapp/spec.md)
- [/specs/001-todo-webapp/plan.md](/specs/001-todo-webapp/plan.md)
- [/specs/001-todo-webapp/tasks.md](/specs/001-todo-webapp/tasks.md)
- Analyze 결과에서 지적된 항목 1개 이상을 반영했는지 확인
- [/app/page.tsx](/app/page.tsx)에서 스펙의 핵심 사용자 플로우가 조립되어 있는지 확인
- [/lib/hooks/useTodos.ts](/lib/hooks/useTodos.ts), [/lib/hooks/usePreferences.ts](/lib/hooks/usePreferences.ts)에서 저장/복원 계약이 구현되어 있는지 확인
- `npm run lint`와 `npx tsc --noEmit`가 실패 없이 동작하는지 확인

## 💡 팁

- 스펙 수정이 발생하면 clarify → plan → tasks 순서로 다시 동기화하세요.
- 작업을 시작하기 전, 반드시 헌법(품질/테스트/UX/성능) 체크리스트를 통과시키세요.
- 작은 MVP(US1)부터 완성한 뒤 단계적으로 확장하세요.


→ **다음 장**: [4. 신규 기능을 위한 완전한 Spec Driven Development 사이클](/sdd/speckit/lab04)
