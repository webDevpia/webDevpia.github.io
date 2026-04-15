---
title: 06. CRUD 완성 (인메모리)
layout: default
grand_parent: Language
parent: FastAPI (리뉴얼)
nav_order: 6
permalink: /language/fastapi-new/crud
---

{% raw %}

## 학습 목표

- Create, Read, Update, Delete 4가지 작업을 하나의 API로 완성할 수 있다
- 인메모리 `list`를 사용한 1단계 전략의 장단점을 설명할 수 있다
- 404, 201, 204 상태 코드를 올바른 상황에 적용할 수 있다

<a id="toc"></a>

## 진행 순서

1. [프로젝트 구조](#part1) - 단일 파일 CRUD 설계
2. [Create (POST)](#part2) - 아이템 생성
3. [Read (GET)](#part3) - 목록 조회와 단일 조회
4. [Update (PUT)](#part4) - 전체 교체
5. [Delete (DELETE)](#part5) - 삭제 + 204 응답
6. [전체 코드](#part6) - 완성된 인메모리 CRUD API
7. [Swagger에서 전체 테스트](#part7) - 4가지 작업 모두 체험
8. [한계: 새로고침하면 사라집니다](#part8) - 인메모리의 제약
9. [정리](#part9) - 핵심 개념 요약

---

# 06장. CRUD 완성 — 인메모리 데이터로 시작

> CRUD는 식당 운영의 4가지 기본 작업과 같습니다.
> **메뉴 등록(Create)** — 새 메뉴를 추가합니다.
> **메뉴 조회(Read)** — 메뉴판을 보거나 특정 메뉴를 확인합니다.
> **메뉴 수정(Update)** — 가격이나 이름을 바꿉니다.
> **메뉴 삭제(Delete)** — 단종된 메뉴를 없앱니다.
> 이 4가지가 모든 데이터 중심 API의 기본입니다.

<a id="part1"></a>

## 1️⃣ 프로젝트 구조 [↑](#toc)

이번 장에서는 **단일 `main.py` 파일**에 Pydantic 모델과 인메모리 리스트를 사용한 완전한 CRUD API를 만듭니다. 이것이 **1단계 전략**입니다.

### 파일 구조

```
my-fastapi/
├── main.py          ← 모든 코드가 여기에
└── .venv/
```

### 데이터 저장 방식

```python
# 데이터베이스 대신 Python 리스트를 사용합니다
# 서버가 실행되는 동안만 데이터가 유지됩니다
items: list[dict] = []
next_id: int = 1  # 자동 증가 ID
```

### Pydantic 모델 설계

```python
from pydantic import BaseModel, Field


# 생성/수정 요청을 받는 모델
class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="아이템 이름")
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(ge=0, description="가격 (0 이상)")
    is_available: bool = True


# 응답으로 내보내는 모델 (id 포함)
class ItemPublic(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    is_available: bool
```

`ItemCreate` — 클라이언트가 보내는 데이터. `id`는 서버에서 자동 부여하므로 포함하지 않습니다.
`ItemPublic` — 서버가 응답으로 돌려주는 데이터. `id`가 포함됩니다.

---

<a id="part2"></a>

## 2️⃣ Create (POST) [↑](#toc)

> "새 메뉴가 들어왔습니다. 등록하겠습니다."
> POST 요청으로 새 아이템을 리스트에 추가합니다.

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

# 인메모리 저장소
items: list[dict] = []
next_id: int = 1


@app.post("/items", response_model=ItemPublic, status_code=status.HTTP_201_CREATED)
def create_item(item_data: ItemCreate):
    global next_id  # 전역 변수 수정

    # 새 아이템 딕셔너리 생성
    new_item = {
        "id": next_id,
        **item_data.model_dump(),  # ItemCreate의 모든 필드를 펼칩니다
    }

    items.append(new_item)
    next_id += 1

    return new_item  # response_model=ItemPublic이 필터링합니다
```

### 테스트

```
POST /items
{
  "name": "아메리카노",
  "description": "진한 에스프레소 커피",
  "price": 4500.0,
  "is_available": true
}
```

응답:
```json
HTTP 201 Created
{
  "id": 1,
  "name": "아메리카노",
  "description": "진한 에스프레소 커피",
  "price": 4500.0,
  "is_available": true
}
```

두 번 더 실행하면 `id`가 2, 3으로 자동 증가합니다.

---

<a id="part3"></a>

## 3️⃣ Read (GET) [↑](#toc)

> "메뉴 전체 보여주세요" + "3번 메뉴만 보여주세요"
> Read는 두 가지입니다: 전체 목록과 단건 조회.

### 전체 목록 조회

```python
@app.get("/items", response_model=list[ItemPublic])
def get_items(
    skip: int = 0,
    limit: int = 10,
    available_only: bool = False,
):
    result = items  # 전체 리스트

    # 판매 가능 필터 (Query 파라미터)
    if available_only:
        result = [item for item in result if item["is_available"]]

    # 페이지네이션
    return result[skip : skip + limit]
```

테스트:
```
GET /items              → 전체 목록 (최대 10개)
GET /items?limit=3      → 최대 3개
GET /items?skip=2       → 2번째부터
GET /items?available_only=true → 판매 가능한 것만
```

### 단건 조회 — 없으면 404

```python
@app.get("/items/{item_id}", response_model=ItemPublic)
def get_item(item_id: int):
    # 리스트에서 id가 일치하는 아이템 찾기
    found = next((item for item in items if item["id"] == item_id), None)

    if found is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {item_id}에 해당하는 아이템을 찾을 수 없습니다",
        )

    return found
```

테스트:
```
GET /items/1  → 1번 아이템 (존재하면 200, 없으면 404)
GET /items/99 → 404 Not Found
```

### next() + 제너레이터 — Python 관용 패턴

```python
# 리스트에서 조건을 만족하는 첫 번째 항목 찾기
found = next((item for item in items if item["id"] == item_id), None)
# ↑ 없으면 None 반환 (두 번째 인자가 기본값)

# 같은 코드를 for문으로 쓰면:
found = None
for item in items:
    if item["id"] == item_id:
        found = item
        break
```

---

<a id="part4"></a>

## 4️⃣ Update (PUT) [↑](#toc)

> "3번 메뉴를 완전히 새 내용으로 교체합니다."
> PUT은 리소스 전체를 교체합니다.

```python
@app.put("/items/{item_id}", response_model=ItemPublic)
def update_item(item_id: int, item_data: ItemCreate):
    # 대상 아이템 찾기
    for index, item in enumerate(items):
        if item["id"] == item_id:
            # 기존 아이템을 새 데이터로 완전 교체 (id는 유지)
            updated_item = {
                "id": item_id,
                **item_data.model_dump(),
            }
            items[index] = updated_item
            return updated_item

    # 찾지 못한 경우
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"ID {item_id}에 해당하는 아이템을 찾을 수 없습니다",
    )
```

테스트:
```
PUT /items/1
{
  "name": "아이스 아메리카노",
  "description": "차갑게 즐기는 아메리카노",
  "price": 5000.0,
  "is_available": true
}
```

응답:
```json
HTTP 200 OK
{
  "id": 1,
  "name": "아이스 아메리카노",
  "description": "차갑게 즐기는 아메리카노",
  "price": 5000.0,
  "is_available": true
}
```

### PUT vs PATCH

| 메서드 | 동작 | 요청 바디 |
|--------|------|---------|
| **PUT** | 리소스 **전체 교체** | 모든 필드 필요 |
| **PATCH** | 리소스 **일부 수정** | 바꿀 필드만 포함 |

이 과정에서는 PUT(전체 교체)만 다룹니다. PATCH 패턴은 7장에서 다룹니다.

---

<a id="part5"></a>

## 5️⃣ Delete (DELETE) [↑](#toc)

> "이 메뉴는 없애겠습니다."
> DELETE 성공 시 돌려줄 데이터가 없으므로 **204 No Content**를 반환합니다.

```python
from fastapi import Response


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    # 삭제할 아이템 찾기
    for index, item in enumerate(items):
        if item["id"] == item_id:
            items.pop(index)
            return None  # 204는 본문이 없어야 합니다

    # 찾지 못한 경우
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"ID {item_id}에 해당하는 아이템을 찾을 수 없습니다",
    )
```

테스트:
```
DELETE /items/1  → 204 No Content (본문 없음)
DELETE /items/99 → 404 Not Found
```

204 응답에는 응답 바디가 없습니다. Swagger UI에서 실행하면 Response body가 비어있는 것을 확인할 수 있습니다.

---

<a id="part6"></a>

## 6️⃣ 전체 코드 [↑](#toc)

지금까지 작성한 코드를 하나의 완성된 파일로 정리합니다.

```python
# main.py — 완전한 인메모리 CRUD API
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="메뉴 관리 API",
    description="FastAPI 인메모리 CRUD 예제",
    version="1.0.0",
)

# ── 모델 ──────────────────────────────────────────────

class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="아이템 이름")
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(ge=0, description="가격 (0 이상)")
    is_available: bool = True


class ItemPublic(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    is_available: bool


# ── 인메모리 저장소 ───────────────────────────────────

items: list[dict] = []
next_id: int = 1


# ── 헬퍼 함수 ─────────────────────────────────────────

def find_item(item_id: int) -> dict:
    """ID로 아이템을 찾습니다. 없으면 404를 발생시킵니다."""
    found = next((item for item in items if item["id"] == item_id), None)
    if found is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {item_id}에 해당하는 아이템을 찾을 수 없습니다",
        )
    return found


# ── 엔드포인트 ────────────────────────────────────────

@app.post("/items", response_model=ItemPublic, status_code=status.HTTP_201_CREATED,
          summary="아이템 생성", tags=["items"])
def create_item(item_data: ItemCreate):
    """새 아이템을 생성합니다."""
    global next_id
    new_item = {"id": next_id, **item_data.model_dump()}
    items.append(new_item)
    next_id += 1
    return new_item


@app.get("/items", response_model=list[ItemPublic],
         summary="아이템 목록", tags=["items"])
def get_items(
    skip: int = 0,
    limit: int = 10,
    available_only: bool = False,
):
    """아이템 목록을 조회합니다. 페이지네이션과 필터를 지원합니다."""
    result = items
    if available_only:
        result = [item for item in result if item["is_available"]]
    return result[skip : skip + limit]


@app.get("/items/{item_id}", response_model=ItemPublic,
         summary="아이템 단건 조회", tags=["items"])
def get_item(item_id: int):
    """특정 ID의 아이템을 조회합니다."""
    return find_item(item_id)


@app.put("/items/{item_id}", response_model=ItemPublic,
         summary="아이템 수정", tags=["items"])
def update_item(item_id: int, item_data: ItemCreate):
    """아이템을 전체 교체합니다."""
    for index, item in enumerate(items):
        if item["id"] == item_id:
            updated_item = {"id": item_id, **item_data.model_dump()}
            items[index] = updated_item
            return updated_item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"ID {item_id}에 해당하는 아이템을 찾을 수 없습니다",
    )


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT,
            summary="아이템 삭제", tags=["items"])
def delete_item(item_id: int):
    """아이템을 삭제합니다."""
    for index, item in enumerate(items):
        if item["id"] == item_id:
            items.pop(index)
            return None
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"ID {item_id}에 해당하는 아이템을 찾을 수 없습니다",
    )
```

실행:
```bash
fastapi dev main.py
```

---

<a id="part7"></a>

## 7️⃣ Swagger에서 전체 테스트 [↑](#toc)

**Swagger UI에서 확인해보세요!** `http://localhost:8000/docs`에 접속합니다.

### 테스트 순서

**1단계 — 아이템 생성 (POST /items)**

`POST /items` → "Try it out" → 아래 데이터 입력 → Execute

```json
{
  "name": "아메리카노",
  "description": "진한 에스프레소 커피",
  "price": 4500.0,
  "is_available": true
}
```

응답 코드가 **201**인지 확인합니다.

다시 한 번 실행해서 두 번째 아이템도 추가합니다:

```json
{
  "name": "라떼",
  "price": 5000.0,
  "is_available": true
}
```

**2단계 — 목록 조회 (GET /items)**

`GET /items` → "Try it out" → Execute

두 아이템이 리스트로 나타나는지 확인합니다.

**3단계 — 단건 조회 (GET /items/{item_id})**

`GET /items/{item_id}` → `item_id` = `1` → Execute

1번 아이템만 나타나는지 확인합니다. 그 다음 `99`로 시도하면 404가 나타납니다.

**4단계 — 수정 (PUT /items/{item_id})**

`PUT /items/{item_id}` → `item_id` = `1` → 아래 데이터 입력 → Execute

```json
{
  "name": "아이스 아메리카노",
  "description": "차갑게 즐기는 아메리카노",
  "price": 5000.0,
  "is_available": true
}
```

`GET /items/1`로 다시 조회하면 이름이 바뀐 것을 확인할 수 있습니다.

**5단계 — 삭제 (DELETE /items/{item_id})**

`DELETE /items/{item_id}` → `item_id` = `1` → Execute

응답 코드가 **204**이고 본문이 없는 것을 확인합니다. `GET /items/1`을 다시 시도하면 404가 나타납니다.

---

<a id="part8"></a>

## 8️⃣ 한계: 새로고침하면 사라집니다 [↑](#toc)

> 인메모리 저장소의 근본적인 한계입니다.

현재 우리가 만든 API는 데이터를 **서버의 메모리(RAM)** 에만 저장합니다.

```
서버 실행 중:  items = [{"id": 1, ...}, {"id": 2, ...}]  ✅ 데이터 있음
서버 재시작:   items = []                                  ❌ 데이터 없음
```

### 언제 데이터가 사라지나요?

- `Ctrl+C`로 서버를 종료하면 사라집니다
- 서버가 크래시(충돌)하면 사라집니다
- 코드를 수정하면 자동 재시작되면서 사라집니다 (`fastapi dev` 모드)
- 서버를 여러 인스턴스로 실행하면 각각 다른 데이터를 가집니다

### 그래도 이 단계가 중요한 이유

인메모리 방식은 **API 구조와 로직을 학습**하기에 완벽합니다.

```
인메모리 단계에서 배운 것:
✅ URL 설계 (RESTful 패턴)
✅ HTTP 메서드 활용 (POST, GET, PUT, DELETE)
✅ Pydantic 검증
✅ 상태 코드 응답 (201, 204, 404)
✅ Swagger UI 테스트
```

```
DB 연동 단계에서 추가되는 것:
+ SQLModel 테이블 정의
+ async/await DB 세션
+ SQL 쿼리 실행
+ 영구 데이터 저장
```

DB 연동 후에도 위에서 배운 API 구조는 거의 그대로 사용합니다. **저장소만 바뀔 뿐, 나머지 로직은 동일합니다.**

11장에서 SQLModel로 데이터베이스를 연결하면 영구 저장이 가능해집니다.

---

<a id="part9"></a>

## 9️⃣ 정리 [↑](#toc)

### CRUD와 HTTP 메서드 매핑

| CRUD | HTTP 메서드 | URL 패턴 | 상태 코드 | 식당 비유 |
|------|-----------|---------|---------|----------|
| **C**reate | `POST` | `/items` | 201 | 새 메뉴 등록 |
| **R**ead (목록) | `GET` | `/items` | 200 | 메뉴판 보기 |
| **R**ead (단건) | `GET` | `/items/{id}` | 200 / 404 | 특정 메뉴 확인 |
| **U**pdate | `PUT` | `/items/{id}` | 200 / 404 | 메뉴 정보 변경 |
| **D**elete | `DELETE` | `/items/{id}` | 204 / 404 | 메뉴 삭제 |

### 핵심 패턴 요약

| 패턴 | 코드 | 설명 |
|------|------|------|
| 인메모리 저장소 | `items: list[dict] = []` | Python 리스트로 임시 저장 |
| 자동 ID | `global next_id; next_id += 1` | 단순 증가 방식 |
| 항목 찾기 | `next((x for x in items if x["id"] == id), None)` | 제너레이터 패턴 |
| 404 처리 | `raise HTTPException(404, ...)` | 없으면 즉시 에러 반환 |
| 생성 응답 | `status_code=201` | 새 리소스 생성 알림 |
| 삭제 응답 | `status_code=204, return None` | 빈 바디 응답 |
| 입력/출력 분리 | `ItemCreate` / `ItemPublic` | 용도별 모델 |

---

### 다음 장 미리보기

| 장 | 내용 |
|---|---|
| 7장 | APIRouter — `items.py`, `users.py`로 파일 분리, 코드 구조화 |
| 8장 | 인증 — JWT 토큰, 의존성 주입, 보호된 엔드포인트 |
| 9장 | SQLModel — 데이터베이스 연동, 영구 저장 시작 |

CRUD API를 완성했습니다. 코드가 단일 파일에 모두 들어있어서 지금은 괜찮지만, 엔드포인트가 늘어나면 관리가 어려워집니다. **다음 장에서 APIRouter로 파일을 깔끔하게 분리합니다.**

---

### 실습 과제

**기본**: 위 전체 코드를 직접 타이핑해서 `main.py`를 만들고 실행해보세요. Swagger UI에서 5단계 테스트 순서대로 모든 작업을 직접 해보세요. 특히 존재하지 않는 ID로 각 작업을 시도해서 404 에러를 확인해보세요!

**중급**: 위 API를 확장해서 `GET /items/search` 엔드포인트를 추가하세요. Query 파라미터 `name_contains: str`을 받아서 이름에 해당 문자열이 포함된 아이템만 반환하세요. (예: `?name_contains=카노`이면 "아메리카노", "차이티라테카노" 등이 반환됩니다.) **주의**: `/items/search`를 `/items/{item_id}` 보다 먼저 정의해야 합니다!

**심화**: 현재 `global next_id`를 사용하는 방식은 실제 서비스에서 문제가 생길 수 있습니다. `items` 리스트에 있는 아이템들의 최대 ID를 찾아서 +1하는 방식으로 `create_item`을 리팩터링해보세요. `max(item["id"] for item in items, default=0) + 1` 패턴을 사용하면 됩니다.

{% endraw %}
