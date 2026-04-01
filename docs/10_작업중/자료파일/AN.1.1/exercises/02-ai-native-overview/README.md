# 02. AI-Native 개발 개요

## 학습 목표

- 전통 소프트웨어 개발 방식과 AI-Native 개발 방식의 구조적 차이를 설명할 수 있다.
- 2026년 1분기 기준, AI 코딩 에이전트 생태계의 발전 양상을 데이터 기반으로 해석할 수 있다.
- 생산성 향상 효과와 주니어 채용시장 위축이라는 상반된 현실을 동시에 이해하고 토론할 수 있다.
- GitHub Copilot, Claude Code, Google Antigravity, OpenAI Codex, Cursor를 기능/운영/비용 관점으로 비교할 수 있다.
- 개인 개발자와 교육기관 관점에서 실무적인 도입 전략을 설계할 수 있다.

---

## 이 수업에서 다루는 것

이 교시는 강의 + 토론 중심으로 진행합니다.
실습 명령 실행은 없으며, 아래 순서로 내용을 학습합니다.

1. 2026 Q1 시장 변화와 AI-Native의 등장 배경
2. 전통 개발 vs AI-Native 개발 패러다임 비교
3. 생산성 향상의 실제 근거와 현실적 한계
4. 주니어 채용시장 변화와 포트폴리오 전략
5. 주요 AI 코딩 에이전트 5종 비교 및 교육 비용 시뮬레이션
6. CLI 방식의 부상과 개발자 변화관리 전략
7. 수업 토론 질문으로 내용 정리

---

## 1) 2026 Q1: 왜 지금 AI-Native인가

### 1-1. 시장 신호 요약

| 구분 | 핵심 지표 | 해석 |
|---|---:|---|
| 개발자 AI 활용 | 개발자의 84%가 AI 도구 사용 또는 사용 계획 (SO 2025) | AI가 실험 단계를 넘어 기본 개발 도구로 이동 |
| AI 결과 신뢰 | AI 출력 신뢰 33%, 불신 46% (SO 2025) | 생산성은 높지만 검증 비용이 여전히 큼 |
| AI 불만 지점 | "거의 맞는 답" 66%, "디버깅 시간 증가" 45.2% (SO 2025) | 코드 생성보다 코드 검증/정제 역량이 핵심 |
| AI 직무 전환 | 2025~2030년 일자리 변동 22%, 순증 7%(+7,800만) (WEF 2025) | 직무 소멸/생성 동시 진행, 재훈련 필수 |
| 재훈련 수요 | 100명 중 59명 재훈련 필요, 11명은 전환 위험 (WEF 2025) | 학습 민첩성이 조직 경쟁력의 본질이 됨 |
| 채용 구조 | 전체 채용은 약세지만 AI 언급 채용은 강화 (Indeed 2026) | "아무나 채용"이 아니라 "AI 역량 채용"으로 집중 |

### 1-2. 강한 결론

- AI-Native는 "코딩 자동화"가 아니라 "개발 운영체제의 교체"다.
- 핵심 병목은 작성 속도가 아니라, 검증/리뷰/배포/책임소재 설계다.
- 개인 경쟁력은 "코드를 얼마나 빨리 쓰는가"에서 "AI와 협업해 얼마나 안정적으로 제품을 내는가"로 이동한다.

---

## 2) 전통 개발 vs AI-Native 개발

### 2-1. 개발 패러다임 비교

| 항목 | 전통 개발 | AI-Native 개발 |
|---|---|---|
| 요구사항 해석 | PM/개발자 문서 중심 | 자연어 + 구조화 컨텍스트(문서, 코드, 로그) 동시 활용 |
| 설계 | 선행 설계 후 구현 | 설계-구현-검증의 짧은 루프 반복 |
| 구현 | 인간이 직접 작성 중심 | 인간 의도 + 에이전트 생성/수정/리팩터 |
| 테스트 | 구현 후 테스트 | 생성 단계부터 테스트/검증 동시 수행 |
| 코드 리뷰 | 사람 중심 PR 리뷰 | AI 1차 리뷰 + 사람 최종 승인 (Human in the Loop) |
| 배포/운영 | CI/CD 파이프라인 수동 관리 | 에이전트 기반 이슈 triage, PR 자동화, 운영 보조 |
| 지식 관리 | 위키/문서 분절 | 프로젝트 컨텍스트 + 메모리 + 스킬/룰 파일 기반 |
| 개발자 역할 | 구현자 | 오케스트레이터(문제정의, 검증, 아키텍처 결정) |

