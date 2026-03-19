---
title: 1. 로컬 Git 리포(todolist-app) → GitHub 원격(SSH) → feature 개발 → PR → merge → 로컬 동기화
layout: default
grand_parent: SDD
parent: speckit
nav_order: 1
permalink: /sdd/speckit/lab01
# nav_exclude: true
# search_exclude: true
--- 
# Lab 01: 로컬 Git 리포(todolist-app) → GitHub 원격(SSH) → feature 개발 → PR → merge → 로컬 동기화

## 🎯 학습 목표

이 실습에서는 1인 개발 상황에서 GitHub를 "원격 저장소 + 코드리뷰/머지 UI"로 사용하는 기본 흐름을 익힙니다.

- 로컬 Git 저장소 초기화 (`todolist-app` 폴더를 리포로 만들기)
- GitHub 원격 저장소 생성 및 SSH 연결
- `main` 기준 `feature/*` 브랜치 개발
- Pull Request(PR) 생성 → merge
- 로컬 `main` 동기화 + 브랜치 정리

> **중요 조건**
> - Git 설정은 리포 단위로만: `git config --local ...`만 사용
> - GitHub 연결은 SSH만 사용 (`git@github.com:...`)

---

## 📋 사전 준비사항

- Git 설치
- GitHub 계정
- PowerShell 사용 가능(Windows)

---

## ✅ 실습 단계

### 0단계: 현재 위치 확인

이 실습은 터미널에서 `create-next-app`으로 `todolist-app` 폴더를 만든 다음 **VS Code에서 `todolist-app` 폴더를 열고** 그 안에서 작업합니다.

```bash
pwd
# 또는
cd
```

---

### 1단계: Next.js 앱 생성(d01 아래에 todolist-app 폴더로)

아래 명령을 **d01 폴더에서 실행**해 Next.js 앱을 생성합니다.

```bash
npx create-next-app@latest todolist-app --typescript --eslint --tailwind --app --disable-git
```

생성 결과로 `todolist-app` 폴더가 만들어지고, 그 안에 Next.js 프로젝트가 생성됩니다.

> 주의: 이미 `todolist-app` 폴더가 있으면 생성이 실패하거나 충돌할 수 있습니다.

#### 1-1) Git 초기화는 나중에(권장)

실습 흐름을 깔끔하게 유지하려고 **Git 리포 초기화/첫 커밋은 아래 단계에서 따로** 진행합니다.

- 위 명령에 `--disable-git`을 넣었기 때문에, `create-next-app`이 `.git`을 만들지 않습니다.

---

### 2단계: VS Code에서 todolist-app 폴더 열기

이후 단계는 **`todolist-app` 폴더에서** 진행합니다.

- (GUI) VS Code → File → Open Folder… → `todolist-app` 선택
- (CLI, 선택) 현재 터미널에서:

```bash
code todolist-app 경로
```

터미널 기준으로도 `todolist-app`으로 이동해 둡니다.

```bash
cd todolist-app
```

---

### 3단계: 로컬 Git 리포(todolist-app) 생성

이제 `todolist-app` 폴더를 Git 리포로 초기화합니다.

```bash
git init -b main
git status
```

---

### 4단계: (리포 단위) Git 사용자 설정 + 초기 커밋 만들기

전역 설정(`--global`)은 사용하지 않습니다. 이 리포에서만 사용할 이름/이메일을 설정합니다.

> `git init` 이전에 `git config --local ...`을 실행하면 다음 오류가 납니다.
>
> - `fatal: --local can only be used inside a git repository`

```bash
git config --local user.name "홍길동"
git config --local user.email "hong@example.com"

git config --local --list
```

첫 커밋을 만듭니다.

```bash
git add -A
git commit -m "chore: initial commit"
```

---

### 5단계: SSH 키 준비 및 GitHub 연결 확인

#### 3-1) SSH 키가 없다면 생성

```bash
ssh-keygen -t ed25519 -C "hong@example.com"
```

기본 경로(예: `C:\Users\<you>\.ssh\id_ed25519`)로 생성하는 것을 권장합니다.

#### 3-2) 공개키를 GitHub에 등록

```bash
# 공개키 출력
cat ~/.ssh/id_ed25519.pub
```

- GitHub → Settings → SSH and GPG keys → New SSH key
- 위 출력 내용을 붙여넣고 저장

#### 3-3) SSH 연결 테스트

```bash
ssh -T git@github.com
```

