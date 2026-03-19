---
title: 3. 할일 편집 기능 추가 - AI 코딩 워크플로우 복습
layout: default
grand_parent: SDD
parent: 3files
nav_order: 3
permalink: /sdd/3files/lab03
# nav_exclude: true
# search_exclude: true
--- 
# Lab 03: 할일 편집 기능 추가 - AI 코딩 워크플로우 복습

## 📚 학습 목표

이 실습을 통해 다음을 학습합니다:

1. **Lab 02 워크플로우 복습**: PRD → TASKS → 구현 프로세스를 실제 기능 추가에 적용
2. **기존 앱 확장 경험**: 새로운 기능 개발이 아닌 기존 코드베이스 수정 시나리오 학습
3. **DoD 기준 준수**: Definition of Done을 통한 품질 관리 실습
4. **1일 집중 개발**: 8시간 내에 PRD 작성부터 배포까지 전체 사이클 완료

## 🎯 주요 개념과 용어 정리

### 1. 기존 기능 확장 vs 새 기능 개발

**새 기능 개발 (Lab 02):**
- 빈 캔버스에서 시작
- 새로운 컴포넌트 생성
- 독립적인 기능 구현

**기존 기능 확장 (Lab 03):**
- 기존 코드베이스 분석 필요
- 기존 컴포넌트 수정
- 하위 호환성 고려
- 기존 테스트 영향도 파악

### 2. Props 확장 패턴

기존 컴포넌트에 새로운 기능을 추가할 때 Props를 확장하는 방법입니다.

**Before:**
```typescript
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

**After:**
```typescript
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
  onEdit: (id: string, title: string, description?: string) => void; // 추가
}
```

### 3. 상태 관리 확장

기존 컴포넌트에 새로운 상태를 추가하는 패턴입니다.

```typescript
// 편집 모드 상태
const [isEditing, setIsEditing] = useState(false);
const [editTitle, setEditTitle] = useState(todo.title);
const [editDescription, setEditDescription] = useState(todo.description || '');
```

### 4. updatedAt 필드

할일이 마지막으로 수정된 시간을 추적하는 필드입니다.

**타입 정의 수정:**
```typescript
interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string | Date;
  updatedAt?: string | Date; // 추가 (선택적 필드로 기존 데이터 호환)
}
```

**사용 예시:**
```typescript
// 할일 편집 시
const handleEditTodo = (id: string, title: string, description?: string) => {
  setTodos((prev) =>
    prev.map((todo) =>
      todo.id === id 
        ? { ...todo, title, description, updatedAt: new Date() } 
        : todo
    )
  );
};
```

### 5. 테스트 보강 전략

기존 기능에 새 기능을 추가할 때의 테스트 전략입니다.

**계층별 테스트:**
1. **유닛 테스트**: 편집 모드 UI, 저장/취소 로직
2. **통합 테스트**: 편집 후 필터링 동작 확인
3. **E2E 테스트**: 전체 편집 플로우 (클릭 → 수정 → 저장 → 로컬 스토리지)
4. **회귀 테스트**: 기존 기능이 여전히 작동하는지 확인

## 📁 할일 편집 기능 구현 범위

### 추가/수정할 파일

```
project-root/
├── .github/
│   └── prompts/                        # 기존 프롬프트 파일 재사용
├── docs/
│   ├── PRD-todo-edit.md                # 🆕 새로 생성
│   └── TASKS-todo-edit.md              # 🆕 새로 생성
├── lib/
│   └── types.ts                        # 🔧 수정 (updatedAt 추가)
├── components/
│   ├── todo-item.tsx                   # 🔧 대폭 수정 (편집 UI 추가)
│   └── todo-list.tsx                   # 🔧 소폭 수정 (onEdit prop 전달)
├── app/
│   └── page.tsx                        # 🔧 소폭 수정 (handleEditTodo 추가)
├── tests/
│   ├── unit/
│   │   └── todo-item.test.tsx          # 🔧 테스트 추가
│   └── e2e/
│       └── todo-edit.spec.ts           # 🆕 새 파일 생성 (선택)
├── CHANGELOG.md                        # 🔧 업데이트 (v1.1.0 추가)
└── README.md                           # 🔧 업데이트 (기능 목록)
```

**범례:**
- 🆕 새로 생성
- 🔧 수정
- 📖 참고

### 기능 요구사항 요약

1. **inline 편집 모드**
   - 할일 항목을 클릭하거나 편집 버튼을 눌러 편집 모드 진입
   - 편집 모드에서 제목과 설명을 input/textarea로 변경
   
2. **저장/취소 기능**
   - 저장 버튼: 변경사항 적용 및 `updatedAt` 업데이트
   - 취소 버튼: 변경사항 무시 및 편집 모드 종료
   
3. **키보드 단축키**
   - `Enter`: 저장 (제목 input에서)
   - `Esc`: 취소
   
4. **updatedAt 필드**
   - 할일 편집 시 자동으로 현재 시간 기록
   - UI에 "수정됨: X분 전" 형태로 표시 (선택)

## 🛠️ 실습 준비

### 사전 요구사항

✅ **필수:**
- Lab 02 완료 (TODO 앱 v1.0.0 구현 완료)
- `docs/PRD-todo-list.md` 파일 존재
- `docs/TASKS-todo-list.md` 파일 존재
- `.github/prompts/` 디렉토리의 프롬프트 파일들 존재
- 기존 TODO 앱이 정상 동작함

✅ **확인사항:**
- GitHub Copilot 활성화 상태
- Node.js 20 이상
- 개발 서버 실행 가능 (`npm run dev`)
- 테스트 실행 가능 (`npm test`, `npm run test:e2e`)

### 환경 확인 (15분)

```bash
# 1. 개발 서버 실행 확인
npm run dev
# → http://localhost:3000 에서 TODO 앱 동작 확인

