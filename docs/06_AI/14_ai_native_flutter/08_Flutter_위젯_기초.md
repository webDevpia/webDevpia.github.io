---
title: "07. Flutter 위젯 기초"
layout: default
parent: AI-Native Flutter
nav_order: 9
permalink: /ai-native-flutter/widgets-basics
---

# 7장. Flutter 위젯 기초
{: .no_toc }

> **Phase 1** · 예상 시간: 120분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 설명 모드만**
> 위젯의 속성이 궁금할 때 AI에게 설명을 요청할 수 있습니다. 하지만 실습 앱의 코드는 직접 작성하세요. 이 장을 마치면 Phase 1이 완료됩니다!

## 학습 목표
- Flutter의 "모든 것은 위젯" 철학을 설명할 수 있다
- `Text`, `Container`, `Icon`, `Image`, `Button` 위젯을 사용할 수 있다
- 위젯 트리(부모-자식) 구조를 그림으로 설명할 수 있다
- 나만의 자기소개 카드 앱을 완성할 수 있다

<a id="toc"></a>
## 진행 순서
1. [위젯이란? — 레고 블록 비유](#part1)
2. ["모든 것은 위젯이다"](#part2)
3. [MaterialApp, Scaffold, AppBar — 앱의 뼈대](#part3)
4. [Text 위젯](#part4)
5. [Container 위젯](#part5)
6. [Icon 위젯](#part6)
7. [Image 위젯](#part7)
8. [ElevatedButton, TextButton](#part8)
9. [위젯 트리 이해하기](#part9)
10. [실습: 자기소개 카드 앱](#part10)
11. [정리 — Phase 1 완주!](#part11)

---

<a id="part1"></a>
## 1️⃣ ⭐ **핵심** — 위젯이란? [↑](#toc)

### 레고 블록 비유

Flutter 앱은 **위젯(Widget)**들을 조립해서 만듭니다. 마치 레고처럼요.

```
🟦 Text 위젯 — 글자를 보여주는 블록
🟩 Container 위젯 — 공간을 차지하는 상자 블록
🟨 Row 위젯 — 블록들을 가로로 나열하는 블록
🟧 Column 위젯 — 블록들을 세로로 나열하는 블록
🟥 ElevatedButton 위젯 — 누를 수 있는 버튼 블록
```

레고 블록을 쌓아서 성을 만들듯이, 위젯들을 조합해서 앱 화면을 만듭니다.

### 위젯의 두 종류

| 종류 | 설명 | 예시 |
|------|------|------|
| **StatelessWidget** | 상태가 없는 위젯 — 화면이 고정됨 | Text, Icon, Image |
| **StatefulWidget** | 상태가 있는 위젯 — 화면이 변함 | Checkbox, TextField, 카운터 |

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — "모든 것은 위젯이다" [↑](#toc)

Flutter의 핵심 철학입니다. 눈에 보이는 것뿐만 아니라, **보이지 않는 것도 전부 위젯**입니다.

```
눈에 보이는 위젯:          눈에 안 보이는 위젯:
- Text                    - Padding (여백)
- Icon                    - Center (가운데 정렬)
- Image                   - Column (세로 배치)
- ElevatedButton          - Row (가로 배치)
- AppBar                  - Expanded (공간 채우기)
```

### 실제 코드에서 확인하기

```dart
Padding(                    // 위젯 1: 여백을 주는 위젯
  padding: EdgeInsets.all(16),
  child: Column(            // 위젯 2: 세로로 배치하는 위젯
    children: [
      Text('안녕하세요'),    // 위젯 3: 텍스트를 보여주는 위젯
      Icon(Icons.star),     // 위젯 4: 아이콘을 보여주는 위젯
    ],
  ),
)
```

화면에 텍스트와 아이콘이 보이지만, 실제로는 Padding, Column, Text, Icon 4개의 위젯이 조합되어 있습니다.

---

<a id="part3"></a>
## 3️⃣ ⭐ **핵심** — MaterialApp, Scaffold, AppBar [↑](#toc)

### 앱의 뼈대 구조

Flutter 앱은 항상 이 기본 구조로 시작합니다:

```dart
MaterialApp          // 앱 전체 설정 (테마, 라우팅)
  └── Scaffold       // 화면의 기본 레이아웃
        ├── AppBar   // 상단 바
        ├── body     // 화면 중앙 내용
        └── floatingActionButton  // 오른쪽 하단 버튼
```

> **비유**: 
> - `MaterialApp` = 건물 전체
> - `Scaffold` = 건물 안 특정 층(방)
> - `AppBar` = 방의 천장/간판
> - `body` = 방의 내부 공간

### MaterialApp 주요 속성

```dart
MaterialApp(
  title: '앱 이름',          // 앱 전환 시 표시되는 이름
  theme: ThemeData(          // 전체 테마 설정
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.blue,
    ),
    useMaterial3: true,
  ),
  home: MyHomePage(),        // 첫 화면
  debugShowCheckedModeBanner: false,  // 디버그 배너 숨기기
)
```

### Scaffold 주요 속성

```dart
Scaffold(
  appBar: AppBar(            // 상단 바
    title: const Text('제목'),
    actions: [               // 오른쪽 버튼들
      IconButton(
        icon: const Icon(Icons.search),
        onPressed: () {},
      ),
    ],
  ),
  body: const Center(        // 화면 내용
    child: Text('본문'),
  ),
  floatingActionButton: FloatingActionButton(  // FAB 버튼
    onPressed: () {},
    child: const Icon(Icons.add),
  ),
  bottomNavigationBar: BottomNavigationBar(    // 하단 탭 바
    items: const [
      BottomNavigationBarItem(icon: Icon(Icons.home), label: '홈'),
      BottomNavigationBarItem(icon: Icon(Icons.person), label: '프로필'),
    ],
    currentIndex: 0,
    onTap: (index) {},
  ),
)
```

---

<a id="part4"></a>
## 4️⃣ ⭐ **핵심** — Text 위젯 [↑](#toc)

### 기본 사용

```dart
// 가장 단순한 사용
const Text('안녕하세요')

// 스타일 적용
Text(
  '안녕하세요, Flutter!',
  style: TextStyle(
    fontSize: 24,              // 글자 크기
    fontWeight: FontWeight.bold,  // 굵기
    color: Colors.blue,        // 색상
    fontStyle: FontStyle.italic,  // 기울임
    letterSpacing: 2.0,        // 자간
    decoration: TextDecoration.underline,  // 밑줄
  ),
)
```

### 텍스트 정렬과 오버플로우

```dart
Text(
  '긴 텍스트가 화면을 벗어날 때 어떻게 처리할지 설정합니다.',
  textAlign: TextAlign.center,  // 가운데 정렬
  maxLines: 2,                   // 최대 줄 수
  overflow: TextOverflow.ellipsis,  // 넘치면 ... 처리
)
```

### Theme 텍스트 스타일 사용

```dart
// 앱 테마에서 미리 정의된 스타일 사용
Text(
  '제목',
  style: Theme.of(context).textTheme.headlineLarge,
)

Text(
  '소제목',
  style: Theme.of(context).textTheme.titleMedium,
)

Text(
  '본문',
  style: Theme.of(context).textTheme.bodyMedium,
)
```

---

<a id="part5"></a>
## 5️⃣ ⭐ **핵심** — Container 위젯 [↑](#toc)

### Container = 만능 상자

Container는 **모든 것을 담을 수 있는 상자** 위젯입니다. 크기, 색상, 여백, 테두리, 그림자 등을 설정할 수 있습니다.

```dart
Container(
  width: 200,           // 가로 크기
  height: 100,          // 세로 크기
  padding: const EdgeInsets.all(16),     // 내부 여백 (내용물과 테두리 사이)
  margin: const EdgeInsets.all(8),       // 외부 여백 (다른 위젯과의 거리)
  decoration: BoxDecoration(
    color: Colors.blue,                  // 배경색
    borderRadius: BorderRadius.circular(12),  // 모서리 둥글게
    boxShadow: [
      BoxShadow(
        color: Colors.black26,
        blurRadius: 8,
        offset: const Offset(0, 4),
      ),
    ],
    border: Border.all(                  // 테두리
      color: Colors.blueAccent,
      width: 2,
    ),
  ),
  child: const Text(
    '상자 안 텍스트',
    style: TextStyle(color: Colors.white),
  ),
)
```

### padding vs margin 차이

```
┌───────────────────────────────┐
│           margin              │
│   ┌───────────────────────┐   │
│   │       padding         │   │
│   │   ┌───────────────┐   │   │
│   │   │   자식 위젯    │   │   │
│   │   └───────────────┘   │   │
│   └───────────────────────┘   │
└───────────────────────────────┘
```

- **padding**: Container 안쪽 여백 (내용물 ↔ 테두리)
- **margin**: Container 바깥쪽 여백 (테두리 ↔ 다른 위젯)

### SizedBox — 크기만 지정하는 간단한 위젯

```dart
// 수직 간격 주기
const SizedBox(height: 16)

// 수평 간격 주기
const SizedBox(width: 8)

// 고정 크기 상자
SizedBox(
  width: 100,
  height: 50,
  child: Text('내용'),
)
```

---

<a id="part6"></a>
## 6️⃣ ⭐ **핵심** — Icon 위젯 [↑](#toc)

### Material Icons 사용하기

Flutter에는 수천 개의 아이콘이 내장되어 있습니다.

```dart
// 기본 아이콘
const Icon(Icons.home)
const Icon(Icons.search)
const Icon(Icons.favorite)
const Icon(Icons.star)

// 크기와 색상 변경
Icon(
  Icons.favorite,
  size: 48,
  color: Colors.red,
)

// 아이콘 버튼
IconButton(
  icon: const Icon(Icons.edit),
  onPressed: () {
    print('편집 버튼 클릭');
  },
  tooltip: '편집',  // 길게 누르면 나타나는 설명
)
```

### 자주 쓰는 아이콘들

| 아이콘 | 코드 |
|--------|------|
| 홈 | `Icons.home` |
| 검색 | `Icons.search` |
| 설정 | `Icons.settings` |
| 하트 | `Icons.favorite` |
| 별 | `Icons.star` |
| 사람 | `Icons.person` |
| 카메라 | `Icons.camera_alt` |
| 위치 | `Icons.location_on` |
| 전화 | `Icons.phone` |
| 이메일 | `Icons.email` |
| 추가 | `Icons.add` |
| 삭제 | `Icons.delete` |
| 편집 | `Icons.edit` |
| 공유 | `Icons.share` |

모든 아이콘: [fonts.google.com/icons](https://fonts.google.com/icons)

---

<a id="part7"></a>
## 7️⃣ 📖 **더 알아보기** — Image 위젯 [↑](#toc)

### 네트워크 이미지

```dart
Image.network(
  'https://placehold.co/200x300',  // 이미지 URL
  width: 200,
  height: 300,
  fit: BoxFit.cover,               // 이미지 크기 맞추기 방식
  loadingBuilder: (context, child, loadingProgress) {
    if (loadingProgress == null) return child;  // 로딩 완료
    return const CircularProgressIndicator();   // 로딩 중
  },
  errorBuilder: (context, error, stackTrace) {
    return const Icon(Icons.broken_image, size: 100);  // 오류 시
  },
)
```

### BoxFit 옵션

| 옵션 | 설명 |
|------|------|
| `BoxFit.cover` | 비율 유지, 빈 공간 없이 채움 (잘릴 수 있음) |
| `BoxFit.contain` | 비율 유지, 전체 이미지 표시 (빈 공간 생길 수 있음) |
| `BoxFit.fill` | 비율 무시, 지정 크기에 꽉 채움 |
| `BoxFit.fitWidth` | 가로 기준으로 맞춤 |
| `BoxFit.fitHeight` | 세로 기준으로 맞춤 |

### CircleAvatar — 원형 이미지

```dart
// 네트워크 이미지로
CircleAvatar(
  radius: 40,
  backgroundImage: NetworkImage('https://placehold.co/100'),
)

// 아이콘으로
CircleAvatar(
  radius: 40,
  backgroundColor: Colors.blue,
  child: const Icon(Icons.person, size: 50, color: Colors.white),
)

// 이니셜로
CircleAvatar(
  radius: 40,
  backgroundColor: Colors.green,
  child: const Text(
    '김',
    style: TextStyle(fontSize: 24, color: Colors.white),
  ),
)
```

---

<a id="part8"></a>
## 8️⃣ ⭐ **핵심** — 버튼 위젯 [↑](#toc)

### ElevatedButton — 입체 버튼

```dart
ElevatedButton(
  onPressed: () {
    print('ElevatedButton 클릭!');
  },
  style: ElevatedButton.styleFrom(
    backgroundColor: Colors.blue,   // 배경색
    foregroundColor: Colors.white,  // 텍스트/아이콘 색
    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(8),
    ),
  ),
  child: const Text('클릭하세요'),
)

// 아이콘과 함께
ElevatedButton.icon(
  onPressed: () {},
  icon: const Icon(Icons.send),
  label: const Text('전송'),
)
```

### TextButton — 텍스트만 있는 버튼

```dart
TextButton(
  onPressed: () {},
  child: const Text('더 보기'),
)
```

### OutlinedButton — 테두리 버튼

```dart
OutlinedButton(
  onPressed: () {},
  child: const Text('취소'),
)
```

### 버튼 비교

```dart
Column(
  children: [
    ElevatedButton(    // 입체감 있는 주요 버튼
      onPressed: () {},
      child: const Text('저장'),
    ),
    OutlinedButton(    // 테두리만 있는 보조 버튼
      onPressed: () {},
      child: const Text('취소'),
    ),
    TextButton(        // 텍스트만 있는 최소 버튼
      onPressed: () {},
      child: const Text('더 보기'),
    ),
  ],
)
```

---

<a id="part9"></a>
## 9️⃣ ⭐ **핵심** — 위젯 트리 이해하기 [↑](#toc)

### 위젯 트리란?

Flutter의 화면은 **나무(Tree) 구조**로 되어 있습니다. 하나의 위젯이 다른 위젯들을 자식으로 가집니다.

```
MaterialApp
└── Scaffold
    ├── AppBar
    │   └── Text('제목')
    └── body
        └── Center
            └── Column
                ├── CircleAvatar
                ├── Text('이름')
                └── ElevatedButton
                    └── Text('클릭')
```

### 실제 코드와 트리 대응

```dart
// 이 코드는 위의 트리와 정확히 대응됩니다
MaterialApp(
  home: Scaffold(
    appBar: AppBar(
      title: const Text('제목'),
    ),
    body: Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const CircleAvatar(radius: 40),
          const Text('이름'),
          ElevatedButton(
            onPressed: () {},
            child: const Text('클릭'),
          ),
        ],
      ),
    ),
  ),
)
```

### 트리 시각화 도구 (Flutter Inspector)

VS Code에서 앱이 실행 중일 때:
1. **View** → **Command Palette** → "Open Flutter Inspector"
2. 실시간으로 위젯 트리 확인 가능
3. 위젯 클릭 시 해당 코드 위치로 이동

---

<a id="part10"></a>
## 🔟 ⭐ **핵심** — 실습: 나만의 자기소개 카드 앱 [↑](#toc)

지금까지 배운 위젯들을 모두 활용해서 자기소개 카드 앱을 만듭니다.

### 완성 모습

```
┌─────────────────────────────┐
│  AppBar: 자기소개 카드       │
├─────────────────────────────┤
│                             │
│         🔵 (아바타)          │
│        김 민 준              │
│     Flutter 개발자           │
│                             │
│  ────────────────────────   │
│                             │
│  📍 서울특별시               │
│  ✉️ minjun@example.com      │
│  📱 010-1234-5678           │
│                             │
│  ────────────────────────   │
│                             │
│  관심사:                     │
│  [Flutter] [AI] [커피]       │
│                             │
│     [프로필 편집하기 버튼]    │
│                             │
└─────────────────────────────┘
```

### 전체 코드

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
      title: '자기소개 카드',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const ProfilePage(),
    );
  }
}

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    // 내 정보 (변수로 관리)
    const String myName = '김민준';
    const String myJob = 'Flutter 개발자';
    const String myCity = '서울특별시';
    const String myEmail = 'minjun@example.com';
    const String myPhone = '010-1234-5678';
    const List<String> myInterests = ['Flutter', 'AI', '커피', '독서'];

    return Scaffold(
      appBar: AppBar(
        title: const Text('자기소개 카드'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // 프로필 사진 (아바타)
            const SizedBox(height: 20),
            CircleAvatar(
              radius: 60,
              backgroundColor: Theme.of(context).colorScheme.primaryContainer,
              child: Text(
                myName[0],  // 이름 첫 글자
                style: TextStyle(
                  fontSize: 48,
                  color: Theme.of(context).colorScheme.primary,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),

            const SizedBox(height: 16),

            // 이름
            Text(
              myName,
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),

            // 직업
            Text(
              myJob,
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                color: Colors.grey[600],
              ),
            ),

            const SizedBox(height: 24),
            const Divider(),
            const SizedBox(height: 16),

            // 연락처 정보
            _InfoRow(
              icon: Icons.location_on,
              iconColor: Colors.red,
              text: myCity,
            ),
            const SizedBox(height: 12),
            _InfoRow(
              icon: Icons.email,
              iconColor: Colors.blue,
              text: myEmail,
            ),
            const SizedBox(height: 12),
            _InfoRow(
              icon: Icons.phone,
              iconColor: Colors.green,
              text: myPhone,
            ),

            const SizedBox(height: 24),
            const Divider(),
            const SizedBox(height: 16),

            // 관심사
            Align(
              alignment: Alignment.centerLeft,
              child: Text(
                '관심사',
                style: Theme.of(context).textTheme.titleSmall?.copyWith(
                  color: Colors.grey,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            const SizedBox(height: 8),

            // 관심사 태그 (Wrap으로 자동 줄바꿈)
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: myInterests.map((interest) {
                return Chip(
                  label: Text(interest),
                  backgroundColor:
                      Theme.of(context).colorScheme.primaryContainer,
                );
              }).toList(),
            ),

            const SizedBox(height: 32),

            // 버튼
            ElevatedButton.icon(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('편집 기능은 다음 챕터에서!')),
                );
              },
              icon: const Icon(Icons.edit),
              label: const Text('프로필 편집하기'),
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 48),
              ),
            ),

            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}

// 정보 행 위젯 (재사용 가능한 컴포넌트)
class _InfoRow extends StatelessWidget {
  final IconData icon;
  final Color iconColor;
  final String text;

  const _InfoRow({
    required this.icon,
    required this.iconColor,
    required this.text,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, color: iconColor, size: 20),
        const SizedBox(width: 12),
        Expanded(
          child: Text(
            text,
            style: Theme.of(context).textTheme.bodyLarge,
          ),
        ),
      ],
    );
  }
}
```

### 코드 구조 설명

이 코드에서 사용한 개념들:

| 코드 | 배운 개념 |
|------|----------|
| `const String myName = '김민준'` | 3장: const 변수 |
| `const List<String> myInterests = [...]` | 6장: List |
| `myName[0]` | 6장: 인덱스 접근 |
| `myInterests.map(...)` | 6장: map() 메서드 |
| `class _InfoRow extends StatelessWidget` | 7장: 클래스 상속 |
| `@override Widget build(...)` | 7장: @override |

---

<a id="part11"></a>
## 1️⃣1️⃣ 정리 — Phase 1 완주! [↑](#toc)

### 이 장에서 배운 위젯들

| 위젯 | 역할 | 핵심 속성 |
|------|------|----------|
| `Text` | 텍스트 표시 | `style`, `textAlign`, `maxLines` |
| `Container` | 상자/레이아웃 | `width`, `height`, `padding`, `decoration` |
| `SizedBox` | 간격/크기 | `width`, `height` |
| `Icon` | 아이콘 | `size`, `color` |
| `IconButton` | 아이콘 버튼 | `icon`, `onPressed` |
| `CircleAvatar` | 원형 이미지 | `radius`, `backgroundImage`, `child` |
| `Image.network` | 네트워크 이미지 | `fit`, `width`, `height` |
| `ElevatedButton` | 주요 버튼 | `onPressed`, `style`, `child` |
| `TextButton` | 텍스트 버튼 | `onPressed`, `child` |
| `OutlinedButton` | 테두리 버튼 | `onPressed`, `child` |
| `Chip` | 태그 칩 | `label`, `backgroundColor` |
| `Wrap` | 자동 줄바꿈 배치 | `spacing`, `runSpacing` |

### Phase 1 완주 체크리스트

- [ ] Dart 변수와 타입 이해
- [ ] const/final 차이 이해
- [ ] if/else, switch, for, while 작성 가능
- [ ] 함수 선언과 호출 가능
- [ ] List와 Map 기본 조작 가능
- [ ] 클래스와 객체 이해
- [ ] 기본 위젯들 (Text, Container, Button 등) 사용 가능
- [ ] 자기소개 카드 앱 완성

### Phase 1 → Phase 2 관문

> "AI 없이 Dart 변수, 함수, 클래스를 작성할 수 있어야 합니다."

간단한 테스트:
1. `Person` 클래스를 만들 수 있나요? (이름, 나이, 자기소개 메서드)
2. 정수 리스트에서 짝수만 골라 새 리스트를 만들 수 있나요?
3. 버튼을 누르면 텍스트가 바뀌는 앱을 만들 수 있나요?

모두 가능하다면 Phase 2로 진행할 준비가 됐습니다!

### 다음 Phase 예고

**Phase 2**에서는:
- Row, Column, Stack으로 복잡한 레이아웃 만들기
- StatefulWidget과 setState로 상호작용 앱 만들기
- ListView로 스크롤 가능한 목록 만들기
- AI가 생성한 Flutter 코드를 읽고 검증하기

---

---

→ **다음 내용으로 넘어갑시다**: [08. 레이아웃 — Row, Column, Expanded](/ai-native-flutter/layout)
