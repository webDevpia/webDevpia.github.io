# 01. 오리엔테이션 & 실습환경 구축

## 목표

- 수업에 필요한 핵심 도구(uv, Python 3.12, Git, VS Code, GitHub Copilot Chat)를 정확히 설치합니다.
- **uv를 기본 환경 관리자**로 사용하도록 실행/검증 습관을 통일합니다.
- Copilot Chat의 Agent 모드까지 진입 가능한 상태를 만들어 2교시 이후 실습을 준비합니다.

---

## 배경 지식

### 이 문서 사용법

- 이 문서는 Windows 11 기준 실습 가이드입니다.
- 아래 순서대로 따라오면, 설치 → 설정 → 검증을 한 번에 끝낼 수 있습니다.
- 이미 설치한 도구가 있어도 "검증 명령"은 꼭 실행해 주세요.

### 운영 원칙 (중요)

이번 과정은 **uv 기본 환경**으로 운영합니다.

- Python 설치/버전 관리는 `uv python ...` 명령으로 수행합니다.
- 프로젝트 명령 실행은 `uv run ...` 중심으로 수행합니다.
- 로컬 PC의 기존 Python 전역 설치에 의존하지 않습니다.

---

## 실습 단계

### 0단계: 사전 준비

- Windows 업데이트를 최신 상태로 맞춥니다.
- PowerShell 실행 권한을 확인합니다.
- GitHub 계정 로그인 가능 상태(2FA 포함)를 확인합니다.

### 1단계: 도구 설치

#### 1-1. uv 설치

Windows에 `install.ps1` 명령으로 설치합니다.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

설치 확인:

```powershell
uv --version
```

업데이트 확인(선택):

```powershell
uv self update
```

---

#### 1-2. Python 3.12 설치 (uv 기준)

공식 가이드 기준으로 Python 3.12를 uv로 설치합니다.

```powershell
uv python install 3.12
```

설치 확인:

```powershell
uv python list
python3.12 --version
```

기본 사용 예시:

```powershell
uv run python --version
```

---

#### 1-3. Git 설치

1. https://git-scm.com/download/win 접속(자동으로 Git for Windows 안내)
2. 설치 파일 실행 후 기본 옵션으로 설치

설치 확인:

```powershell
git --version
```

기본 사용 예시:

```powershell
git status
git log --oneline -5
```

---

#### 1-4. VS Code 설치

1. https://code.visualstudio.com/docs/setup/windows 접속
2. Windows Installer(User setup) 설치
3. 설치 후 새 터미널에서 확인

```powershell
code --version
```

기본 사용 예시:

```powershell
code .
```

---

#### 1-5. GitHub Copilot Chat 설정 (+ Pro 30일 평가판)

기본 설정:

1. VS Code 하단 Copilot 아이콘 클릭
2. `Use AI Features` 선택
3. GitHub 계정으로 로그인
4. Chat 뷰 열기 후 사용 가능 여부 확인

구독이 없는 경우, **Copilot Pro 30일 평가판** 시작 방법:

1. https://github.com/features/copilot/plans 접속
2. `Pro` 카드에서 `Try for 30 days free` 클릭
3. 월/연 결제 주기 선택
4. 결제 정보 입력 후 활성화
5. VS Code로 돌아와 Copilot Chat 재로그인/동기화

평가판 과금 주의사항(공식 문서 기준):

- 30일 내 취소하면 과금되지 않습니다.
- 취소하지 않으면 평가판 종료 후 유료 플랜으로 자동 전환됩니다.
- 취소 경로: GitHub `Settings` → `Billing & licensing` → Copilot 섹션 `Cancel trial`

Agent 모드 확인:

1. Chat 뷰 열기 (`Ctrl+Alt+I` 또는 Chat 아이콘)
2. 에이전트 드롭다운에서 `Agent` 선택 가능 여부 확인

### 2단계: 초기 설정

#### 2-1. Git 사용자 정보 설정

