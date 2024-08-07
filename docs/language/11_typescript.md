---
title: typescript
layout: default
parent: Language
# nav_order: 1
# permalink: /language/emmet
# nav_exclude: true
# search_exclude: true
---

# 타입스크립트

마이크로소프트가 개발하고 유지하는 오픈소스 프로그래밍 언어. 2012년 발표  
c#을 창시한 아네르스 하일스베르(Anders Hejlsberg)가 핵심 개발자로 참여.  
구글 Angular.js팀이 앵귤로 버전2를 만들면서 타입스크립트를 채택한 이후 널리 알려짐.

## js에서 타입 기능

```js
function makePerson(name, age) {}

makePerson(32, "Jack")
```

```js
function makePerson(name: string, age: number) {}

makePerson(32, "Jack")
```

## 1. 타입스크립트 프로젝트 작성

### 1. 타입스크립트 컴파일러 설치 후 확인

설치 후 버전 확인

```bash
npm i -g typescript
tsc -v
```

ch01폴더 생성 후, hello.ts 파일 생성 

```ts
console.log("hello world!")
```

터미널에서 

```bash
tsc hello.ts
```

ch01폴더에 hello.js파일 생성됨.  

js파일을 실행시킴.

```bash
node hello.js
```
tsc는 타입스크립트 코드를 자바스크립트 코드로 변환만 한다.

ts-node설치

```bash
npm i -g ts-node
ts-node -v
ts-node hello.ts
```

ts-node는 컴파일과 실행을 동시 진행한다. 자바스크립트로 코드 변환은 안함.

### 2. 타입스크립트 프로젝트 생성하기

작업폴더를 생성하고 프로젝트 초기화 작업을 진행하는 경우

```bash
mkdir ch02-1
cd ch02-1
npm init -y
npm i -D typescript ts-node
npm i -D @types/node
```

이미 생성된 코드를 받아서 작업하는 경우, 코드는 github에 올려 놓치만 node_modules폴더는 올리지 않으므로 package.json파일에 있는 내용에 따라 다시 다운로드 받는 작업을 한다. 

```bash
npm i
```

### 3. tsconfig.json파일만들기

타입스크립트 프로젝트는 타입스크립트 컴파일러의 설정 파일인 tsconfig.json파일이 있어야 한다.

```bash
tsc --init
```

tsconfig.json에서 아래 내용 주석 제거

```ts
    "outDir": "dist",            
```

### 4. src디렉토리와 소스파일 작성

```bash
mkdir -p src/utils
touch src/index.ts src/utils/makePerson.ts
```

src/utils/makePerson.ts
```ts
export function makePerson(name: string, age: number) {
  return { name: name, age: age }
}
export function testMakePerson() {
  console.log(makePerson('Jane', 22), makePerson('Jack', 33))
}
```

src/index.ts
```ts
import { testMakePerson } from './utils/makePerson'
testMakePerson()
```

### 5. package.json 수정
```ts
 "main": "index.js",
  "scripts": {
    "dev": "ts-node src",
    "build":"tsc && node dist"
  },
```

```bash
# 타입스크립트 파일을 컴파일하고 실행
npm run dev

# 컴파일한 결과 파일을 dist폴더에 생성 하고 실행
npm run build
```

## 2. 모듈

### 1. 모듈

타입스크립트에서 index.ts와 같은 소스 파일을 모듈이라고 한다.  
필요한 내용을 하나의 파일에 다 넣을 수 있지만 코드의 유지.보수 측면에서 소스코드를 분할한다. 이러한 작업을 모듈화(modulization)라고 한다.  

/src/index.ts
```ts
let MAX_AGE = 100

interface IPerson {
  name: string,
  age: number
}

class Person implements IPerson {
  constructor(public name: string, public age: number) {}
}

function makeRandomNumber(max:number = MAX_AGE):number{
	return Math.ceil((Math.random() * max))
}

const makePerson = 
(name: string,	age:number = makeRandomNumber()) => ({name, age})

const testMakePerson = (): void => {
  let jane: IPerson = makePerson("Jane");
  let jack: IPerson = makePerson("Jack");
  console.log(jane, jack);
}

testMakePerson();
```

```bash
npm run dev
```

