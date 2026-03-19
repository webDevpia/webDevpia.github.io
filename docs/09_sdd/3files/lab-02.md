---
title: 2. AI 코딩 워크플로우 - PRD, TASKS, Epic 기반 개발
layout: default
grand_parent: SDD
parent: 3files
nav_order: 2
permalink: /sdd/3files/lab02
# nav_exclude: true
# search_exclude: true
--- 
# Lab 02: AI 코딩 워크플로우 - PRD, TASKS, Epic 기반 개발

## 📚 학습 목표

이 실습을 통해 다음을 학습합니다:

1. **AI 협업 워크플로우 이해**: PRD → TASKS → 구현으로 이어지는 체계적인 개발 프로세스
2. **GitHub Copilot 커스터마이제이션**: Custom Instructions와 Prompt Files 활용
3. **Epic 기반 작업 관리**: 대규모 기능을 Epic과 Task로 분해하여 관리
4. **Definition of Done (DoD) 적용**: 품질 기준을 명확히 하여 일관된 코드 품질 유지
5. **반복 가능한 개발 프로세스**: 구조화된 방법론으로 예측 가능한 개발

## 🎯 주요 개념과 용어 정리

### 1. PRD (Product Requirements Document)
**제품 요구사항 문서**

기능의 목표, 사용자 스토리, 요구사항을 명확히 정의하는 문서입니다. PRD는 개발 전에 "무엇을" 만들지를 명확히 하여 개발자와 이해관계자 간의 의사소통을 돕습니다.

**주요 구성 요소:**
- 기능 개요 및 목표
- 사용자 스토리
- 기능 요구사항
- 비목표 (범위 밖 항목)
- 성공 지표

### 2. TASKS (작업 목록)
**상세 작업 목록 문서**

PRD를 기반으로 생성된 실행 가능한 작업 목록입니다. Epic과 Task로 구조화되어 있으며, 체크박스로 진행 상황을 추적합니다.

### 3. Epic
**상위 목표 단위**

여러 Task를 묶는 큰 단위의 기능 그룹입니다. 예를 들어, "사용자 인증 시스템", "할일 관리 핵심 기능" 등이 Epic이 될 수 있습니다.

**Epic ID 형식:** `EPIC-01`, `EPIC-02` 등

### 4. Task
**개별 작업 항목**

Epic 내의 구체적이고 실행 가능한 작업입니다. 각 Task는 명확한 목표와 완료 기준을 가집니다.

**Task ID 형식:** `TASK-01-01`, `TASK-02-03` 등 (Epic 번호 - Task 번호)

### 5. DoD (Definition of Done)
**작업 완료 기준**

Task를 완료로 표시하기 전에 충족해야 할 조건들입니다. DoD를 명확히 하면 일관된 코드 품질을 유지할 수 있습니다.

**표준 DoD 체크리스트:**
1. ✅ 코드 작성 완료 (타입 에러 없음, ESLint 통과)
2. ✅ 테스트 작성 및 통과 (유닛 테스트, E2E 테스트)
3. ✅ 문서화 (주석, README 업데이트)
4. ✅ 코드 리뷰 (자기 검토, 디버깅 코드 제거)
5. ✅ 통합 확인 (개발 서버에서 동작 확인)

### 6. Custom Instructions
**사용자 정의 지침**

GitHub Copilot에게 프로젝트의 코딩 스타일, 규칙, 워크플로우를 알려주는 설정 파일입니다. `.github/copilot-instructions.md` 파일에 작성합니다.

### 7. Prompt Files
**프롬프트 파일**

재사용 가능한 프롬프트를 파일로 저장하여 일관된 방식으로 AI와 협업할 수 있게 합니다. `.github/prompts/` 디렉토리에 `.prompt.md` 확장자로 저장합니다.

**주요 프롬프트 파일:**
- `create-prd.prompt.md` - PRD 생성
- `generate-tasks.prompt.md` - TASKS 생성
- `execute-task.prompt.md` - 단일 Task 실행
- `run-epic.prompt.md` - Epic 배치 실행

### 8. Agent Mode
**에이전트 모드**

AI가 자율적으로 여러 단계를 실행하는 모드입니다. GitHub Copilot에서는 `@workspace` 멘션을 통해 프로젝트 전체 컨텍스트를 활용할 수 있습니다.

