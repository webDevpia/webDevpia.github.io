---
title: 13. Node.js와 npm
layout: default
grand_parent: Language
parent: JavaScript
nav_order: 13
permalink: /language/javascript/node-npm
---

## 학습 목표

- Node.js의 특징과 역할을 이해하고 서버 사이드 JavaScript를 실행할 수 있다
- npm으로 패키지를 설치, 관리하고 package.json을 이해할 수 있다

<a id="toc"></a>

## 진행 순서

1. [Node.js란?](#part1) — 브라우저 밖에서 동작하는 JavaScript 런타임
2. [Node.js 내장 모듈](#part2) — fs, path, os 실용 예시
3. [간단한 HTTP 서버](#part3) — http 모듈로 서버 직접 만들기
4. [npm이란?](#part4) — 패키지 관리자와 package.json
5. [패키지 설치와 관리](#part5) — install, dependencies, .gitignore
6. [npm 스크립트](#part6) — scripts 섹션과 nodemon
7. [정리](#part7) — 핵심 요약 및 실습 과제

---

# 13장. Node.js와 npm

<a id="part1"></a>

## 1️⃣ Node.js란? [↑](#toc)

### 브라우저 밖으로 나온 JavaScript

JavaScript는 원래 **웹 브라우저 안에서만** 동작했습니다.
Chrome 브라우저의 **V8 엔진**(자바스크립트를 기계어로 변환하는 프로그램)이 코드를 실행해 주었기 때문입니다.

**Node.js**는 이 V8 엔진을 브라우저에서 꺼내어 **어디서든 JavaScript를 실행**할 수 있게 만든 런타임(실행 환경)입니다.

> 비유: 영어 통역사(V8 엔진)가 회의실(브라우저) 안에서만 일하다가, 사무실 어디서든 일할 수 있게 된 것.

### Node.js의 주요 특징

| 특징 | 설명 |
|:-----|:-----|
| **비동기 I/O (논블로킹)** | 파일 읽기·네트워크 요청 등을 기다리지 않고 다음 코드 실행 |
| **싱글 스레드 + 이벤트 루프** | 하나의 스레드로 동시 요청 처리 — 콜백·Promise·async/await으로 관리 |
| **크로스 플랫폼** | Windows, macOS, Linux에서 동일하게 작동 |
| **npm 생태계** | 전 세계 개발자들이 만든 패키지 200만+ 개 즉시 사용 가능 |

### Node.js로 할 수 있는 것

- **웹 서버 / API 서버** — Express, Fastify 등 프레임워크 기반
- **CLI(명령줄) 도구** — 파일 처리, 자동화 스크립트
- **실시간 서비스** — 채팅, 알림 (WebSocket 기반)
- **빌드 도구** — Webpack, Vite, ESLint 등이 Node.js 위에서 동작

### 설치 확인

```bash
node -v   # Node.js 버전 확인
npm -v    # npm 버전 확인
```

```
v20.11.0
10.2.4
```

### 첫 실행

```js
// hello.js
console.log("브라우저 없이도 JavaScript가 실행됩니다!");
```

```bash
node hello.js
```

```
브라우저 없이도 JavaScript가 실행됩니다!
```

---

<a id="part2"></a>

## 2️⃣ Node.js 내장 모듈 [↑](#toc)

Node.js는 별도 설치 없이 바로 쓸 수 있는 **내장 모듈**을 제공합니다.

| 모듈 | 용도 | 대표 메서드 |
|:-----|:-----|:------------|
| **fs** | 파일 읽기·쓰기 | `readFileSync`, `writeFileSync`, `readFile` |
| **path** | 경로 처리 | `join`, `resolve`, `extname`, `basename` |
| **os** | 운영체제 정보 | `platform`, `cpus`, `homedir`, `totalmem` |
| **http** | HTTP 서버·클라이언트 | `createServer`, `request` |

### fs — 파일 읽기 + JSON 파싱

```js
// read-file.js
import fs from "fs";
import path from "path";

// 현재 파일과 같은 폴더의 data.json을 읽는다
const filePath = path.join(import.meta.dirname, "data.json");
const raw = fs.readFileSync(filePath, "utf-8"); // 동기 방식으로 파일 읽기
const data = JSON.parse(raw);                    // 문자열을 객체로 변환

console.log(data);
```

> `import.meta.dirname`은 Node.js 20.11+ 에서 사용 가능합니다.
> 이전 버전이라면 `import { fileURLToPath } from "url"` 방식을 사용합니다.

```json
// data.json
{ "name": "Alice", "age": 30 }
```

```
{ name: 'Alice', age: 30 }
```

### fs — 파일 쓰기 (비동기)

```js
// write-file.js
import fs from "fs/promises"; // Promise 기반 fs 모듈

async function saveLog(message) {
  await fs.writeFile("log.txt", message + "\n", { flag: "a" }); // 'a' = append(추가)
  console.log("로그 저장 완료");
}

saveLog("서버 시작: " + new Date().toISOString());
```

```
로그 저장 완료
```

### path / os — 경로·시스템 정보

```js
import path from "path";
import os from "os";

// path: 경로 처리
const full = "/home/user/project/src/index.js";
console.log(path.basename(full));          // index.js  (파일명)
console.log(path.extname(full));           // .js       (확장자)
console.log(path.join("src", "utils", "helper.js")); // src/utils/helper.js

// os: 운영체제 정보
console.log("플랫폼:", os.platform());          // darwin / win32 / linux
console.log("CPU 코어 수:", os.cpus().length);  // 8
console.log("메모리:", Math.round(os.totalmem() / 1024 ** 3) + "GB");
```

```
index.js
.js
src/utils/helper.js
플랫폼: darwin
CPU 코어 수: 8
메모리: 16GB
```

---

<a id="part3"></a>

## 3️⃣ 간단한 HTTP 서버 [↑](#toc)

Node.js 내장 `http` 모듈만으로 웹 서버를 만들 수 있습니다.

```js
// server.js
import http from "http";

const server = http.createServer((req, res) => {
  // req: 클라이언트 요청 정보, res: 서버 응답 객체

  if (req.url === "/") {
    // 응답 헤더 설정 (상태코드 200 = 정상, Content-Type = JSON)
    res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
    res.end(JSON.stringify({ message: "안녕하세요, Node.js 서버입니다!" }));

  } else if (req.url === "/about") {
    res.writeHead(200, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("소개 페이지입니다.");

  } else {
    // 요청한 경로가 없을 때 404 반환
    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end("Not Found");
  }
});

// 포트 3000에서 서버를 시작한다
server.listen(3000, () => {
  console.log("서버가 http://localhost:3000 에서 실행 중입니다.");
});
```

```bash
node server.js
```

```
서버가 http://localhost:3000 에서 실행 중입니다.
```

브라우저에서 `http://localhost:3000`을 열면 JSON 응답이 표시됩니다.

```json
{ "message": "안녕하세요, Node.js 서버입니다!" }
```

> 이 `http` 모듈 코드가 바로 **Express**, **Fastify** 같은 프레임워크들의 기반입니다.
> 실제 프로젝트에서는 프레임워크를 사용해 라우팅·미들웨어를 더 쉽게 처리합니다.

---

<a id="part4"></a>

## 4️⃣ npm이란? [↑](#toc)

### npm = JavaScript의 앱스토어

**npm(Node Package Manager)**은 전 세계 개발자들이 만든 JavaScript 패키지(라이브러리)를 검색·설치·관리하는 도구입니다.

> 비유: 스마트폰 앱스토어처럼, 다른 사람이 만들어 둔 도구를 검색해서 바로 설치해 쓸 수 있습니다.

- 공식 사이트: [https://www.npmjs.com](https://www.npmjs.com)
- `p` 점수: 인기도(popularity), `q` 점수: 품질(quality), `m` 점수: 유지보수(maintenance)

### package.json 생성

프로젝트 루트 폴더에서 아래 명령어를 실행하면 `package.json`이 생성됩니다.

```bash
npm init -y   # -y 옵션: 모든 질문에 기본값으로 응답
```

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "type": "module",
  "scripts": {
    "start": "node index.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

> ES Module(`import/export`)을 사용하려면 `"type": "module"`을 추가합니다.

### package.json 주요 항목

| 항목 | 설명 |
|:-----|:-----|
| **name** | 필수. 패키지명. 소문자만 허용, 대문자·공백 불가 |
| **version** | 필수. `[Major].[Minor].[Patch]` 형식 (예: `1.2.3`) |
| **description** | npm 검색 시 표시되는 설명 |
| **main** | 패키지 진입점(entry point) 파일 경로 |
| **type** | `"module"` 설정 시 ESM(`import/export`) 사용 가능 |
| **scripts** | 명령어 단축키 정의 (`npm run <이름>`으로 실행) |
| **dependencies** | 운영 환경에서 필요한 패키지 목록 |
| **devDependencies** | 개발 환경에서만 필요한 패키지 목록 |
| **keywords** | npm 검색 키워드 목록 |
| **license** | 라이선스 종류 (ISC, MIT 등) |

---

<a id="part5"></a>

## 5️⃣ 패키지 설치와 관리 [↑](#toc)

### dependencies vs devDependencies

| 구분 | 옵션 | 용도 | 예시 |
|:-----|:-----|:-----|:-----|
| **dependencies** | `npm install <패키지>` (기본) | 실제 서비스 실행에 필요 | express, axios |
| **devDependencies** | `npm install -D <패키지>` | 개발할 때만 필요 | nodemon, eslint |

```bash
npm install express          # dependencies에 추가
npm install -D nodemon       # devDependencies에 추가
npm install -g typescript    # 글로벌 설치 (시스템 전체에서 사용 가능)
```

### 의존성 일괄 설치

다른 사람의 프로젝트를 받았을 때 `package.json`에 명시된 패키지를 한 번에 설치합니다.

```bash
npm install   # 또는 npm i
```

### 패키지 삭제 / 업데이트

```bash
npm uninstall express        # 패키지 삭제
npm update express           # 최신 버전으로 업데이트
npm ls                       # 설치된 패키지 목록 확인
npx create-react-app my-app  # npx: 패키지를 설치하지 않고 일회성으로 실행 (React 등 프로젝트 생성 시 사용)
```

### 트러블슈팅

패키지 설치 중 문제가 발생하면 아래 명령어를 시도하세요.

```bash
npm cache clean --force      # npm 캐시를 강제 삭제 (설치 오류 시 시도)
npm rebuild                  # 네이티브 모듈을 다시 빌드 (OS 업데이트 후 오류 시)
```

> 💡 대부분의 설치 오류는 `node_modules` 폴더를 삭제하고 `npm install`을 다시 실행하면 해결됩니다.

### node_modules와 .gitignore

패키지를 설치하면 `node_modules` 폴더가 생성됩니다.
이 폴더는 용량이 매우 크기 때문에 **Git에 올리지 않습니다.**

```
# .gitignore
node_modules/
.env
```

> `package.json`만 공유하면 누구든 `npm install`로 동일한 환경을 재현할 수 있습니다.

### 실용 예시 1 — chalk로 터미널 컬러 출력

```bash
npm install chalk
```

```js
// colorful.js
import chalk from "chalk";

console.log(chalk.green("성공: 서버가 시작되었습니다."));  // 초록색
console.log(chalk.red("오류: 연결에 실패했습니다."));       // 빨간색
console.log(chalk.blue.bold("정보: 포트 3000"));             // 파란색 굵게
console.log(chalk.yellow("경고: API 키가 없습니다."));       // 노란색
```

```
성공: 서버가 시작되었습니다.   ← 초록색
오류: 연결에 실패했습니다.     ← 빨간색
정보: 포트 3000               ← 파란색 굵게
경고: API 키가 없습니다.       ← 노란색
```

### 실용 예시 2 — dotenv로 환경변수 관리

API 키·비밀번호 같은 민감한 정보를 코드에 직접 쓰지 않고 `.env` 파일로 분리합니다.

```bash
npm install dotenv
```

```
# .env
PORT=3000
DB_HOST=localhost
SECRET_KEY=my-secret-123
```

```js
// app.js
import "dotenv/config"; // .env 파일을 자동으로 로드

const port = process.env.PORT;          // "3000"
const dbHost = process.env.DB_HOST;     // "localhost"

console.log(`서버 포트: ${port}`);
console.log(`DB 호스트: ${dbHost}`);
```

```
서버 포트: 3000
DB 호스트: localhost
```

> `.env` 파일은 반드시 `.gitignore`에 추가해 GitHub에 올라가지 않도록 합니다.

---

<a id="part6"></a>

## 6️⃣ npm 스크립트 [↑](#toc)

`package.json`의 `scripts` 섹션에 자주 쓰는 명령어를 등록해두면 짧게 호출할 수 있습니다.

```json
{
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "build": "tsc",
    "lint": "eslint src/"
  }
}
```

### 실행 방법

```bash
npm start          # "start" 스크립트 실행 (run 생략 가능)
npm run dev        # "dev" 스크립트 실행
npm run build      # "build" 스크립트 실행
npm run lint       # "lint" 스크립트 실행
npm stop           # "stop" 스크립트 실행 (있을 경우)
```

> `start`, `stop`, `test`는 `npm start`처럼 `run` 없이 실행 가능합니다.
> 그 외 커스텀 스크립트는 `npm run <이름>` 형식을 사용합니다.

### nodemon — 코드 변경 시 자동 재시작

개발할 때 코드를 수정할 때마다 `node`를 재실행하는 번거로움을 해결합니다.

```bash
npm install -D nodemon
```

```json
{
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  }
}
```

```bash
npm run dev
```

```
[nodemon] 3.0.1
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,cjs,json
[nodemon] starting `node index.js`
서버가 http://localhost:3000 에서 실행 중입니다.
```

파일을 저장하면 자동으로 서버가 재시작됩니다.

---

<a id="part7"></a>

## 7️⃣ 정리 [↑](#toc)

### Node.js + npm 핵심 요약

| 개념 | 설명 |
|:-----|:-----|
| **Node.js** | V8 엔진 기반, 브라우저 밖에서 JavaScript 실행 가능한 런타임 |
| **이벤트 루프** | 싱글 스레드로 비동기 작업을 처리하는 핵심 메커니즘 |
| **내장 모듈** | `fs`, `path`, `os`, `http` — 설치 없이 즉시 사용 가능 |
| **npm** | JavaScript 패키지 매니저, 200만+ 개 오픈소스 패키지 제공 |
| **package.json** | 프로젝트 메타정보 + 의존성 목록 + 스크립트 단축키 정의 |
| **dependencies** | 운영 환경에 필요한 패키지 (`npm install <패키지>`) |
| **devDependencies** | 개발 시에만 필요한 패키지 (`npm install -D <패키지>`) |
| **node_modules** | 설치된 패키지 실제 파일 — `.gitignore`에 추가 필수 |
| **npm scripts** | 명령어 단축키 — `npm start`, `npm run dev` 등 |

### 다음 장 미리보기

**14장: 통합 프로젝트**에서는 지금까지 배운 JavaScript 문법, 비동기 처리, Node.js, npm을 모두 활용해 실제 동작하는 프로젝트를 완성합니다.

---

### 실습 과제

**기본** — Node.js로 파일을 읽어서 콘솔 출력하기

1. `data.json` 파일을 만들고 본인의 이름과 좋아하는 언어를 JSON으로 작성합니다.
2. `read.js`에서 `fs.readFileSync`로 파일을 읽고 `JSON.parse`로 변환한 뒤 `console.log`로 출력합니다.

```js
// 기대 출력 예시
{ name: '김철수', language: 'JavaScript' }
```

---

**중급** — npm 프로젝트 생성 + chalk로 컬러 출력하기

1. 새 폴더를 만들고 `npm init -y`로 `package.json`을 생성합니다.
2. `npm install chalk`로 chalk 패키지를 설치합니다.
3. `package.json`에 `"type": "module"`을 추가합니다.
4. `index.js`를 작성해 초록·빨강·파랑 메시지를 각각 출력합니다.
5. `package.json`의 `scripts`에 `"start": "node index.js"`를 추가하고 `npm start`로 실행합니다.

---

**심화** — HTTP 서버로 JSON 데이터 응답하기

1. `npm init -y`로 프로젝트를 초기화하고 `"type": "module"`을 추가합니다.
2. `npm install -D nodemon`으로 nodemon을 설치합니다.
3. `server.js`를 작성해 아래 두 엔드포인트(URL 경로)를 구현합니다.
   - `GET /` → `{ "message": "Hello" }` 응답
   - `GET /users` → 사용자 배열 JSON 응답
4. `package.json` scripts에 `"dev": "nodemon server.js"`를 추가하고 `npm run dev`로 실행합니다.
5. 브라우저 또는 `curl http://localhost:3000/users`로 결과를 확인합니다.
