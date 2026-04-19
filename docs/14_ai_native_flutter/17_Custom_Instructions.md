---
title: "16. Custom Instructions + Prompt Files"
layout: default
parent: AI-Native Flutter
nav_order: 18
permalink: /ai-native-flutter/instructions
---

# 16장. Custom Instructions + Prompt Files
{: .no_toc }

> **Phase 3** · 예상 시간: 90분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 완전 페어 프로그래밍**
> AI(Copilot)와 완전한 협업이 가능합니다.
> 내가 설계하고 AI가 구현합니다. 테스트로 검증합니다.
> "신뢰하되 검증한다(Trust but verify)"가 원칙입니다.

## 학습 목표

- Custom Instructions의 역할을 이해하고 Flutter 프로젝트용 파일을 작성할 수 있다
- `.github/instructions/` 폴더로 파일별 규칙을 관리할 수 있다
- Prompt Files(`.github/prompts/`)로 반복 작업을 자동화할 수 있다

<a id="toc"></a>
## 진행 순서

1. [Custom Instructions란?](#part1) — AI에게 프로젝트 규칙 알려주기
2. [copilot-instructions.md 작성](#part2) — Flutter 프로젝트용 전역 규칙
3. [instructions/ 폴더](#part3) — 파일별 규칙
4. [Prompt Files](#part4) — 반복 작업 템플릿
5. [Context Engineering](#part5) — 충분한 맥락 제공하기
6. [더 알아보기: Flutter MCP 서버](#part6)
7. [정리](#part7)

---

<a id="part1"></a>
## 1️⃣ ⭐ **핵심** — Custom Instructions란? [↑](#toc)

### AI가 모르는 것들

GitHub Copilot은 매우 똑똑하지만, **여러분의 프로젝트**에 대해서는 모릅니다.

- 이 프로젝트는 Dart/Flutter를 사용한다
- 상태 관리는 `setState`를 사용한다
- 위젯은 200줄 이상이면 분리한다
- 테스트는 반드시 작성한다

이런 규칙을 매번 채팅창에 설명해야 한다면 비효율적입니다.

**Custom Instructions**는 이 규칙을 파일로 작성해두면, AI가 항상 이 규칙을 참고해서 코드를 생성합니다.

### 파일 구조

```
프로젝트_루트/
└── .github/
    ├── copilot-instructions.md        ← 전체 프로젝트 공통 규칙
    ├── instructions/
    │   ├── flutter.instructions.md    ← Flutter 위젯 규칙
    │   └── testing.instructions.md   ← 테스트 규칙
    └── prompts/
        ├── new-screen.prompt.md       ← 새 화면 추가 템플릿
        ├── write-tests.prompt.md      ← 테스트 작성 템플릿
        └── debug-widget.prompt.md     ← 위젯 디버깅 템플릿
```

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — copilot-instructions.md 작성 [↑](#toc)

### 파일 생성

터미널에서:

```bash
mkdir -p .github/instructions .github/prompts
touch .github/copilot-instructions.md
```

### 내용 작성

`.github/copilot-instructions.md`:

```markdown
# Flutter 프로젝트 AI 협업 규칙

## 프로젝트 개요
이 프로젝트는 Flutter(Dart)로 작성된 모바일 앱입니다.
대상: Android, iOS

## 언어 및 프레임워크
- 언어: Dart 3.x
- 프레임워크: Flutter 3.x (Material 3)
- 최소 SDK: Android API 21, iOS 12.0

## Dart 코딩 컨벤션

### 명명 규칙
- 클래스: `PascalCase` (예: `WeatherScreen`, `UserProfile`)
- 변수/함수: `camelCase` (예: `fetchWeather`, `userName`)
- 상수: `lowerCamelCase` with const (예: `const double kPadding = 16.0;`)
- 파일: `snake_case` (예: `weather_screen.dart`, `user_profile.dart`)

### 타입 규칙
- 모든 공개 API에는 명시적 타입 선언 필수
- `dynamic` 사용 최소화 (JSON 파싱 시 즉시 타입 캐스팅)
- nullable 타입은 필요한 경우에만 사용 (`?`)

### 코드 품질
- 함수는 50줄 이하로 유지
- 중첩 depth는 3단계 이하로 유지
- 매직 넘버 대신 이름 있는 상수 사용

## 위젯 규칙

### 위젯 분리 기준
- 위젯 클래스가 200줄을 초과하면 분리
- 재사용 가능한 UI 요소는 `lib/widgets/` 폴더에 분리
- 화면 단위 위젯은 `lib/screens/` 폴더에 위치

### StatelessWidget vs StatefulWidget
- 내부 상태가 없으면 `StatelessWidget` 사용
- 내부 상태가 있으면 `StatefulWidget` 사용
- 전역/공유 상태는 `Provider` 사용 (해당 패키지가 있을 때)

### 상태 관리
- 단순 UI 상태: `setState()` 사용
- 여러 위젯 공유 상태: `Provider` + `ChangeNotifier` 사용
- `setState()`는 State 클래스 내부에서만 호출

## 프로젝트 구조

```
lib/
├── main.dart
├── models/          # 데이터 모델 클래스
├── services/        # API, DB, 스토리지 서비스
├── screens/         # 화면 위젯 (한 파일 = 한 화면)
├── widgets/         # 재사용 가능한 위젯
└── utils/           # 유틸리티 함수
```

## API 호출 규칙
- HTTP 호출은 Service 클래스에서만 수행
- 에러 처리: try/catch로 감싸고 의미 있는 에러 메시지 반환
- 응답 모델: `fromJson()` factory 생성자 사용

## 테스트 규칙
- 새 Service 클래스 작성 시 반드시 단위 테스트 작성
- 테스트 파일 위치: `test/` 폴더 (lib 구조와 동일)
- 테스트 함수명: `test('given_when_then 형식', ...)`

## 금지 사항
- `print()` 대신 `debugPrint()` 사용
- `BuildContext`를 비동기 간극(await) 뒤에서 직접 사용 금지
- 위젯 트리 안에 비즈니스 로직 직접 작성 금지
```

### Copilot에서 어떻게 작동하는가

VS Code에서 Copilot Chat을 열면 이 파일의 내용이 자동으로 시스템 프롬프트에 포함됩니다. 별도 설정 없이 `.github/copilot-instructions.md` 파일만 있으면 됩니다.

---

<a id="part3"></a>
## 3️⃣ ⭐ **핵심** — instructions/ 폴더: 파일별 규칙 [↑](#toc)

### 파일별 규칙이란?

`copilot-instructions.md`가 전체 프로젝트 규칙이라면,  
`instructions/` 폴더는 **특정 파일 패턴에만** 적용되는 규칙입니다.

예: `*_screen.dart` 파일을 편집할 때만 Flutter 위젯 규칙이 활성화

### flutter.instructions.md

`.github/instructions/flutter.instructions.md`:

```markdown
---
applyTo: "lib/**/*.dart"
---

# Flutter 위젯 작성 규칙

## 위젯 생성 패턴

새 StatelessWidget:
```dart
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
```

새 StatefulWidget:
```dart
class MyWidget extends StatefulWidget {
  const MyWidget({super.key});

  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
```

## 스타일 규칙
- 색상: `Theme.of(context).colorScheme` 사용 (하드코딩 금지)
- 폰트 크기: `Theme.of(context).textTheme` 사용
- 간격: `const SizedBox(height: 16)` 또는 `const EdgeInsets.all(16)` 패턴
- Material 3 사용: `useMaterial3: true`

## 네비게이션
- 화면 이동: `Navigator.push(context, MaterialPageRoute(...))`
- 뒤로 가기: `Navigator.pop(context)`
- 데이터 전달: 생성자 매개변수로 전달

## 비동기 처리
- API 데이터 표시: `FutureBuilder` 사용
- 로딩 상태: `CircularProgressIndicator()` 사용
- 에러 상태: 에러 메시지 + 재시도 버튼 표시
```

### testing.instructions.md

`.github/instructions/testing.instructions.md`:

```markdown
---
applyTo: "test/**/*.dart"
---

# Flutter 테스트 작성 규칙

## 단위 테스트 패턴

```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('클래스명', () {
    late 클래스명 sut; // System Under Test

    setUp(() {
      sut = 클래스명();
    });

    test('given_when_then: 조건_동작_기대결과', () {
      // Arrange
      // ...

      // Act
      final result = sut.method();

      // Assert
      expect(result, equals(기대값));
    });
  });
}
```

## 위젯 테스트 패턴

```dart
testWidgets('위젯명_조건_기대동작', (WidgetTester tester) async {
  // Build
  await tester.pumpWidget(
    MaterialApp(home: 테스트할위젯()),
  );

  // Find & Verify
  expect(find.text('텍스트'), findsOneWidget);
  expect(find.byType(위젯타입), findsWidgets);

  // Interact
  await tester.tap(find.byIcon(Icons.add));
  await tester.pump(); // 상태 변화 반영

  // Verify after interaction
  expect(find.text('결과'), findsOneWidget);
});
```

## 테스트 명명 규칙
- 단위 테스트: `'[조건]일 때 [동작]하면 [결과]여야 한다'`
- 위젯 테스트: `'[위젯명] [조건]에서 [기대동작]'`

## 테스트 범위
- Service 클래스: 모든 public 메서드에 테스트 필수
- Model 클래스: fromJson() 메서드 테스트 필수
- 위젯: 핵심 인터랙션 테스트 (탭, 입력, 네비게이션)
```

---

<a id="part4"></a>
## 4️⃣ ⭐ **핵심** — Prompt Files: 반복 작업 템플릿 [↑](#toc)

### Prompt Files란?

자주 하는 작업을 **프롬프트 템플릿**으로 저장합니다.  
Copilot Chat에서 `/` 명령어로 빠르게 호출할 수 있습니다.

### new-screen.prompt.md

`.github/prompts/new-screen.prompt.md`:

```markdown
---
mode: 'agent'
description: '새 Flutter 화면 생성'
---

# 새 화면 추가

다음 규칙에 따라 새 Flutter 화면을 생성해주세요.

## 입력 정보
- 화면 이름: [화면 이름 (PascalCase)]
- 화면 역할: [이 화면이 하는 일]
- 받아야 할 데이터: [생성자로 받을 데이터가 있으면 명시]
- 상태 유형: [StatelessWidget / StatefulWidget]

## 생성할 파일
- `lib/screens/[snake_case_name]_screen.dart`

## 요구사항
1. `copilot-instructions.md`의 위젯 규칙 준수
2. AppBar에 화면 제목 표시
3. 생성자에 `super.key` 포함
4. const 생성자 사용
5. TODO 주석으로 구현할 부분 표시
```

### write-tests.prompt.md

`.github/prompts/write-tests.prompt.md`:

```markdown
---
mode: 'agent'
description: '선택한 파일의 테스트 작성'
---

# 테스트 작성

현재 선택한 파일에 대한 Flutter 단위 테스트를 작성해주세요.

## 요구사항
1. `testing.instructions.md` 규칙 준수
2. 모든 public 메서드에 테스트 케이스 생성
3. 정상 케이스(happy path)와 예외 케이스(edge case) 모두 포함
4. 테스트 파일 위치: `test/` 폴더 (lib 구조 동일하게 미러링)
5. `group()`으로 클래스별 테스트 묶기

## 테스트 케이스 포함 사항
- 정상 입력 → 올바른 출력
- 빈 값 / null 입력
- 경계값 (빈 리스트, 최댓값 등)
- 예외 발생 케이스 (throw 검증)
```

### debug-widget.prompt.md

`.github/prompts/debug-widget.prompt.md`:

```markdown
---
mode: 'ask'
description: '위젯 문제 진단 및 수정'
---

# 위젯 디버깅

아래 정보를 바탕으로 Flutter 위젯 문제를 진단해주세요.

## 증상
[어떤 문제가 발생하는지 설명]

## 에러 메시지
```
[Flutter console 에러 메시지 붙여넣기]
```

## 관련 코드
[문제가 발생하는 위젯 코드]

## 확인 항목
1. RenderFlex overflow 문제인가?
2. setState() 호출 위치가 올바른가?
3. BuildContext 사용이 비동기 간극 이후인가?
4. initState()에서 적절히 초기화되는가?
5. dispose()에서 리소스를 해제하는가?
```

### Prompt Files 사용 방법

1. VS Code에서 Copilot Chat 열기 (`Ctrl+Shift+I`)
2. 메시지 입력창에 `/` 입력
3. `new-screen`, `write-tests`, `debug-widget` 등 선택
4. 필요한 정보 채워서 전송

---

<a id="part5"></a>
## 5️⃣ 🚀 **도전** — Context Engineering: 충분한 맥락 제공하기 [↑](#toc)

### 맥락이 왜 중요한가

같은 질문이라도 맥락이 다르면 AI 답변의 품질이 크게 달라집니다.

**나쁜 프롬프트:**
> "날씨 앱 만들어줘"

**좋은 프롬프트:**
> "Flutter 날씨 앱을 만들어줘.  
> - OpenWeatherMap API 사용  
> - http 패키지로 GET 요청  
> - 도시명 입력 → 온도/설명/아이콘 표시  
> - FutureBuilder로 로딩/성공/에러 처리  
> - WeatherService 클래스에 API 호출 로직 분리  
> - test/services/weather_service_test.dart에 단위 테스트 포함"

### 좋은 맥락의 구성 요소

| 요소 | 내용 | 예시 |
|------|------|------|
| 기술 스택 | 언어, 프레임워크, 패키지 | Flutter, http, provider |
| 현재 구조 | 기존 파일/클래스 | WeatherService가 있고... |
| 목표 결과 | 무엇을 만들어야 하는지 | 도시 검색 → 날씨 표시 |
| 제약 조건 | 지켜야 할 규칙 | setState만 사용, TDD |
| 예시 | 원하는 코드 스타일 | fromJson() 패턴 사용 |

### #파일 참조 기능

Copilot Chat에서 `#파일명` 형식으로 현재 파일을 맥락으로 추가할 수 있습니다.

```
#weather_service.dart 를 참고해서 이 서비스의 단위 테스트를 작성해줘.
WeatherService.fetchWeather() 메서드의 정상/에러 케이스를 모두 포함해줘.
```

### 점진적 맥락 쌓기

한 번에 모든 것을 요청하지 말고, 단계적으로 진행합니다.

```
1단계: "Weather 모델 클래스 만들어줘 (필드: temp, description, icon)"
2단계: "WeatherService 클래스의 fetchWeather(String city) 메서드 만들어줘"
3단계: "#weather_service.dart 참고해서 테스트 작성해줘"
4단계: "WeatherScreen 위젯 만들어줘. FutureBuilder 사용, 위의 서비스 호출"
```

---

<a id="part6"></a>
## 6️⃣ 📖 **더 알아보기** — Flutter MCP 서버 소개 [↑](#toc)

### MCP(Model Context Protocol)란?

AI 모델이 외부 도구(파일 시스템, 데이터베이스, API)에 접근할 수 있도록 하는 표준 프로토콜입니다.

### Flutter 개발에 MCP를 활용하면

| MCP 서버 | 기능 |
|----------|------|
| Filesystem MCP | 프로젝트 파일을 AI가 직접 읽기 |
| Flutter/Dart MCP | pub.dev 패키지 문서, API 참조 |
| Simulator MCP | iOS 시뮬레이터 제어 |

### 현재 지원 상황

MCP는 빠르게 발전하는 기술입니다. Claude Desktop, VS Code의 Copilot Chat에서 MCP 서버를 직접 연결할 수 있습니다. 자세한 설정 방법은 각 도구의 공식 문서를 참고하세요.

> 이 교육과정에서는 Custom Instructions와 Prompt Files만으로도 충분한 AI 협업이 가능합니다. MCP는 심화 탐구 항목입니다.

---

<a id="part7"></a>
## 7️⃣ 정리 [↑](#toc)

### 이 장에서 만든 파일들

```
.github/
├── copilot-instructions.md        ✅ 전체 규칙 (Dart/Flutter 컨벤션)
├── instructions/
│   ├── flutter.instructions.md   ✅ Flutter 파일 전용 규칙
│   └── testing.instructions.md   ✅ 테스트 파일 전용 규칙
└── prompts/
    ├── new-screen.prompt.md       ✅ 새 화면 생성 템플릿
    ├── write-tests.prompt.md      ✅ 테스트 작성 템플릿
    └── debug-widget.prompt.md     ✅ 디버깅 템플릿
```

### 핵심 원칙

> AI는 규칙을 알아야 규칙에 맞는 코드를 생성합니다.  
> Custom Instructions는 "AI에게 보내는 팀 코드 리뷰 가이드"입니다.

### 체크리스트

- [ ] `.github/copilot-instructions.md` 파일을 만들었다
- [ ] Dart 명명 규칙, 위젯 분리 기준, 상태 관리 규칙을 담았다
- [ ] `flutter.instructions.md`와 `testing.instructions.md`를 만들었다
- [ ] `new-screen.prompt.md`로 새 화면을 빠르게 만들 수 있다
- [ ] Copilot Chat에서 `/` 명령어로 Prompt File을 호출해봤다

### 다음 장 예고

다음 장에서는 **테스트 입문 + TDD**를 배웁니다.  
이 장에서 만든 `testing.instructions.md`가 바로 활용됩니다.

---

→ **다음 내용으로 넘어갑시다**: [17. 테스트 입문 + TDD](/ai-native-flutter/testing-tdd)
