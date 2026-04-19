---
title: "06. Dart — 클래스와 객체"
layout: default
parent: AI-Native Flutter
nav_order: 8
permalink: /ai-native-flutter/dart-classes
---

# 6장. Dart — 클래스와 객체
{: .no_toc }

> **Phase 1** · 예상 시간: 120분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 설명 모드만**
> 클래스 개념이 어렵게 느껴질 수 있습니다. 이해가 안 되는 부분은 AI에게 비유로 설명해달라고 요청하세요. 하지만 코드는 직접 작성합니다.

## 학습 목표
- 클래스가 왜 필요한지 이해하고 직접 선언할 수 있다
- 생성자(Constructor)로 객체를 만들 수 있다
- 속성(Properties)과 메서드(Methods)를 정의하고 사용할 수 있다
- `extends`로 상속을 구현하고, Flutter의 StatelessWidget 구조를 설명할 수 있다

<a id="toc"></a>
## 진행 순서
1. [왜 클래스가 필요한가? — 명함 비유](#part1)
2. [클래스 선언하기 — 설계도와 실제 물건](#part2)
3. [생성자 (Constructor)](#part3)
4. [속성(Properties)과 메서드(Methods)](#part4)
5. [this 키워드](#part5)
6. [상속 기초 (extends)](#part6)
7. [Flutter 연결: StatelessWidget 직접 만들기](#part7)
8. [도전: toString(), @override](#part8)
9. [정리](#part9)

---

<a id="part1"></a>
## 1️⃣ ⭐ **핵심** — 왜 클래스가 필요한가? [↑](#toc)

### 명함 비유

앱에서 사용자 정보를 관리한다고 생각해봅시다.

**클래스 없이** 사용자 3명을 표현하면:

```dart
void main() {
  // 사용자 1
  String user1Name = '김민준';
  int user1Age = 25;
  String user1Email = 'minjun@example.com';
  String user1City = '서울';

  // 사용자 2
  String user2Name = '이영희';
  int user2Age = 23;
  String user2Email = 'younghee@example.com';
  String user2City = '부산';

  // 사용자 3
  String user3Name = '박지수';
  int user3Age = 27;
  String user3Email = 'jisu@example.com';
  String user3City = '대구';

  // 변수가 12개! 사용자 100명이면 변수 400개...
}
```

**클래스를 사용하면**:

```dart
class User {
  String name;
  int age;
  String email;
  String city;

  User(this.name, this.age, this.email, this.city);
}

void main() {
  User user1 = User('김민준', 25, 'minjun@example.com', '서울');
  User user2 = User('이영희', 23, 'younghee@example.com', '부산');
  User user3 = User('박지수', 27, 'jisu@example.com', '대구');

  // 정돈된 구조, 사용자 100명도 같은 방식으로!
}
```

> **비유**: 명함 한 장에는 이름, 회사, 전화번호, 이메일이 정해진 형식으로 들어있습니다. 클래스는 바로 그 명함의 **양식(형식)**이고, 객체는 **실제로 찍혀나온 명함 한 장**입니다.

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — 클래스 선언하기 [↑](#toc)

### 클래스 = 설계도, 객체 = 실제 물건

집을 짓는다고 생각해보세요:
- **설계도**: 방 3개, 화장실 2개, 창문 5개... (클래스)
- **실제 집**: 설계도대로 지어진 집 1채 (객체/인스턴스)

같은 설계도로 여러 집을 지을 수 있듯이, 하나의 클래스로 여러 객체를 만들 수 있습니다.

### 기본 클래스 문법

```dart
class Person {
  // 속성 (Properties/Fields)
  String name;
  int age;

  // 생성자 (Constructor)
  Person(this.name, this.age);

  // 메서드 (Methods)
  void introduce() {
    print('안녕하세요! 저는 $name이고 $age살입니다.');
  }
}

void main() {
  // 객체(인스턴스) 생성
  Person person1 = Person('김민준', 25);
  Person person2 = Person('이영희', 23);

  // 속성 접근
  print(person1.name);  // 김민준
  print(person2.age);   // 23

  // 메서드 호출
  person1.introduce();  // 안녕하세요! 저는 김민준이고 25살입니다.
  person2.introduce();  // 안녕하세요! 저는 이영희이고 23살입니다.
}
```

---

<a id="part3"></a>
## 3️⃣ ⭐ **핵심** — 생성자 (Constructor) [↑](#toc)

### 생성자란?

생성자는 객체를 만들 때 호출되는 특별한 함수입니다. 클래스 이름과 같은 이름을 가집니다.

> **비유**: 공장에서 제품을 만들 때 재료를 투입하는 과정입니다. "Person 하나 만들건데, 이름은 김민준이고 나이는 25야."

### 생성자의 종류

**1. 기본 생성자**

```dart
class Book {
  String title;
  String author;
  int year;

  // 긴 방식
  Book(String title, String author, int year) {
    this.title = title;
    this.author = author;
    this.year = year;
  }
}
```

**2. 축약형 생성자 (Dart 권장)**

```dart
class Book {
  String title;
  String author;
  int year;

  // this. 축약형
  Book(this.title, this.author, this.year);
}
```

**3. Named Constructor (이름 있는 생성자)**

```dart
class Circle {
  double radius;

  // 기본 생성자
  Circle(this.radius);

  // Named Constructor — 다양한 방식으로 생성
  Circle.fromDiameter(double diameter) : radius = diameter / 2;

  double get area => 3.14159 * radius * radius;
}

void main() {
  Circle c1 = Circle(5.0);             // 반지름으로 생성
  Circle c2 = Circle.fromDiameter(10); // 지름으로 생성

  print(c1.area);  // 약 78.54
  print(c2.area);  // 약 78.54 (같은 결과)
}
```

**4. Named Parameters를 사용한 생성자**

```dart
class Product {
  String name;
  int price;
  bool inStock;

  Product({
    required this.name,
    required this.price,
    this.inStock = true,  // 기본값
  });
}

void main() {
  Product p = Product(
    name: '플러터 교재',
    price: 35000,
    // inStock은 기본값 true 사용
  );

  print('${p.name}: ${p.price}원 (재고: ${p.inStock})');
}
```

---

<a id="part4"></a>
## 4️⃣ ⭐ **핵심** — 속성과 메서드 [↑](#toc)

### 속성 (Properties)

클래스가 가진 데이터입니다.

```dart
class BankAccount {
  String owner;       // 계좌주 (공개)
  double _balance;    // 잔액 (_ = 외부에서 직접 접근 금지 관례)

  BankAccount(this.owner, this._balance);

  // getter — 읽기 전용 속성
  double get balance => _balance;

  // getter — 계산된 속성
  bool get isEmpty => _balance <= 0;
}
```

### 메서드 (Methods)

클래스가 할 수 있는 동작입니다.

```dart
class BankAccount {
  String owner;
  double _balance;

  BankAccount(this.owner, this._balance);

  double get balance => _balance;

  // 입금 메서드
  void deposit(double amount) {
    if (amount > 0) {
      _balance += amount;
      print('${amount}원 입금 완료. 잔액: ${_balance}원');
    }
  }

  // 출금 메서드
  bool withdraw(double amount) {
    if (amount > _balance) {
      print('잔액 부족!');
      return false;
    }
    _balance -= amount;
    print('${amount}원 출금 완료. 잔액: ${_balance}원');
    return true;
  }
}

void main() {
  BankAccount account = BankAccount('김민준', 10000);

  account.deposit(5000);    // 5000원 입금 완료. 잔액: 15000.0원
  account.withdraw(3000);   // 3000원 출금 완료. 잔액: 12000.0원
  account.withdraw(20000);  // 잔액 부족!

  print('최종 잔액: ${account.balance}원');
}
```

---

<a id="part5"></a>
## 5️⃣ 📖 **더 알아보기** — this 키워드 [↑](#toc)

### this는 "나 자신"

`this`는 현재 객체 자신을 가리킵니다.

```dart
class Dog {
  String name;
  String breed;

  Dog(String name, String breed) {
    // 매개변수 name과 속성 name이 같은 이름 → this로 구분
    this.name = name;
    this.breed = breed;
  }

  void bark() {
    // this 생략 가능 (이름 충돌 없을 때)
    print('$name: 왈왈!');  // this.name과 동일
  }

  // 메서드 체이닝을 위해 this 반환
  Dog setName(String name) {
    this.name = name;
    return this;  // 자기 자신 반환
  }
}

void main() {
  Dog dog = Dog('초코', '포메라니안');
  dog.bark();  // 초코: 왈왈!

  // this를 반환하면 메서드 체이닝 가능
  dog.setName('몽실').bark();  // 몽실: 왈왈!
}
```

---

<a id="part6"></a>
## 6️⃣ ⭐ **핵심** — 상속 기초 (extends) [↑](#toc)

### 상속이란?

**상속(Inheritance)**은 기존 클래스의 속성과 메서드를 물려받아 새 클래스를 만드는 것입니다.

> **비유**: 부모님의 특징을 자녀가 물려받는 것처럼, 부모 클래스의 기능을 자식 클래스가 물려받습니다.

```dart
// 부모 클래스 (Animal)
class Animal {
  String name;
  int age;

  Animal(this.name, this.age);

  void breathe() {
    print('$name: 숨을 쉽니다');
  }

  void eat() {
    print('$name: 밥을 먹습니다');
  }
}

// 자식 클래스 (Dog extends Animal)
class Dog extends Animal {
  String breed;

  // super: 부모 생성자 호출
  Dog(String name, int age, this.breed) : super(name, age);

  // 새로운 메서드 추가
  void bark() {
    print('$name: 왈왈!');
  }

  // 부모 메서드 재정의 (override)
  @override
  void eat() {
    print('$name: 사료를 먹습니다');  // 개만의 방식
  }
}

void main() {
  Dog dog = Dog('초코', 3, '포메라니안');

  // 부모 클래스의 메서드 사용 가능
  dog.breathe();  // 초코: 숨을 쉽니다

  // override된 메서드
  dog.eat();   // 초코: 사료를 먹습니다 (재정의된 버전)

  // 새로 추가한 메서드
  dog.bark();  // 초코: 왈왈!
}
```

### "Widget이 왜 extends StatelessWidget인가"

Flutter의 모든 위젯도 상속을 사용합니다:

```dart
// Flutter 내부 (간략화)
abstract class Widget { ... }
abstract class StatelessWidget extends Widget {
  Widget build(BuildContext context);  // 이 메서드를 반드시 구현해야 함
}

// 우리가 만드는 위젯
class MyWidget extends StatelessWidget {
  @override           // 부모 메서드 재정의
  Widget build(BuildContext context) {
    return Text('안녕하세요');  // 직접 구현
  }
}
```

> **핵심**: `extends StatelessWidget`은 "StatelessWidget의 자식 클래스로 만들겠다"는 선언입니다. `@override`는 "부모에서 정의된 `build` 메서드를 내가 직접 구현합니다"라는 표시입니다.

---

<a id="part7"></a>
## 7️⃣ ⭐ **핵심** — Flutter 연결: StatelessWidget 만들기 [↑](#toc)

### 나만의 위젯 클래스 만들기

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('클래스와 위젯'),
        ),
        body: Center(
          child: ProfileCard(
            name: '김민준',
            job: 'Flutter 개발자',
            city: '서울',
          ),
        ),
      ),
    );
  }
}

// 나만의 ProfileCard 위젯 클래스
class ProfileCard extends StatelessWidget {
  // 속성 선언
  final String name;
  final String job;
  final String city;

  // 생성자
  const ProfileCard({
    super.key,
    required this.name,
    required this.job,
    required this.city,
  });

  // build 메서드 재정의 (@override)
  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const CircleAvatar(
              radius: 40,
              backgroundColor: Colors.blue,
              child: Icon(Icons.person, size: 50, color: Colors.white),
            ),
            const SizedBox(height: 12),
            Text(
              name,
              style: const TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              job,
              style: const TextStyle(
                fontSize: 16,
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.location_on, size: 16, color: Colors.red),
                Text(city),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

---

<a id="part8"></a>
## 8️⃣ 🚀 **도전** — toString()과 @override [↑](#toc)

### toString() 재정의

Dart의 모든 객체는 `toString()` 메서드를 가지고 있습니다. 기본적으로는 `Instance of 'ClassName'`을 반환하는데, 이를 재정의할 수 있습니다.

```dart
class Product {
  String name;
  int price;
  bool inStock;

  Product({
    required this.name,
    required this.price,
    this.inStock = true,
  });

  // toString() 재정의 — print()할 때 보기 좋게
  @override
  String toString() {
    String stockStatus = inStock ? '재고 있음' : '품절';
    return 'Product{name: $name, price: $price원, $stockStatus}';
  }
}

void main() {
  Product p = Product(name: '플러터 교재', price: 35000);
  print(p);
  // 출력: Product{name: 플러터 교재, price: 35000원, 재고 있음}

  List<Product> products = [
    Product(name: '교재', price: 35000),
    Product(name: '노트북', price: 1500000, inStock: false),
    Product(name: '볼펜', price: 500),
  ];

  for (Product prod in products) {
    print(prod);  // toString()이 자동 호출됨
  }
}
```

### @override 총정리

`@override`는 부모 클래스에서 이미 정의된 메서드를 자식 클래스에서 다시 구현하겠다는 표시입니다.

| 메서드 | 부모 | 자주 재정의하는 경우 |
|--------|------|---------------------|
| `toString()` | Object | 디버깅/로깅 편의 |
| `build()` | StatelessWidget | Flutter 위젯 구현 |
| `initState()` | State | StatefulWidget 초기화 |
| `dispose()` | State | 리소스 해제 |

---

<a id="part9"></a>
## 9️⃣ 정리 — "클래스 = Flutter 위젯의 기본 구조" [↑](#toc)

### 핵심 정리

| 개념 | 키워드 | 설명 |
|------|--------|------|
| 클래스 선언 | `class` | 설계도 정의 |
| 객체 생성 | `ClassName()` | 실제 물건 생성 |
| 생성자 | `ClassName(this.x)` | 객체 초기화 |
| 속성 | `String name;` | 데이터 저장 |
| 메서드 | `void doSomething()` | 동작 정의 |
| 자기 참조 | `this` | 현재 객체 |
| 상속 | `extends` | 부모 기능 물려받기 |
| 메서드 재정의 | `@override` | 부모 메서드를 내 방식으로 |
| 부모 호출 | `super` | 부모 생성자/메서드 호출 |

### Flutter와의 연결

```
Dart 클래스 개념          Flutter 위젯 적용
─────────────────         ──────────────────
class 선언            →   class MyWidget
extends               →   extends StatelessWidget
생성자                →   const MyWidget({super.key, ...})
속성                  →   final String title;
메서드                →   @override Widget build(...)
```

### 연습 문제

**문제 1**: `Student` 클래스를 만드세요.
- 속성: 이름(name), 학번(id), 점수(score)
- 메서드: `isPassed()` — 60점 이상이면 true 반환
- `toString()` 재정의 — 이름과 합격 여부 출력

**문제 2**: `Shape` 부모 클래스와 `Rectangle`, `Circle` 자식 클래스를 만드세요.
- Shape: `String color`, `double area()` (자식에서 구현)
- Rectangle: 너비(width), 높이(height)
- Circle: 반지름(radius)

**문제 3 (도전)**: 위 `Student` 클래스를 사용하는 Flutter 위젯을 만들어서, 학생 정보와 합격/불합격 여부를 화면에 표시하세요.

---

---

→ **다음 내용으로 넘어갑시다**: [07. Flutter 위젯 기초](/ai-native-flutter/widgets-basics)
