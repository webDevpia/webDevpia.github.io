---
title: 1. LangGraph 개발환경
layout: default
grand_parent: LLM
parent: LangGraph
nav_order: 1
permalink: /llm/langgraph/env
# nav_exclude: true
# search_exclude: true
---

# 개발 환경 준비

<a id="toc"></a>

## 진행 순서

1. [프로젝트 생성 및 패키지 설치](#part1)
2. [.env 파일 생성 방법](#part2)
3. [VS Code 설정](#part3)
4. [Ollama 설치 (로컬 모델 — 무료 대안)](#part4)

<a id="part1"></a>

## 1. 프로젝트 생성 및 패키지 설치 [↑](#toc)

> **선수 학습:** [LangChain 개발환경](/llm/langchain/install)에서 uv 설치를 완료한 상태여야 합니다. uv가 설치되어 있지 않다면 해당 페이지의 1번(uv 설치)을 먼저 진행하세요.

### 프로젝트 생성

 VS Code에서 프로젝트 폴더(`langgraph_proj`)를 만들고  `open folder`로 디렉토리을 열고 시작합니다.
```bash
uv init . --python 3.12
uv sync
```
터미널 창을 kill terminar 로 닫고 다시 열어줍니다. 가상환경이 활성화 되는지 확인합니다.

### 필요 패키지 설치

requirements.txt 파일로 설치하거나 명령어로 설치합니다.

```bash
uv add -r requirements.txt
```

```bash
uv add python-dotenv notebook langgraph langchain-openai langchain-community langchain-tavily langchain-ollama
```

### 설치 확인

```bash
uv run python -c "import langgraph; print('langgraph', langgraph.__version__)"
```

**실행 결과 (예시):**
```
langgraph 1.1.6
```

<a id="part2"></a>

## 2. .env 파일 생성 방법 [↑](#toc)

`.env` 파일은 API 키 등 민감한 정보를 저장하는 환경변수 파일입니다.

1. **파일 생성:** VS Code에서 프로젝트 폴더(`langgraph_proj`)의 최상위 경로에 `.env`라는 이름의 새 파일을 만듭니다.
   - VS Code 탐색기에서 우클릭 → **New File** → 파일명을 `.env`로 입력
2. **내용 작성:** 아래와 같이 API 키를 입력합니다.
   ```
   OPENAI_API_KEY=본인의_OpenAI_API키
   OPENAI_MODEL=gpt-4o-mini
   TAVILY_API_KEY=본인의_tavily_api_key
   ```
3. **주의사항:** `.env` 파일에는 민감한 정보가 담기므로, Git에 업로드되지 않도록 `.gitignore` 파일에 반드시 추가하세요.
   ```
   # .gitignore 파일에 아래 내용 추가
   .env
   ```

<a id="part3"></a>

## 3. VS Code 설정 [↑](#toc)

uv로 생성한 가상환경을 VS Code에 연동합니다.

1. **인터프리터 선택:** VS Code에서 `Ctrl+Shift+P`를 눌러 **"Python: Select Interpreter"**를 실행합니다. 목록에서 `langgraph_proj` 프로젝트의 `.venv` 경로에 있는 **Python 3.12**를 선택합니다. (목록에 보이지 않으면 *Enter interpreter path*를 눌러 `.venv/bin/python` 또는 `.venv/Scripts/python.exe`를 직접 지정합니다.)
2. **환경 확인:** VS Code 하단 상태 바에 `Python 3.12.x ('.venv': venv)`와 같이 표시되면 연동이 완료된 것입니다.
3. **테스트:** 터미널에서 다음을 실행하여 환경이 올바른지 확인합니다.
   ```bash
   uv run python --version
   ```
   `Python 3.12.x`가 출력되면 정상입니다.

> 💡 **Jupyter 노트북 사용 시:** VS Code에서 `.ipynb` 파일을 열고, 커널 선택에서 `.venv`의 Python을 지정하면 됩니다.

<a id="part4"></a>

## 4. Ollama 설치 (로컬 모델 — 무료 대안) [↑](#toc)

OpenAI API 키 없이도 LangGraph를 실습할 수 있습니다. Ollama는 로컬에서 LLM을 실행하는 도구입니다.

1. **Ollama 설치:** [https://ollama.com](https://ollama.com)에서 운영체제에 맞는 버전을 다운로드하여 설치합니다.

2. **모델 다운로드:** 터미널에서 다음 명령을 실행합니다.
   ```bash
   ollama pull gemma3:1b
   ```

3. **사용법:** 코드에서 `ChatOpenAI` 대신 `ChatOllama`를 사용합니다.
   ```python
   # OpenAI 사용 시
   from langchain_openai import ChatOpenAI
   llm = ChatOpenAI(model="gpt-4o-mini")

   # Ollama 사용 시 (무료, 로컬 실행)
   from langchain_ollama import ChatOllama
   llm = ChatOllama(model="gemma3:1b")
   ```
   이후 코드는 동일하게 사용할 수 있습니다. 이 교안의 모든 예제에서 `ChatOpenAI` 부분을 위와 같이 교체하면 됩니다.

> 🔑 **참고:** Ollama는 인터넷 연결 없이도 사용할 수 있으며, API 비용이 발생하지 않습니다. 다만 최초 모델 다운로드 시에는 인터넷이 필요합니다 (gemma3:1b 약 815MB).


→ **다음 장**: [2. LangGraph 기본 개념](/llm/langgraph/preview)
