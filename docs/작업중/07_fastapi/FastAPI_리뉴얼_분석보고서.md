---
title: FastAPI 커리큘럼 리뉴얼 분석 보고서
nav_exclude: true
---

{% raw %}

# FastAPI 커리큘럼 리뉴얼 — 다중 페르소나 비판적 분석 보고서
{: .no_toc }

**작성일**: 2026-04-11  
**분석 방법**: 다중 페르소나 비판적 사고 기법 (Multi-Persona Critical Thinking)  
**분석 대상**: `docs/02_language/07_fastapi/` (12개 파일, 16_00 ~ 16_11)  
**데이터 기반**: FastAPI 0.135.x 공식 문서, Pydantic v2, SQLModel, 2024-2026 교육 연구
{: .fs-5 .fw-300 }

---

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 1. 분석 개요

### 1.1 기존 과정 구조

| 장 | 제목 | 주요 내용 | 분량 |
|----|------|----------|------|
| 00 | FastAPI (인덱스) | 제목만 있는 빈 페이지 | 9줄 |
| 01 | FastAPI 소개 | ASGI, 성능 비교, 환경설정(conda), Hello World | 중간 |
| 02 | Request | Path/Query params, Request Body, Form, CORS | 대 |
| 03 | Response | JSONResponse, HTMLResponse, status codes | 중간 |
| 04 | Static file | Jinja2 템플릿, 정적 파일 | 중간 |
| 05 | APIRouter | 라우터 분리 | 소 |
| 06 | Pydantic | BaseModel, 검증, field_validator | 대 |
| 07 | Async | async vs sync (매우 간략) | **41줄** |
| 08 | RDBMS | SQLAlchemy Core, raw SQL, MySQL | 대 |
| 09 | App | Blog CRUD (MySQL+Jinja2+Bootstrap) | 매우 대 |
| 10 | Jinja 템플릿 | Jinja2 문법 기초 | 중간 |
| 11 | Supabase 연동 | async SQLAlchemy ORM + React 풀스택 | 대 |

### 1.2 분석 페르소나

| 페르소나 | 역할 | 관점 |
|---------|------|------|
| **Dr. 백엔드** | 교육공학 연구자 | 학습 순서, 인지 부하, 비유 설계 |
| **박 시니어** | 백엔드 시니어 개발자 (12년차) | 현업 패턴, 기술 정확성, 보안 |
| **김 비평가** | 교육 비평가 / 회의론자 | 기존 문제점, 위험, 구조적 결함 |
| **정 설계자** | 커리큘럼 설계 전문가 | 구조화, 강의 흐름, 스타일 통일 |

---

## 2. 핵심 자료 요약

### 2.1 FastAPI 2025-2026 기술 현황

| 항목 | 현행 |
|------|------|
| FastAPI 버전 | **0.135.x** |
| Python 최소 버전 | **3.10** (0.130.0부터 3.9 드롭) |
| Pydantic 최소 버전 | **v2.9+** (v1 완전 미지원) |
| 공식 ORM | **SQLModel** (Tiangolo 제작, 공식 튜토리얼 사용) |
| 비밀번호 해싱 | **pwdlib[argon2]** (passlib은 유지보수 중단) |
| JWT | **PyJWT** |
| Docker 이미지 | `tiangolo/uvicorn-gunicorn-fastapi` **폐기**, 직접 Dockerfile 작성 |
| 프로세스 관리 | `fastapi run --workers N` (Gunicorn 불필요) |
| 패키지 관리 | **uv** (pip/poetry보다 빠름) |

### 2.2 기존 과정의 폐기/오류 항목