- 성공 예: `Hi <username>! You've successfully authenticated...`
- 처음 접속 시 "Are you sure you want to continue connecting" → `yes`

---

### 6단계: GitHub 원격 저장소 생성(웹 UI)

이번 단계는 **GitHub 웹 UI로 원격 저장소를 만든 뒤**, 로컬에서 `origin`을 연결합니다.

1) GitHub → New repository
2) Repository name: `todolist-app`
3) Public/Private 선택
4) **Initialize this repository with a README 체크하지 않기**(로컬이 이미 있음)
5) Create repository

생성 후 안내되는 SSH URL을 복사합니다. 예:

- `git@github.com:<GITHUB_ID>/todolist-app.git`

---

### 7단계: 로컬에 origin(SSH) 연결 + main 푸시

```bash
git remote add origin git@github.com:<GITHUB_ID>/todolist-app.git

git push -u origin main
```

확인:

```bash
git remote -v
```

---

### 8단계: main 기준 feature 브랜치 개발

`main`에서 기능 브랜치를 따서 작업합니다.

```bash
git switch -c feature/add-lab-00
```

예시 변경(아무 파일이나 OK):

```bash
echo "" >> README.md
echo "- Lab 00 진행 중" >> README.md

git add README.md
git commit -m "docs: add lab 00 note"
```

원격에 브랜치 푸시:

```bash
git push -u origin feature/add-lab-00
```

---

### 9단계: PR 생성 → merge

#### 방법 A) GitHub 웹에서 PR 만들기(권장)

1) GitHub 저장소 페이지에서 “Compare & pull request” 클릭
2) base: `main` ← compare: `feature/add-lab-00` 확인
3) PR 제목/설명 작성 → Create pull request
4) Merge pull request → Confirm merge

#### 머지 전략(권장)

- 1인 실습에서는 **Squash and merge** 또는 **Create a merge commit** 중 아무거나 선택
- 팀 컨벤션이 있으면 그걸 따르기

---

### 10단계: 로컬 main 동기화 + 브랜치 정리

머지가 끝났으면 로컬을 정리합니다.

```bash
git switch main
git pull
```

로컬 feature 브랜치 삭제:

```bash
git branch -d feature/add-lab-00
```

원격 feature 브랜치도 삭제(선택):

```bash
git push origin --delete feature/add-lab-00
```

원격 추적 브랜치 정리(권장):

```bash
git fetch --prune
```

---

## 🔎 결과 확인 체크리스트

```bash
# 1) main에 머지 커밋/스쿼시가 반영되었는지
git log --oneline --decorate -n 10

# 2) 작업 브랜치가 남아있지 않은지
git branch

# 3) origin/main과 로컬 main이 맞는지
git status
```

---

## (선택) GitHub CLI(gh) 설치/사용

> 이 섹션은 **선택 사항**입니다. 웹 UI 대신 `gh`로 PR 생성/머지를 빠르게 할 수 있습니다.

### 설치

- Windows: https://cli.github.com/ 에서 설치
- 설치 확인:

```bash
gh --version
```

### SSH 방식으로 로그인

```bash
gh auth login --git-protocol ssh
```

### (대안) 원격 저장소 생성까지 gh로 한 번에

이미 로컬 리포가 준비된 상태에서, 원격을 만들고 `origin` 연결 + 푸시까지 수행할 수 있습니다.

> 아래 명령은 `todolist-app` 폴더에서 실행한다고 가정합니다.

```bash
# 현재 폴더를 원격으로 생성
# --source . : 현재 폴더 기준
# --remote origin : origin 이름 사용
# --push : 푸시
# 공개/비공개는 --public / --private 선택

gh repo create todolist-app --source . --remote origin --push --public
```

### PR 생성/머지

```bash
# PR 생성 (base=main)
gh pr create --base main --head feature/add-lab-00 --title "docs: add lab 00" --body "lab 00 연습 PR"

# PR 머지(예: squash)
gh pr merge --squash --delete-branch
```

---

## 🧯 트러블슈팅

- `ssh -T git@github.com`가 실패하면:
  - GitHub에 공개키가 등록됐는지 재확인
  - `~/.ssh/config`에 잘못된 설정이 없는지 확인
  - `ssh -vT git@github.com`로 디버그 로그 확인
- `Permission denied (publickey)`:
  - 키 파일 경로/권한/등록 여부 문제일 가능성이 큼
