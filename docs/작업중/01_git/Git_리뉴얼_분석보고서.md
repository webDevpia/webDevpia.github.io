---
title: Git 커리큘럼 리뉴얼 분석 보고서
layout: default
parent: Git
nav_order: 99
permalink: /git/renewal-report
---

{% raw %}

# Git 커리큘럼 리뉴얼 — 다중 페르소나 비판적 분석 보고서
{: .no_toc }

**작성일**: 2026-04-11  
**분석 방법**: 다중 페르소나 비판적 사고 기법 (Multi-Persona Critical Thinking)  
**분석 대상**: `docs/01_git/` (4개 파일, 00_git ~ 03_github_hosting)  
**데이터 기반**: Git 2.49+, GitHub 2025-2026 최신 기능, JISE 2025 교육 연구, 주요 플랫폼 분석
{: .fs-5 .fw-300 }

---

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 1. 분석 개요

### 1.1 기존 과정 구조

| 파일 | 제목 | 내용 | 분량 |
|------|------|------|------|
| `00_git.md` | Git (인덱스) | 나무위키 복사 역사 서술만 | 19줄 |
| `01_gitstart.md` | Git & GitHub | 설치~브랜치~리셋~협업 — **15개 주제를 1파일에** | 476줄 |
| `02_git_pr.md` | Pull Request | Fork, PR 생성, 머지 전략 (스크린샷 중심) | 139줄 |
| `03_github_hosting.md` | GitHub Pages | 4단계 요약 (사실상 메모) | **20줄** |

**총 654줄, 4개 파일** — JS 과정(14장, 10,000줄+)과 비교하면 극도로 부실.

### 1.2 분석 페르소나

| 페르소나 | 역할 | 관점 |
|---------|------|------|
| **Dr. 버전** | 교육공학 연구자 | 학습 순서, 인지 부하, 멘탈 모델 |
| **최 데브옵스** | 시니어 개발자 (15년차) | 현업 워크플로우, 보안, 정확성 |
| **박 비평가** | 교육 비평가 / 회의론자 | 기존 문제점, 위험, 비전공자 적합성 |
| **정 설계자** | 커리큘럼 설계 전문가 | 구조화, 강의 흐름, 스타일 통일 |

---

## 2. 핵심 자료 요약

### 2.1 Git 2025-2026 현황

| 항목 | 현행 |
|------|------|
| Git 최신 버전 | **2.49+** (2025.03) |
| 핵심 변경 | `git switch`/`git restore`가 `git checkout` 대체 (2.23부터) |
| 교육적 영향 | **`checkout` 대신 `switch`/`restore` 가르쳐야 함** |
| GitHub 인증 | 비밀번호 인증 폐지(2021.08) → **SSH 키 또는 PAT 필수** |

### 2.2 GitHub 2025-2026 신기능 (교육 관련)

| 기능 | 설명 |
|------|------|
| **Copilot CLI** | 터미널에서 "how do I undo my last commit?" 직접 질문 가능 |
| **Codespaces** | 브라우저에서 VS Code — 설치 없이 즉시 개발 |
| **GitHub Skills** | 실제 리포지토리에서 진행하는 인터랙티브 튜토리얼 |

### 2.3 교육 연구 — JISE 2025 "Rethinking How We Teach Git"

> Wagner & Thurner (2025)의 연구:  
> - **브랜치 개념을 커밋 전에 먼저 가르쳐야** 한다  
> - 개념적 학습과 실습(명령어)을 분리해야 한다  
> - IS/비전공 학생은 명령어가 너무 일찍 나오면 **압도당한다**

### 2.4 효과적인 Git 비유 모음