| 파일 | 문제 | 심각도 |
|------|------|--------|
| 16_02 | `item.dict()` — Pydantic v1 폐기 메서드 | 중간 |
| 16_02 | `tax` 필드 중복 선언 (339-340줄) | **버그** |
| 16_02 | `starlette.middleware.cors` import — 비표준 | 낮음 |
| 16_03 | `item.model_dump` 괄호 누락 (94줄) | **버그** |
| 16_06 | `Field(..., example=...)` — Pydantic v2 폐기 | 중간 |
| 16_09 | **SQL 인젝션 취약점** — f-string으로 SQL 직접 삽입 | **치명적** |
| 16_09 | `root:root1234` 하드코딩 DB 비밀번호 | **보안** |
| 16_11 | `@app.on_event("startup")` — FastAPI 폐기 | 중간 |
| 16_11 | `declarative_base()` — SQLAlchemy 1.x 레거시 | 중간 |
| 16_11 | `class Config:` — Pydantic v1 패턴 | 낮음 |

### 2.3 교육 플랫폼 공통 커리큘럼 순서

Udemy, TestDriven.io, DataCamp, 공식 튜토리얼 등 5개+ 플랫폼의 공통 순서:

```
HTTP 기초 → 첫 엔드포인트 → Pydantic → CRUD → 에러 처리 
→ DB(SQLModel) → 의존성 주입 → 인증(JWT) → 테스팅 → 배포
```

### 2.4 효과적인 백엔드 비유 모음

| 개념 | 비유 | 출처 |
|------|------|------|
| API | **식당 웨이터** — 주문(요청)을 받아 주방(서버)에 전달하고 음식(응답)을 가져옴 | 업계 표준 |
| GET | "메뉴 보여주세요" | 식당 비유 확장 |
| POST | "새로운 주문이요" | 식당 비유 확장 |
| PUT | "주문 전체를 이걸로 바꿔주세요" | 식당 비유 확장 |
| DELETE | "주문 취소요" | 식당 비유 확장 |
| Path param | **건물 층수** — `/floors/3` = 3층으로 안내 | 커뮤니티 |
| Query param | **검색 필터** — `?color=red&size=L` = 조건 지정 | 커뮤니티 |
| Pydantic | **입국 심사관** — 서류(데이터)를 하나하나 확인, 불일치 시 입국 거부 | 커뮤니티 |
| Swagger UI | **자판기 버튼 패널** — 버튼(엔드포인트)을 눌러 직접 테스트 | 실무 |
| 의존성 주입 | **건물 관리실** — 열쇠(DB 세션, 인증)를 필요할 때 빌려줌 | 커뮤니티 |
| 미들웨어 | **공항 보안** — 모든 승객이 탑승 전 반드시 통과 | 커뮤니티 |
| JWT 토큰 | **콘서트 팔찌** — 한번 받으면 하루 종일 유효, 위조 어려움, 만료됨 | 커뮤니티 |
| async/await | **카페 번호표** — 주문 후 번호표 받고 기다림, 바리스타는 다음 주문 처리 | JS 과정 확장 |
| ORM | **셰프** — 직접 재료(SQL)를 다루지 않고, 셰프(ORM)에게 요리를 주문 | 커뮤니티 |
| Docker | **이사 짐 컨테이너** — 어디로 옮겨도 동일한 환경 보장 | 실무 |

### 2.5 초보자 핵심 실수 (교육 커뮤니티 합의)

| 순위 | 실수 | 증상 |
|------|------|------|
| 1 | **async/await 오용** — `time.sleep()` in async, `await` 누락 | 이벤트 루프 블로킹, 코루틴 객체 직렬화 |
| 2 | **422 Validation Error 당황** | JSON 바디가 Pydantic 스키마와 불일치 |
| 3 | **Pydantic 모델 3종 혼동** | Create/DB/Public 모델 왜 3개가 필요한지 모름 |
| 4 | **Depends() 이해 실패** | 의존성 체이닝의 개념을 모른 채 복붙 |
| 5 | **DB 세션 생명주기 모름** | `yield`가 왜 필요한지, 세션 누수 |

---

## 3. 다중 페르소나 분석