# 2. 테스트 실행 확인
npm test
# → 기존 유닛 테스트 모두 통과 확인

npm run test:e2e
# → 기존 E2E 테스트 모두 통과 확인

# 3. 기존 기능 동작 확인
# - 할일 추가/삭제/완료 동작
# - 필터링 (전체/진행중/완료) 동작
# - 로컬 스토리지 저장/불러오기 동작
# - 다크모드 토글 동작
```

### 기존 코드 분석 (15분)

편집 기능을 추가하기 전에 관련 파일들을 미리 파악하세요.

1. **타입 정의 확인**
   - `lib/types.ts` - `Todo` 인터페이스 구조 파악
   
2. **TodoItem 컴포넌트 분석**
   - `components/todo-item.tsx` - 현재 UI 구조와 Props 파악
   
3. **메인 페이지 로직 파악**
   - `app/page.tsx` - 할일 상태 관리 방식 (`useState`, `useLocalStorage`)
   
4. **기존 테스트 확인**
   - `tests/unit/todo-item.test.tsx` - 어떤 테스트가 있는지 파악

## 📖 단계별 실습

### ⏱️ 실습 타임라인 (총 8시간)

| 시간 | 단계 | 소요시간 | 누적시간 |
|------|------|----------|----------|
| 09:00-09:30 | Step 0: 환경 확인 및 코드 분석 | 30분 | 0.5h |
| 09:30-10:00 | Step 1: PRD 작성 | 30분 | 1h |
| 10:00-10:30 | Step 2-3: TASKS 생성 및 검토 | 30분 | 1.5h |
| 10:30-12:00 | Step 4: EPIC-08 실행 (1/2) | 1.5시간 | 3h |
| 12:00-13:00 | 점심 휴식 | - | - |
| 13:00-15:30 | Step 4: EPIC-08 실행 (2/2) | 2.5시간 | 5.5h |
| 15:30-16:30 | Step 5: 통합 테스트 및 검증 | 1시간 | 6.5h |
| 16:30-17:00 | Step 6: 문서화 및 최종 검증 | 30분 | 7h |
| 17:00-17:30 | Step 7: 회고 및 정리 | 30분 | 7.5h |

**여유 시간: 30분** (예상치 못한 이슈 대응용)

---

### Step 0: 환경 확인 및 코드 분석 (30분)

**목표:** 실습 환경을 확인하고 수정할 코드를 미리 파악합니다.

**작업:**
1. 위의 "환경 확인" 섹션 수행
2. "기존 코드 분석" 섹션 수행
3. 메모 작성: 어떤 파일을 어떻게 수정해야 할지 간단히 정리

**체크:**
- [ ] 개발 서버 정상 실행
- [ ] 기존 유닛 테스트 모두 통과
- [ ] 기존 E2E 테스트 모두 통과
- [ ] `lib/types.ts`의 `Todo` 인터페이스 파악 완료
- [ ] `components/todo-item.tsx` 구조 파악 완료
- [ ] `app/page.tsx` 상태 관리 방식 파악 완료

---

### Step 1: PRD 작성 (30분)

**목표:** 할일 편집 기능의 요구사항을 명확히 정의합니다.

**실습:**

1. **GitHub Copilot Chat 열기**
   - `Ctrl+Shift+I` (Windows) 또는 `Cmd+Shift+I` (Mac)

2. **PRD 생성 프롬프트 사용**

   ```
   /create-prd
   
   기존 TODO 앱(Lab 02에서 완성)에 다음 기능을 추가하려고 합니다:
   
   ## 할일 편집 기능
   
   **주요 기능:**
   1. inline 편집 모드: 할일 항목을 클릭하거나 편집 버튼을 눌러 편집 모드 진입
   2. 제목과 설명 수정 가능
   3. 저장 버튼: 변경사항 적용 및 updatedAt 업데이트
   4. 취소 버튼: 변경사항 무시 및 편집 모드 종료
   5. 키보드 단축키: Enter(저장), Esc(취소)
   6. updatedAt 필드 추가: 할일 편집 시 자동으로 현재 시간 기록
   
   **기술 고려사항:**
   - 기존 컴포넌트 수정 (components/todo-item.tsx)
   - lib/types.ts에 updatedAt 필드 추가 (선택적 필드로 기존 데이터 호환)
   - 기존 테스트 영향도 최소화
   - 로컬 스토리지와 자동 동기화
   
   **목표:**
   - 1일(8시간) 내 완성
   - 기존 기능에 영향 없음 (회귀 테스트 통과)
   - 테스트 커버리지 유지 (85% 이상)
   ```

3. **명확화 질문 답변**

   AI가 질문을 하면 프로젝트 맥락에 맞게 답변하세요. 예시:
   
   ```
   Q1: 편집 중에 다른 할일을 클릭하면 어떻게 되나요?
   A: 현재 편집을 자동 저장하지 않고 편집 모드만 종료 (취소 동작)
   
   Q2: updatedAt을 UI에 표시하나요?
   A: 선택사항. 시간이 남으면 "수정됨: X분 전" 형태로 표시
   
   Q3: 편집 중 검증은?
   A: 제목은 필수 (1-100자), 설명은 선택 (최대 500자)
   ```

4. **생성된 PRD 확인 및 검토**

   `docs/PRD-todo-edit.md` 파일을 열어서 다음이 포함되었는지 확인:
   
   - ✅ 목표 및 배경 (기존 앱 확장)
   - ✅ 사용자 스토리 (편집 플로우)
   - ✅ 기능 요구사항 (inline 편집, 저장/취소, updatedAt)
   - ✅ 비목표 (범위 밖: 편집 히스토리, 실행 취소/다시 실행 등)
   - ✅ 기술 고려사항 (기존 코드 수정, 타입 확장)
   - ✅ 성공 지표 (회귀 테스트 통과, 새 테스트 작성)

**체크:**
- [ ] `docs/PRD-todo-edit.md` 파일 생성 완료
- [ ] PRD에 모든 필수 섹션 포함
- [ ] 모호한 요구사항 없음
- [ ] 비목표(범위 밖) 명확히 정의

---

### Step 2: TASKS 생성 - Epic 생성 (15분)

**목표:** PRD를 Epic 단위로 분해합니다.

**실습:**

1. **TASKS 생성 프롬프트 사용**

   ```
   /generate-tasks
   
   PRD 파일: docs/PRD-todo-edit.md
   ```

2. **Epic 확인**

   AI가 Epic을 생성합니다. 예상되는 Epic 구조:
   
   ```markdown
   ### EPIC-08: 할일 편집 기능
   
   할일 항목의 제목과 설명을 수정할 수 있는 inline 편집 기능을 추가합니다.
   updatedAt 필드를 도입하여 마지막 수정 시간을 추적합니다.
   ```
   
   **참고:** 이번 실습은 단일 Epic으로 구성됩니다 (Lab 02보다 작은 범위).

3. **Epic 승인**

   AI가 "상세 Task를 생성할 준비가 되었나요?"라고 물어보면:
   
   ```
   Go
   ```

**체크:**
- [ ] Epic 제목과 설명이 명확함
- [ ] Epic 범위가 적절함 (8시간 내 완료 가능)

---

### Step 3: TASKS 생성 - Task 분해 (15분)

**목표:** Epic을 실행 가능한 Task로 상세 분해합니다.

**실습:**

1. **Task 자동 생성**

   Step 2에서 "Go"를 입력하면 AI가 자동으로 Task를 생성합니다.

2. **예상되는 Task 구조**

   ```markdown
   ## EPIC-08: 할일 편집 기능
   
   - [ ] TASK-08-01: Todo 타입에 updatedAt 필드 추가
     - lib/types.ts 수정
     - updatedAt을 선택적 필드로 정의 (기존 데이터 호환)
     - TypeScript 컴파일 에러 없음 확인
     - **예상 결과**: Todo 타입에 updatedAt?: string | Date 추가
     - **예상 소요시간**: 15분
   
   - [ ] TASK-08-02: TodoItem 컴포넌트에 편집 모드 UI 추가
     - components/todo-item.tsx 수정
     - isEditing 상태 추가
     - 편집 버튼 추가 (연필 아이콘)
     - 편집 모드일 때 input/textarea로 전환
     - 저장/취소 버튼 UI
     - **예상 결과**: 편집 버튼 클릭 시 입력 필드로 전환
     - **예상 소요시간**: 1.5시간
   
   - [ ] TASK-08-03: TodoItem 편집 저장/취소 로직 구현
     - 저장: onEdit prop 호출 및 편집 모드 종료
     - 취소: 변경사항 무시 및 편집 모드 종료
     - Enter 키로 저장 (제목 input)
     - Esc 키로 취소
     - 빈 제목 검증
     - **예상 결과**: 저장/취소 버튼 및 단축키 동작
     - **예상 소요시간**: 1시간
   
   - [ ] TASK-08-04: TodoItem Props에 onEdit 추가
     - TodoItemProps 인터페이스에 onEdit 추가
     - TodoList에서 onEdit prop 전달
     - **예상 결과**: 타입 에러 없음
     - **예상 소요시간**: 15분
   
   - [ ] TASK-08-05: 메인 페이지에 handleEditTodo 구현
     - app/page.tsx에 handleEditTodo 함수 추가
     - todos 상태 업데이트 (제목, 설명, updatedAt)
     - TodoList에 onEdit prop 전달
     - **예상 결과**: 편집 저장 시 로컬 스토리지 자동 업데이트
     - **예상 소요시간**: 30분
   
   - [ ] TASK-08-06: TodoItem 유닛 테스트 추가
     - tests/unit/todo-item.test.tsx 수정
     - 편집 버튼 클릭 테스트
     - 편집 모드에서 입력 필드 표시 테스트
     - 저장 버튼 클릭 시 onEdit 호출 테스트
     - 취소 버튼 클릭 시 원래 내용 유지 테스트
     - Esc/Enter 키 테스트
     - **예상 결과**: 새 테스트 모두 통과, 기존 테스트도 통과
     - **예상 소요시간**: 1.5시간
   
   - [ ] TASK-08-07: 회귀 테스트 실행 및 수정
     - npm test 실행 → 모든 유닛 테스트 통과 확인
     - npm run test:e2e 실행 → 모든 E2E 테스트 통과 확인
     - 실패한 테스트 수정 (필요시)
     - **예상 결과**: 테스트 커버리지 85% 이상 유지
     - **예상 소요시간**: 1시간
   
   - [ ] TASK-08-08: 문서 업데이트
     - CHANGELOG.md에 v1.1.0 섹션 추가
     - README.md 기능 목록 업데이트
     - PRD-todo-list.md 비목표에서 "할일 편집" 제거 (이제 구현됨)
     - **예상 결과**: 모든 문서가 최신 상태 반영
     - **예상 소요시간**: 30분
   ```

3. **Task 검토**

   생성된 Task를 검토하고 다음을 확인:
   - ✅ 각 Task가 명확하고 실행 가능한가?
   - ✅ Task 순서가 의존성을 고려했는가? (타입 정의 → UI → 로직 → 테스트)
   - ✅ 예상 소요시간이 합리적인가? (총 6-7시간 예상)

4. **TASKS 파일 확인**

   `docs/TASKS-todo-edit.md` 파일이 생성되었는지 확인합니다.

**체크:**
- [ ] `docs/TASKS-todo-edit.md` 파일 생성 완료
- [ ] Task가 Epic 아래 계층 구조로 정리됨
- [ ] 각 Task에 예상 소요시간과 결과 명시
- [ ] Task 순서가 논리적임

---

### Step 4: Epic 실행 (5시간)

**목표:** EPIC-08의 모든 Task를 순차적으로 실행하고 DoD 기준에 따라 검증합니다.

**실습 방법 (2가지 옵션):**

#### 옵션 A: Epic 배치 실행 (권장)

```
/run-epic EPIC-08
```

AI가 모든 Task를 자동으로 순차 실행합니다. 각 Task 완료 후 다음 Task로 자동 진행됩니다.

#### 옵션 B: Task 개별 실행

하나씩 실행하며 학습하고 싶다면:

```
/execute-task TASK-08-01
```

각 Task 완료 후 다음 Task를 실행합니다.

---

**각 Task 실행 후 DoD 체크:**

모든 Task는 다음 5가지 기준을 충족해야 완료로 간주됩니다.

#### 1. ✅ 코드 작성 완료

- [ ] 요구사항에 명시된 모든 기능 구현
- [ ] TypeScript 타입 에러 없음
- [ ] ESLint 경고 없음

**확인 방법:**
```bash
# TypeScript 컴파일 확인
npx tsc --noEmit