| 개념 | 비유 | 출처 |
|------|------|------|
| 버전 관리 | **타임머신** — 언제든 과거로 돌아갈 수 있는 자동 저장 | 업계 표준 |
| 커밋 | **게임 세이브 포인트** — 실수하면 마지막 저장으로 복구 | Towards Data Science |
| 워킹 디렉토리 | **작업 책상** — 현재 작업 중인 파일들 | 커뮤니티 |
| 스테이징 영역 | **택배 포장 상자** — 보낼 물건을 골라 담는 단계 | DEV Community |
| 리포지토리 | **사진 앨범** — 앨범에 붙인 사진은 영구 보존 | freeCodeCamp |
| 브랜치 | **평행 세계** — 메인 타임라인에 영향 없이 실험 | Opensource.com |
| 머지 | **두 평행 세계 합치기** — 각자의 변경을 하나로 결합 | 커뮤니티 |
| 머지 충돌 | **두 사람이 같은 줄을 다르게 고침** — Git이 "어떤 걸 쓸지 결정해주세요" | Library Carpentry |
| 리모트 (GitHub) | **클라우드 백업** — Google Drive처럼 온라인에 코드 저장 | 커뮤니티 |
| Pull Request | **검토 요청서** — "제 변경사항을 확인하고 승인해주세요" | 커뮤니티 |
| Fork | **레시피 복사** — 원본은 그대로, 내 버전에서 실험 | 커뮤니티 |
| `.gitignore` | **비밀 서류함** — 택배 상자에 절대 넣으면 안 되는 것들 | 실무 |

### 2.5 4-Zone 멘탈 모델 (가장 효과적인 교육 프레임워크)

```
┌──────────────┐    git push     ┌──────────────┐
│   Remote     │ ◄────────────── │  Local Repo  │
│  (GitHub)    │ ──────────────► │   (커밋 이력)  │
└──────────────┘    git pull     └──────┬───────┘
                                       │ git commit
                                ┌──────┴───────┐
                                │ Staging Area │
                                │  (포장 상자)   │
                                └──────┬───────┘
                                       │ git add
                                ┌──────┴───────┐
                                │Working Dir   │
                                │ (작업 책상)    │
                                └──────────────┘
```

> **"개념을 먼저, 명령어는 나중에"** — 이 4-Zone 모델을 화이트보드에 먼저 그리고, 모든 명령어가 이 모델의 어느 구간을 이동시키는지 보여줘야 합니다.

### 2.6 초보자 최대 혼란 지점 (빈도순)

| 순위 | 혼란 지점 | 원인 |
|------|----------|------|
| 1 | **스테이징 영역** | 왜 add 후 commit 2단계인지 이해 불가 |
| 2 | **Detached HEAD** | "HEAD가 분리됐다"는 공포 유발 메시지 |
| 3 | **Merge vs Rebase** | 언제 어떤 것을 쓰는지 판단 불가 |
| 4 | **reset 3종** | soft/mixed/hard 차이를 외울 수 없음 |
| 5 | **원격 추적 브랜치** | `origin/main` vs `main`의 차이 |
| 6 | **checkout의 이중 역할** | 브랜치 전환과 파일 복구를 같은 명령어로 |

---

## 3. 다중 페르소나 분석

### 3.1 Dr. 버전 — 교육공학 연구자의 분석

#### 핵심 주장: "15개 주제를 1파일에 넣으면 학습이 불가능하다"

**문제 1: 인지 과부하 — 1파일 476줄에 15개 주제**

`01_gitstart.md` 하나에: 설치, 설정, init, add, commit, remote, push, clone, pull, 리눅스 명령어, 브랜치, .gitignore, reset, reflog, revert, 협업이 전부 들어있다. JS 과정은 이 정도의 내용을 **14개 파일**에 걸쳐 가르친다.

비전공자가 한 수업에서 `git init`부터 `git reset --hard`와 `git revert --no-commit HEAD~3`까지 보면, **아무것도 기억하지 못한다**.

**문제 2: 4-Zone 멘탈 모델 부재**

기존 과정은 "이 명령어를 치세요 → 이런 결과가 나옵니다" 패턴이다. **왜** 이 명령어가 필요한지, 데이터가 **어디에서 어디로** 이동하는지 설명하지 않는다.

교육 연구 합의: "개념을 먼저 가르치고 명령어는 나중에" 접근이 **40-60% 더 높은 기억 정착률**을 보인다 (DEV Community 연구 요약).

**문제 3: 스테이징 영역 설명 부재**