### 3.1 Dr. 백엔드 — 교육공학 연구자의 분석

#### 핵심 주장: "순서가 뒤틀려 있고, 인지 부하가 관리되지 않는다"

**문제 1: Jinja 템플릿 → 정적 파일 순서 역전**

현재 4장(정적 파일/Jinja 템플릿)에서 `{% for item in all_items %}` 같은 Jinja 문법을 사용하지만, Jinja 문법 설명은 10장에 있다. 학습자는 "이 문법이 뭐지?"라는 의문을 6장 동안 품고 있어야 한다.

**문제 2: 비동기(7장)가 41줄로 허약**

비동기는 FastAPI의 **핵심 가치**이자 초보자 최대 혼란 지점이다. 현재 7장은 `asyncio.sleep` vs `time.sleep` 비교만 보여주고 끝난다. 교육 연구에서 async/await 오용이 **초보자 버그 1위**인데, 설명이 사실상 없다.

**문제 3: DB가 갑자기 raw SQL → ORM으로 점프**

```
8장: SQLAlchemy Core + raw SQL (MySQL)
9장: Blog 앱 — 여전히 raw SQL
11장: 갑자기 async SQLAlchemy ORM + React 풀스택
```

8-9장에서 raw SQL만 배운 학습자가 11장에서 `AsyncSession`, `select()`, `relationship()`을 만나면 **완전히 다른 세계**처럼 느껴진다. 둘 사이의 브릿지가 전혀 없다.

**문제 4: "왜"가 없는 코드 나열**

기존 과정은 JS 과정과 달리 **학습 목표, 비유, 연습 문제, 브릿지 문장이 전부 없다**. 코드를 나열하고 "실행하면 이렇게 됩니다"로 끝난다. 비전공자에게 이 패턴은:
- "왜 이렇게 해야 하지?" → 답이 없음
- "이걸 언제 쓰지?" → 맥락이 없음
- "내가 잘 하고 있나?" → 연습 문제가 없음

#### 평가

| 항목 | 판정 |
|------|------|
| 전체 흐름 | **구조적 결함** — 순서 역전 + 난이도 절벽 |
| 비전공자 적합도 | **부적합** — 비유/연습/목표 전무 |
| 비동기 교육 | **심각한 부족** — 41줄로는 불가능 |

---

### 3.2 박 시니어 — 시니어 개발자의 분석

#### 핵심 주장: "보안 취약점이 교재에 있고, 폐기된 기술 스택이 사용된다"

**치명적 문제: SQL 인젝션이 교재 코드에 존재**

```python
# 16_09_fastapi.md — 이 코드가 "정답"으로 제시됨
query = f"""INSERT INTO blog(title, author, content, modified_dt)
values ('{title}', '{author}', '{content}', now())"""
```

이것은 **SQL 인젝션 공격에 완전히 노출된 코드**다. 같은 파일의 다른 함수에서는 바인드 변수를 사용하므로, 학습자는 "두 방법 다 괜찮은가보다"라고 착각한다.

**폐기된 기술 스택 정리**

| 현재 교재 | 대체 필요 | 이유 |
|----------|----------|------|
| `conda create` | **uv** 또는 `python -m venv` | conda는 데이터 과학 전용, 웹 개발에 과도 |
| `passlib[bcrypt]` | **pwdlib[argon2]** | passlib 유지보수 중단, Python 3.13에서 깨짐 |
| `@app.on_event("startup")` | **lifespan** 컨텍스트 매니저 | FastAPI 폐기 |
| `declarative_base()` | **DeclarativeBase** 클래스 상속 | SQLAlchemy 2.x 패턴 |
| `item.dict()` | **item.model_dump()** | Pydantic v2 |
| MySQL + raw SQL | **SQLModel + SQLite** (학습), PostgreSQL (실전) | 공식 튜토리얼 패턴 |
| `tiangolo/uvicorn-gunicorn-fastapi` | 직접 Dockerfile | 공식 폐기 |

