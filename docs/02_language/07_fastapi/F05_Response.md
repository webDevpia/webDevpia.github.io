---
title: 05. Response와 상태 코드
layout: default
grand_parent: Language
parent: FastAPI
nav_order: 5
permalink: /language/fastapi/response
---

{% raw %}

## 학습 목표

- HTTP 상태 코드의 의미를 이해하고 올바른 상황에 적용할 수 있다
- `response_model`로 응답 데이터를 필터링하고 문서화할 수 있다
- `HTTPException`으로 의미있는 에러 응답을 반환할 수 있다

<a id="toc"></a>

## 진행 순서

1. [상태 코드란?](#part1) - 식당 답변 시스템
2. [response_model](#part2) - 응답 데이터 필터링
3. [status_code 지정](#part3) - 201, 204 응답
4. [HTTPException](#part4) - 의미있는 에러 응답
5. [JSONResponse](#part5) - 커스텀 응답
6. [Response Headers / Cookies](#part6) - 헤더와 쿠키
7. [정리](#part7) - 핵심 개념 요약

---

# 05장. Response와 상태 코드

> 식당에서 주문에 대한 답변도 여러 종류가 있습니다.
> "주문 완료됐습니다(200)", "새 메뉴 등록됐습니다(201)", "그 메뉴는 없습니다(404)", "주문서가 잘못됐습니다(422)".
> HTTP 상태 코드는 서버가 클라이언트에게 보내는 **표준 답변 코드**입니다.

<a id="part1"></a>

## 1️⃣ 상태 코드란? [↑](#toc)

모든 HTTP 응답에는 **3자리 숫자 상태 코드**가 포함됩니다. 이 코드로 요청이 성공했는지, 실패했는지, 어떤 종류의 결과인지를 전달합니다.

### 상태 코드 그룹

| 범위 | 의미 | 식당 비유 |
|------|------|----------|
| **2xx** | 성공 | "처리됐습니다!" |
| **3xx** | 리다이렉션 | "저쪽으로 가보세요" |
| **4xx** | 클라이언트 에러 | "손님 쪽 문제입니다" |
| **5xx** | 서버 에러 | "저희 주방 문제입니다" |

### 자주 사용하는 상태 코드

| 코드 | 이름 | 의미 | 식당 비유 |
|------|------|------|----------|
| **200** | OK | 요청 성공, 데이터 반환 | "주문 받았습니다, 음식 나왔습니다" |
| **201** | Created | 새 리소스 생성 성공 | "새 메뉴 등록됐습니다" |
| **204** | No Content | 성공, 반환 데이터 없음 | "주문 취소됐습니다 (영수증 없음)" |
| **400** | Bad Request | 잘못된 요청 형식 | "주문서 형식이 잘못됐습니다" |
| **401** | Unauthorized | 인증 필요 | "회원만 주문할 수 있습니다, 로그인하세요" |
| **403** | Forbidden | 권한 없음 | "VIP 전용 메뉴입니다" |
| **404** | Not Found | 리소스 없음 | "그 메뉴는 없습니다" |
| **422** | Unprocessable Entity | 데이터 검증 실패 | "주문서를 이해할 수 없습니다" |
| **500** | Internal Server Error | 서버 내부 오류 | "주방에서 사고가 났습니다" |

### FastAPI의 기본 상태 코드

별도로 지정하지 않으면 FastAPI는 성공 시 **200**을 반환합니다. 단, 이것이 항상 올바른 것은 아닙니다.

```python
# 이 엔드포인트는 새 아이템을 만들지만 기본으로 200을 반환합니다
# ⚠️ 생성 응답은 201이 더 의미있습니다
@app.post("/items")
def create_item(item: ItemCreate):
    return {"id": 1, **item.model_dump()}
```

---

<a id="part2"></a>

## 2️⃣ response_model [↑](#toc)

> "응답에서 비밀번호 같은 민감 정보를 자동으로 제거합니다."
> `response_model`을 지정하면 FastAPI가 응답 데이터를 해당 모델로 **필터링**합니다.

### 기본 사용법

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8)


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    # password 필드 없음 — 외부에 노출하지 않습니다


@app.post("/users", response_model=UserPublic, status_code=201)
def create_user(user_data: UserCreate):
    # 내부적으로 password를 해싱해서 저장한다고 가정
    # 반환값에 password가 있어도 response_model이 걸러냅니다
    return {
        "id": 1,
        "username": user_data.username,
        "email": user_data.email,
        "password": user_data.password,  # ← 이것은 응답에서 제거됩니다
        "hashed_password": "bcrypt_...",  # ← 이것도 제거됩니다
    }
```

응답 (password 없음):
```json
HTTP 201 Created
{
  "id": 1,
  "username": "홍길동",
  "email": "gildong@example.com"
}
```

`response_model=UserPublic`이 설정되어 있으므로, 함수가 `password`를 포함한 딕셔너리를 반환해도 응답에는 `UserPublic`에 정의된 필드만 포함됩니다.

### response_model의 두 가지 역할

1. **데이터 필터링** — 모델에 없는 필드를 응답에서 제거
2. **문서화** — Swagger UI의 응답 스키마 자동 생성

**Swagger UI에서 확인해보세요!** `/docs`에서 `POST /users`를 열면 응답 스키마가 `UserPublic` 구조로 표시됩니다.

### 리스트 응답

```python
@app.get("/users", response_model=list[UserPublic])
def get_users():
    # 실제로는 DB에서 가져오지만, 지금은 시뮬레이션
    users = [
        {"id": 1, "username": "홍길동", "email": "a@test.com", "password": "secret"},
        {"id": 2, "username": "이영희", "email": "b@test.com", "password": "secret"},
    ]
    return users  # password는 응답에서 자동 제거
```

### response_model_exclude_none

`None` 값인 필드를 응답에서 제외할 수 있습니다.

```python
class ItemPublic(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None  # 없을 수도 있는 필드


@app.get("/items/{item_id}", response_model=ItemPublic, response_model_exclude_none=True)
def get_item(item_id: int):
    return {"id": item_id, "name": "커피", "price": 4500.0, "description": None}
```

응답 (`description: null` 제거됨):
```json
{
  "id": 1,
  "name": "커피",
  "price": 4500.0
}
```

---

<a id="part3"></a>

## 3️⃣ status_code 지정 [↑](#toc)

### 명명된 상수 사용 (권장)

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


# ✅ status 모듈의 상수 사용 — 숫자보다 의미가 명확합니다
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return {"id": 1, **item.model_dump()}


# ✅ 숫자로 직접 지정도 가능
@app.post("/orders", status_code=201)
def create_order(order: dict):
    return order
```

### 자주 사용하는 status 상수

```python
from fastapi import status

status.HTTP_200_OK            # 200 — 일반 성공
status.HTTP_201_CREATED       # 201 — 생성 성공
status.HTTP_204_NO_CONTENT    # 204 — 성공, 내용 없음
status.HTTP_400_BAD_REQUEST   # 400 — 잘못된 요청
status.HTTP_401_UNAUTHORIZED  # 401 — 인증 필요
status.HTTP_403_FORBIDDEN     # 403 — 권한 없음
status.HTTP_404_NOT_FOUND     # 404 — 찾을 수 없음
status.HTTP_422_UNPROCESSABLE_ENTITY  # 422 — 검증 실패
status.HTTP_500_INTERNAL_SERVER_ERROR # 500 — 서버 에러
```

### 204 No Content — DELETE 응답

```python
from fastapi import FastAPI, Response, status

app = FastAPI()


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    # 아이템 삭제 처리...
    # 204 응답은 본문이 없어야 합니다 — return 없음
    return None  # 또는 Response(status_code=204)
```

204는 응답 본문이 없어야 합니다. FastAPI는 `None`을 반환하면 자동으로 빈 본문으로 처리합니다.

---

<a id="part4"></a>

## 4️⃣ HTTPException — 의미있는 에러 응답 [↑](#toc)

> "그 메뉴는 없습니다" — 단순히 오류가 아니라 이유를 설명해야 합니다.
> `HTTPException`으로 상태 코드와 에러 메시지를 함께 전달합니다.

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# 인메모리 데이터 저장소
fake_db: dict[int, dict] = {
    1: {"id": 1, "name": "아메리카노", "price": 4500},
    2: {"id": 2, "name": "라떼", "price": 5000},
}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    # 아이템이 없으면 404 반환
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {item_id}에 해당하는 아이템을 찾을 수 없습니다",
        )
    return fake_db[item_id]
```

테스트:
```
GET /items/1  → 200 OK, {"id": 1, "name": "아메리카노", "price": 4500}
GET /items/99 → 404 Not Found, {"detail": "ID 99에 해당하는 아이템을 찾을 수 없습니다"}
```

### 다양한 HTTPException 사례

```python
@app.get("/admin/dashboard")
def admin_dashboard(token: str | None = None):
    if token is None:
        # 인증 토큰 없음 → 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인이 필요합니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if token != "super-secret-admin-token":
        # 잘못된 토큰 → 403
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 없습니다",
        )

    return {"message": "관리자 대시보드"}
```

### detail에 구조화된 데이터 넣기

```python
@app.post("/orders")
def create_order(order: dict):
    if "item_id" not in order:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "missing_field",
                "field": "item_id",
                "message": "item_id 필드가 필요합니다",
            },
        )
    return order
```

응답:
```json
HTTP 400 Bad Request
{
  "detail": {
    "error": "missing_field",
    "field": "item_id",
    "message": "item_id 필드가 필요합니다"
  }
}
```

---

<a id="part5"></a>

## 5️⃣ JSONResponse [↑](#toc)

대부분의 경우 딕셔너리를 반환하면 FastAPI가 자동으로 JSON 응답을 만듭니다. 하지만 상태 코드나 헤더를 세밀하게 제어하고 싶을 때는 `JSONResponse`를 직접 사용합니다.

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in [1, 2, 3]:
        # 커스텀 응답 — 상태 코드와 본문을 직접 제어
        return JSONResponse(
            status_code=404,
            content={"error": "not_found", "id": item_id},
        )

    return {"id": item_id, "name": f"{item_id}번 아이템"}
```

### JSONResponse vs HTTPException

| | `HTTPException` | `JSONResponse` |
|---|-----------------|----------------|
| **사용 시점** | 에러 상황 | 에러 + 성공 모두 |
| **코드 간결성** | `raise`로 간단 | 명시적 반환 필요 |
| **미들웨어 처리** | 에러 핸들러 통과 | 직접 반환 |
| **권장 상황** | 4xx, 5xx 에러 | 커스텀 헤더가 필요한 경우 |

일반적인 에러 응답은 `HTTPException`을 사용하고, 특별한 헤더가 필요하거나 응답 구조를 완전히 제어하고 싶을 때만 `JSONResponse`를 사용합니다.

---

<a id="part6"></a>

## 6️⃣ Response Headers / Cookies [↑](#toc)

### 커스텀 응답 헤더

```python
from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/items/{item_id}")
def get_item(item_id: int, response: Response):
    # Response 객체를 인자로 받으면 헤더를 설정할 수 있습니다
    response.headers["X-Item-ID"] = str(item_id)
    response.headers["X-Processed-By"] = "FastAPI"
    return {"id": item_id, "name": "아이템"}
```

### 쿠키 설정

```python
@app.post("/login")
def login(response: Response):
    # 로그인 성공 시 쿠키에 세션 토큰 저장
    response.set_cookie(
        key="session_token",
        value="some-secret-token",
        httponly=True,   # JavaScript에서 접근 불가
        secure=True,     # HTTPS에서만 전송
        max_age=3600,    # 1시간 유효
    )
    return {"message": "로그인 성공"}
```

쿠키와 JWT 인증은 8장에서 자세히 다룹니다. 지금은 이런 기능이 있다는 것만 알아두세요.

---

<a id="part7"></a>

## 7️⃣ 정리 [↑](#toc)

### 핵심 개념 요약

| 개념 | 코드 | 설명 |
|------|------|------|
| 상태 코드 지정 | `status_code=201` | 응답 코드 직접 설정 |
| status 상수 | `status.HTTP_201_CREATED` | 숫자 대신 의미있는 이름 |
| response_model | `response_model=UserPublic` | 응답 필터링 + 문서화 |
| exclude_none | `response_model_exclude_none=True` | None 필드 응답에서 제거 |
| HTTPException | `raise HTTPException(404, "...")` | 에러 상황에서 적절한 응답 |
| JSONResponse | `return JSONResponse(status_code=...)` | 완전한 응답 제어 |
| 응답 헤더 | `response.headers["X-..."] = "..."` | 커스텀 헤더 추가 |
| 쿠키 | `response.set_cookie(...)` | 클라이언트에 쿠키 설정 |

### 상황별 상태 코드 정리

| API 동작 | 권장 상태 코드 |
|---------|--------------|
| 데이터 조회 성공 | 200 OK |
| 새 리소스 생성 성공 | 201 Created |
| 수정/삭제 성공 (데이터 반환 없음) | 204 No Content |
| 잘못된 요청 형식 | 400 Bad Request |
| 로그인 필요 | 401 Unauthorized |
| 권한 없음 | 403 Forbidden |
| 리소스 없음 | 404 Not Found |
| 데이터 검증 실패 | 422 Unprocessable Entity |
| 서버 내부 오류 | 500 Internal Server Error |

---

### 다음 장 미리보기

| 장 | 내용 |
|---|---|
| 6장 | CRUD 완성 — 인메모리 리스트로 Create, Read, Update, Delete 전체 구현 |
| 7장 | APIRouter — 엔드포인트를 파일별로 분리하는 구조화 |
| 8장 | 인증 — JWT 토큰, OAuth2 |

지금까지 배운 내용을 합칩니다. 다음 장에서는 파라미터 + Pydantic + 상태 코드를 모두 활용한 **완전한 CRUD API**를 만듭니다.

---

### 실습 과제

**기본**: `GET /items/{item_id}` 엔드포인트를 만드세요. `item_id`가 1~5가 아니면 `HTTPException`으로 404 에러와 함께 `"ID {item_id}에 해당하는 아이템이 없습니다"` 메시지를 반환하세요. Swagger UI에서 1번과 99번을 각각 요청해서 차이를 확인해보세요!

**중급**: `POST /items` 엔드포인트를 만드세요. 요청 바디로 `ItemCreate` 모델을 받고, 응답 모델로 `ItemPublic`을 사용하세요. `ItemCreate`에는 `name`, `price`, `secret_code` 필드가 있고, `ItemPublic`에는 `id`, `name`, `price`만 있어야 합니다. `response_model=ItemPublic`을 설정하면 `secret_code`가 응답에서 사라지는지 확인해보세요.

**심화**: 커스텀 에러 핸들러를 만들어보세요. `from fastapi import Request`와 `from fastapi.responses import JSONResponse`를 활용하고, `@app.exception_handler(HTTPException)` 데코레이터를 사용해서 모든 HTTPException이 `{"success": false, "error": {"code": 상태코드, "message": 에러메시지}}` 형태로 응답하도록 만드세요.

{% endraw %}