# ESLint 확인
npm run lint
```

#### 2. ✅ 테스트 작성 및 통과

- [ ] 해당 기능의 유닛 테스트 작성 (TASK-08-06)
- [ ] 모든 테스트 통과

**확인 방법:**
```bash
# 유닛 테스트 실행
npm test

# 특정 파일만 테스트
npm test todo-item.test.tsx
```

#### 3. ✅ 문서화

- [ ] 복잡한 로직에 주석 추가
- [ ] README 또는 CHANGELOG 업데이트 (TASK-08-08)

#### 4. ✅ 코드 리뷰

- [ ] 불필요한 `console.log` 제거
- [ ] 코드 포맷팅 확인
- [ ] 네이밍 규칙 준수 (camelCase, PascalCase)

**확인 방법:**
```bash
# 코드 포맷팅
npm run format
```

#### 5. ✅ 통합 확인

- [ ] 개발 서버에서 실제 동작 확인
- [ ] 기존 기능에 영향 없음 확인 (회귀 테스트)

**확인 방법:**
```bash
# 개발 서버 실행
npm run dev

# 브라우저에서 http://localhost:3000 열기
# 1. 할일 추가
# 2. 편집 버튼 클릭
# 3. 제목/설명 수정
# 4. 저장 버튼 클릭 → 변경사항 반영 확인
# 5. 취소 버튼 테스트
# 6. Enter/Esc 키 테스트
# 7. 기존 기능 (추가/삭제/완료/필터링) 정상 동작 확인
```

---

**Task 완료 후:**

각 Task가 DoD를 충족하면 `docs/TASKS-todo-edit.md` 파일에서 해당 Task를 `[x]`로 체크합니다.

```markdown
- [x] TASK-08-01: Todo 타입에 updatedAt 필드 추가 ✅
- [x] TASK-08-02: TodoItem 컴포넌트에 편집 모드 UI 추가 ✅
- [ ] TASK-08-03: TodoItem 편집 저장/취소 로직 구현 ⬅️ 현재 작업중
```

---

**중간 체크포인트 (점심 전 12:00):**

- [ ] TASK-08-01 완료 (타입 정의)
- [ ] TASK-08-02 완료 (편집 UI)
- [ ] TASK-08-03 진행중 또는 완료 (로직 구현)

**오후 체크포인트 (15:30):**

- [ ] TASK-08-01 ~ 08-05 완료 (모든 구현 완료)
- [ ] TASK-08-06 진행중 (테스트 작성)

---

### Step 5: 통합 테스트 및 검증 (1시간)

**목표:** 모든 기능이 통합된 상태에서 정상 동작하는지 검증합니다.

**체크리스트:**

#### 1. 유닛 테스트 실행

```bash
npm test
```

- [ ] 모든 유닛 테스트 통과 (기존 + 새로 추가된 테스트)
- [ ] 테스트 커버리지 85% 이상 유지

#### 2. E2E 테스트 실행

```bash
npm run test:e2e
```

- [ ] 모든 E2E 테스트 통과
- [ ] 기존 E2E 시나리오 정상 동작 (회귀 테스트)

#### 3. 수동 통합 테스트

개발 서버에서 다음 시나리오를 직접 테스트:

**시나리오 1: 기본 편집 플로우**
- [ ] 할일 추가 → 편집 버튼 클릭 → 제목 수정 → 저장 → 변경사항 반영
- [ ] 할일 추가 → 편집 버튼 클릭 → 설명 수정 → 저장 → 변경사항 반영
- [ ] 할일 추가 → 편집 버튼 클릭 → 제목+설명 수정 → 저장 → 변경사항 반영

**시나리오 2: 취소 동작**
- [ ] 편집 중 취소 버튼 클릭 → 원래 내용 유지
- [ ] 편집 중 Esc 키 → 원래 내용 유지

**시나리오 3: 검증**
- [ ] 빈 제목으로 저장 시도 → 에러 메시지 표시 또는 저장 방지
- [ ] 제목 100자 초과 → 입력 제한
- [ ] 설명 500자 초과 → 입력 제한

**시나리오 4: 로컬 스토리지**
- [ ] 할일 편집 → 페이지 새로고침 → 변경사항 유지
- [ ] 개발자 도구에서 `localStorage` 확인 → `updatedAt` 필드 존재

**시나리오 5: 다른 기능과의 통합**
- [ ] 편집 후 완료 체크 → 필터링(완료) → 편집된 내용 표시
- [ ] 편집 후 다크모드 토글 → 스타일 정상
- [ ] 여러 할일 중 하나만 편집 → 다른 할일 영향 없음

**시나리오 6: 엣지 케이스**
- [ ] 편집 중 다른 할일 클릭 → 현재 편집 취소 (자동)
- [ ] 완료된 할일도 편집 가능 → 정상 동작

#### 4. 크로스 브라우저 테스트 (선택)

시간이 남으면:
- [ ] Chrome에서 테스트
- [ ] Firefox에서 테스트
- [ ] Safari 또는 Edge에서 테스트

---

### Step 6: 문서화 및 최종 검증 (30분)

**목표:** 모든 문서를 업데이트하고 최종 확인합니다.

#### 1. CHANGELOG 업데이트

`CHANGELOG.md` 파일에 v1.1.0 섹션 추가:

```markdown
## [1.1.0] - 2026-01-16

