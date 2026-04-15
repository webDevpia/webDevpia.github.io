---
title: 07. GitHub 연결
layout: default
parent: Git (리뉴얼)
nav_order: 7
permalink: /git-new/github-remote
---

{% raw %}

## 학습 목표

- GitHub에 원격 리포지토리를 만들고 로컬과 연결할 수 있다
- Personal Access Token(PAT)으로 HTTPS 인증을 설정할 수 있다
- `git push`와 `git clone`의 차이를 설명하고 사용할 수 있다
- `git remote add`, `git remote -v`로 원격 정보를 확인할 수 있다

<a id="toc"></a>

## 진행 순서

1. [4-Zone 모델 복습](#part1) - Remote 영역 추가
2. [GitHub에 리포지토리 만들기](#part2) - 웹에서 5분
3. [HTTPS 인증 설정 (PAT)](#part3) - 필수 과정
4. [git remote add](#part4) - 로컬과 원격 연결
5. [git push](#part5) - 클라우드에 올리기
6. [git clone](#part6) - 원격에서 내 컴퓨터로 가져오기
7. [VS Code에서 확인](#part7) - Sync 버튼 활용
8. [정리](#part8) - 핵심 명령어 요약

---

# 07장. GitHub 연결 — 클라우드 백업

> **GitHub = Google Drive for Code.** 내 컴퓨터의 타임머신 기록을 클라우드에 백업합니다. 컴퓨터가 망가져도 코드는 안전하고, 어디서든 접근할 수 있습니다.

---

<a id="part1"></a>

## 1️⃣ 4-Zone 모델 복습 [↑](#toc)

지금까지 우리는 4-Zone 모델의 아래 세 영역에서만 작업했습니다.

```
┌─────────────────────────────────────────┐
│   Zone 4: Remote (GitHub)               │  ← 이번 장에서 연결!
│   클라우드 백업 / 팀 공유                 │
└──────────────┬──────────────────────────┘
               │  git push / git pull
┌──────────────┴──────────────────────────┐
│   Zone 3: Local Repository              │  ← git commit으로 저장
│   내 컴퓨터의 버전 기록                   │
└──────────────┬──────────────────────────┘
               │  git commit
┌──────────────┴──────────────────────────┐
│   Zone 2: Staging Area (포장 상자)       │  ← git add로 담기
└──────────────┬──────────────────────────┘
               │  git add
┌──────────────┴──────────────────────────┐
│   Zone 1: Working Directory (작업 책상)  │  ← 파일을 직접 수정하는 곳
└─────────────────────────────────────────┘
```

이번 장에서 **Zone 4(Remote)**를 GitHub와 연결합니다. 연결하면:

- `git push` → Local Repo → Remote (GitHub)
- `git pull` → Remote (GitHub) → Local Repo

---

<a id="part2"></a>

## 2️⃣ GitHub에 리포지토리 만들기 [↑](#toc)

> "원격 리포지토리 = 내 코드가 클라우드에 저장되는 공간"

---

### 단계별 안내

**1단계: GitHub 로그인**

[github.com](https://github.com) 에 로그인합니다. 계정이 없다면 먼저 가입합니다.

**2단계: 새 리포지토리 만들기**

오른쪽 상단의 `+` 버튼 → **New repository** 클릭

**3단계: 리포지토리 설정**

| 항목 | 권장 설정 | 설명 |
|------|----------|------|
| Repository name | `my-first-repo` | 영문, 숫자, 하이픈 사용 권장 |
| Description | (선택) 간단한 설명 | 나중에 수정 가능 |
| Public / Private | **Private** | 학습 중에는 Private 권장 |
| Add a README file | **체크하지 않음** | 로컬에 이미 파일이 있을 경우 |
| .gitignore | None | 로컬에서 이미 관리 중 |
| License | None | 나중에 추가 가능 |

> ⚠️ **README 체크 주의**: 로컬에 이미 커밋이 있는 상태에서 GitHub에 README를 추가하면 첫 push 시 충돌이 발생합니다. 기존 로컬 리포지토리를 연결할 때는 **README 체크를 해제**하세요.

**4단계: Create repository 클릭**

리포지토리가 생성되면 주소(`https://github.com/username/my-first-repo.git`)가 표시됩니다. 이 주소를 복사해 둡니다.

---

<a id="part3"></a>

## 3️⃣ HTTPS 인증 설정 (PAT) [↑](#toc)

> ⚠️ **필수 섹션!** 2021년 8월부터 GitHub은 비밀번호 로그인을 폐지했습니다. `git push`를 하려면 **Personal Access Token(PAT)**이 필요합니다. 이 단계를 건너뛰면 push에서 막힙니다.

---

### Personal Access Token이란?

PAT = GitHub이 발급하는 임시 비밀번호입니다. 일반 비밀번호 대신 이것을 사용합니다.

---

### PAT 발급 방법 (step-by-step)

**1단계**: GitHub 오른쪽 상단 프로필 사진 클릭 → **Settings**

**2단계**: 왼쪽 사이드바 맨 아래 → **Developer settings**

**3단계**: **Personal access tokens** → **Tokens (classic)**

**4단계**: **Generate new token** → **Generate new token (classic)**

**5단계**: 토큰 설정

| 항목 | 설정 |
|------|------|
| Note | `git-push-token` (설명용 이름) |
| Expiration | **90 days** (학습용) |
| Scopes | `repo` 체크 (전체 repo 권한) |

**6단계**: 페이지 하단 **Generate token** 클릭

**7단계**: 토큰 복사

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ **중요**: 이 페이지를 벗어나면 토큰을 다시 볼 수 없습니다. 반드시 **지금 복사**해서 안전한 곳에 보관하세요 (메모장, 비밀번호 관리자 등).

---

### 토큰 사용 방법

첫 번째 push 시 아이디/비밀번호 입력 창이 뜹니다:

```
Username: (GitHub 아이디 입력)
Password: (PAT 토큰 붙여넣기 — 일반 비밀번호 아님!)
```

> 💡 **팁**: 한 번 입력하면 운영체제의 자격 증명 관리자(Windows: 자격 증명 관리자, macOS: 키체인)가 저장합니다. 다음 번부터는 자동으로 입력됩니다.

---

### 보너스: SSH 키 설정 (선택)

PAT보다 SSH 키 방식이 더 안전하고 편리합니다. 관심 있다면 아래 명령어로 시작하세요:

```bash
# SSH 키 생성
ssh-keygen -t ed25519 -C "your@email.com"

# 공개 키 확인 (GitHub에 등록할 내용)
cat ~/.ssh/id_ed25519.pub
```

공개 키를 **GitHub → Settings → SSH and GPG keys → New SSH key**에 등록합니다. 이후 원격 주소를 `git@github.com:username/repo.git` 형식으로 사용합니다.

> 💡 **팁**: SSH 방식은 토큰 만료 걱정이 없어 실무에서 많이 사용합니다. 하지만 처음에는 HTTPS + PAT 방식으로 시작하는 것이 더 쉽습니다.

---

<a id="part4"></a>

## 4️⃣ git remote add [↑](#toc)

> "로컬 리포지토리에 원격 주소를 등록합니다."

```bash
# 원격 리포지토리 연결
git remote add origin https://github.com/username/my-first-repo.git
```

- `origin` = 원격 리포지토리의 별명(관례적으로 origin을 사용)
- URL = GitHub에서 복사한 주소

---

### 연결 확인

```bash
git remote -v
```

실행 결과:
```
origin  https://github.com/username/my-first-repo.git (fetch)
origin  https://github.com/username/my-first-repo.git (push)
```

`fetch`(내려받기)와 `push`(올리기) 주소가 모두 등록되었습니다.

---

### 원격 주소 변경 / 삭제

```bash
# 주소 변경 (URL을 잘못 입력했을 때)
git remote set-url origin https://github.com/username/correct-repo.git

# 원격 연결 삭제
git remote remove origin
```

> 💡 **팁**: `origin`이라는 이름은 관례입니다. 다른 이름을 써도 되지만, 팀 협업 시 모두가 `origin`을 기대하므로 그대로 사용하세요.

---

<a id="part5"></a>

## 5️⃣ git push [↑](#toc)

> "로컬 리포지토리의 커밋을 GitHub에 올립니다."

```bash
# 처음 push할 때
git push -u origin main
```

실행 결과:
```
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 250 bytes | 250.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/username/my-first-repo.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

### `-u` 플래그의 의미

`-u`(`--set-upstream`)는 "이 브랜치의 기본 원격 위치를 설정합니다"라는 의미입니다.

```bash
# 처음 한 번: -u 플래그 사용
git push -u origin main

# 이후부터는 그냥 git push
git push
```

`-u`를 한 번 설정하면 Git이 "main 브랜치는 origin/main으로 push한다"는 것을 기억합니다. 이후에는 `git push`만 입력하면 됩니다.

---

### GitHub에서 확인하기

push가 완료되면 `https://github.com/username/my-first-repo`에서 파일들을 확인할 수 있습니다.

커밋 메시지, 파일 목록, 변경 이력이 모두 웹에서 보입니다.

---

### push 이후의 일반 워크플로우

```bash
# 파일 수정 후
git add 파일명
git commit -m "커밋 메시지"
git push                    # -u 설정 후에는 이것만 입력
```

> ⚠️ **push = 공개**: push한 커밋은 GitHub에 올라갑니다. Public 리포지토리라면 누구나 볼 수 있습니다. 비밀번호, API 키 등 민감한 정보를 커밋하지 않았는지 확인하세요.

---

<a id="part6"></a>

## 6️⃣ git clone [↑](#toc)

> "이미 GitHub에 있는 프로젝트를 내 컴퓨터로 가져옵니다."

`git push`가 "올리기"라면, `git clone`은 "처음 내려받기"입니다.

---

### 기본 사용법

```bash
# 새 폴더를 만들고 그 안에 내려받기
git clone https://github.com/username/my-first-repo.git

# 결과: my-first-repo/ 폴더가 생성됩니다
```

실행 결과:
```
Cloning into 'my-first-repo'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (3/3), done.
```

---

### 현재 폴더에 내려받기

```bash
# 현재 폴더에 직접 내려받기 (폴더 이름 대신 . 사용)
# 주의: 폴더가 비어 있어야 합니다
git clone https://github.com/username/my-first-repo.git .
```

---

### clone과 remote의 차이

| 상황 | 명령어 |
|------|--------|
| 처음으로 GitHub → 내 컴퓨터 | `git clone URL` |
| 이미 있는 로컬 → GitHub 연결 | `git remote add origin URL` + `git push` |
| GitHub → 로컬 업데이트 | `git pull` |

---

### clone 후 할 일

```bash
# clone된 폴더로 이동
cd my-first-repo

# 상태 확인
git status
git log --oneline

# remote 자동 설정 확인
git remote -v
```

> 💡 **팁**: `git clone`은 원격 주소를 자동으로 `origin`으로 등록합니다. `git remote add origin`을 따로 할 필요가 없습니다.

---

<a id="part7"></a>

## 7️⃣ VS Code에서 확인 [↑](#toc)

---

### Sync 버튼 (↑↓)

VS Code 하단 상태바에 `↑0 ↓0` 형태의 숫자가 표시됩니다:

| 표시 | 의미 |
|------|------|
| `↑1` | push할 커밋이 1개 있음 |
| `↓2` | pull할 커밋이 2개 있음 |
| `↑1 ↓2` | 양쪽 모두 변경사항 있음 |

이 버튼을 클릭하면 `git push` 또는 `git pull`이 실행됩니다.

---

### Source Control 패널에서 Push

왼쪽 사이드바의 Source Control 아이콘 클릭 → 패널 상단의 `...` 메뉴 → **Push** 또는 **Pull** 선택

---

### Remote 탐색기

왼쪽 사이드바의 **Remote Explorer** 확장 프로그램(선택 설치)을 사용하면 GitHub의 원격 브랜치 목록을 VS Code에서 바로 볼 수 있습니다.

> 💡 **팁**: CLI와 VS Code 중 어느 것을 쓰든 괜찮습니다. 중요한 것은 **push 전에 항상 상태를 확인하는 습관**입니다.

---

<a id="part8"></a>

## 8️⃣ 정리 [↑](#toc)

| 명령어 | 역할 |
|--------|------|
| `git remote add origin URL` | 원격 리포지토리 연결 |
| `git remote -v` | 원격 주소 확인 |
| `git remote set-url origin URL` | 원격 주소 변경 |
| `git push -u origin main` | 처음 push + upstream 설정 |
| `git push` | 이후 push (upstream 설정 후) |
| `git clone URL` | 원격 리포지토리를 로컬로 복사 |
| `git clone URL .` | 현재 폴더에 복사 |

---

### 인증 방법 비교

| 방법 | 장점 | 단점 |
|------|------|------|
| **HTTPS + PAT** | 설정 간단 | 토큰 만료 시 재발급 |
| **SSH 키** | 만료 없음, 더 안전 | 초기 설정 복잡 |

학습 중에는 HTTPS + PAT, 실무 전환 시 SSH 키로 업그레이드하세요.

---

### 4-Zone 모델 완성

```
┌──────────────┐    git push    ┌──────────────┐
│   Remote     │ ◄──────────── │  Local Repo  │
│  (GitHub)    │ ──────────── ►│  (커밋 이력)  │
└──────────────┘    git pull   └──────┬───────┘
                                      │ git commit
                               ┌──────┴───────┐
                               │ Staging Area │
                               │  (포장 상자)  │
                               └──────┬───────┘
                                      │ git add
                               ┌──────┴───────┐
                               │Working Dir   │
                               │ (작업 책상)   │
                               └──────────────┘
```

4-Zone 모델이 이제 완성되었습니다. 모든 영역이 연결되었습니다.

---

### 다음 장 미리보기

GitHub에 코드를 올렸습니다! 이제 혼자가 아니라 **팀으로 작업하는 방법**을 배울 차례입니다. 다음 장에서 협업 초대, 팀 워크플로우, 그리고 "push 전에 반드시 pull"하는 이유를 배웁니다.

{% endraw %}