`git add`를 가르치지만, **왜** add와 commit이 분리되어 있는지 설명하지 않는다. 비전공자에게 이것은 가장 혼란스러운 지점이다.

> **택배 포장 비유**: "작업 책상(워킹 디렉토리)에 있는 것들 중 보내고 싶은 것만 골라서 상자(스테이징)에 담고, 상자를 밀봉(커밋)합니다. 책상의 모든 것을 매번 다 보낼 필요는 없습니다."

#### 평가

| 항목 | 판정 |
|------|------|
| 인지 부하 | **치명적** — 1파일 15주제는 학습 불가 |
| 멘탈 모델 | **부재** — 4-Zone 모델 미교육 |
| 비유/은유 | **전무** — 단 하나의 비유도 없음 |

---

### 3.2 최 데브옵스 — 시니어 개발자의 분석

#### 핵심 주장: "명령어 버그 5건 + 인증 미교육 + 위험 명령어 경고 없음"

**명령어 버그 5건:**

| 위치 | 현재 (오류) | 올바른 명령어 |
|------|-----------|-------------|
| 01_gitstart 101줄 | `git config list` | `git config --list` |
| 01_gitstart 175줄 | `git commit --amend "메시지"` | `git commit --amend -m "메시지"` |
| 01_gitstart 334줄 | `git restore --stated .` | `git restore --staged .` |
| 01_gitstart 339줄 | `// 주석` (JS 문법) | `# 주석` (bash 문법) |
| 02_git_pr 108줄 | "Sueash and Merge" | "Squash and Merge" |

**인증 미교육 — 가장 치명적인 누락:**

2021년 8월부터 GitHub은 비밀번호 인증을 폐지했다. `git push`를 하려면 **SSH 키** 또는 **Personal Access Token**이 필요한데, 기존 과정에서 인증 설정이 **전혀 없다**. 학생이 과정을 따라해도 push에서 막힌다.

**위험 명령어 경고 부재:**

`01_gitstart.md` 341줄의 `git push -f`가 **아무런 경고 없이** 제시된다. 이 명령은 원격 저장소의 히스토리를 **덮어쓰며**, 팀원의 작업을 **영구적으로 파괴**할 수 있다.

**`git checkout` 사용 — 2025년 기준 구식:**

현재 과정은 `git checkout`을 가르치지만, Git 2.23(2019)부터 이 명령은 두 가지로 분리되었다:
- `git switch` — 브랜치 전환
- `git restore` — 파일 변경 취소

2025년 교육 합의: **`switch`/`restore`를 가르치고, `checkout`은 언급만 한다.**

**누락된 핵심 주제:**

| 주제 | 중요도 |
|------|--------|
| **인증 (SSH/PAT)** | 필수 — 없으면 push 불가 |
| **git status 읽기** | 필수 — 현재 상태 파악의 기본 |
| **git diff** | 필수 — 변경 내용 확인 |
| **머지 충돌 해결 (텍스트)** | 필수 — 스크린샷만 있고 마커 설명 없음 |
| **좋은 커밋 메시지 작성법** | 높음 |
| **git stash** | 높음 — 초보자가 자주 필요 |
| **GitHub Issues** | 중간 — 프로젝트 관리 기초 |
| **VS Code Git 패널** | 중간 — GUI+CLI 병행 교육 |

#### 평가

| 항목 | 판정 |
|------|------|
| 기술 정확성 | **버그 5건 즉시 수정 필요** |
| 인증 | **치명적 누락** — push 불가 |
| 보안 | **`push -f` 경고 없음** — 위험 |
| 현행 패턴 | **`checkout` → `switch`/`restore`로 교체 필요** |

---

### 3.3 박 비평가 — 교육 비평가의 분석

#### 핵심 주장: "이것은 강의 교안이 아니라 명령어 메모장이다"

**JS 과정과의 스타일 격차:**

