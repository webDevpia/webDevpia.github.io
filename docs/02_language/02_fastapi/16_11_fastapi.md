---
title: 11. supabase fastapi 연동
layout: default
grand_parent: Language
parent: FastAPI
nav_order: 11
permalink: /language/fastapi/supabase
has_children: false
---
# SupaBase FastApi 연동

학교내 방화벽에서 사이트의 포트가 막혀있을수도 있으므로 개인 핫스팟으로 인터넷 연결해서 테스트 하세요

## 1. SupaBase 셋팅

### 1. 프로젝트 생성
![](./img/fastapi023.png)

### 2. 접속 URL 확인
![](./img/fastapi024.png)

### 3. 패스워드 기억못할 경우 재설정
![](./img/fastapi025.png)

## 2. 코드 작성

### 1. .env 파일 작성

위에서 복사한 url을 수정해서 사용

```py
SUPABASE_DB_URL=postgresql+asyncpg://postgres.gbwxosihvegcwwunskro:[YOUR-PASSWORD]@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres
```

### 2. app/database.py 

```py
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from collections.abc import AsyncGenerator

load_dotenv()

DATABASE_URL = os.getenv("SUPABASE_DB_URL")

if DATABASE_URL is None:
    raise ValueError("SUPABASE_DB_URL 환경변수가 설정되어 있지 않습니다.")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args={
        "statement_cache_size": 0,  # 🔴 PgBouncer(pooler) 때문에 캐시 끄기
    },
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

### 3. app/models.py

```py
from sqlalchemy import Column, Integer, String
from .database import Base

# 회원 테이블 모델
class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
```

### 4. app/schemas.py 

```py
from pydantic import BaseModel, EmailStr

class MemberBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class MemberCreate(MemberBase):
    """회원 생성용 스키마"""
    pass

class MemberUpdate(BaseModel):
    """회원 수정(부분 수정 포함) 스키마"""
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None

class MemberRead(MemberBase):
    """응답용 스키마"""
    id: int

    class Config:
        from_attributes = True  # SQLAlchemy 객체 → Pydantic 변환
```

### 5. app/crud.py 

```py
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from .models import Member
from .schemas import MemberCreate, MemberUpdate

# 회원 생성
async def create_member(db: AsyncSession, member_in: MemberCreate) -> Member:
    # username 또는 email 중복 체크
    result = await db.execute(
        select(Member).where(
            (Member.username == member_in.username) |
            (Member.email == member_in.email)
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")

    member = Member(
        username=member_in.username,
        email=member_in.email,
        full_name=member_in.full_name,
    )
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member

# 전체 회원 목록
async def get_members(db: AsyncSession) -> List[Member]:
    result = await db.execute(select(Member).order_by(Member.id))
    return result.scalars().all()

# 단일 회원 조회
async def get_member(db: AsyncSession, member_id: int) -> Member:
    result = await db.execute(select(Member).where(Member.id == member_id))
    member = result.scalar_one_or_none()
    if member is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return member

# 회원 수정
async def update_member(db: AsyncSession, member_id: int, member_in: MemberUpdate) -> Member:
    member = await get_member(db, member_id)

    if member_in.username is not None:
        member.username = member_in.username
    if member_in.email is not None:
        member.email = member_in.email
    if member_in.full_name is not None:
        member.full_name = member_in.full_name

    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member

# 회원 삭제
async def delete_member(db: AsyncSession, member_id: int) -> None:
    member = await get_member(db, member_id)
    await db.delete(member)
    await db.commit()
```

### 6. app/main.py 

```py
from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Base, engine, get_db
from .schemas import MemberCreate, MemberUpdate, MemberRead
from .crud import (
    create_member,
    get_members,
    get_member,
    update_member,
    delete_member,
)

app = FastAPI(title="Supabase + FastAPI + SQLAlchemy Members REST API")

# 앱 시작 시 테이블 자동 생성 (개발용)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 회원 생성
@app.post("/members", response_model=MemberRead, status_code=201)
async def api_create_member(
    member_in: MemberCreate,
    db: AsyncSession = Depends(get_db),
):
    member = await create_member(db, member_in)
    return member

# 회원 목록 조회
@app.get("/members", response_model=List[MemberRead])
async def api_get_members(
    db: AsyncSession = Depends(get_db),
):
    members = await get_members(db)
    return members

# 단일 회원 조회
@app.get("/members/{member_id}", response_model=MemberRead)
async def api_get_member(
    member_id: int,
    db: AsyncSession = Depends(get_db),
):
    member = await get_member(db, member_id)
    return member

# 회원 수정
@app.put("/members/{member_id}", response_model=MemberRead)
async def api_update_member(
    member_id: int,
    member_in: MemberUpdate,
    db: AsyncSession = Depends(get_db),
):
    member = await update_member(db, member_id, member_in)
    return member

# 회원 삭제
@app.delete("/members/{member_id}", status_code=204)
async def api_delete_member(
    member_id: int,
    db: AsyncSession = Depends(get_db),
):
    await delete_member(db, member_id)
    return None
```

### 7. 실행하기

```bash
uvicorn app.main:app --reload
```

### 8. 테스트
```bash
# 1. 서버 확인
curl http://127.0.0.1:8000/health

# 2. 회원 생성
curl -X POST http://127.0.0.1:8000/members \
  -H "Content-Type: application/json" \
  -d '{"username":"test1","email":"test1@test.com","full_name":"테스트1"}'

# 3. 전체 조회
curl http://127.0.0.1:8000/members

# 4. 단일 조회
curl http://127.0.0.1:8000/members/1

# 5. 수정
curl -X PUT http://127.0.0.1:8000/members/1 \
  -H "Content-Type: application/json" \
  -d '{"full_name":"이름수정됨"}'

# 6. 삭제
curl -X DELETE http://127.0.0.1:8000/members/1
```