### 9. CHANGELOG
**변경 이력 문서**

프로젝트의 주요 변경사항을 시간 순서대로 기록하는 문서입니다. 버전 관리와 팀 커뮤니케이션에 유용합니다.

## 📁 프로젝트 구조

이 실습에서 사용하는 디렉토리 구조는 다음과 같습니다:

```
project-root/
├── .github/
│   ├── copilot-instructions.md        # GitHub Copilot 사용자 정의 지침
│   └── prompts/
│       ├── create-prd.prompt.md       # PRD 생성 프롬프트
│       ├── execute-task.prompt.md     # 단일 Task 실행 프롬프트
│       ├── generate-tasks.prompt.md   # TASKS 생성 프롬프트
│       └── run-epic.prompt.md         # Epic 배치 실행 프롬프트
├── app/                               # Next.js 앱 디렉토리
│   ├── globals.css                    # 전역 스타일 (Tailwind CSS)
│   ├── layout.tsx                     # 레이아웃
│   └── page.tsx                       # 홈 페이지
├── components/                        # 재사용 가능한 컴포넌트
├── docs/
│   ├── PRD-[기능명].md                # 기능별 PRD 문서
│   └── TASKS-[기능명].md              # 기능별 작업 목록
├── labs/                              # 실습 폴더
│   ├── lab-01/                        
│   └── lab-02/
│       └── README.md                  # 이 파일
├── lib/                               # 유틸리티 함수, hooks
│   ├── hooks/                         # Custom React hooks
│   ├── utils/                         # 유틸리티 함수
│   └── types.ts                       # TypeScript 타입 정의
└── tests/                             # 테스트 파일
    ├── setup.ts                       # 테스트 설정
    ├── unit/                          # 유닛 테스트
    └── e2e/                           # E2E 테스트

```

## 🛠️ 실습 준비

### 사전 요구사항

- Lab 01 완료 (Vitest, Playwright 테스트 환경 구축)
- Node.js 20 이상
- VS Code with GitHub Copilot
- Git 설치

### 환경 확인

```bash
# 프로젝트 루트 디렉토리에서 실행
npm install
npm run dev
```

개발 서버가 http://localhost:3000 에서 실행되면 준비가 완료된 것입니다.

## 📖 단계별 실습

### Step 1: AI 코딩 워크플로우 개요 이해

**목표:** PRD → TASKS → 구현 워크플로우의 전체 흐름을 이해합니다.

**워크플로우:**

```mermaid
graph LR
    A[기능 아이디어] --> B[PRD 작성]
    B --> C[TASKS 생성]
    C --> D[Epic 단위 실행]
    D --> E[Task 실행 및 검증]
    E --> F[완료 체크]
    F --> G[다음 Task/Epic]
```

1. **기능 아이디어**: 만들고 싶은 기능을 간단히 설명
2. **PRD 작성**: `/create-prd` 프롬프트로 상세한 요구사항 문서 작성
3. **TASKS 생성**: `/generate-tasks` 프롬프트로 실행 가능한 작업 목록 생성
4. **Epic 단위 실행**: `/run-epic` 프롬프트로 여러 Task를 배치 실행
5. **Task 실행 및 검증**: 각 Task마다 DoD 기준에 따라 검증
6. **완료 체크**: TASKS 문서에 진행 상황 기록
7. **다음 Task/Epic**: 모든 작업이 완료될 때까지 반복

### Step 2: GitHub Copilot 설정 확인

**목표:** Custom Instructions와 Prompt Files가 제대로 설정되었는지 확인합니다.

1. **Custom Instructions 확인**

   `.github/copilot-instructions.md` 파일을 열어서 다음 내용이 포함되어 있는지 확인:
   - 코딩 스타일 규칙
   - 네이밍 규칙
   - 작업 프로세스 (PRD → TASKS → 구현)
   - Definition of Done (DoD)
   - 주요 용어 정의

2. **Prompt Files 확인**

   `.github/prompts/` 디렉토리에 다음 파일들이 있는지 확인:
   - `create-prd.prompt.md` ✅
   - `generate-tasks.prompt.md` ✅
   - `execute-task.prompt.md` ✅
   - `run-epic.prompt.md` ✅

