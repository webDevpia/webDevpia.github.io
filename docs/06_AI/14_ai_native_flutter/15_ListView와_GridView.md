---
title: "14. ListView와 GridView"
layout: default
parent: AI-Native Flutter
nav_order: 16
permalink: /ai-native-flutter/listview-gridview
---

# 14장. ListView와 GridView
{: .no_toc }

> **Phase 2** · 예상 시간: 120분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 생성 + 검증 모드**
> AI(Copilot)가 코드를 생성할 수 있습니다.
> 단, 반드시 생성된 코드를 **읽고, 이해하고, 테스트로 검증**해야 합니다.

## 학습 목표

- ListView.builder로 대량의 데이터를 효율적으로 렌더링할 수 있다
- ListTile로 아이콘+텍스트 목록을 빠르게 구성할 수 있다
- GridView.builder로 격자 레이아웃을 만들 수 있다
- Dismissible로 스와이프 삭제 기능을 구현할 수 있다

<a id="toc"></a>
## 진행 순서

1. [ListView — 스크롤 가능한 목록](#part1) — SNS 피드 비유
2. [ListView.builder — 효율적 렌더링](#part2)
3. [ListTile — 표준 목록 항목](#part3)
4. [Card 위젯 — 카드형 목록](#part4)
5. [GridView — 격자 레이아웃](#part5) — 인스타그램 비유
6. [GridView.builder와 SliverGridDelegate](#part6)
7. [Dismissible — 스와이프 삭제](#part7)
8. [실습: 연락처 목록 앱](#part8)
9. [🚀 도전: 이미지 갤러리](#part9)
10. [정리](#part10)

---

<a id="part1"></a>
## 1️⃣ ⭐ **핵심** — ListView [↑](#toc)

### SNS 피드 비유

> `ListView`는 스마트폰의 **SNS 피드**와 같습니다.
> 끝없이 아래로 스크롤하면서 새 항목이 나타납니다.
> Flutter는 화면에 보이는 항목만 메모리에 올려 효율적으로 관리합니다.

### 기본 ListView

```dart
ListView(
  children: [
    const ListTile(title: Text('항목 1')),
    const ListTile(title: Text('항목 2')),
    const ListTile(title: Text('항목 3')),
  ],
)
```

항목 수가 고정되어 있고 적을 때 (10개 이하) 사용합니다.

### ListView 주요 속성

```dart
ListView(
  scrollDirection: Axis.vertical,      // 세로 스크롤 (기본)
  // scrollDirection: Axis.horizontal, // 가로 스크롤
  reverse: false,                       // 뒤집기 (채팅 앱에서 유용)
  padding: const EdgeInsets.all(8),
  physics: const BouncingScrollPhysics(),  // iOS 스타일 바운스
  // physics: const NeverScrollableScrollPhysics(), // 스크롤 비활성화
  children: [...],
)
```

### ListView.separated — 구분선 추가

```dart
ListView.separated(
  itemCount: items.length,
  separatorBuilder: (context, index) => const Divider(),  // 구분선
  itemBuilder: (context, index) {
    return ListTile(title: Text(items[index]));
  },
)
```

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — ListView.builder [↑](#toc)

### 왜 builder를 써야 하는가?

기본 `ListView`는 **모든 항목을 한 번에 만듭니다**.
항목이 1,000개라면? 1,000개를 모두 메모리에 올립니다. 느립니다.

`ListView.builder`는 **화면에 보이는 항목만 만듭니다**.
아이러니하게도, 1,000개 목록도 화면에 보이는 10~15개만 렌더링하므로 빠릅니다.

```
ListView (기본):          ListView.builder:
┌──────────────┐          ┌──────────────┐
│ 항목 1 (메모리) │          │ 항목 5 (화면) │
│ 항목 2 (메모리) │          │ 항목 6 (화면) │
│ 항목 3 (메모리) │          │ 항목 7 (화면) │  ← 이것만 렌더링
│ ...           │          │ 항목 8 (화면) │
│ 항목 1000(메모리)│          └──────────────┘
└──────────────┘          (스크롤하면 필요한 것만 생성)
```

### ListView.builder 기본 사용

```dart
final List<String> _contacts = [
  '김민수', '이서연', '박지훈', '최유리', '정민호', // ...
];

ListView.builder(
  itemCount: _contacts.length,         // 총 항목 수
  itemBuilder: (context, index) {      // 각 항목을 만드는 함수
    return ListTile(
      leading: CircleAvatar(child: Text('${index + 1}')),
      title: Text(_contacts[index]),
    );
  },
)
```

### itemBuilder 이해하기

```dart
itemBuilder: (BuildContext context, int index) {
  // index: 현재 항목의 번호 (0부터 시작)
  // 이 함수는 화면에 표시될 때마다 호출됨
  final item = items[index];
  return Widget;   // 어떤 위젯이든 반환 가능
}
```

---

<a id="part3"></a>
## 3️⃣ ⭐ **핵심** — ListTile [↑](#toc)

`ListTile`은 **아이콘 + 제목 + 부제목 + 우측 버튼** 패턴의 목록 항목을 빠르게 만드는 위젯입니다.

### ListTile 구조

```
┌──────────────────────────────────────────────┐
│ [leading] [title         ] [trailing]         │
│           [subtitle      ]                    │
└──────────────────────────────────────────────┘
```

```dart
ListTile(
  leading: const CircleAvatar(     // 왼쪽 아이콘/이미지
    child: Icon(Icons.person),
  ),
  title: const Text('홍길동'),       // 제목 (굵게)
  subtitle: const Text('010-1234-5678'),  // 부제목
  trailing: const Icon(Icons.arrow_forward_ios, size: 16),  // 오른쪽
  onTap: () {                      // 탭 이벤트
    print('홍길동 선택됨');
  },
)
```

### ListTile 스타일 커스텀

```dart
ListTile(
  contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
  tileColor: Colors.blue[50],      // 배경색
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(12),
  ),
  leading: const Icon(Icons.email, color: Colors.blue),
  title: const Text(
    '이메일',
    style: TextStyle(fontWeight: FontWeight.bold),
  ),
  subtitle: const Text('user@example.com'),
  trailing: Switch(
    value: true,
    onChanged: (value) {},
  ),
)
```

---

<a id="part4"></a>
## 4️⃣ Card 위젯 — 카드형 목록 [↑](#toc)

`Card`는 그림자와 둥근 모서리를 가진 **카드 형태**의 컨테이너입니다.

```dart
Card(
  elevation: 4,                         // 그림자 높이
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(12),
  ),
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: Row(
      children: [
        const CircleAvatar(
          radius: 30,
          child: Icon(Icons.person, size: 30),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                '홍길동',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              Text(
                'Flutter 개발자',
                style: TextStyle(color: Colors.grey[600]),
              ),
            ],
          ),
        ),
        IconButton(
          icon: const Icon(Icons.more_vert),
          onPressed: () {},
        ),
      ],
    ),
  ),
),
```

### ListView.builder + Card 조합

```dart
ListView.builder(
  padding: const EdgeInsets.all(8),
  itemCount: profiles.length,
  itemBuilder: (context, index) {
    final profile = profiles[index];
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 4),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: Colors.primaries[index % Colors.primaries.length],
          child: Text(profile.name[0]),    // 이름 첫 글자
        ),
        title: Text(profile.name),
        subtitle: Text(profile.role),
        trailing: IconButton(
          icon: const Icon(Icons.call),
          onPressed: () {},
        ),
      ),
    );
  },
)
```

---

<a id="part5"></a>
## 5️⃣ ⭐ **핵심** — GridView [↑](#toc)

### 인스타그램 사진첩 비유

> `GridView`는 인스타그램의 **프로필 사진첩**처럼 격자(Grid) 형태로 항목을 배치합니다.

### GridView.count — 열 개수 고정

```dart
GridView.count(
  crossAxisCount: 3,              // 가로로 3개씩
  crossAxisSpacing: 4,            // 가로 간격
  mainAxisSpacing: 4,             // 세로 간격
  padding: const EdgeInsets.all(8),
  children: [
    Container(color: Colors.red),
    Container(color: Colors.green),
    Container(color: Colors.blue),
    Container(color: Colors.yellow),
    // ...
  ],
)
```

### GridView.extent — 최소 너비 고정

```dart
GridView.extent(
  maxCrossAxisExtent: 150,        // 각 항목 최대 너비
  crossAxisSpacing: 8,
  mainAxisSpacing: 8,
  children: [...],
)
```

> `maxCrossAxisExtent: 150`은 "최대 150px 너비"를 의미합니다.
> 화면이 넓으면 더 많은 열, 좁으면 더 적은 열 — 반응형 레이아웃!

---

<a id="part6"></a>
## 6️⃣ GridView.builder와 SliverGridDelegate [↑](#toc)

`ListView.builder`처럼, `GridView.builder`도 **대량 데이터**를 효율적으로 렌더링합니다.

```dart
GridView.builder(
  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 2,              // 열 개수
    crossAxisSpacing: 8,
    mainAxisSpacing: 8,
    childAspectRatio: 3 / 4,       // 가로:세로 비율
  ),
  itemCount: products.length,
  padding: const EdgeInsets.all(8),
  itemBuilder: (context, index) {
    final product = products[index];
    return Card(
      clipBehavior: Clip.antiAlias,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            child: Container(
              color: Colors.grey[200],
              child: const Center(child: Icon(Icons.image, size: 50)),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(product.name,
                    style: const TextStyle(fontWeight: FontWeight.bold)),
                Text('${product.price}원',
                    style: const TextStyle(color: Colors.blue)),
              ],
            ),
          ),
        ],
      ),
    );
  },
)
```

### SliverGridDelegate 종류

```dart
// 1. 열 개수 고정
SliverGridDelegateWithFixedCrossAxisCount(
  crossAxisCount: 3,
  childAspectRatio: 1.0,          // 정사각형
)

// 2. 최대 너비 고정 (반응형)
SliverGridDelegateWithMaxCrossAxisExtent(
  maxCrossAxisExtent: 200,
  childAspectRatio: 2 / 3,
)
```

---

<a id="part7"></a>
## 7️⃣ 🚀 **도전** — Dismissible: 스와이프 삭제 [↑](#toc)

`Dismissible`로 목록 항목을 **스와이프해서 삭제**하는 기능을 만들 수 있습니다.

> Gmail에서 이메일을 왼쪽으로 스와이프하면 삭제되는 것처럼요.

```dart
class _ContactListState extends State<ContactList> {
  final List<String> _contacts = ['김민수', '이서연', '박지훈', '최유리'];

  void _removeContact(int index) {
    setState(() {
      _contacts.removeAt(index);
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: _contacts.length,
      itemBuilder: (context, index) {
        final contact = _contacts[index];

        return Dismissible(
          key: Key(contact),                // 각 항목의 고유 키 (필수)
          direction: DismissDirection.endToStart,  // 오른쪽→왼쪽 스와이프
          background: Container(
            alignment: Alignment.centerRight,
            padding: const EdgeInsets.only(right: 20),
            color: Colors.red,
            child: const Icon(Icons.delete, color: Colors.white),
          ),
          onDismissed: (direction) {
            _removeContact(index);
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('$contact 삭제됨'),
                action: SnackBarAction(
                  label: '취소',
                  onPressed: () {
                    setState(() {
                      _contacts.insert(index, contact);
                    });
                  },
                ),
              ),
            );
          },
          child: ListTile(
            leading: CircleAvatar(child: Text(contact[0])),
            title: Text(contact),
          ),
        );
      },
    );
  }
}
```

### Dismissible 주요 속성

```dart
Dismissible(
  key: Key(item.id.toString()),    // 반드시 유일한 키 필요
  direction: DismissDirection.horizontal,  // 양방향
  // direction: DismissDirection.startToEnd, // 왼쪽→오른쪽
  // direction: DismissDirection.endToStart, // 오른쪽→왼쪽
  background: Container(color: Colors.green),  // 첫 번째 방향 배경
  secondaryBackground: Container(color: Colors.red),  // 반대 방향 배경
  confirmDismiss: (direction) async {
    // 삭제 전 확인 다이얼로그
    return await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('삭제 확인'),
        content: const Text('정말 삭제하시겠습니까?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('취소')),
          TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('삭제')),
        ],
      ),
    );
  },
  onDismissed: (direction) { /* 삭제 처리 */ },
  child: ListTile(title: Text(item.name)),
)
```

---

<a id="part8"></a>
## 8️⃣ 💪 **보너스 챌린지** — 실습: 연락처 목록 앱 [↑](#toc)

ListTile + 검색 기능을 가진 연락처 앱을 만들어 봅시다.

### 완성 목표

```
┌─────────────────────────────┐
│ 연락처              [검색🔍]  │
├─────────────────────────────┤
│ [검색창]                     │
├─────────────────────────────┤
│ 👤 김민수                     │
│    010-1234-5678             │
│    개발팀                     │
├─────────────────────────────┤
│ 👤 이서연    (스와이프로 삭제) │
│    010-2345-6789             │
└─────────────────────────────┘
```

### 구현 코드

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
      title: '연락처',
      home: ContactListScreen(),
    );
  }
}

class Contact {
  final String name;
  final String phone;
  final String department;

  const Contact({
    required this.name,
    required this.phone,
    required this.department,
  });
}

class ContactListScreen extends StatefulWidget {
  const ContactListScreen({super.key});

  @override
  State<ContactListScreen> createState() => _ContactListScreenState();
}

class _ContactListScreenState extends State<ContactListScreen> {
  final List<Contact> _allContacts = const [
    Contact(name: '김민수', phone: '010-1234-5678', department: '개발팀'),
    Contact(name: '이서연', phone: '010-2345-6789', department: '디자인팀'),
    Contact(name: '박지훈', phone: '010-3456-7890', department: '기획팀'),
    Contact(name: '최유리', phone: '010-4567-8901', department: '개발팀'),
    Contact(name: '정민호', phone: '010-5678-9012', department: '마케팅팀'),
    Contact(name: '한소희', phone: '010-6789-0123', department: '영업팀'),
    Contact(name: '오준혁', phone: '010-7890-1234', department: '개발팀'),
    Contact(name: '윤지민', phone: '010-8901-2345', department: 'HR팀'),
  ];

  List<Contact> _filteredContacts = [];
  String _searchQuery = '';
  bool _isSearching = false;

  @override
  void initState() {
    super.initState();
    _filteredContacts = _allContacts;
  }

  void _filter(String query) {
    setState(() {
      _searchQuery = query;
      if (query.isEmpty) {
        _filteredContacts = _allContacts;
      } else {
        _filteredContacts = _allContacts
            .where((contact) =>
                contact.name.contains(query) ||
                contact.phone.contains(query) ||
                contact.department.contains(query))
            .toList();
      }
    });
  }

  void _deleteContact(Contact contact) {
    // 실제로는 _allContacts에서 제거해야 하지만,
    // const List이므로 여기서는 filteredContacts에서만 제거
    setState(() {
      _filteredContacts.remove(contact);
    });
  }

  Color _departmentColor(String department) {
    switch (department) {
      case '개발팀':
        return Colors.blue;
      case '디자인팀':
        return Colors.purple;
      case '기획팀':
        return Colors.orange;
      case '마케팅팀':
        return Colors.green;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: _isSearching
            ? TextField(
                autofocus: true,
                decoration: const InputDecoration(
                  hintText: '이름, 부서, 전화번호 검색',
                  border: InputBorder.none,
                  hintStyle: TextStyle(color: Colors.white70),
                ),
                style: const TextStyle(color: Colors.white),
                onChanged: _filter,
              )
            : const Text('연락처'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: Icon(_isSearching ? Icons.close : Icons.search),
            onPressed: () {
              setState(() {
                _isSearching = !_isSearching;
                if (!_isSearching) {
                  _filter('');
                }
              });
            },
          ),
        ],
      ),
      body: _filteredContacts.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.search_off, size: 80, color: Colors.grey),
                  const SizedBox(height: 16),
                  Text(
                    '"$_searchQuery" 검색 결과 없음',
                    style: const TextStyle(color: Colors.grey),
                  ),
                ],
              ),
            )
          : ListView.separated(
              itemCount: _filteredContacts.length,
              separatorBuilder: (_, __) => const Divider(height: 1),
              itemBuilder: (context, index) {
                final contact = _filteredContacts[index];
                return Dismissible(
                  key: Key(contact.phone),
                  direction: DismissDirection.endToStart,
                  background: Container(
                    alignment: Alignment.centerRight,
                    padding: const EdgeInsets.only(right: 20),
                    color: Colors.red,
                    child: const Icon(Icons.delete, color: Colors.white),
                  ),
                  onDismissed: (_) => _deleteContact(contact),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor:
                          _departmentColor(contact.department).withOpacity(0.2),
                      child: Text(
                        contact.name[0],
                        style: TextStyle(
                          color: _departmentColor(contact.department),
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    title: Text(contact.name),
                    subtitle: Text(contact.phone),
                    trailing: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: _departmentColor(contact.department).withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        contact.department,
                        style: TextStyle(
                          fontSize: 12,
                          color: _departmentColor(contact.department),
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: const Icon(Icons.person_add),
      ),
    );
  }
}
```

---

<a id="part9"></a>
## 9️⃣ 🚀 **도전** — 이미지 갤러리 (GridView + NetworkImage) [↑](#toc)

GridView와 NetworkImage를 사용해 인스타그램 스타일 갤러리를 만들어보세요.

### NetworkImage 기본 사용

```dart
// 인터넷 이미지 표시
Image.network(
  'https://placehold.co/200x200',
  fit: BoxFit.cover,
  loadingBuilder: (context, child, loadingProgress) {
    if (loadingProgress == null) return child;
    return Center(
      child: CircularProgressIndicator(
        value: loadingProgress.expectedTotalBytes != null
            ? loadingProgress.cumulativeBytesLoaded /
                loadingProgress.expectedTotalBytes!
            : null,
      ),
    );
  },
  errorBuilder: (context, error, stackTrace) {
    return const Center(child: Icon(Icons.broken_image));
  },
)
```

### 이미지 갤러리 구현

```dart
class ImageGalleryScreen extends StatelessWidget {
  const ImageGalleryScreen({super.key});

  // 랜덤 이미지 URL 생성 (placehold.co 무료 서비스)
  String _imageUrl(int id) => 'https://placehold.co/300x300';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('갤러리'),
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
      ),
      backgroundColor: Colors.black,
      body: GridView.builder(
        padding: const EdgeInsets.all(2),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 3,
          crossAxisSpacing: 2,
          mainAxisSpacing: 2,
        ),
        itemCount: 30,
        itemBuilder: (context, index) {
          return GestureDetector(
            onTap: () {
              // 이미지 상세 보기
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (ctx) => ImageDetailScreen(imageId: index),
                ),
              );
            },
            child: Hero(
              tag: 'image-$index',
              child: Image.network(
                _imageUrl(index),
                fit: BoxFit.cover,
                loadingBuilder: (ctx, child, progress) {
                  if (progress == null) return child;
                  return Container(
                    color: Colors.grey[900],
                    child: const Center(
                      child: CircularProgressIndicator(color: Colors.white),
                    ),
                  );
                },
              ),
            ),
          );
        },
      ),
    );
  }
}

// 이미지 상세 화면
class ImageDetailScreen extends StatelessWidget {
  final int imageId;
  const ImageDetailScreen({super.key, required this.imageId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        foregroundColor: Colors.white,
      ),
      body: Center(
        child: Hero(
          tag: 'image-$imageId',
          child: Image.network(
            'https://placehold.co/600x600',
            fit: BoxFit.contain,
          ),
        ),
      ),
    );
  }
}
```

> `Hero` 위젯은 두 화면 간에 같은 `tag`를 가진 위젯을 연결해
> 부드러운 전환 애니메이션을 만들어줍니다.

---

<a id="part10"></a>
## 🔟 정리 [↑](#toc)

### ListView vs GridView 선택 기준

| 상황 | 추천 위젯 |
|------|----------|
| 연락처, 채팅 목록 | `ListView.builder` + `ListTile` |
| 이메일, 뉴스 목록 | `ListView.builder` + `Card` |
| 사진첩, 상품 목록 | `GridView.builder` |
| 대시보드 카드 | `GridView.count` |
| 항목이 10개 이하 | `ListView` 또는 `Column` |

### 성능 규칙

```
항목 수에 따른 선택:
- 10개 이하  → ListView(children:[...]) 또는 Column
- 10개 이상  → ListView.builder (필수!)
- 100개 이상 → ListView.builder + 페이지네이션 고려
```

### Dismissible 체크리스트

```
□ key: Key(유일한 값) — String ID, index 등
□ onDismissed에서 실제로 데이터 삭제 (setState)
□ 삭제 후 UI와 데이터가 일치하는지 확인
□ 취소 기능이 필요하면 SnackBar + SnackBarAction
```

### 다음 장 예고

Phase 2가 완료되었습니다! 다음 Phase 3에서는:
- HTTP 요청으로 실제 API 데이터 가져오기
- Provider/Riverpod으로 전역 상태 관리
- Firebase로 로그인, 데이터베이스 연동

본격적인 실제 앱을 만들어봅니다!

---

> **자기 점검**: 다음 코드는 왜 문제인가요?
> ```dart
> ListView(
>   children: List.generate(10000, (index) => ListTile(
>     title: Text('항목 $index'),
>   )),
> )
> ```
> → 10,000개 위젯을 한 번에 모두 만들어 메모리에 올립니다.
> → 반드시 `ListView.builder`로 바꿔야 합니다:
> ```dart
> ListView.builder(
>   itemCount: 10000,
>   itemBuilder: (context, index) => ListTile(
>     title: Text('항목 $index'),
>   ),
> )
> ```

---

→ **다음 내용으로 넘어갑시다**: [15. 비동기와 API 호출](/ai-native-flutter/async-api)
