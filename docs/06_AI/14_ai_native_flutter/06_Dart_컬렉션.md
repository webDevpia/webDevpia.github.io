---
title: "05. Dart — 컬렉션"
layout: default
parent: AI-Native Flutter
nav_order: 7
permalink: /ai-native-flutter/dart-collections
---

# 5장. Dart — 컬렉션
{: .no_toc }

> **Phase 1** · 예상 시간: 90분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 설명 모드만**
> List나 Map 메서드의 동작이 궁금하면 AI에게 설명을 요청하세요. 코드는 직접 작성합니다.

## 학습 목표
- List를 선언하고 add, remove 등 기본 메서드를 사용할 수 있다
- Map에 키-값을 저장하고 조회할 수 있다
- `map()`, `where()` 메서드로 리스트를 변환/필터링할 수 있다
- Flutter에서 리스트 데이터로 위젯을 동적으로 생성할 수 있다

<a id="toc"></a>
## 진행 순서
1. [List — 장바구니 비유](#part1)
2. [List 조작 메서드](#part2)
3. [Map — 전화번호부 비유](#part3)
4. [Map 조작](#part4)
5. [반복과 변환 — map(), where()](#part5)
6. [Spread 연산자 (...)](#part6)
7. [Flutter 연결 실습](#part7)
8. [정리](#part8)

---

<a id="part1"></a>
## 1️⃣ ⭐ **핵심** — List (장바구니 비유) [↑](#toc)

### List란?

List는 **순서가 있는 데이터의 모음**입니다.

> **비유**: 장바구니를 생각해보세요. 사과, 우유, 빵을 순서대로 담아두고, 몇 번째 칸에 무엇이 있는지 알 수 있습니다.

```
장바구니 (List<String>):
┌──────┬──────┬──────┐
│  [0] │  [1] │  [2] │
│ 사과 │  우유 │  빵  │
└──────┴──────┴──────┘
  ↑ 0번  ↑ 1번  ↑ 2번
  (인덱스는 0부터 시작!)
```

### List 선언하기

```dart
void main() {
  // 방법 1: 타입 명시
  List<String> fruits = ['사과', '바나나', '딸기'];
  
  // 방법 2: var 사용 (자동 추론)
  var numbers = [1, 2, 3, 4, 5];
  
  // 방법 3: 빈 리스트 만들기
  List<String> emptyList = [];
  
  // 요소 접근 — 인덱스(0부터 시작)
  print(fruits[0]);  // 사과
  print(fruits[1]);  // 바나나
  print(fruits[2]);  // 딸기
  
  // 마지막 요소
  print(fruits.last);   // 딸기
  print(fruits.first);  // 사과
  
  // 개수
  print(fruits.length);  // 3
}
```

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — List 조작 메서드 [↑](#toc)

### 추가/삭제

```dart
void main() {
  List<String> cart = ['사과', '우유'];
  
  // 추가
  cart.add('빵');          // 맨 뒤에 추가
  cart.insert(0, '계란'); // 특정 위치에 추가
  print(cart);  // [계란, 사과, 우유, 빵]
  
  // 삭제
  cart.remove('우유');     // 값으로 삭제
  cart.removeAt(0);        // 인덱스로 삭제
  print(cart);  // [사과, 빵]
  
  // 전체 삭제
  cart.clear();
  print(cart);  // []
}
```

### 검색/확인

```dart
void main() {
  List<String> fruits = ['사과', '바나나', '딸기', '포도'];
  
  // 포함 여부
  print(fruits.contains('바나나'));  // true
  print(fruits.contains('수박'));    // false
  
  // 위치 찾기
  print(fruits.indexOf('딸기'));     // 2
  print(fruits.indexOf('수박'));     // -1 (없으면 -1)
  
  // 정렬
  List<int> nums = [3, 1, 4, 1, 5, 9, 2, 6];
  nums.sort();
  print(nums);  // [1, 1, 2, 3, 4, 5, 6, 9]
  
  // 역순
  nums.sort((a, b) => b.compareTo(a));
  print(nums);  // [9, 6, 5, 4, 3, 2, 1, 1]
}
```

### 변환

```dart
void main() {
  List<int> numbers = [1, 2, 3, 4, 5];
  
  // join: 리스트를 문자열로
  print(numbers.join(', '));    // 1, 2, 3, 4, 5
  print(numbers.join(' - '));  // 1 - 2 - 3 - 4 - 5
  
  // reversed: 역순 리스트
  var reversed = numbers.reversed.toList();
  print(reversed);  // [5, 4, 3, 2, 1]
  
  // sublist: 일부만 추출
  var sub = numbers.sublist(1, 3);
  print(sub);  // [2, 3]
}
```

---

<a id="part3"></a>
## 3️⃣ ⭐ **핵심** — Map (전화번호부 비유) [↑](#toc)

### Map이란?

Map은 **키(key)-값(value) 쌍의 모음**입니다.

> **비유**: 전화번호부를 생각해보세요. "홍길동"이라는 이름(키)으로 "010-1234-5678"이라는 번호(값)를 찾을 수 있습니다.

```
전화번호부 (Map<String, String>):
┌──────────┬──────────────────┐
│    Key   │      Value       │
├──────────┼──────────────────┤
│ '홍길동' │ '010-1234-5678'  │
│ '김민준' │ '010-9876-5432'  │
│ '이영희' │ '010-1111-2222'  │
└──────────┴──────────────────┘
```

### Map 선언하기

```dart
void main() {
  // Map<키타입, 값타입>
  Map<String, String> phoneBook = {
    '홍길동': '010-1234-5678',
    '김민준': '010-9876-5432',
    '이영희': '010-1111-2222',
  };
  
  // 값 접근
  print(phoneBook['홍길동']);  // 010-1234-5678
  print(phoneBook['없는사람']);  // null
  
  // 전체 키/값 목록
  print(phoneBook.keys);    // (홍길동, 김민준, 이영희)
  print(phoneBook.values);  // (010-..., 010-..., 010-...)
  
  // 개수
  print(phoneBook.length);  // 3
}
```

---

<a id="part4"></a>
## 4️⃣ ⭐ **핵심** — Map 조작 [↑](#toc)

### 추가/수정/삭제

```dart
void main() {
  Map<String, int> scores = {
    '국어': 85,
    '수학': 92,
    '영어': 78,
  };
  
  // 추가 (없는 키에 할당)
  scores['과학'] = 88;
  print(scores);  // {국어: 85, 수학: 92, 영어: 78, 과학: 88}
  
  // 수정 (있는 키에 할당)
  scores['수학'] = 95;
  print(scores['수학']);  // 95
  
  // 삭제
  scores.remove('영어');
  print(scores);  // {국어: 85, 수학: 95, 과학: 88}
  
  // 포함 여부
  print(scores.containsKey('국어'));    // true
  print(scores.containsValue(100));     // false
}
```

### null-safe 접근

```dart
void main() {
  Map<String, String> config = {
    'theme': 'dark',
    'language': 'ko',
  };
  
  // containsKey로 먼저 확인
  if (config.containsKey('theme')) {
    print(config['theme']);  // dark
  }
  
  // ?? 로 기본값 처리
  String fontSize = config['fontSize'] ?? '16';
  print(fontSize);  // 16 (없는 키라서 기본값)
}
```

---

<a id="part5"></a>
## 5️⃣ ⭐ **핵심** — 반복과 변환 [↑](#toc)

### for-in으로 순회

```dart
void main() {
  List<String> cities = ['서울', '부산', '대구', '인천'];
  
  // List 순회
  for (String city in cities) {
    print('도시: $city');
  }
  
  // Map 순회
  Map<String, int> population = {
    '서울': 950,
    '부산': 340,
    '대구': 240,
  };
  
  for (var entry in population.entries) {
    print('${entry.key}: ${entry.value}만명');
  }
}
```

### map() — 각 요소를 변환

```dart
void main() {
  List<int> numbers = [1, 2, 3, 4, 5];
  
  // 각 숫자를 제곱으로 변환
  List<int> squared = numbers.map((n) => n * n).toList();
  print(squared);  // [1, 4, 9, 16, 25]
  
  // 각 숫자를 문자열로 변환
  List<String> strings = numbers.map((n) => '$n번').toList();
  print(strings);  // [1번, 2번, 3번, 4번, 5번]
  
  // 과일 이름 대문자로
  List<String> fruits = ['apple', 'banana', 'cherry'];
  List<String> upper = fruits.map((f) => f.toUpperCase()).toList();
  print(upper);  // [APPLE, BANANA, CHERRY]
}
```

### where() — 조건에 맞는 요소만 필터

```dart
void main() {
  List<int> scores = [72, 85, 91, 60, 78, 95, 55, 88];
  
  // 80점 이상만 필터
  List<int> highScores = scores.where((s) => s >= 80).toList();
  print(highScores);  // [85, 91, 95, 88]
  
  // 짝수만 필터
  List<int> evens = scores.where((s) => s % 2 == 0).toList();
  print(evens);  // [72, 60, 78, 88]
  
  // 여러 조건 조합
  List<int> passingHighScores = scores
      .where((s) => s >= 70 && s <= 90)
      .toList();
  print(passingHighScores);  // [72, 85, 78, 88]
}
```

### 메서드 체이닝

```dart
void main() {
  List<int> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  
  // 짝수만 골라서 → 제곱으로 → 리스트로
  List<int> result = numbers
      .where((n) => n % 2 == 0)      // [2, 4, 6, 8, 10]
      .map((n) => n * n)              // [4, 16, 36, 64, 100]
      .toList();
  
  print(result);  // [4, 16, 36, 64, 100]
}
```

### 유용한 집계 메서드

```dart
void main() {
  List<int> numbers = [3, 1, 4, 1, 5, 9, 2, 6];
  
  // 최대값, 최소값
  print(numbers.reduce((a, b) => a > b ? a : b));  // 9 (max)
  print(numbers.reduce((a, b) => a < b ? a : b));  // 1 (min)
  
  // 합계
  int sum = numbers.fold(0, (acc, n) => acc + n);
  print(sum);  // 31
  
  // 모든 요소가 조건 만족?
  print(numbers.every((n) => n > 0));   // true (모두 양수)
  print(numbers.every((n) => n > 5));   // false
  
  // 하나라도 조건 만족?
  print(numbers.any((n) => n > 8));     // true (9가 있음)
  print(numbers.any((n) => n > 10));    // false
}
```

---

<a id="part6"></a>
## 6️⃣ 📖 **더 알아보기** — Spread 연산자 (...) [↑](#toc)

### 리스트 합치기

```dart
void main() {
  List<String> fruits = ['사과', '바나나'];
  List<String> vegetables = ['당근', '브로콜리'];
  
  // spread 연산자로 합치기
  List<String> food = [...fruits, ...vegetables];
  print(food);  // [사과, 바나나, 당근, 브로콜리]
  
  // 중간에 요소 추가하면서 합치기
  List<String> menu = ['밥', ...fruits, '디저트', ...vegetables];
  print(menu);  // [밥, 사과, 바나나, 디저트, 당근, 브로콜리]
}
```

### Flutter에서 spread 활용

```dart
// Flutter 위젯 리스트 조합에 자주 사용
List<Widget> baseWidgets = [
  const Text('기본 내용'),
  const Divider(),
];

List<Widget> extraWidgets = [
  const Text('추가 내용 1'),
  const Text('추가 내용 2'),
];

Column(
  children: [
    ...baseWidgets,
    ...extraWidgets,
  ],
)
```

---

<a id="part7"></a>
## 7️⃣ ⭐ **핵심** — Flutter 연결 실습 [↑](#toc)

### 리스트 데이터로 Text 위젯 여러 개 생성

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MenuListApp());
}

class MenuListApp extends StatelessWidget {
  const MenuListApp({super.key});

  @override
  Widget build(BuildContext context) {
    // 메뉴 데이터 리스트
    List<Map<String, dynamic>> menuItems = [
      {'name': '아메리카노', 'price': 4500, 'popular': true},
      {'name': '카페라떼', 'price': 5000, 'popular': true},
      {'name': '카푸치노', 'price': 5500, 'popular': false},
      {'name': '에스프레소', 'price': 4000, 'popular': false},
      {'name': '녹차라떼', 'price': 5500, 'popular': true},
    ];

    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('카페 메뉴'),
          backgroundColor: Colors.brown,
          foregroundColor: Colors.white,
        ),
        body: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '전체 메뉴 ${menuItems.length}개',
                style: const TextStyle(
                  fontSize: 14,
                  color: Colors.grey,
                ),
              ),
              const SizedBox(height: 8),
              // map()으로 메뉴 아이템 위젯 생성
              ...menuItems.map(
                (item) => Card(
                  child: ListTile(
                    title: Row(
                      children: [
                        Text(item['name'] as String),
                        if (item['popular'] == true) ...[
                          const SizedBox(width: 6),
                          const Chip(
                            label: Text('인기', style: TextStyle(fontSize: 10)),
                            backgroundColor: Colors.amber,
                            padding: EdgeInsets.zero,
                          ),
                        ],
                      ],
                    ),
                    trailing: Text(
                      '${item['price']}원',
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.brown,
                      ),
                    ),
                  ),
                ),
              ),
              const Divider(),
              // where()로 인기 메뉴만 필터링
              Text(
                '인기 메뉴: ${menuItems.where((i) => i['popular'] == true).length}개',
                style: const TextStyle(fontSize: 14),
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

<a id="part8"></a>
## 8️⃣ 정리 [↑](#toc)

### 핵심 정리

| 컬렉션 | 특징 | 선언 |
|--------|------|------|
| `List<T>` | 순서 있음, 중복 허용 | `[1, 2, 3]` |
| `Map<K, V>` | 키-값 쌍, 키는 유일 | `{'a': 1}` |

| 메서드 | 용도 | 예시 |
|--------|------|------|
| `.add()` | 요소 추가 | `list.add('값')` |
| `.remove()` | 요소 삭제 | `list.remove('값')` |
| `.contains()` | 포함 여부 | `list.contains('값')` |
| `.length` | 개수 | `list.length` |
| `.map()` | 변환 | `list.map((e) => e*2)` |
| `.where()` | 필터 | `list.where((e) => e>5)` |
| `.toList()` | Iterable → List | `.toList()` |
| `...` | 스프레드 | `[...a, ...b]` |

### 연습 문제

**문제 1**: 다음 리스트에서 5 이상인 숫자만 골라 새 리스트를 만드세요.
```dart
List<int> numbers = [2, 7, 1, 8, 2, 8, 1, 8, 2, 8];
```

**문제 2**: 학생 이름 리스트를 받아 각 이름 앞에 "학생: "을 붙인 새 리스트를 만드세요.
```dart
List<String> names = ['민준', '영희', '지수', '철수'];
```

**문제 3**: 다음 Map에서 점수가 80 이상인 과목만 출력하세요.
```dart
Map<String, int> grades = {
  '국어': 75,
  '수학': 88,
  '영어': 92,
  '과학': 70,
  '사회': 85,
};
```

**문제 4 (도전)**: 두 리스트를 합쳐서 중복을 제거한 리스트를 만드세요.
```dart
List<int> a = [1, 2, 3, 4];
List<int> b = [3, 4, 5, 6];
// 결과: [1, 2, 3, 4, 5, 6]
// 힌트: Set을 활용해보세요 - Set<int> set = {...a, ...b};
```

---

---

→ **다음 내용으로 넘어갑시다**: [06. Dart — 클래스와 객체](/ai-native-flutter/dart-classes)
