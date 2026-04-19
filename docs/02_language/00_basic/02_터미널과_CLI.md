---
title: "02. 터미널과 CLI"
layout: default
parent: 기초 도구
grand_parent: Language
nav_order: 2
permalink: /language/basic/terminal
---

# 02. 터미널과 CLI
{: .no_toc }

> 코드를 작성하기 전에, 파일과 폴더를 다루는 방법을 손에 익혀야 한다.  
> 터미널은 낯설지만, 익숙해지면 가장 빠른 도구가 된다.

---

## 학습 목표
{: .no_toc }

- 터미널이 무엇인지, GUI와 어떻게 다른지 이해한다
- `pwd`, `cd`, `ls` 명령어로 현재 위치를 파악하고 이동할 수 있다
- 절대경로와 상대경로의 차이를 설명할 수 있다
- `mkdir`, `touch`, `rm`, `mv`, `cp`로 파일과 폴더를 다룰 수 있다
- 환경변수와 `.env` 파일의 역할을 이해한다

---

<a id="toc"></a>

## 진행 순서
{: .no_toc }

1. [터미널이란?](#1)
2. [현재 위치 확인 — pwd / cd](#2)
3. [폴더 이동과 목록 — cd / ls](#3)
4. [폴더와 파일 만들기 — mkdir / touch](#4)
5. [파일 삭제와 이동 — rm / mv / cp](#5)
6. [환경변수와 .env](#6)
7. [정리](#7)

---

## 1️⃣ 터미널이란? [↑](#toc)

### 비유: 음성 주문 vs 키오스크

카페에서 주문하는 방법은 두 가지다.

- **키오스크(GUI)**: 화면을 눈으로 보면서 버튼을 누른다. 직관적이지만 메뉴가 많으면 느리다.
- **음성 주문(CLI)**: "아메리카노 한 잔"이라고 말한다. 정확히 알면 훨씬 빠르다.

**터미널(Terminal)**은 컴퓨터에게 텍스트 명령을 직접 입력하는 창이다.  
**CLI(Command Line Interface)**는 그 명령어 기반의 인터페이스를 뜻한다.

### GUI vs CLI 비교

| 구분 | GUI (그래픽 인터페이스) | CLI (명령줄 인터페이스) |
|:---|:---|:---|
| 조작 방식 | 마우스로 클릭 | 키보드로 명령어 입력 |
| 학습 난이도 | 쉬움 | 처음엔 어렵지만 빠름 |
| 자동화 | 어렵다 | 스크립트로 반복 가능 |
| 원격 서버 | 화면이 없으면 불가 | 언제나 사용 가능 |
| 사용 예 | 파일 탐색기, 아이콘 클릭 | `cd`, `mkdir`, `git` |

프로그래밍을 하면 서버, Git, Python 등 모든 곳에서 CLI를 쓴다.  
처음엔 낯설어도, 결국 CLI가 더 빠르다는 것을 느끼게 된다.

### VS Code에서 터미널 열기

VS Code 안에 터미널이 내장되어 있다.

| 방법 | 단축키 |
|:---|:---|
| 터미널 열기/닫기 | <kbd>Ctrl</kbd> + <kbd>`</kbd> (백틱) |
| 새 터미널 추가 | <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd> |
| 메뉴에서 열기 | 상단 메뉴 → Terminal → New Terminal |

> **백틱(`)** 은 키보드 왼쪽 위, `1` 키 바로 왼쪽에 있다.

VS Code 터미널을 열면 아래쪽에 검은 창이 나타난다.  
Mac/Linux는 **bash** 또는 **zsh**, Windows는 **PowerShell** 또는 **Command Prompt**가 기본으로 열린다.

---

## 2️⃣ 현재 위치 확인 — pwd / cd [↑](#toc)

### "나는 지금 어디에 있는가?"

터미널을 열면 내가 지금 **어느 폴더에 있는지** 알아야 한다.  
파일 탐색기에서 "현재 폴더"를 보는 것과 같다.

| 운영체제 | 명령어 | 의미 |
|:---|:---|:---|
| Mac / Linux | `pwd` | **P**rint **W**orking **D**irectory — 현재 경로 출력 |
| Windows (PowerShell) | `cd` 또는 `pwd` | 현재 경로 출력 |

```bash
# Mac / Linux
$ pwd
/Users/sunny/projects/my-app
```

```powershell
# Windows PowerShell
PS C:\Users\sunny\projects\my-app> pwd

Path
----
C:\Users\sunny\projects\my-app
```

결과로 나오는 텍스트가 **현재 내 위치(경로)**다.

### 경로(Path)란?

경로는 파일이나 폴더가 어디에 있는지 알려주는 주소다.

- Mac/Linux: `/Users/sunny/projects/my-app`  (슬래시 `/` 구분)
- Windows: `C:\Users\sunny\projects\my-app` (역슬래시 `\` 구분)

---

## 3️⃣ 폴더 이동과 목록 — cd / ls [↑](#toc)

### 폴더 이동 — cd

`cd` = **C**hange **D**irectory. 폴더 안으로 들어가거나 나온다.

```bash
cd 폴더이름        # 하위 폴더로 이동
cd ..             # 상위 폴더로 이동 (한 칸 올라감)
cd ../..          # 두 칸 올라감
cd ~              # 홈 폴더로 이동 (Mac/Linux)
cd /              # 최상위 폴더로 이동
```

### 폴더 목록 보기 — ls / dir

현재 폴더 안에 무엇이 있는지 확인한다.

| 운영체제 | 명령어 | 설명 |
|:---|:---|:---|
| Mac / Linux | `ls` | 파일·폴더 목록 |
| Mac / Linux | `ls -l` | 상세 정보 포함 목록 |
| Mac / Linux | `ls -a` | 숨김 파일 포함 |
| Windows | `dir` | 파일·폴더 목록 |

```bash
$ ls
README.md   index.html   src/   package.json

$ ls -l
total 24
-rw-r--r--  1 sunny  staff   412 Apr 15 10:00 README.md
drwxr-xr-x  3 sunny  staff    96 Apr 15 10:00 src/
```

### 절대경로 vs 상대경로

| 구분 | 설명 | 예시 |
|:---|:---|:---|
| **절대경로** | 최상위 폴더부터 전체 주소 | `/Users/sunny/projects/my-app` |
| **상대경로** | 현재 위치 기준의 주소 | `./src`, `../images` |

- `.` (점 하나) = 현재 폴더
- `..` (점 두 개) = 상위 폴더

```bash
# 현재 위치: /Users/sunny/projects
cd my-app          # 상대경로: 현재 폴더 안의 my-app으로 이동
cd /Users/sunny    # 절대경로: 어디서든 /Users/sunny로 이동
```

### Tab 자동완성

폴더나 파일 이름을 입력하다가 <kbd>Tab</kbd> 키를 누르면 자동으로 완성된다.

```bash
cd pr[Tab]    →    cd projects/
```

이름이 여러 개 겹치면 <kbd>Tab</kbd> 을 두 번 눌러서 목록을 본다.  
**Tab 자동완성은 터미널에서 가장 중요한 습관이다.**

---

## 4️⃣ 폴더와 파일 만들기 — mkdir / touch [↑](#toc)

### 폴더 만들기 — mkdir

`mkdir` = **M**ake **Dir**ectory

```bash
mkdir my-project              # my-project 폴더 생성
mkdir -p src/components       # 중간 폴더도 같이 생성 (Mac/Linux)
mkdir src\components          # Windows
```

### 파일 만들기 — touch / ni

| 운영체제 | 명령어 | 예시 |
|:---|:---|:---|
| Mac / Linux | `touch 파일명` | `touch index.html` |
| Windows PowerShell | `ni 파일명` | `ni index.html` |

```bash
# Mac / Linux
touch index.html
touch README.md

# Windows PowerShell
ni index.html
ni README.md
```

> `touch`는 원래 "파일의 수정 시각을 갱신"하는 명령이지만,  
> 파일이 없으면 빈 파일을 새로 만든다. 실무에서 새 파일 생성에 가장 많이 쓴다.

### 실습: 프로젝트 폴더 구조 만들기

다음 구조를 터미널로 직접 만들어보자.

```
my-project/
├── index.html
├── README.md
└── src/
    ├── style.css
    └── main.js
```

```bash
# 1. 프로젝트 폴더 생성 및 이동
mkdir my-project
cd my-project

# 2. 파일 생성
touch index.html
touch README.md

# 3. src 하위 폴더 및 파일 생성
mkdir src
touch src/style.css
touch src/main.js

# 4. 결과 확인
ls
ls src
```

---

## 5️⃣ 파일 삭제와 이동 — rm / mv / cp [↑](#toc)

### 파일 삭제 — rm

```bash
rm 파일명            # 파일 삭제
rm -r 폴더명         # 폴더와 내용 전체 삭제 (Mac/Linux)
```

> ⚠️ **경고: rm은 휴지통이 없다.**  
> `rm`으로 삭제하면 복구할 수 없다. 특히 `rm -rf /`처럼 잘못 입력하면 시스템 전체가 날아간다.  
> **삭제 전에 반드시 경로를 두 번 확인하자.**

Windows에서는 `del 파일명`, `rmdir /s 폴더명`을 사용한다.

### 파일 이동 및 이름 변경 — mv

`mv` = **M**o**v**e. 이동과 이름 변경 모두 `mv`로 한다.

```bash
mv old.txt new.txt           # 이름 변경
mv file.txt ./src/           # src 폴더로 이동
mv src/ ../backup/           # 폴더 이동
```

### 파일 복사 — cp

```bash
cp file.txt file_copy.txt    # 파일 복사
cp -r src/ src_backup/       # 폴더 복사 (Mac/Linux, -r 필요)
```

### 명령어 요약

| 명령어 | Mac/Linux | Windows (PowerShell) |
|:---|:---|:---|
| 삭제 | `rm 파일`, `rm -r 폴더` | `del 파일`, `rmdir /s 폴더` |
| 이동/이름 변경 | `mv 원본 대상` | `mv 원본 대상` |
| 복사 | `cp 원본 대상` | `cp 원본 대상` |

---

## 6️⃣ 환경변수와 .env [↑](#toc)

### 환경변수란?

환경변수(Environment Variable)는 **운영체제 전체에서 사용할 수 있는 설정값**이다.  
비유하자면, 건물 전체에 공유되는 "안내판" 같은 것이다.  
어떤 프로그램에서든 이 값을 읽어올 수 있다.

```bash
# 환경변수 확인 (Mac/Linux)
echo $HOME        # /Users/sunny
echo $USER        # sunny

# 환경변수 확인 (Windows)
echo %USERPROFILE%   # C:\Users\sunny
```

### PATH 환경변수

`PATH`는 가장 중요한 환경변수다.  
터미널에서 `python`, `git`, `node` 같은 명령어를 입력할 때,  
운영체제는 `PATH`에 등록된 폴더들을 순서대로 뒤져서 해당 프로그램을 찾는다.

```bash
# PATH에 어떤 폴더들이 등록되어 있는지 확인
echo $PATH
# 예: /usr/local/bin:/usr/bin:/bin
```

`python3 --version`이 안 된다면, Python이 설치되어 있어도 PATH에 없기 때문일 가능성이 높다.

### .env 파일이란?

`.env` 파일은 **프로젝트에서만 쓰는 비밀 설정값**을 저장하는 파일이다.

```bash
# .env 파일 예시
DATABASE_URL=postgresql://localhost:5432/mydb
SECRET_KEY=my-super-secret-key-12345
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

### API 키를 .env에 저장하는 이유

API 키는 돈과 직결된다. OpenAI, 카카오, 네이버 등 대부분의 API는 키가 노출되면 누군가가 내 계정으로 과금 요청을 보낼 수 있다.

**절대 하면 안 되는 것**: 코드 파일에 API 키를 직접 작성하고 GitHub에 올리기

```python
# 위험한 방법 - 절대 사용 금지
api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
```

**올바른 방법**: `.env` 파일에 저장하고, `.gitignore`에 추가해서 GitHub에 올라가지 않게 한다.

```python
# 안전한 방법
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

```bash
# .gitignore 파일에 반드시 추가
.env
```

> `.env` 파일은 팀원과 공유할 때도 직접 전달하지 않는다.  
> 대신 `.env.example` 파일에 키 이름만 적어서 공유하고, 값은 각자 채운다.

---

## 7️⃣ 정리 [↑](#toc)

### 명령어 요약 표

| 명령어 | 설명 | 예시 |
|:---|:---|:---|
| `pwd` | 현재 위치 출력 | `pwd` |
| `cd 폴더` | 폴더로 이동 | `cd projects` |
| `cd ..` | 상위 폴더로 이동 | `cd ..` |
| `ls` | 파일·폴더 목록 (Mac/Linux) | `ls -l` |
| `dir` | 파일·폴더 목록 (Windows) | `dir` |
| `mkdir 폴더` | 폴더 생성 | `mkdir src` |
| `touch 파일` | 파일 생성 (Mac/Linux) | `touch index.html` |
| `ni 파일` | 파일 생성 (Windows) | `ni index.html` |
| `rm 파일` | 파일 삭제 (복구 불가) | `rm old.txt` |
| `rm -r 폴더` | 폴더 삭제 (복구 불가) | `rm -r build/` |
| `mv 원본 대상` | 이동 또는 이름 변경 | `mv a.txt b.txt` |
| `cp 원본 대상` | 복사 | `cp a.txt a_copy.txt` |
| `echo $변수명` | 환경변수 출력 (Mac/Linux) | `echo $PATH` |

### 학습 체크리스트

- [ ] VS Code에서 <kbd>Ctrl</kbd> + <kbd>`</kbd>로 터미널을 열 수 있다
- [ ] `pwd`로 현재 위치를 확인할 수 있다
- [ ] `cd`로 폴더를 이동할 수 있다
- [ ] `ls`(또는 `dir`)로 폴더 내용을 볼 수 있다
- [ ] 절대경로와 상대경로의 차이를 설명할 수 있다
- [ ] `mkdir`과 `touch`로 폴더와 파일을 만들 수 있다
- [ ] `rm`의 위험성을 알고, 삭제 전 경로를 확인한다
- [ ] `.env` 파일이 무엇인지, 왜 `.gitignore`에 넣는지 설명할 수 있다

---

→ **다음 장**: [03. Markdown](/language/basic/markdown)