### Added
- 할일 편집 기능 (inline 편집 모드)
- 편집 저장/취소 버튼 및 키보드 단축키 (Enter/Esc)
- `updatedAt` 필드 추가 (할일 마지막 수정 시간 추적)

### Changed
- `components/todo-item.tsx` - 편집 모드 UI 및 로직 추가
- `lib/types.ts` - Todo 타입에 `updatedAt` 필드 추가

### Fixed
- (있다면 수정된 버그 기록)
```

#### 2. README 업데이트

`README.md`의 기능 목록에 편집 기능 추가:

```markdown
## 주요 기능

- ✅ 할일 추가 (제목, 설명)
- ✅ 할일 편집 (제목, 설명 수정) 🆕
- ✅ 할일 완료 체크/해제
- ✅ 할일 삭제
- ✅ 필터링 (전체, 진행중, 완료)
- ✅ 로컬 스토리지 자동 저장
- ✅ 다크모드 지원
- ✅ 반응형 디자인
```

#### 3. PRD-todo-list.md 업데이트 (선택)

원본 PRD의 비목표 섹션에서 "할일 편집" 제거:

```markdown
## 비목표 (범위 밖)

~~- ❌ 할일 편집 기능~~ ✅ v1.1.0에서 구현됨
- ❌ 할일 우선순위
- ❌ 할일 마감일
...
```

#### 4. 최종 체크리스트

- [ ] `docs/TASKS-todo-edit.md`의 모든 Task `[x]` 체크 완료
- [ ] `CHANGELOG.md` 업데이트 완료
- [ ] `README.md` 업데이트 완료
- [ ] Git 커밋 메시지 작성 (의미있는 메시지)

```bash
git add .
git commit -m "feat: 할일 편집 기능 추가 (v1.1.0)

