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

1. [개발 환경 준비 가이드](#part1)
2. [.env 파일 생성 방법](#part2)
3. [VS Code에서 conda 가상환경 연동 방법](#part3)
4. [Ollama 설치 (로컬 모델 — 무료 대안)](#part4)

<a id="part1"></a>

## 1. 개발 환경 준비 가이드 [↑](#toc)

### Python 3.12용 conda 가상환경 생성

1. **가상환경 생성:** Anaconda Prompt에서 다음 명령을 실행합니다.  
   ```
   conda create -n langgraph_env python=3.12 -y
   ```  
  
2. **환경 활성화:** 환경을 생성한 후 아래 명령으로 해당 환경을 활성화합니다.  
   ```
   conda activate langgraph_env
   ```  

3. **필요 패키지 설치:** 이 환경에 개발에 필요한 패키지를 추가로 설치합니다:  
   ```
   pip install python-dotenv notebook langgraph langchain-openai langchain-community langchain-tavily tavily-python
   ```

<a id="part2"></a>

### .env 파일 생성 방법 [↑](#toc)

`.env` 파일은 API 키 등 민감한 정보를 저장하는 환경변수 파일입니다.

1. **파일 생성:** VS Code에서 프로젝트 폴더의 최상위 경로에 `.env`라는 이름의 새 파일을 만듭니다.
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

### VS Code에서 conda 가상환경 연동 방법 [↑](#toc)

앞서 생성한 conda 가상환경(langgraph_env)을 VS Code에 연동하여, 터미널과 디버거, 에디터가 모두 해당 환경의 Python을 사용하도록 설정해야 합니다. 설정하는 방법은 아래와 같습니다:

1. **인터프리터 선택:** VS Code에서 `Ctrl+Shift+P`를 눌러 **“Python: Select Interpreter”**를 실행합니다. 그러면 설치된 Python 인터프리터 목록이 나타나는데, 여기서 **langgraph_basic (Python 3.12)**와 같은 항목을 찾아 선택합니다. (목록에 바로 보이지 않는 경우, *Enter interpreter path*를 눌러 Miniconda 설치 경로의 `envs/langgraph_env/python.exe`를 직접 지정할 수도 있습니다.)
2. **환경 활성화 확인:** 인터프리터를 선택하면 VS Code 하단 상태 바에 선택된 Python 버전과 환경명이 표시됩니다. 예를 들어 `Python 3.12.0 64-bit ('langgraph_env': conda)`처럼 보입니다. 또한 새 터미널을 열 때 자동으로 `conda activate langgraph_env`가 실행되어 해당 환경이 활성화된 터미널이 열리게 됩니다.
3. **테스트:** 터미널 패널에서 `python --version`을 쳐서 3.12 버전이 출력되는지 확인합니다. 또, 간단한 파이썬 파일을 열고 실행해보거나 (우클릭 -> **터미널에서 Python 파일 실행**), 혹은 Jupyter 노트북을 열어 커널로 해당 환경의 파이썬을 선택해 보는 방식으로 환경이 올바르게 연결되었는지 테스트합니다.

이제 VS Code에서 파이썬 파일을 실행하거나 디버깅할 때 langgraph_env 가상환경이 사용됩니다.

<a id="part4"></a>

### Ollama 설치 (로컬 모델 — 무료 대안) [↑](#toc)

OpenAI API 키 없이도 LangGraph를 실습할 수 있습니다. Ollama는 로컬에서 LLM을 실행하는 도구입니다.

1. **Ollama 설치:** [https://ollama.com](https://ollama.com)에서 운영체제에 맞는 버전을 다운로드하여 설치합니다.

2. **모델 다운로드:** 터미널에서 다음 명령을 실행합니다.
   ```bash
   ollama pull llama3.2
   ```

3. **패키지 설치:** LangChain Ollama 연동 패키지를 설치합니다.
   ```bash
   pip install langchain-ollama
   ```

4. **사용법:** 코드에서 `ChatOpenAI` 대신 `ChatOllama`를 사용합니다.
   ```python
   # OpenAI 사용 시
   from langchain_openai import ChatOpenAI
   llm = ChatOpenAI(model="gpt-4o-mini")

   # Ollama 사용 시 (무료, 로컬 실행)
   from langchain_ollama import ChatOllama
   llm = ChatOllama(model="llama3.2")
   ```
   이후 코드는 동일하게 사용할 수 있습니다. 이 교안의 모든 예제에서 `ChatOpenAI` 부분을 위와 같이 교체하면 됩니다.

> 🔑 **참고:** Ollama는 인터넷 연결 없이도 사용할 수 있으며, API 비용이 발생하지 않습니다. 다만 최초 모델 다운로드 시에는 인터넷이 필요합니다 (llama3.2 약 2GB).