### 2-2. 핵심 역량 이동

- Before: 알고리즘/문법 숙련 중심
- After: 문제분해, 컨텍스트 설계, 검증 자동화, 위험 통제, 협업 프로토콜 설계

---

## 3) 생산성 향상: 실제 근거와 현실적 한계

### 3-1. 긍정 시그널

- Stack Overflow 2025:
  - AI 도구 사용/사용 계획: 84%
  - AI 도구/에이전트가 개발 생산성에 긍정적 영향: 52%
  - 에이전트 사용자 집단에서는 생산성 증가 동의 비율이 더 높게 나타남
- Anthropic (2025-04, 소프트웨어 개발 리포트):
  - Claude Code 대화의 자동화 성격 비중 79% (Claude.ai 49% 대비 높음)
  - 코드 에이전트 환경에서 업무 위임 폭이 빠르게 확대
- Anthropic (2026-01, Economic Index v4):
  - Claude 사용은 여전히 코딩 업무에 강하게 집중
  - 성공률/복잡도/작업시간 데이터를 포함한 실사용 지표가 공개되며 "체감"이 아닌 "계량" 가능성 확대

### 3-2. 부정 시그널

- Stack Overflow 2025:
  - "거의 맞는 답"으로 인한 반복 수정: 66%
  - AI 생성 코드 디버깅 시간이 더 걸림: 45.2%
  - 정확도 불신(부분+강한 불신): 46%
- 이는 AI를 "자동 완성기"로만 쓰면 오히려 생산성이 역전될 수 있음을 의미한다.
- 결론: AI-Native 생산성의 본질은 생성량이 아니라 검증 파이프라인의 성숙도다.

---

## 4) 주니어 채용시장 한파: 무엇이 달라졌는가

### 4-1. 데이터로 보는 위축

- SignalFire 2025:
  - Big Tech 신규 채용 중 신입 비중 7%
  - 신입 채용 수는 2023 대비 25% 감소, 2019(팬데믹 이전) 대비 50%+ 감소
  - 스타트업 신입 비중 6% 미만, 2023 대비 11% 감소, 2019 대비 30%+ 감소
- Handshake Class of 2025:
  - 플랫폼 내 구인공고 1년간 15% 감소
  - 공고당 지원자 수 30% 증가
  - 컴퓨터공학 전공생의 비관 인식이 타 전공 대비 높게 나타남
- Indeed Hiring Lab (2026-01):
  - 전체 채용은 정체/약세이지만 AI 언급 채용은 확대
  - 즉, "채용 절벽"이 아니라 "역량 필터 강화"에 가까운 구조 변화

### 4-2. 왜 주니어가 먼저 타격받는가

- 과거 주니어의 업무였던 보일러플레이트/단순 수정/초기 조사 업무를 에이전트가 대체
- 경기 불확실성으로 조직이 "교육 가능한 잠재력"보다 "즉시 전력" 선호
- 팀 생산성 측정 기준이 "개인 산출량"에서 "AI 협업 기반 결과 신뢰성"으로 이동

### 4-3. 수업 포인트

- "AI가 개발자를 대체한다"가 아니라 "개발자 포트폴리오의 가치함수가 바뀐다"가 더 정확한 진단이다.
- 신입 전략은 "많이 코딩했다"보다 "AI와 함께 끝까지 배송했다"(문제정의-구현-검증-릴리즈) 증명이 중요하다.

---

## 5) 2026-03 기준 AI 코딩 에이전트 5종 비교

### 5-1. 제품 성격 비교