- inline 편집 모드 구현
- 저장/취소 버튼 및 단축키 (Enter/Esc)
- updatedAt 필드 추가로 마지막 수정 시간 추적
- 유닛 테스트 및 회귀 테스트 통과
- EPIC-08 완료"
```

---

### Step 7: 회고 및 정리 (30분)

**목표:** 실습을 통해 배운 점을 정리하고 다음 단계를 계획합니다.

**회고 질문:**

1. **워크플로우 이해도**
   - PRD → TASKS → 구현 프로세스가 명확해졌나요?
   - 어느 단계가 가장 유용했나요?
   - 어느 단계가 가장 어려웠나요?

2. **기존 코드 수정 경험**
   - 새로운 기능 개발과 기존 기능 확장의 차이를 느꼈나요?
   - Props 확장 패턴을 이해했나요?
   - 하위 호환성 고려 (updatedAt을 선택적 필드로)의 중요성을 알았나요?

3. **DoD 적용**
   - 5가지 DoD 기준이 품질 관리에 도움이 되었나요?
   - 어떤 DoD 항목이 가장 중요하다고 느꼈나요?

4. **GitHub Copilot 활용**
   - Custom Instructions가 유용했나요?
   - Prompt Files를 잘 활용했나요?
   - AI가 생성한 코드를 얼마나 수정했나요?

5. **테스트**
   - 유닛 테스트를 먼저 작성하는 것이 도움이 되었나요?
   - E2E 테스트의 가치를 느꼈나요?
   - 회귀 테스트의 중요성을 이해했나요?

**개선 아이디어:**

다음 프로젝트에서 시도해볼 것들:
- [ ] 더 작은 Task 단위로 분해 (1-2시간 이하)
- [ ] TDD (Test-Driven Development) 방식 시도
- [ ] E2E 테스트 먼저 작성 (기능 명세로 활용)
- [ ] Pair Programming with AI (더 많은 질문과 리뷰)

**다음 단계:**

Lab 03을 완료했다면 다음을 시도해보세요:

1. **추가 기능 구현**
   - 할일 우선순위 (상/중/하)
   - 할일 마감일 및 알림
   - 할일 카테고리/태그
   - 할일 검색 기능

2. **고급 주제**
   - 상태 관리 라이브러리 도입 (Zustand, Jotai)
   - 서버 컴포넌트 활용 (Next.js App Router)
   - API 통합 (백엔드 연동)
   - 인증/권한 관리

3. **배포**
   - Vercel에 배포
   - Lighthouse 최적화
   - PWA 전환

---

## ✅ 전체 체크리스트

### 준비 단계
- [ ] Lab 02 완료 확인
- [ ] 개발 서버 실행 확인
- [ ] 기존 테스트 모두 통과
- [ ] 기존 코드 분석 완료

### PRD 작성 (30분)
- [ ] `/create-prd` 프롬프트 사용
- [ ] 명확화 질문 답변
- [ ] `docs/PRD-todo-edit.md` 생성
- [ ] PRD 검토 및 승인

### TASKS 생성 (30분)
- [ ] `/generate-tasks` 프롬프트 사용
- [ ] Epic 검토 및 승인
- [ ] Task 상세 분해
- [ ] `docs/TASKS-todo-edit.md` 생성

### Epic 실행 (5시간)
- [ ] TASK-08-01: updatedAt 필드 추가
- [ ] TASK-08-02: 편집 UI 추가
- [ ] TASK-08-03: 저장/취소 로직
- [ ] TASK-08-04: Props 확장
- [ ] TASK-08-05: handleEditTodo 구현
- [ ] TASK-08-06: 유닛 테스트
- [ ] TASK-08-07: 회귀 테스트
- [ ] TASK-08-08: 문서 업데이트

### 검증 (1시간)
- [ ] 모든 유닛 테스트 통과
- [ ] 모든 E2E 테스트 통과
- [ ] 수동 통합 테스트 완료
- [ ] 테스트 커버리지 85% 이상

### 문서화 (30분)
- [ ] CHANGELOG.md 업데이트
- [ ] README.md 업데이트
- [ ] Git 커밋

### 회고 (30분)
- [ ] 회고 질문에 답변
- [ ] 개선 아이디어 기록
- [ ] 다음 단계 계획

---

## 🔍 문제 해결 가이드

### 문제 1: Task 순서 의존성 오류

**증상:**
- TASK-08-04를 먼저 실행했더니 타입 에러 발생
- "Property 'onEdit' is missing"

**원인:**
- Task 순서를 무시하고 실행함
- 타입 정의(TASK-08-01)와 Props 확장(TASK-08-04)을 먼저 완료해야 함

**해결책:**
1. TASKS 문서의 Task 순서대로 실행
2. 의존성 확인: 타입 정의 → UI → 로직 → 테스트
3. `/run-epic`을 사용하면 자동으로 순서대로 실행됨

---

### 문제 2: 기존 테스트 실패 (회귀)

**증상:**
- 새 기능 추가 후 기존 유닛 테스트 실패
- "TypeError: onEdit is not a function"

**원인:**
- Props를 확장했지만 기존 테스트 mock을 업데이트하지 않음

**해결책:**

`tests/unit/todo-item.test.tsx` 수정:

```typescript
// Before
const mockTodo: Todo = { ... };
const mockOnToggle = vi.fn();
const mockOnDelete = vi.fn();

