---
title: JavaScript
layout: default
parent: Language
nav_order: 4
has_children: true
permalink: /language/javascript
---


## 학습 목표

- JavaScript가 무엇이고 어디에 사용되는지 설명할 수 있다
- VSCode + Node.js 개발 환경을 설정하고 첫 코드를 실행할 수 있다

<a id="toc"></a>

## 진행 순서

1. [JavaScript란?](#part1) - 프로그래밍 언어 소개와 역사
2. [JavaScript로 할 수 있는 것](#part2) - 프론트엔드, 백엔드, 모바일 등 활용 분야
3. [실행 환경 이해](#part3) - 브라우저 vs Node.js 차이
4. [개발 환경 설정](#part4) - Node.js 설치, VSCode 설정, 추천 확장 프로그램
5. [첫 JavaScript 코드 실행](#part5) - 브라우저 콘솔, Node.js, .js 파일 3가지 방법
6. [정리](#part6) - 핵심 개념 요약 및 다음 장 미리보기

---

# 01장. JavaScript 시작하기

<a id="part1"></a>

## 1️⃣ JavaScript란? [↑](#toc)

**JavaScript**는 웹 브라우저(Chrome, Safari 등)에서 동작하는 프로그래밍 언어로,
웹페이지에 **움직임과 상호작용**을 부여합니다.

### 건물 비유

> HTML이 건물의 뼈대, CSS가 외관 디자인이라면,
> **JavaScript는 건물 안의 엘리베이터, 자동문, 조명 센서** — 움직임과 상호작용을 담당합니다.

| 기술 | 역할 | 비유 |
|------|------|------|
| HTML | 웹페이지의 구조와 내용 | 건물의 뼈대 |
| CSS | 색상, 폰트, 레이아웃 등 시각적 스타일 | 건물의 외관 디자인 |
| **JavaScript** | 버튼 클릭, 데이터 처리, 애니메이션 등 동작 | 엘리베이터, 자동문, 조명 센서 |

---

### 역사

- **1995년**: Brendan Eich(브랜든 아이크)가 단 **10일 만에** 만든 언어
- **1996년**: Netscape(넷스케이프) 브라우저에 최초 탑재
- **2009년**: Node.js 등장 — 브라우저 밖에서도 실행 가능해짐
- **현재**: 세계에서 가장 많이 사용되는 프로그래밍 언어 (Stack Overflow 개발자 설문 13년 연속 1위)

---

### Java와 JavaScript는 다른 언어입니다

> **Java와 JavaScript는 이름만 비슷할 뿐, 완전히 다른 언어입니다.**
> 마치 "햄"과 "햄스터"가 다른 것처럼, 이름의 유사성은 마케팅 전략에서 비롯된 것입니다.

| | Java | JavaScript |
|---|------|-----------|
| 주요 용도 | 안드로이드 앱, 기업용 서버 | 웹 브라우저, 웹 서버 |
| 실행 방식 | JVM(자바 가상 머신) 위에서 실행 | 브라우저 또는 Node.js에서 실행 |
| 타입 | 정적 타입 (컴파일 시 타입 확정) | 동적 타입 (실행 중 타입 결정) |

---

<a id="part2"></a>

## 2️⃣ JavaScript로 할 수 있는 것 [↑](#toc)

JavaScript는 처음에는 웹 브라우저 전용 언어였지만, 지금은 거의 모든 분야에서 활용됩니다.

| 분야 | 설명 | 예시 |
|------|------|------|
| 웹 프론트엔드 | 웹페이지에 동적 기능 추가 | 버튼 클릭, 애니메이션, 폼 검증 |
| 웹 백엔드 | 서버 프로그램 개발 | Node.js로 API 서버 구축 |
| 모바일 앱 | 스마트폰 앱 개발 | React Native |
| 데스크톱 앱 | PC 프로그램 개발 | Electron (VSCode도 JS로 만듦!) |
| AI/ML | 머신러닝 | TensorFlow.js |

> **하나의 언어로 이 모든 것을 할 수 있다는 것**이 JavaScript의 가장 큰 강점입니다.
> 웹 프론트엔드부터 시작해서 백엔드, 앱까지 확장할 수 있습니다.

---

<a id="part3"></a>

## 3️⃣ 실행 환경 이해 [↑](#toc)

### 통역사 비유

> JavaScript는 외국어처럼 **'통역사'가 필요합니다**.
> 브라우저와 Node.js가 바로 그 통역사입니다.

JavaScript 코드 자체는 텍스트 파일입니다. 이 텍스트를 컴퓨터가 이해할 수 있도록
**해석(interpret)해주는 환경**이 필요한데, 대표적으로 두 가지가 있습니다.

| | 브라우저 | Node.js |
|---|---------|---------|
| 역할 | 웹페이지에서 JS 실행 | 컴퓨터에서 직접 JS 실행 |
| DOM 접근 | ✅ 가능 | ❌ 불가 |
| 파일 시스템 | ❌ 불가 (보안) | ✅ 가능 |
| 사용 예 | 버튼 클릭, 페이지 변경 | 서버, 스크립트, 자동화 |

> **DOM(Document Object Model)이란?**
> 웹페이지의 HTML 요소들을 JavaScript로 제어할 수 있도록 트리 구조로 표현한 것입니다.
> "버튼 텍스트를 바꾼다", "이미지를 숨긴다" 같은 동작이 DOM을 통해 이루어집니다.

**이 강의에서는 두 환경 모두 사용합니다.**
- **1~4장**: 브라우저 콘솔로 빠르게 실습
- **5장 이후**: VSCode + Node.js로 실제 개발 방식으로 진행

---

<a id="part4"></a>

## 4️⃣ 개발 환경 설정 [↑](#toc)

### 1단계: Node.js 설치

1. [https://nodejs.org/](https://nodejs.org/) 접속
2. **LTS(Long Term Support)** 버전 다운로드 (안정적인 장기 지원 버전)
3. 설치 완료 후 터미널(Terminal)에서 확인:

```bash
node -v    # v22.x.x 이상 확인
npm -v     # 10.x.x 이상 확인
```

실행 결과:
```
v22.11.0
10.9.0
```

> **npm(Node Package Manager)이란?**
> JavaScript 라이브러리(다른 사람이 만든 코드 묶음)를 설치하고 관리하는 도구입니다.
> Node.js 설치 시 자동으로 함께 설치됩니다.

---

### 2단계: VSCode 설치

1. [https://code.visualstudio.com/](https://code.visualstudio.com/) 접속
2. 운영체제에 맞는 버전 다운로드 후 설치

**VSCode(Visual Studio Code)**는 Microsoft가 만든 무료 코드 편집기로,
JavaScript 개발에 가장 널리 사용됩니다.

---

### 3단계: 추천 확장 프로그램 설치

VSCode 왼쪽 사이드바의 확장 아이콘(Extensions)을 클릭하거나 `Ctrl+Shift+X`로 검색합니다.

| 확장 프로그램 | 용도 | 설치 필수 여부 |
|-------------|------|-------------|
| ESLint | 코드 오류 실시간 검사 | 필수 |
| Prettier | 자동 코드 정리 | 필수 |
| Error Lens | 에러를 코드 줄 옆에 표시 | 추천 |
| Live Server | HTML 파일 자동 새로고침 | 추천 (9장~) |

> **ESLint**는 코드의 문법 오류나 잠재적 버그를 미리 알려주는 도구입니다.
> **Prettier**는 들여쓰기, 따옴표 스타일 등 코드 형식을 자동으로 통일해줍니다.
> 두 도구 모두 실무에서 거의 필수로 사용됩니다.

---

<a id="part5"></a>

## 5️⃣ 첫 JavaScript 코드 실행 [↑](#toc)

JavaScript를 실행하는 방법은 여러 가지입니다. 3가지 방법을 순서대로 실습해봅니다.

---

### 방법 1: 브라우저 콘솔 (설치 없이 바로 실행)

가장 빠르게 코드를 테스트할 수 있는 방법입니다.

```
1. Chrome 또는 Edge 브라우저 열기
2. F12 (또는 Ctrl+Shift+I / Mac: Cmd+Option+I) 눌러 개발자 도구 열기
3. 상단 탭에서 "Console" 클릭
4. 아래 코드를 한 줄씩 입력하고 Enter
```

```javascript
// 브라우저 콘솔에서 직접 입력해보세요
// console.log()는 괄호 안의 내용을 콘솔에 출력하는 함수입니다
console.log("안녕하세요, JavaScript!");
2 + 3
"안녕" + "하세요"
```

실행 결과:
```
안녕하세요, JavaScript!
5
'안녕하세요'
```

> **주석(Comment)이란?**
> `//` 이후의 텍스트는 JavaScript 엔진이 무시합니다. 코드에 설명을 달 때 사용합니다.
> 나중에 코드를 다시 볼 때, 또는 다른 사람이 코드를 읽을 때 이해를 돕습니다.

---

### 방법 2: Node.js REPL

**REPL(Read-Eval-Print Loop)**은 코드를 한 줄씩 입력하면 즉시 실행 결과를 보여주는 대화형 실행 환경입니다.

```bash
# 터미널을 열고 node 입력
node
```

```javascript
// Node.js REPL에서 입력 (> 는 프롬프트, 직접 입력하지 않습니다)
> console.log("Node.js에서 실행!");
Node.js에서 실행!
> 10 * 5
50
> "Hello" + " " + "World"
'Hello World'
> .exit    // 종료 명령어
```

실행 결과:
```
Node.js에서 실행!
undefined
50
'Hello World'
```

> `console.log()` 다음 줄에 `undefined`가 출력되는 것은 정상입니다.
> REPL은 모든 표현식의 반환값을 출력하는데, `console.log()`는 출력 후 `undefined`를 반환합니다.

---

### 방법 3: .js 파일로 실행 (실무 방식)

실제 개발에서 사용하는 방법입니다. VSCode에서 파일을 만들고 Node.js로 실행합니다.

```
1. VSCode 실행
2. 새 폴더 생성 (예: js-practice)
3. VSCode에서 해당 폴더 열기 (File → Open Folder)
4. 새 파일 생성: hello.js
5. 아래 코드 작성 후 저장 (Ctrl+S)
```

```javascript
// hello.js — 나의 첫 JavaScript 파일

// console.log()는 화면에 메시지를 출력하는 함수입니다
// 프로그래밍의 "Hello World"는 모든 언어의 전통적인 첫 코드입니다
console.log("Hello, JavaScript!");
console.log("1 + 2 =", 1 + 2);
console.log("오늘부터 자바스크립트를 시작합니다!");
```

```bash
# VSCode 터미널에서 실행 (Ctrl+` 로 터미널 열기)
node hello.js
```

실행 결과:
```
Hello, JavaScript!
1 + 2 = 3
오늘부터 자바스크립트를 시작합니다!
```

---

### 어떤 방법을 사용해야 할까요?

> - **빠른 실험**: 브라우저 콘솔 (1~2줄 코드 테스트)
> - **간단한 실습**: Node.js REPL (변수, 연산 즉시 확인)
> - **실제 개발**: .js 파일 + VSCode (이 강의의 주요 방식)

---

<a id="part6"></a>

## 6️⃣ 정리 [↑](#toc)

### 핵심 개념 요약

| 개념 | 설명 | 비유 |
|------|------|------|
| JavaScript | 웹의 동작을 담당하는 프로그래밍 언어 | 건물의 엘리베이터, 자동문 |
| 브라우저 | JS를 웹에서 실행하는 환경 | 통역사 A |
| Node.js | JS를 컴퓨터에서 실행하는 환경 | 통역사 B |
| console.log() | 화면에 메시지를 출력하는 함수 | "말하기" 기능 |
| 주석 (`//`) | 코드에 설명을 추가하는 텍스트, 실행되지 않음 | 코드의 메모지 |

---

### 다음 장 미리보기

| 장 | 내용 |
|---|---|
| 2장 | 변수와 데이터 타입 — `let`, `const`, string, number 등 |
| 3장 | 연산자와 조건문 — `if/else`로 판단하기 |
| 4장 | 반복문과 배열 기초 — `for` 루프로 반복하기 |

---

### 실습 과제

**기본**: 브라우저 콘솔에서 자신의 이름을 `console.log()`로 출력해보세요.

**중급**: `hello.js`에 5줄의 `console.log()`를 작성하여 자기소개를 출력해보세요.

**심화**: 아래 코드를 브라우저 콘솔이나 Node.js REPL에서 실행하고 결과를 확인해보세요. (2장에서 배울 "데이터 타입" 미리보기입니다!)

```javascript
// typeof는 값의 타입(종류)을 문자열로 반환하는 연산자입니다
console.log(typeof "안녕");   // 문자열의 타입은?
console.log(typeof 42);       // 숫자의 타입은?
console.log(typeof true);     // 참/거짓의 타입은?
```

실행 결과:
```
string
number
boolean
```