| 도구 | 포지셔닝 | 주요 인터페이스 | 강점 | 주의점 |
|---|---|---|---|---|
| GitHub Copilot | IDE/PR/조직 정책 통합형 | VS Code/JetBrains/GitHub/CLI | GitHub 생태계 결합, 엔터프라이즈 정책/감사 적합 | 최신 모델 사용은 Premium Request 관리 필요 |
| Cursor | 에이전트 중심 IDE | IDE + Cloud Agents + CLI | 고성능 워크플로, 모델 선택 폭, 팀 운영 기능 | 사용량 기반 과금 이해 없으면 비용 예측 어려움 |
| Claude Code | 터미널/에이전트 실행형 | Terminal/Desktop/IDE/Slack | 멀티파일 편집, 이슈->PR 흐름 자동화, 강한 코드 이해 | 사용량 상한 및 상위 플랜 비용 고려 필요 |
| OpenAI Codex | ChatGPT 연계 에이전트 + CLI | Web/App/IDE/CLI | ChatGPT 계정 기반 연속 경험, 클라우드 작업/리뷰 지원 | 크레딧/모델별 한도 이해 필요 |
| Google Antigravity | 에이전트 중심 IDE (Google AI 연동) | IDE + Browser/Agent Manager | 무료 개인 플랜, Google AI Pro/Ultra와 자연 결합 | 정량 쿼터/기업 가격은 공개 정보 제한적 |

### 5-2. 가격/과금 구조 (교육 비용 관점)

참고: 지역/세금/환율에 따라 실제 결제액은 달라질 수 있음. 아래는 2026-03-18 기준 공식 페이지 값.

용어 빠른 해설(한/영 병행):

- 좌석 라이선스 비용(seat price): 사용자 1명당 월/연 구독료
- 초과 사용량(overage): 플랜 기본 한도를 넘긴 사용분에 대한 추가 과금
- 롤링 윈도우(rolling window): "지금 시점 기준 직전 N시간" 사용량으로 한도 계산
- 크레딧(credits): 벤더가 제공하는 선불/포함 사용량 포인트

| 도구 | 개인 기본 유료 | 팀/기업 기본 | 학생/교육 혜택 | 과금 포인트 |
|---|---:|---:|---|---|
| GitHub Copilot | Pro $10/월, Pro+ $39/월 | Business $19/좌석/월, Enterprise $39/좌석/월 | Verified Student 무료, 교사/OSS 유지보수자 무료 | Premium Request 추가 구매 $0.04/건 |
| Cursor | Pro $20/월, Pro+ $60/월, Ultra $200/월 | Teams $40/사용자/월, Enterprise 별도 | 대학생 1년 Cursor Pro 무료 | API 풀/초과 사용량(overage), Max mode(개인) API 단가 +20% |
| Claude Code/Claude | Pro $20(월)/$17(연환산), Max 5x $100, Max 20x $200 | Team Standard $25(월)/$20(연환산), Team Premium $125(월)/$100(연환산) | 별도 학생 무료 요금 공개 확인 어려움 | 모델/플랜별 사용량 제한, API는 토큰 과금 별도 |
| OpenAI Codex (ChatGPT 기반) | Plus $20/월 (한국 페이지 표기: 약 KRW 29,000) | Business $30/사용자/월, Enterprise/Edu 별도 | Edu 플랜 존재(세부는 영업 채널) | 포함 한도 초과 시 크레딧/토큰 과금, API 키 별도 |
| Google Antigravity | Individual $0/월 | Team: Workspace AI Ultra for Business 연계(Preview), Org: Cloud(Coming soon) | 개인 무료 플랜 존재 | AI Pro/Ultra 사용 시 AI credits로 초과 사용량(overage) 정산(Vertex API 단가 적용) |

### 5-3. Codex 사용 한도 예시 (5시간 롤링 윈도우, 5-hour rolling window 기준)

해석 가이드:

- 5시간 롤링 윈도우: 현재 시점에서 직전 5시간 사용량을 기준으로 한도를 계산하는 방식
- 표의 값(예: 45-225): 고정값이 아니라 공식 FAQ에 제시된 범위(range) 값

| 플랜 | GPT-5.4 | GPT-5.4-mini | GPT-5.3-Codex |
|---|---:|---:|---:|
| ChatGPT Plus | 45-225 | 10-60 | 10-25 |
| ChatGPT Pro | 300-1500 | 50-400 | 100-250 |
| ChatGPT Business | 45-225 | 10-60 | 10-25 |

참고: 실제 허용량은 서비스 상태, 안전 정책, 계정 상태에 따라 변동될 수 있다.

### 5-4. 교육용 의사결정 체크포인트 (용어 병행 표기)