render(
  <TodoItem 
    todo={mockTodo} 
    onToggle={mockOnToggle} 
    onDelete={mockOnDelete} 
  />
);

// After
const mockTodo: Todo = { ... };
const mockOnToggle = vi.fn();
const mockOnDelete = vi.fn();
const mockOnEdit = vi.fn(); // 추가

render(
  <TodoItem 
    todo={mockTodo} 
    onToggle={mockOnToggle} 
    onDelete={mockOnDelete}
    onEdit={mockOnEdit} // 추가
  />
);
```

---

### 문제 3: 로컬 스토리지 데이터 호환성

**증상:**
- 기존 할일에 `updatedAt`이 없어서 UI에서 "undefined" 표시

**원인:**
- 기존에 저장된 할일 데이터는 `updatedAt` 필드가 없음
- 타입을 선택적(`updatedAt?`)으로 정의했지만 UI에서 처리하지 않음

**해결책:**

1. **타입 정의 확인** (`lib/types.ts`):
```typescript
interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string | Date;
  updatedAt?: string | Date; // 선택적 필드
}
```

2. **UI에서 조건부 렌더링** (선택적으로 구현):
```typescript
{todo.updatedAt && (
  <p className="text-xs text-gray-500">
    수정됨: {new Date(todo.updatedAt).toLocaleString()}
  </p>
)}
```

3. **마이그레이션 함수** (필요시):
```typescript
// app/page.tsx
useEffect(() => {
  // 기존 데이터에 updatedAt 추가
  setTodos((prev) =>
    prev.map((todo) => ({
      ...todo,
      updatedAt: todo.updatedAt || todo.createdAt, // 없으면 createdAt 사용
    }))
  );
}, []);
```

---

### 문제 4: Props Drilling

**증상:**
- `onEdit`을 TodoList → TodoItem으로 전달하는 것이 번거로움
- 컴포넌트가 많아지면 Props 전달이 복잡해짐

**원인:**
- React의 Props drilling 문제
- 상태 관리가 최상위(page.tsx)에 있음

**해결책:**

**지금 (간단한 앱):**
- Props drilling이 1-2 레벨이므로 괜찮음
- 명시적이고 이해하기 쉬움

**나중 (복잡한 앱):**
- Context API 사용
- 상태 관리 라이브러리 (Zustand, Jotai) 도입

**예시 (Context API):**{% raw %}
```typescript 
// contexts/TodoContext.tsx

