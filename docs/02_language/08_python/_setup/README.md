---
title: 자가진단 Google Form 만들기
layout: default
parent: Python (8시간 재수강)
grand_parent: Language
nav_order: 100
permalink: /language/python/setup-diagnostic-form
---

{% raw %}

# 사전 자가진단을 Google Form으로 만들기

`docs/02_language/08_python/_setup/create_diagnostic_form.gs` 스크립트를 한 번 실행하면 **10문항 + 이름/이메일 + 관심 챕터 조사** 가 포함된 퀴즈형 Google Form이 자동 생성됩니다.

---

## 1단계 — Apps Script 프로젝트 만들기

1. [https://script.google.com](https://script.google.com) 접속
2. 좌측 상단 **[+ 새 프로젝트]** 클릭
3. 좌측 코드 영역의 기본 `function myFunction() { ... }` 모두 삭제
4. `_setup/create_diagnostic_form.gs` 파일 **전체** 복사 → 붙여넣기
5. 좌측 상단 프로젝트 이름을 클릭해 적당한 이름으로 변경 (예: "Python 자가진단 폼")
6. **💾 저장** (Ctrl/Cmd+S)

---

## 2단계 — 실행

1. 상단 함수 선택 드롭다운에서 **`createPythonDiagnosticForm`** 선택
2. **▶ [실행]** 버튼 클릭
3. (처음 실행 시) 권한 동의 절차:
   - **[권한 검토]** 클릭
   - 본인 Google 계정 선택
   - "Google에서 확인하지 않은 앱" 경고 → 하단 **[고급]** → **[프로젝트로 이동(안전하지 않음)]**
   - **[허용]** 클릭

> ℹ️ 본인이 만든 스크립트이므로 외부 노출 위험은 없습니다. Google이 검증한 앱이 아니라는 일반 경고일 뿐입니다.

---

## 3단계 — 생성된 URL 확인

실행 후 하단 **실행 로그(Ctrl+Enter 또는 우측 하단 아이콘)** 패널을 확인:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Google Form 생성 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 학생용 응답 URL:
   https://docs.google.com/forms/d/e/xxx/viewform
🔗 단축 URL: https://forms.gle/xxxxxxx

✏️  강사용 편집 URL:
   https://docs.google.com/forms/d/yyy/edit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

- **단축 URL** 을 학생에게 공유 (가장 깔끔)
- **편집 URL** 로 들어가서 문구·디자인 손보기 가능

---

## 4단계 — 응답을 스프레드시트로 모으기 (선택)

1. 편집 URL 열기 → 상단 **[응답]** 탭
2. 우측 상단 **초록색 스프레드시트 아이콘** 클릭
3. **새 스프레드시트 만들기** → 이름 정하기 → [만들기]

이제 학생이 응답할 때마다 한 행씩 자동 추가됩니다. 강사가 점수·답안을 한눈에 확인 + 평균 계산 + 챕터별 정답률 분석 가능.

---

## 문제 발생 시

### "Authorization required" 가 계속 뜸
브라우저 시크릿 모드 또는 캐시 삭제 후 재시도. 학교/회사 계정이면 IT 관리자가 차단했을 수 있음 — 개인 Gmail로 시도.

### `setIsQuiz is not a function` 같은 에러
Google Apps Script V8 런타임 확인:
- 좌측 ⚙️ **[프로젝트 설정]** → "Chrome V8 런타임 사용" 체크

### URL 단축이 안 됨
`form.shortenFormUrl(publishedUrl)` 라인을 주석 처리하고 publishedUrl만 사용. (드물게 지역 제한 있음)

### 폼을 다시 만들고 싶음
이전 폼은 Google Drive에 남아 있습니다. 스크립트를 한 번 더 실행하면 **새 폼이 추가로** 생성됩니다. 기존 폼은 Drive에서 수동 삭제.

---

## 폼 구성 요약

| # | 형식 | 자동 채점 | 비고 |
|---|---|---|---|
| 이름 | 단답 | — | 필수, 식별용 |
| Q1 변수·타입 | 객관식 | ✅ | 정답: 에러 |
| Q2 == vs is | 장문 | ❌ (수동) | 모범답안·해설 자동 표시 |
| Q3 슬라이싱 | 장문 | ❌ | 모범답안 표시 |
| Q4 mutability | 객관식 | ✅ | 정답: [1,2,3,4] |
| Q5 KeyError | 단답 | ❌ | 정답·해설 표시 |
| Q6 range | 단답 | ❌ | 정답·해설 표시 |
| Q7 return | 단답 | ❌ | 정답: None |
| Q8 가변 기본값 | 객관식 | ✅ | 정답: ["apple","banana"] |
| Q9 컴프리헨션 | 단답 | ❌ | 정답: [4,8] |
| Q10 try/except | 장문 | ❌ | 모범답안 표시 |
| 관심 챕터 | 객관식 | — | 강의 비중 조정용 |

> 💡 Google Forms 단답형의 자동 채점은 **정확 일치**만 지원합니다. "[4, 8]" vs "[4,8]" 같은 사소한 차이로 오답 처리되는 걸 피하려고 단답·장문은 **수동 채점**으로 설정했습니다. 강사 화면(응답 탭 → 개인 응답)에서 한 명씩 보며 점수 부여하시면 됩니다.

{% endraw %}
