---
title: 07. APIRouter — 코드 분리
layout: default
grand_parent: Language
parent: FastAPI
nav_order: 7
permalink: /language/fastapi/router
---

{% raw %}

# 07장. APIRouter — 코드 분리
{: .no_toc }

> "APIRouter = 식당의 부서 — 주방, 홀, 바를 나누듯 라우트를 모듈로 분리합니다"
> 메뉴가 200개인 식당이 한 장짜리 메뉴판을 쓸 수 있을까요?
> 코드도 마찬가지입니다. 엔드포인트가 늘어날수록 하나의 파일은 감당하기 어려워집니다.

## 학습 목표
{: .no_toc }

- `main.py` 한 파일에 모든 코드를 몰아 넣는 방식의 문제를 이해합니다
- `APIRouter`로 엔드포인트를 파일별로 나누는 방법을 익힙니다
- Pydantic 스키마를 별도 파일로 분리하는 패턴을 배웁니다
- `app.include_router()`로 라우터를 앱에 등록하는 방법을 습득합니다
- Swagger UI에서 태그(tags)로 그룹화된 API 문서를 확인합니다

<a id="toc"></a>

## 진행 순서

1. [문제: main.py가 너무 길다](#1) — 100줄 단일 파일의 한계
2. [APIRouter 기본 사용법](#2) — `prefix`, `tags` 설정
3. [프로젝트 구조 설계](#3) — 디렉터리 구조 잡기
4. [스키마 분리: schemas.py](#4) — Pydantic 모델 모으기
5. [라우터 파일 작성](#5) — `routers/items.py`, `routers/users.py`
6. [app.include_router() 연결](#6) — `main.py` 간결하게 유지하기
7. [Swagger에서 태그 확인](#7) — 그룹화된 문서 보기
8. [정리](#8)

---

<a id="1"></a>

## 1️⃣ 문제: main.py가 너무 길다 [↑](#toc)

Part 1에서 만든 인메모리 CRUD API를 떠올려보세요. 아이템과 사용자 엔드포인트를 함께 넣으면 `main.py`가 순식간에 100줄을 넘어갑니다.

```python
# main.py  ← 모든 것이 한 파일에
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# --- Pydantic 모델 ---
class ItemCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ItemPublic(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: str

class UserPublic(BaseModel):
    id: int
    username: str
    email: str

# --- 인메모리 저장소 ---
items_db: list[dict] = []
users_db: list[dict] = []
item_id_counter = 1
user_id_counter = 1

# --- 아이템 엔드포인트 ---
@app.get("/items", response_model=list[ItemPublic])
def list_items():
    return items_db

@app.get("/items/{item_id}", response_model=ItemPublic)
def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")

@app.post("/items", response_model=ItemPublic, status_code=201)
def create_item(item: ItemCreate):
    global item_id_counter
    new_item = {"id": item_id_counter, **item.model_dump()}
    items_db.append(new_item)
    item_id_counter += 1
    return new_item

@app.put("/items/{item_id}", response_model=ItemPublic)
def update_item(item_id: int, item: ItemCreate):
    for i, existing in enumerate(items_db):
        if existing["id"] == item_id:
            items_db[i] = {"id": item_id, **item.model_dump()}
            return items_db[i]
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")

# --- 사용자 엔드포인트 ---
@app.get("/users", response_model=list[UserPublic])
def list_users():
    return users_db

@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

@app.post("/users", response_model=UserPublic, status_code=201)
def create_user(user: UserCreate):
    global user_id_counter
    new_user = {"id": user_id_counter, **user.model_dump()}
    users_db.append(new_user)
    user_id_counter += 1
    return new_user

# ... 아직 더 남아있습니다
```

이 파일이 길어질수록 어떤 문제가 생길까요?

| 문제 | 설명 |
|------|------|
| **찾기 어렵다** | "아이템 삭제 함수가 몇 번째 줄이지?" 스크롤이 필요합니다 |
| **팀 작업 충돌** | A가 아이템 수정, B가 사용자 수정 → 같은 파일 충돌 |
| **테스트 어렵다** | 아이템 기능만 테스트하고 싶어도 전체 import |
| **재사용 불가** | 다른 프로젝트에 사용자 API를 옮기려면 잘라내야 함 |

> 식당 비유로 돌아가겠습니다.
> 주방 레시피, 홀 서비스 매뉴얼, 바 칵테일 목록을 한 장에 적은 식당은 없습니다.
> 각 부서에 맞는 메뉴얼이 따로 있어야 직원이 자신의 역할에 집중할 수 있습니다.

---

<a id="2"></a>

## 2️⃣ APIRouter 기본 사용법 [↑](#toc)

`APIRouter`는 `FastAPI` 앱과 거의 동일한 방식으로 라우트를 등록합니다. 다른 점은 나중에 `app.include_router()`로 메인 앱에 "붙인다"는 것입니다.

```python
# routers/items.py

from fastapi import APIRouter, HTTPException

# APIRouter 생성
# prefix   → 이 라우터의 모든 경로 앞에 붙는 접두어
# tags     → Swagger UI 에서 그룹 이름
router = APIRouter(
    prefix="/items",
    tags=["Items"],
)

@router.get("")               # GET /items
def list_items():
    return []

@router.get("/{item_id}")     # GET /items/{item_id}
def get_item(item_id: int):
    raise HTTPException(status_code=404, detail="아이템 없음")

@router.post("", status_code=201)  # POST /items
def create_item():
    return {"id": 1}
```

`prefix="/items"`를 설정했기 때문에 `@router.get("")`은 `GET /items`가 됩니다.
`@router.get("/{item_id}")`는 `GET /items/{item_id}`가 됩니다.

---

<a id="3"></a>

## 3️⃣ 프로젝트 구조 설계 [↑](#toc)

이번 장에서 만들 최종 구조입니다.

```
app/
├── main.py          ← 앱 생성 + 라우터 등록만 담당
├── schemas.py       ← Pydantic 모델 모음
└── routers/
    ├── __init__.py  ← 빈 파일 (패키지 표시)
    ├── items.py     ← 아이템 관련 엔드포인트
    └── users.py     ← 사용자 관련 엔드포인트
```

이 구조의 규칙은 단순합니다.

- `main.py` — 앱 설정과 라우터 등록만. 엔드포인트 함수 없음
- `schemas.py` — 모든 Pydantic 모델 정의
- `routers/*.py` — 도메인별 엔드포인트 함수

먼저 디렉터리를 만들겠습니다.

```bash
mkdir -p app/routers
touch app/__init__.py
touch app/routers/__init__.py
touch app/schemas.py
touch app/routers/items.py
touch app/routers/users.py
touch app/main.py
```

---

<a id="4"></a>

## 4️⃣ 스키마 분리: schemas.py [↑](#toc)

Pydantic 모델을 `schemas.py` 한 곳에 모아두면 라우터 파일이 얼마나 늘어나도 모델을 재사용할 수 있습니다.

```python
# app/schemas.py

from pydantic import BaseModel, Field
from typing import Optional


# ── 아이템 ──────────────────────────────────────────────
class ItemCreate(BaseModel):
    """아이템 생성 요청 스키마"""
    name: str = Field(..., min_length=1, max_length=100, description="아이템 이름")
    price: float = Field(..., gt=0, description="가격 (0보다 커야 합니다)")
    description: Optional[str] = Field(None, max_length=500)


class ItemUpdate(BaseModel):
    """아이템 수정 요청 스키마 (모든 필드 선택적)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=500)


class ItemPublic(BaseModel):
    """아이템 응답 스키마"""
    id: int
    name: str
    price: float
    description: Optional[str] = None


# ── 사용자 ──────────────────────────────────────────────
class UserCreate(BaseModel):
    """사용자 생성 요청 스키마"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., description="이메일 주소")


class UserPublic(BaseModel):
    """사용자 응답 스키마"""
    id: int
    username: str
    email: str
```

> 왜 `ItemCreate`와 `ItemPublic`을 분리할까요?
> 클라이언트가 보내는 데이터와 서버가 돌려주는 데이터는 다를 수 있습니다.
> `id`는 서버가 생성하므로 요청에 포함되면 안 됩니다.
> `password`는 응답에 포함되면 안 됩니다.
> 이 분리 패턴은 보안과 유연성 모두에 필요합니다.

---

<a id="5"></a>

## 5️⃣ 라우터 파일 작성 [↑](#toc)

### routers/items.py

```python
# app/routers/items.py

from fastapi import APIRouter, HTTPException
from app.schemas import ItemCreate, ItemUpdate, ItemPublic

router = APIRouter(
    prefix="/items",
    tags=["Items"],
)

# 인메모리 저장소
_items_db: list[dict] = []
_id_counter = 1


@router.get("", response_model=list[ItemPublic])
def list_items():
    """모든 아이템을 반환합니다."""
    return _items_db


@router.get("/{item_id}", response_model=ItemPublic)
def get_item(item_id: int):
    """특정 아이템을 반환합니다."""
    for item in _items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")


@router.post("", response_model=ItemPublic, status_code=201)
def create_item(item: ItemCreate):
    """새 아이템을 생성합니다."""
    global _id_counter
    new_item = {"id": _id_counter, **item.model_dump()}
    _items_db.append(new_item)
    _id_counter += 1
    return new_item


@router.put("/{item_id}", response_model=ItemPublic)
def update_item(item_id: int, item: ItemUpdate):
    """아이템을 수정합니다. 전달된 필드만 업데이트됩니다."""
    for i, existing in enumerate(_items_db):
        if existing["id"] == item_id:
            # exclude_unset=True → 보내지 않은 필드는 수정하지 않음
            updated = {**existing, **item.model_dump(exclude_unset=True)}
            _items_db[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int):
    """아이템을 삭제합니다."""
    for i, item in enumerate(_items_db):
        if item["id"] == item_id:
            _items_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
```

### routers/users.py

```python
# app/routers/users.py

from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate, UserPublic

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

_users_db: list[dict] = []
_user_id_counter = 1


@router.get("", response_model=list[UserPublic])
def list_users():
    """모든 사용자를 반환합니다."""
    return _users_db


@router.get("/{user_id}", response_model=UserPublic)
def get_user(user_id: int):
    """특정 사용자를 반환합니다."""
    for user in _users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")


@router.post("", response_model=UserPublic, status_code=201)
def create_user(user: UserCreate):
    """새 사용자를 생성합니다."""
    global _user_id_counter
    new_user = {"id": _user_id_counter, **user.model_dump()}
    _users_db.append(new_user)
    _user_id_counter += 1
    return new_user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    """사용자를 삭제합니다."""
    for i, user in enumerate(_users_db):
        if user["id"] == user_id:
            _users_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
```

---

<a id="6"></a>

## 6️⃣ app.include_router() 연결 [↑](#toc)

이제 `main.py`는 라우터를 불러와서 등록하는 역할만 합니다.

```python
# app/main.py

from fastapi import FastAPI
from app.routers import items, users

app = FastAPI(
    title="구조화된 아이템 API",
    description="APIRouter로 파일을 나눈 예제",
    version="1.0.0",
)

# 라우터 등록
app.include_router(items.router)
app.include_router(users.router)


@app.get("/", tags=["Health"])
def root():
    """서버 상태를 확인합니다."""
    return {"status": "ok", "message": "API가 정상 작동 중입니다"}
```

서버를 실행합니다.

```bash
uvicorn app.main:app --reload
```

실행 결과:

```
INFO:     Will watch for changes in these directories: ['...']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### include_router 옵션

`include_router()`에 추가 옵션을 넘길 수 있습니다. 라우터 파일의 `prefix`나 `tags`를 **등록 시점에 오버라이드**하고 싶을 때 유용합니다.

```python
# prefix나 tags를 등록 시점에 지정하는 것도 가능합니다
app.include_router(
    items.router,
    prefix="/api/v1",   # /items → /api/v1/items
    tags=["Items v1"],
)
```

> 일반적으로는 라우터 파일 안에 `prefix`와 `tags`를 넣는 방식을 권장합니다.
> 라우터 파일을 보는 것만으로 어떤 경로를 담당하는지 한눈에 보이기 때문입니다.

---

<a id="7"></a>

## 7️⃣ Swagger에서 태그 확인 [↑](#toc)

`http://localhost:8000/docs`를 열어보세요.

태그별로 엔드포인트가 그룹화되어 있습니다.

```
┌─────────────────────────────────┐
│ Items                         ▼ │  ← tags=["Items"]
├─────────────────────────────────┤
│ GET    /items         목록      │
│ POST   /items         생성      │
│ GET    /items/{id}    조회      │
│ PUT    /items/{id}    수정      │
│ DELETE /items/{id}    삭제      │
├─────────────────────────────────┤
│ Users                         ▼ │  ← tags=["Users"]
├─────────────────────────────────┤
│ GET    /users         목록      │
│ POST   /users         생성      │
│ GET    /users/{id}    조회      │
│ DELETE /users/{id}    삭제      │
├─────────────────────────────────┤
│ Health                        ▼ │  ← tags=["Health"]
├─────────────────────────────────┤
│ GET    /             상태 확인  │
└─────────────────────────────────┘
```

태그는 Swagger UI에서 **시각적 구분선** 역할을 합니다. 팀원과 API를 공유할 때 "Items 그룹에서 생성 엔드포인트를 봐주세요" 하고 말할 수 있습니다.

### 직접 테스트해보세요

1. `POST /items` 클릭 → "Try it out" → 요청 본문 입력 → "Execute"
2. `GET /items` 클릭 → "Try it out" → "Execute" → 방금 만든 아이템이 보입니다
3. `GET /items/{item_id}` 클릭 → id 입력 → "Execute"

---

<a id="8"></a>

## 8️⃣ 정리 [↑](#toc)

| 개념 | 설명 |
|------|------|
| `APIRouter` | 라우트 묶음. `FastAPI` 앱처럼 `@router.get()`, `@router.post()` 사용 |
| `prefix` | 라우터의 모든 경로 앞에 붙는 공통 접두어 (`/items`, `/users`) |
| `tags` | Swagger UI에서 엔드포인트를 그룹화하는 이름 |
| `app.include_router()` | 라우터를 메인 앱에 등록. 이 시점에 실제 경로가 생성됨 |
| `schemas.py` | Pydantic 모델을 한 파일에 모아 라우터 간에 공유 |

### 파일 구조 최종 확인

```
# ❌ 분리 전
main.py   ← 100줄 이상, 모든 것이 섞여 있음

# ✅ 분리 후
app/
├── main.py        ← 10줄, 등록만
├── schemas.py     ← 모델만
└── routers/
    ├── items.py   ← 아이템만
    └── users.py   ← 사용자만
```

### 다음 장 미리보기

코드를 깔끔하게 분리했습니다. 그런데 여러 엔드포인트에서 같은 로직(예: 인증 확인, 페이지네이션 파라미터 파싱)이 반복된다면 어떻게 해야 할까요?

다음 08장에서 **의존성 주입(Depends)** 을 배우면 코드 중복을 더 줄일 수 있습니다. 여러 라우터에서 공통 로직을 한 곳에 정의하고 재사용하는 방법입니다.

---

### 실습

**기본**: 위 구조대로 프로젝트를 만들고 `uvicorn app.main:app --reload`로 실행한 뒤, Swagger UI(`/docs`)에서 아이템을 하나 생성하고 조회해보세요.

**중급**: `routers/` 아래에 `categories.py`를 추가하고, `GET /categories` 엔드포인트(고정 목록 반환)를 만들어 `main.py`에 등록해보세요. Swagger에서 새 "Categories" 그룹이 보이는지 확인하세요.

**심화**: `ItemUpdate`의 `exclude_unset=True` 옵션을 제거하면 어떤 일이 생기는지 테스트해보세요. `PUT /items/1`에 `{"price": 9.99}` 만 보냈을 때 `name`과 `description`이 어떻게 되는지 비교하고, 왜 `exclude_unset=True`가 필요한지 설명해보세요.

{% endraw %}
