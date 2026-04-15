---
title: 01. FastAPI란?
layout: default
grand_parent: Language
parent: FastAPI
nav_order: 1
permalink: /language/fastapi/intro
---

{% raw %}

## 학습 목표

- 웹 API가 무엇인지 식당 비유로 설명할 수 있다
- HTTP 메서드(GET, POST, PUT, DELETE)의 역할을 구분할 수 있다
- FastAPI를 선택하는 이유 3가지를 말할 수 있다

<a id="toc"></a>

## 진행 순서

1. [웹 API란?](#part1) - 식당 비유로 이해하는 API
2. [HTTP 메서드](#part2) - GET, POST, PUT, DELETE의 역할
3. [JSON — 주문서 양식](#part3) - API가 사용하는 데이터 형식
4. [왜 FastAPI인가?](#part4) - 성능, 자동 문서화, 타입 안전성
5. [FastAPI의 3대 장점](#part5) - Swagger, Pydantic, 비동기
6. [정리](#part6) - 핵심 개념 요약

---

# 01장. FastAPI란? — 웹 API와 식당 비유

<a id="part1"></a>

## 1️⃣ 웹 API란? [↑](#toc)

> 손님이 웨이터에게 주문하면, 웨이터가 주방에 전달하고, 주방에서 요리를 만들어 가져다줍니다.
> 웹 API도 똑같습니다. 클라이언트(손님)가 API(웨이터)에게 요청하면, 서버(주방)가 처리하고 결과를 돌려줍니다.

### 식당 비유로 이해하기

카페를 생각해보세요. 손님은 메뉴판을 보고 웨이터에게 주문합니다. 웨이터는 주방에 주문을 전달하고, 바리스타가 커피를 만들어 웨이터가 손님에게 가져다줍니다. 손님은 커피가 어떻게 만들어지는지 몰라도 됩니다. 그냥 주문하면 됩니다.

| 식당 | 웹 API |
|------|--------|
| 손님 | 클라이언트 (브라우저, 앱, 다른 서버) |
| 웨이터 | API (요청을 받고 응답을 전달하는 인터페이스) |
| 주방 | 서버 (실제 로직이 실행되는 곳) |
| 주문 | HTTP 요청 (Request) |
| 음식 | HTTP 응답 (Response) |
| 주문서 | JSON 데이터 |
| 주문 번호 | URL (어떤 메뉴인지 지정) |

### 실생활 속 API

우리는 이미 매일 API를 사용합니다.

- **카카오맵 길 찾기** — 앱(손님)이 카카오 서버(주방)에 "서울역에서 강남역 가는 길"을 요청하면, 서버가 경로를 계산해서 돌려줍니다
- **날씨 앱** — 앱이 기상청 API에 "오늘 서울 날씨"를 요청하면, 기상 데이터를 응답으로 받습니다
- **결제** — 쇼핑몰이 결제 API에 "이 카드로 10,000원 결제"를 요청하면, 결제 결과를 돌려받습니다

이 모든 상황에서 클라이언트는 **서버 내부가 어떻게 동작하는지 알 필요가 없습니다**. API라는 창구에 정해진 형식으로 요청하면 됩니다.

### API vs 웹사이트의 차이

| | 웹사이트 | 웹 API |
|---|---------|--------|
| **응답 형식** | HTML (사람이 보는 화면) | JSON (프로그램이 처리하는 데이터) |
| **사용자** | 브라우저를 쓰는 사람 | 다른 프로그램, 앱, 서비스 |
| **예시** | naver.com | api.naver.com/v1/search |

FastAPI는 **웹 API** 를 만드는 도구입니다. HTML 화면이 아니라 JSON 데이터를 주고받는 서버를 만듭니다.

---

<a id="part2"></a>

## 2️⃣ HTTP 메서드 [↑](#toc)

> 식당에서도 "새 주문이요", "주문 변경해주세요", "주문 취소요" 처럼 요청의 종류가 다릅니다.
> HTTP도 마찬가지입니다. 요청의 **종류(메서드)** 에 따라 서버가 다르게 동작합니다.

웹에서 클라이언트가 서버에게 요청할 때는 반드시 **HTTP 메서드**를 함께 지정합니다. 메서드는 "이 요청이 어떤 종류인지"를 알려주는 동사 역할을 합니다.

| HTTP 메서드 | 의미 | 식당 비유 |
|------------|------|----------|
| **GET** | 데이터 조회 | "메뉴판 보여주세요" / "오늘 주문 목록 보여주세요" |
| **POST** | 새 데이터 생성 | "아메리카노 한 잔 주문할게요" |
| **PUT** | 데이터 전체 수정 | "주문을 라떼로 완전히 바꿔주세요" |
| **PATCH** | 데이터 일부 수정 | "설탕만 빼주세요" |
| **DELETE** | 데이터 삭제 | "주문 취소할게요" |

### GET — 조회 요청

```
GET /menu           ← 전체 메뉴 목록 가져오기
GET /menu/3         ← 3번 메뉴 하나만 가져오기
GET /orders?table=5 ← 5번 테이블 주문 목록 가져오기
```

GET 요청은 서버의 데이터를 **읽기만** 합니다. 데이터를 바꾸지 않습니다.

### POST — 생성 요청

```
POST /orders
Body: {"menu_id": 3, "quantity": 2, "table": 5}
← 새 주문 등록
```

POST 요청은 서버에 **새로운 데이터를 만들** 때 씁니다. 본문(Body)에 새 데이터를 JSON으로 담아 보냅니다.

### PUT — 전체 수정

```
PUT /orders/7
Body: {"menu_id": 5, "quantity": 1, "table": 5}
← 7번 주문을 완전히 새 내용으로 교체
```

### DELETE — 삭제

```
DELETE /orders/7
← 7번 주문 삭제
```

### 메서드와 URL의 조합

동일한 URL이라도 메서드에 따라 다른 동작을 합니다.

```
GET    /items/     → 전체 목록 조회
POST   /items/     → 새 항목 생성

GET    /items/5    → 5번 항목 조회
PUT    /items/5    → 5번 항목 전체 수정
DELETE /items/5    → 5번 항목 삭제
```

이것이 REST API 설계의 기본 원칙입니다. FastAPI는 이 방식을 그대로 따릅니다.

---

<a id="part3"></a>

## 3️⃣ JSON — 주문서 양식 [↑](#toc)

> 식당에서 주문서를 쓸 때 정해진 양식이 있듯이, API에서도 데이터를 주고받는 표준 형식이 있습니다.
> 그것이 바로 JSON입니다. 웨이터(API)가 이해하는 표준 주문서 양식입니다.

**JSON(JavaScript Object Notation)** 은 데이터를 텍스트로 표현하는 형식입니다. 사람도 읽기 쉽고, 모든 프로그래밍 언어에서 다룰 수 있어서 API의 표준 데이터 형식이 되었습니다.

### JSON 예시 — 메뉴 항목 하나

```json
{
  "id": 3,
  "name": "아메리카노",
  "price": 4500,
  "available": true,
  "description": "진한 에스프레소에 물을 더한 커피"
}
```

### JSON 예시 — 주문 목록 (배열)

```json
[
  {
    "order_id": 101,
    "table": 5,
    "items": ["아메리카노", "치즈케이크"],
    "total": 12000,
    "status": "준비중"
  },
  {
    "order_id": 102,
    "table": 2,
    "items": ["라떼"],
    "total": 5000,
    "status": "완료"
  }
]
```

### JSON의 데이터 타입

| 타입 | 예시 | Python 대응 |
|------|------|------------|
| 문자열 | `"안녕하세요"` | `str` |
| 숫자 | `4500`, `3.14` | `int`, `float` |
| 불리언 | `true`, `false` | `bool` |
| null | `null` | `None` |
| 배열 | `["a", "b", "c"]` | `list` |
| 객체 | `{"key": "value"}` | `dict` |

Python의 딕셔너리(`dict`)와 JSON 객체는 거의 동일한 구조입니다. FastAPI는 Python 딕셔너리를 자동으로 JSON으로 변환해줍니다.

---

<a id="part4"></a>

## 4️⃣ 왜 FastAPI인가? [↑](#toc)

> Python으로 웹 API를 만드는 방법은 여러 가지입니다.
> Flask도 있고 Django도 있습니다. 그런데 왜 FastAPI를 선택할까요?

### Python 웹 프레임워크 비교

| 프레임워크 | 출시 | 특징 | 적합한 용도 |
|-----------|------|------|------------|
| **Django** | 2005 | 풀스택, 많은 기능 기본 내장 | 대규모 웹 사이트, CMS |
| **Flask** | 2010 | 가볍고 자유로움, 설정 많음 | 소규모 API, 프로토타입 |
| **FastAPI** | 2018 | 타입 기반, 자동 문서화, 고성능 | 모던 REST API, 마이크로서비스 |

### FastAPI의 성능

FastAPI는 **Node.js, Go 수준의 성능**을 자랑합니다. 이는 Python의 `asyncio`(비동기 처리)를 기반으로 동작하기 때문입니다.

```
벤치마크 (초당 처리 요청 수, 참고 수치):
Django REST Framework : ~5,000 req/sec
Flask                 : ~8,000 req/sec
FastAPI               : 20,000+ req/sec
```

물론 실제 성능은 코드 내용, 서버 사양, DB 쿼리 등에 따라 크게 달라집니다. 하지만 프레임워크 자체의 오버헤드가 매우 적다는 의미입니다.

### 자동 문서화 — Flask/Django에서는 없는 것

Flask나 Django REST Framework에서는 API 문서를 **직접 작성**해야 합니다. FastAPI는 코드에서 **자동으로** Swagger UI 문서를 생성합니다.

```python
# ✅ FastAPI — 이 코드 하나로 Swagger UI 문서 자동 생성
@app.get("/items/{item_id}", summary="아이템 조회", tags=["items"])
def get_item(item_id: int) -> ItemPublic:
    ...
```

### 타입 안전성 — Pydantic과의 결합

FastAPI는 Python 타입 힌트와 Pydantic을 결합해서 **잘못된 데이터를 자동으로 거부**합니다.

```python
# ❌ 잘못된 데이터 예시 (클라이언트가 실수로 보낸 경우)
POST /items/
{"name": "커피", "price": "무료"}  # price가 숫자여야 하는데 문자열

# FastAPI의 자동 응답
HTTP 422 Unprocessable Entity
{"detail": [{"loc": ["body", "price"], "msg": "Input should be a valid number"}]}
```

별도 코드 없이 자동으로 422 에러와 명확한 에러 메시지를 반환합니다.

---

<a id="part5"></a>

## 5️⃣ FastAPI의 3대 장점 [↑](#toc)

### 장점 1 — 자동 문서화 (Swagger UI)

코드를 작성하면 `http://localhost:8000/docs`에서 인터랙티브한 API 문서가 자동으로 생성됩니다.

- 브라우저에서 직접 API를 테스트할 수 있습니다
- 요청 파라미터, 응답 스키마가 자동으로 문서화됩니다
- 팀원, 프론트엔드 개발자와 API 명세를 공유하기 쉽습니다

**Swagger UI에서 확인해보세요!** — 이 과정 내내 가장 많이 들을 말입니다.

### 장점 2 — 타입 기반 검증 (Pydantic)

Python 타입 힌트와 Pydantic v2를 결합해서 입력 데이터를 자동으로 검증합니다.

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(min_length=1, max_length=50)   # 1~50자
    price: float = Field(ge=0)                        # 0 이상
    quantity: int = Field(ge=1, le=999)               # 1~999
```

이 모델 하나로:
- 잘못된 타입 → 자동 422 에러
- 범위 초과 → 자동 422 에러
- 누락된 필드 → 자동 422 에러

검증 코드를 한 줄도 직접 작성하지 않았습니다.

### 장점 3 — 비동기 지원

FastAPI는 `async def`를 지원해서 DB 쿼리나 외부 API 호출 같은 I/O 작업을 비동기로 처리할 수 있습니다.

```python
# ✅ 비동기 엔드포인트 — DB 쿼리가 완료될 때까지 기다리는 동안
#    다른 요청을 처리할 수 있습니다
@app.get("/items/{item_id}")
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await session.get(Item, item_id)
    return item
```

동기 함수(`def`)와 비동기 함수(`async def`) 모두 지원합니다. 이 과정에서는 먼저 `def`로 시작하고, DB를 배울 때 `async def`를 도입합니다.

---

<a id="part6"></a>

## 6️⃣ 정리 [↑](#toc)

### 핵심 개념 요약

| 개념 | 설명 | 식당 비유 |
|------|------|----------|
| API | 클라이언트와 서버 사이의 인터페이스 | 웨이터 |
| HTTP 요청 | 클라이언트가 서버에 보내는 메시지 | 주문 |
| HTTP 응답 | 서버가 클라이언트에게 돌려주는 데이터 | 음식 |
| GET | 데이터 조회 | "메뉴 보여주세요" |
| POST | 데이터 생성 | "새 주문이요" |
| PUT | 데이터 전체 수정 | "주문 전체 변경이요" |
| DELETE | 데이터 삭제 | "주문 취소요" |
| JSON | API 데이터 교환 표준 형식 | 주문서 양식 |
| FastAPI | Python 웹 API 프레임워크 | 식당 운영 시스템 |
| Swagger UI | 자동 생성 API 문서 | 디지털 메뉴판 + 주문 시스템 |

---

### 다음 장 미리보기

| 장 | 내용 |
|---|---|
| 2장 | 개발 환경 설정 — Python, 가상환경, FastAPI 설치, 첫 API 실행 |
| 3장 | Path & Query 파라미터 — URL에서 데이터 받기 |
| 4장 | Pydantic — 요청 바디 검증 |

API가 무엇인지, FastAPI가 왜 좋은지 이해했습니다. 다음 장에서 환경을 설정하고 **첫 번째 API를 직접 만들어봅니다.**

---

### 실습 과제

**기본**: 아래 JSON을 보고 각 값의 타입(문자열/숫자/불리언/배열/객체)을 구별해보세요.

```json
{
  "user_id": 42,
  "username": "홍길동",
  "is_active": true,
  "scores": [95, 87, 91],
  "address": {
    "city": "서울",
    "district": "강남구"
  }
}
```

**중급**: 카카오맵 앱에서 길을 검색할 때 어떤 HTTP 메서드를 사용할지 생각해보세요. 검색(조회)이니 GET일까요, 아니면 다른 메서드일까요? 이유도 생각해보세요.

**심화**: [httpbin.org](https://httpbin.org)에 접속해서 `GET /get`을 직접 요청해보세요. 브라우저 주소창에 `https://httpbin.org/get`을 입력하면 JSON 응답을 볼 수 있습니다. 응답에서 `origin`, `headers` 값이 무엇을 의미하는지 확인해보세요.

{% endraw %}
