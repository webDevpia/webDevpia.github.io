---
title: 1. LangChain 개발환경
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 1
permalink: /llm/langchain/install
---


## 학습 목표

- uv를 사용하여 LangChain 개발환경을 구축할 수 있다
- requirements.txt로 패키지를 관리할 수 있다

<a id="toc"></a>

## 진행 순서

1. [uv 설치](#part1)
2. [프로젝트 생성](#part2)
3. [패키지 설치](#part3)
4. [자주 쓰는 uv 명령어](#part4)
5. [VS Code 설정](#part5)
6. [Ollama / LM Studio 설치](#part6)
7. [API 키 발급](#part7)
8. [환경변수 설정](#part8)


---

# LangChain 개발환경 설정

## uv란?

[uv](https://docs.astral.sh/uv/)는 Astral(ruff 개발사)이 만든 **Rust 기반 초고속 Python 패키지 매니저**다.
pip, pip-tools, virtualenv, pyenv를 하나로 통합하며, 기존 도구 대비 10~100배 빠르다.

---

<a id="part1"></a>

## 1. uv 설치 [↑](#toc)

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```
# 보안 오류 발생 시:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope currentuser
# 입력 후 실행
```

### 설치 확인

```bash
uv --version
```

---

<a id="part2"></a>

## 2. 프로젝트 생성 [↑](#toc)

VS Code에서 프로젝트 폴더(`langchain_project`)를 만들고 `Open Folder`로 디렉토리를 열고 시작합니다.

```bash
uv init . --python 3.12
uv sync
```

터미널 창을 Kill Terminal로 닫고 다시 열어줍니다. 가상환경이 활성화되는지 확인합니다.

생성되는 파일 구조:

```
langchain_project/
├── .python-version    # Python 버전 고정
├── pyproject.toml     # 프로젝트 설정 및 의존성
├── README.md
└── main.py
```

---

<a id="part3"></a>

## 3. 패키지 설치 [↑](#toc)

프로젝트 루트에 `requirements.txt` 파일을 생성하고, 필요한 패키지를 작성합니다.

### requirements.txt 예시 (Ollama + FAISS 기반 RAG)

```text
langchain
langchain-core
langchain-text-splitters
langchain-community
langchain-ollama
faiss-cpu
pymupdf
python-dotenv
streamlit
```

### requirements.txt 예시 (OpenAI + Pinecone 기반 RAG)

```text
langchain
langchain-core
langchain-text-splitters
langchain-community
langchain-openai
langchain-pinecone
pymupdf
python-dotenv
streamlit
```

### 설치 명령어

```bash
uv add -r requirements.txt
```

> `uv add`는 패키지를 설치하면서 `pyproject.toml`에도 기록합니다. `requirements.txt`에 패키지를 추가/삭제한 후 다시 위 명령어를 실행하면 됩니다.

### requirements.txt 생성

현재 설치된 패키지 목록을 `requirements.txt`로 내보내려면:

```bash
uv pip freeze > requirements.txt
```

> 💡 다른 환경에서 동일한 패키지를 설치할 때 이 파일을 공유하면 됩니다.

---

<a id="part4"></a>

## 4. 자주 쓰는 uv 명령어 [↑](#toc)

| 명령어 | 설명 |
|---|---|
| `uv add 패키지명` | 패키지 설치 및 pyproject.toml에 기록 |
| `uv remove 패키지명` | 패키지 제거 |
| `uv sync` | pyproject.toml 기반으로 환경 동기화 |
| `uv run python main.py` | 가상환경에서 스크립트 실행 |
| `uv run streamlit run app.py` | 가상환경에서 streamlit 실행 |
| `uv lock` | 의존성 잠금 파일 갱신 |
| `uv tree` | 의존성 트리 확인 |
| `uv pip list` | 설치된 패키지 목록 |

---

<a id="part5"></a>

## 5. VS Code 설정 [↑](#toc)

### 확장 설치

1. **Python** (Microsoft) — 필수
2. **Jupyter** (Microsoft) — 노트북 사용 시
3. **Even Better TOML** — pyproject.toml 편집

### 인터프리터 선택

1. `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`) → `Python: Select Interpreter`
2. `.venv` 경로의 Python 선택 (예: `./langchain_project/.venv/bin/python`)

> uv는 프로젝트 디렉터리 내 `.venv` 폴더에 가상환경을 자동 생성합니다. VS Code가 자동으로 감지하는 경우가 많습니다.

### 터미널에서 가상환경 활성화

uv 명령어(`uv run`)를 사용하면 가상환경 활성화 없이 실행 가능하지만, 직접 활성화하려면:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

---

<a id="part6"></a>

## 6. Ollama / LM Studio 설치 (로컬 모델용) [↑](#toc)

이 교재의 예제에서는 OpenAI(유료) 외에 **로컬 LLM**도 사용합니다. 로컬 모델을 쓰려면 아래 중 하나를 설치합니다.

### Ollama 설치

[Ollama 공식 사이트](https://ollama.com)에서 운영체제에 맞는 설치 파일을 다운로드합니다.

```bash
# 설치 확인
ollama --version

# 모델 다운로드 (예시)
ollama pull gemma3:1b
ollama pull nomic-embed-text   # 임베딩 모델 (15장에서 사용)
```

> Ollama는 설치 후 백그라운드에서 자동 실행됩니다. `http://127.0.0.1:11434`에서 API를 제공합니다.

---

<a id="part7"></a>

## 7. API 키 발급 [↑](#toc)

### OpenAI API 키

1. [OpenAI Platform](https://platform.openai.com) 접속 → 회원가입/로그인
2. 좌측 메뉴 **API keys** → **Create new secret key**
3. 생성된 키를 복사하여 `.env` 파일에 저장

### Google AI API 키 (Gemini용)

1. [Google AI Studio](https://aistudio.google.com) 접속 → 로그인
2. **Get API key** → **Create API key**
3. 생성된 키를 복사하여 `.env` 파일에 저장

---

<a id="part8"></a>

## 8. 환경변수 설정 [↑](#toc)

프로젝트 루트에 `.env` 파일을 생성합니다.

```
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AI...
OLLAMA_URL=http://127.0.0.1:11434
```

Python 코드에서 로드:

```python
from dotenv import load_dotenv
load_dotenv()
```

> `.env` 파일은 `.gitignore`에 반드시 추가하여 API 키가 공개 저장소에 올라가지 않도록 합니다.

---

## 자주 발생하는 에러

| 에러 | 원인 | 해결 |
|---|---|---|
| `AuthenticationError` | API 키 미설정 또는 잘못됨 | `.env` 파일 확인, `load_dotenv()` 호출 여부 확인 |
| `ConnectionRefusedError` | Ollama/LM Studio 서버 미실행 | `ollama serve` 또는 LM Studio 실행 확인 |
| `ModuleNotFoundError` | 패키지 미설치 | `uv add -r requirements.txt` 재실행 |
| `openai.RateLimitError` | API 호출 한도 초과 | 잠시 기다린 후 재시도, 또는 유료 플랜 확인 |

---

## 환경 제거

```bash
# 가상환경 제거 (프로젝트 디렉터리 내)
rm -rf .venv

# 다시 생성
uv sync
```

---

## uv vs Conda 비교

| | uv | Conda |
|---|---|---|
| **속도** | 매우 빠름 (Rust 기반) | 느림 |
| **Python 버전 관리** | `uv python install` | `conda create -n env python=3.12` |
| **패키지 소스** | PyPI | conda-forge / defaults |
| **의존성 파일** | `pyproject.toml` + `uv.lock` | `environment.yml` |
| **가상환경 위치** | 프로젝트 내 `.venv/` | `~/miniconda3/envs/` |
| **non-Python 패키지** | 미지원 (시스템 패키지 매니저 필요) | 지원 (CUDA, MKL 등) |

> **참고:** CUDA 드라이버나 시스템 레벨 라이브러리가 필요한 경우(GPU 학습 등)에는 Conda가 여전히 유용하다. 일반적인 LangChain 개발에는 uv가 더 간편하다.


→ **다음 장**: [2. 기본 사용 예제](/llm/langchain/example)