3. **VS Code에서 Prompt Files 사용법**

   GitHub Copilot Chat에서 `/` 명령어를 입력하면 사용 가능한 프롬프트가 표시됩니다:
   
   ```
   /create-prd
   /generate-tasks
   /execute-task
   /run-epic
   ```

### Step 3: Todo List 앱 PRD 작성

**목표:** 실제 기능에 대한 PRD를 작성하여 요구사항을 명확히 합니다.

**실습 과제:** 간단한 Todo List 앱의 PRD를 작성해봅시다.

1. **GitHub Copilot Chat 열기**
   - VS Code에서 `Ctrl+Shift+I` (Windows) 또는 `Cmd+Shift+I` (Mac)

2. **PRD 생성 프롬프트 사용**

   ```
   /create-prd
   
   다음 기능을 가진 할일 관리 앱의 PRD를 작성해줘:
   
   1. 할일 추가 (제목, 설명)
   2. 할일 완료 체크/해제
   3. 할일 삭제
   4. 필터링 (전체, 진행중, 완료)
   5. 로컬 스토리지 자동 저장
   6. 다크모드 지원
   7. 반응형 디자인 (모바일, 데스크톱)
   
   대상 사용자는 개인 사용자이고, MVP로 2일 내 완성을 목표로 합니다.
   ```

3. **명확화 질문에 답변**

   AI가 3-5개의 명확화 질문을 할 것입니다. 예시:
   
   ```
   1. 이 기능의 주요 목표는 무엇인가요?
      A. 사용자 온보딩 경험 개선
      B. 사용자 유지율 증가
      C. 지원 부담 감소
      D. 개인 생산성 향상 ✅
   
   2. 우선순위가 높은 기능은?
      A. 할일 추가/삭제/완료
      B. 필터링
      C. 다크모드
      D. 로컬 스토리지
   
   응답: 1D, 2A
   ```

4. **생성된 PRD 확인**

   AI가 `docs/PRD-todo-list.md` 파일을 생성합니다. 다음 섹션이 포함되어 있는지 확인:
   
   - ✅ 소개/개요
   - ✅ 목표
   - ✅ 사용자 스토리
   - ✅ 기능 요구사항
   - ✅ 비목표 (범위 밖)
   - ✅ 디자인 고려사항
   - ✅ 기술 고려사항
   - ✅ 성공 지표
   - ✅ 미해결 질문

5. **PRD 검토 및 수정**

   생성된 PRD를 검토하고 필요한 경우 수정합니다. 모호한 부분이 있다면 AI에게 명확화를 요청하세요.

**✨ 팁:** PRD는 개발 전에 모든 이해관계자가 동의하는 "계약서"와 같습니다. 시간을 들여 명확히 작성하면 나중에 시간을 절약할 수 있습니다.

### Step 4: TASKS 생성 (Epic과 Task 분해)

**목표:** PRD를 실행 가능한 작업 목록(Epic과 Task)으로 분해합니다.

1. **TASKS 생성 프롬프트 사용**

   ```
   /generate-tasks
   
   PRD 파일: docs/PRD-todo-list.md
   ```

2. **Epic 생성 단계**

   AI가 먼저 고수준 Epic을 생성합니다. 예시:
   
   ```markdown
   ### EPIC-00: 프로젝트 설정
   ### EPIC-01: 할일 관리 핵심 기능
   ### EPIC-02: 필터링 및 정렬
   ### EPIC-03: 로컬 스토리지 통합
   ### EPIC-04: 다크모드 지원
   ### EPIC-05: 반응형 디자인
   ### EPIC-06: 테스트 및 검증
   ### EPIC-07: 문서화 및 정리
   ```
   
   AI가 "상세 Task를 생성할 준비가 되었나요? 계속하려면 'Go'로 응답하세요."라고 물어봅니다.

3. **Epic 검토 및 확인**

   생성된 Epic을 검토합니다. Epic의 순서와 범위가 적절한지 확인하세요. 문제가 없다면:
   
   ```
   Go
   ```

4. **상세 Task 생성**

   AI가 각 Epic을 더 작은 Task로 분해합니다. 예시:
   
   ```markdown
   ### EPIC-01: 할일 관리 핵심 기능
   
   - [ ] TASK-01-01: 할일 데이터 타입 정의
   - [ ] TASK-01-02: 할일 추가 UI 컴포넌트 생성
   - [ ] TASK-01-03: 할일 목록 표시 컴포넌트 생성
   - [ ] TASK-01-04: 할일 완료/미완료 토글 기능 구현
   - [ ] TASK-01-05: 할일 삭제 기능 구현
   - [ ] TASK-01-06: 할일 관리 상태 관리 (useState)
   ```