| 항목 | JS 과정 | Git 과정 |
|------|---------|---------|
| 학습 목표 | **매 챕터** | 없음 |
| 진행 순서 (TOC) | 앵커 링크 | 없음 |
| 비유/은유 | **매 개념** | **없음** (0개) |
| 연습 문제 | 기본/중급/심화 | 없음 |
| 브릿지 문장 | 다음 장 미리보기 | 없음 |
| 핵심 요약 표 | 개념/설명/비유 | 없음 |
| 실행 결과 | `실행 결과:` 블록 | 없음 |
| 문체 | `~합니다` (대화체) | `~함` (게시판체) |
| `[↑](#toc)` | 모든 섹션 | 없음 |

**인덱스 페이지가 나무위키 복사:**

`00_git.md`는 나무위키에서 복사한 Git 역사 서술이 전부다. 학습자에게 "이 과정에서 무엇을 배우는지"를 알려주지 않는다.

**섹션 번호 혼란:**

`01_gitstart.md`에서:
- `## 4.` 가 **2번** 등장 (85줄, 239줄)
- 번호가 8에서 **13으로 점프** (9-12 누락)
- `nav_order`가 주석 처리됨 — 네비게이션에서 순서 불확실

**GitHub Pages 20줄:**

`03_github_hosting.md`는 20줄짜리 메모다. 정적 호스팅이 무엇인지, 왜 필요한지, 트러블슈팅은 어떻게 하는지 전혀 없다. 미사용 스크린샷(`github_hosting02.png`, `github_hosting03.png`)이 img 폴더에 있지만 참조되지 않는다.

#### 평가

| 항목 | 판정 |
|------|------|
| 교육 자료 완성도 | **미완성** — 명령어 메모장 수준 |
| 비전공자 적합도 | **부적합** — 설명, 비유, 연습 전무 |
| 스타일 통일 | **완전 불일치** — JS 과정과 다른 세계 |

---

### 3.4 정 설계자 — 커리큘럼 설계 전문가의 분석

#### 핵심 주장: "전면 재작성, 12장 구조가 최적"

**설계 원칙:**

1. **개념 먼저, 명령어 나중** — JISE 2025 연구 기반
2. **4-Zone 멘탈 모델**을 첫날 화이트보드에 그림
3. **1주제 1파일** — 강사가 "오늘은 5장까지"라고 말할 수 있어야 함
4. **비유 선행** — 매 개념 시작에 일상 비유
5. **CLI + VS Code GUI 병행** — 명령어 입력 후 VS Code에서 시각적 확인
6. **연습 문제 필수** — 기본/중급/심화
7. **`switch`/`restore` 표준** — `checkout` 미사용
8. **learngitbranching.js.org** — 브랜치 챕터 숙제로 활용

**리뉴얼 커리큘럼 구조 (12장):**

```
Git 리뉴얼 과정 (12장)
│
├── Part 0: 시작 (2장)
│   ├── 01. 버전 관리란? — 타임머신 비유
│   └── 02. Git 설치와 초기 설정
│
├── Part 1: 혼자 쓰는 Git (4장)
│   ├── 03. 첫 번째 커밋 — 사진 찍고 앨범에 넣기
│   ├── 04. 변경 이력 관리 — diff, log, .gitignore
│   ├── 05. 브랜치 — 평행 세계 만들기
│   └── 06. 머지와 충돌 해결 — 평행 세계 합치기
│
├── Part 2: 함께 쓰는 Git (4장)
│   ├── 07. GitHub 연결 — 클라우드 백업
│   ├── 08. 협업 기초 — push, pull, 팀 워크플로우
│   ├── 09. Pull Request — 검토 요청서
│   └── 10. 되돌리기 — 실수를 복구하는 방법들
│
└── Part 3: 실전 (2장)
    ├── 11. GitHub 활용 — Pages, Issues, README
    └── 12. 실전 워크플로우 — 팀 시뮬레이션
```

**시간 배분:**

| Part | 장 | 예상 시간 |
|------|-----|----------|
| Part 0 | 01-02 | 3시간 |
| Part 1 | 03-06 | 8시간 |
| Part 2 | 07-10 | 8시간 |
| Part 3 | 11-12 | 5시간 |
| **합계** | | **24시간** |