- 좌석 라이선스 비용(seat price)만 보지 말고 다음 4요소를 함께 계산한다.
  - 기본 좌석 라이선스 비용(base seat price)
  - 초과 사용량 비용(overage: 포함 한도 초과분)
  - 상위 모델 사용 시 단가 변화(model tier uplift)
  - 운영/관리 인력 비용(operations overhead: SSO, 정책, 로그, 보안 검토)

바로 아래 공식으로 묶어 보면 예산 계산이 쉬워진다.

---

## 6) 학생 교육 비용 시뮬레이션 (예시)

수식:

`월 총비용 = (월 좌석 라이선스 비용(seat price) x 인원) + 월 초과 사용량(overage) + 부가 API/크레딧(credits)`

### 6-1. 30명, 4개월 부트캠프 예시 (좌석 라이선스 비용만 단순 비교, seat-only)

| 시나리오 | 계산식 | 총액 |
|---|---|---:|
| Copilot Pro 통일 | $10 x 30 x 4 | $1,200 |
| Cursor Pro 통일 | $20 x 30 x 4 | $2,400 |
| Claude Pro 통일 | $20 x 30 x 4 | $2,400 |
| Codex Plus 통일(USD 기준) | $20 x 30 x 4 | $2,400 |
| Codex Plus 통일(한국 페이지 KRW 기준) | KRW 29,000 x 30 x 4 | KRW 3,480,000 |

### 6-2. 시나리오별 비교 (Copilot Pro 기준, 인원 30명, 4개월)

가정: 기본 좌석 라이선스 비용 $10/인/월, 부가 API/크레딧 $120/월

| 항목 | 보수 시나리오 (5%) | 기준 시나리오 (20%) | 피크 시나리오 (35%) |
|---|---:|---:|---:|
| 월 좌석 라이선스 총액 | $300 | $300 | $300 |
| 월 초과 사용량(overage) | $15 | $60 | $105 |
| 월 부가 API/크레딧(credits) | $120 | $120 | $120 |
| 월 총비용 | $435 | $480 | $525 |
| 4개월 총비용 | $1,740 | $1,920 | $2,100 |
| 6-1(좌석-only) 대비 증가액 | +$540 | +$720 | +$900 |
| 6-1(좌석-only) 대비 증가율 | +45% | +60% | +75% |

강의 활용 팁:

- 기준 시나리오(20%)를 기본값으로 제시하고, 보수(5%)/피크(35%)를 하한-상한 범위로 설명하면 학습자가 예산 감각을 빠르게 잡는다.

### 6-3. 학생 혜택 반영 시

- Copilot Student: 검증 학생은 프리미엄 기능 무료 접근 가능
- Cursor Students: 자격 학생 1년 Pro 무료
- Antigravity Individual: 기본 $0

실무 팁:

- 교육기관은 "전원 유료"보다 "학생 혜택 + 제한적 유료 좌석(조교/강사)" 혼합 모델이 비용 효율적이다.
- 초반 4주간은 무료/학생 요금으로 시작하고, 프로젝트 후반에만 상위 유료 모델을 제한 개방하는 것이 예산 관리에 유리하다.

### 6-4. 미니 결론 (3줄)

- 기본 계획값은 기준 시나리오(월 초과 사용량 20%)로 잡는다.
- 예산 버퍼는 기준 시나리오 총액의 최소 10%를 별도로 확보한다.
- 모니터링 주기는 주 1회 사용량 점검 + 월 1회 플랜/한도 재설정으로 운영한다.

---

## 7) 왜 CLI 방식이 2026년에 두각을 보이는가

### 7-1. 구조적 이유

- 자동화 친화성: 터미널 명령은 스크립트/CI/CD에 바로 연결 가능
- 재현성: 명령 로그 기반으로 같은 작업을 반복 실행하기 쉬움
- 에이전트 병렬화: 이슈 triage, 테스트, 리팩터를 백그라운드로 동시에 실행 가능
- 컨텍스트 통합: Git, 테스트, 빌드, 배포 도구와의 결합 비용이 낮음

### 7-2. 제품 수렴(Convergence)

