---
title: 10. MCP 도구 연결 & 로컬 LLM
layout: default
grand_parent: LLM
parent: AI Agent
nav_order: 10
permalink: /llm/ai-agent/mcp-local
---

## 학습 목표

- MCP(Model Context Protocol)의 개념을 이해하고 기존 MCP 서버를 Agent에 연결할 수 있다
- Ollama로 로컬 LLM을 CrewAI에 연동할 수 있다

<a id="toc"></a>

## 진행 순서

1. [MCP란?](#part1) - 표준화된 AI 도구 연결 프로토콜
2. [CrewAI에서 MCP 사용](#part2) - mcps 파라미터로 도구 연결
3. [로컬 LLM (Ollama) 연동](#part3) - 무료로 GPT 수준의 AI 사용
4. [정리](#part4) - MCP 생태계, 로컬 vs 클라우드 LLM 비교

---

# 10장. MCP 도구 연결 & 로컬 LLM

<a id="part1"></a>

## 1️⃣ MCP란? [↑](#toc)

**MCP(Model Context Protocol)**는 AI 모델이 외부 도구(검색, 파일 시스템, 데이터베이스 등)와 **표준화된 방식으로 연결**할 수 있도록 설계된 공개 프로토콜입니다.

### USB 규격 비유

> 과거에는 제조사마다 다른 충전 케이블을 사용했습니다. USB-C라는 표준이 생기면서 어떤 기기든 같은 케이블로 연결할 수 있게 되었죠.
>
> **MCP는 AI 세계의 USB-C 규격입니다.**
> 어떤 AI 모델이든 동일한 MCP 인터페이스를 통해 어떤 도구든 연결할 수 있습니다.

### MCP 이전의 문제: N×M 통합 지옥

```
MCP 도입 전:
  Claude  ─── 검색 도구 (Claude 전용 코드)
  Claude  ─── 파일 도구 (Claude 전용 코드)
  GPT-4   ─── 검색 도구 (GPT 전용 코드)
  GPT-4   ─── 파일 도구 (GPT 전용 코드)
  ...  (N개 모델 × M개 도구 = N×M 통합 코드 필요)

MCP 도입 후:
  [MCP 서버: 검색]
  [MCP 서버: 파일]     → 어떤 AI 모델이든 동일한 방식으로 연결
  [MCP 서버: DB]
```

### MCP 생태계

2025년 12월, **AAIF(Agentic AI Interoperability Foundation)**가 설립되어 MCP가 사실상 표준으로 자리잡았습니다. OpenAI, Google, Microsoft, AWS가 공동 참여하며 AI 업계 전체가 MCP를 채택하는 방향으로 움직이고 있습니다.

### MCP의 구성 요소

| 구성요소 | 역할 | 예시 |
|---------|------|------|
| MCP 서버 | 도구를 MCP 형식으로 제공 | 검색 서버, 파일 서버, DB 서버 |
| MCP 클라이언트 | AI 모델이 MCP 서버 호출 | Claude, GPT-4, CrewAI |
| MCP 프로토콜 | 통신 표준 규격 | JSON-RPC 2.0 기반 |

### 공개 MCP 서버 예시

```
Filesystem  — 파일 읽기/쓰기/검색
Web Search  — 웹 검색 (Brave, DuckDuckGo 등)
GitHub      — 저장소 읽기/이슈 관리
PostgreSQL  — 데이터베이스 쿼리
Slack       — 채널 읽기/메시지 전송
Notion      — 문서 읽기/편집
```

---

<a id="part2"></a>

## 2️⃣ CrewAI에서 MCP 사용 [↑](#toc)

CrewAI는 `mcps` 파라미터를 통해 MCP 서버를 에이전트에 직접 연결할 수 있습니다.

### MCPServerAdapter를 사용한 연결

```python
from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter
from dotenv import load_dotenv

load_dotenv()

# ─── MCP 서버 설정 ───────────────────────────────────────────
# stdio 방식: 로컬에 설치된 MCP 서버를 프로세스로 실행
mcp_server_params = {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {"BRAVE_API_KEY": "your-brave-api-key"}
}

# ─── MCP 서버 어댑터 생성 및 사용 ───────────────────────────
with MCPServerAdapter(mcp_server_params) as mcp_tools:
    # mcp_tools에는 MCP 서버가 제공하는 도구 목록이 담김
    agent = Agent(
        role="리서치 전문가",
        goal="MCP 검색 도구를 활용하여 최신 정보를 수집한다",
        backstory="웹 검색을 통해 신뢰할 수 있는 정보를 제공하는 리서처입니다.",
        tools=mcp_tools,    # MCP 도구를 에이전트에 연결
        verbose=True
    )

    task = Task(
        description="2025년 AI 에이전트 관련 최신 뉴스를 검색하고 요약하세요.",
        expected_output="최신 뉴스 5개의 제목과 요약",
        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    print(result)
```

### SSE 방식 MCP 서버 연결 (원격)

```python
# HTTP SSE 방식: 원격 MCP 서버 연결
mcp_sse_params = {
    "url": "https://mcp.example.com/search",
    "transport": "sse"    # Server-Sent Events
}

with MCPServerAdapter(mcp_sse_params) as mcp_tools:
    agent = Agent(
        role="리서치 전문가",
        tools=mcp_tools,
        # ...
    )
```

### 여러 MCP 서버를 동시에 연결

```python
from crewai_tools import MCPServerAdapter

# 여러 MCP 서버 설정
search_server = {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {"BRAVE_API_KEY": "your-key"}
}

filesystem_server = {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
}

# 각각 어댑터를 열어 도구를 수집
with MCPServerAdapter(search_server) as search_tools, \
     MCPServerAdapter(filesystem_server) as fs_tools:

    all_tools = search_tools + fs_tools  # 도구 목록 합치기

    agent = Agent(
        role="만능 리서치 에이전트",
        goal="검색과 파일 저장을 모두 할 수 있다",
        backstory="웹 검색과 파일 처리를 동시에 수행하는 에이전트입니다.",
        tools=all_tools,
        verbose=True
    )
```

### MCP 사용 전 준비사항

```bash
# Node.js 필요 (MCP 서버 대부분이 npm 패키지)
node --version    # v18 이상 권장

# crewai-tools 설치 (MCPServerAdapter 포함)
pip install crewai-tools

# 필요한 MCP 서버 미리 설치 (선택사항)
npx -y @modelcontextprotocol/server-filesystem --help
```

---

<a id="part3"></a>

## 3️⃣ 로컬 LLM (Ollama) 연동 [↑](#toc)

**Ollama**는 Llama, Gemma, Mistral 등 오픈소스 LLM을 **로컬 PC에서 무료로 실행**할 수 있는 도구입니다.

### 로컬 LLM 사용의 장단점

| 구분 | 로컬 LLM (Ollama) | 클라우드 LLM (GPT-4o 등) |
|------|------------------|------------------------|
| 비용 | 완전 무료 | API 사용료 발생 |
| 개인정보 | 데이터가 외부로 나가지 않음 | API 제공사 정책 적용 |
| 성능 | GPU 성능에 따라 제한 | 최고 수준 성능 |
| 속도 | GPU 없으면 느림 | 안정적인 응답 속도 |
| 설정 | Ollama 설치 필요 | API 키만 있으면 됨 |
| 오프라인 | 인터넷 불필요 | 인터넷 필수 |

### Ollama 설치 및 모델 다운로드

```bash
# Ollama 설치 (macOS)
brew install ollama

# Ollama 설치 (Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Ollama 서버 실행
ollama serve

# 모델 다운로드 (별도 터미널에서)
ollama pull llama3.2          # Meta Llama 3.2 (3B, 가볍고 빠름)
ollama pull gemma3             # Google Gemma 3 (한국어 성능 좋음)
ollama pull mistral            # Mistral 7B (균형 잡힌 성능)
ollama pull qwen2.5-coder      # 코드 특화 모델

# 설치된 모델 확인
ollama list
```

### CrewAI에 Ollama 연동

```python
# 파일명: 10_local_llm.py
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv

load_dotenv()

# ─── 로컬 LLM 설정 ───────────────────────────────────────────
local_llm = LLM(
    model="ollama/llama3.2",            # ollama/[모델명] 형식
    base_url="http://localhost:11434"   # Ollama 기본 포트
)

# ─── 에이전트에 로컬 LLM 적용 ──────────────────────────────
agent = Agent(
    role="로컬 AI 어시스턴트",
    goal="개인정보를 안전하게 처리하며 사용자를 돕는다",
    backstory=(
        "외부 서버에 데이터를 전송하지 않는 프라이버시 중심 AI 어시스턴트입니다. "
        "모든 처리가 로컬에서 이루어집니다."
    ),
    llm=local_llm,   # 로컬 LLM 지정
    verbose=True
)

task = Task(
    description="사용자의 개인 일기를 분석하여 감정 상태를 요약하세요: {diary}",
    expected_output="감정 분석 결과 (주요 감정, 감정 강도, 조언)",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff(inputs={
    "diary": "오늘은 발표가 있었는데 생각보다 잘 됐다. 하지만 아직 부족한 부분이 많다는 걸 느꼈다."
})
print(result)
```

### 다양한 Ollama 모델 선택 가이드

```python
from crewai import LLM

# 가볍고 빠른 모델 (일반 작업)
fast_llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

# 성능 중시 모델 (복잡한 분석)
powerful_llm = LLM(
    model="ollama/gemma3",
    base_url="http://localhost:11434"
)

# 코드 작성 특화 모델
code_llm = LLM(
    model="ollama/qwen2.5-coder",
    base_url="http://localhost:11434"
)

# 에이전트별 다른 LLM 사용 가능
simple_agent = Agent(
    role="간단한 정리 담당",
    llm=fast_llm,      # 가벼운 모델
    # ...
)

complex_agent = Agent(
    role="심층 분석 담당",
    llm=powerful_llm,  # 강력한 모델
    # ...
)
```

### LiteLLM을 통한 다양한 LLM 지원

CrewAI는 내부적으로 **LiteLLM**을 사용하므로, Ollama 외에도 다양한 LLM 제공자를 동일한 방식으로 사용할 수 있습니다:

```python
from crewai import LLM

# OpenAI (기본)
openai_llm = LLM(model="gpt-4o-mini")

# Anthropic Claude
claude_llm = LLM(model="claude-3-5-haiku-20241022")

# Google Gemini
gemini_llm = LLM(model="gemini/gemini-2.0-flash")

# Ollama (로컬)
ollama_llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

# Crew에서 기본 LLM 설정
crew = Crew(
    agents=[agent],
    tasks=[task],
    # 모든 에이전트에 기본 LLM 적용 (에이전트에서 개별 지정하면 덮어씀)
)
```

---

<a id="part4"></a>

## 4️⃣ 정리 [↑](#toc)

### MCP 생태계 요약

```
[MCP 서버 유형]
  로컬 stdio  ─── PC에서 프로세스로 실행 (npx, python 명령어 등)
  원격 SSE    ─── HTTP로 접근 가능한 원격 서버
  원격 HTTP   ─── REST API 방식

[대표적인 공개 MCP 서버]
  @modelcontextprotocol/server-filesystem  — 파일 시스템
  @modelcontextprotocol/server-brave-search — 웹 검색
  @modelcontextprotocol/server-github      — GitHub
  @modelcontextprotocol/server-postgres    — PostgreSQL
  @modelcontextprotocol/server-slack       — Slack
```

### 로컬 vs 클라우드 LLM 비교표

| 항목 | Ollama (로컬) | GPT-4o / Claude (클라우드) |
|------|-------------|--------------------------|
| 비용 | 무료 | 토큰당 과금 |
| 데이터 보안 | 완전 로컬 처리 | 외부 전송 |
| 성능 | 모델 크기와 GPU에 따라 다름 | 최고 수준 |
| 속도 | GPU 없으면 느림 | 빠르고 안정적 |
| 모델 선택 | 50+ 오픈소스 모델 | 제공사 모델만 |
| 오프라인 | 가능 | 불가 |
| 권장 용도 | 개인정보 처리, 비용 절감 | 최고 품질 필요 시 |

### 핵심 요약

- MCP는 AI와 외부 도구를 표준화된 방식으로 연결하는 **USB-C 같은 규격**
- CrewAI에서 `MCPServerAdapter`로 어떤 MCP 서버든 도구로 연결 가능
- `LLM(model="ollama/모델명", base_url="http://localhost:11434")`로 로컬 LLM 연동
- 에이전트마다 다른 LLM을 지정하여 비용과 성능을 최적화 가능

> **다음 장 미리보기:** Pydantic으로 에이전트 출력을 구조화하고, Guardrail로 품질을 보장하는 방법을 배웁니다.
