---
title: LangChain
layout: default
parent: AI
nav_order: 5
permalink: /ai/langchain
# nav_exclude: true
# search_exclude: true
---
# LangChain

## 수업전 체크리스트 

### 기존 설치 환경 제거 시 
1. Microsoft Visual Studio Code, Miniconda3 혹은 Anaconda 제거
2. 사용자계정 폴더의 .conda, .ipython, .vscode, miniconda3 폴더와 .condarc 파일을 제거.   
   C:\Users\사용자계정\AppData\Roaming\Code 폴더도 제거.  

### 환경 설정
[ 실습 환경 설정 ]

1. miniconda3를 설치합니다.

https://docs.anaconda.com/miniconda/install/#quick-command-line-install

윈도우즈 커맨드 프롬프트에서 다음 명령을 입력해 실행합니다.
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
start /wait "" .\miniconda.exe /S
del miniconda.exe


2. 시작 > Miniconda3 (64-bit) > Anaconda Prompt (miniconda)를 실행합니다.

3. 패키지 다운로드를 위한 conda-forge 리포지토리  채널을 추가하고, 채널 우선 순위를 변경합니다.

conda config --show channels 
channels:   
  - defaults
  
conda config --add channels conda-forge && conda config --set channel_priority strict

conda config --show channels
channels:
  - conda-forge
  - defaults

4. Conda 가상 환경(langchain_basic_env)을 만들고 확인합니다.

conda create -n langchain_basic_env python=3.12 -y

conda info --envs                      
# conda environments:
#
base                              C:\Users\사용자계정\miniconda3
langchain_basic_env    C:\Users\사용자계정\miniconda3\envs\langchain_basic_env   

5.Conda 가상 환경(langchain_basic_env)을 활성화 합니다.

conda activate langchain_basic_env
(langchain_basic_env) C:\Users\사용자계정>

6. Jupyter Notebook을 설치합니다.

conda install notebook -y

7. Anaconda Prompt (miniconda) 창을 닫습니다.

8. visual studio code를 설치합니다. 

https://code.visualstudio.com/Download

9. visual studio code를 실행합니다. 

10. 확장 탭(CTRL+SHIFT+X)을 선택합니다.

11. Korean Language Pack for Visual Studio Code 확장팩을 설치하고, 재실행 버튼을 눌러 visual studio code를 재실행합니다.

12. Python 확장팩을 설치합니다.

13. Jupyter 확장팩을 설치합니다.

14. 탐색기(CTRL+SHIFT+E)를 선택합니다. / 폴더 열기를 누릅니다. / langchain_basic 폴더를 생성합니다. / langchain_basic 폴더를 선택합니다.

15. 명령팔레트(CTRL+SHIFT+P)를 실행합니다. / Python: Select Interpreter를 선택합니다. / Conda 가상환경 (langchain_basic_env)을 선택합니다.  

16. 터미널(CTRL + J)을 엽니다. / Command Prompt를 선택합니다.

17. 터미널에 Conda 가상환경 (langchain_basic_env) 활성화되었는지 확인합니다. 활성화되어 있지 않을 경우 다음 명령으로 활성화합니다. 
conda activate langchain_basic_env
(langchain_basic_env) C:\Users\사용자계정\langchain_basic>

18. python-dotenv 패키지를 설치합니다. 
conda install python-dotenv -y 

19. .env 파일에 OpenAI 개발자 플랫폼에서 생성한 API secret key를 OPENAI API_KEY=xxxxxxxxxxxxxxxxxxx 형식으로 등록합니다.

20. VSCode를 재시작 후 터미널에서 echo %OPENAI_API_KEY% 명령으로 API key를 확인합니다.