### 2. index.ts파일의 모듈화

앞에 파일은 모듈화하기 위해 Person.ts을 하나 만들어 준다.

/src/Person.ts
```ts
let MAX_AGE = 100

interface IPerson {
  name: string,
  age: number
}

class Person implements IPerson {
  constructor(public name: string, public age: number) {}
}

function makeRandomNumber(max:number = MAX_AGE):number{
	return Math.ceil((Math.random() * max))
}

const makePerson = 
(name: string,	age:number = makeRandomNumber()) => ({name, age})
```

/src/index.ts
```ts
const testMakePerson = (): void => {
  let jane: IPerson = makePerson("Jane");
  let jack: IPerson = makePerson("Jack");
  console.log(jane, jack);
}

testMakePerson();
```

분리 후 실행을 해보면 IPerson, makePerson을 찾을 수 없다고 오류 발생한다.
export와 import 구문을 통해 해결 

### 3. export 키워드

앞에서 작성한 index.ts파일이 동작하려면 Person.ts 파일에 선언한 IPerson과 makePerson이란 심벌의 의미를 index.ts에 전달해야 한다.  이 때 export 키워드를 사용한다.

Person.ts파일에서 IPerson, makePerson 선언부에 export키워드를 추가  
export 키워드는 interface, class, type, let, const 키워드 앞에 붙일 수 있다.

/src/Person.ts
```ts
let MAX_AGE = 100

export interface IPerson {
  name: string,
  age: number
}

class Person implements IPerson {
  constructor(public name: string, public age: number) {}
}

function makeRandomNumber(max:number = MAX_AGE):number{
	return Math.ceil((Math.random() * max))
}

export const makePerson = 
(name: string,	age:number = makeRandomNumber()) => ({name, age})
```

### 4. import 키워드

어떤 파일이 export 키워드로 내보낸 심벌을 받아서 사용하려면 import 키워드로 해당 심벌을 불러와야 한다. 

```ts
import {심벌 목록} from  '파일 상대 경로'
import * as 심벌 from '파일 상대 경로'
```

/src/index.ts
```ts
import {IPerson, makePerson} from './person/Person'

const testMakePerson = (): void => {
  let jane: IPerson = makePerson("Jane");
  let jack: IPerson = makePerson("Jack");
  console.log(jane, jack);
}

testMakePerson();
```

#### import * as 구문

/src/utils/makeRandomNumber.ts
```ts
let MAX_AGE = 100;

export function makeRandomNumber(max: number = MAX_AGE): number {
  return Math.ceil((Math.random() * max))
}
```
Person.ts 파일을 열고 첫 줄에 import * as 구문을 작성  

/src/person/Person.ts
```js
import {makeRandomNumber} as U from '../utils/makeRandomNumber'
import IPerson from './IPerson'

export default class Person implements IPerson {
  constructor(public name: string, public age: number = makeRandomNumber()) {}
}

export const makePerson = (name: string, 
                          age:number = U.makeRandomNumber()): IPerson => ({name, age});
```
#### export default 키워드

한 모듈에서 오직 하나만 붙일 수 있다.
export default 붙은 항목은 import로 불러 올 때 중괄호 {} 없이 사용할 수 있다.

```ts
export default class Person implements IPerson {...}
```

```ts
import IPerson, {makePerson} from './person/Person'
```

### 5. tsconfig.json 파일 살펴보기

```bash
tsc --help
```

compilerOptions 항목은 tsc명령 형식에서 옵션을 나타냄.  
include 항목은 대상 파일 목록을 나타냄.  
"include" 항목에서 ["src/**/*"]는 src디렉토리는 물론 그 하위 디렉토리에 있는 모든 파일을 컴파일 대상으로 포함한다는 의미임.  

```json
{
  "compilerOptions": {
    "module": "commonjs",
    "esModuleInterop": true,
    "target": "es2015",      
    "moduleResolution": "node",      
    "outDir": "dist",
    "baseUrl": ".",
    "sourceMap": true,
    "downlevelIteration": true,
    "noImplicitAny": false,
    "paths": { "*": ["node_modules/*"] }
  },
  "include": ["src/**/*"]
}
```
#### compilerOptions (컴파일러 옵션)

