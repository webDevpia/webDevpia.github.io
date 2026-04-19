---
title: "12. 미니 프로젝트 — BMI 계산기"
layout: default
parent: AI-Native Flutter
nav_order: 14
permalink: /ai-native-flutter/bmi-calculator
---

# 12장. 미니 프로젝트 — BMI 계산기
{: .no_toc }

> **Phase 2** · 예상 시간: 150분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 생성 + 검증 모드**
> AI(Copilot)가 코드를 생성할 수 있습니다.
> 단, 반드시 생성된 코드를 **읽고, 이해하고, 테스트로 검증**해야 합니다.
> AI 코드를 이해 없이 복붙하는 것은 금지입니다.

## 학습 목표

- 요구사항을 자연어로 명확하게 작성할 수 있다
- 핵심 로직을 먼저 테스트로 검증하고 구현할 수 있다
- Flutter 화면 간 Navigator.push로 데이터를 전달할 수 있다
- AI가 생성한 코드를 체크리스트로 검증하고 수정할 수 있다

<a id="toc"></a>
## 진행 순서

1. [프로젝트 소개](#part1) — 무엇을 만드는가
2. [요구사항 작성하기](#part2) — AI-Native 개발의 첫 단계
3. [프로젝트 구조 만들기](#part3) — 파일 구조 준비
4. [핵심 로직부터 — 테스트 먼저](#part4) — 미니 TDD 경험
5. [UI 연결하기](#part5) — 화면 구성과 연결
6. [검증하고 개선하기](#part6) — Bug Hunt 체크리스트
7. [Phase 2 관문](#part7) — 자기 점검 체크리스트
8. [정리](#part8)

---

<a id="part1"></a>
## 1️⃣ 프로젝트 소개 [↑](#toc)

이 장은 Phase 2의 **최종 관문**입니다. 지금까지 배운 모든 것을 하나의 프로젝트에 담습니다.

- 레이아웃 — Row, Column, Expanded (08장)
- 상태 관리 — StatefulWidget + setState (09장)
- AI 도구 — Copilot 생성 + 검증 (10장)
- 사용자 입력 — TextField + Form (11장)

그리고 이번 장에서 처음 배우는:
- 화면 전환 — Navigator.push

### 우리가 만들 것: BMI 계산기 앱

```
화면 1 (입력 화면)          화면 2 (결과 화면)
┌────────────────┐          ┌────────────────┐
│   BMI 계산기    │  →       │   결과 화면     │
│               │  계산     │               │
│  키: [_____]  │  버튼     │   BMI: 22.5   │
│               │          │               │
│  몸무게:[___] │          │   정상 체중    │
│               │          │   ████████░░  │
│  [  계산하기  ] │          │               │
│               │          │   [다시 계산]   │
└────────────────┘          └────────────────┘
```

### AI-Native 협업 흐름

| 여러분 | AI (Copilot) |
|--------|--------------|
| 요구사항 작성 | 코드 생성 |
| 테스트 작성 | 구현 코드 생성 |
| 코드 읽고 설명하기 | UI 연결 코드 생성 |
| 버그 찾고 수정하기 | 수정 제안 |

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — 요구사항 작성하기 [↑](#toc)

> 강사와 함께 요구사항을 작성해 봅시다

AI-Native 개발의 첫 단계는 **무엇을 만들지 명확하게 쓰는 것**입니다.

> 건축가가 설계도 없이 집을 짓지 않듯이,
> AI-Native 개발자는 요구사항 없이 AI에게 코드를 요청하지 않습니다.

### 기능 요구사항

```
기능 요구사항:
1. 키(cm)와 몸무게(kg)를 입력받는다
2. "계산하기" 버튼을 누르면 BMI를 계산한다
3. 결과 화면에서 BMI 수치와 등급을 표시한다
   - 저체중: BMI < 18.5
   - 정상:   18.5 <= BMI < 23.0
   - 과체중: 23.0 <= BMI < 25.0
   - 비만:   BMI >= 25.0
4. 등급에 따라 색상이 다르다
   (파랑: 저체중, 초록: 정상, 주황: 과체중, 빨강: 비만)
5. "다시 계산" 버튼으로 입력 화면으로 돌아간다
```

### 제약 조건

```
제약 조건:
- BMI 계산 로직은 순수 Dart 함수로 분리한다 (lib/utils/bmi_calculator.dart)
- 핵심 로직은 Flutter test로 먼저 검증한다
- 빈 입력이나 0 이하 값은 에러 처리한다
- AI 생성 코드는 반드시 Bug Hunt 체크리스트를 통과해야 한다
```

### 나쁜 요구사항 vs 좋은 요구사항

**나쁜 요구사항:**
```
BMI 앱 만들어줘
```

**좋은 요구사항:**
```
Flutter 앱으로 BMI 계산기를 만들어줘.

화면 구성:
- 입력 화면: 키(cm), 몸무게(kg) TextField + 계산 버튼
- 결과 화면: BMI 수치, 등급 텍스트, 색상 표시, 다시 계산 버튼

BMI 계산 로직 (lib/utils/bmi_calculator.dart에 분리):
- calculateBMI(double heightCm, double weightKg) → double
- getBmiGrade(double bmi) → String

등급 기준:
- BMI < 18.5: "저체중"
- 18.5 <= BMI < 23.0: "정상"
- 23.0 <= BMI < 25.0: "과체중"
- BMI >= 25.0: "비만"
```

---

<a id="part3"></a>
## 3️⃣ 프로젝트 구조 만들기 [↑](#toc)

새 Flutter 프로젝트를 만들고 파일 구조를 준비합니다.

```bash
# 새 Flutter 프로젝트 생성
flutter create bmi_calculator
cd bmi_calculator
```

### 최종 파일 구조

```
bmi_calculator/
├── lib/
│   ├── main.dart                       ← 앱 시작점
│   ├── screens/
│   │   ├── input_screen.dart           ← 입력 화면
│   │   └── result_screen.dart          ← 결과 화면
│   └── utils/
│       └── bmi_calculator.dart         ← 순수 Dart 로직
├── test/
│   └── bmi_calculator_test.dart        ← 테스트 파일
└── pubspec.yaml
```

### 폴더 만들기

```bash
# bmi_calculator 프로젝트 안에서
mkdir -p lib/screens lib/utils
```

### main.dart 준비

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'screens/input_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BMI 계산기',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const InputScreen(),
    );
  }
}
```

---

<a id="part4"></a>
## 4️⃣ ⭐ **핵심** — 테스트 먼저 작성하기 [↑](#toc)

> 실제 기능을 만들기 전에 **테스트를 먼저** 작성합니다.
> 이것이 TDD(테스트 주도 개발)의 핵심입니다.

### 테스트 파일 작성

`test/bmi_calculator_test.dart`를 만들고 직접 작성하세요:

```dart
// test/bmi_calculator_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:bmi_calculator/utils/bmi_calculator.dart';

void main() {
  group('calculateBMI', () {
    test('정상 체중 BMI 계산', () {
      // 키 170cm, 몸무게 65kg → BMI = 65 / (1.7 * 1.7) = 22.49...
      final bmi = calculateBMI(170, 65);
      expect(bmi, closeTo(22.49, 0.01));
    });

    test('저체중 BMI 계산', () {
      // 키 170cm, 몸무게 50kg → BMI = 50 / (1.7 * 1.7) = 17.30...
      final bmi = calculateBMI(170, 50);
      expect(bmi, closeTo(17.30, 0.01));
    });

    test('비만 BMI 계산', () {
      // 키 160cm, 몸무게 80kg → BMI = 80 / (1.6 * 1.6) = 31.25
      final bmi = calculateBMI(160, 80);
      expect(bmi, closeTo(31.25, 0.01));
    });

    test('키 0 입력 시 에러', () {
      expect(() => calculateBMI(0, 65), throwsArgumentError);
    });

    test('몸무게 0 입력 시 에러', () {
      expect(() => calculateBMI(170, 0), throwsArgumentError);
    });

    test('음수 입력 시 에러', () {
      expect(() => calculateBMI(-170, 65), throwsArgumentError);
    });
  });

  group('getBmiGrade', () {
    test('저체중 판정 (BMI 17.0)', () {
      expect(getBmiGrade(17.0), '저체중');
    });

    test('정상 판정 (BMI 22.0)', () {
      expect(getBmiGrade(22.0), '정상');
    });

    test('과체중 판정 (BMI 24.0)', () {
      expect(getBmiGrade(24.0), '과체중');
    });

    test('비만 판정 (BMI 30.0)', () {
      expect(getBmiGrade(30.0), '비만');
    });

    test('경계값 — BMI 18.5는 정상', () {
      expect(getBmiGrade(18.5), '정상');
    });

    test('경계값 — BMI 23.0은 과체중', () {
      expect(getBmiGrade(23.0), '과체중');
    });
  });
}
```

### 테스트 먼저 실행 (빨간 상태 확인)

```bash
flutter test
```

아직 `bmi_calculator.dart`가 없으니 오류가 납니다. 이게 정상입니다!

```
❌ Error: Cannot find 'bmi_calculator.dart'
→ 이제 이 테스트를 통과시키는 코드를 작성합니다
```

### Copilot에게 구현 요청

```
다음 테스트를 통과하는 Dart 함수를 작성해줘.
파일: lib/utils/bmi_calculator.dart

함수 1: calculateBMI(double heightCm, double weightKg) → double
  - BMI = 몸무게(kg) / (키(m) * 키(m))
  - 키와 몸무게가 0 이하면 ArgumentError 던지기
  - 소수점 2자리로 반올림

함수 2: getBmiGrade(double bmi) → String
  - BMI < 18.5: "저체중"
  - 18.5 <= BMI < 23.0: "정상"
  - 23.0 <= BMI < 25.0: "과체중"
  - BMI >= 25.0: "비만"
```

### AI가 생성한 코드 (검증 후)

```dart
// lib/utils/bmi_calculator.dart

/// BMI를 계산합니다.
///
/// [heightCm]: 키 (cm 단위)
/// [weightKg]: 몸무게 (kg 단위)
///
/// BMI = 몸무게(kg) / (키(m) ^ 2)
double calculateBMI(double heightCm, double weightKg) {
  if (heightCm <= 0) {
    throw ArgumentError('키는 0보다 커야 합니다: $heightCm');
  }
  if (weightKg <= 0) {
    throw ArgumentError('몸무게는 0보다 커야 합니다: $weightKg');
  }

  final heightM = heightCm / 100;
  final bmi = weightKg / (heightM * heightM);

  // 소수점 2자리로 반올림
  return double.parse(bmi.toStringAsFixed(2));
}

/// BMI 등급을 반환합니다.
///
/// - 저체중: BMI < 18.5
/// - 정상:   18.5 <= BMI < 23.0
/// - 과체중: 23.0 <= BMI < 25.0
/// - 비만:   BMI >= 25.0
String getBmiGrade(double bmi) {
  if (bmi < 18.5) return '저체중';
  if (bmi < 23.0) return '정상';
  if (bmi < 25.0) return '과체중';
  return '비만';
}
```

### 테스트 다시 실행 (초록 상태 확인)

```bash
flutter test
```

```
✅ All tests passed!
  calculateBMI ✓ 정상 체중 BMI 계산
  calculateBMI ✓ 저체중 BMI 계산
  calculateBMI ✓ 비만 BMI 계산
  calculateBMI ✓ 키 0 입력 시 에러
  calculateBMI ✓ 몸무게 0 입력 시 에러
  calculateBMI ✓ 음수 입력 시 에러
  getBmiGrade  ✓ 저체중 판정
  ...
```

모든 테스트가 통과했습니다. 이제 UI를 만들 준비가 되었습니다.

---

<a id="part5"></a>
## 5️⃣ ⭐ **핵심** — UI 연결하기 [↑](#toc)

### 입력 화면 만들기

Copilot에게 요청하거나 직접 작성하세요:

```dart
// lib/screens/input_screen.dart
import 'package:flutter/material.dart';
import '../utils/bmi_calculator.dart';
import 'result_screen.dart';

class InputScreen extends StatefulWidget {
  const InputScreen({super.key});

  @override
  State<InputScreen> createState() => _InputScreenState();
}

class _InputScreenState extends State<InputScreen> {
  final _formKey = GlobalKey<FormState>();
  final _heightController = TextEditingController();
  final _weightController = TextEditingController();

  @override
  void dispose() {
    _heightController.dispose();
    _weightController.dispose();
    super.dispose();
  }

  void _calculate() {
    if (_formKey.currentState!.validate()) {
      final height = double.parse(_heightController.text);
      final weight = double.parse(_weightController.text);
      final bmi = calculateBMI(height, weight);
      final grade = getBmiGrade(bmi);

      // 결과 화면으로 이동 (데이터 전달)
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ResultScreen(
            bmi: bmi,
            grade: grade,
            height: height,
            weight: weight,
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text('BMI 계산기'),
        centerTitle: true,
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(32),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 32),

              // 아이콘 및 제목
              const Icon(Icons.monitor_weight, size: 80, color: Colors.blue),
              const SizedBox(height: 16),
              const Text(
                '나의 BMI를 계산해보세요',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 18, color: Colors.grey),
              ),
              const SizedBox(height: 48),

              // 키 입력
              TextFormField(
                controller: _heightController,
                keyboardType:
                    const TextInputType.numberWithOptions(decimal: true),
                decoration: InputDecoration(
                  labelText: '키 (cm)',
                  hintText: '예: 170',
                  prefixIcon: const Icon(Icons.height),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  suffixText: 'cm',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '키를 입력해주세요';
                  }
                  final height = double.tryParse(value);
                  if (height == null) {
                    return '올바른 숫자를 입력해주세요';
                  }
                  if (height <= 0 || height > 300) {
                    return '50 ~ 300 사이의 값을 입력해주세요';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),

              // 몸무게 입력
              TextFormField(
                controller: _weightController,
                keyboardType:
                    const TextInputType.numberWithOptions(decimal: true),
                decoration: InputDecoration(
                  labelText: '몸무게 (kg)',
                  hintText: '예: 65',
                  prefixIcon: const Icon(Icons.fitness_center),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  suffixText: 'kg',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '몸무게를 입력해주세요';
                  }
                  final weight = double.tryParse(value);
                  if (weight == null) {
                    return '올바른 숫자를 입력해주세요';
                  }
                  if (weight <= 0 || weight > 500) {
                    return '1 ~ 500 사이의 값을 입력해주세요';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 40),

              // 계산 버튼
              ElevatedButton(
                onPressed: _calculate,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 18),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text(
                  '계산하기',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
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

### 결과 화면 만들기

```dart
// lib/screens/result_screen.dart
import 'package:flutter/material.dart';

class ResultScreen extends StatelessWidget {
  final double bmi;
  final String grade;
  final double height;
  final double weight;

  const ResultScreen({
    super.key,
    required this.bmi,
    required this.grade,
    required this.height,
    required this.weight,
  });

  Color get _gradeColor {
    switch (grade) {
      case '저체중':
        return Colors.blue;
      case '정상':
        return Colors.green;
      case '과체중':
        return Colors.orange;
      case '비만':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  String get _gradeMessage {
    switch (grade) {
      case '저체중':
        return '체중이 약간 부족합니다.\n균형 잡힌 식사가 필요해요.';
      case '정상':
        return '건강한 체중 범위입니다!\n지금처럼 유지하세요.';
      case '과체중':
        return '체중이 약간 높습니다.\n규칙적인 운동을 권장해요.';
      case '비만':
        return '건강 관리가 필요합니다.\n전문가 상담을 권장해요.';
      default:
        return '';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text('결과'),
        centerTitle: true,
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(32),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: 32),

            // BMI 수치 표시
            Container(
              padding: const EdgeInsets.all(32),
              decoration: BoxDecoration(
                color: _gradeColor.withOpacity(0.1),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: _gradeColor, width: 2),
              ),
              child: Column(
                children: [
                  Text(
                    bmi.toStringAsFixed(1),
                    style: TextStyle(
                      fontSize: 72,
                      fontWeight: FontWeight.bold,
                      color: _gradeColor,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    grade,
                    style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.w600,
                      color: _gradeColor,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // BMI 게이지 바
            _buildGaugeBar(),
            const SizedBox(height: 24),

            // 메시지
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.grey[50],
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                _gradeMessage,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 16, height: 1.6),
              ),
            ),
            const SizedBox(height: 24),

            // 입력값 요약
            Row(
              children: [
                Expanded(child: _buildInfoCard('키', '${height.toStringAsFixed(1)} cm')),
                const SizedBox(width: 12),
                Expanded(child: _buildInfoCard('몸무게', '${weight.toStringAsFixed(1)} kg')),
              ],
            ),
            const SizedBox(height: 40),

            // 다시 계산 버튼
            OutlinedButton(
              onPressed: () => Navigator.pop(context),
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 18),
                side: const BorderSide(color: Colors.blue, width: 2),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: const Text(
                '다시 계산하기',
                style: TextStyle(fontSize: 18, color: Colors.blue),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildGaugeBar() {
    // BMI 범위: 15 ~ 35 사이에서 현재 BMI 위치 계산
    final position = ((bmi - 15) / (35 - 15)).clamp(0.0, 1.0);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('BMI 범위', style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        Stack(
          children: [
            // 배경 게이지 (4색 그라데이션)
            Container(
              height: 20,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(10),
                gradient: const LinearGradient(
                  colors: [Colors.blue, Colors.green, Colors.orange, Colors.red],
                ),
              ),
            ),
            // 현재 위치 표시
            Positioned(
              left: (position * 280).clamp(0, 280),
              top: 0,
              child: Container(
                width: 20,
                height: 20,
                decoration: BoxDecoration(
                  color: Colors.white,
                  shape: BoxShape.circle,
                  border: Border.all(color: _gradeColor, width: 3),
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 4),
        const Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text('저체중', style: TextStyle(fontSize: 11, color: Colors.blue)),
            Text('정상', style: TextStyle(fontSize: 11, color: Colors.green)),
            Text('과체중', style: TextStyle(fontSize: 11, color: Colors.orange)),
            Text('비만', style: TextStyle(fontSize: 11, color: Colors.red)),
          ],
        ),
      ],
    );
  }

  Widget _buildInfoCard(String label, String value) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: [
          Text(label, style: TextStyle(color: Colors.grey[600], fontSize: 13)),
          const SizedBox(height: 4),
          Text(
            value,
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }
}
```

### 실행 및 확인

```bash
flutter run
```

1. 키 170, 몸무게 65 입력 → "계산하기" 클릭
2. 결과 화면에서 BMI 22.5, "정상" 표시 확인
3. "다시 계산하기"로 돌아오는지 확인

---

<a id="part6"></a>
## 6️⃣ 🚀 **도전** — Bug Hunt 체크리스트 적용 [↑](#toc)

AI가 생성한 코드 전체에 다음 체크리스트를 적용하세요.

### Flutter Bug Hunt 체크리스트

```
□ 1. dispose() 확인
   - _heightController.dispose() ← 있는가?
   - _weightController.dispose() ← 있는가?
   - super.dispose() 마지막에 있는가?

□ 2. const 최적화
   - 변하지 않는 위젯에 const 붙어 있는가?
   - InputDecoration에 const 사용 불가한 경우 명확한가?
     (suffixText, suffixIcon이 동적이면 const 불가)

□ 3. null safety
   - double.tryParse 결과 null 체크 완료?
   - Navigator.push의 context 유효성 (BuildContext 사용 주의)

□ 4. 경계값 처리
   - 키 0, 몸무게 0 입력 시 어떻게 되는가?
   - 매우 큰 값(키 999, 몸무게 999) 입력 시 어떻게 되는가?
   - validator에서 범위 체크가 있는가?

□ 5. 위젯 분리
   - _buildGaugeBar(), _buildInfoCard() 로 적절히 분리됨

□ 6. 에러 메시지
   - 사용자가 이해할 수 있는 메시지인가?
   - "올바른 숫자를 입력해주세요" (O)
   - "Invalid input" (X)
```

### 발견한 버그 수정 실습

다음 시나리오를 직접 테스트하고 버그를 찾아보세요:

```
시나리오 1: 키 필드에 "abc" 입력 후 계산
  → 예상: "올바른 숫자를 입력해주세요" 에러
  → 실제: ?

시나리오 2: 키 0 입력 후 계산
  → 예상: "50 ~ 300 사이의 값" 에러
  → 실제: ?

시나리오 3: 두 필드 모두 비운 채 계산
  → 예상: 두 에러 메시지 모두 표시
  → 실제: ?
```

---

<a id="part7"></a>
## 7️⃣ Phase 2 관문 — 자기 점검 체크리스트 [↑](#toc)

> 솔직하게 체크해 보세요. 모든 항목을 스스로 통과해야 Phase 3로 갑니다.

### 레이아웃 (08장)

```
□ Row와 Column 안에서 Expanded로 공간을 나눌 수 있다
□ Stack과 Positioned로 위젯을 겹칠 수 있다
□ EdgeInsets.all, symmetric, only, fromLTRB의 차이를 안다
```

### 상태 관리 (09장)

```
□ StatefulWidget 구조(2개 클래스)를 외워서 쓸 수 있다
□ setState() 없이 상태를 변경하면 화면이 안 바뀌는 이유를 설명할 수 있다
□ 투표 앱(좋아요/싫어요)을 처음부터 혼자 만들 수 있다
```

### AI 도구 (10장)

```
□ GitHub Copilot의 인라인 제안을 Tab으로 수락할 수 있다
□ AI 코드 평가 체크리스트 7가지를 외우지 않아도 적용할 수 있다
□ Bug Hunt에서 setState 누락, dispose 누락을 찾을 수 있다
```

### 폼 (11장)

```
□ TextEditingController를 생성, 사용, dispose 하는 흐름을 안다
□ Form + GlobalKey + TextFormField + validator 조합을 쓸 수 있다
□ 이메일, 비밀번호, 비밀번호 확인 validator를 직접 작성할 수 있다
```

### 미니 프로젝트 (12장)

```
□ 요구사항 → 테스트 → 구현 → 검증 순서를 이해한다
□ BMI 계산기를 처음부터 혼자 다시 만들 수 있다
□ Navigator.push로 화면을 전환하고 데이터를 전달할 수 있다
```

### Phase 2 완주 선언

모든 항목에 체크했다면 다음 문장을 완성해 보세요:

```
나는 Flutter로 ________________(앱 이름)을 만들 수 있다.
이 앱은 ________ 화면이 있고,
________와 ________를 사용해 상태를 관리하며,
________ 로직을 별도로 분리해서 테스트한다.
```

---

<a id="part8"></a>
## 8️⃣ 정리 [↑](#toc)

### Phase 2 에서 배운 것

| 장 | 핵심 내용 |
|----|-----------|
| 08장 | Row, Column, Expanded, Stack으로 복잡한 레이아웃 구성 |
| 09장 | StatefulWidget + setState로 상태 변화 화면 구현 |
| 10장 | Copilot 설치, AI 코드 평가 체크리스트, Bug Hunt |
| 11장 | TextField, Form, validator로 입력 처리 |
| 12장 | 요구사항 → 테스트 → AI생성 → 검증 미니 TDD 흐름 |

### AI-Native 개발자 선언

> Phase 2를 완주한 여러분은 이제:
>
> 1. AI에게 **명확한 요구사항**을 줄 수 있습니다
> 2. AI 코드를 **읽고 이해**할 수 있습니다
> 3. AI 코드를 **테스트로 검증**할 수 있습니다
> 4. AI 코드의 **버그를 찾고 수정**할 수 있습니다
>
> 이것이 AI를 도구로 사용하는 개발자와
> AI에게 끌려다니는 사용자의 차이입니다.

### 다음 장 예고

다음 장(13장)에서는 **네비게이션과 라우팅**을 배웁니다.
Named Routes, 화면 간 데이터 전달, BottomNavigationBar를 배우고
진짜 앱다운 다중 화면 앱을 만들어봅니다!

---

> **혼자 해보기**: 이 BMI 계산기에 다음 기능 중 하나를 추가해보세요.
> 1. BMI 계산 기록을 리스트로 보여주기 (List 상태)
> 2. 이상적인 몸무게 범위 계산하여 표시
> 3. 키/몸무게 단위 전환 (cm ↔ ft/in, kg ↔ lb)