> 24시간은 3일(1일 8시간) 분량. Git은 보통 프로그래밍 과정의 **사전 과정**이므로 이 정도가 적절하다.

---

## 4. 쟁점별 페르소나 간 교차 분석

### 4.1 "`checkout` vs `switch`/`restore`"

| 페르소나 | 입장 | 근거 |
|---------|------|------|
| 최 데브옵스 | **`switch`/`restore`만 가르침** | 2025년 표준, checkout의 이중 역할이 혼란의 주범 |
| Dr. 버전 | **`switch`/`restore` 우선**, checkout은 "참고" 언급 | 인지 부하 감소 |
| 박 비평가 | **`switch`/`restore` only** | 비전공자에게 checkout은 혼란만 가중 |
| 정 설계자 | **`switch`/`restore` 표준**, "예전에는 checkout이라고 했습니다" 한 줄 | 절충 |

**합의**: `git switch`/`git restore`를 표준으로. `checkout`은 "참고" 박스에 한 줄 언급.

### 4.2 "인증은 SSH vs PAT?"

| 페르소나 | 입장 | 근거 |
|---------|------|------|
| 최 데브옵스 | **SSH 키** — 한 번 설정하면 영구 | 현업 표준 |
| Dr. 버전 | **HTTPS + PAT** — 설정이 더 간단 | 비전공자 진입 장벽 낮음 |
| 정 설계자 | **둘 다 가르치되 HTTPS+PAT 먼저**, SSH는 선택 | 점진적 |

**합의**: **HTTPS + PAT를 기본**으로 가르치고, SSH 키는 "더 편리한 방법" 보너스 섹션.

### 4.3 "CLI만 vs GUI 병행?"

| 페르소나 | 입장 | 근거 |
|---------|------|------|
| 최 데브옵스 | CLI 필수, GUI는 보조 | 현업/CI 환경에서 CLI 필수 |
| Dr. 버전 | **GUI 먼저, CLI를 옆에** | 시각적 확인이 이해를 돕는다 |
| 정 설계자 | **CLI + VS Code GUI 동시** | "명령어 입력 → VS Code에서 결과 확인" |

**합의**: **CLI를 주력으로, VS Code Source Control 패널로 시각적 확인 병행**. "CLI에서 `git add file.txt` → VS Code에서 파일이 'Staged Changes'로 이동한 것 확인."

### 4.4 "learngitbranching.js.org 활용?"

**합의**: **05장(브랜치) 숙제로 활용**. "이 장의 실습 과제: learngitbranching.js.org에서 'Introduction Sequence'를 완료하세요."

---

## 5. 기존 콘텐츠 재활용 판정

### 5.1 유지/활용할 것

| 기존 콘텐츠 | 위치 | 리뉴얼 활용 |
|-----------|------|-----------|
| **협업 시나리오 스크린샷 22장** (`git_13_01`~`git_13_22`) | 01_gitstart 412-476줄 | **12장 실전 워크플로우** — 팀장/팀원 역할 분담, 충돌 해결 시각 자료 |
| **git 작업순서 다이어그램 3장** (`git_3_1`~`git_3_3`) | 01_gitstart 74-83줄 | **03장 첫 번째 커밋** — 4-Zone 모델과 결합하여 init→stage→commit 흐름 시각화 |
| **reset 전후 다이어그램 7장** (`git_6_1`~`git_6_7`) | 01_gitstart 360-368줄 | **10장 되돌리기** — push 전/후 되돌리기 차이를 시각적으로 비교 |
| **머지 전략 3종 다이어그램** (`git_pr_merge_01`~`03`) | 02_git_pr 106-116줄 | **09장 Pull Request** — Merge/Squash/Rebase 비교 핵심 자료 |
| **PR 과정 스크린샷 26장** (`git_pr_01`~`git_pr_26`) | 02_git_pr 전체 | **09장 Pull Request** — Fork→PR→Review→Merge 전체 흐름 시각 자료 |
| **Git 설치 스크린샷 10장** (`git_001`~`git_010`) | 01_gitstart 31-49줄 | **02장 설치** — Windows 설치 과정 시각 자료 (버전 확인 필요) |
| **리눅스 기본 명령어** (pwd, ls, cd, mkdir, rm) | 01_gitstart 209-237줄 | **02장 설치** — "터미널 기초" 섹션으로 포함 (비전공자 필수) |
| **운영체제별 줄바꿈 설정** (`core.autocrlf`) | 01_gitstart 157-161줄 | **02장 설치** — Win/Mac 혼재 교실에서 실제 발생하는 문제 해결 |
| **.gitignore 패턴 설명** | 01_gitstart 292-322줄 | **04장 변경 이력** — 상세한 패턴 예시 (경로별, 확장자별, 예외) |
| **upstream 추가 + sync fork** | 02_git_pr 118-138줄 | **09장 PR** — PR 이후 fork 동기화 워크플로우 |
| **브랜치 그래프 스크린샷** (`git_10_1`, `git_10_2`) | 01_gitstart 261, 281줄 | **05장 브랜치** — 브랜치 생성/병합 전후 시각 자료 |
| **reflog, revert 설명** | 01_gitstart 370-409줄 | **10장 되돌리기** — revert --no-commit, --continue, --abort 패턴 |
| **`git commit -am` 단축** | 01_gitstart 172줄 | **03장 또는 04장** — 실무 팁으로 소개 |

