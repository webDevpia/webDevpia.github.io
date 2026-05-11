---
title: "18. Provider 상태 관리"
layout: default
parent: AI-Native Flutter
nav_order: 20
permalink: /ai-native-flutter/provider
---

# 18장. Provider 상태 관리
{: .no_toc }

> **Phase 3** · 예상 시간: 120분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 완전 페어 프로그래밍**
> AI(Copilot)와 완전한 협업이 가능합니다.
> 내가 설계하고 AI가 구현합니다. 테스트로 검증합니다.
> "신뢰하되 검증한다(Trust but verify)"가 원칙입니다.

> 🚀 **도전 챕터** — Phase 3 핵심 내용을 완료한 후 여유가 있을 때 진행하세요.

## 학습 목표

- `setState`의 한계를 이해하고 Provider가 필요한 상황을 설명할 수 있다
- `ChangeNotifier`로 상태 클래스를 작성할 수 있다
- `ChangeNotifierProvider`, `Consumer`, `context.watch`로 여러 화면이 상태를 공유할 수 있다

<a id="toc"></a>
## 진행 순서

1. [setState의 한계](#part1) — 다른 화면과 상태 공유 문제
2. [Provider란?](#part2) — 방송국 비유
3. [provider 패키지 설치](#part3)
4. [ChangeNotifier](#part4) — 데이터 + 알림
5. [ChangeNotifierProvider](#part5) — 방송국 설치
6. [Consumer](#part6) — 데이터 수신
7. [context.read vs context.watch](#part7)
8. [실습: 장바구니](#part8)
9. [더 알아보기: Riverpod 소개](#part9)
10. [정리](#part10)

---

<a id="part1"></a>
## 1️⃣ ⭐ **핵심** — setState의 한계 [↑](#toc)

### 지금까지 우리가 쓴 방식

```dart
class CounterScreen extends StatefulWidget { ... }

class _CounterScreenState extends State<CounterScreen> {
  int _count = 0;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () => setState(() => _count++),
      child: Text('$_count'),
    );
  }
}
```

`setState`는 **같은 화면 안에서** 상태를 바꿀 때 완벽합니다.

### 문제 상황

쇼핑몰 앱을 만들다고 가정합시다.

- **상품 목록 화면**: 각 상품 옆에 "장바구니 담기" 버튼 → 장바구니 개수 표시
- **하단 탭 바**: 장바구니 아이콘에 뱃지(개수) 표시
- **장바구니 화면**: 담긴 상품 목록 + 총 금액

이 3곳이 **같은 장바구니 데이터**를 공유해야 합니다.

`setState`만으로는 이 문제를 해결하기 어렵습니다:

```
상품 화면 ←→ 장바구니 데이터 ←→ 탭 바
                  ↕
             장바구니 화면
```

데이터를 누가 가지고 있어야 하는지, 어떻게 전달해야 하는지 복잡해집니다.

### setState로 억지로 해결하면

```dart
// 최상위 위젯에 상태를 두고 콜백으로 내려보냄
class MyApp extends StatefulWidget { ... }
class _MyAppState extends State<MyApp> {
  List<CartItem> cartItems = [];  // 여기에 상태

  void addToCart(CartItem item) {
    setState(() => cartItems.add(item));
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: ProductScreen(
        onAddToCart: addToCart,  // 콜백 전달
        cartCount: cartItems.length,  // 데이터 전달
      ),
    );
  }
}
```

위젯이 깊어질수록 **prop drilling**(상태를 계속 내려주는 것)이 발생해 코드가 지저분해집니다.

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — Provider란? [↑](#toc)

### 방송국 비유

**방송국**은 콘텐츠를 한 곳에서 만들어 **불특정 다수**에게 동시에 전달합니다.

| 방송국 비유 | Provider |
|------------|----------|
| 방송국 | Provider (데이터 제공자) |
| TV 수신기 | Consumer / context.watch (데이터 수신자) |
| 채널 변경 | notifyListeners() |
| 방송 수신 | 위젯 자동 리빌드 |

### Provider의 작동 방식

```
앱 최상단에 Provider 설치
    ↓
어디서든 이 데이터를 "구독"할 수 있음
    ↓
데이터가 변경되면 구독 중인 위젯만 자동으로 리빌드
```

### 핵심 3요소

| 역할 | 클래스/위젯 | 설명 |
|------|------------|------|
| 데이터 + 알림 | `ChangeNotifier` | 상태 클래스의 부모 |
| 앱에 데이터 주입 | `ChangeNotifierProvider` | 방송국 설치 |
| 데이터 수신 | `Consumer` / `context.watch` | 방송 수신기 |

---

<a id="part3"></a>
## 3️⃣ ⭐ **핵심** — provider 패키지 설치 [↑](#toc)

```bash
flutter pub add provider
```

또는 `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  provider: ^6.1.2
```

```bash
flutter pub get
```

임포트:

```dart
import 'package:provider/provider.dart';
```

---

<a id="part4"></a>
## 4️⃣ ⭐ **핵심** — ChangeNotifier: 데이터 + 알림 기능 [↑](#toc)

### ChangeNotifier란?

상태(데이터)를 가지고 있으면서, 상태가 변경될 때 **"변경됐어!"** 라고 알려주는 클래스입니다.

```dart
import 'package:flutter/foundation.dart';

class CartNotifier extends ChangeNotifier {
  // 내부 상태
  final List<CartItem> _items = [];

  // 읽기 전용 getter
  List<CartItem> get items => List.unmodifiable(_items);
  int get itemCount => _items.length;
  double get total => _items.fold(0, (sum, item) => sum + item.price);

  // 상태 변경 메서드
  void addItem(CartItem item) {
    _items.add(item);
    notifyListeners(); // ← 핵심! "나 변경됐어!"
  }

  void removeItem(String id) {
    _items.removeWhere((item) => item.id == id);
    notifyListeners();
  }

  void clear() {
    _items.clear();
    notifyListeners();
  }
}
```

### 핵심: notifyListeners()

```dart
void addItem(CartItem item) {
  _items.add(item);
  notifyListeners(); // ← 이걸 호출해야 Consumer가 리빌드됨
}
```

`notifyListeners()`를 빠뜨리면 데이터는 변경되지만 UI가 업데이트되지 않습니다.

---

<a id="part5"></a>
## 5️⃣ ⭐ **핵심** — ChangeNotifierProvider: 방송국 설치 [↑](#toc)

### 앱 최상단에 Provider 배치

```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'notifiers/cart_notifier.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(
    // ChangeNotifierProvider로 앱 감싸기
    ChangeNotifierProvider(
      create: (context) => CartNotifier(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: const HomeScreen(),
    );
  }
}
```

### 여러 Provider를 동시에 사용할 때

```dart
// MultiProvider 사용
void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => CartNotifier()),
        ChangeNotifierProvider(create: (_) => UserNotifier()),
        ChangeNotifierProvider(create: (_) => ThemeNotifier()),
      ],
      child: const MyApp(),
    ),
  );
}
```

---

<a id="part6"></a>
## 6️⃣ ⭐ **핵심** — Consumer: 데이터 수신 [↑](#toc)

### Consumer 위젯

```dart
Consumer<CartNotifier>(
  builder: (context, cart, child) {
    // cart: CartNotifier 인스턴스
    // notifyListeners()가 호출될 때마다 builder가 다시 실행됨

    return Text('장바구니: ${cart.itemCount}개');
  },
)
```

### 실제 예시

```dart
class CartIconWidget extends StatelessWidget {
  const CartIconWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<CartNotifier>(
      builder: (context, cart, child) {
        return Stack(
          children: [
            const Icon(Icons.shopping_cart),
            if (cart.itemCount > 0)
              Positioned(
                right: 0,
                top: 0,
                child: CircleAvatar(
                  radius: 8,
                  backgroundColor: Colors.red,
                  child: Text(
                    '${cart.itemCount}',
                    style: const TextStyle(fontSize: 10, color: Colors.white),
                  ),
                ),
              ),
          ],
        );
      },
    );
  }
}
```

### child 파라미터: 최적화

Consumer가 리빌드될 때 변경되지 않는 위젯은 `child`로 전달해서 재사용합니다.

```dart
Consumer<CartNotifier>(
  builder: (context, cart, child) {
    return Row(
      children: [
        child!, // 리빌드 안 됨
        Text('${cart.itemCount}개'),
      ],
    );
  },
  child: const Icon(Icons.shopping_cart), // 한 번만 빌드
)
```

---

<a id="part7"></a>
## 7️⃣ ⭐ **핵심** — context.read vs context.watch [↑](#toc)

### 두 가지 접근 방법

| 방법 | 리빌드 여부 | 사용 시점 |
|------|-----------|----------|
| `context.watch<T>()` | 변경 시 리빌드 | build() 안에서 UI 업데이트 필요 |
| `context.read<T>()` | 리빌드 안 함 | 이벤트 핸들러에서 메서드 호출 |

### context.watch — build() 안에서 사용

```dart
@override
Widget build(BuildContext context) {
  // notifyListeners()가 호출될 때마다 이 build()가 다시 실행됨
  final cart = context.watch<CartNotifier>();

  return Text('${cart.itemCount}개');
}
```

### context.read — 이벤트 핸들러에서 사용

```dart
ElevatedButton(
  onPressed: () {
    // 버튼을 탭할 때 한 번만 읽음 (리빌드 유발 안 함)
    context.read<CartNotifier>().addItem(item);
  },
  child: const Text('장바구니 담기'),
)
```

### 주의: build() 안에서 context.read 사용 금지

```dart
@override
Widget build(BuildContext context) {
  // ❌ 잘못된 사용: build()에서 read() 사용
  final count = context.read<CartNotifier>().itemCount;
  // 이렇게 하면 notifyListeners()가 호출돼도 UI가 안 바뀜

  // ✅ 올바른 사용: build()에서 watch() 사용
  final count = context.watch<CartNotifier>().itemCount;
}
```

### Selector: 특정 값만 감시

전체 CartNotifier를 감시하는 대신, 특정 값이 바뀔 때만 리빌드:

```dart
// itemCount가 바뀔 때만 리빌드
Selector<CartNotifier, int>(
  selector: (context, cart) => cart.itemCount,
  builder: (context, count, child) {
    return Text('$count개');
  },
)
```

---

<a id="part8"></a>
## 8️⃣ 🚀 **도전** — 실습: 장바구니 기능 [↑](#toc)

### 목표

두 화면이 장바구니 데이터를 공유합니다:
- **상품 목록 화면**: 상품 목록 + 장바구니 담기 버튼
- **장바구니 화면**: 담긴 상품 목록 + 총 금액 + 비우기

### 파일 구조

```
lib/
├── main.dart
├── models/
│   └── cart_item.dart
├── notifiers/
│   └── cart_notifier.dart
└── screens/
    ├── product_screen.dart
    └── cart_screen.dart
```

### Step 1: CartItem 모델

```dart
// lib/models/cart_item.dart
class CartItem {
  final String id;
  final String name;
  final double price;

  const CartItem({
    required this.id,
    required this.name,
    required this.price,
  });
}
```

### Step 2: CartNotifier

```dart
// lib/notifiers/cart_notifier.dart
import 'package:flutter/foundation.dart';
import '../models/cart_item.dart';

class CartNotifier extends ChangeNotifier {
  final List<CartItem> _items = [];

  List<CartItem> get items => List.unmodifiable(_items);
  int get itemCount => _items.length;
  double get total => _items.fold(0, (sum, item) => sum + item.price);

  bool containsItem(String id) => _items.any((item) => item.id == id);

  void addItem(CartItem item) {
    if (!containsItem(item.id)) {
      _items.add(item);
      notifyListeners();
    }
  }

  void removeItem(String id) {
    _items.removeWhere((item) => item.id == id);
    notifyListeners();
  }

  void clear() {
    _items.clear();
    notifyListeners();
  }
}
```

### Step 3: 상품 목록 화면

```dart
// lib/screens/product_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/cart_item.dart';
import '../notifiers/cart_notifier.dart';
import 'cart_screen.dart';

class ProductScreen extends StatelessWidget {
  const ProductScreen({super.key});

  static final List<CartItem> _products = [
    CartItem(id: '1', name: '아메리카노', price: 4500),
    CartItem(id: '2', name: '카페라떼', price: 5000),
    CartItem(id: '3', name: '바닐라라떼', price: 5500),
    CartItem(id: '4', name: '카라멜마끼아또', price: 6000),
    CartItem(id: '5', name: '에스프레소', price: 3500),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('메뉴'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          Stack(
            alignment: Alignment.topRight,
            children: [
              IconButton(
                icon: const Icon(Icons.shopping_cart),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const CartScreen()),
                  );
                },
              ),
              // 장바구니 개수 뱃지
              Consumer<CartNotifier>(
                builder: (context, cart, _) {
                  if (cart.itemCount == 0) return const SizedBox.shrink();
                  return Positioned(
                    right: 4,
                    top: 4,
                    child: CircleAvatar(
                      radius: 9,
                      backgroundColor: Colors.red,
                      child: Text(
                        '${cart.itemCount}',
                        style: const TextStyle(fontSize: 11, color: Colors.white),
                      ),
                    ),
                  );
                },
              ),
            ],
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: _products.length,
        itemBuilder: (context, index) {
          final product = _products[index];
          return Consumer<CartNotifier>(
            builder: (context, cart, _) {
              final inCart = cart.containsItem(product.id);
              return ListTile(
                title: Text(product.name),
                subtitle: Text('${product.price.toInt()}원'),
                trailing: IconButton(
                  icon: Icon(
                    inCart ? Icons.check_circle : Icons.add_circle_outline,
                    color: inCart ? Colors.green : Colors.blue,
                  ),
                  onPressed: () {
                    if (inCart) {
                      context.read<CartNotifier>().removeItem(product.id);
                    } else {
                      context.read<CartNotifier>().addItem(product);
                    }
                  },
                ),
              );
            },
          );
        },
      ),
    );
  }
}
```

### Step 4: 장바구니 화면

```dart
// lib/screens/cart_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../notifiers/cart_notifier.dart';

class CartScreen extends StatelessWidget {
  const CartScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('장바구니'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Consumer<CartNotifier>(
        builder: (context, cart, _) {
          if (cart.itemCount == 0) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.shopping_cart_outlined, size: 64, color: Colors.grey),
                  SizedBox(height: 16),
                  Text('장바구니가 비어있습니다', style: TextStyle(color: Colors.grey)),
                ],
              ),
            );
          }
          return Column(
            children: [
              Expanded(
                child: ListView.builder(
                  itemCount: cart.itemCount,
                  itemBuilder: (context, index) {
                    final item = cart.items[index];
                    return ListTile(
                      title: Text(item.name),
                      subtitle: Text('${item.price.toInt()}원'),
                      trailing: IconButton(
                        icon: const Icon(Icons.delete_outline, color: Colors.red),
                        onPressed: () {
                          context.read<CartNotifier>().removeItem(item.id);
                        },
                      ),
                    );
                  },
                ),
              ),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.surfaceVariant,
                  border: Border(top: BorderSide(color: Colors.grey.shade300)),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      '합계: ${cart.total.toInt()}원',
                      style: const TextStyle(
                          fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    ElevatedButton.icon(
                      onPressed: () {
                        context.read<CartNotifier>().clear();
                      },
                      icon: const Icon(Icons.delete_sweep),
                      label: const Text('비우기'),
                    ),
                  ],
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
```

### Step 5: main.dart

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'notifiers/cart_notifier.dart';
import 'screens/product_screen.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => CartNotifier(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '장바구니 앱',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      home: const ProductScreen(),
    );
  }
}
```

---

<a id="part9"></a>
## 9️⃣ 📖 **더 알아보기** — Riverpod 소개 [↑](#toc)

### Riverpod이란?

Provider의 제작자가 만든 **차세대 상태 관리 라이브러리**입니다.

| 비교 | Provider | Riverpod |
|------|----------|----------|
| 학습 난이도 | 낮음 | 중간 |
| BuildContext 의존 | 있음 | 없음 |
| 타입 안전성 | 보통 | 높음 |
| 테스트 용이성 | 보통 | 매우 높음 |
| 현업 사용 | 많음 | 증가 중 |

### 언제 Riverpod을 쓰나?

- 복잡한 상태 로직이 필요할 때
- 테스트 코드를 많이 작성할 때
- 팀 규모가 크고 코드 일관성이 중요할 때

> 이 교육과정에서는 Provider로 충분합니다. Riverpod은 실무에서 Flutter 앱을 계속 만들 때 공부하면 됩니다.

---

<a id="part10"></a>
## 🔟 정리 [↑](#toc)

### setState vs Provider 비교

| 상황 | setState | Provider |
|------|---------|---------|
| 같은 화면 내 상태 | ✅ 적합 | 불필요하게 복잡 |
| 여러 화면 공유 상태 | ❌ 불편 | ✅ 적합 |
| 전역 설정 (테마 등) | ❌ 불편 | ✅ 적합 |
| 학습 난이도 | 쉬움 | 중간 |

### Provider 핵심 패턴

```dart
// 1. 상태 클래스 정의
class MyNotifier extends ChangeNotifier {
  int _value = 0;
  int get value => _value;

  void increment() {
    _value++;
    notifyListeners();
  }
}

// 2. 앱 최상단에 제공
ChangeNotifierProvider(
  create: (_) => MyNotifier(),
  child: MyApp(),
)

// 3. UI에서 읽기 (build() 안)
final value = context.watch<MyNotifier>().value;

// 4. 이벤트에서 변경
context.read<MyNotifier>().increment();
```

### 다음 장 예고

다음 장부터는 **통합 프로젝트**를 시작합니다.  
지금까지 배운 모든 것 — API 호출, Custom Instructions, TDD — 을 하나의 앱으로 통합합니다.

---

→ **다음 내용으로 넘어갑시다**: [19. 통합 프로젝트 — 날씨 앱](/ai-native-flutter/weather-app)