```powershell
git config --global user.name "YOUR_NAME"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

확인:

```powershell
git config --global --list
```

#### 2-2. 프로젝트 의존성 동기화

프로젝트 루트에서 실행:

```powershell
uv sync
```

#### 2-3. VS Code 확장 확인

- GitHub Copilot Chat

Chat 입력창에서 간단히 확인:

```text
현재 워크스페이스 구조를 3줄로 요약해줘.
```

응답이 오면 연동 정상입니다.

### 3단계: 기본 사용법 미니 실습

#### uv + Python 3.12

```powershell
uv python list
uv run python --version
```

#### 프로젝트 실행

```powershell
uv sync
uv run pytest -v
```

#### Git

```powershell
git status
git add .
git commit -m "chore: environment check"
```

#### Copilot Chat (Agent)

- Chat 뷰에서 `Agent` 선택
- 아래 프롬프트 실행:

```text
이 저장소의 테스트 실행 명령과 주요 폴더를 요약해줘.
```

### 4단계: 최종 검증

아래를 순서대로 실행해 모두 성공하면 실습 준비 완료입니다.

```powershell
uv --version
uv python list
git --version
code --version
uv sync
uv run pytest -v
```

검증 결과 확인표:

| 항목 | 확인 명령 | 기대 결과 |
|------|----------|----------|
| uv 버전 | `uv --version` | 버전 번호 출력 |
| Python 3.12 | `uv python list` | 3.12.x 포함 확인 |
| Git 버전 | `git --version` | 버전 번호 출력 |
| VS Code | `code --version` | 버전 번호 출력 |
| 의존성 동기화 | `uv sync` | 오류 없이 완료 |
| 테스트 실행 | `uv run pytest -v` | 오류 없이 수집 완료 |
| Copilot Chat | Chat에서 응답 확인 | 응답이 반환됨 |
| Agent 모드 | 드롭다운에서 Agent 선택 | 선택 가능 |

---

## 체크리스트

- [ ] `uv --version` 성공
- [ ] `uv python list`에서 3.12 확인
- [ ] `git --version` 성공
- [ ] `code --version` 성공
- [ ] VS Code에서 Copilot Chat 사용 가능
- [ ] Chat에서 Agent 선택 가능(또는 조직 정책으로 제한 여부 확인)
- [ ] (선택) Copilot Pro 30일 평가판 활성화 완료
- [ ] `uv sync` 성공
- [ ] `uv run pytest -v` 성공

---

## 자주 발생하는 문제와 해결

### `uv` 명령이 인식되지 않을 때

- 터미널을 완전히 종료 후 재실행
- 설치 명령을 다시 실행

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### `python3.12` 명령이 인식되지 않을 때

- `uv python list`로 실제 설치 여부 확인
- 새 터미널을 다시 열어 PATH 반영 확인
- 당장 실행이 필요하면 `uv run python --version`으로 우회 실행

### `code` 명령이 안 될 때

- VS Code 재설치 시 User setup으로 설치
- 설치 후 새 터미널에서 다시 확인

### Copilot Chat/Agent가 안 보일 때

- Copilot/Copilot Chat 확장 설치 및 로그인 상태 점검
- 조직 관리 환경이면 관리자 정책(`chat.agent.enabled`) 확인 필요

### Copilot Pro 평가판 취소 방법

- GitHub `Settings` → `Billing & licensing` → Copilot 섹션 → `Cancel trial`
- 30일 내 취소하면 과금되지 않음

### 테스트 실행 중 의존성 오류가 날 때

```powershell
uv sync
uv run pytest -v
```

를 다시 순서대로 실행합니다.

---

## 참고

### 공식 문서 기준 (최신 확인: 2026-03)

| 항목 | 공식 문서 | 반영 내용 |
|---|---|---|
| uv 설치 | https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2 | Windows PowerShell `install.ps1` 방식 사용 |
| uv로 Python 설치 | https://docs.astral.sh/uv/guides/install-python/ | `uv python install 3.12` 기준 |
| Copilot 설정 | https://code.visualstudio.com/docs/copilot/setup | VS Code에서 Copilot Chat 설정 |
| Copilot 플랜 | https://github.com/features/copilot/plans | Pro 플랜 `Try for 30 days free` 안내 |
| Copilot 플랜 관리 | https://docs.github.com/en/copilot/how-tos/manage-your-account/view-and-change-your-copilot-plan | 30일 평가판 취소/자동 과금 전환 안내 |

참고: 정책/요금은 수시로 바뀔 수 있으므로, 수업 직전 공식 링크를 다시 확인해 주세요.

---

## 다음 단계

실습환경 검증이 끝나면 AI-Native 개발 배경과 시장 변화를 학습합니다.

→ **2교시**: `../02-ai-native-overview/`