**누락된 핵심 주제 (현업 필수)**

| 주제 | 중요도 | 현재 |
|------|--------|------|
| **에러 처리 (HTTPException, 커스텀 핸들러)** | 필수 | 완전 부재 |
| **의존성 주입 (개념 + 실습)** | 필수 | 사용만 되고 설명 없음 |
| **인증 (OAuth2 + JWT)** | 필수 | 완전 부재 |
| **테스팅 (pytest + TestClient)** | 필수 | 완전 부재 |
| **환경 설정 (pydantic-settings, .env)** | 필수 | 사용만 되고 교육 없음 |
| **배포 (Docker)** | 높음 | 완전 부재 |
| **파일 업로드** | 중간 | 목차에만 있고 내용 없음 |
| **백그라운드 태스크** | 중간 | 완전 부재 |
| **미들웨어 (개념)** | 중간 | CORS 복붙만 |

#### 평가

| 항목 | 판정 |
|------|------|
| 보안 | **즉시 수정 필요** — SQL 인젝션 교재 |
| 기술 정확성 | **대폭 수정** — 폐기 패턴 10건+ |
| 현업 적합도 | **부족** — 인증, 테스팅, 에러 처리 전무 |

---

### 3.3 김 비평가 — 교육 비평가의 분석

#### 핵심 주장: "기존 과정은 '참고 자료 모음'이지 '교육 과정'이 아니다"

**JS 과정과의 스타일 격차**

