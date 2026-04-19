---
title: "17. 테스트 입문 + TDD"
layout: default
parent: AI-Native Flutter
nav_order: 19
permalink: /ai-native-flutter/testing-tdd
---

# 17장. 테스트 입문 + TDD
{: .no_toc }

> **Phase 3** · 예상 시간: 120분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 완전 페어 프로그래밍**
> AI(Copilot)와 완전한 협업이 가능합니다.
> 내가 설계하고 AI가 구현합니다. 테스트로 검증합니다.
> "신뢰하되 검증한다(Trust but verify)"가 원칙입니다.

## 학습 목표

- 테스트의 필요성을 이해하고 Flutter 테스트 피라미드를 설명할 수 있다
- `test()`, `expect()`, `group()`으로 단위 테스트를 작성할 수 있다
- `testWidgets()`로 UI 인터랙션을 검증할 수 있다
- TDD(Red → Green → Refactor) 사이클로 기능을 개발할 수 있다

<a id="toc"></a>
## 진행 순서

1. [테스트란?](#part1) — 자동화된 검증
2. [Flutter 테스트 피라미드](#part2) — 3가지 테스트 종류
3. [단위 테스트](#part3) — 순수 Dart 함수 테스트
4. [위젯 테스트](#part4) — UI 검증
5. [TDD 사이클](#part5) — Red → Green → Refactor
6. [AI + TDD 워크플로우](#part6) — AI와 함께하는 TDD
7. [실습](#part7) — 카운터 앱 TDD로 만들기
8. [정리](#part8)

---

<a id="part1"></a>
## 1️⃣ ⭐ **핵심** — 테스트란? [↑](#toc)

### 공장 품질검사 비유

자동차 공장에서 차를 만들 때, 생산 라인에 품질 검사 구간이 있습니다.

- 엔진이 올바르게 조립되었는가?
- 브레이크가 제대로 작동하는가?
- 도어가 잘 닫히는가?

이 검사를 **매번 사람이 직접 확인**한다면 시간이 너무 오래 걸립니다.  
그래서 로봇이 자동으로 매번 동일한 기준으로 검사합니다.

소프트웨어 테스트도 마찬가지입니다.  
코드를 변경할 때마다 사람이 앱을 켜서 모든 기능을 눌러볼 수 없습니다.  
**자동화된 테스트**가 대신 확인해줍니다.

### 테스트가 없으면 어떤 일이 벌어지나

```
A 기능 수정 → 앱 실행 → B 기능이 갑자기 깨짐 😱
```

테스트가 있으면:

```
A 기능 수정 → 테스트 실행 (3초) → B 관련 테스트 실패 알림 → 즉시 수정
```

### Flutter 테스트의 장점

| 상황 | 테스트 없이 | 테스트 있이 |
|------|------------|------------|
| 코드 수정 후 확인 | 앱 실행 → 직접 클릭 (5분) | `flutter test` 명령어 (10초) |
| 버그 발견 시점 | 출시 후 (최악) | 개발 중 (최선) |
| AI 코드 신뢰도 | "이게 맞나?" | "테스트 통과 = 동작 보장" |

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — Flutter 테스트 피라미드 [↑](#toc)

```
         ╱╲
        ╱  ╲
       ╱ 통합 ╲    ← 느리고, 설정 복잡, 전체 앱 테스트
      ╱  테스트  ╲
     ╱────────────╲
    ╱  위젯 테스트  ╲  ← 중간 속도, UI 동작 검증
   ╱                ╲
  ╱────────────────────╲
 ╱     단위 테스트       ╲  ← 빠르고, 쉽고, 많이 작성
╱──────────────────────────╲
```

| 종류 | 속도 | 범위 | 비율 |
|------|------|------|------|
| 단위(Unit) 테스트 | 매우 빠름 | 함수 하나 | 70% |
| 위젯(Widget) 테스트 | 빠름 | 위젯 하나 | 20% |
| 통합(Integration) 테스트 | 느림 | 앱 전체 | 10% |

이 장에서는 **단위 테스트**와 **위젯 테스트**를 배웁니다.

### flutter_test 패키지

Flutter에는 테스트 패키지가 기본으로 포함되어 있습니다.  
`pubspec.yaml`의 `dev_dependencies`에 이미 있습니다:

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
```

---

<a id="part3"></a>
## 3️⃣ ⭐ **핵심** — 단위 테스트: 순수 Dart 함수 테스트 [↑](#toc)

### 기본 구조

```dart
// test/models/bmi_calculator_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/models/bmi_calculator.dart';

void main() {
  group('BmiCalculator', () {
    test('정상 체중일 때 BMI를 올바르게 계산한다', () {
      // Arrange (준비)
      final calculator = BmiCalculator();

      // Act (실행)
      final bmi = calculator.calculate(weight: 70, height: 1.75);

      // Assert (검증)
      expect(bmi, closeTo(22.86, 0.01));
    });
  });
}
```

### 핵심 함수들

#### test()

```dart
test('테스트 이름', () {
  // 테스트 내용
});
```

#### expect()

```dart
// 값이 같은지
expect(result, equals(42));
expect(name, equals('Flutter'));

// 값이 참/거짓인지
expect(isValid, isTrue);
expect(isEmpty, isFalse);

// null 확인
expect(value, isNull);
expect(value, isNotNull);

// 범위 확인
expect(bmi, closeTo(22.86, 0.01));  // 오차 0.01 이내

// 예외 발생 확인
expect(() => calculator.calculate(weight: -1, height: 1.75),
    throwsArgumentError);

// 타입 확인
expect(result, isA<List<String>>());
```

#### group()

```dart
group('BmiCalculator', () {
  // 한 클래스의 테스트를 묶음
  group('calculate()', () {
    test('정상 입력 시 올바른 BMI 반환', () { ... });
    test('음수 체중 입력 시 ArgumentError 발생', () { ... });
    test('키가 0일 때 ArgumentError 발생', () { ... });
  });

  group('getBmiCategory()', () {
    test('BMI 18.5 미만 → 저체중', () { ... });
    test('BMI 18.5~24.9 → 정상', () { ... });
    test('BMI 25 이상 → 과체중', () { ... });
  });
});
```

### setUp() / tearDown()

```dart
group('BmiCalculator', () {
  late BmiCalculator calculator;

  setUp(() {
    // 각 테스트 전에 실행
    calculator = BmiCalculator();
  });

  tearDown(() {
    // 각 테스트 후에 실행 (리소스 해제 등)
  });

  test('BMI 계산', () {
    // calculator가 이미 초기화되어 있음
    expect(calculator.calculate(weight: 70, height: 1.75), closeTo(22.86, 0.01));
  });
});
```

### 실습: BMI 계산 함수 테스트

**테스트할 클래스:**

```dart
// lib/models/bmi_calculator.dart
class BmiCalculator {
  /// BMI = 체중(kg) / 키(m)^2
  double calculate({required double weight, required double height}) {
    if (weight <= 0) throw ArgumentError('체중은 0보다 커야 합니다');
    if (height <= 0) throw ArgumentError('키는 0보다 커야 합니다');
    return weight / (height * height);
  }

  String getCategory(double bmi) {
    if (bmi < 18.5) return '저체중';
    if (bmi < 25.0) return '정상';
    if (bmi < 30.0) return '과체중';
    return '비만';
  }
}
```

**테스트 파일:**

```dart
// test/models/bmi_calculator_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/models/bmi_calculator.dart';

void main() {
  group('BmiCalculator', () {
    late BmiCalculator calculator;

    setUp(() {
      calculator = BmiCalculator();
    });

    group('calculate()', () {
      test('정상 입력 시 올바른 BMI를 반환한다', () {
        final bmi = calculator.calculate(weight: 70, height: 1.75);
        expect(bmi, closeTo(22.857, 0.001));
      });

      test('체중이 0 이하이면 ArgumentError를 발생시킨다', () {
        expect(
          () => calculator.calculate(weight: 0, height: 1.75),
          throwsArgumentError,
        );
      });

      test('키가 0 이하이면 ArgumentError를 발생시킨다', () {
        expect(
          () => calculator.calculate(weight: 70, height: 0),
          throwsArgumentError,
        );
      });
    });

    group('getCategory()', () {
      test('BMI 17은 저체중이다', () {
        expect(calculator.getCategory(17.0), equals('저체중'));
      });

      test('BMI 22는 정상이다', () {
        expect(calculator.getCategory(22.0), equals('정상'));
      });

      test('BMI 27은 과체중이다', () {
        expect(calculator.getCategory(27.0), equals('과체중'));
      });

      test('BMI 32는 비만이다', () {
        expect(calculator.getCategory(32.0), equals('비만'));
      });
    });
  });
}
```

**테스트 실행:**

```bash
flutter test test/models/bmi_calculator_test.dart
```

---

<a id="part4"></a>
## 4️⃣ ⭐ **핵심** — 위젯 테스트: UI 검증 [↑](#toc)

### testWidgets() 기본 구조

```dart
testWidgets('카운터 초기값은 0이다', (WidgetTester tester) async {
  // 1. 위젯 빌드
  await tester.pumpWidget(const MyApp());

  // 2. 텍스트 찾기
  expect(find.text('0'), findsOneWidget);
  expect(find.text('1'), findsNothing);
});
```

### 주요 find 메서드

```dart
// 텍스트로 찾기
find.text('Hello Flutter')

// 위젯 타입으로 찾기
find.byType(ElevatedButton)
find.byType(TextField)

// 아이콘으로 찾기
find.byIcon(Icons.add)
find.byIcon(Icons.delete)

// Key로 찾기 (가장 정확)
find.byKey(Key('counter-text'))

// 여러 위젯 찾기
find.byType(ListTile)  // 여러 개 있을 수 있음
```

### 찾은 위젯 수 검증

```dart
expect(find.text('0'), findsOneWidget);   // 정확히 1개
expect(find.text('항목'), findsWidgets);   // 1개 이상
expect(find.text('없음'), findsNothing);   // 0개
expect(find.byType(Card), findsNWidgets(3)); // 정확히 3개
```

### 인터랙션

```dart
// 버튼 탭
await tester.tap(find.byIcon(Icons.add));
await tester.pump();  // 상태 변화 반영 (한 번)

// 텍스트 입력
await tester.enterText(find.byType(TextField), '서울');
await tester.pump();

// 스크롤
await tester.drag(find.byType(ListView), Offset(0, -300));
await tester.pump();

// 애니메이션 완료까지 기다리기
await tester.pumpAndSettle();
```

### 위젯 테스트 예시

```dart
// test/widgets/counter_widget_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/main.dart';

void main() {
  group('CounterApp', () {
    testWidgets('초기 카운터 값은 0이다', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());
      expect(find.text('0'), findsOneWidget);
    });

    testWidgets('+버튼을 탭하면 카운터가 1 증가한다', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());

      // + 버튼 탭
      await tester.tap(find.byIcon(Icons.add));
      await tester.pump();

      expect(find.text('1'), findsOneWidget);
    });

    testWidgets('+버튼을 3번 탭하면 카운터가 3이 된다', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());

      for (int i = 0; i < 3; i++) {
        await tester.tap(find.byIcon(Icons.add));
        await tester.pump();
      }

      expect(find.text('3'), findsOneWidget);
    });
  });
}
```

---

<a id="part5"></a>
## 5️⃣ ⭐ **핵심** — TDD 사이클: Red → Green → Refactor [↑](#toc)

### TDD란?

**Test-Driven Development**: 코드를 작성하기 전에 테스트를 먼저 작성하는 개발 방법입니다.

```
🔴 Red: 실패하는 테스트 작성
    ↓
🟢 Green: 테스트를 통과시키는 최소한의 코드 작성
    ↓
🔵 Refactor: 코드 개선 (테스트는 여전히 통과)
    ↓
    다시 🔴 Red로...
```

### 왜 테스트를 먼저 작성하는가?

1. **명확한 목표**: 테스트를 쓰면서 "무엇을 만들어야 하는지"가 명확해집니다
2. **즉각적인 피드백**: 내가 만든 코드가 요구사항을 만족하는지 바로 알 수 있습니다
3. **두려움 없는 수정**: 테스트가 있으면 코드를 마음껏 개선할 수 있습니다
4. **AI 검증**: AI가 만든 코드가 의도대로 동작하는지 확인할 수 있습니다

### 사이클 시연: 문자열 뒤집기

#### 🔴 Step 1: 실패하는 테스트 작성

```dart
// test/utils/string_utils_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/utils/string_utils.dart';

void main() {
  group('StringUtils', () {
    test('reverse(): 문자열을 뒤집는다', () {
      expect(StringUtils.reverse('Flutter'), equals('rettulF'));
    });

    test('reverse(): 빈 문자열은 빈 문자열을 반환한다', () {
      expect(StringUtils.reverse(''), equals(''));
    });

    test('reverse(): 한 글자는 그대로 반환한다', () {
      expect(StringUtils.reverse('A'), equals('A'));
    });
  });
}
```

`flutter test` 실행 → **컴파일 에러** (StringUtils가 없으니까) → 🔴 Red

#### 🟢 Step 2: 통과시키는 최소 코드 작성

```dart
// lib/utils/string_utils.dart
class StringUtils {
  static String reverse(String text) {
    return text.split('').reversed.join('');
  }
}
```

`flutter test` 실행 → **3/3 통과** → 🟢 Green

#### 🔵 Step 3: 리팩토링

```dart
// 더 간결하게 개선 (String extension 사용)
extension StringExtension on String {
  String get reversed => split('').reversed.join('');
}
```

`flutter test` 실행 → **여전히 통과** → 🔵 Refactor 완료

---

<a id="part6"></a>
## 6️⃣ 🚀 **도전** — AI + TDD 워크플로우 [↑](#toc)

### 사람이 테스트, AI가 구현

TDD와 AI의 완벽한 조합:

```
사람 (요구사항 이해)
    ↓
테스트 작성 (내가 기대하는 동작을 코드로 표현)
    ↓
Copilot에게 요청: "이 테스트를 통과하는 구현을 만들어줘"
    ↓
AI가 구현 코드 생성
    ↓
테스트 실행으로 검증
    ↓
통과하면 완성 / 실패하면 AI에게 수정 요청
```

### 프롬프트 예시

```
아래 테스트를 모두 통과하는 CartService 클래스를 구현해줘.

테스트 파일:
- addItem(): 상품을 장바구니에 추가한다
- removeItem(): 상품을 장바구니에서 제거한다
- getTotal(): 모든 상품 가격의 합을 반환한다
- clear(): 장바구니를 비운다

기술 제약:
- 순수 Dart (Flutter 없이)
- CartItem 모델: id(String), name(String), price(double), quantity(int)
- lib/services/cart_service.dart에 작성
```

### "신뢰하되 검증한다"의 의미

AI가 생성한 코드가 테스트를 통과한다고 해서 무조건 좋은 코드는 아닙니다.

**테스트 통과는 최소 조건입니다.** 추가로 확인해야 할 것:

- 엣지 케이스(빈 값, 최댓값 등)가 처리되는가?
- 코드가 읽기 쉬운가?
- 불필요한 복잡성은 없는가?

---

<a id="part7"></a>
## 7️⃣ 🚀 **도전** — 실습: 카운터 앱 TDD로 만들기 [↑](#toc)

### 목표

기본 카운터 앱을 TDD로 만들되, 추가 요구사항을 구현합니다:

- 증가 버튼(+1), 감소 버튼(-1), 초기화 버튼(0으로)
- 카운터는 음수가 될 수 없음 (0이 최솟값)
- 카운터 최댓값은 10

### Step 1: CounterService 단위 테스트 (🔴 Red)

```bash
flutter create tdd_counter
cd tdd_counter
```

```dart
// test/services/counter_service_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:tdd_counter/services/counter_service.dart';

void main() {
  group('CounterService', () {
    late CounterService service;

    setUp(() {
      service = CounterService();
    });

    test('초기값은 0이다', () {
      expect(service.count, equals(0));
    });

    test('increment(): 카운터가 1 증가한다', () {
      service.increment();
      expect(service.count, equals(1));
    });

    test('decrement(): 카운터가 1 감소한다', () {
      service.increment();
      service.decrement();
      expect(service.count, equals(0));
    });

    test('decrement(): 0에서 감소하면 0을 유지한다', () {
      service.decrement();
      expect(service.count, equals(0));
    });

    test('increment(): 10에서 증가하면 10을 유지한다', () {
      for (int i = 0; i < 10; i++) {
        service.increment();
      }
      service.increment(); // 11번째 시도
      expect(service.count, equals(10));
    });

    test('reset(): 카운터가 0으로 초기화된다', () {
      service.increment();
      service.increment();
      service.reset();
      expect(service.count, equals(0));
    });
  });
}
```

### Step 2: Copilot에게 구현 요청 (🟢 Green)

```
위 테스트를 모두 통과하는 CounterService 클래스를 작성해줘.
- 파일 위치: lib/services/counter_service.dart
- count 속성 (int, 초기값 0)
- increment(), decrement(), reset() 메서드
- 최솟값 0, 최댓값 10
```

예상 구현:

```dart
// lib/services/counter_service.dart
class CounterService {
  static const int _minCount = 0;
  static const int _maxCount = 10;

  int _count = 0;

  int get count => _count;

  void increment() {
    if (_count < _maxCount) {
      _count++;
    }
  }

  void decrement() {
    if (_count > _minCount) {
      _count--;
    }
  }

  void reset() {
    _count = _minCount;
  }
}
```

### Step 3: 테스트 실행

```bash
flutter test test/services/counter_service_test.dart
```

모든 테스트 통과 확인.

### Step 4: 위젯 테스트 (🔴 Red)

```dart
// test/widgets/counter_screen_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:tdd_counter/main.dart';

void main() {
  group('CounterScreen', () {
    testWidgets('초기 카운터는 0을 표시한다', (tester) async {
      await tester.pumpWidget(const MyApp());
      expect(find.text('0'), findsOneWidget);
    });

    testWidgets('+ 버튼을 탭하면 카운터가 1 증가한다', (tester) async {
      await tester.pumpWidget(const MyApp());
      await tester.tap(find.byIcon(Icons.add));
      await tester.pump();
      expect(find.text('1'), findsOneWidget);
    });

    testWidgets('- 버튼을 탭하면 카운터가 1 감소한다', (tester) async {
      await tester.pumpWidget(const MyApp());
      await tester.tap(find.byIcon(Icons.add));
      await tester.pump();
      await tester.tap(find.byIcon(Icons.remove));
      await tester.pump();
      expect(find.text('0'), findsOneWidget);
    });

    testWidgets('초기화 버튼을 탭하면 카운터가 0이 된다', (tester) async {
      await tester.pumpWidget(const MyApp());
      await tester.tap(find.byIcon(Icons.add));
      await tester.pump();
      await tester.tap(find.byIcon(Icons.refresh));
      await tester.pump();
      expect(find.text('0'), findsOneWidget);
    });
  });
}
```

### Step 5: UI 구현

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'services/counter_service.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TDD 카운터',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const CounterScreen(),
    );
  }
}

class CounterScreen extends StatefulWidget {
  const CounterScreen({super.key});

  @override
  State<CounterScreen> createState() => _CounterScreenState();
}

class _CounterScreenState extends State<CounterScreen> {
  final CounterService _service = CounterService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('TDD 카운터'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              '${_service.count}',
              style: Theme.of(context).textTheme.displayLarge,
            ),
            const SizedBox(height: 32),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton.filled(
                  onPressed: () => setState(() => _service.decrement()),
                  icon: const Icon(Icons.remove),
                  iconSize: 32,
                ),
                const SizedBox(width: 16),
                IconButton.filled(
                  onPressed: () => setState(() => _service.reset()),
                  icon: const Icon(Icons.refresh),
                  iconSize: 32,
                ),
                const SizedBox(width: 16),
                IconButton.filled(
                  onPressed: () => setState(() => _service.increment()),
                  icon: const Icon(Icons.add),
                  iconSize: 32,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

### Step 6: 전체 테스트 실행

```bash
flutter test
```

---

<a id="part8"></a>
## 8️⃣ 정리 [↑](#toc)

### 이 장에서 배운 것

| 개념 | 핵심 |
|------|------|
| 테스트 피라미드 | 단위(70%) > 위젯(20%) > 통합(10%) |
| test() | 단위 테스트 함수 |
| expect() | 결과 검증 |
| group() | 테스트 묶기 |
| testWidgets() | UI 테스트 함수 |
| find.text() | 텍스트로 위젯 찾기 |
| tester.tap() | 버튼 탭 시뮬레이션 |
| TDD | 테스트 → 구현 → 리팩토링 |

### TDD + AI 조합의 핵심

```
내가 테스트를 작성한다  ←  요구사항을 내가 이해하는 증거
AI가 구현을 생성한다   ←  반복적인 코딩 작업은 AI에게
테스트로 AI를 검증한다 ←  "신뢰하되 검증한다"
```

### 다음 장 예고

다음 장에서는 **Provider 상태 관리**를 배웁니다.  
여러 화면이 같은 데이터를 공유해야 할 때 `setState`의 한계를 넘어서는 방법입니다.