"module": "commonjs"
> CommonJS 모듈 시스템을 사용하도록 지정합니다.  웹(amd), node(commonjs)

"esModuleInterop": true
> ES 모듈 및 CommonJS 모듈 간의 상호 운용성을 향상시키기 위해 ES 모듈 인터옵을 활성화합니다.  오픈소스 자바스크립트 라이브러리 중에는 웹 브라우저에서 동작한다는 가정으로 만들어진 것들이 있는데, 이들은 CommonJS방식으로 동작하는 타입스크립트 코드에 혼란을 줄 수 있다. 이에 해당하는 패키지가 동작하려면 해당 키값이 true로 설정되어 있어야 한다.

"target": "es2015"
> ECMAScript 2015(ES6)를 대상으로 하는 JavaScript 코드를 생성하도록 지정합니다.

"moduleResolution": "node"
> 모듈 해상도 방법으로 Node.js 스타일을 사용하도록 지정합니다.

"outDir": "dist"
> 컴파일된 파일들을 저장할 디렉토리를 "dist"로 설정합니다.

"baseUrl": "."
> 상대 경로 모듈을 해석할 때의 기준 경로를 프로젝트 루트로 설정합니다.

"sourceMap": true
> 소스 맵 파일을 생성하도록 지정하여 디버깅을 용이하게 합니다.

"downlevelIteration": true
> ES6 이전의 반복 프로토콜을 사용하는 코드를 ES3/ES5에서 실행되도록 설정합니다.

"noImplicitAny": false
> 암시적인 'any' 타입 사용을 허용합니다.

"paths": { "*": ["node_modules/*"] }
> 모듈 경로에 대한 별칭을 설정합니다. 여기서는 ''(모든 모듈)에 대한 경로를 'node_modules/'로 지정합니다.

#### include (포함할 파일 및 디렉토리 목록)

"src/**/*"
> 프로젝트에 포함시킬 TypeScript 소스 코드가 있는 디렉토리를 지정합니다. 여기서는 "src" 디렉토리 및 그 하위 모든 파일을 포함합니다.

## 3. 변수 선언문

### 1. 타입 주석(type annotation)

타입 스크립트는 자바스크립트 변수 선언문을 확장해 다음과 같은 형태로 타입을 명시할 수 있다. 

```ts
let 변수명:타입 [=초깃값]
const 변수명:타입 = 초깃값
```

```ts
let n: number = 1
let b: boolean = true
let s: string = 'hello'
let o: object = {}
```

선언된 타입과 다른 타입의 값으로 변수값을 바꾸려고 하면 오류 발생

```ts
n = 'a'
b = 1
s = false
o = {name:'Jack',age:32}
```

### 2. 타입추론

타입스크립트는 자바스크립트와 호환성을 위해 타입 주석 부분을 생략할 수 있다. 타입스크립트 컴파일러는 다음과 같은 코드를 만나면 대입 연산자 = 오른쪽 값에 따라 변수의 타입을 지정한다.

```ts
// string으로 판단
let n = 'a'
// number로 판단
let b = 1
// boolean으로 판단
let s = false
// object로 판단
let o = {name:'Jack',age:32}

// n은 string이므로 오류발생
n = 1
```

### 3. any 타입

자바스크립트와의 호환을 위해 any 타입 제공

```ts
let a: any = 0
a = 'hello'
a = true
a = {}
```

### 4. undefined 타입

자바스크립트에서 변수를 초기화하지 않으면 해당 변수는 undefined값을 가진다. 타입스크립트에서는 undefined는 타입이기도 하고 값이기도 하다.

```ts
let u: undefined = undefined
// Type '1' is not assignable to type 'undefined' 오류 발생
u = 1 
```

### 5. 템플릿 문자열 제공

```ts
`${변수이름}`
```

## 4. 객체와 인터페이스

### 1. 인터페이스

객체의 타입을 정의

```ts
interface 인터페이스 이름 {
	속성이름[?]: 속성타입[,...]
}
```

