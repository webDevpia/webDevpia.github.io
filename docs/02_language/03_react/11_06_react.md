---
title: 6. 데이터 정렬
layout: default
grand_parent: Language
parent: React
nav_order: 6
has_children: false
permalink: /language/react/react_6
---

### 6. render lists

#### 배열 정렬(Array Sort)

```js
// 기본 문법
// compareFunction : 정렬 순서를 정의하는 함수.  
// 반환값 : 정렬한 배열. 원 배열이 정렬됨.  
arr.sort([compareFunction]);
```

##### 1. compareFunction 없이 정렬

```js
const fruits = ['banana', 'cherry', 'apple'];
fruits.sort(); // ['apple', 'banana', 'cherry']
```
- 기본적으로 문자열 유니코드 순서로 정렬됨
- 숫자는 문자열로 변환되어 정렬되므로 주의 필요

```js
[9, 80].sort(); // [80, 9] - 문자열로 변환되어 정렬됨
```
##### 2. compareFunction으로 정렬
2.1 숫자 정렬

```js
const numbers = [1, 30, 4, 21, 100];

// 오름차순
numbers.sort((a, b) => a - b);  // [1, 4, 21, 30, 100]

// 내림차순
numbers.sort((a, b) => b - a);  // [100, 30, 21, 4, 1]
```
2.2 문자열 정렬
```js
const fruits = ['banana', 'cherry', 'Apple'];

// 오름차순 (대소문자 구분)
fruits.sort((a, b) => a.localeCompare(b));

// 내림차순 (대소문자 구분)
fruits.sort((a, b) => b.localeCompare(a));
```
2.3 객체 배열 정렬

```js
const items = [
  { name: 'banana', price: 1000 },
  { name: 'apple', price: 2000 },
  { name: 'cherry', price: 1500 }
];

// 가격 기준 오름차순
items.sort((a, b) => a.price - b.price);

// 이름 기준 오름차순
items.sort((a, b) => a.name.localeCompare(b.name));
```
**compareFunction 작동 원리**
- 반환값이 음수(-) → a가 b보다 앞에 위치
- 반환값이 0 → 순서 변경 없음
- 반환값이 양수(+) → b가 a보다 앞에 위치

#### 리스트에서 데이터 처리

src/App.jsx
```jsx
import List from "./06/List"
function App() {

  return (
    <>
      <List/>
    </>
  )
}

export default App
```

src/06/List.jsx
```jsx
export default function List(){
  const fruits = ['apple','orange','banana','cocount','pineapple']
  fruits.sort();
  const listItem = fruits.map(fruit => <li>{fruit}</li>)
  return(
    <ul>
      {listItem}
    </ul>
  )
}
```

#### 리스트에서 객체 데이터 처리

src/06/List.jsx
```jsx
export default function List(){

  const fruits = [{id:1, name:'apple', calories:95},
                  {id:2, name:'orange', calories:45},
                  {id:3, name:'banana', calories:105},
                  {id:4, name:'cocount', calories:159},
                  {id:5, name:'pineapple', calories:37}];

  const listItem = fruits.map(fruit => <li>{fruit.name}</li>)

  return(
    <ul>
      {listItem}
    </ul>
  )
}
```
웹브라우저 Console 확인  
List.jsx:9 Warning: Each child in a list should have a unique "key" prop.  

li태그에 key값을 추가해 준다.

src/06/List.jsx
```jsx
  const listItem = fruits.map((fruit,index) => 
                               <li key={index}>{fruit.name}</li>)
```

##### 오름차순, 내림차순 정렬

