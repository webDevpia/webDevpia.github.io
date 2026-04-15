---
title: 11. supabase fastapi react 연동
layout: default
grand_parent: Language
parent: FastAPI
nav_order: 11
permalink: /language/fastapi/supabase
has_children: false
---
# SupaBase FastApi react 연동

학교내 방화벽에서 사이트의 포트가 막혀있을수도 있으므로 개인 핫스팟으로 인터넷 연결해서 테스트 하세요

## 1. SupaBase 셋팅

### 1. 프로젝트 생성
![](./img/fastapi023.png)

### 2. 접속 URL 확인
![](./img/fastapi024.png)

### 3. 패스워드 기억못할 경우 재설정
![](./img/fastapi025.png)

### 4. 테이블 생성
Supabase → SQL Editor → 실행:
```sql
create table members (
  id bigserial primary key,
  username text unique not null,
  email text unique not null,
  full_name text,
  created_at timestamptz default now()
);
```
## 2. FastAPI 코드 작성

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

async def get_db():
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

**curl**로 테스트 
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

**swagger**로 테스트
![](./img/fastapi026.png)


## 3. React 코드 작성

### 1. app/main.py 에 CORS 설정 추가

```py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Supabase + FastAPI + SQLAlchemy Members REST API")

# 🔹 CORS 설정 추가
origins = [
    "http://localhost:5173",  # Vite 기본 포트
    "http://127.0.0.1:5173",
    "http://localhost:3000",  # CRA 쓴다면
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. 리액트 프로젝트 생성

```bash
npm create vite@latest members-react -- --template react
```

### 3. App.jsx 작성

members-react/src/App.jsx 내용을 아래 코드로 통째로 교체해 주세요.
```js{%raw%}
import { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");

  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({
    username: "",
    email: "",
    full_name: "",
  });

  // 공통 메시지 헬퍼
  const showError = (msg) => {
    console.error(msg);
    setError(msg);
    setTimeout(() => setError(""), 3000);
  };

  const showInfo = (msg) => {
    console.log(msg);
    setInfo(msg);
    setTimeout(() => setInfo(""), 3000);
  };

  // 회원 목록 불러오기
  const fetchMembers = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/members`);
      if (!res.ok) {
        throw new Error(`목록 조회 실패 (HTTP ${res.status})`);
      }
      const data = await res.json();
      setMembers(data);
    } catch (err) {
      showError(err.message || "목록 조회 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  // 첫 렌더링 시 목록 로딩
  useEffect(() => {
    fetchMembers();
  }, []);

  // 입력 변경 핸들러
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  // 생성/수정 제출
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      const payload = {
        username: form.username || undefined,
        email: form.email || undefined,
        full_name: form.full_name || undefined,
      };

      let url = `${API_BASE}/members`;
      let method = "POST";

      if (editingId !== null) {
        url = `${API_BASE}/members/${editingId}`;
        method = "PUT";
      }

      const res = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errBody = await res.json().catch(() => ({}));
        const detail =
          errBody.detail ||
          `저장 실패 (HTTP ${res.status})`;
        throw new Error(
          typeof detail === "string" ? detail : JSON.stringify(detail)
        );
      }

      await fetchMembers();
      if (editingId === null) {
        showInfo("회원이 생성되었습니다.");
      } else {
        showInfo("회원 정보가 수정되었습니다.");
      }
      resetForm();
    } catch (err) {
      showError(err.message || "저장 중 오류가 발생했습니다.");
    } finally {
      setSaving(false);
    }
  };

  // 수정 버튼 클릭
  const handleEdit = (member) => {
    setEditingId(member.id);
    setForm({
      username: member.username || "",
      email: member.email || "",
      full_name: member.full_name || "",
    });
  };

  // 삭제
  const handleDelete = async (id) => {
    if (!window.confirm(`정말 ID ${id} 회원을 삭제하시겠습니까?`)) return;
    try {
      const res = await fetch(`${API_BASE}/members/${id}`, {
        method: "DELETE",
      });
      if (!res.ok && res.status !== 204) {
        throw new Error(`삭제 실패 (HTTP ${res.status})`);
      }
      showInfo("회원이 삭제되었습니다.");
      await fetchMembers();
    } catch (err) {
      showError(err.message || "삭제 중 오류가 발생했습니다.");
    }
  };

  // 폼 초기화
  const resetForm = () => {
    setEditingId(null);
    setForm({
      username: "",
      email: "",
      full_name: "",
    });
  };

  return (
    <div style={styles.container}>
      <h1>Members 관리 (FastAPI + Supabase + React)</h1>

      {/* 상태 메시지 */}
      {error && <div style={{ ...styles.alert, ...styles.alertError }}>{error}</div>}
      {info && <div style={{ ...styles.alert, ...styles.alertInfo }}>{info}</div>}

      {/* 입력 폼 */}
      <section style={styles.card}>
        <h2>{editingId ? `회원 수정 (ID: ${editingId})` : "새 회원 추가"}</h2>
        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>
            Username
            <input
              name="username"
              value={form.username}
              onChange={handleChange}
              style={styles.input}
              placeholder="예: sunny"
              required={!editingId} // 생성 시 필수, 수정 시 선택
            />
          </label>
          <label style={styles.label}>
            Email
            <input
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              style={styles.input}
              placeholder="예: sunny@example.com"
              required={!editingId}
            />
          </label>
          <label style={styles.label}>
            Full Name
            <input
              name="full_name"
              value={form.full_name}
              onChange={handleChange}
              style={styles.input}
              placeholder="예: 선조 심"
            />
          </label>

          <div style={styles.buttonRow}>
            <button type="submit" style={styles.button} disabled={saving}>
              {saving
                ? "저장 중..."
                : editingId
                ? "수정 저장"
                : "회원 생성"}
            </button>
            {editingId && (
              <button
                type="button"
                style={{ ...styles.button, ...styles.buttonSecondary }}
                onClick={resetForm}
              >
                취소
              </button>
            )}
          </div>
        </form>
      </section>

      {/* 목록 */}
      <section style={styles.card}>
        <div style={styles.listHeader}>
          <h2>회원 목록</h2>
          <button style={styles.buttonSmall} onClick={fetchMembers} disabled={loading}>
            {loading ? "불러오는 중..." : "새로고침"}
          </button>
        </div>
        {loading && <p>목록을 불러오는 중입니다...</p>}
        {!loading && members.length === 0 && <p>등록된 회원이 없습니다.</p>}

        {!loading && members.length > 0 && (
          <table style={styles.table}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Full Name</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {members.map((m) => (
                <tr key={m.id}>
                  <td>{m.id}</td>
                  <td>{m.username}</td>
                  <td>{m.email}</td>
                  <td>{m.full_name}</td>
                  <td>
                    <button
                      style={styles.buttonSmall}
                      onClick={() => handleEdit(m)}
                    >
                      수정
                    </button>
                    <button
                      style={{ ...styles.buttonSmall, ...styles.buttonDanger }}
                      onClick={() => handleDelete(m.id)}
                    >
                      삭제
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "960px",
    margin: "0 auto",
    padding: "2rem",
    fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
  },
  card: {
    border: "1px solid #ddd",
    borderRadius: "8px",
    padding: "1.5rem",
    marginBottom: "1.5rem",
    backgroundColor: "#fff",
    boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "0.75rem",
  },
  label: {
    display: "flex",
    flexDirection: "column",
    fontSize: "0.9rem",
    fontWeight: 500,
    gap: "0.25rem",
  },
  input: {
    padding: "0.5rem 0.75rem",
    borderRadius: "4px",
    border: "1px solid #ccc",
    fontSize: "0.95rem",
  },
  buttonRow: {
    marginTop: "0.75rem",
    display: "flex",
    gap: "0.5rem",
  },
  button: {
    padding: "0.5rem 1rem",
    borderRadius: "4px",
    border: "none",
    backgroundColor: "#2563eb",
    color: "#fff",
    fontWeight: 600,
    cursor: "pointer",
  },
  buttonSecondary: {
    backgroundColor: "#6b7280",
  },
  buttonDanger: {
    backgroundColor: "#dc2626",
  },
  buttonSmall: {
    padding: "0.3rem 0.6rem",
    borderRadius: "4px",
    border: "none",
    backgroundColor: "#2563eb",
    color: "#fff",
    fontSize: "0.8rem",
    cursor: "pointer",
    marginRight: "0.25rem",
  },
  alert: {
    padding: "0.5rem 0.75rem",
    borderRadius: "4px",
    marginBottom: "0.75rem",
    fontSize: "0.9rem",
  },
  alertError: {
    backgroundColor: "#fee2e2",
    color: "#b91c1c",
  },
  alertInfo: {
    backgroundColor: "#e0f2fe",
    color: "#1d4ed8",
  },
  listHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "0.75rem",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    fontSize: "0.9rem",
  },
  tableCell: {
    border: "1px solid #e5e7eb",
    padding: "0.4rem 0.6rem",
  },
};

export default App;{%endraw%}
```