```ts
interface IPerson {
  name: string
  age: number
}

let good: IPerson = { name: 'Jack', age: 32 }

// age 속성이 없으므로 오류
// let bad1: IPerson = {name: "Jack"}; 

// name 속성이 없으므로 오류
// let bad2: IPerson = {age: 32}; 

// name 과 age 속성이 모두 없으므로 오류
// let bad3: IPerson = {}; 

// etc란 속성이 있으므로 오류
// let bad4: IPerson = { name: "Jack", age: 32, etc: true}; 

```
### 2. 선택 속성 구문

인터페이스 설계할 때 어떤 속성은 반드시 있어야 하지만, 어떤 속성은 있어도 되고 없어도 되는 형태로 만들고 싶을 경우 이러한 속성을 선택속성이라고 하고 속성이름 뒤에 물음표 기호를 붙여서 만듬.

```ts
interface IPerson2 {
  name: string
  age: number
  etc?: boolean
}

let good1: IPerson2 = { name: 'Jack', age: 32 }

let good2: IPerson2 = { name: 'Jack', age: 32, etc: true } 
```

### 3. 익명 인터페이스

타입스크립트는 interface 키워드도 사용하지 않고 인터페이스의 이름도 없는 인터페이스를 만들 수 있다. 이를 익명 인터페이스 라고 한다.


```ts
let ai: {
  name: string
  age: number
  etc?: boolean
} = { name: 'Jack', age: 32 }

// 익명 인터페이스는 주로 다음처럼 함수를 구현할 때 사용
function printMe(me: { name: string; age: number; etc?: boolean }) {
  console.log(me.etc ? `${me.name} ${me.age} ${me.etc}` : `${me.name} ${me.age}`)
}
printMe(ai)
```

### 4. 클래스

클래스 속성은 public,private,protect와 같은 접근제한자를 이름 앞에 붙일 수 있음. 생략시 public으로 간주함.

```ts
class 클래스명 {
	[ private | protected | public ] 속성이름[?]: 속성타입[...]
}
```

```ts
// @ts-nocheck
class Person1 {
	name: string
	age?: number
}

let jack1: Person1 = new Person1()
jack1.name = 'Jack'
jack1.age = 32
console.log(jack1)
```

### 5. 생성자

타입스크립트 클래스는 constructor라는 매서드를 포함하는데, 이를 생성자라고 한다.

```ts
class Person2 {
  constructor(public name: string, public age?: number) {}
}

let jack2: Person2 = new Person2('Jack', 32)
console.log(jack2)
```

```ts
class Person3 {
  name: string
  age?: number
  constructor(name: string, age?: number) {
    this.name = name
    this.age = age
  }
}
let jack3: Person3 = new Person3('Jack', 32)
console.log(jack3)
```

### 6. 인터페이스 구현

다른 객체지향 언어와 마찬가지로 타입스크립트 클래스는 인터페이스를 구현할 수 있습니다. 클래스가 인터페이스를 구현할 때는 다음처름 implements 키워드를 사용한다.

```ts
class 클래스명 implements 인터페이스명 {

}
```

```ts
interface IPerson4 {
  name: string
  age?: number
}

class Person4 implements IPerson4 {
  constructor(public name: string, public age?: number) {}
}

let jack4: IPerson4 = new Person4('Jack', 32)
console.log(jack4) // Person4 { name: 'Jack', age: 32 }
```

### 7. 추상클래스

타입스크립트는 다른 언어처럼 abstract 키워드를 사용해 추상 클래스를 만들 수 있다.  추상 클래스는 다음처럼 abstract 키워드를 class 키워드 앞에 붙여서 만든다. 추상 클래스는 자신의 속성이나 메서드 앞에 abstract를 붙여 나를 상속하는 다른 클래스에서 이 속성이나 메서드를 구현하게 한다.

```ts
abstract class 클래스명 {
	abstract 속성명: 속성타입
	abstract 메서드명(){}
}
```

다음 AbstractPerson5는 name 속성 앞에 abstract가 붙었으므로 new 연산자를 적용해 객체를 만들 수 없다.

```ts
abstract class AbstractPerson5 {
  abstract name: string
  constructor(public age?: number) {}
}

class Person5 extends AbstractPerson5 {
  constructor(public name: string, age?: number) {
    super(age)
  }
}

// let jane:AbstractPerson5 = new AbstractPerson5('jane')

let jack5: Person5 = new Person5('Jack', 32)

console.log(jack5) 
// Person5 { name: 'Jack', age: 32 }
```

