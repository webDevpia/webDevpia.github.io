---
title: "15. 비동기와 API 호출"
layout: default
parent: AI-Native Flutter
nav_order: 17
permalink: /ai-native-flutter/async-api
---

# 15장. 비동기와 API 호출
{: .no_toc }

> **Phase 3** · 예상 시간: 120분

> 💡 **실습 흐름**: 강사 시연 보기 → 함께 따라하기 → 혼자 변형해 보기

> **이 장의 AI 사용 규칙 — 완전 페어 프로그래밍**
> AI(Copilot)와 완전한 협업이 가능합니다.
> 내가 설계하고 AI가 구현합니다. 테스트로 검증합니다.
> "신뢰하되 검증한다(Trust but verify)"가 원칙입니다.

## 학습 목표

- 비동기 프로그래밍의 개념을 이해하고 `Future`, `async/await`를 사용할 수 있다
- `http` 패키지로 REST API를 호출하고 JSON을 파싱할 수 있다
- `FutureBuilder`로 로딩 · 성공 · 에러 3가지 상태를 화면에 표현할 수 있다

<a id="toc"></a>
## 진행 순서

1. [비동기란?](#part1) — 카페 주문 비유
2. [Future](#part2) — "나중에 올 값"
3. [async/await](#part3) — 기다리는 방법
4. [try/catch](#part4) — 에러 처리
5. [http 패키지 설치](#part5) — pubspec.yaml
6. [REST API 호출하기](#part6) — GET 요청
7. [JSON 파싱](#part7) — 데이터 추출
8. [FutureBuilder](#part8) — 데이터 로딩 패턴
9. [실습](#part9) — JSONPlaceholder로 포스트 목록
10. [정리](#part10)

---

<a id="part1"></a>
## 1️⃣ ⭐ **핵심** — 비동기란? [↑](#toc)

### 카페 주문 비유

카페에 가서 아메리카노를 주문합니다.

**동기(Synchronous) 방식:**
> 주문대 앞에 멈춰 서서 커피가 나올 때까지 아무것도 못 합니다.  
> 다른 손님도 내 뒤에서 꼼짝없이 기다려야 합니다.

**비동기(Asynchronous) 방식:**
> 주문하고 **번호표**를 받습니다.  
> 자리에 앉아 스마트폰도 보고, 친구와 대화도 합니다.  
> 번호가 불리면 그때 가서 커피를 받습니다.

앱도 마찬가지입니다. 인터넷에서 데이터를 가져오는 데 시간이 걸리는데, 그 동안 화면이 멈춰버리면 사용자는 답답합니다. **비동기 프로그래밍**은 "기다리는 동안 다른 일을 계속하는" 방법입니다.

### 비동기가 필요한 상황

| 상황 | 이유 |
|------|------|
| API 호출 | 네트워크 응답 시간이 불확실 |
| 파일 읽기/쓰기 | 디스크 접근에 시간 소요 |
| 데이터베이스 쿼리 | 처리 시간이 걸림 |
| 이미지 다운로드 | 파일 크기에 따라 가변 |

---

<a id="part2"></a>
## 2️⃣ ⭐ **핵심** — Future: "나중에 올 값" [↑](#toc)

### 택배 비유

`Future`는 **택배 운송장**과 같습니다.

- 주문 직후에는 물건이 없지만, 운송장 번호가 있습니다
- "나중에 이 번호로 택배가 도착할 거야"라는 **약속**입니다
- 택배가 도착하면(성공) 물건을 받거나, 배송 실패(에러)를 통보받습니다

```dart
// Future<String> = "나중에 String이 올 거야"라는 약속
Future<String> fetchGreeting() {
  // 2초 후에 값을 돌려주는 예시
  return Future.delayed(
    Duration(seconds: 2),
    () => 'Hello, Flutter!',
  );
}
```

### Future의 3가지 상태

```
대기 중(Pending) → 완료(Completed with value)
                 ↘ 실패(Completed with error)
```

| 상태 | 설명 | 비유 |
|------|------|------|
| Pending | 아직 값이 없음 | 택배 배송 중 |
| Completed (value) | 성공적으로 값 도착 | 택배 수령 완료 |
| Completed (error) | 에러 발생 | 배송 실패 |

### Future 기본 사용

```dart
void main() {
  print('1. 주문 완료');

  Future.delayed(Duration(seconds: 2), () {
    print('3. 커피 준비 완료!');
  });

  print('2. 자리에 앉아서 기다리는 중...');
}

// 출력 순서:
// 1. 주문 완료
// 2. 자리에 앉아서 기다리는 중...
// (2초 후)
// 3. 커피 준비 완료!
```

---

<a id="part3"></a>
## 3️⃣ ⭐ **핵심** — async/await: 기다리는 방법 [↑](#toc)

### 문제: then() 체인의 단점

```dart
// then()으로 연결하면 코드가 복잡해집니다
fetchUser()
  .then((user) {
    return fetchPosts(user.id);
  })
  .then((posts) {
    return fetchComments(posts.first.id);
  })
  .then((comments) {
    print(comments);
  });
```

### 해결: async/await

`async/await`를 쓰면 비동기 코드가 **동기 코드처럼** 읽힙니다.

```dart
// async: "이 함수 안에서 await를 쓸 거야"
Future<void> loadData() async {
  // await: "이 Future가 완료될 때까지 여기서 기다려"
  final user = await fetchUser();
  final posts = await fetchPosts(user.id);
  final comments = await fetchComments(posts.first.id);
  print(comments);
}
```

### 규칙

| 키워드 | 위치 | 의미 |
|--------|------|------|
| `async` | 함수 선언부 | "이 함수는 비동기 함수입니다" |
| `await` | Future 앞 | "이 Future가 완료될 때까지 기다려" |

```dart
// async 없이 await를 쓰면 에러!
void wrong() {
  final result = await someFuture(); // ❌ 컴파일 에러
}

// async가 있어야 await 사용 가능
Future<void> correct() async {
  final result = await somefuture(); // ✅
}
```

### 반환 타입

```dart
// 반환값이 없으면 Future<void>
Future<void> doSomething() async { ... }

// String을 반환하면 Future<String>
Future<String> getName() async {
  await Future.delayed(Duration(seconds: 1));
  return 'Flutter';
}

// int를 반환하면 Future<int>
Future<int> getCount() async {
  await Future.delayed(Duration(seconds: 1));
  return 42;
}
```

---

<a id="part4"></a>
## 4️⃣ ⭐ **핵심** — try/catch: 에러 처리 [↑](#toc)

### 에러가 발생할 수 있는 상황

- 인터넷 연결 없음
- 서버가 응답 없음 (타임아웃)
- 잘못된 URL
- 서버 에러 (404, 500 등)

```dart
Future<String> fetchData() async {
  try {
    // 실패할 수 있는 코드를 try 안에
    final response = await http.get(Uri.parse('https://api.example.com/data'));

    if (response.statusCode == 200) {
      return response.body;
    } else {
      throw Exception('서버 에러: ${response.statusCode}');
    }
  } catch (e) {
    // 에러가 발생하면 catch에서 처리
    print('에러 발생: $e');
    return '데이터를 가져올 수 없습니다';
  } finally {
    // 성공이든 실패든 항상 실행
    print('요청 완료');
  }
}
```

### 에러 타입 구분

```dart
Future<void> fetchWithDetail() async {
  try {
    final response = await http.get(Uri.parse('https://api.example.com'));
    // ...
  } on SocketException {
    // 인터넷 연결 없음
    print('인터넷 연결을 확인해주세요');
  } on TimeoutException {
    // 타임아웃
    print('응답 시간이 초과되었습니다');
  } catch (e) {
    // 그 외 모든 에러
    print('알 수 없는 에러: $e');
  }
}
```

---

<a id="part5"></a>
## 5️⃣ ⭐ **핵심** — http 패키지 설치 [↑](#toc)

### pubspec.yaml에 의존성 추가

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.2.0        # 추가
```

### 터미널에서 설치

```bash
flutter pub add http
```

또는 직접 pubspec.yaml을 수정한 후:

```bash
flutter pub get
```

### 임포트

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';  // JSON 파싱용
```

---

<a id="part6"></a>
## 6️⃣ ⭐ **핵심** — REST API 호출하기 (GET 요청) [↑](#toc)

### REST API란?

인터넷을 통해 데이터를 주고받는 약속입니다.

| 메서드 | 용도 | 비유 |
|--------|------|------|
| GET | 데이터 가져오기 | 도서관에서 책 빌리기 |
| POST | 데이터 보내기 | 도서관에 책 기부하기 |
| PUT | 데이터 수정하기 | 책 내용 수정 요청 |
| DELETE | 데이터 삭제하기 | 책 폐기 요청 |

이 장에서는 **GET**만 사용합니다.

### 기본 GET 요청

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<Map<String, dynamic>> fetchPost(int id) async {
  // 1. URL 만들기
  final url = Uri.parse('https://jsonplaceholder.typicode.com/posts/$id');

  // 2. GET 요청 보내기
  final response = await http.get(url);

  // 3. 응답 확인
  if (response.statusCode == 200) {
    // 4. JSON 파싱
    return jsonDecode(response.body) as Map<String, dynamic>;
  } else {
    throw Exception('포스트를 불러오지 못했습니다. 상태 코드: ${response.statusCode}');
  }
}
```

### HTTP 상태 코드

| 코드 | 의미 | 비유 |
|------|------|------|
| 200 | 성공 | 주문한 물건 정상 도착 |
| 400 | 잘못된 요청 | 주문서를 잘못 작성 |
| 401 | 인증 필요 | 회원 전용 서비스인데 로그인 안 함 |
| 404 | 찾을 수 없음 | 없는 상품 주문 |
| 500 | 서버 에러 | 물류 창고 화재 |

---

<a id="part7"></a>
## 7️⃣ ⭐ **핵심** — JSON 파싱 [↑](#toc)

### JSON이란?

데이터를 텍스트로 표현하는 형식입니다.

```json
{
  "id": 1,
  "title": "Flutter는 재미있다",
  "body": "AI와 함께 배우면 더욱 즐겁습니다",
  "userId": 1
}
```

### jsonDecode: JSON 문자열 → Dart 객체

```dart
import 'dart:convert';

final jsonString = '{"id": 1, "title": "Flutter"}';

// jsonDecode는 dynamic 타입을 반환
final data = jsonDecode(jsonString);

// Map으로 캐스팅해서 사용
final map = jsonDecode(jsonString) as Map<String, dynamic>;
print(map['id']);     // 1
print(map['title']); // Flutter
```

### 리스트 JSON 파싱

```dart
final jsonString = '[{"id": 1, "title": "첫 번째"}, {"id": 2, "title": "두 번째"}]';

final list = jsonDecode(jsonString) as List<dynamic>;

// 각 항목 접근
for (final item in list) {
  final map = item as Map<String, dynamic>;
  print(map['title']);
}

// 또는 map으로 변환
final titles = list
    .map((item) => (item as Map<String, dynamic>)['title'] as String)
    .toList();
```

### 모델 클래스로 변환 (권장)

```dart
class Post {
  final int id;
  final String title;
  final String body;

  Post({required this.id, required this.title, required this.body});

  // JSON Map에서 Post 객체 생성
  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(
      id: json['id'] as int,
      title: json['title'] as String,
      body: json['body'] as String,
    );
  }
}

// 사용
final response = await http.get(url);
final json = jsonDecode(response.body) as Map<String, dynamic>;
final post = Post.fromJson(json);
```

---

<a id="part8"></a>
## 8️⃣ ⭐ **핵심** — FutureBuilder: 데이터 로딩 패턴 [↑](#toc)

### 3가지 상태를 화면으로

API 호출에는 항상 3가지 상태가 있습니다:

| 상태 | 화면 | 비유 |
|------|------|------|
| 로딩 중 | 스피너 / 로딩 바 | 택배 배송 중 |
| 성공 | 데이터 표시 | 택배 수령 |
| 에러 | 에러 메시지 | 배송 실패 알림 |

### FutureBuilder 기본 구조

```dart
FutureBuilder<Post>(
  // 어떤 Future를 기다릴지
  future: fetchPost(1),

  // Future 상태에 따라 위젯을 반환하는 함수
  builder: (context, snapshot) {
    // 1. 로딩 중
    if (snapshot.connectionState == ConnectionState.waiting) {
      return Center(child: CircularProgressIndicator());
    }

    // 2. 에러 발생
    if (snapshot.hasError) {
      return Center(
        child: Text('에러: ${snapshot.error}'),
      );
    }

    // 3. 데이터 없음 (null)
    if (!snapshot.hasData) {
      return Center(child: Text('데이터가 없습니다'));
    }

    // 4. 성공 — 데이터 표시
    final post = snapshot.data!;
    return Padding(
      padding: EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            post.title,
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 8),
          Text(post.body),
        ],
      ),
    );
  },
)
```

### snapshot의 주요 속성

| 속성 | 설명 |
|------|------|
| `snapshot.connectionState` | Future 진행 상태 |
| `snapshot.hasData` | 데이터가 있는지 여부 |
| `snapshot.data` | 실제 데이터 (nullable) |
| `snapshot.hasError` | 에러가 있는지 여부 |
| `snapshot.error` | 에러 객체 |

### ConnectionState 값

```dart
ConnectionState.none     // Future가 없음
ConnectionState.waiting  // 기다리는 중
ConnectionState.active   // 진행 중 (Stream용)
ConnectionState.done     // 완료
```

---

<a id="part9"></a>
## 9️⃣ 🚀 **도전** — 실습: JSONPlaceholder API로 포스트 목록 [↑](#toc)

JSONPlaceholder는 테스트용 무료 API입니다. API 키 없이 사용할 수 있습니다.

- API URL: `https://jsonplaceholder.typicode.com/posts`

### Step 1: 새 프로젝트 만들기

```bash
flutter create async_demo
cd async_demo
flutter pub add http
```

### Step 2: Post 모델 작성

`lib/models/post.dart`:

```dart
class Post {
  final int id;
  final int userId;
  final String title;
  final String body;

  Post({
    required this.id,
    required this.userId,
    required this.title,
    required this.body,
  });

  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(
      id: json['id'] as int,
      userId: json['userId'] as int,
      title: json['title'] as String,
      body: json['body'] as String,
    );
  }
}
```

### Step 3: API 서비스 작성

`lib/services/post_service.dart`:

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/post.dart';

class PostService {
  static const String baseUrl = 'https://jsonplaceholder.typicode.com';

  Future<List<Post>> fetchPosts() async {
    final url = Uri.parse('$baseUrl/posts');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      final List<dynamic> jsonList = jsonDecode(response.body);
      return jsonList
          .map((json) => Post.fromJson(json as Map<String, dynamic>))
          .toList();
    } else {
      throw Exception('포스트 목록을 불러오지 못했습니다');
    }
  }
}
```

### Step 4: 화면 작성

`lib/screens/posts_screen.dart`:

```dart
import 'package:flutter/material.dart';
import '../models/post.dart';
import '../services/post_service.dart';

class PostsScreen extends StatefulWidget {
  const PostsScreen({super.key});

  @override
  State<PostsScreen> createState() => _PostsScreenState();
}

class _PostsScreenState extends State<PostsScreen> {
  final PostService _service = PostService();
  late Future<List<Post>> _postsFuture;

  @override
  void initState() {
    super.initState();
    _postsFuture = _service.fetchPosts();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('포스트 목록'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: FutureBuilder<List<Post>>(
        future: _postsFuture,
        builder: (context, snapshot) {
          // 로딩 중
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          }

          // 에러
          if (snapshot.hasError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.error_outline, size: 64, color: Colors.red),
                  SizedBox(height: 16),
                  Text(
                    '데이터를 불러오지 못했습니다',
                    style: TextStyle(fontSize: 18),
                  ),
                  SizedBox(height: 8),
                  Text(
                    '${snapshot.error}',
                    style: TextStyle(color: Colors.grey),
                  ),
                  SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () {
                      setState(() {
                        _postsFuture = _service.fetchPosts();
                      });
                    },
                    child: Text('다시 시도'),
                  ),
                ],
              ),
            );
          }

          // 성공
          final posts = snapshot.data!;
          return ListView.builder(
            itemCount: posts.length,
            itemBuilder: (context, index) {
              final post = posts[index];
              return Card(
                margin: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                child: ListTile(
                  leading: CircleAvatar(
                    child: Text('${post.id}'),
                  ),
                  title: Text(
                    post.title,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  subtitle: Text(
                    post.body,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
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

### Step 5: main.dart 연결

```dart
import 'package:flutter/material.dart';
import 'screens/posts_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '포스트 앱',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const PostsScreen(),
    );
  }
}
```

### Step 6: 실행 및 확인

```bash
flutter run
```

**확인 포인트:**
- 앱 실행 시 로딩 스피너가 나타나는가?
- 데이터 로드 후 100개의 포스트 목록이 표시되는가?
- 비행기 모드로 전환 후 재실행 시 에러 화면이 나타나는가?
- "다시 시도" 버튼이 동작하는가?

### 💡 Copilot 활용 팁

> "PostsScreen에 상세 화면으로 이동하는 기능을 추가해줘. 포스트를 탭하면 Navigator.push로 상세 화면(PostDetailScreen)으로 이동하고, 선택한 포스트의 제목과 내용을 전체 텍스트로 표시해줘."

---

<a id="part10"></a>
## 🔟 정리 [↑](#toc)

### 이 장에서 배운 것

| 개념 | 핵심 내용 |
|------|----------|
| 비동기 | 기다리는 동안 다른 일을 계속함 |
| Future | "나중에 올 값"에 대한 약속 |
| async/await | Future를 동기 코드처럼 작성하는 문법 |
| try/catch | 에러를 안전하게 처리 |
| http 패키지 | REST API 호출 |
| jsonDecode | JSON 문자열 → Dart 객체 변환 |
| FutureBuilder | 로딩/성공/에러 3상태를 위젯으로 표현 |

### 핵심 패턴 정리

```dart
// API 서비스 패턴
Future<T> fetchData() async {
  final response = await http.get(url);
  if (response.statusCode == 200) {
    return parse(response.body);
  } else {
    throw Exception('에러 메시지');
  }
}

// FutureBuilder 패턴
FutureBuilder<T>(
  future: _future,
  builder: (context, snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return LoadingWidget();
    }
    if (snapshot.hasError) {
      return ErrorWidget();
    }
    return DataWidget(snapshot.data!);
  },
)
```

### 다음 장 예고

다음 장에서는 **Custom Instructions + Prompt Files**를 배웁니다.  
AI(Copilot)에게 프로젝트 규칙을 알려주어, 더 일관된 코드를 받는 방법입니다.