### 5.2 제거/대체할 것

| 기존 | 이유 | 대체 |
|------|------|------|
| 나무위키 역사 서술 (00_git) | 비교육적, 저작권 이슈 | 자체 작성 Git 소개 |
| 476줄 단일 파일 (01_gitstart) | 인지 과부하 | 8개 챕터로 분리 |
| 20줄 GitHub Pages (03) | 메모 수준 | 11장에서 확장 |
| `git checkout` 사용 | 구식 | `switch`/`restore`로 교체 |
| 명령어 버그 5건 | 오류 | 수정 |

---

## 6. 종합 권고안

### 6.1 확정된 결정사항

| 항목 | 결정 | 근거 |
|------|------|------|
| 과정 방식 | **전면 재작성** | 기존 4파일 → 12장 재구성 |
| 대상 | **비전공자** | 사용자 확정 |
| 장 수 | **12장** | 설계자 권고 |
| 브랜치 전환 | **`git switch`** | `checkout` 미사용, 2025 표준 |
| 파일 복구 | **`git restore`** | `checkout` 미사용 |
| 인증 | **HTTPS + PAT 기본**, SSH 보너스 | 비전공자 접근성 |
| GUI | **VS Code 병행** | CLI 입력 → VS Code에서 시각 확인 |
| 멘탈 모델 | **4-Zone 모델** 첫날 교육 | 교육 연구 합의 |
| 비유 | **매 개념마다** | JS 과정 스타일 통일 |
| 스타일 | **JS/TS 과정과 동일** | 목표, 비유, 연습, 브릿지 |
| 인터랙티브 | **learngitbranching.js.org** 숙제 | 28,000+ GitHub stars |
| 충돌 해결 | **텍스트 기반 step-by-step** | 스크린샷만으로 불충분 |

### 6.2 12장 상세 구조

| Part | 장 | 제목 | 핵심 비유 | 시간 |
|------|-----|------|----------|------|
| **0** | 01 | 버전 관리란? | 타임머신 + 게임 세이브 | 1.5h |
| | 02 | Git 설치와 초기 설정 | 도구함 준비 | 1.5h |
| **1** | 03 | 첫 번째 커밋 | 사진 찍고 앨범에 넣기 | 2h |
| | 04 | 변경 이력 관리 | 변경 일지 읽고 쓰기 | 2h |
| | 05 | 브랜치 | 평행 세계 만들기 | 2h |
| | 06 | 머지와 충돌 해결 | 두 세계 합치기 | 2h |
| **2** | 07 | GitHub 연결 | 클라우드 백업 | 2h |
| | 08 | 협업 기초 | 같이 문서 편집하기 | 2h |
| | 09 | Pull Request | 검토 요청서 보내기 | 2h |
| | 10 | 되돌리기 | 실수 복구 방법들 | 2h |
| **3** | 11 | GitHub 활용 | GitHub로 프로젝트 관리 | 2.5h |
| | 12 | 실전 워크플로우 | 실제 팀처럼 일하기 | 2.5h |
| | | **합계** | | **24h** |