### 8. 클래스 상속

객체지향 언어는 부모 클래스를 상속받는 상속 클래스를 만들 수 있는데, 타입스크립트는 다음 처럼 extends 키워드를 사용해 상속 클래스를 만듭니다.

```ts
class 상속클래스 extends 부모클래스 {

}
```
다음 클래스는 AbstractPerson5 추상 클래스를 상속해 AbstractPerson5가 구현한 age를 얻고, AbstractPerson5를 상속받는 클래스가 구현해야 할 name 속성을 구현한다. 
참고로 타입스크립트에서는 부모 클래스의 생성자를 super 키워드로 호출할 수 있다.

```js
abstract class AbstractPerson5 {
  abstract name: string
  constructor(public age?: number) {}
}
class Person5 extends AbstractPerson5 {
  constructor(public name: string, age?: number) {
    super(age)
  }
}
// let jane:AbstractPerson5 = new AbstractPerson5('jane')
let jack5: Person5 = new Person5('Jack', 32)
console.log(jack5) // Person5 { name: 'Jack', age: 32 }

```
### 9. static 속성

다른 객체지향 언어처럼 타입스크립트 클래스는 정적인 속성을 가질 수 있다. 클래스의 정적 속성은 다음과 같은 형태로 선언한다.

```ts
class 클래스명 {
	static 정적속성명: 속성타입
}
```

```ts
class A {
  static initValue = 1
}

let initVal = A.initValue // 1
```

### 10. 객체의 비구조화 할당문

#### 구조화

다음 코드는 name과 age라는 단어가 각기 다른 의미로 사용되므로 personName, companyName처럼 이 둘을 구분하고 있다.

```ts
let personName = 'Jack'
let personAge = 32

let companyName = 'Apple Company, Inc'
let companyAge = 43
```

그런데 코드를 이런 방식으로 구현하면 작성하기도 번거롭고 기능을 확장하기도 어렵다. 따라서 다음처럼 인터페이스나 클래스를 사용해 관련된 정보를 묶어 새로운 타입으로 표현한다. 이를 구조화라고 한다.

```ts
export interface IPerson {
  name: string
  age: number
}

export interface ICompany {
  name: string
  age: number
}
```
코드를 이처럼 구조화하면 다음 코드에서 보듯 jack이나 apple은 물론 jane이나 ms와 같은 비슷한 유형의 변수를 쉽게 만들 수 있다. 이로써 코드이 확장이 수월해 진다.

```ts
import { IPerson, ICompany } from './IPerson_ICompany'

let jack: IPerson = { name: 'Jack', age: 32 },
  jane: IPerson = { name: 'Jack', age: 32 }

let apple: ICompany = { name: 'Apple Computer, Inc', age: 43 },
  ms: ICompany = { name: 'Microsoft', age: 44 }

```

#### 비구조화
구조환된 데이터는 어떤 시점에서 데이터의 일부만 사용해야 할 때가 있다. 다음 코드는 구조화된 jack 변수에서 jack이 아닌 jack.name, jack.age 부분을 각각 name과 age 변수에 저장한다. 그런데 이 시점부터는 jack 변수는 더 사용하지 않고 그 대신 name과 age 변수만 사용한다. 이처럼 구조화된 데이터를 분해하는 것을 비구조화라고 한다.

```ts
let name = jack.name, age = jack.age
```

#### 비구조화 할당

비구조화 할당은 ESNext 자바스크립트의 구문으로 타입스크립트에서도 사용할 수 있다. 비구조화 할당은 객체와 더불어 배열과 튜플에도 적용할 수 있다. 비구조화 할당을 객체에 적용하려면 얻고 싶은 속성을 중괄호를 묶는다.

```ts
let {name, age} = jack
```

name과 age 변수가 새롭게 만들어지고 name 변수는 jack.name의 값, age 변수는 jack.age의 값을 각각 초깃값으로 할당받는다.

```ts
import { IPerson } from './IPerson_ICompany'

let jack: IPerson = { name: 'Jack', age: 32 }
let { name, age } = jack
console.log(name, age) // Jack 32
```

