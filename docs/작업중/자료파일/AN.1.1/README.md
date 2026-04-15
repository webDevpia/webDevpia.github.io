# AI-Native 소프트웨어 개발: AI 코딩 에이전트 커스터마이징을 위한 프롬프트 엔지니어링

> **실습환경**: Windows 11 + uv + Python + VS Code + GitHub Copilot Chat (Agent Mode)

---

## 워크스페이스 구조

```
AN.1.1/
├── .github/              ← ★ 실습 결과물 공간 (과정을 통해 직접 채워나갑니다)
│   ├── copilot-instructions.md   (4교시)
│   ├── instructions/             (4교시)
│   ├── prompts/                  (5-6교시)
│   └── agents/                   (7-12교시)
│
├── docs/                 ← 과정 문서 + Context Engineering 실습 문서
├── src/todo/             ← 통합 실습 소스 코드 (Todo Manager)
├── tests/                ← TDD 실습 테스트 코드
├── exercises/            ← 교시별 학습 자료 (참조 자료 / 템플릿 / 솔루션)
│   ├── 01-orientation/           (1교시)
│   ├── 02-ai-native-overview/    (2교시)
│   ├── 03-copilot-customization/ (3교시)
│   ├── 04-custom-instructions/   (4교시)
│   ├── 05-prompt-files/          (5-6교시)
│   ├── 06-custom-agents/         (7-8교시)
│   ├── 07-context-engineering/   (9교시)
│   ├── 08-tdd/                   (10-12교시)
│   └── 09-integration/           (13교시)
│
├── pyproject.toml        ← uv 프로젝트 설정
└── README.md
```

---

## 실습 흐름

1. 각 교시 시작 시 `exercises/XX-주제/README.md` 를 확인합니다.
2. `exercises/XX-주제/starter/` 의 템플릿 파일을 복사하여 `.github/` 에 붙여넣습니다.
3. 내용을 직접 수정하며 실습합니다.
4. 막히면 `exercises/XX-주제/solution/` 을 참조합니다.
5. 13교시 통합 실습에서는 `.github/` 가 완비된 상태로 Todo Manager 전체 구현을 진행합니다.

---

## 환경 설정

```powershell
# 프로젝트 초기화 (uv 사용)
uv sync

# 테스트 실행
uv run pytest

# 테스트 상세 출력
uv run pytest -v
```

---