5. **생성된 TASKS 확인**

   `docs/TASKS-todo-list.md` 파일이 생성됩니다. 다음 내용이 포함되어 있는지 확인:
   
   - ✅ 관련 파일 목록
   - ✅ 작업 완료 지침
   - ✅ Definition of Done (DoD)
   - ✅ Epic 및 Tasks (체크박스 포함)

**✨ 팁:** Epic은 대략 3-7개 정도가 적당합니다. 각 Epic은 5-10개의 Task로 구성되는 것이 이상적입니다.

### Step 5: 단일 Task 실행

**목표:** 개별 Task를 실행하고 DoD 기준에 따라 검증하는 방법을 배웁니다.

1. **첫 번째 Task 실행**

   ```
   /execute-task TASK-00-01
   
   TASKS 파일: docs/TASKS-todo-list.md
   ```

2. **AI의 Task 실행 과정 관찰**

   AI가 다음 단계를 수행합니다:
   
   a. **Task 내용 확인**
      ```
      🚀 시작: TASK-00-01 - 기능 브랜치 생성
      ```
   
   b. **구현**
      - 새 브랜치 생성: `git checkout -b feature/todo-list`
   
   c. **DoD 체크리스트 수행**
      - ✅ 코드 작성 완료 (해당 없음 - 브랜치 생성만)
      - ✅ 테스트 작성 및 통과 (해당 없음)
      - ✅ 문서화 (해당 없음)
      - ✅ 코드 리뷰 (해당 없음)
      - ✅ 통합 확인 (브랜치 생성 확인)
   
   d. **Task 체크 표시**
      - `docs/TASKS-todo-list.md`에서 `- [x] TASK-00-01` 로 변경
   
   e. **결과 보고**
      ```
      ✅ TASK-00-01 완료!
      
      다음 Task: TASK-00-02
      ```

3. **다음 Task 실행**

   ```
   /execute-task TASK-00-02
   ```

4. **코드 검토**

   AI가 생성한 코드를 검토합니다:
   - TypeScript 타입이 올바른가?
   - ESLint 규칙을 준수하는가?
   - 테스트가 작성되었는가?

5. **개발 서버에서 확인**

   ```bash
   npm run dev
   ```
   
   브라우저에서 http://localhost:3000 을 열어 변경사항을 확인합니다.

**✨ 팁:** 각 Task를 완료한 후 반드시 개발 서버에서 동작을 확인하세요. 조기에 문제를 발견할수록 수정이 쉽습니다.

### Step 6: Epic 배치 실행 (EPIC-01)

**목표:** 여러 Task를 묶어서 Epic 단위로 효율적으로 실행하는 방법을 배웁니다.

1. **Epic 실행**

   ```
   /run-epic EPIC-01
   
   TASKS 파일: docs/TASKS-todo-list.md
   ```

2. **진행 상황 관찰**

   AI가 Epic의 모든 Task를 순차적으로 실행합니다:
   
   ```
   📊 Epic 진행 상황: EPIC-01
   
   ✅ TASK-01-01: 할일 데이터 타입 정의
   ✅ TASK-01-02: 할일 추가 UI 컴포넌트 생성
   🔄 TASK-01-03: 할일 목록 표시 컴포넌트 생성 (진행 중...)
   ⏳ TASK-01-04: 할일 완료/미완료 토글 기능 구현 (대기 중)
   ⏳ TASK-01-05: 할일 삭제 기능 구현 (대기 중)
   ⏳ TASK-01-06: 할일 관리 상태 관리 (대기 중)
   
   진행률: 40% (2/6 완료)
   ```

3. **각 Task의 DoD 검증**

   Epic 실행 중에도 각 Task마다 DoD가 검증됩니다:
   - ✅ 코드 작성 완료
   - ✅ 테스트 작성 및 통과
   - ✅ 문서화
   - ✅ 코드 리뷰
   - ✅ 통합 확인

