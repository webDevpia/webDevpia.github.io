---
title: 11. SQLModel + SQLite
layout: default
grand_parent: Language
parent: FastAPI (리뉴얼)
nav_order: 11
permalink: /language/fastapi-new/sqlmodel
---

{% raw %}

## 학습 목표

- Python 리스트(인메모리)와 데이터베이스(영구 저장)의 차이를 설명할 수 있다
- SQLModel로 DB 테이블을 정의하고 Base / table=True / Create / Public 패턴을 적용할 수 있다
- SQLite 엔진과 세션을 설정하고 FastAPI의 `Depends`로 주입할 수 있다
- lifespan 이벤트로 애플리케이션 시작 시 테이블을 자동 생성할 수 있다
- Swagger UI에서 DB 기반 CRUD 엔드포인트를 직접 테스트할 수 있다

<a id="toc"></a>

## 진행 순서

1. [왜 데이터베이스가 필요한가?](#why-db) — 인메모리의 한계
2. [SQLModel이란?](#what-is-sqlmodel) — Pydantic + SQLAlchemy 결합
3. [설치](#install) — `pip install sqlmodel`
4. [모델 정의](#model) — Base / table=True / Create / Public
5. [엔진과 세션](#engine) — `create_engine`, `Session`, `Depends`
6. [CRUD 구현](#crud) — 생성·조회·수정·삭제
7. [lifespan으로 테이블 생성](#lifespan) — 권장 방식
8. [SQLite 파일 확인](#sqlite-file) — `database.db`
9. [정리 + 다음 장 미리보기](#summary)

---

# 11장. SQLModel + SQLite — 데이터베이스 연동

<a id="why-db"></a>

## 1️⃣ 왜 데이터베이스가 필요한가? [↑](#toc)

10장까지 만든 ToDo API는 Python 리스트에 데이터를 저장했습니다.

```python
# 10장의 인메모리 저장소
todos: list[Todo] = []
```

이 방식은 코드를 배우기에 완벽했지만, 실제 서비스에서는 치명적인 문제가 있습니다.

> "DB = 식당의 냉장고 — 카운터 위(인메모리)에 올려둔 재료는 퇴근하면 사라지지만,
> 냉장고(DB)에 넣으면 내일 아침에도 그대로 있습니다."

### 인메모리 방식의 한계

| 상황 | 인메모리 결과 | DB 결과 |
|------|-------------|---------|
| 서버 재시작 | **데이터 전부 삭제** | 데이터 유지 |
| 서버 2대 운영 | 서버마다 다른 데이터 | 공유 데이터베이스 |
| 메모리 부족 | 저장 불가 | 디스크 용량까지 활용 |
| 100만 건 검색 | 전체 리스트 순회 | 인덱스로 빠른 검색 |

실제로 10장 코드를 서버에 올리고, 할 일을 10개 입력한 뒤 서버를 재시작해보세요. 모두 사라집니다.
이제 이 문제를 해결합니다.

---

<a id="what-is-sqlmodel"></a>

## 2️⃣ SQLModel이란? [↑](#toc)

SQLModel은 FastAPI를 만든 **Sebastián Ramírez(Tiangolo)**가 직접 만든 ORM입니다.

> "같은 사람이 만들었기 때문에 FastAPI와 완벽하게 어울립니다."
> Pydantic v2(데이터 검증) + SQLAlchemy(DB 처리)를 하나로 합쳤습니다.

### SQLModel의 핵심 장점

```
Pydantic BaseModel  +  SQLAlchemy ORM
      ↓                      ↓
  데이터 검증              DB 테이블 관리
      ↓                      ↓
         SQLModel — 하나의 클래스로 둘 다!
```

기존에는 Pydantic 모델과 SQLAlchemy 모델을 **따로** 만들어야 했습니다.
SQLModel은 **하나의 클래스**로 API 검증과 DB 저장을 모두 처리합니다.

### 원시 SQL vs SQLModel

# ❌ 원시 SQL (SQLModel 없이)
```python
cursor.execute(
    "INSERT INTO hero (name, age) VALUES (?, ?)",
    (hero.name, hero.age)
)
conn.commit()
```

# ✅ SQLModel 방식
```python
session.add(hero)
session.commit()
session.refresh(hero)
```

SQL 문법을 몰라도 Python 객체처럼 DB를 다룰 수 있습니다.

---

<a id="install"></a>

## 3️⃣ 설치 [↑](#toc)

```bash
pip install sqlmodel
```

SQLModel 하나를 설치하면 Pydantic v2, SQLAlchemy, aiosqlite 등 필요한 패키지가 함께 설치됩니다.
SQLite는 Python 표준 라이브러리에 포함되어 있어 **별도 설치가 필요 없습니다**.

```bash
# 설치 확인
python -c "import sqlmodel; print(sqlmodel.__version__)"
```

실행 결과:
```
0.0.21
```

---

<a id="model"></a>

## 4️⃣ 모델 정의 [↑](#toc)

SQLModel에서는 **3개의 클래스**를 목적에 맞게 분리하는 패턴을 사용합니다.

> "하나의 클래스로 모든 것을 처리하면 편해 보이지만,
> API 입력에는 id가 없고, DB에는 id가 있고, 응답에는 비밀번호가 없어야 합니다.
> 역할별로 나누는 것이 안전합니다."

### 3-모델 패턴

```python
# models.py
from sqlmodel import Field, SQLModel


# 1️⃣ Base — 공통 필드만 모읍니다
class HeroBase(SQLModel):
    name: str = Field(index=True)          # 검색 속도를 위한 인덱스
    age: int | None = Field(default=None)  # 선택 필드


# 2️⃣ table=True — 실제 DB 테이블이 됩니다
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # primary_key=True → DB가 자동으로 1, 2, 3... 번호를 붙여줍니다


# 3️⃣ Create — API 요청(입력)용. id는 아직 없으니 포함하지 않습니다
class HeroCreate(HeroBase):
    pass


# 4️⃣ Public — API 응답(출력)용. id는 반드시 포함합니다
class HeroPublic(HeroBase):
    id: int
```

### 각 모델의 역할 정리

| 클래스 | `table=True` | id 포함 | 사용 위치 |
|--------|:-----------:|:-------:|-----------|
| `HeroBase` | - | - | 공통 필드 정의 (상속 전용) |
| `Hero` | ✅ | ✅ | DB 저장 / 내부 처리 |
| `HeroCreate` | - | - | POST 요청 Body |
| `HeroPublic` | - | ✅ | 모든 응답 |

### 왜 이렇게 나누나요?

# ❌ 하나의 클래스로 전부 처리하면
```python
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int | None = None
    secret_note: str | None = None  # 비밀 메모도 포함됨!

# POST /heroes 에서 클라이언트가 id를 직접 보내버릴 수 있습니다
# GET /heroes 에서 secret_note가 노출될 수 있습니다
```

# ✅ 분리하면
```python
# 클라이언트는 HeroCreate만 볼 수 있습니다 → id 조작 불가
# 응답은 HeroPublic만 반환합니다 → secret_note 노출 없음
```

---

<a id="engine"></a>

## 5️⃣ 엔진과 세션 [↑](#toc)

### 엔진 (Engine)

엔진은 **데이터베이스 파일에 연결하는 통로**입니다.
애플리케이션이 시작될 때 한 번만 만들면 됩니다.

```python
# database.py
from sqlmodel import create_engine

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,  # 실행되는 SQL 쿼리를 콘솔에 출력합니다 (개발 시 유용)
)
```

> "엔진 = 식당의 전화선. 식당(DB)에 전화(쿼리)를 걸기 위한 회선입니다.
> 회선은 하나만 있으면 됩니다."

`sqlite:///database.db`의 의미:
- `sqlite://` — SQLite 드라이버 사용
- `///database.db` — 현재 디렉토리의 `database.db` 파일

### 세션 (Session)

세션은 **하나의 요청 동안 DB와 대화하는 창구**입니다.
요청이 시작되면 세션을 열고, 요청이 끝나면 닫습니다.

```python
# database.py (계속)
from sqlmodel import Session
from typing import Generator


def get_session() -> Generator[Session, None, None]:
    """FastAPI의 Depends에서 사용할 세션 제공 함수"""
    with Session(engine) as session:
        yield session
        # yield 이후 코드는 요청이 끝난 뒤 실행됩니다
        # Session이 context manager이므로 자동으로 close됩니다
```

> "세션 = 식당에서 주문을 받는 직원.
> 손님(요청)이 오면 직원을 배정하고, 손님이 나가면 직원도 쉬게 합니다."

### FastAPI에 세션 주입

```python
# routers/heroes.py
from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..database import get_session

router = APIRouter(prefix="/heroes", tags=["Heroes"])


@router.get("/", response_model=list[HeroPublic])
def read_heroes(session: Session = Depends(get_session)):
    # session은 자동으로 주입됩니다
    ...
```

`Depends(get_session)`이 동작하는 순서:

```
요청 도착
    ↓
Depends(get_session) 호출 → Session(engine) 생성
    ↓
session을 엔드포인트 함수에 전달
    ↓
함수 실행 (DB 작업)
    ↓
응답 전송
    ↓
세션 자동 종료 (yield 이후 코드 실행)
```

---

<a id="crud"></a>

## 6️⃣ CRUD 구현 [↑](#toc)

### Create — 데이터 저장

```python
@router.post("/", response_model=HeroPublic, status_code=201)
def create_hero(
    hero_data: HeroCreate,
    session: Session = Depends(get_session),
):
    # 1. API 입력(HeroCreate) → DB 모델(Hero) 변환
    db_hero = Hero.model_validate(hero_data)

    # 2. 세션에 추가 (아직 DB에 저장되지 않은 상태)
    session.add(db_hero)

    # 3. 실제 DB에 저장
    session.commit()

    # 4. DB가 생성한 id 등 최신 데이터 가져오기
    session.refresh(db_hero)

    return db_hero
```

실행 결과 (Swagger UI에서 POST `/heroes` 호출):
```json
{
  "name": "Deadpond",
  "age": 30,
  "id": 1
}
```

콘솔에는 실행된 SQL이 출력됩니다 (`echo=True` 설정 때문):
```sql
INSERT INTO hero (name, age) VALUES ('Deadpond', 30)
```

### Read — 데이터 조회

```python
from sqlmodel import select


@router.get("/", response_model=list[HeroPublic])
def read_heroes(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 10,
):
    # select(Hero) = "Hero 테이블의 모든 행을 선택"
    statement = select(Hero).offset(offset).limit(limit)
    heroes = session.exec(statement).all()
    return heroes


@router.get("/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
```

> "offset/limit = 책의 목차에서 '11페이지부터 10개만 보여줘'.
> 데이터가 많아질수록 페이지네이션이 필수입니다."

### Update — 데이터 수정

```python
from sqlmodel import SQLModel


class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None


@router.patch("/{hero_id}", response_model=HeroPublic)
def update_hero(
    hero_id: int,
    hero_data: HeroUpdate,
    session: Session = Depends(get_session),
):
    # 1. 기존 데이터 조회
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    # 2. 입력된 필드만 업데이트 (None인 필드는 건너뜀)
    hero_dict = hero_data.model_dump(exclude_unset=True)
    db_hero.sqlmodel_update(hero_dict)

    # 3. 저장
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)

    return db_hero
```

### Delete — 데이터 삭제

```python
@router.delete("/{hero_id}", status_code=204)
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    # 204 No Content → 응답 본문 없음
```

---

<a id="lifespan"></a>

## 7️⃣ lifespan으로 테이블 생성 [↑](#toc)

애플리케이션이 시작될 때 DB 테이블을 자동으로 만들어야 합니다.
FastAPI 0.93 이후의 **권장 방식**은 `lifespan`입니다.

# ❌ 구식 방법 (deprecated)
```python
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
```

# ✅ 현재 권장 방법 (lifespan)
```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── 시작 시 실행 (yield 이전) ──────────────────────
    print("애플리케이션 시작 — 테이블 생성 중...")
    SQLModel.metadata.create_all(engine)
    print("테이블 생성 완료!")

    yield  # ← 여기서 FastAPI가 실제 요청을 처리합니다

    # ── 종료 시 실행 (yield 이후) ──────────────────────
    print("애플리케이션 종료")


app = FastAPI(lifespan=lifespan)
```

`lifespan`의 흐름:

```
uvicorn 시작
    ↓
lifespan 함수 진입
    ↓
SQLModel.metadata.create_all(engine)  ← 테이블 없으면 생성, 있으면 건너뜀
    ↓
yield  ← FastAPI가 여기서 요청을 받기 시작합니다
    ↓
(서버 운영 중)
    ↓
Ctrl+C 또는 종료 신호
    ↓
yield 이후 코드 실행
    ↓
종료 완료
```

> "`create_all`은 테이블이 이미 있으면 건너뜁니다.
> 실수로 두 번 실행해도 기존 데이터가 삭제되지 않으니 안심하세요."

### 전체 main.py 구조

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine
from .routers import heroes


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Hero API",
    description="SQLModel + SQLite 예제",
    lifespan=lifespan,
)

app.include_router(heroes.router)
```

---

<a id="sqlite-file"></a>

## 8️⃣ SQLite 파일 확인 [↑](#toc)

서버를 실행하고 데이터를 하나라도 저장하면 프로젝트 루트에 `database.db` 파일이 생성됩니다.

```bash
uvicorn app.main:app --reload
```

실행 결과:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
애플리케이션 시작 — 테이블 생성 중...
테이블 생성 완료!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

```bash
# 파일이 생성되었는지 확인
ls -lh database.db
```

실행 결과:
```
-rw-r--r-- 1 user staff 8.0K  Apr 10 10:00 database.db
```

### DB Browser for SQLite로 확인하기

1. [DB Browser for SQLite](https://sqlitebrowser.org/) 설치 (무료)
2. `database.db` 파일 열기
3. "Browse Data" 탭에서 테이블 내용 확인

또는 터미널에서 직접 확인:

```bash
# Python REPL에서
python3 -c "
from sqlmodel import create_engine, Session, select
from app.models import Hero
engine = create_engine('sqlite:///database.db')
with Session(engine) as session:
    heroes = session.exec(select(Hero)).all()
    for h in heroes:
        print(h)
"
```

실행 결과:
```
id=1 name='Deadpond' age=30
id=2 name='Spider-Boy' age=None
```

### .gitignore에 추가하기

```bash
# .gitignore
database.db        # 개발용 DB는 git에 올리지 않습니다
*.db               # 모든 SQLite 파일 제외
```

> "실제 서비스의 데이터베이스를 git에 올리면 안 됩니다.
> 개인정보, 비밀번호, 민감한 데이터가 공개될 수 있습니다."

---

<a id="summary"></a>

## 9️⃣ 정리 [↑](#toc)

### 핵심 개념 정리

| 개념 | 설명 | 코드 |
|------|------|------|
| `SQLModel` | Pydantic + SQLAlchemy 통합 ORM | `from sqlmodel import SQLModel` |
| `table=True` | 클래스를 DB 테이블로 지정 | `class Hero(HeroBase, table=True)` |
| `Field(primary_key=True)` | 기본 키 (DB 자동 증가 ID) | `id: int \| None = Field(default=None, primary_key=True)` |
| `create_engine` | DB 연결 생성 | `create_engine("sqlite:///database.db")` |
| `Session` | DB 작업 단위 | `with Session(engine) as session:` |
| `session.add()` | 객체를 세션에 추가 | 아직 DB 저장 전 |
| `session.commit()` | DB에 실제 저장 | 트랜잭션 확정 |
| `session.refresh()` | DB에서 최신값 다시 읽기 | id 등 자동 생성값 반영 |
| `select()` | SELECT 쿼리 빌더 | `select(Hero).where(...)` |
| `lifespan` | 앱 시작/종료 이벤트 | 테이블 자동 생성 |

### 3-모델 패턴 요약

```
HeroCreate (입력) → Hero (DB 저장) → HeroPublic (응답)
     ↑                    ↑                 ↑
  id 없음          table=True         id 포함
  API Body용       실제 테이블         응답 직렬화용
```

### Swagger UI에서 확인하기

서버 실행 후 `http://localhost:8000/docs` 에서:
1. `POST /heroes` — Hero 생성, 응답에서 `id` 자동 생성 확인
2. `GET /heroes` — 전체 목록 조회
3. `GET /heroes/{hero_id}` — id=1 조회
4. `PATCH /heroes/1` — name 또는 age만 수정
5. `DELETE /heroes/1` — 삭제 후 `GET /heroes/1` → 404 확인

서버를 재시작해도 데이터가 남아있습니다! 인메모리 방식과의 가장 큰 차이입니다.

---

### 다음 장 미리보기

12장에서는 **관계(Relationship)**를 배웁니다.
지금까지 Hero 하나만 다뤘지만, 실제 서비스에서는 데이터가 서로 연결되어 있습니다.

- "한 사용자가 여러 개의 할 일을 가진다" → 1:N 관계
- "한 게시글에 여러 개의 태그가 붙는다" → M:N 관계

그리고 **Alembic**으로 이미 배포된 DB의 스키마를 안전하게 변경하는 방법도 배웁니다.

---

### 실습

**기본**: 이번 장의 Hero 예제를 그대로 따라 구현하고, 서버 재시작 후에도 데이터가 유지되는지 Swagger UI에서 확인해보세요.

**중급**: `HeroBase`에 `secret_identity: str | None = None` 필드를 추가하되, `HeroPublic`에는 포함시키지 마세요. Swagger UI에서 POST로 생성한 뒤 GET 응답에 해당 필드가 나타나지 않는지 확인하세요.

**심화**: `offset`과 `limit`을 이용해 페이지네이션을 구현하세요. Hero를 5개 생성하고 `GET /heroes?offset=2&limit=2`로 3번째~4번째 Hero만 가져오는 것을 확인하세요. 힌트: `select(Hero).offset(offset).limit(limit)`.

{% endraw %}
