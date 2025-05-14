---
title: LangChain
layout: default
parent: LangChain
nav_order: 2
permalink: /langchain/langchain
# nav_exclude: true
# search_exclude: true
---
# LangChain

## 수업전 체크리스트 

### 기존 설치 환경 제거 시 

#### 1. Microsoft Visual Studio Code, Miniconda3 혹은 Anaconda 제거'

#### 2. 폴더 제거
사용자계정 폴더의 .conda, .ipython, .vscode, miniconda3 폴더와 .condarc 파일을 제거.  
C:\Users\사용자계정\AppData\Roaming\Code 폴더도 제거.  

### 환경 설정
[ 실습 환경 설정 ]

#### 1. miniconda3를 설치합니다.  
[Quick command line install](https://docs.anaconda.com/miniconda/install/#quick-command-line-install)

```bash
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
start /wait "" .\miniconda.exe /S
del miniconda.exe
```

#### 2. 시작 > Miniconda3 (64-bit) > Anaconda Prompt (miniconda)를 실행합니다.

#### 3. 채널 추가 및 변경 
패키지 다운로드를 위한 conda-forge 리포지토리 채널을 추가하고, 채널 우선 순위를 변경합니다.  
(아나콘다는 비영리기관에서만 무료 사용 가능) 

```bash
conda config --show channels 

channels:   
  - defaults
```

```bash  
conda config --add channels conda-forge && conda config --set channel_priority strict

conda config --show channels

channels:
  - conda-forge
  - defaults
```

#### 4. Conda 가상 환경(langchain_basic_env)을 만들고 확인합니다.

```bash
conda create -n langchain_basic_env python=3.12 -y

conda info --envs                      
# conda environments:
#
base                   C:\Users\사용자계정\miniconda3
langchain_basic_env    C:\Users\사용자계정\miniconda3\envs\langchain_basic_env   
```

#### 5. Conda 가상 환경(langchain_basic_env)을 활성화 합니다.

```bash
conda activate langchain_basic_env
(langchain_basic_env) C:\Users\사용자계정>
```

#### 6. Jupyter Notebook을 설치합니다.

```bash
conda install notebook -y
```

#### 7. visual studio code를 설치합니다. 

[visualstudio](https://code.visualstudio.com/Download)

확장 탭(CTRL+SHIFT+X)을 선택,  Python 확장팩, Jupyter 확장팩을 설치.  
명령팔레트(CTRL+SHIFT+P)를 실행, Python: Select Interpreter를 선택, Conda 가상환경 (langchain_basic_env)을 선택.  
탐색기(CTRL+SHIFT+E)를 선택하고, langchain_basic 폴더를 생성하고 폴더 열기
터미널(CTRL + J)을 열고, Command Prompt를 선택.  
터미널에 Conda 가상환경 (langchain_basic_env) 활성화되었는지 확인.   
활성화되어 있지 않을 경우 다음 명령으로 활성화합니다. 

```bash
conda activate langchain_basic_env
(langchain_basic_env) C:\Users\사용자계정\langchain_basic>
```

## env 파일 로드 테스트

```bash
conda install python-dotenv -y 
```

.env
```
OPENAI API_KEY=xxxxxxxxxxxxxxxxxxx
```

01_env_config_test.py
```python
from dotenv import load_dotenv
import os

# dotenv 라이브러리로 .env 파일을 로드
load_dotenv()

# 환경 변수에서 OPENAI_API_KEY를 읽어와 출력
print(os.getenv('OPENAI_API_KEY'))
```

## LangChain

### 연결테스트

```bash
pip install langchain
pip install langchain_openai
pip install langchain_ollama
```

02_hello.py
```python
import langchain
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()

print(f"langchain: {langchain.__version__}")
print(os.getenv('OPENAI_API_KEY'))

ollama_url = "http://127.0.0.1:11434"  
lmstudio_url = "http://127.0.0.1:1234/v1"

# llm = OllamaLLM(model="gemma3:1b", base_url=ollama_url)
# llm = ChatOpenAI(model="gemma-3-1b-it", base_url=lmstudio_url, api_key="dummy")
llm = ChatOpenAI(model="gpt-4.1-nano")

print(llm)

#system(시스템 지시) 및 human(사용자 질문) 메시지를 포함한 메시지 리스트 생성

# messages = [
#     SystemMessage("당신은 서울의 음식과 문화에 대한 전문가입니다."),
#     HumanMessage("서울을 대표하는 음식을 맛볼 수 있는 레스토랑 5개를 추천해 주세요.")
# ]

messages = [
    ("system", "당신은 서울의 음식과 문화에 대한 전문가입니다."),
    ("human", "서울을 대표하는 음식을 맛볼 수 있는 레스토랑 5개를 추천해 주세요.")
]

ai_message = llm.invoke(messages)

# print(ai_message)
print(ai_message.content)

```

### 기본사용법

03_chat_model.py
```python
import langchain
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()

ollama_url = "http://127.0.0.1:11434"  
lmstudio_url = "http://127.0.0.1:1234/v1"

# llm = OllamaLLM(model="gemma3:1b", base_url=ollama_url)
# llm = ChatOpenAI(model="gemma-3-1b-it", base_url=lmstudio_url, api_key="dummy")
llm = ChatOpenAI(model="gpt-4.1-nano")

# invoke(): 단일 요청 처리
# [ INVOKE ]
# messages = [
#     ("system", "당신은 서울의 음식과 문화에 대한 전문가입니다."),
#     ("human", "서울 광장시장에서 먹을 만한 길거리 음식을 소개해 주세요.")
# ]

# ai_message = llm.invoke(messages)
# print(ai_message.content)

# batch(): 여러 요청을 한 번에 처리
# [ BATCH ]
# messages = [
#     [("system", "당신은 서울의 음식에 대한 전문가입니다."),
#     ("human", "서울 광장시장에서 먹을 만한 길거리 음식을 소개해 주세요.")],
#     [("system", "당신은 서울의 문화에 대한 전문가입니다."),
#     ("human", "서울에서 데이트할 떄 가 볼 만한 분위기 좋은 곳을 알려주세요.")]
# ]

# ai_messages = llm.batch(messages)
# for ai_message in ai_messages:
#     print(ai_message.content)
#     print()

#stream(): 응답을 실시간으로 스트리밍하여 출력
# [STERAM]
messages = [
    ("system", "당신은 서울의 문화에 대한 전문가입니다."),
    ("human", "서울에서 데이트할 떄 가 볼 만한 분위기 좋은 곳을 알려주세요.")
]

ai_message = llm.stream(messages)
for chunk in ai_message:
    print(chunk.content, end="")
```

### 동기 방식, 비동기 방식

04_chat_async.py

```python
import langchain
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os
import asyncio
import time

# ainvoke()로 비동기 호출 수행
async def invoke_async(llm, messages):
    ai_message = await llm.ainvoke(messages)
    print(ai_message.content)

# asyncio.gather()로 여러 요청을 병렬 처리
async def invoke_parallel(llm, messages):
    tasks = [invoke_async(llm, messages) for _ in range(10)]
    await asyncio.gather(*tasks)

load_dotenv()

ollama_url = "http://127.0.0.1:11434"  
lmstudio_url = "http://127.0.0.1:1234/v1"

# llm = OllamaLLM(model="gemma3:1b", base_url=ollama_url)
# llm = ChatOpenAI(model="gemma-3-1b-it", base_url=lmstudio_url, api_key="dummy")
llm = ChatOpenAI(model="gpt-4.1-nano")

messages = [
    ("system", "당신은 서울의 문화에 대한 전문가입니다."),
    ("human", "서울에서 데이트할 떄 가 볼 만한 분위기 좋은 곳을 알려주세요.")
]

start = time.perf_counter()

# print("Sync")
# for _ in range(10):
#     ai_message = llm.invoke(messages)
#     print(ai_message.content)
#     print()

print("Async")
asyncio.run(invoke_parallel(llm, messages))

end = time.perf_counter()
print(f"Elapsed time: {end - start:.2f} seconds")
```

### 대화 기록을 관리하는 두 가지 방법 비교
이전 대화를 기억하고 맥락을 유지하는 방법에 직접 메시지 리스트를 관리하는 방식과 LangChain의 ChatMessageHistory 클래스를 사용하는 방식. 

05_message_history.py

```python
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv


load_dotenv()

ollama_url = "http://127.0.0.1:11434"  
lmstudio_url = "http://127.0.0.1:1234/v1"

# llm = OllamaLLM(model="gemma3:1b", base_url=ollama_url)
# llm = ChatOpenAI(model="gemma-3-1b-it", base_url=lmstudio_url, api_key="dummy")
llm = ChatOpenAI(model="gpt-4.1-nano")

# 직접 메시지 리스트를 관리하는 방식

# messages = [
#     SystemMessage("당신은 여행 전문가로 고객의 여행 일정에 도움을 줍니다."),
#     HumanMessage("부산 여행에서 딱 한 곳만을 가봐야 한다면 어떤 곳인지 알려주세요.")
# ]

# ai_message = llm.invoke(messages)
# messages.append(ai_message)
# messages.append(HumanMessage("부산역에서 그 곳에 가는 교통편을 알려주세요. "))
# ai_message = llm.invoke(messages)
# messages.append(HumanMessage("그 근처에서 먹을 만한 음식점들을을 추천해해주세요."))
# ai_message = llm.invoke(messages)
# messages.append(ai_message)
# for message in messages:
#     print(type(message), message)


# LangChain의 ChatMessageHistory 클래스를 사용하는 방식

history = ChatMessageHistory()

history.add_message(SystemMessage("당신은 여행 전문가로 고객의 여행 일정에 도움을 줍니다."))
history.add_user_message("부산 여행에서 딱 한 곳만을 가봐야 한다면 어떤 곳인지 알려주세요.")
ai_message = llm.invoke(history.messages)

history.add_ai_message(ai_message.content)
history.add_user_message("부산역에서 그 곳에 가는 교통편을 알려주세요.")
ai_message = llm.invoke(history.messages)

history.add_ai_message(ai_message.content)
history.add_user_message("그 근처에서 먹을 만한 음식점들을을 추천해해주세요.")
ai_message = llm.invoke(history.messages)

history.add_ai_message(ai_message.content)

for message in history.messages:
    print(type(message), message)
```

### ConversationBufferMemory를 사용한 대화 기억 관리

06_memory.py

```python
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()

ollama_url = "http://127.0.0.1:11434"  
lmstudio_url = "http://127.0.0.1:1234/v1"

# llm = OllamaLLM(model="gemma3:1b", base_url=ollama_url)
# llm = ChatOpenAI(model="gemma-3-1b-it", base_url=lmstudio_url, api_key="dummy")
llm = ChatOpenAI(model="gpt-4.1-nano")

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
memory.clear()

memory.save_context({"human": "안녕하세요, 챗봇님"}, 
                    {"bot": "안녕하세요! 반가워요, 호칭을 어떠게 하는게 좋을까요?"})
memory.save_context({"human": "음, 전 홍길동입니다."}, 
                    {"bot": "네, 홍길동님! 만나서 반갑습니다."})
memory.save_context({"human": "경복궁을 가고 싶은데 혹시 어떻게 가는지 알려 줄 수 있나요?"}, 
                    {"bot": "물론이죠. 경복궁은 지하철 3호선을 타고 가면 편리해요."})

print(memory.load_memory_variables({}))
```

### PromptTemplate을 사용한 템플릿 기반 프롬프트 생성

07_prompt_template.py

```python
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.prompts import PromptTemplate, load_prompt
from dotenv import load_dotenv

load_dotenv()

ollama_url = "http://127.0.0.1:11434"  
lmstudio_url = "http://127.0.0.1:1234/v1"

# llm = OllamaLLM(model="gemma3:1b", base_url=ollama_url)
# llm = ChatOpenAI(model="gemma-3-1b-it", base_url=lmstudio_url, api_key="dummy")
llm = ChatOpenAI(model="gpt-4.1-nano")

# 변수를 포함한 템플릿 정의 및 값 주입
template = PromptTemplate.from_template("{city}에서 {adjective} {topic}을 알려주세요.")
prompt = template.format(city="서울", adjective="가장 유명한", topic="맛집")

ai_message = llm.invoke(prompt)
print(ai_message.content)

# 템플릿을 파일로 저장하고 다시 로드하는 방법
template.save("template.json")
template = load_prompt("template.json")
prompt = template.format(city="부산", adjective="가장 맛있는", topic="음식점")

ai_message = llm.invoke(prompt)
print(ai_message.content)
```

### LangChain Expression Language(LCEL)을 사용한 체인 생성

08_lcel.ipynb

```python
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

ollama_url = "http://127.0.0.1:11434"  
lmstudio_url = "http://127.0.0.1:1234/v1"

# llm = OllamaLLM(model="gemma3:1b", base_url=ollama_url)
# llm = ChatOpenAI(model="gemma-3-1b-it", base_url=lmstudio_url, api_key="dummy")
llm = ChatOpenAI(model="gpt-4.1-nano")

# 파이프라인(|) 연산자를 사용한 간결한 체인 구성
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

prompt = PromptTemplate.from_template("{city}에서 가장 유명한 랜드마크가 무엇인가요?")
chain = LLMChain(llm=llm, prompt=prompt)
chain.invoke({"city": "파리"})

chain = prompt | llm # LCEL
chain.invoke({"city": "파리"})


# SequentialChain을 사용한 여러 단계의 체인 연결
# 첫 번째 체인의 출력이 두 번째 체인의 입력으로 사용되는 구조

from langchain.chains import SequentialChain

p_1 = PromptTemplate.from_template("{city}에서 가장 유명한 랜드마크가 무엇인가요? 설명은 필요없고 딱 이름 하나만 알려주세요.")
p_2 = PromptTemplate.from_template("{landmark}에 {transport}로 가려면 어떻게 가나요?")

c_1 = LLMChain(llm=llm, prompt=p_1, verbose=True, output_key="landmark")
c_2 = LLMChain(llm=llm, prompt=p_2, verbose=True)

chain = SequentialChain(chains=[c_1, c_2], input_variables=["city", "transport"], verbose=True)

chain.invoke({"city": "서울", "transport": "지하철"})
```