4. **Epic 완료 보고서 확인**

   모든 Task가 완료되면 Epic 요약 보고서가 생성됩니다:
   
   ```
   ✅ EPIC-01 완료!
   
   📊 Epic 요약:
   제목: 할일 관리 핵심 기능
   완료된 Tasks: 6/6 (100%)
   
   📝 작업 내용:
   - 할일 데이터 타입 정의
   - 할일 추가 UI 컴포넌트 생성
   - 할일 목록 표시 컴포넌트 생성
   - 할일 완료/미완료 토글 기능 구현
   - 할일 삭제 기능 구현
   - 할일 관리 상태 관리
   
   📄 변경된 파일:
   ✨ 새 파일:
   - lib/types.ts
   - components/todo-form.tsx
   - components/todo-form.test.tsx
   - components/todo-list.tsx
   - components/todo-list.test.tsx
   - components/todo-item.tsx
   - components/todo-item.test.tsx
   - app/todos/page.tsx
   
   🧪 테스트 결과:
   - 유닛 테스트: 12/12 통과 ✅
   - E2E 테스트: 3/3 통과 ✅
   
   다음 Epic:
   - EPIC-02: 필터링 및 정렬 기능
   ```

5. **Epic 통합 테스트**

   Epic이 완료되면 전체 기능이 잘 작동하는지 확인합니다:
   
   ```bash
   # 유닛 테스트 실행
   npm test
   
   # E2E 테스트 실행
   npm run test:e2e
   
   # 개발 서버에서 확인
   npm run dev
   ```

**✨ 팁:** Epic 실행은 여러 Task를 한 번에 처리하므로 효율적이지만, 중간에 에러가 발생하면 중단됩니다. 작은 Epic부터 시작하여 점진적으로 진행하는 것이 좋습니다.

### Step 7: DoD 검증 및 품질 확인

**목표:** Definition of Done (DoD) 기준을 이해하고 적용하는 방법을 배웁니다.

1. **DoD 체크리스트 확인**

   각 Task 완료 시 다음 5가지를 반드시 확인합니다:

   **1. 코드 작성 완료 ✅**
   ```bash
   # TypeScript 타입 에러 확인
   npx tsc --noEmit
   
   # ESLint 실행
   npm run lint
   ```

   **2. 테스트 작성 및 통과 ✅**
   ```bash
   # 유닛 테스트 실행
   npm test
   
   # 테스트 커버리지 확인
   npm run test:coverage
   
   # E2E 테스트 실행
   npm run test:e2e
   ```

   **3. 문서화 ✅**
   - 복잡한 로직에 주석 추가 확인
   - JSDoc 형식으로 함수 문서화 확인
   - README 업데이트 필요 시 업데이트

   **4. 코드 리뷰 ✅**
   - 불필요한 `console.log` 제거
   - 사용하지 않는 import 제거
   - 코드 포맷팅 확인 (Prettier)

   **5. 통합 확인 ✅**
   ```bash
   # 개발 서버 실행
   npm run dev
   ```
   - 브라우저에서 기능 동작 확인
   - 기존 기능에 영향 없는지 확인

2. **DoD 미충족 시 처리**

   DoD 기준을 충족하지 못한 경우:
   
   a. **Task를 체크하지 않음**
      - TASKS 파일에서 해당 Task는 `- [ ]` 상태 유지
   
   b. **문제 해결**
      - 테스트 추가 작성
      - 타입 에러 수정
      - 문서화 추가
   
   c. **재검증**
      - 다시 DoD 체크리스트 수행
   
   d. **완료 표시**
      - 모든 기준 충족 시 `- [x]`로 변경

3. **품질 지표 모니터링**

   ```bash
   # 테스트 커버리지 확인
   npm run test:coverage
   
   # 브라우저에서 커버리지 리포트 확인
   # coverage/index.html 파일 열기
   ```
   
   목표 커버리지: 80% 이상

**✨ 팁:** DoD는 협상 가능하지 않습니다. 모든 기준을 충족해야만 Task를 완료로 표시하세요. 이것이 일관된 코드 품질을 유지하는 핵심입니다.

### Step 8: 나머지 Epic 완료

**목표:** 학습한 워크플로우를 적용하여 Todo List 앱을 완성합니다.

1. **EPIC-02: 필터링 및 정렬**

   ```
   /run-epic EPIC-02
   ```
   
   - 전체/진행중/완료 필터링 구현
   - 필터 상태 관리
   - UI 토글 버튼 추가