const TodoContext = createContext<{
  todos: Todo[];
  addTodo: (...) => void;
  editTodo: (...) => void;
  deleteTodo: (...) => void;
}>(null!);

// app/page.tsx
<TodoContext.Provider value={{ todos, addTodo, editTodo, deleteTodo }}>
  <TodoList />
</TodoContext.Provider>

// components/todo-item.tsx
const { editTodo } = useContext(TodoContext); 
```
{% endraw %}
---

### 문제 5: 편집 중 다른 할일 클릭

**증상:**
- 편집 중에 다른 할일을 클릭하면 어떻게 되어야 하나?
- 변경사항이 저장되지 않고 손실됨

**원인:**
- 각 TodoItem이 독립적인 `isEditing` 상태를 가짐
- 동시에 여러 항목 편집 가능 (의도하지 않음)

**해결책 (선택):**

**Option A: 현재 상태 유지**
- 각 항목 독립적으로 편집 가능
- 간단하고 구현 쉬움

**Option B: 한 번에 하나만 편집**
- 상태를 page.tsx로 이동
- `editingId` 상태로 현재 편집 중인 항목 추적

```js
// app/page.tsx
const [editingId, setEditingId] = useState<string | null>(null);

// TodoItem
<TodoItem
  todo={todo}
  isEditing={editingId === todo.id}
  onStartEdit={() => setEditingId(todo.id)}
  onCancelEdit={() => setEditingId(null)}
  ...
