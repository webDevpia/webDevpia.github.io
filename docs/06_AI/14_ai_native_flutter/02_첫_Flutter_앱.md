---
title: "01. 첫 Flutter 앱 만들기"
layout: default
parent: AI-Native Flutter
nav_order: 3
permalink: /ai-native-flutter/first-app
---

# 1장. 첫 Flutter 앱 만들기
{: .no_toc }

> **Phase 0** · 예상 시간: 90분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 개념 이해 전용**
> 오류 메시지 해석은 AI에게 물어봐도 됩니다. 코드를 대신 써달라는 요청은 아직 하지 마세요.

## 학습 목표
- `flutter create` 명령어로 새 프로젝트를 만들 수 있다
- Flutter 프로젝트 폴더 구조를 설명할 수 있다
- Hot Reload를 이용해 앱을 실시간으로 수정할 수 있다

<a id="toc"></a>
## 진행 순서
1. [flutter create로 프로젝트 생성](#part1)
2. [프로젝트 폴더 구조 이해](#part2)
3. [main.dart 코드 읽기](#part3)
4. [Hot Reload 체험](#part4)
5. [Hot Reload vs Hot Restart](#part5)
6. [실제 Android 기기 연결](#part6)
7. [실습: 나만의 인사 앱](#part7)
8. [정리](#part8)

---

<a id="part1"></a>
## 1️⃣ ⭐ **핵심** — flutter create로 프로젝트 생성 [↑](#toc)

### 프로젝트 만들기

터미널(명령 프롬프트)을 열고 작업할 폴더로 이동합니다.

```bash
# 원하는 위치로 이동 (예: 바탕화면의 flutter_projects 폴더)
# Windows:
cd C:\Users\사용자이름\Desktop

# macOS:
cd ~/Desktop
```

Flutter 앱을 만드는 명령어:
```bash
flutter create my_first_app
```

> **이름 규칙**: 앱 이름에는 **소문자와 밑줄(_)만** 사용하세요. 공백, 대문자, 특수문자는 오류가 납니다.

성공하면 이런 메시지가 나옵니다:
```
Creating project my_first_app...
  ...
Your application code is in my_first_app/lib/main.dart.

Run your application with:
  $ cd my_first_app
  $ flutter run
```

### 앱 실행하기

```bash
cd my_first_app
flutter run
```

에뮬레이터가 켜져 있으면 앱이 자동으로 설치되고 실행됩니다. 처음 실행 시 1~3분 정도 걸립니다 (컴파일 시간).

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — 프로젝트 폴더 구조 이해 [↑](#toc)

### 폴더 구조 한눈에 보기

VS Code에서 `my_first_app` 폴더를 열면 이런 구조가 보입니다:

```
my_first_app/
├── lib/                  ← 여기가 핵심! Dart 코드가 여기에
│   └── main.dart         ← 앱의 시작점
├── android/              ← Android 앱 관련 파일 (건드리지 않음)
├── ios/                  ← iOS 앱 관련 파일 (건드리지 않음)
├── web/                  ← 웹 앱 관련 파일
├── test/                 ← 테스트 코드 폴더
│   └── widget_test.dart  ← 기본 테스트 파일
├── pubspec.yaml          ← 앱 설정 파일 (패키지 의존성 등)
└── README.md             ← 프로젝트 설명서
```

### 각 폴더/파일의 역할

| 이름 | 역할 | 자주 수정? |
|------|------|-----------|
| `lib/main.dart` | 앱의 시작점, 화면 구성 | ✅ 매일 |
| `pubspec.yaml` | 앱 이름, 패키지 목록, 에셋(이미지 등) 등록 | ✅ 자주 |
| `android/` | Android 빌드 설정 | 거의 안함 |
| `ios/` | iOS 빌드 설정 | 거의 안함 |
| `test/` | 자동화 테스트 코드 | Phase 3에서 |

> **비유**: `lib/` 폴더는 건물의 "인테리어 공간"이고, `android/`, `ios/`는 "건물의 외벽"입니다. 우리가 꾸미는 곳은 인테리어 공간(lib/)입니다.

### pubspec.yaml 미리보기

```yaml
name: my_first_app
description: "A new Flutter project."
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter
```

- `name`: 앱의 패키지 이름
- `version`: 앱 버전 (앱스토어 제출 시 사용)
- `dependencies`: 프로젝트에서 사용하는 외부 패키지들

---

<a id="part3"></a>
## 3️⃣ ⭐ **핵심** — main.dart 코드 읽기 [↑](#toc)

`lib/main.dart`를 VS Code에서 엽니다. 한 줄씩 읽어보겠습니다.

```dart
// 1. Flutter Material 디자인 라이브러리 불러오기
import 'package:flutter/material.dart';

// 2. 앱의 시작점 — 이 함수부터 실행 시작
void main() {
  runApp(const MyApp());
}

// 3. 앱 전체를 감싸는 루트 위젯
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

// 4. 홈 화면 위젯
class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

// 5. 홈 화면의 상태(State)
class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text('You have pushed the button this many times:'),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

### 코드 설명 (한 블록씩)

**1. import 문** — 도구 상자 가져오기
```dart
import 'package:flutter/material.dart';
```
> 마치 요리할 때 칼, 도마 등 도구를 꺼내는 것처럼, Flutter의 기본 도구들을 가져옵니다.

**2. main() 함수** — 앱의 시동 버튼
```dart
void main() {
  runApp(const MyApp());
}
```
> 책의 첫 페이지처럼, 앱을 실행하면 가장 먼저 이 함수가 호출됩니다.

**3. MyApp class** — 앱 전체 설정
```dart
class MyApp extends StatelessWidget { ... }
```
> 건물의 설계도면입니다. MaterialApp은 Material Design(Google의 디자인 시스템)을 적용합니다.

**4-5. MyHomePage** — 실제 화면
```dart
class MyHomePage extends StatefulWidget { ... }
class _MyHomePageState extends State<MyHomePage> { ... }
```
> StatefulWidget은 상태(데이터)가 변할 수 있는 화면입니다. 버튼을 누르면 숫자가 바뀌기 때문에 상태가 있습니다.

---

<a id="part4"></a>
## 4️⃣ ⭐ **핵심** — Hot Reload 체험 [↑](#toc)

### Hot Reload란?

Hot Reload는 코드를 수정하면 **1-2초 안에** 앱에 반영해주는 기능입니다. 앱을 처음부터 다시 시작하지 않아도 됩니다.

> **비유**: 레고를 만들다가 한 블록만 교체하는 것처럼, 변경된 부분만 업데이트합니다.

### 텍스트 바꾸기

`lib/main.dart`에서 이 부분을 찾아보세요:
```dart
const Text('You have pushed the button this many times:'),
```

이렇게 바꿔보세요:
```dart
const Text('버튼을 이만큼 눌렀어요:'),
```

저장하면 (`Ctrl+S` 또는 `Cmd+S`) 즉시 에뮬레이터에 반영됩니다!

### 색상 바꾸기

`seedColor`를 찾아서 색상을 바꿔보세요:
```dart
// 변경 전
colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),

// 변경 후 — 빨간색
colorScheme: ColorScheme.fromSeed(seedColor: Colors.red),

// 초록색
colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),

// 주황색
colorScheme: ColorScheme.fromSeed(seedColor: Colors.orange),
```

저장하면 앱 전체 테마 색상이 바뀝니다.

### 타이틀 바꾸기

```dart
// 변경 전
home: const MyHomePage(title: 'Flutter Demo Home Page'),

// 변경 후
home: const MyHomePage(title: '내 첫 번째 앱!'),
```

---

<a id="part5"></a>
## 5️⃣ 📖 **더 알아보기** — Hot Reload vs Hot Restart [↑](#toc)

### 두 가지 새로고침 방식

| 구분 | Hot Reload | Hot Restart |
|------|-----------|------------|
| **단축키 (터미널)** | `r` | `R` |
| **VS Code 버튼** | ⚡ (번개) | 🔄 (화살표 원) |
| **속도** | 매우 빠름 (1-2초) | 빠름 (3-5초) |
| **상태 유지** | ✅ 카운터 숫자 유지 | ❌ 카운터 0으로 초기화 |
| **언제 필요?** | 대부분의 UI 수정 | 변수 초기값 변경, 새 패키지 추가 |

### 실습: 차이 직접 확인하기

1. 버튼을 5번 눌러서 카운터를 5로 만드세요
2. 텍스트를 수정하고 저장하세요 → **Hot Reload**: 카운터가 5 그대로
3. 터미널에서 `R` 키를 누르세요 → **Hot Restart**: 카운터가 0으로 초기화

---

<a id="part6"></a>
## 6️⃣ 🚀 **도전** — 실제 Android 기기 연결 [↑](#toc)

에뮬레이터보다 훨씬 빠르게 실행됩니다. 본인의 Android 스마트폰이 있다면 연결해보세요.

### USB 디버깅 활성화

**Android 기기에서:**
1. **설정** → **휴대전화 정보** (또는 **기기 정보**)
2. **소프트웨어 정보** → **빌드 번호**를 **7번 연속** 탭
3. "개발자가 되셨습니다" 메시지 확인
4. 뒤로 가서 **개발자 옵션** 메뉴 진입
5. **USB 디버깅** 활성화

### USB 연결

1. USB 케이블로 컴퓨터에 연결
2. 기기에서 "USB 디버깅을 허용할까요?" → **허용** 탭
3. 터미널에서 기기 확인:
   ```bash
   flutter devices
   # 연결된 기기 목록에 스마트폰이 나타남
   ```
4. 앱 실행:
   ```bash
   flutter run
   ```

> **Mac + iPhone**: iPhone은 macOS에서만 연결 가능하며, Xcode가 설치되어 있어야 합니다. Apple Developer 계정(무료)도 필요합니다.

---

<a id="part7"></a>
## 7️⃣ ⭐ **핵심** — 실습: 나만의 인사 앱 [↑](#toc)

지금까지 배운 것을 응용해서 **나만의 인사 앱**을 만들어봅니다.

### 목표

- 앱 이름을 내 이름으로 바꾸기
- 메시지를 "안녕하세요, [이름]입니다!"로 바꾸기
- 배경색/테마색을 좋아하는 색으로 바꾸기
- 버튼 아이콘을 바꾸기

### Step 1: 앱 타이틀 변경

```dart
// lib/main.dart
home: const MyHomePage(title: '김민준의 앱'),
```

### Step 2: 화면 메시지 변경

기존 카운터 앱의 텍스트들을 바꿔봅니다:
```dart
// 변경 전
const Text('You have pushed the button this many times:'),

// 변경 후
const Text('안녕하세요, 김민준입니다! 버튼을 눌러보세요:'),
```

### Step 3: 테마 색상 변경

```dart
colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
```

사용 가능한 색상들:
```dart
Colors.red       // 빨강
Colors.blue      // 파랑
Colors.green     // 초록
Colors.orange    // 주황
Colors.purple    // 보라
Colors.teal      // 청록
Colors.pink      // 분홍
Colors.indigo    // 남색
```

### Step 4: 버튼 아이콘 변경

```dart
// 변경 전
child: const Icon(Icons.add),

// 변경 후 — 하트 아이콘
child: const Icon(Icons.favorite),

// 또는 엄지척
child: const Icon(Icons.thumb_up),

// 또는 별
child: const Icon(Icons.star),
```

모든 Material 아이콘 목록: [fonts.google.com/icons](https://fonts.google.com/icons)

### Step 5: AppBar 색상 커스터마이징

```dart
appBar: AppBar(
  backgroundColor: Colors.teal,        // AppBar 배경색
  foregroundColor: Colors.white,        // 텍스트/아이콘 색상
  title: Text(widget.title),
),
```

### 최종 코드 예시

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '김민준의 앱',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: '김민준의 앱'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text('안녕하세요, 김민준입니다!'),
            const Text('버튼을 이만큼 눌렀어요:'),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: '누르기',
        child: const Icon(Icons.favorite),
      ),
    );
  }
}
```

---

<a id="part8"></a>
## 8️⃣ 정리 [↑](#toc)

### 이 장에서 배운 것

| 개념 | 설명 |
|------|------|
| `flutter create` | 새 Flutter 프로젝트 생성 |
| `flutter run` | 앱 실행 |
| `lib/main.dart` | 앱의 핵심 코드 파일 |
| `pubspec.yaml` | 앱 설정 + 패키지 목록 |
| Hot Reload | 저장하면 즉시 반영 (상태 유지) |
| Hot Restart | 앱 전체 재시작 (상태 초기화) |
| `StatelessWidget` | 상태 변경이 없는 위젯 |
| `StatefulWidget` | 상태가 변하는 위젯 (카운터 등) |

### 완성 체크리스트

- [ ] `flutter create` 로 프로젝트 생성 성공
- [ ] 에뮬레이터 또는 실제 기기에서 앱 실행 성공
- [ ] Hot Reload로 텍스트 변경 확인
- [ ] Hot Reload vs Hot Restart 차이 경험
- [ ] 나만의 인사 앱 완성 (이름, 색상, 아이콘 변경)

### 💪 보너스 챌린지

1. 카운터가 10에 도달하면 숫자 색상이 빨간색으로 바뀌게 해보세요
2. 버튼을 두 개 만들어서 하나는 +1, 하나는 -1이 되게 해보세요

### 다음 장 예고

다음 장부터는 Dart 언어를 본격적으로 배웁니다. 변수, 타입, 조건문, 반복문... Flutter 앱을 자유자재로 만들기 위한 언어 기초를 다집니다.

---

---

→ **다음 내용으로 넘어갑시다**: [02. Dart — 변수와 데이터 타입](/ai-native-flutter/dart-variables)