2. **EPIC-03: 로컬 스토리지 통합**

   ```
   /run-epic EPIC-03
   ```
   
   - localStorage에 데이터 저장
   - 페이지 로드 시 데이터 복원
   - Custom hook (useTodoStorage) 구현

3. **EPIC-04: 다크모드 지원**

   ```
   /run-epic EPIC-04
   ```
   
   - 다크모드 토글 버튼
   - 테마 상태 관리
   - Tailwind CSS 다크모드 클래스 적용

4. **EPIC-05: 반응형 디자인**

   ```
   /run-epic EPIC-05
   ```
   
   - 모바일 레이아웃 조정
   - 태블릿 레이아웃 조정
   - 데스크톱 레이아웃 최적화

5. **EPIC-06: 테스트 및 검증**

   ```
   /run-epic EPIC-06
   ```
   
   - 통합 테스트 작성
   - E2E 테스트 작성
   - 엣지 케이스 테스트

6. **EPIC-07: 문서화 및 정리**

   ```
   /run-epic EPIC-07
   ```
   
   - README 업데이트
   - 코드 주석 추가
   - 최종 코드 리뷰

**✨ 팁:** 한 Epic을 완전히 완료한 후에 다음 Epic으로 넘어가세요. 여러 Epic을 동시에 진행하면 관리가 어려워집니다.

### Step 9: 최종 검증 및 배포 준비

**목표:** 전체 앱이 제대로 작동하는지 최종 검증합니다.

1. **전체 테스트 실행**

   ```bash
   # 유닛 테스트
   npm test
   
   # E2E 테스트
   npm run test:e2e
   
   # 빌드 테스트
   npm run build
   ```

2. **수동 테스트**

   브라우저에서 다음 시나리오를 테스트:
   
   - [ ] 할일 추가
   - [ ] 할일 완료 체크
   - [ ] 할일 삭제
   - [ ] 필터링 (전체/진행중/완료)
   - [ ] 다크모드 토글
   - [ ] 페이지 새로고침 후 데이터 유지
   - [ ] 모바일 화면에서 동작 확인
   - [ ] 데스크톱 화면에서 동작 확인

3. **TASKS 완료 확인**

   `docs/TASKS-todo-list.md` 파일을 열어서:
   - 모든 Epic이 `[x]`로 표시되었는지 확인
   - 모든 Task가 `[x]`로 표시되었는지 확인

4. **CHANGELOG 작성**

   `CHANGELOG.md` 파일을 생성하여 주요 변경사항 기록:
   
   ```markdown
   # Changelog
   
   ## [1.0.0] - 2026-01-16
   
   ### Added
   - 할일 추가, 완료, 삭제 기능
   - 전체/진행중/완료 필터링
   - 로컬 스토리지 자동 저장
   - 다크모드 지원
   - 반응형 디자인 (모바일, 데스크톱)
   
   ### Tests
   - 유닛 테스트 12개 작성
   - E2E 테스트 5개 작성
   - 테스트 커버리지 85%
   ```

5. **Git 커밋**

   ```bash
   git add .
   git commit -m "feat: Todo List 앱 MVP 완성
   
   - 할일 관리 핵심 기능 구현
   - 필터링 및 로컬 스토리지 통합
   - 다크모드 및 반응형 디자인
   - 테스트 커버리지 85%
   "
   ```

**✨ 팁:** CHANGELOG는 프로젝트의 변경 이력을 추적하는 중요한 문서입니다. 주요 릴리스마다 업데이트하세요.

## 🎓 학습 정리

### 배운 내용

1. **구조화된 AI 협업 워크플로우**
   - PRD로 요구사항 명확화
   - TASKS로 실행 계획 수립
   - Epic과 Task로 체계적 구현

2. **GitHub Copilot 커스터마이제이션**
   - Custom Instructions로 프로젝트 규칙 설정
   - Prompt Files로 재사용 가능한 워크플로우 구축

3. **Epic 기반 작업 관리**
   - 큰 기능을 Epic으로 분해
   - Task 단위로 점진적 구현
   - 진행 상황 체계적 추적

4. **Definition of Done (DoD)**
   - 명확한 완료 기준 설정
   - 일관된 코드 품질 유지
   - 테스트 및 문서화 강제

5. **반복 가능한 개발 프로세스**
   - 예측 가능한 개발 일정
   - 품질 보장
   - 효율적인 협업

