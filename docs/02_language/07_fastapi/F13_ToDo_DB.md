---
title: 13. ToDo API → DB 버전
layout: default
grand_parent: Language
parent: FastAPI
nav_order: 13
permalink: /language/fastapi/todo-db
---

{% raw %}

## 학습 목표

- 10장의 인메모리 ToDo API 코드와 DB 버전 코드의 차이를 명확히 설명할 수 있다
- SQLModel + SQLite 기반의 완성된 ToDo CRUD API를 처음부터 끝까지 구현할 수 있다
- `session.exec(select(Todo).where(...))` 패턴으로 조건 조회를 작성할 수 있다
- Before / After 비교를 통해 "저장소만 교체한다"는 추상화 개념을 체험할 수 있다
- Swagger UI에서 서버 재시작 후에도 데이터가 유지됨을 직접 확인할 수 있다

<a id="toc"></a>

## 진행 순서

1. [리팩터링 전략](#strategy) — 무엇이 바뀌고 무엇이 유지되는가
2. [프로젝트 구조 업데이트](#structure) — 새 파일 / 수정 파일
3. [Step 1: 모델 정의](#step1-models) — SQLModel 모델들
4. [Step 2: 데이터베이스 설정](#step2-database) — engine, session, lifespan
5. [Step 3: CRUD 리팩터링](#step3-crud) — Before / After 비교
6. [Step 4: 필터링 with DB](#step4-filter) — WHERE 절 활용
7. [완성 코드](#full-code) — 전체 파일 모음
8. [Before / After 비교표](#comparison) — 핵심 차이 정리
9. [정리 + 다음 Part 미리보기](#summary)

---

# 13장. ToDo API → 데이터베이스 버전

<a id="strategy"></a>

## 1️⃣ 리팩터링 전략 [↑](#toc)

10장에서 완성한 ToDo API는 Python 리스트에 데이터를 저장했습니다.
이번 장에서는 그 코드를 SQLModel + SQLite로 교체합니다.

> "저장소만 바꿉니다.
> API 엔드포인트 구조, Pydantic 검증, Router 분리, HTTP 상태 코드 — 이 모든 것은 그대로입니다."

### 변하는 것 vs 유지되는 것

| 항목 | 변경 여부 | 설명 |
|------|:---------:|------|
| API URL 구조 | ✅ 유지 | `/todos`, `/todos/{id}` 그대로 |
| HTTP 메서드 | ✅ 유지 | GET, POST, PATCH, DELETE 그대로 |
| 응답 형태 | ✅ 유지 | JSON 구조 동일 |
| Pydantic 검증 | ✅ 유지 | 입력 검증 그대로 |
| Router 구조 | ✅ 유지 | APIRouter 그대로 |
| 저장소 | 🔄 변경 | `list` → `SQLite` |
| ID 생성 | 🔄 변경 | 수동 카운터 → DB auto-increment |
| 검색 | 🔄 변경 | list comprehension → SQL WHERE |
| 영속성 | 🔄 변경 | 서버 종료 시 삭제 → 영구 저장 |

---

<a id="structure"></a>

## 2️⃣ 프로젝트 구조 업데이트 [↑](#toc)

```
todo-api/
├── app/
│   ├── __init__.py
│   ├── main.py           ← UPDATED  (lifespan 추가)
│   ├── database.py       ← NEW      (engine, get_session)
│   ├── models.py         ← NEW      (SQLModel 모델)
│   ├── routers/
│   │   ├── __init__.py
│   │   └── todos.py      ← UPDATED  (session 기반 CRUD)
│   ├── schemas.py        ← UPDATED  (TodoUpdate 수정)
│   └── dependencies.py   ← UPDATED  (fake_db 제거)
├── requirements.txt      ← UPDATED  (sqlmodel 추가)
└── .gitignore            ← UPDATED  (database.db 추가)
```

### requirements.txt

```txt
fastapi>=0.135.0
uvicorn[standard]
sqlmodel
```

---

<a id="step1-models"></a>

## 3️⃣ Step 1: 모델 정의 [↑](#toc)

10장의 Pydantic 모델을 SQLModel로 교체합니다.

### 10장의 스키마 (Before)

```python
# schemas.py (10장)
from pydantic import BaseModel
from enum import Enum


class TodoStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    status: TodoStatus = TodoStatus.todo


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TodoStatus | None = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TodoStatus
```

### 13장의 모델 (After)

```python
# models.py  ← 새 파일
from sqlmodel import Field, SQLModel
from enum import Enum


class TodoStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


# ── 공통 필드 ────────────────────────────────────────────

class TodoBase(SQLModel):
    title: str
    description: str | None = Field(default=None)
    status: TodoStatus = Field(default=TodoStatus.todo)


# ── DB 테이블 ────────────────────────────────────────────

class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # DB가 자동으로 1, 2, 3... 부여합니다


# ── API 입력용 ──────────────────────────────────────────

class TodoCreate(TodoBase):
    pass
    # id 없이 title, description, status만 받습니다


# ── API 응답용 ──────────────────────────────────────────

class TodoPublic(TodoBase):
    id: int
    # id를 반드시 포함해서 반환합니다


# ── 부분 수정용 (PATCH) ──────────────────────────────────

class TodoUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    status: TodoStatus | None = None
    # 모든 필드가 선택사항 — 보낸 필드만 업데이트됩니다
```

### 모델 변경 포인트

| 10장 (Pydantic) | 13장 (SQLModel) | 이유 |
|-----------------|-----------------|------|
| `BaseModel` | `SQLModel` | SQLAlchemy 연동 |
| `TodoResponse` | `TodoPublic` | SQLModel 관례 |
| id는 `TodoResponse`에만 | Base/table/Create/Public 분리 | 역할 명확화 |
| id 직접 정의 없음 | `primary_key=True` | DB auto-increment |

---

<a id="step2-database"></a>

## 4️⃣ Step 2: 데이터베이스 설정 [↑](#toc)

### database.py (새 파일)

```python
# app/database.py
from typing import Generator
from sqlmodel import Session, create_engine

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,  # True로 바꾸면 SQL 쿼리가 콘솔에 출력됩니다
    connect_args={"check_same_thread": False},
    # SQLite는 기본적으로 하나의 스레드만 허용합니다
    # FastAPI는 멀티스레드 환경이므로 이 설정이 필요합니다
)


def get_session() -> Generator[Session, None, None]:
    """의존성 주입용 세션 제공 함수"""
    with Session(engine) as session:
        yield session
```

> "`check_same_thread=False`는 SQLite 전용 설정입니다.
> 나중에 PostgreSQL로 교체하면 이 줄은 필요 없습니다."

### main.py 업데이트

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine
from .routers import todos


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시: DB 테이블 생성
    SQLModel.metadata.create_all(engine)
    yield
    # 서버 종료 시: 필요한 정리 작업 (지금은 없음)


app = FastAPI(
    title="ToDo API — DB 버전",
    description="SQLModel + SQLite 기반 ToDo 관리 API",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(todos.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "2.0.0", "storage": "SQLite"}
```

---

<a id="step3-crud"></a>

## 5️⃣ Step 3: CRUD 리팩터링 [↑](#toc)

인메모리 코드와 DB 코드를 나란히 비교합니다.
구조는 완전히 같고, 저장 방법만 다릅니다.

### CREATE — POST /todos

# ❌ 10장 인메모리
```python
# routers/todos.py (10장)
fake_db: list[dict] = []
id_counter = 1


@router.post("/", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate):
    global id_counter
    new_todo = {"id": id_counter, **todo.model_dump()}
    fake_db.append(new_todo)
    id_counter += 1
    return new_todo
```

# ✅ 13장 DB 버전
```python
# routers/todos.py (13장)
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Todo, TodoCreate, TodoPublic, TodoUpdate


router = APIRouter(prefix="/todos", tags=["ToDo"])


@router.post("/", response_model=TodoPublic, status_code=201)
def create_todo(
    todo_data: TodoCreate,
    session: Session = Depends(get_session),
):
    db_todo = Todo.model_validate(todo_data)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)  # DB가 부여한 id를 가져옵니다
    return db_todo
```

핵심 변경: `fake_db.append()` → `session.add() + session.commit()`

### READ ALL — GET /todos

# ❌ 10장 인메모리
```python
@router.get("/", response_model=list[TodoResponse])
def read_todos():
    return fake_db
```

# ✅ 13장 DB 버전
```python
@router.get("/", response_model=list[TodoPublic])
def read_todos(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 20,
):
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return todos
```

핵심 변경: `return fake_db` → `session.exec(select(Todo)).all()`

### READ ONE — GET /todos/{todo_id}

# ❌ 10장 인메모리
```python
@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int):
    for item in fake_db:
        if item["id"] == todo_id:
            return item
    raise HTTPException(status_code=404, detail="Todo not found")
```

# ✅ 13장 DB 버전
```python
@router.get("/{todo_id}", response_model=TodoPublic)
def read_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
```

핵심 변경: `for` 루프 순회 → `session.get(Todo, todo_id)`

### UPDATE — PATCH /todos/{todo_id}

# ❌ 10장 인메모리
```python
@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, updates: TodoUpdate):
    for item in fake_db:
        if item["id"] == todo_id:
            update_data = updates.model_dump(exclude_unset=True)
            item.update(update_data)
            return item
    raise HTTPException(status_code=404, detail="Todo not found")
```

# ✅ 13장 DB 버전
```python
@router.patch("/{todo_id}", response_model=TodoPublic)
def update_todo(
    todo_id: int,
    updates: TodoUpdate,
    session: Session = Depends(get_session),
):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = updates.model_dump(exclude_unset=True)
    db_todo.sqlmodel_update(update_data)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo
```

핵심 변경: `item.update()` → `db_todo.sqlmodel_update() + session.commit()`

### DELETE — DELETE /todos/{todo_id}

# ❌ 10장 인메모리
```python
@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    for i, item in enumerate(fake_db):
        if item["id"] == todo_id:
            fake_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Todo not found")
```

# ✅ 13장 DB 버전
```python
@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(db_todo)
    session.commit()
```

핵심 변경: `fake_db.pop(i)` → `session.delete() + session.commit()`

---

<a id="step4-filter"></a>

## 6️⃣ Step 4: 필터링 with DB [↑](#toc)

10장에서는 list comprehension으로 필터링했습니다.
DB 버전에서는 SQL `WHERE` 절을 사용합니다.

### 상태별 필터링

# ❌ 10장 인메모리
```python
@router.get("/", response_model=list[TodoResponse])
def read_todos(status: TodoStatus | None = None):
    if status:
        return [item for item in fake_db if item["status"] == status]
    return fake_db
```

# ✅ 13장 DB 버전
```python
from sqlmodel import select
from ..models import Todo, TodoPublic, TodoStatus


@router.get("/", response_model=list[TodoPublic])
def read_todos(
    session: Session = Depends(get_session),
    status: TodoStatus | None = None,
    offset: int = 0,
    limit: int = 20,
):
    statement = select(Todo)

    if status:
        statement = statement.where(Todo.status == status)

    statement = statement.offset(offset).limit(limit)
    todos = session.exec(statement).all()
    return todos
```

Swagger UI에서 쿼리 파라미터로 테스트:
```
GET /todos?status=in_progress
GET /todos?status=done&limit=5
GET /todos?offset=10&limit=5
```

실행 결과 (`GET /todos?status=done`):
```json
[
  {
    "id": 2,
    "title": "운동하기",
    "description": null,
    "status": "done"
  },
  {
    "id": 5,
    "title": "책 읽기",
    "description": "파이썬 책",
    "status": "done"
  }
]
```

### 제목 검색 추가하기

```python
@router.get("/search", response_model=list[TodoPublic])
def search_todos(
    q: str,
    session: Session = Depends(get_session),
):
    # LIKE 연산자로 제목 검색 (대소문자 구분 없음)
    statement = select(Todo).where(Todo.title.contains(q))
    todos = session.exec(statement).all()
    return todos
```

실행 결과 (`GET /todos/search?q=공부`):
```json
[
  {
    "id": 1,
    "title": "FastAPI 공부하기",
    "description": null,
    "status": "todo"
  },
  {
    "id": 4,
    "title": "SQLModel 공부하기",
    "description": "11장 예제",
    "status": "in_progress"
  }
]
```

---

<a id="full-code"></a>

## 7️⃣ 완성 코드 [↑](#toc)

### app/models.py

```python
from sqlmodel import Field, SQLModel
from enum import Enum


class TodoStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TodoBase(SQLModel):
    title: str
    description: str | None = Field(default=None)
    status: TodoStatus = Field(default=TodoStatus.todo)


class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TodoCreate(TodoBase):
    pass


class TodoPublic(TodoBase):
    id: int


class TodoUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    status: TodoStatus | None = None
```

### app/database.py

```python
from typing import Generator
from sqlmodel import Session, create_engine

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
```

### app/main.py

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine
from .routers import todos


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="ToDo API — DB 버전",
    description="SQLModel + SQLite 기반 ToDo 관리 API",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(todos.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "2.0.0", "storage": "SQLite"}
```

### app/routers/todos.py

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import Todo, TodoCreate, TodoPublic, TodoStatus, TodoUpdate

router = APIRouter(prefix="/todos", tags=["ToDo"])


@router.post("/", response_model=TodoPublic, status_code=201)
def create_todo(
    todo_data: TodoCreate,
    session: Session = Depends(get_session),
):
    db_todo = Todo.model_validate(todo_data)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.get("/", response_model=list[TodoPublic])
def read_todos(
    session: Session = Depends(get_session),
    status: TodoStatus | None = None,
    offset: int = 0,
    limit: int = 20,
):
    statement = select(Todo)
    if status:
        statement = statement.where(Todo.status == status)
    statement = statement.offset(offset).limit(limit)
    return session.exec(statement).all()


@router.get("/search", response_model=list[TodoPublic])
def search_todos(q: str, session: Session = Depends(get_session)):
    statement = select(Todo).where(Todo.title.contains(q))
    return session.exec(statement).all()


@router.get("/{todo_id}", response_model=TodoPublic)
def read_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.patch("/{todo_id}", response_model=TodoPublic)
def update_todo(
    todo_id: int,
    updates: TodoUpdate,
    session: Session = Depends(get_session),
):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = updates.model_dump(exclude_unset=True)
    db_todo.sqlmodel_update(update_data)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(db_todo)
    session.commit()
```

### 실행 및 Swagger UI 확인

```bash
uvicorn app.main:app --reload
```

실행 결과:
```
INFO:     Started server process [99999]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

`http://localhost:8000/docs` 접속:

```
📋 ToDo API — DB 버전

ToDo
  POST   /todos/             ← 할 일 생성
  GET    /todos/             ← 목록 조회 (상태 필터, 페이지네이션)
  GET    /todos/search       ← 제목 검색
  GET    /todos/{todo_id}    ← 단건 조회
  PATCH  /todos/{todo_id}    ← 부분 수정
  DELETE /todos/{todo_id}    ← 삭제

default
  GET    /health             ← 헬스체크
```

**영속성 테스트**:
1. `POST /todos`로 할 일 3개 생성
2. `Ctrl+C`로 서버 종료
3. 다시 `uvicorn app.main:app --reload`로 시작
4. `GET /todos` → 데이터가 그대로 남아있습니다!

---

<a id="comparison"></a>

## 8️⃣ Before / After 비교표 [↑](#toc)

### 저장소 비교

| 항목 | 인메모리 (10장) | DB (13장) |
|------|----------------|-----------|
| 저장소 | Python `list` | SQLite 파일 |
| ID 생성 | 수동 카운터 (`id_counter += 1`) | DB auto-increment |
| 영속성 | 서버 종료 시 삭제 | 영구 저장 |
| 검색 | list comprehension | SQL `WHERE` 절 |
| 페이지네이션 | 슬라이싱 (`[offset:offset+limit]`) | `.offset().limit()` |
| 동시 접속 | 문제 발생 가능 | 트랜잭션으로 안전 |

### 코드 비교

| 작업 | 인메모리 (10장) | DB (13장) |
|------|----------------|-----------|
| 저장 | `fake_db.append(item)` | `session.add(db_todo)` + `session.commit()` |
| 전체 조회 | `return fake_db` | `session.exec(select(Todo)).all()` |
| 단건 조회 | `for` 루프 | `session.get(Todo, id)` |
| 필터링 | `[x for x in db if x["status"] == s]` | `select(Todo).where(Todo.status == s)` |
| 수정 | `item.update(data)` | `sqlmodel_update(data)` + `session.commit()` |
| 삭제 | `fake_db.pop(i)` | `session.delete(todo)` + `session.commit()` |
| ID 부여 | `id_counter += 1` | 자동 (DB가 처리) |

### 변하지 않은 것들

```python
# 10장과 13장이 완전히 동일한 부분들

# 1. HTTP 상태 코드
status_code=201  # 생성
status_code=204  # 삭제

# 2. 404 처리
raise HTTPException(status_code=404, detail="Todo not found")

# 3. PATCH의 부분 업데이트
updates.model_dump(exclude_unset=True)

# 4. Router 구조
router = APIRouter(prefix="/todos", tags=["ToDo"])
app.include_router(todos.router)

# 5. lifespan 패턴 (10장에서 배운 구조 그대로)
@asynccontextmanager
async def lifespan(app: FastAPI):
    ...
    yield
```

---

<a id="summary"></a>

## 9️⃣ 정리 [↑](#toc)

### 이번 장에서 한 일

```
10장 ToDo API (인메모리)
    ↓
1. models.py 생성     — Pydantic → SQLModel 전환
2. database.py 생성   — engine, get_session 설정
3. main.py 수정      — lifespan으로 테이블 자동 생성
4. routers/todos.py 수정 — session 기반 CRUD로 교체
    ↓
13장 ToDo API (SQLite 영구 저장)
```

### 핵심 교훈

> "API 계층과 저장소 계층은 분리되어 있습니다.
> Router와 엔드포인트 코드는 거의 그대로이고,
> 저장 방법만 교체했습니다.
> 나중에 SQLite를 PostgreSQL로 바꿀 때도 마찬가지입니다 — `DATABASE_URL`만 바꾸면 됩니다."

### 최종 점검 체크리스트

```
✅ database.db 파일이 생성됩니까?
✅ Swagger UI에서 POST → GET 순서로 데이터가 보입니까?
✅ 서버 재시작 후에도 데이터가 남아있습니까?
✅ GET /todos?status=done 필터링이 작동합니까?
✅ 존재하지 않는 id로 GET 시 404가 반환됩니까?
✅ PATCH로 title만 보냈을 때 나머지 필드가 유지됩니까?
```

---

### 다음 Part 미리보기

데이터가 영구 저장됩니다!

이제 Part 4에서는 이 API를 **실전 수준**으로 완성합니다.

| 장 | 제목 | 내용 |
|----|------|------|
| 14장 | 테스트 (pytest) | `TestClient`로 API 자동 테스트 |
| 15장 | 미들웨어와 CORS | 프론트엔드와 연결하기 |
| 16장 | Docker 배포 | 컨테이너로 서버에 올리기 |

다음 14장에서는 지금까지 만든 DB 버전 API에 pytest 테스트를 작성합니다.
"잘 만들었다고 생각했는데 배포하니 오류가 나더라" — 테스트가 이 상황을 막아줍니다.

---

### 실습

**기본**: 이번 장의 완성 코드를 그대로 구현하고, 아래 순서로 Swagger UI에서 테스트해보세요.
1. `POST /todos` × 5회 (다양한 status 포함)
2. `GET /todos?status=done`
3. 서버 `Ctrl+C` 종료 후 재시작
4. `GET /todos` — 데이터가 그대로인지 확인

**중급**: `GET /todos`에 `title` 쿼리 파라미터를 추가하세요. title이 주어지면 `.contains()`로 필터링하고, 없으면 전체를 반환합니다. 기존 `search` 엔드포인트와 중복되지만 쿼리 파라미터 방식도 익혀봅니다.

**심화**: `GET /todos/stats` 엔드포인트를 추가하세요. 응답 형태는 아래와 같습니다. SQLModel의 `select(func.count())` 또는 Python에서 각 status별로 `session.exec(select(Todo).where(...)).all()`을 호출해서 계산해도 됩니다.
```json
{
  "total": 10,
  "todo": 4,
  "in_progress": 3,
  "done": 3
}
```

{% endraw %}