- Claude Code: "터미널에서 이슈->코드->테스트->PR" 워크플로를 핵심 가치로 제시
- OpenAI Codex: CLI(`@openai/codex`) + IDE + 앱을 단일 계정으로 연동
- Gemini Code Assist: Gemini CLI를 공식 제공(일일 모델 요청 한도 공개)
- GitHub Copilot: Copilot CLI를 기본 포함
- Cursor: CLI 제품군 및 에이전트/클라우드 작업 흐름과 결합

### 7-3. 최신 이슈

- 권한/보안: 강한 자동화는 잘못된 명령 실행 시 리스크가 큼
- 비용 가시성: "무제한"처럼 보이지만 실제는 쿼터/크레딧/초과 사용량(overage) 관리가 핵심
- 품질 책임: 생성 속도가 빨라질수록 최종 책임은 사람에게 집중
- 표준화: MCP 등 도구 연결 표준은 확장성을 높이지만 운영 복잡도도 증가

### 7-4. 미니 결론 (3줄)

- 기본 운영 기준은 "CLI 우선, IDE 보조"로 잡으면 자동화/재현성을 동시에 확보하기 쉽다.
- 도입 초기에는 생산성보다 권한/보안 가드레일(승인 규칙, 실행 범위 제한)을 먼저 고정해야 한다.
- 운영 지표는 주 1회로 점검하며, 자동화 성공률/오류율/비용(초과 사용량)을 함께 추적한다.

---

## 8) 개발자 변화관리: 개인과 팀의 액션플랜

### 8-1. 개인(주니어 포함) 30-60-90일

- 30일:
  - 매일 같은 유형의 업무(버그 수정, 테스트 작성, 문서화)를 AI와 함께 수행
  - "프롬프트"보다 "검증 체크리스트"를 먼저 만든다
- 60일:
  - 1개 프로젝트에서 issue -> branch -> test -> PR -> review 전 과정을 AI 보조로 완주
  - 실패 로그(오답 패턴, 환각 패턴, 보안 실수)를 축적
- 90일:
  - 팀 표준 지침(instructions/prompt/agent)을 직접 작성
  - "AI를 잘 쓰는 사람"에서 "팀의 AI 품질을 높이는 사람"으로 포지셔닝

### 8-2. 팀/조직 체크리스트

- 정책: 허용 모델, 금지 데이터, 승인 경로 정의
- 품질: 테스트 커버리지/정적분석/보안스캔 게이트 강제
- 비용: 좌석 라이선스 + 초과 사용량(overage) + 크레딧 사용 대시보드 운영
- 역량: 정기 교육(프롬프트, 검증, 보안) + 실패 사례 공유

### 8-3. 미니 결론 (3줄)

- 개인은 30-60-90일 루프로 "작업량"보다 "검증 가능한 결과"를 남기는 습관을 먼저 만든다.
- 팀은 도구 숙련도보다 공통 운영 규칙(정책, 품질 게이트, 비용 대시보드)을 먼저 고정한다.
- 조직은 주 1회 실행 지표, 월 1회 역량/프로세스 회고로 변화관리 리듬을 유지한다.

---

## 수업 토론 질문

진행 방법: 각 질문은 3분 개인 정리 + 5분 팀 토론 + 2분 대표 공유 순서로 운영한다.  
답변 형식: 주장 1개 + 근거 데이터 1개 + 다음 액션 1개로 정리한다.

1. "AI가 코드를 써준다"는 말은 우리 팀에서 어느 단계까지 사실인가?
2. 주니어 채용이 줄어드는 상황에서 교육기관은 어떤 포트폴리오를 요구해야 하는가?
3. 우리 조직은 좌석 라이선스 비용(seat price)보다 초과 사용량(overage) 리스크가 큰가, 작은가?
4. CLI 중심 워크플로 도입 시 가장 먼저 바꿔야 할 팀 규칙은 무엇인가?

---

## 체크리스트

- [ ] 2026 Q1 시장 데이터에서 핵심 신호 3개를 설명할 수 있다
- [ ] AI-Native 개발에서 개발자 역할이 어떻게 바뀌는지 설명할 수 있다
- [ ] 생산성 향상의 긍정/부정 시그널을 각각 1개 이상 말할 수 있다
- [ ] 주니어 채용에서 강조되는 포트폴리오 방향을 설명할 수 있다
- [ ] 주요 AI 코딩 에이전트 5종의 포지셔닝 차이를 설명할 수 있다
- [ ] 교육 비용 시뮬레이션에서 초과 사용량(overage)의 영향을 설명할 수 있다
- [ ] 토론 질문에 주장 + 근거 데이터 + 다음 액션 형식으로 답변을 준비했다

