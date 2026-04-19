---
title: "03. Dart — 조건문과 반복문"
layout: default
parent: AI-Native Flutter
nav_order: 5
permalink: /ai-native-flutter/dart-control-flow
---

# 3장. Dart — 조건문과 반복문
{: .no_toc }

> **Phase 1** · 예상 시간: 90분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 설명 모드만**
> 코드 오류 원인이나 개념 설명은 AI에게 물어봐도 됩니다. 문제 풀이 코드는 반드시 직접 작성하세요.

## 학습 목표
- if/else로 조건에 따라 다른 동작을 실행할 수 있다
- switch 표현식으로 다중 분기를 처리할 수 있다
- for, while, for-in 반복문을 적절히 선택하여 사용할 수 있다
- Flutter 위젯에서 조건부 렌더링과 반복 위젯 생성을 할 수 있다

<a id="toc"></a>
## 진행 순서
1. [if/else — 교통 신호등 비유](#part1)
2. [else if 체이닝](#part2)
3. [논리 연산자](#part3)
4. [switch 표현식](#part4)
5. [for 반복문 — 우편배달부 비유](#part5)
6. [while 반복문](#part6)
7. [for-in 반복문](#part7)
8. [Flutter 연결 실습](#part8)
9. [정리 + 연습 문제](#part9)

---

<a id="part1"></a>
## 1️⃣ ⭐ **핵심** — if/else [↑](#toc)

### 교통 신호등 비유

교통 신호등은 조건에 따라 다른 행동을 지시합니다:
- 초록불 → 가세요
- 빨간불 → 멈추세요

프로그램도 조건에 따라 다른 코드를 실행합니다. 이것이 **조건문(if/else)**입니다.

### 기본 if/else 문법

```dart
void main() {
  int light = 1;  // 1: 초록, 2: 노랑, 3: 빨강

  if (light == 1) {
    print('가세요!');
  } else {
    print('멈추세요!');
  }
}
```

### 비교 연산자

| 연산자 | 의미 | 예시 |
|--------|------|------|
| `==` | 같다 | `a == b` |
| `!=` | 다르다 | `a != b` |
| `>` | 크다 | `a > b` |
| `<` | 작다 | `a < b` |
| `>=` | 크거나 같다 | `a >= b` |
| `<=` | 작거나 같다 | `a <= b` |

### 실용 예제

```dart
void main() {
  int age = 17;

  if (age >= 18) {
    print('성인입니다. 영화 관람 가능합니다.');
  } else {
    print('미성년자입니다. 보호자 동반이 필요합니다.');
  }

  // 점수 합격 여부
  int score = 72;
  if (score >= 60) {
    print('합격!');
  } else {
    print('불합격. 재시험을 봐야 합니다.');
  }
}
```

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — else if 체이닝 [↑](#toc)

### 세 가지 이상의 경우 처리

신호등이 3가지 색인 것처럼, 조건이 여러 개일 때는 `else if`를 연결합니다.

```dart
void main() {
  int score = 85;

  String grade;

  if (score >= 90) {
    grade = 'A';
  } else if (score >= 80) {
    grade = 'B';
  } else if (score >= 70) {
    grade = 'C';
  } else if (score >= 60) {
    grade = 'D';
  } else {
    grade = 'F';
  }

  print('점수: $score, 등급: $grade');
  // 출력: 점수: 85, 등급: B
}
```

### 삼항 연산자 (간단한 조건)

if/else가 한 줄로 줄어드는 형태입니다:

```dart
void main() {
  int age = 20;

  // 일반 if/else
  String status;
  if (age >= 18) {
    status = '성인';
  } else {
    status = '미성년자';
  }

  // 삼항 연산자 — 조건 ? 참일때 : 거짓일때
  String status2 = age >= 18 ? '성인' : '미성년자';

  print(status);   // 성인
  print(status2);  // 성인
}
```

---

<a id="part3"></a>
## 3️⃣ ⭐ **핵심** — 논리 연산자 [↑](#toc)

### 조건을 조합하기

여러 조건을 AND(그리고), OR(또는), NOT(아니다)으로 조합할 수 있습니다.

```dart
void main() {
  int age = 22;
  bool hasMembership = true;

  // && (AND) — 둘 다 참이어야 함
  if (age >= 18 && hasMembership) {
    print('회원 혜택 이용 가능');
  }

  // || (OR) — 하나라도 참이면 됨
  bool isWeekend = false;
  bool isHoliday = true;

  if (isWeekend || isHoliday) {
    print('오늘은 쉬는 날!');
  }

  // ! (NOT) — 참을 거짓으로, 거짓을 참으로
  bool isRaining = false;
  if (!isRaining) {
    print('우산 없이 나가도 됩니다');
  }
}
```

### 복합 조건 예제

```dart
void main() {
  int score = 75;
  bool isPresent = true;
  int absenceCount = 2;

  // 출석 2회 미만이고 점수 70 이상이면 합격
  if (absenceCount < 3 && score >= 70 && isPresent) {
    print('최종 합격!');
  } else {
    print('조건 미충족');
  }
}
```

---

<a id="part4"></a>
## 4️⃣ 📖 **더 알아보기** — switch 표현식 [↑](#toc)

### 여러 값을 깔끔하게 처리

하나의 변수가 여러 값 중 하나인 경우, if/else if 대신 switch를 쓰면 더 깔끔합니다.

```dart
void main() {
  String day = '월요일';

  // if/else if 방식 — 반복이 많음
  if (day == '토요일' || day == '일요일') {
    print('주말');
  } else if (day == '월요일') {
    print('한 주의 시작');
  } else {
    print('평일');
  }

  // switch 방식 — 더 깔끔
  switch (day) {
    case '월요일':
      print('한 주의 시작');
    case '토요일':
    case '일요일':
      print('주말');
    default:
      print('평일');
  }
}
```

### Dart 3의 switch 표현식 (값 반환)

```dart
void main() {
  String weather = '맑음';

  // switch 표현식으로 값 반환
  String recommendation = switch (weather) {
    '맑음' => '자전거 타기 좋은 날!',
    '흐림' => '산책은 가능합니다',
    '비' => '우산 챙기세요',
    '눈' => '따뜻하게 입으세요',
    _ => '날씨 정보 없음',  // default
  };

  print(recommendation);  // 자전거 타기 좋은 날!
}
```

---

<a id="part5"></a>
## 5️⃣ ⭐ **핵심** — for 반복문 [↑](#toc)

### 우편배달부 비유

우편배달부가 10개의 집에 편지를 배달한다고 생각해봅시다. 집마다 방문해서 편지를 넣는 동작을 10번 반복합니다. 이처럼 **같은 작업을 정해진 횟수만큼 반복**하는 것이 for 반복문입니다.

### 기본 for 문법

```dart
void main() {
  // for (초기화; 조건; 증감) { 반복할 코드 }
  for (int i = 0; i < 5; i++) {
    print('$i번째 반복');
  }
  // 출력:
  // 0번째 반복
  // 1번째 반복
  // 2번째 반복
  // 3번째 반복
  // 4번째 반복
}
```

`i++`는 `i = i + 1`의 짧은 표현입니다.

### 실용 예제

```dart
void main() {
  // 1부터 10까지 합계
  int sum = 0;
  for (int i = 1; i <= 10; i++) {
    sum += i;  // sum = sum + i
  }
  print('1~10 합계: $sum');  // 55

  // 구구단 3단
  print('--- 3단 ---');
  for (int i = 1; i <= 9; i++) {
    print('3 × $i = ${3 * i}');
  }
}
```

### 역방향 반복

```dart
void main() {
  // 10에서 1까지 카운트다운
  for (int i = 10; i >= 1; i--) {
    print('$i...');
  }
  print('발사!');
}
```

---

<a id="part6"></a>
## 6️⃣ ⭐ **핵심** — while 반복문 [↑](#toc)

### 조건이 만족하는 동안 반복

while은 "조건이 참인 동안" 계속 반복합니다. 몇 번 반복할지 모를 때 유용합니다.

> **비유**: 버스 기다리기. 버스가 올 때까지(조건이 거짓이 될 때까지) 계속 기다립니다.

```dart
void main() {
  int count = 0;

  while (count < 5) {
    print('현재 카운트: $count');
    count++;  // 이 줄이 없으면 무한 반복!
  }
  print('완료!');
}
```

### do-while — 최소 한 번은 실행

```dart
void main() {
  int number = 0;

  // do-while: 조건 체크 전에 먼저 한 번 실행
  do {
    print('number: $number');
    number++;
  } while (number < 3);

  // 출력:
  // number: 0
  // number: 1
  // number: 2
}
```

### break와 continue

```dart
void main() {
  // break: 반복문 완전 종료
  for (int i = 0; i < 10; i++) {
    if (i == 5) break;  // i가 5가 되면 반복 종료
    print(i);
  }
  // 출력: 0 1 2 3 4

  print('---');

  // continue: 현재 반복만 건너뜀
  for (int i = 0; i < 5; i++) {
    if (i == 2) continue;  // i가 2일 때는 건너뜀
    print(i);
  }
  // 출력: 0 1 3 4
}
```

---

<a id="part7"></a>
## 7️⃣ ⭐ **핵심** — for-in 반복문 [↑](#toc)

### 컬렉션 순회

리스트(목록)의 각 항목을 순서대로 처리할 때 사용합니다.

```dart
void main() {
  List<String> fruits = ['사과', '바나나', '딸기', '포도'];

  // for-in: 리스트의 각 항목에 대해 반복
  for (String fruit in fruits) {
    print('과일: $fruit');
  }
  // 출력:
  // 과일: 사과
  // 과일: 바나나
  // 과일: 딸기
  // 과일: 포도
}
```

### for vs while vs for-in 선택 기준

| 상황 | 선택 |
|------|------|
| 몇 번 반복할지 정해져 있음 | `for` |
| 조건이 충족되는 동안 반복 | `while` |
| 리스트/컬렉션의 모든 항목 처리 | `for-in` |

---

<a id="part8"></a>
## 8️⃣ ⭐ **핵심** — Flutter 연결 실습 [↑](#toc)

### 실습 1: 점수에 따라 등급 표시

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const GradeApp());
}

class GradeApp extends StatelessWidget {
  const GradeApp({super.key});

  String getGrade(int score) {
    if (score >= 90) return 'A';
    if (score >= 80) return 'B';
    if (score >= 70) return 'C';
    if (score >= 60) return 'D';
    return 'F';
  }

  Color getGradeColor(String grade) {
    switch (grade) {
      case 'A':
        return Colors.blue;
      case 'B':
        return Colors.green;
      case 'C':
        return Colors.orange;
      case 'D':
        return Colors.amber;
      default:
        return Colors.red;
    }
  }

  @override
  Widget build(BuildContext context) {
    const int myScore = 85;
    final String grade = getGrade(myScore);
    final Color gradeColor = getGradeColor(grade);

    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('성적 확인')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('내 점수', style: TextStyle(fontSize: 20)),
              Text(
                '$myScore점',
                style: const TextStyle(fontSize: 48, fontWeight: FontWeight.bold),
              ),
              Text(
                '등급: $grade',
                style: TextStyle(
                  fontSize: 32,
                  color: gradeColor,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 실습 2: 반복문으로 여러 항목 표시

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MenuApp());
}

class MenuApp extends StatelessWidget {
  const MenuApp({super.key});

  @override
  Widget build(BuildContext context) {
    List<String> menuItems = ['아메리카노', '카페라떼', '카푸치노', '에스프레소'];

    // 반복문으로 Text 위젯 리스트 만들기
    List<Widget> menuWidgets = [];
    for (String item in menuItems) {
      menuWidgets.add(
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Text(
            item,
            style: const TextStyle(fontSize: 18),
          ),
        ),
      );
    }

    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('카페 메뉴')),
        body: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: menuWidgets,
        ),
      ),
    );
  }
}
```

---

<a id="part9"></a>
## 9️⃣ 정리 + 연습 문제 [↑](#toc)

### 핵심 정리

| 구문 | 용도 | 예시 |
|------|------|------|
| `if (조건)` | 단일 조건 | `if (age >= 18)` |
| `if/else` | 두 가지 경우 | `if (...) ... else ...` |
| `else if` | 여러 경우 | `else if (score >= 80)` |
| `조건 ? A : B` | 간단한 분기 | `age >= 18 ? '성인' : '미성년자'` |
| `switch` | 다중 값 분기 | `switch (day) { case '월': ... }` |
| `for` | 횟수 반복 | `for (int i=0; i<10; i++)` |
| `while` | 조건 반복 | `while (count < 5)` |
| `for-in` | 컬렉션 순회 | `for (String s in list)` |
| `break` | 반복 종료 | 반복문 안에서 사용 |
| `continue` | 현재 회차 건너뜀 | 반복문 안에서 사용 |

### 연습 문제

**문제 1**: 1에서 100까지 중 짝수만 출력하는 코드를 작성하세요.  
힌트: `%` 연산자 사용 (짝수 조건: `i % 2 == 0`)

**문제 2**: 아래 리스트에서 80점 이상인 점수만 출력하세요.

```dart
List<int> scores = [72, 85, 91, 60, 78, 95, 55, 88];
```

**문제 3**: 1에서 100까지 더하면 얼마인지 while 반복문으로 구하세요.  
힌트: 정답은 5050

**문제 4 (도전)**: 구구단 전체(2~9단)를 출력하는 코드를 작성하세요.  
힌트: 반복문 안에 반복문(중첩 반복문) 사용

---