### 주요 명령어 정리

| 명령어 | 설명 | 사용 예시 |
|--------|------|-----------|
| `/create-prd` | PRD 생성 | 기능 설명 제공 |
| `/generate-tasks` | TASKS 생성 | PRD 파일 참조 |
| `/execute-task` | 단일 Task 실행 | TASK-01-01 실행 |
| `/run-epic` | Epic 배치 실행 | EPIC-01 전체 실행 |

### DoD 체크리스트 (암기용)

각 Task 완료 시 반드시 확인:

1. ✅ **코드 작성 완료** - 타입 에러 0, ESLint 통과
2. ✅ **테스트 작성 및 통과** - 유닛/E2E 테스트
3. ✅ **문서화** - 주석, README
4. ✅ **코드 리뷰** - 디버깅 코드 제거
5. ✅ **통합 확인** - 개발 서버에서 동작 확인

## 🚀 다음 단계

### 추가 실습 과제

1. **기능 확장**
   - 할일 편집 기능 추가
   - 할일 우선순위 설정
   - 할일 마감일 추가
   - 할일 카테고리/태그

2. **PRD → TASKS → 구현 반복**
   - 위 기능 중 하나를 선택
   - PRD 작성
   - TASKS 생성
   - Epic 단위로 구현

3. **자신만의 프로젝트 시작**
   - 만들고 싶은 기능 선택
   - 이 워크플로우 적용
   - 학습한 내용 실전 활용

### 추가 학습 자료

- [Ryan Carson's 3-File System](https://github.com/snarktank/ai-dev-tasks)
- [GitHub Copilot Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [GitHub Copilot Prompt Files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- [Next.js 공식 문서](https://nextjs.org/docs)
- [Tailwind CSS 공식 문서](https://tailwindcss.com/docs)

## 💡 팁과 모범 사례

### PRD 작성 팁

1. **구체적으로 작성**: 모호한 표현 피하기
2. **사용자 관점**: 사용자 스토리 중심으로 작성
3. **범위 명확화**: 비목표(Non-Goals) 명시
4. **측정 가능한 목표**: 정량적 지표 설정

### TASKS 생성 팁

1. **적절한 크기**: Task는 1-4시간 내 완료 가능하도록
2. **순서 고려**: 의존성을 고려한 Task 순서
3. **명확한 설명**: Task 제목만 봐도 이해 가능하도록
4. **테스트 포함**: 각 Task에 테스트 계획 포함

### Epic 실행 팁

1. **작은 Epic부터**: 처음에는 작은 Epic으로 시작
2. **중간 점검**: Epic 중간에 통합 테스트
3. **문제 조기 발견**: 각 Task 완료 시 즉시 확인
4. **문서화 지속**: Epic 진행 중에도 문서 업데이트

### DoD 적용 팁

1. **타협 금지**: 모든 기준 반드시 충족
2. **자동화**: ESLint, 테스트는 자동화
3. **리뷰 습관**: 자기 리뷰를 습관화
4. **지속적 개선**: DoD 기준을 지속적으로 개선

## 📝 실습 체크리스트

완료한 항목에 체크하세요:

- [ ] Step 1: AI 코딩 워크플로우 개요 이해
- [ ] Step 2: GitHub Copilot 설정 확인
- [ ] Step 3: Todo List 앱 PRD 작성
- [ ] Step 4: TASKS 생성 (Epic과 Task 분해)
- [ ] Step 5: 단일 Task 실행 (TASK-01-01)
- [ ] Step 6: Epic 배치 실행 (EPIC-01)
- [ ] Step 7: DoD 검증 및 품질 확인
- [ ] Step 8: 나머지 Epic 완료
- [ ] Step 9: 최종 검증 및 배포 준비

## 🤝 도움이 필요하신가요?

문제가 발생하거나 질문이 있으면:

1. **TASKS 파일 확인**: 현재 진행 상황과 다음 단계 확인
2. **PRD 참조**: 기능 요구사항 재확인
3. **DoD 체크리스트**: 누락된 항목 확인
4. **GitHub Copilot에게 질문**: 구체적으로 문제 설명

---

**Happy Coding! 🎉**

이 워크플로우를 마스터하면 AI와 함께 더 빠르고 품질 높은 코드를 작성할 수 있습니다!