#### 잔여 연산자(rest operator) 

ESNext 자바스크립트와 타입스크립트는 점을 연이어 3개 사용하는 ... 연산자를 제공합니다. 이 연산자는 사용되는 위치에 따라 잔여 연산자 혹은 전개 연산자라고 한다.

다음 코드에서 address 변수는 5개 속성을 가지고 있는데 이 중 country와 city를 제외한 나머지 속성을 별도의 detail이라는 변수에 저장하고 싶다면 detail 변수 앞에 잔여 연산자를 붙인다.

```ts
let address: any = {
  country: 'Korea',
  city: 'Seoul',
  address1: 'Gangnam-gu',
  address2: 'Sinsa-dong 123-456',
  address3: '789 street, 2 Floor ABC building'
}
const { country, city, ...detail } = address
console.log(detail)
```
```
//실행 결과 
{ address1: 'Gangnam-gu', 
  address2: 'Sinsa-dong 123-456', 
  address3: '789 street, 2 Floor ABC building'
  }

```

#### 전개연산자(spread operator)

전개연산자는 의미 그대로 객체의 속성을 모두 전개해 새로운 객체로 만들어 준다. 
```ts
let part1 = { name: 'jane' },
  part2 = { age: 22 },
  part3 = { city: 'Seoul', country: 'Kr' }

let merged = { ...part1, ...part2, ...part3 }
console.log(merged) 
// { name: 'jane', age: 22, city: 'Seoul', country: 'Kr' }

let coord = { ...{ x: 0 }, ...{ y: 0 } }
console.log(coord) // {x:0, y: 0}
```
## 5. 객체와 타입 변환

### 1. 타입변환

타입이 있는 언어들은 특정 타입의 변수값을 다른 타입의 값으로 변환할 수 있는 기능을 제공한다. 이를 타입변환이라고 한다.  person 변수의 타입은 object이다. 그런데 object타입은 name속성을 가지지 않으므로 오류가 발생한다.

```ts
let person : object = {name:'Jack', age: 32};
console.log(person.name)
```

person 변수를 일시적으로 name 속성이 있는 타입, 즉 {name: string} 타입으로 변환해 person.name 속성값을 얻게 한다.

```ts
let person : object = {name:'Jack', age: 32};
console.log((<{name:string}>person).name)
```

### 2. 타입단언

그런데 타입스크립트는 독특하게 타입 변환이 아닌 타입단언이라는 용어를 사용한다.

```ts
(<타입>객체)
(객체 as 타입)
```

```ts
export default interface INameable {
  name: string
}
```
```ts
import INameable from './INameable'
let obj: object = { name: 'Jack' }

let name1 = (<INameable>obj).name
let name2 = (obj as INameable).name
console.log(name1, name2) // Jack Jack
```
## 6. 함수와 메서드

### 1. 함수 선언문

```ts

function 함수 이름(매개변수1: 타입1, 매개변수2: 타입2[, ...]) : 반환값 타입 {
  함수 몸통
  }
```

```ts
function add(a: number, b: number): number { return a + b }
```
#### void 타입

값을 반환하지 않는 함수는 반환 타입이 void이다. 함수 반환 타입으로만 사용 할 수 있다.

```ts
function printMe(name: string, age: number): void { 
  console.log(`name: ${name}, age: ${age}`)
  }
```
#### 함수 시그니처

변수에 타입이 있듯이 함수 또한 타입이 있는데 함수의 타입을 함수 시그니처라고 한다.

```ts
 (매개변수1 타입,매개변수2 타입[,..]) => 반환값 타입
 ```
```ts
let printMe: (String, number) => void = function (name: String, age: number ):void {}
```
만약 매개변수가 없으면 ()로 표현  
() => void 매개변수없고, 반환값도 없음.  

#### type 키워드로 타입 별칭 만들기
```ts

```
```ts

```
#### undefined 관련 주의 사항
```ts

```
```ts

```
```ts

```
#### 선택적 매개변수
```ts

```
```ts

```
```ts

```

### 2. 함수 표현식
### 3. 화살표 함수와 표현식문
### 4. 일등 함수 살펴보기
### 5. 함수 구현 기법
### 6. 클래스 매서드

## 7.