### 6.3 매 챕터 특수 요소

| 요소 | 설명 |
|------|------|
| **4-Zone 다이어그램** | 매 명령어가 4-Zone의 어느 구간을 이동시키는지 표시 |
| **CLI + VS Code 병행** | "터미널에서 입력 → VS Code에서 확인" 패턴 반복 |
| **`실행 결과:` 블록** | 모든 명령어에 예상 출력 표시 |
| **> ⚠️ 위험 경고** | `push -f`, `reset --hard` 등에 필수 |
| **> 💡 실무 팁** | 커밋 메시지 작성법, 브랜치 네이밍 등 |
| **learngitbranching.js.org** | 05장 숙제로 활용 |

---

## 7. 결론 — 페르소나 간 최종 합의

### 4인이 동의하는 것

1. **전면 재작성** 필요 — 기존 4파일은 명령어 메모장 수준
2. **명령어 버그 5건** 즉시 수정
3. **인증(SSH/PAT)** 챕터 필수 추가 — 없으면 push 불가
4. **4-Zone 멘탈 모델** 첫날 교육
5. **`switch`/`restore` 표준**, `checkout` 미사용
6. **비유 선행** — 매 개념에 일상 비유
7. **CLI + VS Code GUI 병행**
8. **머지 충돌을 텍스트로 step-by-step** 교육
9. **위험 명령어 경고** 필수 (`push -f`, `reset --hard`)
10. **JS/TS/FastAPI 과정과 동일한 교육 스타일**

### 4인이 동의하지 않는 것

| 쟁점 | 범위 |
|------|------|
| Rebase 교육 여부 | 최 데브옵스(포함) vs 박 비평가(제외 — 위험) |
| GitHub Actions 포함 | 정 설계자(11장에 맛보기) vs Dr. 버전(범위 초과) |
| SSH 키 교육 깊이 | 최 데브옵스(필수) vs Dr. 버전(보너스만) |

---

## 부록: 참고 문헌

### 교육 연구
- Wagner & Thurner (2025). "Teaching Tip: Rethinking How We Teach Git." JISE, Vol. 36, No. 1.
- DEV Community — "Learn Git Concepts, Not Commands" (4,000+ reactions)
- Library Carpentry — Git Instructor Notes
- Software Carpentry — Instructor Training: Teaching Practices

### Git/GitHub 공식
- [Git 2.49 Highlights — GitHub Blog](https://github.blog/open-source/git/highlights-from-git-2-49/)
- [GitHub Pages Quickstart](https://docs.github.com/en/pages/quickstart)
- [GitHub Actions Quickstart](https://docs.github.com/actions/quickstart)
- [VS Code Source Control](https://code.visualstudio.com/docs/sourcecontrol/overview)

### 교육 플랫폼
- Codecademy — Learn Git
- freeCodeCamp — Git & GitHub Crash Course
- Udemy — Git & GitHub Bootcamp (Colt Steele)
- Boot.dev — Learn Git
- learngitbranching.js.org (28,000+ GitHub stars)
- Oh My Git! (ohmygit.org)
- GitHub Skills (skills.github.com)

### 비유/은유
- [Getting Git for Beginners — Analogy](https://ammonshepherd.github.io/git-for-beginners/analogy.html)
- [Git: The Beginner's Guide — freeCodeCamp](https://www.freecodecamp.org/news/git-the-laymans-guide-to-understanding-the-core-concepts)
- [Explaining Git branches with LEGO — Opensource.com](https://opensource.com/article/22/4/git-branches)

---

*본 보고서는 다중 페르소나 비판적 사고 기법을 적용하여,*  
*교육공학자, 시니어 개발자, 교육 비평가, 커리큘럼 설계자 4가지 관점에서 독립 분석한 후 종합하였습니다.*

{% endraw %}
