---
title: FastAPI
layout: default
parent: Language
nav_order: 7
has_children: true
permalink: /language/fastapi
---

{% raw %}

## 학습 목표

- Python 기초 지식으로 실제 운영 가능한 REST API를 만들 수 있다
- FastAPI, Pydantic v2, SQLModel을 활용한 현대적인 API 개발 흐름을 이해할 수 있다

<a id="toc"></a>

## 진행 순서

1. [과정 소개](#intro) - 학습 대상, 사용 도구
2. [과정 구조](#structure) - 4 Parts, 16 chapters
3. [전체 흐름](#flow) - 학습 로드맵
4. [최종 프로젝트](#project) - 블로그 API + Docker 배포
5. [인메모리 → DB 2단계 전략](#strategy) - 학습 방식 설명
6. [Swagger UI 소개](#swagger) - 매 챕터의 핵심 도구

---

# FastAPI — 비전공자를 위한 모던 웹 API

<a id="intro"></a>

## 1️⃣ 과정 소개 [↑](#toc)

### 학습 대상

이 과정은 **Python 기초 이수자**를 위한 과정입니다.
변수, 함수, 클래스, 타입 힌트(`str`, `int`, `list[str]`)를 이해하고 있다면 시작할 수 있습니다.

> "Python으로 계산기를 만들 수 있다면, FastAPI로 웹 API도 만들 수 있습니다."
> CS 전공 지식 없이도 실제 서비스에서 사용하는 수준의 API를 만드는 것이 목표입니다.

### 사용 도구

| 도구 | 버전 | 용도 |
|------|------|------|
| Python | 3.12+ | 프로그래밍 언어 |
| FastAPI | 0.135.x | 웹 API 프레임워크 |
| Pydantic | v2 | 데이터 검증 라이브러리 |
| SQLModel | 최신 | ORM (DB 연동) |
| uvicorn | 최신 | ASGI 서버 |
| pytest | 최신 | 테스트 프레임워크 |
| Docker | 최신 | 컨테이너 배포 |
| uv | 최신 | 빠른 패키지 관리자 (pip 대체) |

### 이 과정을 마치면

- Path/Query 파라미터를 활용한 REST API를 설계하고 구현할 수 있다
- Pydantic v2로 데이터를 검증하고 직렬화할 수 있다
- SQLModel로 SQLite/PostgreSQL 데이터베이스를 연동할 수 있다
- pytest로 API 엔드포인트를 테스트할 수 있다
- Docker로 완성된 API를 컨테이너화하여 배포할 수 있다

---

<a id="structure"></a>

## 2️⃣ 과정 구조 [↑](#toc)

### Part 1 — API 기초 (1~2일차)

| 장 | 제목 | 핵심 개념 |
|----|------|-----------|
| 01 | [FastAPI란?](/language/fastapi-new/intro) | 웹 API 개념, HTTP, JSON, FastAPI 장점 |
| 02 | [환경 설정 + 첫 API](/language/fastapi-new/setup) | 가상환경, 설치, Swagger UI 첫 경험 |
| 03 | [Path & Query 파라미터](/language/fastapi-new/parameters) | URL 파라미터, 타입 검증, 필터링 |
| 04 | [Pydantic — 데이터 검증](/language/fastapi-new/pydantic) | BaseModel, Field, validator |

### Part 2 — API 완성 (3일차)

| 장 | 제목 | 핵심 개념 |
|----|------|-----------|
| 05 | [Response와 상태 코드](/language/fastapi-new/response) | response_model, status_code, JSONResponse |
| 06 | [CRUD 완성 (인메모리)](/language/fastapi-new/crud) | 인메모리 CRUD, 전체 흐름 실습 |
| 07 | APIRouter로 구조화 | router 분리, 파일 구조 설계 |
| 08 | 인증과 보안 기초 | JWT, OAuth2PasswordBearer, 의존성 주입 |

### Part 3 — 데이터베이스 연동 (4일차)

| 장 | 제목 | 핵심 개념 |
|----|------|-----------|
| 09 | SQLModel 기초 | 테이블 정의, 세션 관리 |
| 10 | DB CRUD | async 세션, 트랜잭션 |
| 11 | 관계(Relationship) | 1:N, M:N, JOIN 쿼리 |
| 12 | 마이그레이션 (Alembic) | 스키마 변경 관리 |

### Part 4 — 실전 (5일차)

| 장 | 제목 | 핵심 개념 |
|----|------|-----------|
| 13 | 테스트 (pytest) | TestClient, pytest fixtures |
| 14 | 미들웨어와 CORS | 요청/응답 가공, 프론트엔드 연결 |
| 15 | Docker 배포 | Dockerfile, docker-compose |
| 16 | 최종 프로젝트 | 블로그 API 완성 |

---

<a id="flow"></a>

## 3️⃣ 전체 흐름 [↑](#toc)

```
시작: Python 기초 이수
     ↓
[Part 1] API 기초
  01장 개념 → 02장 환경설정 → 03장 파라미터 → 04장 Pydantic
     ↓
[Part 2] API 완성
  05장 응답/상태코드 → 06장 CRUD(인메모리) → 07장 구조화 → 08장 인증
     ↓
[Part 3] DB 연동
  09장 SQLModel → 10장 DB CRUD → 11장 관계 → 12장 마이그레이션
     ↓
[Part 4] 실전
  13장 테스트 → 14장 미들웨어 → 15장 Docker → 16장 최종 프로젝트
     ↓
완성: 블로그 API + Docker 배포
```

---

<a id="strategy"></a>

## 4️⃣ 인메모리 → DB 2단계 전략 [↑](#toc)

이 과정은 **2단계로 데이터를 다룹니다**. 처음부터 데이터베이스를 다루면 복잡하기 때문에, 먼저 Python 리스트로 API 로직을 완성하고, 나중에 DB로 교체합니다.

| 단계 | 사용 | 챕터 | 목적 |
|------|------|------|------|
| **1단계** | Python `list` (인메모리) | 01 ~ 08장 | API 구조와 로직 학습 |
| **2단계** | SQLModel + SQLite/PostgreSQL | 09 ~ 16장 | 영구 데이터 저장 |

> 인메모리 단계에서는 서버를 재시작하면 데이터가 사라집니다.
> 하지만 API의 구조, 요청/응답 흐름, Pydantic 검증은 모두 동일하게 작동합니다.
> DB 연동 단계에서는 저장소만 교체합니다 — 나머지 코드는 거의 그대로입니다.

이 방식의 장점:

1. **복잡도 분리** — API 로직과 DB 로직을 따로 배울 수 있습니다
2. **빠른 피드백** — DB 설정 없이 바로 API를 실행하고 테스트할 수 있습니다
3. **자연스러운 전환** — "저장소만 바꾼다"는 경험으로 추상화 개념을 체험합니다

---

<a id="swagger"></a>

## 5️⃣ Swagger UI — 매 챕터의 핵심 도구 [↑](#toc)

FastAPI의 가장 강력한 기능 중 하나는 **자동 문서화**입니다. 코드를 작성하면 `http://localhost:8000/docs`에서 아래와 같은 인터랙티브 문서가 자동으로 생성됩니다.

```
http://localhost:8000/docs   ← Swagger UI (인터랙티브)
http://localhost:8000/redoc  ← ReDoc (읽기 전용 문서)
http://localhost:8000/openapi.json ← OpenAPI JSON 스펙
```

이 과정의 모든 챕터에서 **"Swagger UI에서 확인해보세요!"** 라는 안내를 볼 수 있습니다.

- 코드를 작성한 직후 브라우저에서 즉시 테스트할 수 있습니다
- API 문서가 코드와 항상 동기화됩니다 — 문서를 따로 작성할 필요가 없습니다
- Postman 같은 별도 도구 없이 파라미터를 입력하고 응답을 확인할 수 있습니다

---

### 실습 과제

**기본**: Python 3.12가 설치되어 있는지 확인하세요. `python --version` 명령어를 실행해보세요.

**중급**: FastAPI 공식 사이트(fastapi.tiangolo.com)에 접속해서 "Features" 페이지를 읽어보세요.

**심화**: REST API와 GraphQL API의 차이를 검색해보고, 각각 어떤 상황에 적합한지 정리해보세요.

{% endraw %}
