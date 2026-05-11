---
title: "02. Dart — 변수와 데이터 타입"
layout: default
parent: AI-Native Flutter
nav_order: 4
permalink: /ai-native-flutter/dart-variables
---

# 2장. Dart — 변수와 데이터 타입
{: .no_toc }

> **Phase 1** · 예상 시간: 90분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 설명 모드만**
> 코드의 의미나 오류 원인을 AI에게 설명해달라고 요청할 수 있습니다. 하지만 "이 코드 대신 써줘"는 아직 하지 마세요. 직접 써야 실력이 쌓입니다.

## 학습 목표
- 변수의 개념을 이해하고 Dart에서 변수를 선언할 수 있다
- `int`, `double`, `String`, `bool` 타입을 구분하여 사용할 수 있다
- `const`와 `final`의 차이를 설명하고 적절히 활용할 수 있다
- Null Safety 기초 개념을 이해하고 `?` 연산자를 사용할 수 있다

<a id="toc"></a>
## 진행 순서
1. [변수란? — 상자 비유](#part1)
2. [기본 타입: var, int, double, String, bool](#part2)
3. [const vs final](#part3)
4. [문자열 보간법](#part4)
5. [Null Safety 기초](#part5)
6. [타입 추론](#part6)
7. [Flutter 연결 실습](#part7)
8. [정리 + 연습 문제](#part8)

---

<a id="part1"></a>
## 1️⃣ ⭐ **핵심** — 변수란? [↑](#toc)

### 상자 비유

변수(variable)는 **데이터를 저장하는 이름 붙은 상자**입니다.

```
┌─────────┐    ┌─────────────┐    ┌─────────┐
│  name   │    │     age     │    │  score  │
│"김민준" │    │     25      │    │  95.5   │
└─────────┘    └─────────────┘    └─────────┘
```

택배 상자를 생각해보세요. 상자에 이름표가 붙어있고, 그 안에 물건이 들어있습니다. 변수도 마찬가지입니다. `name`이라는 이름표 안에 `"김민준"` 이라는 값이 들어있는 거죠.

### Dart에서 변수 선언하기

```dart
void main() {
  // 변수 선언과 값 할당
  String name = '김민준';  // 이름표: name, 내용물: '김민준'
  int age = 25;            // 이름표: age, 내용물: 25
  
  print(name);  // 출력: 김민준
  print(age);   // 출력: 25
  
  // 값 변경 (상자 안의 내용물 교체)
  age = 26;
  print(age);   // 출력: 26
}
```

> DartPad([dartpad.dev](https://dartpad.dev))에서 직접 실행해보세요!

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — 기본 타입 [↑](#toc)

### 왜 타입이 필요한가?

상자의 종류를 생각해봅시다. 냉장 보관이 필요한 음식은 냉장 상자에, 깨지기 쉬운 물건은 뽁뽁이 상자에 넣듯이, 데이터 종류에 따라 맞는 타입을 사용합니다.

### int — 정수

소수점 없는 숫자입니다.

```dart
void main() {
  int score = 95;
  int year = 2026;
  int temperature = -5;  // 음수도 가능
  
  // 산술 연산
  int a = 10;
  int b = 3;
  print(a + b);   // 13  (더하기)
  print(a - b);   // 7   (빼기)
  print(a * b);   // 30  (곱하기)
  print(a ~/ b);  // 3   (정수 나누기)
  print(a % b);   // 1   (나머지)
}
```

### double — 실수 (소수점 있는 숫자)

```dart
void main() {
  double height = 175.5;
  double weight = 68.0;
  double pi = 3.14159;
  
  // int와 double 연산
  double bmi = weight / (height / 100 * (height / 100));
  print(bmi);  // 약 22.1 출력
  
  // int를 double로
  int x = 5;
  double y = x.toDouble();  // 5.0
  
  // double을 int로 (소수점 버림)
  double d = 7.9;
  int i = d.toInt();  // 7 (반올림 아닌 버림!)
}
```

### String — 문자열

문자(글자)의 모음입니다.

```dart
void main() {
  String name = '김민준';      // 작은따옴표
  String city = "서울";         // 큰따옴표도 가능
  String greeting = '안녕하세요!';
  
  // 문자열 길이
  print(name.length);  // 3
  
  // 대문자/소문자 변환
  String eng = 'hello';
  print(eng.toUpperCase());  // HELLO
  print(eng.toLowerCase());  // hello
  
  // 문자열 연결
  String fullGreeting = greeting + ' ' + name;
  print(fullGreeting);  // 안녕하세요! 김민준
  
  // 포함 여부 확인
  print(name.contains('민'));  // true
}
```

### bool — 참/거짓

`true` 또는 `false` 두 가지 값만 가집니다.

```dart
void main() {
  bool isLoggedIn = true;
  bool hasError = false;
  bool isAdult = true;
  
  // 비교 연산의 결과는 bool
  int age = 20;
  bool canVote = age >= 18;
  print(canVote);  // true
  
  print(10 > 5);   // true
  print(10 == 5);  // false (같음 비교는 == )
  print(10 != 5);  // true  (다름 비교는 !=)
}
```

### 타입 요약

| 타입 | 용도 | 예시 |
|------|------|------|
| `int` | 정수 | 나이, 점수, 수량 |
| `double` | 소수 | 키, 몸무게, 금액 |
| `String` | 문자열 | 이름, 주소, 메시지 |
| `bool` | 참/거짓 | 로그인 여부, 에러 여부 |

---

<a id="part3"></a>
## 3️⃣ ⭐ **핵심** — const vs final [↑](#toc)

### 일반 변수의 문제

```dart
void main() {
  int maxScore = 100;
  maxScore = 200;  // 실수로 바꿔버림! 버그 발생 가능
}
```

게임에서 "최고 점수는 100점"이라고 규칙을 정했는데, 나중에 실수로 200으로 바꿔버리면 큰일납니다. 이런 상황을 방지하기 위해 `const`와 `final`이 있습니다.

### const — 절대로 안 바뀌는 값 (컴파일 시 결정)

```dart
void main() {
  const int maxScore = 100;
  const double pi = 3.14159;
  const String appName = '나의 앱';
  
  // maxScore = 200;  // ❌ 오류! const는 변경 불가
  
  print(maxScore);  // 100
  print(pi);        // 3.14159
}
```

**const는 언제?**: 앱이 실행되기 전부터 값을 알고 있고, 절대 바뀌지 않을 때

```dart
// Flutter에서의 const 사용 예
const Text('안녕하세요');  // 텍스트 내용이 절대 안 바뀜
const EdgeInsets.all(16.0);  // 여백 값이 고정됨
```

### final — 한 번만 정하는 값 (실행 중 결정)

```dart
void main() {
  final String userName = '김민준';
  final DateTime now = DateTime.now();  // 실행 시점에 결정!
  
  // userName = '이영희';  // ❌ 오류! final은 재할당 불가
  
  print(userName);  // 김민준
  print(now);       // 현재 시각 출력
}
```

**final은 언제?**: 값이 실행 중에 한 번 정해지면 이후 바뀌지 않을 때

### 세 가지 차이 정리

```dart
void main() {
  // 일반 변수 — 언제든 변경 가능
  int count = 0;
  count = 5;  // ✅ 가능

  // final — 한 번만 할당 가능, 실행 시 값 결정
  final int userId = getUserId();  // 함수 결과값도 OK
  // userId = 999;  // ❌ 불가

  // const — 컴파일 시 상수, 함수 결과값 사용 불가
  const int maxRetry = 3;  // ✅ 리터럴 값만 가능
  // const int t = DateTime.now().millisecond;  // ❌ 불가
}

int getUserId() => 42;
```

> **실용 팁**: 값이 안 바뀔 것 같으면 일단 `const`로 시작하세요. 오류가 나면 `final`로, 그래도 안 되면 일반 변수로 바꾸면 됩니다.

---

<a id="part4"></a>
## 4️⃣ ⭐ **핵심** — 문자열 보간법 [↑](#toc)

### 문자열 안에 변수 넣기

문자열 보간(String interpolation)은 문자열 안에 변수나 표현식을 직접 넣는 방법입니다.

```dart
void main() {
  String name = '김민준';
  int age = 25;
  
  // 방법 1: 연결 연산자 (+)  — 복잡하고 읽기 어려움
  String msg1 = '이름은 ' + name + '이고, 나이는 ' + age.toString() + '살입니다.';
  
  // 방법 2: 문자열 보간 ($)  — 깔끔하고 읽기 쉬움
  String msg2 = '이름은 $name이고, 나이는 $age살입니다.';
  
  print(msg1);  // 이름은 김민준이고, 나이는 25살입니다.
  print(msg2);  // 이름은 김민준이고, 나이는 25살입니다.
}
```

### 표현식 사용: ${...}

변수 하나가 아니라 계산식을 넣을 때는 `${}` 를 씁니다:

```dart
void main() {
  int a = 10;
  int b = 5;
  
  print('$a + $b = ${a + b}');           // 10 + 5 = 15
  print('$a * $b = ${a * b}');           // 10 * 5 = 50
  
  String name = '김민준';
  print('이름 길이: ${name.length}자');  // 이름 길이: 3자
  
  double score = 95.5;
  print('점수: ${score.toStringAsFixed(1)}점');  // 점수: 95.5점
}
```

### 여러 줄 문자열

```dart
void main() {
  String name = '김민준';
  
  // 여러 줄 문자열 (삼중 따옴표)
  String profile = '''
이름: $name
직업: Flutter 개발자
취미: 코딩, 독서
  ''';
  
  print(profile);
}
```

---

<a id="part5"></a>
## 5️⃣ ⭐ **핵심** — Null Safety 기초 [↑](#toc)

### null이란?

null은 "값이 없음"을 의미합니다.

> **비유**: 빈 택배 상자. 상자는 있는데 안에 아무것도 없는 상태.

많은 프로그래밍 언어에서 null 때문에 앱이 갑자기 꺼지는 오류가 발생합니다. Flutter/Dart는 이를 언어 차원에서 방지합니다.

### Null Safety: 물음표(?)의 역할

```dart
void main() {
  // null을 허용하지 않는 변수 (기본)
  String name = '김민준';
  // name = null;  // ❌ 컴파일 오류! null 불가

  // null을 허용하는 변수 (타입 뒤에 ? 붙임)
  String? nickname;  // null 허용, 초기값은 null
  print(nickname);   // null

  nickname = '민준이';
  print(nickname);   // 민준이
  
  nickname = null;   // ✅ ? 타입이므로 null 허용
  print(nickname);   // null
}
```

### null 체크하기

null인지 아닌지 확인 후 사용해야 합니다:

```dart
void main() {
  String? nickname = null;
  
  // 방법 1: if 문으로 null 체크
  if (nickname != null) {
    print('닉네임: $nickname');
  } else {
    print('닉네임이 없습니다');
  }
  
  // 방법 2: ?? 연산자 (null이면 기본값 사용)
  String displayName = nickname ?? '이름 없음';
  print(displayName);  // 이름 없음
  
  nickname = '민준이';
  displayName = nickname ?? '이름 없음';
  print(displayName);  // 민준이
}
```

### ?. 연산자 — null-safe 접근

```dart
void main() {
  String? name = null;
  
  // name이 null이면 오류 발생
  // print(name.length);  // ❌ 위험!
  
  // ?. 를 사용하면 null일 때 null 반환 (오류 없음)
  print(name?.length);  // null (오류 없이 안전하게)
  
  name = '김민준';
  print(name?.length);  // 3
}
```

### Null Safety 요약

| 문법 | 의미 | 예시 |
|------|------|------|
| `String name` | null 불허 | 항상 값이 있음 |
| `String? name` | null 허용 | 없을 수도 있음 |
| `a ?? b` | null이면 b 사용 | `nickname ?? '없음'` |
| `a?.method()` | null이면 null 반환 | `name?.length` |

---

<a id="part6"></a>
## 6️⃣ 📖 **더 알아보기** — 타입 추론 [↑](#toc)

### var 키워드

타입을 명시하지 않고 `var`를 쓰면 Dart가 자동으로 타입을 추론합니다.

```dart
void main() {
  var name = '김민준';    // Dart가 String으로 추론
  var age = 25;           // Dart가 int로 추론
  var height = 175.5;     // Dart가 double로 추론
  var isAdult = true;     // Dart가 bool로 추론
  
  // 한 번 정해진 타입은 바꿀 수 없음
  // name = 100;  // ❌ String에 int 할당 불가
}
```

### var vs 명시적 타입 — 언제 무엇을?

| 상황 | 권장 |
|------|------|
| 지역 변수, 타입이 명확한 경우 | `var` 사용 |
| 함수 매개변수, 반환값 | 명시적 타입 |
| 클래스 속성 | 명시적 타입 |
| 코드 읽는 사람이 타입을 알아야 할 때 | 명시적 타입 |

```dart
// Good: 타입이 명확 → var OK
var name = '김민준';
var items = [1, 2, 3];

// Good: 함수 시그니처는 명시적 타입
String formatName(String firstName, String lastName) {
  return '$firstName $lastName';
}
```

---

<a id="part7"></a>
## 7️⃣ ⭐ **핵심** — Flutter 연결 실습 [↑](#toc)

### 앱 제목을 변수로 변경하기

`lib/main.dart`를 열고 변수를 활용하도록 수정합니다.

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // 변수를 사용해서 앱 정보 관리
    const String appTitle = 'AI-Native Flutter';
    const String authorName = '김민준';
    
    return MaterialApp(
      title: appTitle,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text(appTitle),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                '안녕하세요!',
                style: Theme.of(context).textTheme.headlineMedium,
              ),
              Text('개발자: $authorName'),
              const Text('Flutter로 만든 첫 앱입니다.'),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 실습 과제

다음 변수들을 추가하고 화면에 표시해보세요:

```dart
const String appVersion = '1.0.0';
const int buildYear = 2026;
const bool isDarkMode = false;
```

---

<a id="part8"></a>
## 8️⃣ 정리 + 연습 문제 [↑](#toc)

### 핵심 정리

| 개념 | 문법 | 예시 |
|------|------|------|
| 정수 | `int` | `int age = 25;` |
| 실수 | `double` | `double score = 95.5;` |
| 문자열 | `String` | `String name = '민준';` |
| 참/거짓 | `bool` | `bool isOn = true;` |
| 상수 | `const` | `const pi = 3.14;` |
| 한번-할당 | `final` | `final now = DateTime.now();` |
| 자동 타입 | `var` | `var x = 42;` |
| null 허용 | `타입?` | `String? nickname;` |
| null 기본값 | `??` | `name ?? '없음'` |
| 문자열 보간 | `$변수` | `'이름: $name'` |

### 연습 문제

DartPad([dartpad.dev](https://dartpad.dev))에서 풀어보세요.

**문제 1**: 다음 변수를 선언하고 출력하세요.
- 자신의 이름 (String)
- 나이 (int)
- 키 (double)
- 학생 여부 (bool)

```dart
void main() {
  // 여기에 코드를 작성하세요
  
}
```

**문제 2**: 다음 코드의 출력 결과를 예상해보세요.

```dart
void main() {
  String? city = null;
  String displayCity = city ?? '서울';
  print(displayCity);
  
  city = '부산';
  displayCity = city ?? '서울';
  print(displayCity);
}
```

**문제 3**: 아래 코드에서 오류가 있는 줄을 찾고 이유를 설명하세요.

```dart
void main() {
  const int maxScore = 100;
  maxScore = 200;  // (A)
  
  final String name = '김민준';
  name = '이영희';  // (B)
  
  int count = 0;
  count = 5;       // (C)
}
```

**정답 힌트**: A와 B는 오류입니다. C는 정상입니다.

---

---

→ **다음 내용으로 넘어갑시다**: [03. Dart — 조건문과 반복문](/ai-native-flutter/dart-control-flow)