src/06/List.jsx
```jsx
export default function List(){
  const fruits = [{id:1, name:'apple', calories:95},
                  {id:2, name:'orange', calories:45},
                  {id:3, name:'banana', calories:105},
                  {id:4, name:'cocount', calories:159},
                  {id:5, name:'pineapple', calories:37}];

  // 오름차순(문자열)
  fruits.sort((a,b) => a.name.localeCompare(b.name));
  // 내림차순(문자열)
  fruits.sort((a,b) => b.name.localeCompare(a.name));
  // 오름차순(숫자)
  fruits.sort((a,b) => a.calories - b.calories);
  // 내림차순(숫자)
  fruits.sort((a,b) => b.calories - a.calories);

  const listItem = fruits.map(fruit => <li key={fruit.id}>
                                        {fruit.name}: &nbsp; 
                                        <b>{fruit.calories}</b>
                                      </li>);

    return(
      <ul>
        {listItem}
      </ul>
  )
}
```

#### 데이터 필터링해서 표시하기
filter() 결과 배열에 요소를 유지하려면 참 값을 반환하고 그렇지 않으면 거짓 값을 반환  

src/06/List.jsx
```jsx
export default function List(){
  const fruits = [{id:1, name:'apple', calories:95},
                  {id:2, name:'orange', calories:45},
                  {id:3, name:'banana', calories:105},
                  {id:4, name:'cocount', calories:159},
                  {id:5, name:'pineapple', calories:37}];
  
  // 100칼로리 미만
  const lowCalFruits = fruits.filter(fruit => fruit.calories < 100);
  // 100칼로리 이상 
  const highCalFruits = fruits.filter(fruit => fruit.calories >= 100);
  
  const listItem = highCalFruits.map(highCalFruit => 
                                        <li key={highCalFruit.id}>
                                          {highCalFruit.name}: &nbsp; 
                                          <b>{highCalFruit.calories}</b>
                                        </li>);
    return(
      <ul>
        {listItem}
      </ul>
  )
}
```

#### ListTest.jsx에서 List.jsx로 데이터 전달

src/App.jsx
```jsx
import ListTest from "./06/ListTest"

function App() {

  return (
    <>
      <ListTest/>
    </>
  )
}

export default App
```

src/06/ListTest.jsx
```jsx
import List from "./List"

export default function ListTest() {
  const fruits = [{id:1,name:'apple',calories:95},
                  {id:2,name:'orange',calories:45},
                  {id:3,name:'banana',calories:105},
                  {id:4,name:'cocount',calories:159},
                  {id:5,name:'pineapple',calories:37}];
  const vegetables = [{id:6,name:'potatoes',calories:110},
                      {id:7,name:'celery',calories:15},
                      {id:8,name:'carrots',calories:25},
                      {id:9,name:'corn',calories:63},
                      {id:10,name:'broccoli',calories:50}];
  const item=[];
  return (
    <>
      <List items={fruits} category="Fruits"/>
      <List items={vegetables} category="Vegetables"/>
      <List items={item} category="Item"/>
      <List/>
    </>
  )
}
```

src/06/List.jsx
```jsx
export default function List({category="Category", items=[]}){
  return (
    <>
      <h2 className="text-4xl font-bold text-gray-800 mb-2.5 text-center border-1 rounded-md bg-blue-400 m-10 p-5">
        {category}
      </h2>
      <ul>
        {items.map(item => (
          <li key={item.id} 
              className="text-3xl list-none text-gray-700 text-center m-0 
                         hover:text-gray-500 hover:cursor-pointer">
            {item.name}
          </li>
        ))}
      </ul>
    </>
  )
}

```


#### 데이터가 있을 경우에만 처리

src/06/ListTest.jsx return() 부분 수정
```jsx
    <>
      {fruits.length > 0 ? <List items={fruits} category="Fruits"/> : null}
      {vegetables.length > 0 ? <List items={vegetables} category="Vegetables"/> : null }
    </>
```

혹은 
src/06/ListTest.jsx  return() 부분 수정
```jsx
    <>
      {fruits.length > 0 && <List items={fruits} category="Fruits"/>}
      {vegetables.length > 0 && <List items={vegetables} category="Vegetables"/>}
      {item.length > 0 && <List items={item} category="Item"/>} 
      {item.length > 0 || <List items={vegetables} category="Vegetables"/>} 
    </>
```