---

## 참고

가격/쿼터/플랜은 수시로 변경됩니다. 강의 직전 반드시 공식 링크를 재검증하세요.  
일부 벤더(특히 엔터프라이즈/부가기능)는 정량 가격을 공개하지 않고 영업 문의로 전환됩니다.  
국가/통화/세금/프로모션에 따라 동일 플랜의 실결제 금액이 다를 수 있습니다.

### 참고 자료 (2025 H2~2026 중심)

### 10-1. 노동시장/거시/개발자 데이터

1. Stack Overflow Developer Survey 2025 - AI 섹션  
   https://survey.stackoverflow.co/2025/ai
2. WEF, The Future of Jobs Report 2025 (Key Findings)  
   https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/
3. OECD Employment Outlook 2025  
   https://www.oecd.org/en/publications/oecd-employment-outlook-2025_194a947b-en.html
4. OECD Employment Outlook 2025: United States (Country Note)  
   https://www.oecd.org/en/publications/oecd-employment-outlook-2025-country-notes_f91531f7-en/united-states_a87f27e3-en.html
5. Indeed Hiring Lab (2026-01), AI mentions vs broader hiring weakness  
   https://www.hiringlab.org/2026/01/22/january-labor-market-update-jobs-mentioning-ai-are-growing-amid-broader-hiring-weakness/
6. Handshake State of the Graduate, Class of 2025  
   https://joinhandshake.com/network-trends/class-of-2025-graduation/
7. SignalFire State of Tech Talent Report 2025  
   https://www.signalfire.com/blog/signalfire-state-of-talent-report-2025

### 10-2. AI 코딩 에이전트/제품/가격 (공식)

8. GitHub Copilot Plans  
   https://github.com/features/copilot/plans
9. GitHub Docs - Plans for GitHub Copilot  
   https://docs.github.com/en/copilot/get-started/plans
10. GitHub Docs - Copilot Student 무료 접근  
    https://docs.github.com/en/copilot/how-tos/manage-your-account/free-access-with-copilot-student
11. Cursor Pricing  
    https://cursor.com/pricing
12. Cursor Models & Pricing (usage pool, Max mode)  
    https://cursor.com/docs/models-and-pricing
13. Cursor Students (1년 Pro 무료)  
    https://cursor.com/students
14. Claude Pricing  
    https://claude.com/pricing
15. Claude Team Pricing  
    https://claude.com/pricing/team
16. Claude Max Pricing  
    https://claude.com/pricing/max
17. Claude API Pricing  
    https://claude.com/pricing#api
18. Claude Code 제품 페이지  
    https://claude.com/product/claude-code
19. OpenAI Codex 제품 페이지  
    https://openai.com/codex/
20. OpenAI Developers - Codex Overview  
    https://developers.openai.com/codex/
21. OpenAI Developers - Codex Pricing  
    https://developers.openai.com/codex/pricing
22. OpenAI API Pricing  
    https://openai.com/api/pricing/
23. ChatGPT Pricing  
    https://chatgpt.com/pricing
24. Google AI Plans (Google One)  
    https://one.google.com/about/google-ai-plans/
25. Google Workspace Pricing  
    https://workspace.google.com/pricing.html
26. Google Antigravity Pricing  
    https://antigravity.google/pricing
27. Google Antigravity Plans (quota/overage)  
    https://antigravity.google/docs/plans
28. Gemini Code Assist (가격/한도)  
    https://codeassist.google/
29. Jules (Google Labs, beta/무료/향후 과금 예고)  
    https://blog.google/technology/google-labs/jules/

### 10-3. 보조 리포트 (AI와 개발 업무)

30. Anthropic Economic Index: AI’s impact on software development (2025-04)  
    https://www.anthropic.com/research/impact-software-development
31. Anthropic Economic Index report: economic primitives (2026-01)  
    https://www.anthropic.com/research/anthropic-economic-index-january-2026-report

---

## 다음 단계

2교시 이론을 바탕으로 Copilot 커스터마이징 3요소의 관계를 정리합니다.  
→ **3교시**: `../03-copilot-customization/`
