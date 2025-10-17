---
title: 1. LangChain 개발환경
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 1
permalink: llm/langchain/install
---
# LangChain

## 수업전 체크리스트 

### 기존 설치 환경에 문제가 있어서 제거할 경우 

#### 1. Microsoft Visual Studio Code, Miniconda3 혹은 Anaconda 제거

#### 2. 폴더 제거
사용자계정 폴더의 .conda, .ipython, .vscode, miniconda3 폴더와 .condarc 파일을 제거.  
C:\Users\사용자계정\AppData\Roaming\Code 폴더도 제거.  

### 환경 설정
[ 실습 환경 설정 ]

#### 1. miniconda3를 설치합니다. (비영리기관에서는 Anaconda 설치해도 상관없음.) 
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

#### 4. Conda 가상 환경(langchain_env)을 만들고 확인합니다.

```bash
conda create -n langchain_env python=3.12 -y

conda env list          
# conda environments:
#
base             C:\Users\사용자계정\miniconda3
langchain_env    C:\Users\사용자계정\miniconda3\envs\langchain_env   
```

#### 5. Conda 가상 환경(langchain_basic_env)을 활성화 합니다.

```bash
conda activate langchain_env
(langchain_env) C:\Users\사용자계정>
```

#### 6. Jupyter Notebook을 설치합니다.

```bash
conda install notebook -y
```

#### 7. visual studio code를 설치합니다. 

[visualstudio](https://code.visualstudio.com/Download)

- 확장 탭(CTRL+SHIFT+X)을 선택,  Python 확장팩, Jupyter 확장팩을 설치.  
- 명령팔레트(CTRL+SHIFT+P)를 실행, Python: Select Interpreter를 선택, Conda 가상환경 (langchain_basic_env)을 선택.  
- 탐색기(CTRL+SHIFT+E)를 선택하고, langchain_basic 폴더를 생성하고 폴더 열기
- 터미널(CTRL + J)을 열고, Command Prompt를 선택.  
- 터미널에 Conda 가상환경 (langchain_basic_env) 활성화되었는지 확인.   
- 활성화되어 있지 않을 경우 다음 명령으로 활성화합니다. 

```bash
conda activate langchain_env
(langchain_env) C:\Users\사용자계정\langchain_basic>
```

#### 8. conda 환경 제거 할 경우 명령어

```bash
conda remove --name langchain_env --all
#  --all 옵션은 해당 환경의 모든 패키지 및 설정을 포함해 완전 삭제
```


### 맥에서 제거 후 재설치

#### 1. 아나콘다 경로 확인
```bash
where conda
```

#### 2. 아나콘다 폴더 삭제
```bash
rm -rf ~/anaconda3
# 또는
rm -rf /opt/homebrew/anaconda3
```

#### 3. 쉘 환경설정에서 관련 내용 제거
```bash
# zsh
nano ~/.zshrc

# bash
nano ~/.bash_profile
```

다음과 같은 내용 삭제
```bash
# >>> conda initialize >>>
__conda_setup="$('/Users/username/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
eval "$__conda_setup"
# <<< conda initialize <<<
```

수정 후 저장(Ctrl + O, Enter, Ctrl + X) 하고 반영
```bash
source ~/.zshrc
```

#### 4. 캐시 및 환경 설정 파일 제거

```bash
rm -rf ~/.conda
rm -rf ~/.continuum
rm -rf ~/.anaconda_backup
```

#### 5. 제거확인
```bash
conda --version
```

#### 6. Homebrew로 아나콘다 설치

```bash
brew install --cask anaconda
# 혹은 미니콘다
brew install --cask miniconda
```

```bash
# 설치 후 PATH에 자동 등록되지 않는 경우가 많으므로, 다음 명령으로 환경 변수를 추가
echo 'export PATH="/usr/local/anaconda3/bin:$PATH"' >> ~/.zshrc
# M1/M2 Mac인 경우
echo 'export PATH="/opt/homebrew/anaconda3/bin:$PATH"' >> ~/.zshrc
# 미니콘다인 경우
echo 'export PATH="/opt/homebrew/Caskroom/miniconda/base/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```
