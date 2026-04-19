---
title: "04. Dart — 함수"
layout: default
parent: AI-Native Flutter
nav_order: 6
permalink: /ai-native-flutter/dart-functions
---

# 4장. Dart — 함수
{: .no_toc }

> **Phase 1** · 예상 시간: 90분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 설명 모드만**
> 함수 개념이 헷갈릴 때 AI에게 설명을 요청할 수 있습니다. 하지만 실습 문제의 코드는 직접 작성하세요.

## 학습 목표
- 함수의 개념과 왜 필요한지 설명할 수 있다
- 매개변수(parameter)와 반환값(return value)을 가진 함수를 작성할 수 있다
- Named Parameters와 Optional Parameters를 사용할 수 있다
- 화살표 함수(`=>`)를 적절히 사용할 수 있다

<a id="toc"></a>
## 진행 순서
1. [함수란? — 레시피/자판기 비유](#part1)
2. [함수 선언과 호출](#part2)
3. [매개변수와 반환값](#part3)
4. [Named Parameters](#part4)
5. [Optional Parameters + 기본값](#part5)
6. [화살표 함수 (=>)](#part6)
7. [함수를 변수에 저장하기](#part7)
8. [Flutter 연결 실습: onPressed 콜백](#part8)
9. [정리](#part9)

---

<a id="part1"></a>
## 1️⃣ ⭐ **핵심** — 함수란? [↑](#toc)

### 레시피 비유

함수(Function)는 **이름 붙은 코드 묶음**입니다.

레시피를 생각해보세요:
- **레시피 이름**: "김치찌개 만들기"
- **재료(입력)**: 김치, 돼지고기, 두부
- **과정**: 1. 재료 씻기, 2. 냄비에 넣기, 3. 끓이기 ...
- **결과(출력)**: 완성된 김치찌개

함수도 마찬가지입니다:
- **함수 이름**: `makeKimchiStew`
- **매개변수(입력)**: kimchi, pork, tofu
- **함수 본문**: 처리 과정
- **반환값(출력)**: 완성된 음식

### 왜 함수가 필요한가?

**함수 없이** 같은 코드를 3번 쓰는 경우:
```dart
void main() {
  // 사용자 1 인사
  String name1 = '김민준';
  int age1 = 25;
  print('안녕하세요! 저는 $name1이고, $age1살입니다.');
  
  // 사용자 2 인사
  String name2 = '이영희';
  int age2 = 23;
  print('안녕하세요! 저는 $name2이고, $age2살입니다.');
  
  // 사용자 3 인사
  String name3 = '박지수';
  int age3 = 27;
  print('안녕하세요! 저는 $name3이고, $age3살입니다.');
}
```

**함수를 쓰면**:
```dart
void greet(String name, int age) {
  print('안녕하세요! 저는 $name이고, $age살입니다.');
}

void main() {
  greet('김민준', 25);
  greet('이영희', 23);
  greet('박지수', 27);
}
```

훨씬 깔끔합니다. 인사 형식을 바꾸고 싶다면? 함수 안만 바꾸면 됩니다.

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — 함수 선언과 호출 [↑](#toc)

### 함수 문법

```
반환타입 함수이름(매개변수) {
  // 함수 본문
  return 반환값;
}
```

### 반환값이 없는 함수 (void)

```dart
// void = 아무것도 반환하지 않음
void sayHello() {
  print('Hello, Flutter!');
}

void main() {
  sayHello();  // 함수 호출
  sayHello();  // 여러 번 호출 가능
}
```

### 반환값이 있는 함수

```dart
// int를 반환하는 함수
int add(int a, int b) {
  return a + b;
}

// String을 반환하는 함수
String getFullName(String first, String last) {
  return '$first $last';
}

void main() {
  int result = add(3, 5);
  print(result);  // 8

  String name = getFullName('김', '민준');
  print(name);  // 김 민준
}
```

---

<a id="part3"></a>
## 3️⃣ ⭐ **핵심** — 매개변수와 반환값 [↑](#toc)

### 위치 매개변수 (Positional Parameters)

순서대로 전달하는 매개변수입니다.

```dart
double calculateBMI(double weight, double heightCm) {
  double heightM = heightCm / 100;
  return weight / (heightM * heightM);
}

void main() {
  double bmi = calculateBMI(68.0, 175.0);
  print('BMI: ${bmi.toStringAsFixed(1)}');  // BMI: 22.2
  
  // 순서가 중요! 바꾸면 잘못된 결과
  // calculateBMI(175.0, 68.0)  // ← 잘못된 순서
}
```

### 여러 값 반환하기 (Record 타입 — Dart 3+)

```dart
// 여러 값을 반환하려면 Record 사용
(String, int) getPersonInfo() {
  return ('김민준', 25);
}

void main() {
  var (name, age) = getPersonInfo();
  print('이름: $name, 나이: $age');
}
```

### 함수 안에서 함수 호출하기

```dart
double celsiusToFahrenheit(double celsius) {
  return celsius * 9 / 5 + 32;
}

void printTemperature(double celsius) {
  double fahrenheit = celsiusToFahrenheit(celsius);  // 함수 안에서 다른 함수 호출
  print('${celsius}°C = ${fahrenheit.toStringAsFixed(1)}°F');
}

void main() {
  printTemperature(0);    // 0.0°C = 32.0°F
  printTemperature(100);  // 100.0°C = 212.0°F
  printTemperature(37);   // 37.0°C = 98.6°F
}
```

---

<a id="part4"></a>
## 4️⃣ ⭐ **핵심** — Named Parameters [↑](#toc)

### 이름으로 전달하는 매개변수

위치 매개변수는 순서를 틀리면 버그가 생깁니다. **Named Parameters**는 이름으로 전달하므로 순서를 틀릴 걱정이 없습니다.

```dart
// Named Parameters: 중괄호 {} 안에 선언
void createProfile({
  required String name,
  required int age,
  required String city,
}) {
  print('이름: $name, 나이: $age, 도시: $city');
}

void main() {
  // 이름으로 전달 — 순서 무관!
  createProfile(
    name: '김민준',
    age: 25,
    city: '서울',
  );

  // 순서를 바꿔도 됩니다
  createProfile(
    city: '부산',
    name: '이영희',
    age: 23,
  );
}
```

### required 키워드

`required`를 붙이면 반드시 전달해야 하는 매개변수입니다:

```dart
void sendMessage({
  required String to,
  required String content,
  String subject = '(제목 없음)',  // 기본값 있음
}) {
  print('수신: $to');
  print('제목: $subject');
  print('내용: $content');
}

void main() {
  sendMessage(
    to: 'alice@example.com',
    content: '안녕하세요!',
    // subject는 생략 가능 (기본값 사용)
  );
}
```

### Flutter에서 Named Parameters

Flutter의 모든 위젯이 Named Parameters를 사용합니다!

```dart
// Flutter 위젯의 Named Parameters 예시
Text(
  '안녕하세요',
  style: TextStyle(fontSize: 24),
  textAlign: TextAlign.center,
)

ElevatedButton(
  onPressed: () {},
  child: const Text('클릭'),
)
```

---

<a id="part5"></a>
## 5️⃣ ⭐ **핵심** — Optional Parameters + 기본값 [↑](#toc)

### 선택적 매개변수

전달해도 되고 안 해도 되는 매개변수입니다.

```dart
// Named Parameter에 기본값 설정
void greet({
  required String name,
  String language = '한국어',  // 기본값
  bool formal = false,          // 기본값
}) {
  if (language == '한국어') {
    if (formal) {
      print('안녕하십니까, $name님.');
    } else {
      print('안녕하세요, $name!');
    }
  } else {
    print('Hello, $name!');
  }
}

void main() {
  greet(name: '민준');                       // 기본값 사용
  greet(name: '민준', formal: true);         // formal만 변경
  greet(name: 'Alice', language: 'English'); // language만 변경
}
```

### 위치 선택적 매개변수 (대괄호 [])

```dart
// [ ] 안에 있는 매개변수는 선택적
String buildAddress(String city, [String? district, String? street]) {
  if (district != null && street != null) {
    return '$city $district $street';
  } else if (district != null) {
    return '$city $district';
  }
  return city;
}

void main() {
  print(buildAddress('서울'));             // 서울
  print(buildAddress('서울', '강남구'));  // 서울 강남구
  print(buildAddress('서울', '강남구', '테헤란로'));  // 서울 강남구 테헤란로
}
```

---

<a id="part6"></a>
## 6️⃣ ⭐ **핵심** — 화살표 함수 (=>) [↑](#toc)

### 한 줄 함수를 더 짧게

함수 본문이 `return 표현식;` 단 하나일 때, `=>` 기호로 더 짧게 쓸 수 있습니다.

```dart
// 일반 함수
int square(int n) {
  return n * n;
}

// 화살표 함수 — 완전히 동일한 동작
int squareArrow(int n) => n * n;

// 또 다른 예
String greet(String name) => '안녕하세요, $name!';

bool isEven(int n) => n % 2 == 0;

void main() {
  print(square(5));       // 25
  print(squareArrow(5));  // 25
  print(greet('민준'));  // 안녕하세요, 민준!
  print(isEven(4));       // true
  print(isEven(7));       // false
}
```

### Flutter에서 화살표 함수

```dart
ElevatedButton(
  // 화살표 함수로 간결하게
  onPressed: () => print('버튼 클릭!'),
  child: const Text('클릭'),
)
```

---

<a id="part7"></a>
## 7️⃣ 📖 **더 알아보기** — 함수를 변수에 저장하기 [↑](#toc)

### 함수는 값이다

Dart에서 함수는 변수에 저장하고, 다른 함수에 전달할 수 있습니다. 이를 **일급 함수(First-class function)**라고 합니다.

```dart
// 함수 타입: Function
void sayHi() {
  print('안녕!');
}

void main() {
  // 함수를 변수에 저장
  var myFunc = sayHi;
  myFunc();  // 안녕!

  // 함수를 다른 함수의 매개변수로 전달
  void execute(Function f) {
    print('실행 전...');
    f();
    print('실행 후...');
  }

  execute(sayHi);
  // 출력:
  // 실행 전...
  // 안녕!
  // 실행 후...
}
```

### 익명 함수 (Anonymous Function)

이름 없이 즉석에서 만드는 함수입니다:

```dart
void main() {
  List<int> numbers = [1, 2, 3, 4, 5];

  // 익명 함수 전달
  numbers.forEach((number) {
    print('숫자: $number');
  });

  // 화살표로 더 짧게
  numbers.forEach((n) => print('값: $n'));
}
```

---

<a id="part8"></a>
## 8️⃣ ⭐ **핵심** — Flutter 연결 실습: onPressed 콜백 [↑](#toc)

### 콜백 함수란?

**콜백(Callback)**은 나중에 호출될 함수입니다. "이 일이 일어나면 이 함수를 불러줘"라고 등록해두는 개념입니다.

Flutter의 버튼 `onPressed`가 대표적인 콜백입니다.

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const CalculatorApp());
}

class CalculatorApp extends StatefulWidget {
  const CalculatorApp({super.key});

  @override
  State<CalculatorApp> createState() => _CalculatorAppState();
}

class _CalculatorAppState extends State<CalculatorApp> {
  int _result = 0;

  // 함수로 버튼 동작 분리
  void _add(int value) {
    setState(() {
      _result += value;
    });
  }

  void _reset() {
    setState(() {
      _result = 0;
    });
  }

  // 화살표 함수로 결과 문자열 만들기
  String get _displayText => '결과: $_result';

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('간단 계산기')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                _displayText,
                style: const TextStyle(fontSize: 32),
              ),
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ElevatedButton(
                    onPressed: () => _add(1),   // 화살표 함수 콜백
                    child: const Text('+1'),
                  ),
                  const SizedBox(width: 10),
                  ElevatedButton(
                    onPressed: () => _add(10),  // 화살표 함수 콜백
                    child: const Text('+10'),
                  ),
                  const SizedBox(width: 10),
                  ElevatedButton(
                    onPressed: _reset,          // 함수 참조 전달
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red,
                    ),
                    child: const Text('초기화'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

---

<a id="part9"></a>
## 9️⃣ 정리 [↑](#toc)

### 핵심 정리

| 개념 | 문법 | 예시 |
|------|------|------|
| 함수 선언 | `반환타입 이름(매개변수) {...}` | `int add(int a, int b)` |
| 반환 없음 | `void` | `void printName()` |
| Named Parameter | `{required 타입 이름}` | `{required String name}` |
| 기본값 | `= 기본값` | `String city = '서울'` |
| 화살표 함수 | `=> 표현식` | `int sq(int n) => n*n` |
| 익명 함수 | `(매개변수) { ... }` | `(n) => n * 2` |

### 연습 문제

**문제 1**: 두 정수를 받아 더 큰 값을 반환하는 `max` 함수를 작성하세요.
```dart
int max(int a, int b) {
  // 여기에 코드 작성
}
```

**문제 2**: 이름(name), 직업(job), 취미(hobby, 선택)를 받아 자기소개 문자열을 반환하는 함수를 Named Parameters로 작성하세요.

**문제 3**: 다음 함수를 화살표 함수로 변환하세요.
```dart
bool isPositive(int number) {
  return number > 0;
}
```

**문제 4 (도전)**: 숫자 리스트를 받아 평균을 반환하는 `average` 함수를 작성하세요.
```dart
double average(List<int> numbers) {
  // 여기에 코드 작성
}
```

---
