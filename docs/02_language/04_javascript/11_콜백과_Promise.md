---
title: 11. 콜백과 Promise
layout: default
grand_parent: Language
parent: JavaScript
nav_order: 11
permalink: /language/javascript/callback-promise
---


## 학습 목표

- 동기와 비동기의 차이를 설명할 수 있다
- 콜백 함수의 문제점(콜백 지옥)을 이해하고 Promise로 해결할 수 있다
- Promise의 then/catch/finally 체이닝을 활용할 수 있다

<a id="toc"></a>

## 진행 순서

1. [동기 vs 비동기](#part1) - 카페 비유: 번호표를 받고 기다리는 동안 다른 손님도 주문
2. [콜백 함수 복습](#part2) - 5장 콜백을 비동기 맥락에서 재방문
3. [콜백 지옥](#part3) - 마트료시카 인형: 열 때마다 또 인형이 나오는 문제
4. [Promise 기본](#part4) - 음식점 번호표: 주문 → 번호표 → 번호 호출 → 음식 수령
5. [Promise 체이닝](#part5) - .then().then()으로 콜백 지옥을 깔끔하게 해결
6. [Promise 정적 메서드](#part6) - all, race, allSettled 비교와 활용
7. [정리](#part7) - 핵심 개념 요약, 다음 장 미리보기, 실습 과제

---

# 11장. 콜백과 Promise

<a id="part1"></a>

## 1️⃣ 동기 vs 비동기 [↑](#toc)

자바스크립트를 처음 배울 때는 코드가 위에서 아래로 순서대로 실행됩니다.
하지만 실제 웹 앱에서는 서버에서 데이터를 받아오거나, 타이머를 걸거나,
파일을 읽는 **시간이 걸리는 작업**이 반드시 필요합니다.
이때 **비동기(asynchronous)** 처리가 등장합니다.

### 카페 비유

> **동기(synchronous)**: 카운터 직원이 한 손님의 음료를 완전히 다 만들어 줄 때까지
> 다음 손님은 줄만 서서 기다립니다. 손님이 많으면 대기 시간이 길어집니다.
>
> **비동기(asynchronous)**: 손님이 주문하면 번호표를 받고 자리에 앉습니다.
> 직원은 바로 다음 손님을 받습니다. 음료가 완성되면 번호를 불러서 전달합니다.
> 여러 손님이 동시에 기다릴 수 있어서 훨씬 효율적입니다.

### 동기 프로그래밍

코드가 한 줄씩, **위에서 아래로** 순서대로 실행됩니다.
앞 줄이 끝나야 다음 줄로 넘어갑니다.

```javascript
console.log('작업 1 시작');
console.log('작업 2 처리 중');
console.log('작업 3 완료');
```

```
// 실행 결과
작업 1 시작
작업 2 처리 중
작업 3 완료
```

순서가 보장되어 직관적이지만, 시간이 오래 걸리는 작업이 있으면
그 작업이 끝날 때까지 **모든 것이 멈춥니다(blocking)**.

### 비동기 프로그래밍

`setTimeout`은 대표적인 비동기 함수입니다.
실행을 시작해두고, 완료를 기다리지 않고 바로 다음 줄로 넘어갑니다.

```javascript
console.log('작업 1'); // 즉시 실행

setTimeout(() => {
    console.log('작업 2'); // 3초 후 실행
}, 3000);

console.log('작업 3'); // 즉시 실행 — 작업 2보다 먼저 출력됨!
```

```
// 실행 결과 (실행 순서 퀴즈)
작업 1
작업 3
작업 2   ← 3초 후에 출력됩니다
```

> 자바스크립트는 **싱글 스레드(single thread)** 언어입니다.
> 하지만 브라우저의 Web API나 Node.js 환경이 비동기 작업을 별도로 처리해주기 때문에
> 마치 동시에 여러 일을 하는 것처럼 동작합니다.

---

<a id="part2"></a>

## 2️⃣ 콜백 함수 복습 [↑](#toc)

5장에서 콜백(callback) 함수를 배웠습니다.
콜백은 **다른 함수에 인자로 전달되는 함수**입니다.
비동기 처리에서는 "작업이 끝난 후 실행할 함수"를 미리 전달해두는 방식으로 사용합니다.

### setTimeout 콜백

```javascript
// setTimeout(실행할 함수, 지연 시간(ms))
// 지연 시간이 지나면 콜백 함수를 실행합니다
setTimeout(() => {
    console.log('1초 후 메시지가 출력됩니다');
}, 1000);

console.log('이 줄이 먼저 실행됩니다');
```

```
// 실행 결과
이 줄이 먼저 실행됩니다
1초 후 메시지가 출력됩니다
```

### 파일 읽기 시뮬레이션

실제 Node.js의 파일 읽기나 서버 요청처럼, 비동기 작업이 끝난 후
결과를 콜백으로 받는 패턴을 흉내 내 봅니다.

```javascript
// 비동기 데이터 조회를 흉내 내는 함수
// 실제로는 서버 API 호출, DB 조회 등이 이 자리에 들어갑니다
function readUserData(userId, callback) {
    setTimeout(() => {
        // 2초 후 데이터를 받아왔다고 가정
        const userData = { id: userId, name: '홍길동', age: 30 };
        callback(userData); // 데이터를 콜백에 넘겨줌
    }, 2000);
}

// 콜백 함수: 데이터를 받으면 실행할 동작을 미리 정의
readUserData(1, (data) => {
    console.log(`사용자 이름: ${data.name}`);
    console.log(`나이: ${data.age}`);
});

console.log('데이터 요청 완료, 결과를 기다리는 중...');
```

```
// 실행 결과
데이터 요청 완료, 결과를 기다리는 중...
사용자 이름: 홍길동     ← 2초 후 출력
나이: 30               ← 2초 후 출력
```

이처럼 콜백은 **"나중에 호출해줘"** 라는 약속을 코드로 표현하는 방법입니다.

---

<a id="part3"></a>

## 3️⃣ 콜백 지옥 [↑](#toc)

콜백 함수 자체는 문제가 없습니다.
문제는 비동기 작업을 **순서대로** 처리해야 할 때, 콜백 안에 콜백이 중첩되면서
코드가 **오른쪽으로 계속 밀려나는** 현상이 생기는 것입니다.

### 마트료시카 비유

> 러시아 전통 인형 **마트료시카(matryoshka)** 를 생각해보세요.
> 인형을 열면 그 안에 또 인형이 있고, 그 인형을 열면 또 인형이 있습니다.
> 콜백 지옥도 마찬가지입니다. 함수를 열면 또 함수, 그 안에 또 함수...
> 무한히 중첩되어 코드를 읽거나 수정하기가 매우 힘들어집니다.

### 온라인 쇼핑몰 시나리오

로그인 → 장바구니 담기 → 결제 순서로 처리해야 하는 상황입니다.
각 단계는 **이전 단계가 완료된 후에만** 실행할 수 있습니다.

```javascript
// 각 함수는 비동기로 동작합니다 (실제 서버 통신을 흉내 냄)
function login(username, callback) {
    setTimeout(() => callback(username), 3000);
}
function addToCart(product, callback) {
    setTimeout(() => callback(product), 2000);
}
function makePayment(cardNumber, product, callback) {
    setTimeout(() => callback(cardNumber, product), 1000);
}
```

콜백으로 순서를 보장하려면 이렇게 됩니다.

```javascript
// 콜백 지옥 — 들여쓰기가 오른쪽으로 계속 밀려납니다
login('홍길동', (username) => {
    console.log(`${username}님 안녕하세요`);
    addToCart('감자', (product) => {
        console.log(`${product}를 장바구니에 넣었습니다`);
        makePayment('1234123412341234', product, (cardNumber, item) => {
            console.log(`${cardNumber.slice(0, 6)}로 ${item} 결제 완료`);
            // 여기에 다음 작업이 또 생기면... 더 깊어집니다
        });
    });
});
```

```
// 실행 결과 (총 6초 소요)
홍길동님 안녕하세요
감자를 장바구니에 넣었습니다
123412로 감자 결제 완료
```

실행 결과는 원하는 대로 나오지만, 코드에는 세 가지 심각한 문제가 있습니다.

| 문제 | 설명 |
|------|------|
| **가독성** | 들여쓰기가 깊어져 코드 흐름을 파악하기 어렵습니다 |
| **에러 처리** | 각 단계마다 에러를 따로 처리해야 해서 코드가 폭발적으로 늘어납니다 |
| **유지보수** | 단계를 추가하거나 순서를 바꾸려면 전체 구조를 다시 짜야 합니다 |

---

<a id="part4"></a>

## 4️⃣ Promise 기본 [↑](#toc)

**Promise(프로미스)** 는 ES6에서 등장한 비동기 처리를 위한 자바스크립트 내장 객체입니다.
콜백 지옥을 해결하고, 비동기 작업의 결과를 더 깔끔하게 다룰 수 있게 해줍니다.

### 음식점 번호표 비유

> 1. **주문(요청)**: 카운터에서 음식을 주문합니다
> 2. **번호표 수령(Promise 생성)**: 직원이 번호표를 건네줍니다. 이 시점엔 음식이 없습니다
> 3. **대기(pending)**: 음식을 만드는 중입니다. 번호표를 들고 자리에서 기다립니다
> 4. **번호 호출 성공(resolve)**: 음식이 완성되어 번호를 부릅니다
> 5. **음식 수령(then)**: 번호표를 내고 음식을 받습니다
> 6. **품절 안내(reject)**: 재료가 없어 만들지 못했습니다
> 7. **대안 선택(catch)**: 다른 메뉴를 선택합니다

### Promise의 3가지 상태

Promise 객체는 항상 세 가지 상태(state) 중 하나에 있습니다.

| 상태 | 의미 | 전환 조건 |
|------|------|-----------|
| **pending** (대기) | 비동기 작업이 진행 중 | 생성 직후 |
| **fulfilled** (이행) | 작업이 성공적으로 완료됨 | `resolve()` 호출 시 |
| **rejected** (거부) | 작업이 실패함 | `reject()` 호출 시 |

한 번 fulfilled나 rejected 상태가 되면 다시 변경할 수 없습니다.

### Promise 객체 생성

```javascript
// new Promise(실행 함수)
// 실행 함수(executor)는 Promise 생성과 동시에 바로 실행됩니다
const promise = new Promise((resolve, reject) => {
    // 이 안에 비동기 처리할 작업을 작성합니다
    // resolve(값)  — 성공 시 호출, fulfilled 상태로 전환
    // reject(에러) — 실패 시 호출, rejected 상태로 전환
});
```

실제 서버 데이터 조회를 흉내 낸 예시입니다.

```javascript
function getData() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const data = { name: '철수' }; // 서버에서 받아온 데이터
            // const data = null;          // 에러 상황을 테스트하려면 이 줄 사용

            if (data) {
                resolve(data);              // 성공 — fulfilled
            } else {
                reject(new Error('데이터를 받아오지 못했습니다')); // 실패 — rejected
            }
        }, 1000);
    });
}
```

### .then() / .catch() / .finally()

Promise의 결과는 `.then()`, `.catch()`, `.finally()`로 처리합니다.

```javascript
getData()
    .then((data) => {
        // resolve(data)가 호출되면 실행됩니다
        // data에는 resolve에 넘긴 값이 담겨 있습니다
        console.log(`${data.name}님 안녕하세요`);
    })
    .catch((error) => {
        // reject(error)가 호출되거나 예외가 발생하면 실행됩니다
        console.log(`오류 발생: ${error.message}`);
    })
    .finally(() => {
        // 성공이든 실패든 항상 마지막에 실행됩니다
        console.log('처리 완료');
    });
```

```
// 실행 결과 (data = { name: '철수' } 일 때)
철수님 안녕하세요
처리 완료

// 실행 결과 (data = null 일 때)
오류 발생: 데이터를 받아오지 못했습니다
처리 완료
```

---

<a id="part5"></a>

## 5️⃣ Promise 체이닝 [↑](#toc)

`.then()`은 항상 새로운 Promise를 반환합니다.
그래서 `.then().then().then()`처럼 **체이닝(chaining)** 이 가능합니다.
이 특성을 이용하면 콜백 지옥을 평탄하고 읽기 쉬운 구조로 바꿀 수 있습니다.

### 쇼핑몰 시나리오를 Promise로 리팩토링

먼저 각 함수를 Promise를 반환하도록 바꿉니다.

```javascript
// Promise를 반환하는 버전으로 재작성
function login(username) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (username) {
                resolve(username);
            } else {
                reject(new Error('아이디를 입력해 주세요'));
            }
        }, 3000);
    });
}

function addToCart(product) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (product) {
                resolve(product);
            } else {
                reject(new Error('장바구니에 넣을 상품이 없어요'));
            }
        }, 2000);
    });
}

function makePayment(cardNumber, product) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (cardNumber.length !== 16) {
                reject(new Error('잘못된 카드 번호입니다'));
                return;
            }
            resolve(product);
        }, 1000);
    });
}
```

**Before (콜백 지옥)** vs **After (Promise 체이닝)** 비교입니다.

```javascript
// Before — 콜백 지옥, 계속 오른쪽으로 밀려납니다
login('홍길동', (username) => {
    addToCart('감자', (product) => {
        makePayment('1234123412341234', product, (cardNumber, item) => {
            console.log('결제 완료');
        });
    });
});

// After — Promise 체이닝, 위에서 아래로 읽힙니다
login('홍길동')
    .then((username) => {
        console.log(`${username}님 안녕하세요`);
        return addToCart('감자'); // then에서 Promise를 return하면 다음 then으로 이어짐
    })
    .then((product) => {
        console.log(`${product}를 장바구니에 넣었습니다`);
        return makePayment('1234123412341234', product);
    })
    .then((product) => {
        console.log(`${product} 결제 완료`);
    })
    .catch((error) => {
        // 어느 단계에서 실패하든 이 catch 하나로 처리됩니다
        console.log(`오류: ${error.message}`);
    })
    .finally(() => {
        console.log('쇼핑 프로세스 종료');
    });
```

```
// 실행 결과 (정상 케이스)
홍길동님 안녕하세요
감자를 장바구니에 넣었습니다
감자 결제 완료
쇼핑 프로세스 종료
```

### 에러 전파: 체인 중간에 오류가 발생하면?

체인 중간에 `reject`가 발생하면, 이후의 `.then()`은 모두 건너뛰고
가장 가까운 `.catch()`로 바로 이동합니다.

```javascript
login('')           // 빈 문자열 — reject 발생
    .then((username) => {
        // login이 실패했으므로 이 then은 실행되지 않습니다
        return addToCart('감자');
    })
    .then((product) => {
        // 이 then도 건너뜁니다
        return makePayment('1234123412341234', product);
    })
    .then((product) => {
        // 이 then도 건너뜁니다
        console.log(`${product} 결제 완료`);
    })
    .catch((error) => {
        // login의 reject가 여기로 곧장 넘어옵니다
        console.log(`오류: ${error.message}`);
    });
```

```
// 실행 결과
오류: 아이디를 입력해 주세요
```

---

<a id="part6"></a>

## 6️⃣ Promise 정적 메서드 [↑](#toc)

Promise에는 여러 비동기 작업을 동시에 다루는 **정적 메서드(static method)** 가 있습니다.

### 예제에서 사용할 함수 준비

```javascript
// 사용자 이름 조회 — 1초 소요
function getName() {
    return new Promise((resolve) => {
        setTimeout(() => resolve('홍길동'), 1000);
    });
}

// 할일 목록 조회 — 2초 소요
function getTodo() {
    return new Promise((resolve) => {
        setTimeout(() => resolve(['청소하기', '밥먹기']), 2000);
    });
}

// 포인트 조회 — 1.5초 소요
function getPoints() {
    return new Promise((resolve) => {
        setTimeout(() => resolve(3500), 1500);
    });
}
```

### Promise.all() — 모두 완료될 때

모든 Promise가 fulfilled 되면 결과 배열을 반환합니다.
**하나라도 실패하면 즉시 reject**됩니다.
세 작업이 서로 관련 없이 독립적이면 순차 실행(1+2+1.5=4.5초) 대신
병렬 실행(최대 2초)으로 시간을 크게 줄일 수 있습니다.

```javascript
// 세 요청을 동시에 시작하고, 모두 완료되면 결과를 받습니다
Promise.all([getName(), getTodo(), getPoints()])
    .then(([name, todo, points]) => {
        // 결과 배열을 구조 분해 할당으로 받습니다
        console.log(`이름: ${name}`);
        console.log(`할일: ${todo}`);
        console.log(`포인트: ${points}`);
    })
    .catch((error) => {
        // 세 개 중 하나라도 실패하면 여기 실행됩니다
        console.log(`오류: ${error.message}`);
    });
```

```
// 실행 결과 (약 2초 소요 — 가장 오래 걸리는 getTodo 기준)
이름: 홍길동
할일: 청소하기,밥먹기
포인트: 3500
```

### Promise.race() — 가장 빠른 것

가장 먼저 완료된(성공이든 실패든) Promise의 결과를 반환합니다.
**타임아웃 구현**에 유용합니다.

```javascript
// 3초 안에 데이터를 받지 못하면 타임아웃으로 처리합니다
function timeout(ms) {
    return new Promise((_, reject) => {
        setTimeout(() => reject(new Error(`${ms}ms 초과`)), ms);
    });
}

Promise.race([getName(), timeout(500)])
    .then((result) => {
        console.log(`결과: ${result}`);
    })
    .catch((error) => {
        console.log(`실패: ${error.message}`);
    });
```

```
// 실행 결과 (getName은 1000ms, timeout은 500ms → timeout이 먼저)
실패: 500ms 초과

// getName의 지연을 300ms로 바꾸면
결과: 홍길동
```

### Promise.allSettled() — 성공/실패 관계없이 모두

모든 Promise가 완료될 때까지 기다리고,
각각의 결과(성공 또는 실패)를 배열로 반환합니다.
**일부 실패해도 나머지 결과를 계속 받고 싶을 때** 사용합니다.

```javascript
// 이름 조회는 성공, 포인트 조회는 실패하는 시나리오
function getPointsFail() {
    return new Promise((_, reject) => {
        setTimeout(() => reject(new Error('포인트 서버 오류')), 1000);
    });
}

Promise.allSettled([getName(), getPointsFail(), getTodo()])
    .then((results) => {
        results.forEach((result, index) => {
            if (result.status === 'fulfilled') {
                // 성공한 경우: { status: 'fulfilled', value: 결과값 }
                console.log(`작업 ${index + 1} 성공:`, result.value);
            } else {
                // 실패한 경우: { status: 'rejected', reason: 에러 }
                console.log(`작업 ${index + 1} 실패:`, result.reason.message);
            }
        });
    });
```

```
// 실행 결과 (약 2초 소요)
작업 1 성공: 홍길동
작업 2 실패: 포인트 서버 오류
작업 3 성공: 청소하기,밥먹기
```

### 세 메서드 비교

| 메서드 | 반환 조건 | 실패 시 동작 | 주요 사용처 |
|--------|-----------|--------------|-------------|
| `Promise.all` | 모두 성공 | 즉시 reject | 모든 데이터가 필요한 경우 |
| `Promise.race` | 가장 빠른 완료 | 가장 빠른 실패도 전달 | 타임아웃, 빠른 응답 우선 |
| `Promise.allSettled` | 모두 완료(성공/실패 무관) | 실패 포함해서 전달 | 부분 실패 허용하는 경우 |

---

<a id="part7"></a>

## 7️⃣ 정리 [↑](#toc)

### 핵심 개념 요약

| 개념 | 설명 |
|------|------|
| **동기** | 한 작업이 끝나야 다음으로 넘어가는 순차 실행 |
| **비동기** | 작업 완료를 기다리지 않고 다음 줄로 진행 |
| **콜백** | 비동기 작업 완료 후 실행할 함수를 미리 전달 |
| **콜백 지옥** | 콜백 중첩으로 인해 코드가 깊어지는 현상 |
| **Promise** | 비동기 작업의 미래 결과를 담는 객체 |
| **pending** | Promise 생성 후 완료 전 대기 상태 |
| **fulfilled** | `resolve()` 호출로 성공한 상태 |
| **rejected** | `reject()` 호출로 실패한 상태 |
| **.then()** | 성공(fulfilled) 시 실행할 콜백 등록 |
| **.catch()** | 실패(rejected) 시 실행할 콜백 등록 |
| **.finally()** | 성공/실패 무관하게 항상 마지막에 실행 |
| **체이닝** | `.then().then()` 으로 순차 비동기 처리 |

### 다음 장 미리보기

12장에서는 **async / await** 를 배웁니다.
async/await는 Promise 위에 만들어진 문법 설탕(syntactic sugar)으로,
비동기 코드를 마치 동기 코드처럼 읽기 쉽게 작성할 수 있게 해줍니다.

```javascript
// Promise 체이닝
login('홍길동')
    .then((username) => addToCart('감자'))
    .then((product) => makePayment('1234123412341234', product))
    .then((product) => console.log(`${product} 결제 완료`));

// async/await — 위와 동일한 동작, 더 읽기 쉬운 코드
async function shopping() {
    const username = await login('홍길동');
    const product  = await addToCart('감자');
    const result   = await makePayment('1234123412341234', product);
    console.log(`${result} 결제 완료`);
}
```

---

### 실습 과제

**기본** — setTimeout + 콜백으로 1초 후 메시지 출력

```javascript
// 1초 후에 "안녕하세요!"를 출력하는 코드를 작성하세요
// setTimeout과 콜백 함수를 사용합니다
setTimeout(() => {
    console.log('안녕하세요!');
}, 1000);
```

**중급** — Promise로 주사위 굴리기 (짝수면 resolve, 홀수면 reject)

```javascript
// 주사위를 굴려 짝수면 성공(resolve), 홀수면 실패(reject)하는 함수를 완성하세요
function rollDice() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const num = Math.floor(Math.random() * 6) + 1; // 1 ~ 6
            console.log(`주사위: ${num}`);
            if (num % 2 === 0) {
                resolve(`${num} — 짝수! 성공입니다`);
            } else {
                reject(new Error(`${num} — 홀수... 다시 도전하세요`));
            }
        }, 500);
    });
}

rollDice()
    .then((msg) => console.log(msg))
    .catch((err) => console.log(err.message));
```

**심화** — Promise.all로 3개의 비동기 작업을 동시에 실행하고 모든 결과 출력

```javascript
// 아래 세 함수를 Promise.all로 동시에 실행하고
// 모든 결과를 한 번에 출력하는 코드를 작성하세요
function fetchWeather() {
    return new Promise((resolve) => setTimeout(() => resolve('맑음'), 1000));
}
function fetchTemperature() {
    return new Promise((resolve) => setTimeout(() => resolve('23°C'), 800));
}
function fetchHumidity() {
    return new Promise((resolve) => setTimeout(() => resolve('55%'), 1200));
}

// 여기에 Promise.all을 사용하는 코드를 작성하세요
Promise.all([fetchWeather(), fetchTemperature(), fetchHumidity()])
    .then(([weather, temp, humidity]) => {
        console.log(`날씨: ${weather}`);
        console.log(`기온: ${temp}`);
        console.log(`습도: ${humidity}`);
    });
```

```
// 심화 과제 실행 결과 (약 1.2초 소요)
날씨: 맑음
기온: 23°C
습도: 55%
```