/>
```

**권장:** 시간이 없으면 Option A, 시간이 남으면 Option B

---

## 📚 추가 학습 자료

### 관련 문서
- [Lab 01: 테스트 환경 설정](../lab-01/README.md)
- [Lab 02: AI 코딩 워크플로우](../lab-02/README.md)
- [PRD 템플릿](.github/prompts/create-prd.prompt.md)
- [TASKS 템플릿](.github/prompts/generate-tasks.prompt.md)

### 공식 문서
- [Next.js 공식 문서](https://nextjs.org/docs)
- [React 공식 문서](https://react.dev)
- [TypeScript 공식 문서](https://www.typescriptlang.org/docs)
- [Vitest 공식 문서](https://vitest.dev)
- [Playwright 공식 문서](https://playwright.dev)

### 추천 읽기
- [Definition of Done (DoD) 가이드](https://www.scrum.org/resources/blog/walking-through-definition-done)
- [PRD 작성 베스트 프랙티스](https://www.atlassian.com/agile/product-management/requirements)
- [Epic과 User Story 차이](https://www.atlassian.com/agile/project-management/epics-stories-themes)

---

## 💡 팁과 모범 사례

### 1. 작은 단위로 커밋

각 Task 완료 후 Git 커밋하세요:

```bash
git add .
git commit -m "feat(TASK-08-01): Todo 타입에 updatedAt 필드 추가"
```

**장점:**
- 작업 단위 추적 가능
- 문제 발생 시 롤백 용이
- 코드 리뷰 시 변경사항 파악 쉬움

### 2. 테스트 먼저 실행

코드 수정 전에 기존 테스트를 실행하세요:

```bash
npm test
```

**장점:**
- 기존 기능이 정상 작동하는지 확인
- 회귀 방지
- 자신감 있게 코드 수정 가능

### 3. AI에게 구체적으로 질문

모호한 질문보다 구체적인 질문이 좋습니다:

❌ **나쁜 예:**
```
편집 기능을 추가해줘
```

✅ **좋은 예:**
```
components/todo-item.tsx에 편집 모드를 추가하려고 합니다.
다음 요구사항을 만족하도록 구현해주세요:

1. useState로 isEditing 상태 관리
2. 편집 버튼 클릭 시 isEditing을 true로 변경
3. isEditing이 true일 때 제목과 설명을 input/textarea로 표시
4. 저장/취소 버튼 추가
5. 기존 스타일(Tailwind CSS) 유지

Props에 onEdit을 추가하고 타입도 정의해주세요.
```

### 4. DoD를 체크리스트로 활용

각 Task 시작 시 DoD를 복사하여 체크리스트로 사용하세요:

```markdown
## TASK-08-02 DoD

- [ ] 1. 코드 작성 완료
  - [ ] isEditing 상태 추가
  - [ ] 편집 버튼 UI
  - [ ] 조건부 렌더링 (보기 모드 vs 편집 모드)
  - [ ] TypeScript 에러 없음
  - [ ] ESLint 통과
  
- [ ] 2. 테스트 작성 및 통과
  - (TASK-08-06에서 수행)
  
- [ ] 3. 문서화
  - [ ] 복잡한 로직에 주석 추가
  
- [ ] 4. 코드 리뷰
  - [ ] console.log 제거
  - [ ] 네이밍 규칙 확인
  
- [ ] 5. 통합 확인
  - [ ] 개발 서버에서 편집 버튼 클릭 동작 확인
```

### 5. 에러 메시지를 AI에게 공유

문제 발생 시 전체 에러 메시지를 AI에게 공유하세요:

```
다음 에러가 발생했습니다:

```
TypeError: Cannot read properties of undefined (reading 'title')
  at TodoItem (components/todo-item.tsx:15:23)
```

코드:
[문제가 되는 코드 블록 붙여넣기]

어떻게 수정해야 할까요?
```

### 6. 점진적 개선

완벽을 추구하지 말고 점진적으로 개선하세요:

**1차 구현 (필수 기능만):**
- 편집 버튼
- 저장/취소 버튼
- 기본 동작

**2차 개선 (시간이 남으면):**
- 키보드 단축키 (Enter/Esc)
- 입력 검증 (빈 제목 방지)
- 에러 메시지

**3차 고도화 (추가 도전):**
- updatedAt UI 표시
- 편집 히스토리
- 애니메이션

---

## 🎉 완료!

축하합니다! Lab 03을 완료하셨습니다.

**배운 내용:**
- ✅ PRD → TASKS → 구현 워크플로우 복습
- ✅ 기존 코드베이스 확장 경험
- ✅ Props 확장 및 상태 관리 패턴
- ✅ DoD 기반 품질 관리
- ✅ 회귀 테스트의 중요성

**다음 단계:**
1. 추가 기능 구현 (우선순위, 마감일, 검색 등)
2. 상태 관리 라이브러리 도입
3. 백엔드 API 연동
4. 배포 및 최적화

**피드백:**
이 Lab에서 어려웠던 점이나 개선 아이디어가 있다면 공유해주세요!

---

**추가 기능 - PRD 생성 프롬프트(검색기능)**

   ```
   /create-prd
   
   기존 TODO 앱(Lab 03에서 완성)에 다음 기능을 추가하려고 합니다:
   
   ## 검색 기능
   
   **주요 기능:**
   1. inline 편집 모드: 검색 키워드를 입력하고  검색 버튼을 눌러 검색
   2. 검색된 내용은 현재 전체 내용을 보여주는 리스트에 검색된 내용만 출력되도록 함
   3. 검색 키워드 일부 일치하거나 전부 일치하는 모든 내용을 출력
   3. 검색 버튼: 검색 진행
   4. 키보드 단축키: Enter(검색), Esc(취소)

   
   **기술 고려사항:**
   - 기존 컴포넌트 수정 (components/todo-item.tsx)
   - 기존 테스트 영향도 최소화
   - 로컬 스토리지와 자동 동기화
   
   **목표:**
   - 1시간 내 완성
   - 기존 기능에 영향 없음 (회귀 테스트 통과)
   - 테스트 커버리지 유지 (85% 이상)
   ```

---

**Happy Coding! 🚀**
