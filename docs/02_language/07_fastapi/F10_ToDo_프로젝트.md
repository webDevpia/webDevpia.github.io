---
title: 10. 미니 프로젝트 — ToDo API
layout: default
grand_parent: Language
parent: FastAPI
nav_order: 10
permalink: /language/fastapi/todo-project
---

{% raw %}

# 10장. 미니 프로젝트 — ToDo API (인메모리)
{: .no_toc }

> "이번 장은 Part 2의 캡스톤입니다."
> APIRouter로 구조를 나누고, Depends()로 중복을 제거하고, 커스텀 에러로 우아하게 실패합니다.
> 처음부터 끝까지 직접 만들어보는 것이 가장 좋은 복습입니다.

## 학습 목표
{: .no_toc }

- Part 2에서 배운 APIRouter, Depends, 에러 처리를 하나의 프로젝트로 통합합니다
- 실제 프로젝트 파일 구조를 손으로 만들어보며 각 파일의 역할을 이해합니다
- ToDo 항목의 CRUD와 상태 필터링 기능을 완성합니다
- Swagger UI로 전체 API를 테스트하는 흐름을 경험합니다

<a id="toc"></a>

## 진행 순서

1. [프로젝트 소개](#1) — 무엇을 만드는가
2. [프로젝트 구조 설계](#2) — 디렉터리 구조
3. [Step 1: 스키마 정의](#3) — schemas.py
4. [Step 2: 커스텀 예외](#4) — exceptions.py
5. [Step 3: 의존성 정의](#5) — dependencies.py
6. [Step 4: CRUD 엔드포인트](#6) — routers/todos.py
7. [Step 5: 메인 앱 연결](#7) — main.py
8. [완성 코드 전체](#8) — 파일별 전체 코드
9. [Swagger에서 전체 테스트](#9) — 시나리오 따라하기
10. [정리 + 브릿지](#10)

---

<a id="1"></a>

## 1️⃣ 프로젝트 소개 [↑](#toc)

이번 장에서 만들 것은 **인메모리 ToDo API**입니다.

### 기능 목록

| 기능 | 메서드 | 경로 | 설명 |
|------|--------|------|------|
| ToDo 생성 | `POST` | `/todos` | 새 할 일 추가 |
| ToDo 목록 조회 | `GET` | `/todos` | 전체 또는 상태별 필터 |
| ToDo 단건 조회 | `GET` | `/todos/{todo_id}` | 특정 할 일 조회 |
| ToDo 수정 | `PUT` | `/todos/{todo_id}` | 제목/내용/상태 수정 |
| ToDo 삭제 | `DELETE` | `/todos/{todo_id}` | 특정 할 일 삭제 |

### ToDo 상태 정의

```
pending  → 대기 중 (기본값)
done     → 완료
archived → 보관됨
```

### 완성 후 Swagger UI 미리보기

```
┌─────────────────────────────────────┐
│ Todos                             ▼ │
├─────────────────────────────────────┤
│ POST   /todos           ToDo 생성   │
│ GET    /todos           ToDo 목록   │
│ GET    /todos/{id}      ToDo 조회   │
│ PUT    /todos/{id}      ToDo 수정   │
│ DELETE /todos/{id}      ToDo 삭제   │
├─────────────────────────────────────┤
│ Health                            ▼ │
├─────────────────────────────────────┤
│ GET    /                상태 확인   │
└─────────────────────────────────────┘
```

---

<a id="2"></a>

## 2️⃣ 프로젝트 구조 설계 [↑](#toc)

```
todo-api/
├── app/
│   ├── __init__.py
│   ├── main.py            ← 앱 생성 + 라우터 등록
│   ├── schemas.py         ← Pydantic 모델
│   ├── exceptions.py      ← 커스텀 예외 클래스
│   ├── dependencies.py    ← Depends() 함수들
│   └── routers/
│       ├── __init__.py
│       └── todos.py       ← CRUD 엔드포인트
└── requirements.txt
```

먼저 디렉터리를 만들겠습니다.

```bash
mkdir -p todo-api/app/routers
touch todo-api/app/__init__.py
touch todo-api/app/routers/__init__.py
touch todo-api/app/main.py
touch todo-api/app/schemas.py
touch todo-api/app/exceptions.py
touch todo-api/app/dependencies.py
touch todo-api/app/routers/todos.py
touch todo-api/requirements.txt
```

`requirements.txt`:

```
fastapi[standard]>=0.135.0
```

설치:

```bash
cd todo-api
pip install -r requirements.txt
```

---

<a id="3"></a>

## 3️⃣ Step 1: 스키마 정의 [↑](#toc)

`app/schemas.py` 파일을 작성합니다.

```python
# app/schemas.py

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# ── 상태 타입 ──────────────────────────────────────────
TodoStatus = Literal["pending", "done", "archived"]


# ── 요청 스키마 ────────────────────────────────────────
class TodoCreate(BaseModel):
    """ToDo 생성 요청 스키마"""
    title: str = Field(..., min_length=1, max_length=200, description="할 일 제목")
    content: Optional[str] = Field(None, max_length=1000, description="상세 내용")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "FastAPI 08장 복습",
                    "content": "Depends() 패턴 다시 정리하기",
                }
            ]
        }
    }


class TodoUpdate(BaseModel):
    """ToDo 수정 요청 스키마 (모든 필드 선택적)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, max_length=1000)
    status: Optional[TodoStatus] = None


# ── 응답 스키마 ────────────────────────────────────────
class TodoPublic(BaseModel):
    """ToDo 응답 스키마"""
    id: int
    title: str
    content: Optional[str] = None
    status: TodoStatus
    created_at: datetime


# ── 에러 응답 스키마 ───────────────────────────────────
class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    code: str
    message: str
```

> `Literal["pending", "done", "archived"]`는 세 값 중 하나만 허용하는 타입입니다.
> Pydantic이 자동으로 검증합니다. "완료됨"이나 "DONE" 같은 값을 보내면 422 에러가 반환됩니다.
> Swagger UI에서 드롭다운으로 선택할 수 있도록 표시됩니다.

---

<a id="4"></a>

## 4️⃣ Step 2: 커스텀 예외 [↑](#toc)

`app/exceptions.py` 파일을 작성합니다.

```python
# app/exceptions.py

class TodoNotFoundError(Exception):
    """ToDo 항목을 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, todo_id: int):
        self.todo_id = todo_id
        super().__init__(f"ToDo {todo_id} not found")


class TodoAlreadyDoneError(Exception):
    """이미 완료된 ToDo를 다시 완료 처리하려 할 때 발생하는 예외"""
    def __init__(self, todo_id: int):
        self.todo_id = todo_id
        super().__init__(f"ToDo {todo_id} is already done")
```

---

<a id="5"></a>

## 5️⃣ Step 3: 의존성 정의 [↑](#toc)

`app/dependencies.py` 파일을 작성합니다.

인메모리 저장소와 ID 카운터를 모듈 수준 변수로 관리하고, 의존성 함수로 접근합니다.

```python
# app/dependencies.py

from typing import Annotated
from fastapi import Depends
from app.schemas import TodoPublic
from datetime import datetime

# ── 인메모리 저장소 ───────────────────────────────────
# 실제 dict로 저장 (id → todo dict)
_todos_store: dict[int, dict] = {}
_id_counter: int = 1


def get_todos_store() -> dict[int, dict]:
    """인메모리 ToDo 저장소를 반환합니다."""
    return _todos_store


def get_next_id() -> int:
    """다음 사용 가능한 ID를 반환하고 카운터를 증가시킵니다."""
    global _id_counter
    current = _id_counter
    _id_counter += 1
    return current


# ── Annotated 타입 별칭 ──────────────────────────────
TodoStoreDep = Annotated[dict[int, dict], Depends(get_todos_store)]
```

> 이 예제에서는 저장소를 모듈 변수로 관리합니다.
> 다음 Part에서 데이터베이스로 전환할 때 `get_todos_store`를 `get_db_session`으로 교체하면 됩니다.
> 라우터 코드 대부분을 유지할 수 있습니다 — 이것이 의존성 주입의 진가입니다.

---

<a id="6"></a>

## 6️⃣ Step 4: CRUD 엔드포인트 [↑](#toc)

`app/routers/todos.py` 파일을 작성합니다.

```python
# app/routers/todos.py

from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, timezone

from app.schemas import TodoCreate, TodoUpdate, TodoPublic, TodoStatus
from app.exceptions import TodoNotFoundError, TodoAlreadyDoneError
from app.dependencies import TodoStoreDep, get_next_id

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
)


@router.post(
    "",
    response_model=TodoPublic,
    status_code=201,
    summary="ToDo 생성",
)
def create_todo(todo: TodoCreate, store: TodoStoreDep):
    """새 ToDo 항목을 생성합니다."""
    todo_id = get_next_id()
    new_todo = {
        "id": todo_id,
        "title": todo.title,
        "content": todo.content,
        "status": "pending",
        "created_at": datetime.now(timezone.utc),
    }
    store[todo_id] = new_todo
    return new_todo


@router.get(
    "",
    response_model=list[TodoPublic],
    summary="ToDo 목록 조회",
)
def list_todos(
    store: TodoStoreDep,
    status: Optional[TodoStatus] = Query(
        None,
        description="상태로 필터링 (pending / done / archived)",
    ),
):
    """ToDo 목록을 반환합니다. status 파라미터로 필터링할 수 있습니다."""
    todos = list(store.values())
    if status is not None:
        todos = [t for t in todos if t["status"] == status]
    return todos


@router.get(
    "/{todo_id}",
    response_model=TodoPublic,
    summary="ToDo 단건 조회",
    responses={404: {"description": "ToDo를 찾을 수 없습니다"}},
)
def get_todo(todo_id: int, store: TodoStoreDep):
    """특정 ToDo 항목을 반환합니다."""
    if todo_id not in store:
        raise TodoNotFoundError(todo_id)
    return store[todo_id]


@router.put(
    "/{todo_id}",
    response_model=TodoPublic,
    summary="ToDo 수정",
    responses={
        404: {"description": "ToDo를 찾을 수 없습니다"},
        409: {"description": "이미 완료된 ToDo입니다"},
    },
)
def update_todo(todo_id: int, todo_update: TodoUpdate, store: TodoStoreDep):
    """ToDo 항목을 수정합니다. 전달된 필드만 업데이트됩니다."""
    if todo_id not in store:
        raise TodoNotFoundError(todo_id)

    existing = store[todo_id]

    # 이미 완료된 항목을 다시 완료 처리 방지
    if todo_update.status == "done" and existing["status"] == "done":
        raise TodoAlreadyDoneError(todo_id)

    # exclude_unset=True: 클라이언트가 보내지 않은 필드는 무시
    updated_fields = todo_update.model_dump(exclude_unset=True)
    store[todo_id] = {**existing, **updated_fields}
    return store[todo_id]


@router.delete(
    "/{todo_id}",
    status_code=204,
    summary="ToDo 삭제",
    responses={404: {"description": "ToDo를 찾을 수 없습니다"}},
)
def delete_todo(todo_id: int, store: TodoStoreDep):
    """ToDo 항목을 삭제합니다."""
    if todo_id not in store:
        raise TodoNotFoundError(todo_id)
    del store[todo_id]
```

---

<a id="7"></a>

## 7️⃣ Step 5: 메인 앱 연결 [↑](#toc)

`app/main.py` 파일을 작성합니다. 예외 핸들러도 여기에 등록합니다.

```python
# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.routers import todos
from app.exceptions import TodoNotFoundError, TodoAlreadyDoneError

app = FastAPI(
    title="ToDo API",
    description="Part 2 캡스톤 — APIRouter + Depends + 에러 처리",
    version="1.0.0",
)


# ── 예외 핸들러 등록 ──────────────────────────────────
@app.exception_handler(TodoNotFoundError)
def todo_not_found_handler(request: Request, exc: TodoNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "code": "TODO_NOT_FOUND",
            "message": f"ToDo {exc.todo_id}을(를) 찾을 수 없습니다",
        },
    )


@app.exception_handler(TodoAlreadyDoneError)
def todo_already_done_handler(request: Request, exc: TodoAlreadyDoneError):
    return JSONResponse(
        status_code=409,
        content={
            "code": "TODO_ALREADY_DONE",
            "message": f"ToDo {exc.todo_id}은(는) 이미 완료 처리되었습니다",
        },
    )


@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " → ".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({"field": field, "message": error["msg"]})
    return JSONResponse(
        status_code=422,
        content={
            "code": "VALIDATION_ERROR",
            "message": "입력값을 확인해주세요",
            "errors": errors,
        },
    )


# ── 라우터 등록 ───────────────────────────────────────
app.include_router(todos.router)


# ── 헬스 체크 ─────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "ToDo API 작동 중"}
```

서버 실행:

```bash
cd todo-api
uvicorn app.main:app --reload
```

실행 결과:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process using WatchFiles
INFO:     Application startup complete.
```

---

<a id="8"></a>

## 8️⃣ 완성 코드 전체 [↑](#toc)

각 파일의 전체 코드를 한 번에 확인합니다.

### app/schemas.py

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

TodoStatus = Literal["pending", "done", "archived"]


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = Field(None, max_length=1000)

    model_config = {
        "json_schema_extra": {
            "examples": [{"title": "FastAPI 복습", "content": "Depends() 정리"}]
        }
    }


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, max_length=1000)
    status: Optional[TodoStatus] = None


class TodoPublic(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    status: TodoStatus
    created_at: datetime


class ErrorResponse(BaseModel):
    code: str
    message: str
```

### app/exceptions.py

```python
class TodoNotFoundError(Exception):
    def __init__(self, todo_id: int):
        self.todo_id = todo_id
        super().__init__(f"ToDo {todo_id} not found")


class TodoAlreadyDoneError(Exception):
    def __init__(self, todo_id: int):
        self.todo_id = todo_id
        super().__init__(f"ToDo {todo_id} is already done")
```

### app/dependencies.py

```python
from typing import Annotated
from fastapi import Depends

_todos_store: dict[int, dict] = {}
_id_counter: int = 1


def get_todos_store() -> dict[int, dict]:
    return _todos_store


def get_next_id() -> int:
    global _id_counter
    current = _id_counter
    _id_counter += 1
    return current


TodoStoreDep = Annotated[dict[int, dict], Depends(get_todos_store)]
```

### app/routers/todos.py

```python
from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, timezone

from app.schemas import TodoCreate, TodoUpdate, TodoPublic, TodoStatus
from app.exceptions import TodoNotFoundError, TodoAlreadyDoneError
from app.dependencies import TodoStoreDep, get_next_id

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("", response_model=TodoPublic, status_code=201)
def create_todo(todo: TodoCreate, store: TodoStoreDep):
    todo_id = get_next_id()
    new_todo = {
        "id": todo_id,
        "title": todo.title,
        "content": todo.content,
        "status": "pending",
        "created_at": datetime.now(timezone.utc),
    }
    store[todo_id] = new_todo
    return new_todo


@router.get("", response_model=list[TodoPublic])
def list_todos(
    store: TodoStoreDep,
    status: Optional[TodoStatus] = Query(None),
):
    todos = list(store.values())
    if status is not None:
        todos = [t for t in todos if t["status"] == status]
    return todos


@router.get("/{todo_id}", response_model=TodoPublic)
def get_todo(todo_id: int, store: TodoStoreDep):
    if todo_id not in store:
        raise TodoNotFoundError(todo_id)
    return store[todo_id]


@router.put("/{todo_id}", response_model=TodoPublic)
def update_todo(todo_id: int, todo_update: TodoUpdate, store: TodoStoreDep):
    if todo_id not in store:
        raise TodoNotFoundError(todo_id)
    existing = store[todo_id]
    if todo_update.status == "done" and existing["status"] == "done":
        raise TodoAlreadyDoneError(todo_id)
    updated_fields = todo_update.model_dump(exclude_unset=True)
    store[todo_id] = {**existing, **updated_fields}
    return store[todo_id]


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, store: TodoStoreDep):
    if todo_id not in store:
        raise TodoNotFoundError(todo_id)
    del store[todo_id]
```

### app/main.py

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.routers import todos
from app.exceptions import TodoNotFoundError, TodoAlreadyDoneError

app = FastAPI(title="ToDo API", version="1.0.0")


@app.exception_handler(TodoNotFoundError)
def todo_not_found_handler(request: Request, exc: TodoNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"code": "TODO_NOT_FOUND", "message": f"ToDo {exc.todo_id}을(를) 찾을 수 없습니다"},
    )


@app.exception_handler(TodoAlreadyDoneError)
def todo_already_done_handler(request: Request, exc: TodoAlreadyDoneError):
    return JSONResponse(
        status_code=409,
        content={"code": "TODO_ALREADY_DONE", "message": f"ToDo {exc.todo_id}은(는) 이미 완료되었습니다"},
    )


@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": " → ".join(str(loc) for loc in e["loc"] if loc != "body"), "message": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"code": "VALIDATION_ERROR", "message": "입력값을 확인해주세요", "errors": errors},
    )


app.include_router(todos.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok"}
```

---

<a id="9"></a>

## 9️⃣ Swagger에서 전체 테스트 [↑](#toc)

`http://localhost:8000/docs`를 열고 아래 순서로 테스트해보세요.

### 시나리오 1: ToDo 생성과 조회

**1단계** — `POST /todos` 클릭 → "Try it out" → 아래 내용 입력:

```json
{
  "title": "FastAPI 10장 실습",
  "content": "Swagger에서 전체 API 테스트하기"
}
```

"Execute" 클릭. 응답:

```json
{
  "id": 1,
  "title": "FastAPI 10장 실습",
  "content": "Swagger에서 전체 API 테스트하기",
  "status": "pending",
  "created_at": "2026-04-10T10:00:00Z"
}
```

**2단계** — `POST /todos` 한 번 더 실행:

```json
{
  "title": "운동하기",
  "content": null
}
```

**3단계** — `GET /todos` 클릭 → "Try it out" → "Execute". 두 개의 ToDo가 보입니다.

### 시나리오 2: 상태 필터링

**4단계** — `PUT /todos/1` 클릭 → "Try it out" → id: `1` → 본문:

```json
{
  "status": "done"
}
```

**5단계** — `GET /todos` → `status` 파라미터에 `pending` 입력 → "Execute". ToDo 1은 사라지고 ToDo 2만 보입니다.

**6단계** — `GET /todos` → `status` 파라미터에 `done` 입력. ToDo 1만 보입니다.

### 시나리오 3: 에러 테스트

**7단계** — `GET /todos/999` 실행. 응답:

```json
{
  "code": "TODO_NOT_FOUND",
  "message": "ToDo 999을(를) 찾을 수 없습니다"
}
```

**8단계** — `PUT /todos/1` → `status`: `"done"` 재전송 (이미 완료된 항목). 응답:

```json
{
  "code": "TODO_ALREADY_DONE",
  "message": "ToDo 1은(는) 이미 완료 처리되었습니다"
}
```

**9단계** — `POST /todos` → 빈 title 전송 (`"title": ""`). 응답:

```json
{
  "code": "VALIDATION_ERROR",
  "message": "입력값을 확인해주세요",
  "errors": [
    {
      "field": "title",
      "message": "String should have at least 1 character"
    }
  ]
}
```

**10단계** — `DELETE /todos/1` → "Execute". 응답: `204 No Content`.

`GET /todos` 다시 실행하면 ToDo 1이 없어진 것을 확인할 수 있습니다.

---

<a id="10"></a>

## 🔟 정리 + 브릿지 [↑](#toc)

### Part 2에서 배운 것

| 장 | 기술 | 이 프로젝트에서의 역할 |
|----|------|----------------------|
| 07장 APIRouter | `routers/todos.py` | 엔드포인트를 별도 파일로 분리 |
| 08장 Depends | `TodoStoreDep` | 저장소 접근을 의존성으로 주입 |
| 09장 에러 처리 | `TodoNotFoundError` 등 | 커스텀 예외 + 핸들러로 일관된 에러 응답 |
| 04~06장 Pydantic/CRUD | `schemas.py` | 요청·응답 스키마 분리 |

### 이 구조의 강점 복습

```
# ❌ Part 1 방식: 한 파일에 모든 것
main.py  (스키마 + 라우트 + 에러처리 혼재)

# ✅ Part 2 방식: 역할별 분리
schemas.py       ← 데이터 형태
exceptions.py    ← 에러 분류
dependencies.py  ← 공통 준비 로직
routers/todos.py ← 비즈니스 로직
main.py          ← 조립 + 등록
```

### 인메모리의 한계

지금 만든 API는 **서버를 재시작하면 데이터가 사라집니다**. 프로덕션 서비스에는 쓸 수 없습니다.

```bash
# 서버 재시작
^C
uvicorn app.main:app --reload

# GET /todos → 빈 배열 []
# 데이터가 사라졌습니다
```

이것이 바로 다음 Part의 출발점입니다.

### Part 3 미리보기

인메모리 ToDo API를 완성했습니다. 하지만 서버를 재시작하면 데이터가 사라집니다.

**다음 Part에서 데이터베이스를 연결하여 영구 저장합니다.**

| 장 | 내용 |
|----|------|
| 11장 | SQLModel 기초 — 테이블을 Python 클래스로 정의 |
| 12장 | DB CRUD — 지금 만든 라우터를 DB 저장소로 교체 |
| 13장 | 관계 — 여러 테이블을 연결 |

가장 중요한 점: **라우터 코드(`routers/todos.py`)는 거의 바뀌지 않습니다.**

`dependencies.py`의 `get_todos_store`를 SQLModel 세션을 반환하는 함수로 교체하는 것이 전부입니다. 의존성 주입 덕분에 변경 범위가 최소화됩니다.

---

### 실습

**기본**: 이번 장의 코드를 처음부터 직접 타이핑해서 만들어보세요. 복사·붙여넣기 없이 한 파일씩 완성하면서 각 파일의 역할을 체감해보세요. 완성 후 Swagger에서 시나리오 1~3을 그대로 따라해보세요.

**중급**: `PUT /todos/{todo_id}` 엔드포인트에 `archived` 상태로 이미 보관된 ToDo를 수정 불가하게 만드는 검증 로직을 추가해보세요. `TodoArchivedError` 커스텀 예외를 만들고, 핸들러를 등록해 409 상태로 응답하도록 구현하세요.

**심화**: `GET /todos`에 `keyword` 쿼리 파라미터를 추가해서 `title`에 해당 키워드가 포함된 ToDo만 필터링하도록 구현해보세요. `status`와 `keyword`를 함께 사용할 수 있어야 합니다. 예) `GET /todos?status=pending&keyword=FastAPI`.

{% endraw %}
