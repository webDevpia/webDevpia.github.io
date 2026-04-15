---
title: 04. Pydantic — 데이터 검증
layout: default
grand_parent: Language
parent: FastAPI (리뉴얼)
nav_order: 4
permalink: /language/fastapi-new/pydantic
---

{% raw %}

## 학습 목표

- Pydantic BaseModel로 요청 바디를 정의하고 자동 검증을 활용할 수 있다
- `Field`로 세부 제약 조건(길이, 범위, 패턴)을 설정할 수 있다
- 입력/출력/DB용 다중 모델 패턴을 이해하고 적용할 수 있다

<a id="toc"></a>

## 진행 순서

1. [왜 데이터 검증이 필요한가?](#part1) - 검증 없이 생기는 문제
2. [BaseModel 기초](#part2) - 첫 번째 Pydantic 모델
3. [자동 검증 확인](#part3) - 422 에러 직접 보기
4. [Field 제약](#part4) - 길이, 범위, 패턴 설정
5. [선택적 필드](#part5) - `None`과 기본값
6. [중첩 모델](#part6) - 모델 안의 모델
7. [field_validator](#part7) - 커스텀 검증 로직
8. [model_validator](#part8) - 필드 간 교차 검증
9. [다중 모델 패턴](#part9) - Create / Public / InDB
10. [Swagger에서 스키마 확인](#part10) - 자동 스키마 문서
11. [정리](#part11) - 핵심 개념 요약

---

# 04장. Pydantic — 데이터 검증의 입국 심사관

> Pydantic은 입국 심사관과 같습니다.
> 여권(데이터)을 꼼꼼히 확인하고, 서류가 미비하면 입국을 거부(422 에러)합니다.
> 주방(서버 로직)에는 검증을 통과한 깨끗한 데이터만 들어옵니다.

<a id="part1"></a>

## 1️⃣ 왜 데이터 검증이 필요한가? [↑](#toc)

### 검증 없는 API의 위험

```python
# ❌ 검증 없는 API — 어떤 데이터든 주방으로 들어갑니다
@app.post("/orders")
def create_order(order: dict):
    # 클라이언트가 뭘 보냈는지 모릅니다
    item_name = order["item_name"]   # KeyError 가능
    price = order["price"] * 1.1     # price가 문자열이면 TypeError
    return {"status": "주문 완료", "total": price}
```

클라이언트가 실수로 이런 데이터를 보내면:

```json
{
  "item": "아메리카노",
  "cost": "무료"
}
```

- `order["item_name"]` → `KeyError` (키 이름이 다름)
- `order["price"]` → `KeyError` (이 키도 없음)
- 서버가 500 에러로 충돌합니다

### 검증의 3가지 필요성

1. **타입 안전** — `price`가 반드시 숫자여야 계산이 됩니다
2. **필수 필드 확인** — `item_name`, `price` 없이는 주문이 불완전합니다
3. **비즈니스 규칙** — 가격은 0원 이상이어야 하고, 이름은 1자 이상이어야 합니다

> 주방에 이상한 주문이 들어가면 사고가 납니다.
> 검증은 웨이터(API)가 주방에 전달하기 전에 주문서를 확인하는 과정입니다.

---

<a id="part2"></a>

## 2️⃣ BaseModel 기초 [↑](#toc)

Pydantic의 `BaseModel`을 상속해서 데이터 구조를 정의합니다.

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# 메뉴 아이템 모델 정의
class Item(BaseModel):
    name: str           # 필수 — 문자열
    description: str    # 필수 — 문자열
    price: float        # 필수 — 숫자 (소수점 포함)
    quantity: int       # 필수 — 정수


# POST 엔드포인트 — 요청 바디를 Item 모델로 받습니다
@app.post("/items")
def create_item(item: Item):
    # 여기 도달한 item은 이미 검증 완료된 데이터입니다
    return {
        "message": "아이템 생성 완료",
        "name": item.name,
        "price": item.price,
        "total_value": item.price * item.quantity,
    }
```

### 요청 예시 (올바른 데이터)

```json
POST /items
Content-Type: application/json

{
  "name": "아메리카노",
  "description": "진한 에스프레소 커피",
  "price": 4500.0,
  "quantity": 2
}
```

응답:
```json
{
  "message": "아이템 생성 완료",
  "name": "아메리카노",
  "price": 4500.0,
  "total_value": 9000.0
}
```

### 모델 접근 방법

Pydantic 모델은 속성으로 접근합니다.

```python
# ✅ 속성 접근 (권장)
item.name
item.price
item.quantity

# ✅ 딕셔너리로 변환
item.model_dump()
# → {"name": "아메리카노", "description": "...", "price": 4500.0, "quantity": 2}

# ✅ JSON 문자열로 변환
item.model_dump_json()
```

---

<a id="part3"></a>

## 3️⃣ 자동 검증 확인 [↑](#toc)

> 입국 심사관이 거부했습니다!
> 422 에러를 직접 확인해봅니다.

**Swagger UI에서 확인해보세요!** `/docs`에서 `POST /items`를 열고 잘못된 데이터를 보내봅니다.

### 잘못된 타입 전송

```json
POST /items
{
  "name": "아메리카노",
  "description": "커피",
  "price": "무료",
  "quantity": 2
}
```

응답:
```json
HTTP 422 Unprocessable Entity
{
  "detail": [
    {
      "type": "float_parsing",
      "loc": ["body", "price"],
      "msg": "Input should be a valid number, unable to parse string as a number",
      "input": "무료",
      "url": "https://errors.pydantic.dev/2.x/v/float_parsing"
    }
  ]
}
```

### 필수 필드 누락

```json
POST /items
{
  "name": "아메리카노",
  "price": 4500.0
}
```

응답:
```json
HTTP 422 Unprocessable Entity
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "description"],
      "msg": "Field required",
      "input": {...}
    },
    {
      "type": "missing",
      "loc": ["body", "quantity"],
      "msg": "Field required",
      "input": {...}
    }
  ]
}
```

에러 메시지가 **어느 필드에서**, **무슨 문제가** 발생했는지 정확히 알려줍니다.

---

<a id="part4"></a>

## 4️⃣ Field 제약 [↑](#toc)

> "이름은 50자 이하, 가격은 0원 이상" 같은 비즈니스 규칙을 코드로 표현합니다.

`Field`를 사용하면 기본 타입 검사 이상의 세부 제약을 추가할 수 있습니다.

```python
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(
        min_length=1,       # 최소 1자 이상
        max_length=50,      # 최대 50자 이하
        description="아이템 이름 (1~50자)",
    )
    description: str = Field(
        max_length=500,
        description="상세 설명 (최대 500자)",
    )
    price: float = Field(
        ge=0,               # greater than or equal: 0 이상
        description="가격 (0 이상)",
    )
    quantity: int = Field(
        ge=1,               # 1개 이상
        le=999,             # 999개 이하
        description="수량 (1~999)",
    )
    discount_rate: float = Field(
        default=0.0,
        ge=0.0,             # 0% 이상
        le=1.0,             # 100% 이하 (0.0~1.0 범위)
        description="할인율 (0.0~1.0)",
    )
```

### Field 제약 조건 표

| 제약 | 의미 | 적용 타입 |
|------|------|---------|
| `min_length=N` | 최소 N자 | `str` |
| `max_length=N` | 최대 N자 | `str` |
| `pattern=r"..."` | 정규식 패턴 매칭 | `str` |
| `ge=N` | N 이상 (≥) | `int`, `float` |
| `gt=N` | N 초과 (>) | `int`, `float` |
| `le=N` | N 이하 (≤) | `int`, `float` |
| `lt=N` | N 미만 (<) | `int`, `float` |
| `min_length=N` | 최소 N개 원소 | `list` |
| `max_length=N` | 최대 N개 원소 | `list` |

### 정규식 패턴 예시

```python
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_]+$",  # 영문, 숫자, 밑줄만 허용
        description="사용자명 (3~20자, 영문/숫자/밑줄)",
    )
    phone: str = Field(
        pattern=r"^010-\d{4}-\d{4}$",  # 010-XXXX-XXXX 형식
        description="휴대폰 번호 (010-XXXX-XXXX)",
    )
```

---

<a id="part5"></a>

## 5️⃣ 선택적 필드 [↑](#toc)

모든 필드가 필수일 필요는 없습니다. `None`을 기본값으로 지정하면 선택적 필드가 됩니다.

```python
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(ge=0)

    # 선택적 필드 — 없어도 됩니다
    description: str | None = None
    tags: list[str] | None = None
    image_url: str | None = None

    # 기본값이 있는 선택적 필드
    is_available: bool = True
    discount_rate: float = Field(default=0.0, ge=0.0, le=1.0)
```

테스트 — 최소 데이터만:
```json
POST /items
{
  "name": "아메리카노",
  "price": 4500.0
}
```

응답:
```json
{
  "name": "아메리카노",
  "price": 4500.0,
  "description": null,
  "tags": null,
  "image_url": null,
  "is_available": true,
  "discount_rate": 0.0
}
```

테스트 — 모든 데이터:
```json
POST /items
{
  "name": "아메리카노",
  "price": 4500.0,
  "description": "진한 에스프레소 커피",
  "tags": ["커피", "음료", "인기"],
  "is_available": true,
  "discount_rate": 0.1
}
```

---

<a id="part6"></a>

## 6️⃣ 중첩 모델 [↑](#toc)

> 주문서(Order) 안에 메뉴 아이템(Item) 목록이 들어있는 구조입니다.

Pydantic 모델을 다른 모델 안에서 사용할 수 있습니다.

```python
from pydantic import BaseModel, Field


class Item(BaseModel):
    menu_id: int
    name: str
    price: float = Field(ge=0)
    quantity: int = Field(ge=1, le=99)


class Address(BaseModel):
    street: str
    city: str
    postal_code: str = Field(pattern=r"^\d{5}$")  # 5자리 우편번호


class Order(BaseModel):
    table_number: int = Field(ge=1, le=50)
    items: list[Item]            # Item 모델의 리스트
    delivery_address: Address | None = None  # 배달 주소 (선택)
    note: str | None = None      # 요청사항 (선택)
```

테스트:
```json
POST /orders
{
  "table_number": 5,
  "items": [
    {"menu_id": 1, "name": "아메리카노", "price": 4500, "quantity": 2},
    {"menu_id": 3, "name": "치즈케이크", "price": 7500, "quantity": 1}
  ],
  "note": "설탕 빼주세요"
}
```

Pydantic이 자동으로 검증합니다:
- `items` 배열 안의 각 `Item`도 검증
- `table_number`가 1~50 범위인지 확인
- 중첩된 모델의 모든 필드를 재귀적으로 검증

---

<a id="part7"></a>

## 7️⃣ field_validator — 커스텀 검증 [↑](#toc)

`Field`의 기본 제약으로는 표현할 수 없는 복잡한 검증 로직을 작성할 수 있습니다.

```python
from pydantic import BaseModel, Field, field_validator


class Item(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(ge=0)
    tags: list[str] = []

    @field_validator("name")
    @classmethod
    def name_must_not_be_whitespace(cls, v: str) -> str:
        # 공백만 있는 이름은 거부합니다
        if v.strip() == "":
            raise ValueError("이름은 공백만 포함할 수 없습니다")
        return v.strip()  # 앞뒤 공백 제거 후 반환

    @field_validator("tags")
    @classmethod
    def tags_must_be_unique(cls, v: list[str]) -> list[str]:
        # 중복 태그 제거
        unique_tags = list(set(v))
        if len(unique_tags) != len(v):
            # 중복이 있었다면 경고 대신 중복 제거 후 반환
            return unique_tags
        return v

    @field_validator("price")
    @classmethod
    def price_must_be_sensible(cls, v: float) -> float:
        # 비즈니스 규칙: 가격은 1,000,000원 이하
        if v > 1_000_000:
            raise ValueError("가격은 1,000,000원을 초과할 수 없습니다")
        return round(v, 2)  # 소수점 2자리로 반올림
```

### Pydantic v2 — `@field_validator` 주의사항

```python
# ✅ Pydantic v2 방식
@field_validator("name")
@classmethod
def validate_name(cls, v: str) -> str:
    ...
    return v


# ❌ Pydantic v1 방식 (v2에서 deprecated)
@validator("name")
def validate_name(cls, v):
    ...
```

이 과정에서는 Pydantic v2를 사용합니다. `@field_validator`와 `@classmethod`를 함께 씁니다.

---

<a id="part8"></a>

## 8️⃣ model_validator — 필드 간 교차 검증 [↑](#toc)

두 필드를 비교하는 검증은 `model_validator`를 사용합니다.

```python
from pydantic import BaseModel, Field, model_validator


class PriceRange(BaseModel):
    min_price: float = Field(ge=0)
    max_price: float = Field(ge=0)

    @model_validator(mode="after")
    def max_must_be_greater_than_min(self) -> "PriceRange":
        # min_price가 max_price보다 크면 에러
        if self.min_price > self.max_price:
            raise ValueError(
                f"최소 가격({self.min_price})은 최대 가격({self.max_price})보다 클 수 없습니다"
            )
        return self


class SaleItem(BaseModel):
    original_price: float = Field(ge=0)
    sale_price: float = Field(ge=0)
    sale_start: str  # "YYYY-MM-DD"
    sale_end: str    # "YYYY-MM-DD"

    @model_validator(mode="after")
    def validate_sale_logic(self) -> "SaleItem":
        # 할인가는 원가보다 낮아야 합니다
        if self.sale_price >= self.original_price:
            raise ValueError("할인가는 원가보다 낮아야 합니다")
        return self
```

테스트:
```json
POST /price-range
{
  "min_price": 10000,
  "max_price": 5000
}
```

응답:
```json
HTTP 422 Unprocessable Entity
{
  "detail": [
    {
      "type": "value_error",
      "msg": "Value error, 최소 가격(10000.0)은 최대 가격(5000.0)보다 클 수 없습니다"
    }
  ]
}
```

---

<a id="part9"></a>

## 9️⃣ 다중 모델 패턴 [↑](#toc)

> "왜 모델이 3개나 필요하죠?"

실제 API에서는 하나의 리소스에 여러 모델을 사용합니다. 각 상황마다 필요한 필드가 다르기 때문입니다.

### 문제 — 하나의 모델로 모든 것을 처리하면

```python
# ❌ 비밀번호가 응답에 노출될 수 있습니다
class User(BaseModel):
    id: int
    username: str
    email: str
    password: str   # 절대 응답으로 보내면 안 됩니다!
    created_at: str

@app.post("/users")
def create_user(user: User):
    # user.password를 해싱해서 저장...
    return user  # ❌ password가 그대로 응답에 포함됩니다
```

### 해결 — 용도별로 모델을 분리합니다

```python
from pydantic import BaseModel, Field, EmailStr


# 1. 입력 모델 — 클라이언트가 보내는 데이터
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr                     # 이메일 형식 자동 검증
    password: str = Field(min_length=8) # 비밀번호 받기


# 2. 출력 모델 — 클라이언트에게 돌려주는 데이터
class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    # password 없음! — 절대 외부로 노출하지 않습니다


# 3. DB 모델 — 데이터베이스에 저장하는 데이터 (다음 파트에서 SQLModel로 다룸)
class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str  # 해싱된 비밀번호
    is_active: bool = True
    created_at: str
```

### 엔드포인트에서 사용

```python
@app.post("/users", response_model=UserPublic)
def create_user(user_data: UserCreate):
    # 1. 입력 검증은 UserCreate가 담당 (자동)
    # 2. 비밀번호 해싱
    hashed = f"hashed_{user_data.password}"  # 실제는 bcrypt 사용

    # 3. DB에 저장 (지금은 시뮬레이션)
    new_user = UserInDB(
        id=1,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed,
        created_at="2026-04-10",
    )

    # 4. UserPublic으로 반환 — password 필드 없음
    return UserPublic(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
    )
```

응답 (비밀번호 없음):
```json
{
  "id": 1,
  "username": "홍길동",
  "email": "gildong@example.com"
}
```

### 3가지 모델 패턴 요약

| 모델 이름 | 용도 | 포함하는 것 | 제외하는 것 |
|----------|------|-----------|-----------|
| `ItemCreate` | 생성 요청 받기 | 사용자 입력 필드 | id, created_at |
| `ItemPublic` | 응답으로 내보내기 | 공개 가능한 필드 | password, 내부 필드 |
| `ItemInDB` | DB 저장용 | 모든 필드 포함 | (모두 포함) |

---

<a id="part10"></a>

## 🔟 Swagger에서 스키마 확인 [↑](#toc)

**Swagger UI에서 확인해보세요!** Pydantic 모델은 `/docs` 하단의 **Schemas** 섹션에 자동으로 문서화됩니다.

`main.py`에 아래 코드를 작성하고 `/docs`를 열어보세요.

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="아이템 이름")
    price: float = Field(ge=0, description="가격 (0 이상)")
    description: str | None = Field(default=None, description="상세 설명")


class ItemPublic(BaseModel):
    id: int
    name: str
    price: float
    description: str | None


@app.post("/items", response_model=ItemPublic, status_code=201)
def create_item(item: ItemCreate):
    return ItemPublic(id=1, **item.model_dump())
```

`/docs`에서 확인할 것들:
- `POST /items` 엔드포인트의 **Request body** 섹션: `ItemCreate` 스키마
- **Response** 섹션: `ItemPublic` 스키마
- 페이지 하단 **Schemas** 섹션: 모든 모델의 전체 구조

각 필드의 `description`, `minimum`, `maxLength` 등이 자동으로 문서에 표시됩니다.

---

<a id="part11"></a>

## 1️⃣1️⃣ 정리 [↑](#toc)

### 핵심 개념 요약

| 개념 | 코드 | 설명 |
|------|------|------|
| BaseModel | `class Item(BaseModel)` | 데이터 구조 정의 |
| 필수 필드 | `name: str` | 기본값 없음 → 필수 |
| 선택적 필드 | `name: str \| None = None` | None이 기본값 |
| Field 제약 | `Field(ge=0, le=100)` | 세부 제약 설정 |
| field_validator | `@field_validator("name")` | 단일 필드 커스텀 검증 |
| model_validator | `@model_validator(mode="after")` | 필드 간 교차 검증 |
| 자동 422 에러 | FastAPI + Pydantic 내장 | 검증 실패 시 자동 응답 |
| 다중 모델 패턴 | Create / Public / InDB | 용도별 모델 분리 |
| model_dump() | `item.model_dump()` | 모델 → 딕셔너리 변환 |

---

### 다음 장 미리보기

| 장 | 내용 |
|---|---|
| 5장 | Response와 상태 코드 — response_model로 출력 제어, status.HTTP_201_CREATED |
| 6장 | CRUD 완성 — 인메모리로 전체 Create/Read/Update/Delete 구현 |
| 7장 | APIRouter — 파일 구조 분리, 모듈화 |

Pydantic으로 데이터 검증을 자동화하는 방법을 익혔습니다. 다음 장에서는 응답(Response)을 더 세밀하게 제어하는 방법을 배웁니다.

---

### 실습 과제

**기본**: `BlogPost`라는 Pydantic 모델을 만드세요. 필드: `title` (필수, 1~100자), `content` (필수, 최소 10자), `author` (필수), `tags` (선택, 문자열 리스트). `POST /posts` 엔드포인트에서 이 모델을 받아서 그대로 반환하세요. Swagger UI에서 올바른 데이터와 잘못된 데이터를 각각 보내서 응답을 확인해보세요!

**중급**: `UserCreate` 모델에 `@field_validator`를 추가하세요: 비밀번호는 최소 8자이고, 최소 하나의 숫자를 포함해야 합니다. 검증 실패 시 명확한 한국어 에러 메시지를 반환하세요.

**심화**: `PasswordChange` 모델을 만드세요. `current_password`, `new_password`, `new_password_confirm` 3개 필드를 가지며, `@model_validator`를 사용해서 `new_password`와 `new_password_confirm`이 일치하는지 검증하세요. 또한 `new_password`가 `current_password`와 달라야 한다는 조건도 추가하세요.

{% endraw %}