| 항목 | JS 과정 | FastAPI 과정 | 격차 |
|------|---------|-------------|------|
| 학습 목표 | **매 챕터** | 없음 | 치명적 |
| 진행 순서 (TOC) | 앵커 링크 목차 | 없음 | 치명적 |
| 비유/은유 | **매 개념마다** | 없음 | 치명적 |
| 연습 문제 | 기본/중급/심화 3단계 | 없음 | 치명적 |
| 브릿지 문장 | 다음 장 미리보기 | 없음 | 높음 |
| 핵심 요약 표 | 개념/설명/비유 3열 | 없음 | 높음 |
| 에러 출력 예시 | 모든 코드에 `실행 결과:` | 불규칙 | 높음 |
| 문체 | `~합니다/~하세요` (대화체) | `~함/~됨` (게시판체) | 중간 |
| [↑](#toc) 백링크 | 모든 섹션 | 없음 | 중간 |

**인덱스 페이지가 빈 껍데기**

`16_00_fastapi.md`는 `# FastAPI` 한 줄뿐이다. JS 과정의 인덱스는 과정 소개, 전체 흐름, 최종 프로젝트, 도구 목록을 포함한다.

**파일/폴더 네이밍 혼란**

```
welcome/main.py        ← 소문자
Requests/main_path.py  ← 대문자 시작
DB_Fundamentals/       ← 언더스코어 + 대문자
```

Python 네이밍 컨벤션(PEP 8: 소문자+언더스코어)을 위반하는 예제를 가르치고 있다.

**React 코드의 범위 초과 (11장)**

11장은 200줄 이상의 React 코드를 포함한다. 이것은 FastAPI 과정이 아니라 풀스택 과정이다. FastAPI를 배우러 온 학생이 갑자기 React 코드를 이해해야 하는 것은 범위 초과다.

#### 평가

| 항목 | 판정 |
|------|------|
| 교육 자료로서의 완성도 | **미완성** — 코드 모음집 수준 |
| 비전공자 적합도 | **부적합** — 설명, 비유, 연습 전무 |
| 스타일 통일 | **불일치** — JS 과정과 완전히 다른 포맷 |

---

### 3.4 정 설계자 — 커리큘럼 설계 전문가의 분석

#### 핵심 주장: "전면 재작성이 필요하다. 16장 구조로 재설계한다."

기존 과정의 문제는 **부분 수정으로 해결할 수 없다**. 순서가 뒤틀려 있고, 핵심 주제가 누락되어 있으며, 교육 스타일이 통일되지 않았다. 전면 재작성을 권고한다.

**리뉴얼 커리큘럼 구조 (16장)**

```
FastAPI 리뉴얼 과정 (16장)
│
├── Part 0: 시작 (2장)
│   ├── 01. FastAPI란? — 웹 API와 식당 비유
│   └── 02. 개발 환경 설정 + 첫 API
│
├── Part 1: 핵심 기초 (4장)
│   ├── 03. Path & Query 파라미터
│   ├── 04. Pydantic — 데이터 검증
│   ├── 05. Response와 상태 코드
│   └── 06. CRUD 완성 (인메모리)
│
├── Part 2: 구조화 (4장)
│   ├── 07. APIRouter — 코드 분리
│   ├── 08. 의존성 주입 (Depends)
│   ├── 09. 에러 처리
│   └── 10. 미니 프로젝트: ToDo API (인메모리)
│
├── Part 3: 데이터베이스 (3장)
│   ├── 11. SQLModel + SQLite — DB 연동
│   ├── 12. 관계와 마이그레이션 (Alembic)
│   └── 13. ToDo API → DB 연동 버전
│
└── Part 4: 실전 (3장)
    ├── 14. 인증 — OAuth2 + JWT
    ├── 15. 테스팅 + 환경 설정
    └── 16. 통합 프로젝트: 블로그 API + Docker
```

**시간 배분**

| Part | 장 | 내용 | 예상 시간 |
|------|-----|------|----------|
| Part 0 | 01-02 | HTTP 기초, 환경설정, Hello World | 4h |
| Part 1 | 03-06 | 파라미터, Pydantic, Response, CRUD | 10h |
| Part 2 | 07-10 | Router, DI, 에러, ToDo 프로젝트 | 8h |
| Part 3 | 11-13 | SQLModel, 관계, DB ToDo | 9h |
| Part 4 | 14-16 | 인증, 테스팅, 블로그+Docker | 9h |
| **합계** | | | **40h** |

---

## 4. 쟁점별 페르소나 간 교차 분석

### 4.1 "DB는 SQLModel vs SQLAlchemy Core vs ORM?"

| 페르소나 | 입장 | 근거 |
|---------|------|------|
| Dr. 백엔드 | **SQLModel** — 학습 곡선이 낮음 | Pydantic과 통합, 모델 중복 감소 |
| 박 시니어 | SQLModel (학습) + SQLAlchemy async (언급) | 현업에서는 둘 다 사용 |
| 김 비평가 | **SQLModel + SQLite** — 인프라 설치 장벽 제거 | MySQL 설치는 비전공자에게 과도 |
| 정 설계자 | **SQLModel + SQLite** (11-13장), PostgreSQL은 16장에서 소개 | 공식 튜토리얼 패턴 준수 |

**합의**: **SQLModel + SQLite**를 기본으로. MySQL/PostgreSQL은 16장 배포에서 선택적 소개.

### 4.2 "Jinja2 템플릿을 포함하는가?"

| 페르소나 | 입장 | 근거 |
|---------|------|------|
| Dr. 백엔드 | 제외 | API 과정에 SSR 템플릿은 범위 초과 |
| 박 시니어 | 제외 | 현업에서 FastAPI는 API 전용, 프론트는 React/Vue |
| 김 비평가 | **제외** | Jinja가 순서를 뒤틀리게 한 원인 |
| 정 설계자 | 제외, 단 "참고: SSR이 필요하면 Jinja2를 사용할 수 있습니다" 언급 | 절충 |

**합의**: Jinja2/정적 파일/Bootstrap **제외**. API 전용 과정으로 집중.

### 4.3 "React 풀스택 내용을 포함하는가?"

| 페르소나 | 입장 | 근거 |
|---------|------|------|
| 모든 페르소나 | **제외** | FastAPI 과정에 React 200줄은 범위 초과 |

**합의**: React 연동은 **별도 풀스택 과정**으로 분리.

### 4.4 "비동기를 어디서 어떻게 가르치는가?"

| 페르소나 | 입장 | 근거 |
|---------|------|------|
| Dr. 백엔드 | DB 챕터 직전 (10-11장 사이) | async가 필요한 이유를 DB에서 체감 |
| 박 시니어 | 초반에 개념만, DB에서 실전 | `async def` vs `def`는 첫날부터 |
| 정 설계자 | **02장에서 `async def` 소개 + 11장 DB에서 실전 적용** | 점진적 도입 |

**합의**: 02장에서 `async def` 기본 소개 ("FastAPI는 두 가지 다 지원합니다"). DB 챕터에서 "왜 async가 중요한가" 실전 경험.

### 4.5 "인증을 어디까지 가르치는가?"

| 페르소나 | 입장 | 근거 |
|---------|------|------|
| 박 시니어 | OAuth2 + JWT + 리프레시 토큰 | 현업 최소 역량 |
| 김 비평가 | OAuth2 + JWT (리프레시 제외) | 40시간에 리프레시까지 무리 |
| 정 설계자 | **OAuth2 + JWT 기본**, 리프레시는 "다음으로 배우면" | 절충 |

**합의**: OAuth2 패스워드 플로우 + JWT 액세스 토큰까지. 리프레시 토큰은 심화로 안내.

---

## 5. 비전공자 특화 설계 원칙

### 5.1 매 챕터 구조 (JS/TS 과정과 통일)

```
┌─ 학습 목표 (2-3개)
├─ <a id="toc"></a> + 진행 순서 (앵커 링크)
├─ 1️⃣ 비유로 시작 — 식당/공항 비유 [↑](#toc)
├─ 2️⃣ 고통 (문제) → 해결 (FastAPI의 답) [↑](#toc)
├─ 3️⃣ 코드 + 실행 결과 + Swagger UI 확인 [↑](#toc)
├─ ...
├─ N️⃣ 정리 [↑](#toc)
│   ├── 핵심 개념 요약 (표: 개념 | 설명 | 비유)
│   ├── 다음 장 미리보기
│   └── 실습 과제 (기본 / 중급 / 심화)
└─ "Swagger UI에서 직접 확인해보세요!" 끝맺음
```

### 5.2 Swagger UI — 최강의 교육 도구

FastAPI의 `/docs` (Swagger UI)는 **다른 어떤 프레임워크에도 없는 교육 도구**다:
- 코드를 작성하면 즉시 UI에서 테스트 가능
- 요청/응답 스키마가 시각적으로 표시
- "Try it out" 버튼으로 브라우저에서 API 호출

**매 챕터의 마지막 단계**: "지금 `http://localhost:8000/docs`를 열고 직접 테스트해 보세요."

### 5.3 인메모리 → DB 2단계 전략

DB를 너무 일찍 도입하면 "FastAPI를 배우는 건지 DB를 배우는 건지" 혼란이 발생한다.

```
Phase 1 (Part 1-2): 인메모리 리스트로 CRUD
  todos = []  ← Python 리스트에 데이터 저장
  "새로고침하면 사라지지만, API 개념에 집중할 수 있다"

Phase 2 (Part 3): SQLModel + SQLite로 전환
  "이제 데이터를 영구 저장합시다"
  같은 CRUD 로직을 DB 버전으로 리팩터링
```

이 전략은 Udemy, TestDriven.io, 공식 튜토리얼에서 공통으로 사용된다.

### 5.4 TypeScript 과정과의 브릿지

이 프로젝트에 TypeScript 과정이 존재하므로, Python 타입 힌트를 TS와 연결할 수 있다:

| TypeScript | Python (FastAPI) |
|-----------|-----------------|
| `string` | `str` |
| `number` | `int` / `float` |
| `boolean` | `bool` |
| `string[]` | `list[str]` |
| `string \| null` | `str \| None` |
| `interface User {}` | `class User(BaseModel):` |
| `field?: string` | `field: str \| None = None` |

> "TypeScript를 배웠다면 Python 타입 힌트의 80%는 이미 알고 있습니다."

---

## 6. 기존 콘텐츠 재활용 판정

### 6.1 유지/활용할 것

| 기존 파일 | 내용 | 활용 방법 |
|----------|------|----------|
| 16_01 | ASGI 설명, 성능 비교 | 01장에 압축 포함 |
| 16_02 | Path/Query/Body 패턴 | 03장에 재구성 (버그 수정) |
| 16_03 | Response 패턴 | 05장에 재구성 (버그 수정) |
| 16_05 | APIRouter | 07장에 유지 |
| 16_06 | Pydantic 검증 | 04장에 재구성 (폐기 패턴 수정) |

### 6.2 제거/대체할 것

| 기존 파일 | 이유 | 대체 |
|----------|------|------|
| 16_04 (Jinja 정적) | Jinja 제외 결정 | API 전용으로 전환 |
| 16_07 (Async 41줄) | 너무 부실 | 02장+11장으로 분산 확장 |
| 16_08 (raw SQL) | SQLAlchemy Core는 초보자에게 과도 | SQLModel로 대체 |
| 16_09 (Blog CRUD) | SQL 인젝션 + MySQL 의존 | 16장 블로그 프로젝트로 재설계 |
| 16_10 (Jinja 문법) | Jinja 제외 결정 | 제거 |
| 16_11 (Supabase+React) | React 범위 초과 + 폐기 패턴 | 별도 풀스택 과정 |

---

## 7. 종합 권고안

### 7.1 확정된 결정사항

| 항목 | 결정 | 근거 |
|------|------|------|
| 대상 | **비전공자** | 사용자 확정 |
| 과정 방식 | **전면 재작성** | 부분 수정 불가한 구조적 문제 |
| 장 수 | **16장** | 설계자 권고 |
| FastAPI 버전 | **0.135.x** | 최신 안정 |
| Python 버전 | **3.10+ (3.12 권장)** | 0.130.0+ 요구사항 |
| Pydantic | **v2** | v1 완전 미지원 |
| DB | **SQLModel + SQLite** (학습) | 공식 튜토리얼 + 설치 장벽 제거 |
| 인증 | **pwdlib + PyJWT** | passlib 폐기 |
| Jinja2/SSR | **제외** | API 전용 과정 |
| React 풀스택 | **제외** (별도 과정) | 범위 초과 |
| 스타일 | **JS/TS 과정과 통일** | 비유, 목표, 연습, 브릿지 |
| 테스팅 | **pytest + TestClient** | 현업 필수 |
| 배포 | **Docker** | 기초 수준만 |
| Swagger UI | **매 챕터 활용** | FastAPI 최강 교육 도구 |

### 7.2 16장 상세 구조

| Part | 장 | 제목 | 주요 내용 | 시간 |
|------|-----|------|----------|------|
| **0** | 01 | FastAPI란? | HTTP 기초, REST, 식당 비유, 왜 FastAPI인가 | 2h |
| | 02 | 환경 설정 + 첫 API | uv/venv, uvicorn, Hello World, Swagger, async 기초 | 2h |
| **1** | 03 | Path & Query 파라미터 | 경로/쿼리 매개변수, 타입 검증, 자동 문서화 | 2.5h |
| | 04 | Pydantic — 입국 심사관 | BaseModel, 검증, field_validator, 다중 모델 패턴 | 3h |
| | 05 | Response와 상태 코드 | response_model, status codes, JSONResponse | 2h |
| | 06 | CRUD 완성 (인메모리) | GET/POST/PUT/DELETE 전체, 리스트 저장 | 2.5h |
| **2** | 07 | APIRouter | 코드 분리, prefix, tags | 1.5h |
| | 08 | 의존성 주입 | Depends(), Annotated, 체이닝, 건물 관리실 비유 | 2.5h |
| | 09 | 에러 처리 | HTTPException, 커스텀 핸들러, 검증 에러 | 2h |
| | 10 | 미니 프로젝트: ToDo API | 인메모리 ToDo 완성 (Router+DI+에러) | 2h |
| **3** | 11 | SQLModel + SQLite | 모델, 세션, CRUD, Depends(get_session) | 3h |
| | 12 | 관계와 마이그레이션 | 1:N 관계, Alembic 기초 | 3h |
| | 13 | ToDo API → DB 버전 | 10장 프로젝트를 DB로 리팩터링 | 3h |
| **4** | 14 | 인증 (OAuth2+JWT) | 회원가입, 로그인, 토큰, 보호 라우트 | 3h |
| | 15 | 테스팅 + 환경 설정 | TestClient, pytest, pydantic-settings, .env | 3h |
| | 16 | 블로그 API + Docker | 종합 프로젝트 + Dockerfile + 배포 기초 | 3h |
| | | **합계** | | **40h** |

---

## 8. 결론 — 페르소나 간 최종 합의

### 4인이 동의하는 것

1. **전면 재작성**이 필요하다 — 부분 수정으로는 구조적 문제 해결 불가
2. **SQL 인젝션 취약점**은 즉시 제거해야 한다
3. **JS/TS 과정과 동일한 스타일**(비유, 목표, 연습, 브릿지)로 통일
4. **식당 비유**를 중심 비유로 사용하여 HTTP/API 개념 설명
5. **인메모리 → DB** 2단계 전략으로 인지 부하 관리
6. **SQLModel + SQLite**가 비전공자에게 최적
7. **Jinja2/React 제외** — API 전용 과정으로 집중
8. **Swagger UI를 매 챕터 교육 도구**로 활용
9. **인증, 테스팅, 에러 처리** 챕터 신설 필수
10. **비동기 설명 대폭 확장** — 41줄 → 분산 교육

### 4인이 동의하지 않는 것

| 쟁점 | 범위 |
|------|------|
| Alembic 깊이 | 박 시니어(상세히) vs 김 비평가(기초만) |
| Docker 범위 | 정 설계자(기초) vs 박 시니어(docker-compose까지) |
| async 교육 시점 | Dr. 백엔드(DB 직전) vs 정 설계자(02장부터 점진적) |

---

## 부록: 참고 문헌

### FastAPI 공식
- [FastAPI Release Notes](https://fastapi.tiangolo.com/release-notes/)
- [FastAPI SQL Databases Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [FastAPI OAuth2 JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [FastAPI Docker Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [FastAPI Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

### 교육 플랫폼
- Udemy — FastAPI: The Complete Course 2026 (10,590 ratings, 4.6/5)
- TestDriven.io — FastAPI Tutorials
- DataCamp — Introduction to FastAPI
- zhanymkanov/fastapi-best-practices (GitHub)

### 기술 문서
- [Pydantic v2 Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [SQLModel Official Docs](https://sqlmodel.tiangolo.com/)
- [pwdlib — passlib 대체](https://github.com/frankie567/pwdlib)
- [FastAPI Production Deployment Guide 2025](https://blog.greeden.me/en/2025/09/02/the-definitive-guide-to-fastapi-production-deployment/)

---

*본 보고서는 다중 페르소나 비판적 사고 기법(Multi-Persona Critical Thinking)을 적용하여,*  
*교육공학자, 시니어 개발자, 교육 비평가, 커리큘럼 설계자 4가지 관점에서 독립 분석한 후 종합하였습니다.*

{% endraw %}
