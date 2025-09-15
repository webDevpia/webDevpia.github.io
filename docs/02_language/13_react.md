---
title: React
layout: default
parent: Language
nav_order: 11
permalink: /language/react
# nav_exclude: true
# search_exclude: true
---

# React

리액트(react)는 2013년에 페이스북에서 발표한 오픈소스 자바스크립트 프레임워크  

## 특징
- 가상 Dom(Virtual Document Object Model)  
- JSX(javascript XML)  
- SPA(single page application) : 백엔드에서 받은 JSON 데이터를 해석하여 현재 화면에서 사용자가 새로 요청한 부분만 동적으로 화면을 생성.  
- 클라이언트에서 동작하는 템플릿 엔진 : 서버쪽 템플릿 엔진의 출력물은 HTML이지만 프론트엔드쪽 템플릿 엔진의 출력물은 DOM객체들의 조합.  


## 1. 기본설정

### 1.  node.js 설치

설치 후 버전 확인
```bash
node -v
npm -v
```

### 2. 프로젝트 생성
[vite+react+tailwindcss 프로젝트 생성](https://tailwindcss.com/docs/guides/vite#react)  

- vite로 리액트 프로젝트 생성
```bash
npm create vite@latest
```

- 워킹디렉토리로 이동하고 필요한 라이브러리 설치 후 실행
```bash
cd my-react-app
npm i
npm run dev
```

### 3. tailwind css 사용시 셋팅

- tailwind 설치 및 초기화

```bash
npm install tailwindcss @tailwindcss/vite
```

- vite.config.ts 파일 설정

```js{% raw %}
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
}){% endraw %}
```

- App.css에 @tailwindcss의 각 레이어에 대한 지시문을 파일에 추가

```css
@import "tailwindcss";
```

- 빌드 프로세스 시작

```bash
npm run dev
```

- 프로젝트에서 Tailwind 사용

```js{% raw %}
import './App.css'

function App() {
  return (
    <>
<div class="flex flex-col items-center gap-6 p-7 md:flex-row rounded-2xl">
  <div>
    <img class="size-48 shadow-xl rounded-md" alt="" src="https://picsum.photos/200/300" />
  </div>
  <div class="flex items-center">
    <span class="text-2xl font-medium">Class Warfare</span>
    <span class="font-medium text-sky-500">The Anti-Patterns</span>
    <span class="flex gap-2 font-medium text-gray-600 dark:text-gray-400">
      <span>No. 4</span>
      <span>·</span>
      <span>2025</span>
    </span>
  </div>
</div>
    </>
  )
}

export default App{% endraw %}
```

## 2. React 기본 
### 1. 기본구조

- index.html 파일이 진입점 id=root 태그에 내용이 삽입  
- src/main.jsx에서 코드 처리

index.html
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite + React</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

- index.html파일의 id값이 root를 찾아서 App컴포넌트를 랜더링해서 넣어준다.

src/main.jsx
```jsx {% raw %}
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
{% endraw %}
```

다른 컴포넌트에서 import 해서 사용할 컴포넌트는 반드시 export 해야 한다. 
return 함수안에 최상위 태그는 반드시 하나만 존재해야 한다. 

src/App.jsx
```jsx {% raw %}
import Header from "./Header"
import Footer from "./Footer"
import Food from "./Food";
function App() {
  return (
    <>
      <Header/>
      <Food/>
      <Food/>
      <Footer/>
    </>
  );
}

export default App {% endraw %}
```

return함수에서 사용한 태그는 html의 태그가 아니다.  
JSX(javascript XML)이다.  

src/Header.jsx
```js
function Header(){
  return(
    <header>
      <h1>My website</h1>
      <nav>
        <ul>
          <li><a href="#">Home</a></li>
          <li><a href="#">About</a></li>
          <li><a href="#">Service</a></li>
          <li><a href="#">Contact</a></li>
        </ul>
      </nav>
      <hr/>
    </header>
  );
}

export default Header
```

JSX에서 {}에는 값만 출력한다. 표현식은 안됨

src/Footer.jsx
```jsx
function Footer(){
  return(
    <footer>
      <p>&copy; {new Date().getFullYear()} Your website name</p>
    </footer>
  );
}

export default Footer
```

src/Food.jsx
```jsx
function Food(){
  const food1 = "Orange";
  const food2 = "Banana";

  return(
    <ul>
      <li>Apple</li>
      <li>{food1}</li>
      <li>{food2.toLocaleUpperCase()}</li>
    </ul>
  );
}

export default Food
```

### 2. Card 컴포넌트

#### 이미지 넣기

src/App.jsx
```jsx
import Card from "./Card"

function App() {
  return (
    <>
      <Card/>
    </>
  )
}

export default App
```
보통 사용할 이미지파일은 assets폴더에 저장하고,  
이미지 파일도 import 해서 가져온 후 사용한다.  

src/Card.jsx
```jsx
import profilePic from './assets/profile.png'
function Card(){
  return(
    <div>
      {/* <img src="https://via.placeholder.com/150" alt="profile picture" /> */}
      <img src={profilePic} alt="profile picture" />
      <h2>Test</h2>
      <p>I make Youtube videos and play</p>
    </div>
  )
}
export default Card
```

#### css 적용해보기

src/main.jsx 파일에  
import './index.css' 구문이 있으므로 작성하면 Card.jsx에 적용됨

src/index.css
```css
.card{
  border: 1px solid hsl(0, 0%, 80%);
  border-radius: 10px;
  box-shadow: 5px 5px 5px hsla(0, 0%, 0%, 0.1);
  padding: 20px;
  margin: 10px;
  text-align: center;
  max-width: 250px;
  display: inline-block;
}

.card-image{
  max-width: 60%;
  height: auto;
  border-radius: 50%;
  margin-bottom: 10px;
}

.card .card-title{
  font-family: Arial, sans-serif;
  margin: 0;
  color: hsl(0, 0%, 20%);
}

.card .card-text{
  font-family: Arial, sans-serif;
  color: hsl(0, 0%, 30%);
}
```

src/Card.jsx
```jsx
import profilePic from './assets/profile.png'
function Card(){
  return(
    <div className="card">
      {/* <img src="https://via.placeholder.com/150" alt="profile picture" /> */}
      <img className="card-image" src={profilePic} alt="profile picture" />
      <h2 className="card-title">Test</h2>
      <p className='card-text'>I make Youtube videos and play</p>
    </div>
  )
}
export default Card
```

### 3. React Components with css
외부 프레임워크나 전처리기는 제외

#### 1. external

src/App.jsx
```jsx
import Button from './03/Button'
function App() {
  return (
    <>
      <Button/>
    </>
  )
}

export default App
```

src/03/Button.jsx
```jsx
import './button.css'
function Button(){
  return(
    <button className="button">
      Click me
    </button>
  )
}
export default Button
```

src/03/Button.css
```css
.button{
  background-color: hsl(200, 100% , 50%);
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}
```

#### 2. modules

src/03/Button.module.css 생성
```css
.button{
  background-color: hsl(200, 100% , 50%);
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}
```

src/03/Button.jsx
```jsx
import styles from './Button.module.css'
function Button(){
  return(
    <button className={styles.button}>
      Click me
    </button>
  )
}
export default Button
```

#### 3. inline
css를 객체 형태로 작성해야하며, 값이름에 -을 사용할수 없고 카멜표기법으로 작성한다.  

src/03/Button.jsx
```jsx
function Button(){

  const styles = {
    backgroundColor:" hsl(200, 100% , 50%)",
    color: "white",
    padding: "10px 20px",
    borderRadius: "5px",
    border: "none",
    cursor: "pointer",
  }
  return(
    <button style={styles}>
      Click me
    </button>
  )
}
export default Button
```
혹은  

src/03/Button.jsx
```jsx
function Button(){
  return(
    <button style={ {
    backgroundColor:" hsl(200, 100% , 50%)",
    color: "white",
    padding: "10px 20px",
    borderRadius: "5px",
    border: "none",
    cursor: "pointer",
  } }>
      Click me
    </button>
  )
}
export default Button
```

### 4. props 

읽기만 가능한 값으로 컴포넌트 사이에서 값을 공유할 때 사용할 수 있으며, 부모 컴포넌트에서 자식 컴포넌트로만 보낼 수 있다.
값을 전달할 때 문자열은 따옴표로 감싸서 전달할 수 있지만 숫자값이나 논리값은 따옴표로 싸면 문자열이 되므로 { }로 감싸서 전달해야 한다.  

src/App.jsx
```jsx
import StudentList from './04/StudentList'

function App() {
  return (
    <>
      <StudentList />
    </>
  )
}

export default App
```

src/04/StudentList.jsx
```jsx
import Student from "./Student"
function StudentList() {
  return (
    <>
      <Student name="홍길동" age={30} isStudent={true} />
      <Student name="김철수" age={41} isStudent={false} />
      <Student name="박나리" age={50} isStudent={false} />
      <Student name="이정인" age={20} isStudent={true} />
      <Student/>
    </>
  )
}

export default StudentList
```

propTypes을 이용하여 값의 타입을 지정, 오류의 확인은 웹브라우저의 콘솔창에서 확인할 수 있다.  

src/04/Student.jsx
```jsx
import './Student.css'
import PropTypes from 'prop-types'
function Student(props){
  return(
    <div className="student">
      <p>Name : {props.name}</p>
      <p>Age : {props.age}</p>
      <p>Student : {props.isStudent ? "Yes" : "No" }</p>
    </div>
  )
}
// 타입이 안맞을경우 웹브라우저 콘솔에서 오류확인, 실행은 됨.
Student.propTypes = {
  name: PropTypes.string,
  age: PropTypes.number,
  isStudent: PropTypes.bool,
}

Student.defaultProps = {
  name: "Guest",
  age: 0,
  isStudent: false,
}
export default Student
```

src/04/Student.css
```css
.student{
  font-family: Arial, Helvetica, sans-serif;
  font-size: 2em;
  padding: 10px;
  border: 1px solid hsla(0, 0%, 50%, 0.8);
}
.student p{
  margin: 0;
}
```

### 5. conditional rendering(조건부 랜더링)
리액트에서는 조건을 작성하기 위한 특별한 문법이 없다.  
조건에 따른 분기가 필요하다면 삼항연산자를 이용
 -  조건 ? 참일때 : 거짓일때  

조건에 따른 분기가 필요없다면 단축평가(short-circuit evaluation)를 사용한다.  
논리식이 false라면 실행구문은 처리되지 않는다.
- 논리식 && 실행구문

#### 삼항연산자 이용

src/App.jsx
```jsx
import UserList from './05/UserList'
function App() {

  return (
    <>
      <UserList/>
    </>
  )
}

export default App
```

src/05/UserGreeting.jsx
```jsx
import './UserGreeting.css'
import PropTypes from 'prop-types'

export default function UserGreeting(props){
  // 1.
  // if (props.isLoggedIn){
  //   return <h2>Welcome {props.username}</h2>
  // }else{
  //   return <h2>Please log in to continue</h2>
  // }

  // 2.
  // return(props.isLoggedIn ? <h2 className="welcome-message">Welcome {props.username}</h2> :
  //                           <h2 className="login-prompt">Please log in to continue</h2>)


  const welcomeMessage =  <h2 className="welcome-message">
                            Welcome {props.username}
                          </h2>
  const loginPrompt = <h2 className="login-prompt">
                        Please log in to continue
                      </h2>
                      
  // return(props.isLoggedIn ? welcomeMessage : loginPrompt)

  return(
    <>
      {props.isLoggedIn && welcomeMessage}
      {props.isLoggedIn || loginPrompt}
    </>
  )
}

UserGreeting.propTypes = {
  isLoggedIn: PropTypes.bool,
  username: PropTypes.string,
}
UserGreeting.defaultProps = {
  isLoggedIn: false,
  username: "Guest",
}
```

src/05/UserGreeting.css
```css
.welcome-message{
  font-size: 2.5em;
  background-color: hsl(120, 100%, 42%);
  color: white;
  padding: 10px;
  border-radius: 5px;
  margin: 0;
}

.login-prompt{
  font-size: 2.5em;
  background-color: hsl(0, 100%, 42%);
  color: white;
  padding: 10px;
  border-radius: 5px;
  margin: 0;
}
```

#### 단축 평가

##### falsy 값
- false
- 0, -0
- '', "", ``
- null
- undefined
- NaN  

##### truthy 값
- true
- {}
- []
- 0이 아닌 숫자
- 비어있지 않은 문자열

JavaScript에서 0은 falsy 값이므로 아무것도 렌더링이 되지 않아야 한다.   
하지만 아래의 예제에서는 0이 렌더링 되어 보인다.  
이유는 JavaScript에서 && 연산자는 앞의 조건이 falsy 한 값이라면, 해당 객체를 반환하기 때문에 위의 예제에서는 0이 반환되어 렌더링 되는 것입니다.

src/05/Profile.css
```css
.avatar {
  border-radius: 50%;
}
```

src/05/Profile.jsx
```jsx
import './Profile.css'

export default function Profile(prop) {
  return (
    <>
      <h1>{prop.user.name}</h1>
      <img
        className="avatar"
        src={prop.user.imageUrl}
        alt={'Photo of ' + prop.user.name}
        style={ {
          width: prop.user.imageSize,
          height: prop.user.imageSize
        } }
      />
    </>
  );
}
```

src/05/ConditionTest.jsx
```jsx
import Profile from './Profile';
const user = [
  {
    id: 0,
    name: "Hedy Lamarr1",
    imageUrl: "https://i.imgur.com/yXOvdOSs.jpg",
    imageSize: 90
  },
  {
    id: "Hedy Lamarr2",
    name: "Hedy Lamarr2",
    imageUrl: "https://i.imgur.com/yXOvdOSs.jpg",
    imageSize: 90
  }
];

export default  function ConditionTest() {
  return (
    <>
      {user.map(
        (userInfo) =>
          userInfo.id && <Profile user={userInfo} key={userInfo.id} />
      )}
    </>
  );
}
```

### 6. render lists

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

#### 데이터 정렬해서 표시하기

```js
arr.sort([compareFunction]);
```
compareFunction : 정렬 순서를 정의하는 함수.  
                  생략하면 배열은 각 요소의 문자열 변환에 따라 각 문자의 유니 코드 코드 포인트 값에 따라 정렬  
반환값 : 정렬한 배열. 원 배열이 정렬됨.  

compareFunction이 제공되지 않으면 요소를 문자열로 변환하고 유니 코드 코드 포인트 순서로 문자열을 비교하여 정렬됩니다. 예를 들어 "바나나"는 "체리"앞에옵니다. 숫자 정렬에서는 9가 80보다 앞에 오지만 숫자는 문자열로 변환되기 때문에 "80"은 유니 코드 순서에서 "9"앞에옵니다.

compareFunction이 제공되면 배열 요소는 compare 함수의 반환 값에 따라 정렬.  

a와 b가 비교되는 두 요소라면,
compareFunction(a, b)이 0보다 작은 경우 a를 b보다 낮은 색인으로 정렬. 즉, a가 먼저옴.
compareFunction(a, b)이 0을 반환하면 a와 b를 서로에 대해 변경하지 않고 모든 다른 요소에 대해 정렬. 
compareFunction(a, b)이 0보다 큰 경우, b를 a보다 낮은 인덱스로 정렬.

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
  return (
    <>
      <List items={fruits} category="Fruits"/>
      <List items={vegetables} category="Vegetables"/>
    </>
  )
}
```

src/06/List.jsx
```jsx
import  './List.css'

export default function List(props){

  const category = props.category;
  const itemList = props.items;

  const listItem = itemList.map(item => <li key={item.id}>
                                          {item.name}: &nbsp; 
                                          <b>{item.calories}</b>
                                        </li>);
  return(
    <>
      <h3 className="list-category">{category}</h3>
      <ul className="list-items">{listItem}</ul>
    </>
  )
}
```

src/06/List.css
```css
.list-category{
  font-size: 2.5em;
  font-weight: bold;
  color: hsl(0, 0%, 20%);
  margin-bottom: 10px;
  text-align: center;
  border: 3px solid;
  border-radius: 5px;
  background-color: cornflowerblue;
}
.list-items li{
  font-size: 2em;
  list-style: none;
  color: hsl(0, 0%, 25%);
  text-align: center;
  margin: 0;
}
.list-items li:hover{
  color: hsl(0, 0%, 45%);
  cursor: pointer;
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
    </>
```

#### 자료형 및 기본값 설정

src/06/List.jsx
```jsx
import PropTypes from 'prop-types';
import  './List.css'

export default function List(props){

  const category = props.category;
  const itemList = props.items;

  const listItem = itemList.map(item => <li key={item.id}>
                                          {item.name}: &nbsp; 
                                          <b>{item.calories}</b>
                                        </li>);
  return(
    <>
      <h3 className="list-category">{category}</h3>
      <ol className="list-items">{listItem}</ol>
    </>
  )
}

List.propTypes ={
  category: PropTypes.string,
  items: PropTypes.arrayOf(PropTypes.shape({  id: PropTypes.number,
                                              name: PropTypes.string,
                                              calories: PropTypes.number})),
}
List.defaultProps = {
  category: "Category",
  item:[],
}
```

### 7. click events

src/App.jsx
```jsx
import Button from "./07/Button"
import ProfilePicture from "./07/ProfilePicture"

export default function App() {

  return (
    <>
      <Button/>
      <ProfilePicture/>
    </>
  )
}
```

src/07/Button.jsx
```jsx
export default function Button(){

// 인자값을 전달하지 않을 때 함수 호출
  const handleClick = () => console.log("Ouch!");

//  인자값을 전달하는 경우 함수 호출
  const handleClick2 = (name) => console.log(`${name} stop clicking me`);

  let count = 0;
  const handleClick3 = (name)=>{
    if(count<3){
      count++;
      console.log(`${name} you clicked me ${count} tiems`);
    }else{
      console.log(`${name} stop clicking me!`);
    }
  }
// 이벤트 객체를 인자값으로 전달하는 경우
  const handleClick4 = (e) => {
    // console.log(e)
    e.target.textContent = "OUCH! 😣";
  }
  return(
    <>
      <button onClick={handleClick}>Click me 😁</button>
      <button onClick={() => handleClick2("hong")}>Click me 😁</button>
      <button onClick={() => handleClick3("hong")}>Click me 😊</button>
      {/* <button onClick={(e) => handleClick4(e)}>Click me 😊</button> */}
      <button onDoubleClick={(e) => handleClick4(e)}>Click me 😊</button>
    </>
  )
}
```

src/App.jsx
```jsx
import ProfilePicture from "./07/ProfilePicture"

export default function App() {
  return (
    <>
      <ProfilePicture/>
    </>
  )
}
```

src/07/ProfilePicture.jsx
```jsx
export default function ProfilePicture(){

  const imgurl = './src/assets/profile.png';
  const handleClick = (e) => {
    // console.log("OUCH!");
    e.target.style.display = "none";
  }
  
  return(
    <img src={imgurl} onClick={(e)=>handleClick(e)}></img>
  )
}
```

### 8. useState() hook

리액트에서의 state는 리액트 컴포넌트의 상태를 의미, 즉 리액트 컴포넌트의 변경 가능한 데이터  

- 직접 state를 수정하지 않는다. 랜더링이 일이나지 않음.
- set함수를 이용하여 값을 수정

```jsx
const [변수명,set함수명] = useState(초깃값)
```

![](/assets/img/react/react000.png)

src/App.jsx
```jsx
import ProfilePicture from "./08/ProfilePicture"
import MyComponent_08 from "./08/MyComponent"
import Counter from "./08/Counter"

export default function App() {

  return (
    <>
      <ProfilePicture/>
      <MyComponent_08/>
      <Counter/>
    </>
  )
}
```

src/08/ProfilePicture.jsx
```jsx
import { useState } from "react";

export default function ProfilePicture(){

  const imgurl = './src/assets/profile.png';

  let displayVales = ""
  const styles = {display:displayVales}

  const handleClick = () => {
    displayVales ? displayVales = "" : displayVales = "none" 
    document.getElementById('dis').style.display = displayVales
  } 

  const [display,setDisplay] = useState("");
  const styles1 = {display:display}
  const handleClick1 = () => {
    setDisplay(display ? "" : "none" )
  }

  return(
    <>
    <img src={imgurl} id="dis"></img>
    <button onClick={handleClick}>이미지1</button>
    <br/>
    <img src={imgurl} style={styles1}></img>
    <button onClick={handleClick1}>이미지2</button>
    </>
  )
}
```

src/08/MyComponent.jsx
```jsx
import { useState } from "react";

export default function MyComponent_08(){

  const [name,setName] = useState("Guest");
  const [age, setAge] = useState(0);
  const [isEmployed,setIsEmployed] = useState(false);

  const updateName = () => {
    setName("홍길동");
  }
  const incrementAge = () => {
    setAge(age+1);
  }
  const toggleEmployedStatus = () => {
    setIsEmployed(!isEmployed);
  }
  
  return(
    <div>
      <p>Name: {name}</p>
      <button onClick={updateName}>Set Name</button>

      <p>Age: {age}</p>
      <button onClick={incrementAge}>Increment Age</button>

      <p>Is employed: {isEmployed?"yes":"no"}</p>
      <button onClick={toggleEmployedStatus}>Toggle Status</button>
    </div>
  )
}
```

src/08/Counter.jsx
```jsx
import { useState } from "react";
import './Counter.css'

export default function Counter(){
  
  const [count,setCount] = useState(0);
  const increment = () =>{
    setCount(count + 1);
  }
  const decrement = () => {
    setCount(count - 1);
  }
  const reset = () => {
    setCount(0);
  }
  return(
    <div className="counter-container">
      <p className="count-display">{count}</p>
      <button className="counter-button" onClick={decrement}>Decrement</button>
      <button className="counter-button" onClick={reset}>Reset</button>
      <button className="counter-button" onClick={increment}>Increment</button>
    </div>
  );
}
```

src/08/Counter.css
```css
.counter-container{
  text-align: center;
  font-family: Arial, Helvetica, sans-serif;
}

.count-display{
  font-size: 10em;
  margin-top: 0;
  margin-bottom: 50px;
}

.counter-button{
  width: 150px;
  height: 50px;
  font-size: 1.5em;
  font-weight: bold;
  margin: 0px 5px;
  background-color: hsl(197, 100%, 58%);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.counter-button:hover{
  background-color: hsl(197, 100%, 48%);
}
```

### 9. onChange event handler

src/App.jsx
```jsx
import MyComponent_09 from './09/MyComponent'

export default function App() {

  return (
    <>
      <MyComponent_09/>
    </>
  )
}
```

src/09/MyComponent.jsx
```jsx
import { useState } from "react"

export default function MyComponent_09(){

  const [name,setName] = useState("Guest");
  const [quantity,setQuantity] = useState(1);
  const [comment,setComment] = useState("");
  const [payment,setPayment] = useState("Visa");
  const [shipping,setShipping] = useState("Delivery");

  function handleNameChange(event){
    setName(event.target.value);
  }
  function handleQuantityChange(event){
    setQuantity(event.target.value);
  }
  function handleCommentChange(event){
    setComment(event.target.value);
  }
  function handlePaymentChange(event){
    setPayment(event.target.value);
  }
  function handleShippingChange(event){
    setShipping(event.target.value)
  }

  return(
    <div>
      <input value={name} onChange={handleNameChange} />
      <p>Name:{name}</p>

      <input value={quantity} onChange={handleQuantityChange} />
      <p>Quantity:{quantity}</p>

      <textarea value={comment} onChange={handleCommentChange} placeholder="Enter delivery instaructions" ></textarea>
      <p>Comment: {comment}</p>
      <select value={payment} onChange={handlePaymentChange}>
        <option value="">Select an option</option>
        <option value="Visa">Visa</option>
        <option value="Mastercard">Mastercard</option>
        <option value="Giftcard">Giftcard</option>
      </select>
      <p>Payment: {payment}</p>
      <label>
        <input type="radio" value="Pick up" checked={shipping === "Pick up"} onChange={handleShippingChange} />
        Pick up
      </label><br/>
      <label >
        <input type="radio" value="Delivery" checked={shipping === "Delivery"} onChange={handleShippingChange} />
        Delivery
      </label>
      <p>Shipping: {shipping}</p>
    </div>
  )
}
```

### 10. color picker app

src/App.jsx
```jsx
import ColorPicker from './10/ColorPicker'

export default function App() {

  return (
    <>
      <ColorPicker/>
    </>
  )
}
```

src/10/ColorPicker.jsx
```jsx
import { useState } from "react"
import './ColorPicker.css'

export default function ColorPicker() {
  const [color, setColor] = useState("#ffffff");

  function handleColorChange(event){
    setColor(event.target.value);
  }
  return (
    <div className="color-picker-container">
      <h1>Color Picker</h1>
      <div className="color-display" style={ {backgroundColor:color} }>
        <p>Selected Color: {color}</p>
      </div>
      <label htmlFor="color">Select a Color</label>
      <input type="color" value={color} onChange={handleColorChange} id="color"/>
    </div>
  )
}
```

src/10/ColorPicker.css
```css
body{
  font-family: Arial, Helvetica, sans-serif;
}
.color-picker-container{
  display: flex;
  flex-direction: column;
  align-items: center;
}
h1{
  margin: 50px;
  font-size: 3rem;
}
.color-display{
  width: 300px;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 5px solid hsl(0, 0%, 80%);
  border-radius: 25px;
  margin-bottom: 25px;
  transition: 0.25s ease;
}
label{
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}
input[type="color"]{
  width: 75px;
  height: 50px;
  padding: 5px;
  border-radius: 10px;
  border: 3px solid hsl(0, 0%, 80%);
}
```

### 11. updater functions

src/11/App.jsx
```jsx
import MyComponent_11 from './11/MyComponent'
export default function App() {

  return (
    <>
      <MyComponent_11/>
    </>
  )
}
```

src/11/MyComponent.jsx
```jsx
import { useState } from "react";

export default function MyComponent_11(){
  const [count,setCount] = useState(0);
  const increment = () =>{
    setCount(count + 1)
    setCount(count + 1)

    // setCount(count => count + 1);
    // setCount(count => count + 1);

    // setCount(c => c + 1);
    // setCount(c => c + 1);

  }
  const decrement = () => {
    setCount(count - 1);
    // setCount(count => count - 1);
  }
  const reset = () => {
    setCount(0);
  }
  return(
    <div className="counter-container">
      <p className="count-display">{count}</p>
      <button className="counter-button" onClick={decrement}>Decrement</button>
      <button className="counter-button" onClick={reset}>Reset</button>
      <button className="counter-button" onClick={increment}>Increment</button>
    </div>
  );
}
```

### 12. update OBJECTS in state
src/App.jsx
```jsx
import MyComponent_12 from "./12/MyComponent"
export default function App() {

  return (
    <>
      <MyComponent_12/>
    </>
  )
}
```

src/MyComponent.jsx
```jsx
import { useState } from "react";

export default function MyComponent_12(){

  const [car, setCar] = useState({
    year:2024,
    make: "Ford",
    model: "Mustang"
  });

  function handleYearChange(event){
    setCar(car => ({...car, year:event.target.value}));
  }

  function handleMakeChange(event){
    setCar(c => ({...c, make:event.target.value}));
  }

  function handleModelChange(event){
    setCar(c => ({...c, model:event.target.value}));
  }

  return(
    <div>
      <p>
        Your favorite car is : {car.year} {car.make} {car.model}
      </p>
      <input type="number" value={car.year} onChange={handleYearChange} /><br/>
      <input type="text" value={car.make} onChange={handleMakeChange} /><br/>
      <input type="text" value={car.model}  onChange={handleModelChange}/><br/>
    </div>
  );
}
```

### 13. update ARRAYS in state

src/App.jsx
```jsx
import MyComponent_13 from "./13/MyComponent"
export default function App() {
  return (
    <>
      <MyComponent_13 />
    </>
  )
}
```

src/13/MyComponent.jsx
```jsx

import { useState } from "react";

export default function MyComponent_13(){

  const [foods,setFoods] = useState(["Apple","Orange","Banana"]);

  function handleAddFood(){

    const newFood = document.getElementById("foodInput").value;
    document.getElementById("foodInput").value = "";
    setFoods(f => [...f, newFood]);
    console.log(foods)

  }

  function handleRemoveFood(index){

    setFoods(foods.filter((_,i) => i !== index))

  }

  return(
    <div>
      <h2>List of Food</h2>
      <ul>
        {foods.map((food,index) => 
          <li key={index} onClick={()=>handleRemoveFood(index)}>
            {food}
          </li>
        )}
      </ul>
      <input type="text" id="foodInput" placeholder="Enter food name" />
      <button onClick={handleAddFood}>Add Food</button>
    </div>
  );
}
```

### 14. update ARRAY of OBJECTS in state
```jsx
import { useState } from "react";

export default function MyComponent_14(){

  const [cars,setCars] = useState([]);
  const [carYear,setCarYear] = useState(new Date().getFullYear());
  const [carMake,setCarMake] = useState("");
  const [carModel,setCarModel] = useState("");

  function handleAddCar(){

    const newCar = {
      year:carYear,
      make:carMake,
      model:carModel,
    };

    setCars(c => [...c, newCar]);
    setCarYear(new Date().getFullYear());
    setCarMake("");
    setCarModel("");

  }

  function handleRemoveCar(index){
    setCars(c => c.filter((_,i) => i !== index));
  }

  function handleYearChange(event){
    setCarYear(event.target.value);
  }

  function handleMakeChange(event){
    setCarMake(event.target.value);
  }

  function handleModelChange(event){
    setCarModel(event.target.value);
  }

  return(
    <div>
      <h2>List of Car Objects</h2>
      <ul>
        {cars.map((car,index) => 
          <li key={index} onClick={()=>handleRemoveCar(index)}> 
          {car.year} {car.make} {car.model} 
          </li>
        )}
      </ul>
      <input type="number" value={carYear} onChange={handleYearChange} /><br/>
      <input type="text" value={carMake} onChange={handleMakeChange} placeholder="Enter car make" /><br/>
      <input type="text" value={carModel} onChange={handleModelChange} placeholder="Enter car model" /><br/>
      <button onClick={handleAddCar}>Add Car</button>
    </div>
  );
}
```

### 15. to-do list app

src/App.jsx
```jsx
import ToDoList from './15/ToDoList'

export default function App() {

  return (
    <>
      <ToDoList/>
    </>
  )
}
```

src/15/ToDoList.jsx
```jsx
import { useState } from "react";
import './ToDoList.css'

export default function ToDoList(){

  const [tasks,setTasks] = useState(["Eat Breakfast","Take a shower","walk the dog"]);
  const [newTask,setNewTask] = useState("");

  function handleInputChange(event){
    setNewTask(event.target.value);
  }

  function addTask(){
    if(newTask.trim() !== ""){
      setTasks(t => [...t, newTask]);
      setNewTask("");
    }
  }

  function deleteTask(index){
    const updatedTasks = tasks.filter((_, i) => i !== index);
    setTasks(updatedTasks);
  }

  function moveTaskUp(index){
    if(index > 0){
      const updatedTasks = [...tasks];
      [updatedTasks[index],updatedTasks[index - 1]] = 
      [updatedTasks[index - 1],updatedTasks[index]];
      setTasks(updatedTasks);
    }
  }

  function moveTaskDown(index){
    if(index < tasks.length - 1 ){
      const updatedTasks = [...tasks];
      [updatedTasks[index],updatedTasks[index + 1]] = 
      [updatedTasks[index + 1],updatedTasks[index]];
      setTasks(updatedTasks);
    }
  }

  return(
    <div className="to-do-list">
      <h1>To-Do-List</h1>
      <div>
        <input type="text" placeholder="Enter a task..." value={newTask} onChange={handleInputChange} />
        <button className="add-button" onClick={addTask}>
          Add
        </button>
      </div>
      <ol>
        {tasks.map((task,index) =>
          <li key={index}>
            <span className="text">{task}</span>
            <button className="delete-button" onClick={()=> deleteTask(index)}>
              Delete
            </button>
            <button className="move-button" onClick={()=> moveTaskUp(index)}>
              👆
            </button>
            <button className="move-button" onClick={()=> moveTaskDown(index)}>
              👇
            </button>
          </li>
        )}
      </ol>
    </div>
  );
}
```

src/15/ToDoList.css
```css
body{
  background-color: hsl(0, 0%, 10%);
}
.to-do-list{
  font-family: Arial, Helvetica, sans-serif;
  text-align: center;
  margin-top: 100px;
}
h1{
  font-size: 4rem;
  color: white;
}
button{
  font-size: 1.7rem;
  font-weight: bold;
  padding: 10px 20px;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.5s ease;
}
.add-button{
  background-color: hsl(125, 47%, 54%);
}
.add-button:hover{
  background-color: hsl(125, 47%, 44%);
}
.delete-button{
  background-color: hsl(10, 90%, 50%);
}
.delete-button:hover{
  background-color: hsl(10, 90%, 40%);
}
.move-button{
  background-color: hsl(207, 90%, 64%);
}
.move-button:hover{
  background-color: hsl(2-7, 90%, 54%);
}
input[type="text"]{
  font-size: 1.6rem;
  padding: 10px;
  border: 2px solid hsla(0, 0%, 80%, 0.5);
  border-radius: 5px;
  color: hsla(0, 0%, 0%, 0.5);
}
ol{
  padding: 0;
}
li{
  font-size: 2rem;
  font-weight: bold;
  padding: 15px;
  background-color: hsl(0, 0%, 97%);
  margin-bottom: 10px;
  border-radius: 5px;
  display: flex;
  align-items: center;
}
.text{
  flex: 1;
}
.delete-button, .move-button{
  padding: 8px 12px;
  font-size: 1.4rem;
  margin-left: 10px;
}
```

### 16. useEffect() hook
처음 컴포넌트가 렌더링된 이후, 업데이트로 인한 재렌더링 이후에 실행

src/16/MyComponent1.jsx
```jsx

// useEffect(function,[dependencies])
// 1. 의존성 배열 생략 시 컴포넌트 업데이트 시마다 실행 
// useEffect(()=>{})
// 2. 의존성 배열 비어 있을 경우 마운트와 언마운트시에 단 한번씩만 실행
// useEffect(()=>{},[])
// 3. 컴포넌트 마운트되었을때, 의존성 배열에 있는 변수들 중 하나라도 값이 변경되었을 때 실행
// useEffect(()=>{},[value])
// 4. 함수안에 리턴구문은 컴포넌트가 마운트 해제되기 전에 실행
// useEffect(()=>{  return () => { } })

// uses
// 1. Event Listeners
// 2. DOM 조작
// 3. 구독 (real-time updates)
// 4. API에서 데이터 가져오기
// 5. 컴포넌트가 언마운트 될때 정리 작업

import { useState, useEffect } from "react";

export default function MyComponent_16(){
  
  const [count, setCount] = useState(0);
  const [color, setColor] = useState("green");

  useEffect(() => {
    document.title = `Count: ${count}  ${color}`;
    return() => {
      // some cleanup code
    }
  },[count,color]);

  function addCount(){
    setCount(c => c + 1);
  }

  function subtractCount(){
    setCount(c => c - 1);
  }

  function changeColor(){
    setColor(c => c === "green" ? "red" : "green");
  }

  return(
    <>
      <p style={ {color:color} }>Count: {count}</p>
      <button onClick={addCount}>Add</button>
      <button onClick={subtractCount}>Subtract</button><br/>
      <button onClick={changeColor}>Change color</button>
    </>
  )
}
```

src/16/MyComponent2.jsx
```jsx
import { useState, useEffect } from "react";

export default function MyComponent_16_2(){

    const [width,setWidth] = useState(window.innerWidth);
    const [height,setHeight] = useState(window.innerHeight);

    // window.addEventListener("resize",handleResize);
    // console.log("EVENT LISTENER ADDED");

    useEffect(() => {
      window.addEventListener("resize",handleResize);
      console.log("EVENT LISTENER ADDED");
      return () => {
        window.removeEventListener("resize",handleResize);
        console.log("EVENT LISTENER REMOVED");
      }
    },[]);

    useEffect(() => {
      document.title = `Size: ${width} * ${height}`
    },[width,height])

    function handleResize(){
      setWidth(window.innerWidth);
      setHeight(window.innerHeight);
    }

    return(
      <>
        <p>Window Width: {width}px</p>
        <p>Window Height: {height}px</p>
      </>
    );
}
```

### 17. digital clock app

src/17/DigitalClock.jsx
```jsx
import { useState,useEffect } from "react";
import './DigitalClock.css'

export default function DigitalClock(){
  const [time,setTime] = useState(new Date());

  useEffect(()=>{
    const intervalId = setInterval(()=>{
      setTime(new Date());
    },1000)

    return () => {
      clearInterval(intervalId);
    }
  },[]);

  function formatTime(){
    let hours = time.getHours();
    const minutes = time.getMinutes();
    const seconds = time.getSeconds();
    const meridiem = hours >= 12 ? "PM" :"AM";
    hours = hours % 12 || 12;
    return `${padZero(hours)}:${padZero(minutes)}:${padZero(seconds)} ${meridiem}`
  }

  function padZero(number){
    return (number < 10 ? "0" : "" ) + number;
  }

  return(
    <div className="clock-container">
      <div className="clock">
        <span>{formatTime()}</span>
      </div>
    </div>
  );
}
```

src/17/DigitalClock.css
```css
body{
  background-image: url('../assets/bg1.jpg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  margin: 0;
  /* optional */
  display: flex;
  justify-content: center;
  min-height: 100vh;
  align-items: center;
}
.clock-container{
  backdrop-filter: blur(10px);
  width: 100vw;
  padding: 10px 0;
}
.clock{
  color: white;
  font-size: 6rem;
  font-weight: bold;
  font-family: monospace;
  text-align: center;
  text-shadow: 3px 3px 5px hsla(0, 0%, 0%, 0.75);
}
```

### 18. useContext() hook

#### prop drilling

src/18/Component.css
```css
.box{
  border: 3px solid;
  padding: 25px;
}
```

src/18/ComponentA.jsx
```jsx
import { useState } from 'react'
import './Component.css'
import ComponentB from './ComponentB'

export default function ComponentA(){
  const [user, setUser] = useState("홍길동")
  return(
    <div className="box">
      <h1>ComponentA</h1>
      <h2>{`Hello ${user}`}</h2>
      <ComponentB user={user}/>
    </div>
  )
}
```

```jsx
import ComponentC from './ComponentC'

export default function ComponentB(prop){

  return(
    <div className="box">
      <h1>ComponentB</h1>
      <ComponentC user={prop.user} />
    </div>
  )
}
```

```jsx
import ComponentD from './ComponentD'

export default function ComponentC(prop){

  return(
    <div className="box">
      <h1>ComponentC</h1>
      <ComponentD user={prop.user} />
    </div>
  )
}
```

```jsx
export default function ComponentD(prop){

  return(
    <div className="box">
      <h1>ComponentD</h1>
      <h2>{`Hello ${prop.user}`}</h2>
    </div>
  )
}
```

#### userContext()

```jsx
import { createContext, useState } from 'react'
import './Component.css'
import ComponentB from './ComponentB'

export const UserContext = createContext()

export default function ComponentA(){

  const [user, setUser] = useState("홍길동")

  return(
    <div className="box">
      <h1>ComponentA</h1>
      <h2>{`Hello ${user}`}</h2>
      <UserContext.Provider value={user}>
        <ComponentB user={user}/>
      </UserContext.Provider>
    </div>
  )
}
```

```jsx
import ComponentC from './ComponentC'

export default function ComponentB(){

  return(
    <div className="box">
      <h1>ComponentB</h1>
      <ComponentC />
    </div>
  )
}
```

```jsx
import { useContext } from 'react'
import ComponentD from './ComponentD'
import { UserContext } from './ComponentA'

export default function ComponentC(){

  const user = useContext(UserContext);
  return(
    <div className="box">
      <h1>ComponentC</h1>
      <h2>{`Hello again ${user}`}</h2>
      <ComponentD />
    </div>
  )
}
```

```jsx
import { useContext } from "react"
import { UserContext } from "./ComponentA"

export default function ComponentD(){

  const user = useContext(UserContext);
  return(
    <div className="box">
      <h1>ComponentD</h1>
      <h2>{`bye ${user}`}</h2>
    </div>
  )
}
```

### 19. useRef() hook

useRef()는 레퍼런스 객체를 반환한다.  
레퍼런스 객체에는 .current라는 속성이 있는데 이것은 현재 레퍼런스하고 있는 엘리먼트를 의미

```jsx
const refContainer = useRef(초깃값)
```
아래와 같은 파라미터로 들어온 초깃값으로 초기화된 레퍼런스 객체를 반환한다.

```jsx
{current: value}
```
 만약 초깃값이 null이라면 .current의 값이 null인 레퍼런스 객체가 반환된다.   
 이렇게 반환된 레퍼런스 객체는 컴포넌트 라이프타임 전체에 걸쳐서 유지된다.  즉 컴포넌트가 마운트 해제 전까지는 계속 유지된다.

#### 저장공간
 State의 변화 -> 렌더링 -> 컴포넌트 내부 변수들 초기화  
 Ref의 변화 -> No 렌더링 -> 변수들의 값이 유지됨  
 변수값의 변화 -> No 렌더링 -> 값이 초기화됨.  

```jsx
import { useState,useRef } from "react";

export default function MyComponent_19_1(){

  const [count,SetCount] = useState(0)
  const countRef = useRef(0)
  let countVar = 0

  const incrementCountState =  () => {
    SetCount(count + 1)
    console.log('state:',count)
    console.log('ref:',countRef)
    console.log('var:',countVar)
  }
  const incrementCountRef = () => {
    countRef.current = countRef.current + 1
    console.log('state:',count)
    console.log('ref:',countRef)
    console.log('var:',countVar)
  }

  const incrementCountVar = ()  => {
    countVar = countVar + 1
    console.log('state:',count)
    console.log('ref:',countRef)
    console.log('var:',countVar)
  }
  return(
    <div>
      <p>State: {count}</p>
      <p>Ref: {countRef.current}</p>
      <p>Var: {countVar}</p>
      <button onClick={incrementCountState}>State 증가</button>
      <button onClick={incrementCountRef}>Ref 증가</button>
      <button onClick={incrementCountVar}>Var 증가</button>
    </div>
  )
}
```

#### 변화는 감지해야 하지만 그 변화가 랜더링을 발생시키면 안되는 경우 사용할 수 있다.

```jsx
import { useState,useRef,useEffect } from "react";

export default function MyComponent_19_2(){

  const [count,setCount] = useState(0)
  const [renderCount,setRenderCount] = useState(0)
  const renderRef = useRef(0)

  // 의존성 배열이 생략되었으므로 컴포넌트 업데이트시마다 실행
  // 생성시 초기값 0, 생성후 실행되므로 1
  useEffect(()=>{
    // console.log('렌더링:',renderCount)
    // setRenderCount(renderCount+1)
    console.log('렌더링:',renderRef.current)
    renderRef.current = renderRef.current + 1
  })

  return(
    <div>
      <p>State: {count}</p>
      <p>render State: {renderCount}</p>
      <p>Ref: {renderRef.current}</p>
      <button onClick={() => setCount(count + 1)}>State Count 증가</button>
    </div>
  )
}
```
#### useRef를 이용해서 DOM에 접근하기

```jsx
const ref = useRef(value)
...
<input ref={ref}/>
```

```jsx
import { useRef, useEffect } from "react";

export default function MyComponent_19_3(){

  const inputRef = useRef()

  useEffect( () => {
    console.log(inputRef)
    inputRef.current.focus()
  },[] )

  const login = () => {
    alert(`Hello! ${inputRef.current.value} ~`)
    inputRef.current.value = ""
    inputRef.current.focus()
  }

  const handleOnKeyPress = e => {
    if (e.key == 'Enter'){
      login()
    }
  }
  return(
    <div>
      <input ref={inputRef} type="text" placeholder="username" onKeyUp={handleOnKeyPress} />
      <button onClick={login}>로그인</button>
    </div>
  )
}
```

### 20. stopwatch app

src/20/StopWatch.jsx
```jsx
import { useState,useEffect,useRef } from "react";
import './StopWatch.css'

export default function StopWatch(){
  const [isRunning, setIsRunning] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0)
  const intervalIdRef = useRef(null);
  const startTimeRef = useRef(0);

    useEffect(()=>{
      if(isRunning){
        intervalIdRef.current = setInterval(()=>{
          setElapsedTime(Date.now() - startTimeRef.current);
        },10);
      }
      return () => {
        clearInterval(intervalIdRef.current);
      }
    },[isRunning]);

    function start(){
      setIsRunning(true);
      startTimeRef.current = Date.now() - elapsedTime;
    }
    function stop(){
      setIsRunning(false);
    }
    function reset(){
      setElapsedTime(0);
      setIsRunning(false);
    }
    function formatTime(){
      let hours = Math.floor( elapsedTime / ( 1000 * 60 * 60 ));
      let minutes = Math.floor( elapsedTime / ( 1000 * 60 ) % 60 );
      let seconds = Math.floor( elapsedTime / ( 1000 ) % 60 );
      let milliseconds = Math.floor(( elapsedTime % 1000 ) / 10 );

      hours = String(hours).padStart(2,"0");
      minutes = String(minutes).padStart(2,"0");
      seconds = String(seconds).padStart(2,"0");
      milliseconds = String(milliseconds).padStart(2,"0");

      return `${minutes}:${seconds}:${milliseconds}`;
    }

    return(
      <div className="stopwatch">
        <div className="display">{formatTime()}</div>
        <div className="controls">
          <button className="start-button" onClick={start}>Start</button>
          <button className="stop-button" onClick={stop}>Stop</button>
          <button className="reset-button" onClick={reset}>Reset</button>
        </div>
      </div>
    );
}
```

src/20/StopWatch.css
```css
body{
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: hsl(0, 0%, 95%);
}
.stopwatch{
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 5px solid;
  border-radius: 50px;
  background-color: white;
  padding: 30px;
}
.display{
  font-size: 5rem;
  font-family: monospace;
  font-weight: bold;
  color: hsl(0, 0%, 30%);
  text-shadow: 2px 2px 2px hsla(0, 0%, 0%, 0.75);
  margin-bottom: 25px;
}
.controls button{
  font-size: 1.5rem;
  font-weight: bold;
  padding: 10px 20px;
  margin: 5px;
  min-width: 125px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  color: white;
  transition: background-color 0.5s ease;
}
.start-button{
  background-color: hsl(115, 100%, 40%);
}
.start-button:hover{
  background-color: hsl(115, 100%, 35%);
}
.stop-button{
  background-color: hsl(0, 90%, 50%);
}
.stop-button:hover{
  background-color: hsl(0, 90%, 40%);
}
.reset-button{
  background-color: hsl(205, 100%, 60%);
}
.reset-button:hover{
  background-color: hsl(205, 100%, 50%);
}
```

### 21. axios

#### server

프로젝트 생성
```bash
mkdir server
cd server
npm init -y
npm i express mongoose axios cors mongoose-sequence
npm i nodemon -D
```

package.json 수정
```
  "scripts":{
    "start": "nodemon index.js"
  },
```

Models/Todo.js 생성
```js
const mongoose = require('mongoose')
const AutoIncrement = require("mongoose-sequence")(mongoose);

const TodoSchema = new mongoose.Schema({
  // id 필드는 스키마에서 안만들어도 plugin()에서 설정하면 해당 필드 자동 생성
  task: {type: String},
  done: {
    type: Boolean,
    default: false
  }},{
    // mongoose를 통해서 데이터를 삽입하면 '__v' 필드가 생긴다. 
    // 의미하는 바는 버전 키라고 하는데 문서의 내부 개정판을 설명하고 기본 값은 0이다.
    // 삭제할려면 versionKey값을 false로 설정
    versionKey: false }
)
TodoSchema.plugin(AutoIncrement,{inc_field:"id"})

module.exports = mongoose.model("Todo",TodoSchema)
```

index.js 생성
```jsx
const express = require('express')
const mongoose = require('mongoose')
const cors = require('cors')
const Todo = require('./Models/Todo')

const app = express()
app.use(cors())
app.use(express.json())

// mongoose.connect('mongodb://localhost:27017/todolist')
mongoose.connect(process.env.DB_CONN)

app.get('/get',async(req,res)=>{
  const todos = await Todo.find()
  console.log('/get 호출')
  console.log(todos)
  res.json(todos)
})

app.put('/update/:id', async(req,res) => {
  const {id} = req.params
  const todo = await Todo.findById(id)
  todo.done = !todo.done
  todo.save()
  console.log('/update/:id 호출')
  console.log(todo)
  res.json(todo)
})

app.delete('/delete/:id',async(req,res)=>{
  const {id} = req.params
  const todos = await Todo.findByIdAndDelete({_id:id})
  console.log('/delete/:id 호출')
  console.log(todos)
  res.json(todos)
})

app.post('/add',async(req,res) => {
  const task = req.body.task;
  const todos = await Todo.create({task:task})
  console.log('/add 호출')
  console.log(todos)
  res.json(todos)
})

app.listen(3001,() => {
  console.log("Server is Running!")
})
```

#### server koyeb 배포하기

##### 1. github에 올리기

.gitignore 파일 작성해서 node_modules는 제외시키고 server폴더를 기준으로 git init 해서 github에 올려준다.

![](/assets/img/react/react001.png)

##### 2. koyeb 배포

로그인 해서 overview에서 'Create Web Service' 클릭
![](/assets/img/react/react002.png)

'GitHub' 클릭
![](/assets/img/react/react003.png)

소스 올린 리파지토리 선택
![](/assets/img/react/react004.png)

Run Command - npm i;npm start 설정
![](/assets/img/react/react005.png)

Advanced에서 Environment variables에 몽고DB 서버 연결 URL 작성     
Port를 3001번으로 코드에 셋팅했으므로 맞게 설정.   
App name 값도 입력  
deploy 버튼 클릭  
![](/assets/img/react/react007.png)

배포작업이 진행되고  
![](/assets/img/react/react008.png)

로그에 서버가 Started 되는 메시지 확인  
![](/assets/img/react/react009.png)


##### 3. vscode 에서 확인
![](/assets/img/react/react010.png)
![](/assets/img/react/react011.png)
![](/assets/img/react/react012.png)
![](/assets/img/react/react013.png)

##### 4. koyeb에 배포한 서비스 삭제할 경우
![](/assets/img/react/react014.png)


#### client

프로젝트 생성
```bash
npm create vite
# project -> 이름: client, react, javascript 로 생성 
cd client
npm i
npm i axios
npm run dev
```

src/App.jsx
```jsx
import Home from './Home'

export default function App() {
  return (
    <>
      <Home/>
    </>
  )
}
```

src/Home.jsx
```jsx
import { useState, useEffect, useRef } from "react"
import axios from 'axios'
import './Home.css'

export default function Home(){
  const [todos,setTodos] = useState([])
  const [task,setTask] = useState("")

  const inputRef = useRef()

  useEffect(() => {
    async function getData(){
      const result = await axios.get('http://localhost:3001/get')
      setTodos(result.data)
      inputRef.current.focus()  
    }
    getData()
  },[])

  const handleAdd = async () => {
    await axios.post('http://localhost:3001/add',{task:task})
    const result = await axios.get('http://localhost:3001/get')
    setTodos(result.data) 
    inputRef.current.value = ""
    inputRef.current.focus()
  }

  const handleEdit = async (id) => {
    await axios.put('http://localhost:3001/update/'+id)
    const result = await axios.get('http://localhost:3001/get')
    setTodos(result.data)  
  }

  const handleDelete = async (id) => {
    await axios.delete('http://localhost:3001/delete/'+id)
    const result = await axios.get('http://localhost:3001/get')
    setTodos(result.data)  
  }

  return(
    <div className="home">
      <h2>Todo List</h2>
      <div className="create_form">
      <input type="text" placeholder="Enter Task" 
            onChange={(e) => setTask(e.target.value)}
            ref={inputRef}/>
      <button onClick={handleAdd}>Add</button>
      </div>
      {
        todos.length === 0
        ?
        <div><h2>No Record</h2></div>
        :
        todos.map(todo => (
          <div className="task" key = {todo._id}>
            <input type="checkbox" 
                  onChange={ () => handleEdit(todo._id)}
                  checked={todo.done ? "checked" : ""}/>
            <p className={todo.done ? "line_through" : ""}>{todo.task}</p>
            <div>
              <button onClick={() => handleDelete(todo._id)}> Delete </button>
            </div>
          </div>
        ))
      }
    </div>
  )
}
```

src/Home.css
```css
.home{
  display: flex;
  flex-direction: column;
  align-items: center;
}
.create_form input{
  width: 300px;
  padding: 10px;
  border-bottom: 2px solid;
  outline: none;
  margin-bottom: 10px;
}
.create_form button{
  padding: 10px;
  background-color: hsl(0, 0%, 15%);
  color: rgb(209, 206, 206);
  cursor: pointer;
}
.task{
  display: flex;
  align-items: center;
  width: 360px;
  justify-content: space-between;
  background-color: hsl(0, 0%, 15%);
  color: rgb(208, 204, 204);
  height: 35px;
  padding: 2px 5px 2px 5px;
  margin-top: 2px;
}
.line_through{
  text-decoration: line-through;
}
button ,input[type="checkbox"]{
  cursor: pointer;
}
```

#### client netlify 배포

##### 1. axios쪽 접속 url은 koyeb에 배포한 url로 수정한다. 

##### 2. github 레파지토리 생성 후 client 코드 올려준다.

##### 3. import from Git 클릭
![](/assets/img/react/react015.png)

##### 4. Deploy with GitHub 클릭
![](/assets/img/react/react016.png)

##### 5. 레파지토리 선택
![](/assets/img/react/react018.png)

##### 6. Site name 항목 입력후 중복체크 후, Deploy 사이트명 클릭
![](/assets/img/react/react019.png)

##### 7. 성공메시지 창이 나타남.
![](/assets/img/react/react020.png)

##### 8. 배포 내역 확인
![](/assets/img/react/react021.png)

### 22. React Router
우선 라우팅의 개념을 간단하게 알아보면 사용자가 요청한 링크주소
즉, URL에 맞는 페이지를 찾아서 보여주는 것이라고 할 수 있다.
MPA 방식에서는 여러 페이지를 분리해두고 페이지간의 이동으로 이 라우트 시스템을 구축을 하지만, SPA 방식의 리액트에서 라우트 시스템을 구축하기 위해서 React Router를 사용한다.
신규페이지를 불러오지 않는 SPA에서 각각의 URL에 따라 선택된 페이지를 렌더링 해준다.

#### 설치

```bash
npm i react-router-dom
```

#### <BrowserRouter>태그로 감싸기

react-router-dom에 내장되어 있는 BrowserRouter라는 컴포넌트를 사용하여 감싸면 된다.

src/main.jsx
```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { BrowserRouter } from "react-router-dom";

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
)
```

#### Routes, Route 컴포넌트 사용하기

< Routes > 컴포넌트는 여러 Route를 감싸서 그 중에서 해당되는 Route를 렌더링 해주는 역할을 합니다.
그리고 < Route >는 path 속성에는 경로를 element 속성에는 보여주고 싶은 컴포넌트를 넣어주면 됩니다.

```jsx
<Routes>
  <Route path="경로" element={<컴포넌트 />} />
</Routes>
```

src/App.jsx
```jsx
import { Route, Routes } from "react-router-dom";
import "./App.css";
import About from "./pages/About";
import Home from "./pages/Home";
import Profile from "./pages/Profile";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/profiles/:username" element={<Profile />} />
  </Routes>
  )
}
```
#### Link를 이용한 이동
html 페이지에서는 링크를 넣어줄 때 a 태그를 사용하지만,
리액트 라우터를 사용하는 프로젝트에서는 a 태그를 바로 사용하면 안된다.
왜냐하면 a 태그를 클릭하여 페이지를 이동할 때 브라우저에서는 페이지를 새로 불러오게 되기 때문에 Link를 사용한다.
Link 컴포넌트 역시 a 태그를 사용하긴 하지만, 페이지를 새로 불러오는 것을 막고
History API를 통해 브라우저 주소의 경로만 바꾸는 기능이 내장되어 있다.

```jsx
<Link to="경로">링크 이름</Link>
```
src/pages/Home.jsx
```jsx
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div>
      <h1>Home</h1>
      <p>가장 먼저 보여지는 페이지입니다.</p>
      <ul>
        <li>
          <Link to="/about">About</Link>
        </li>
        <li>
          <Link to="/profiles/chanwoong">profile1</Link>
        </li>
        <li>
          <Link to="/profiles/gildong">profile2</Link>
        </li>
        <li>
          <Link to="/profiles/void">존재하지 않는 프로필</Link>
        </li>
      </ul>
    </div>
  );
}
```

src/pages/About.jsx
```jsx
export default function About() {
  return (
    <div>
      <h1>소개</h1>
      <p>리액트 라우터를 사용해 보는 프로젝트입니다.</p>
    </div>
  );
}
```

#### url 파라미터

```jsx
 <Route path="/profiles/:username" element={<Profile />} />
```
```jsx
import { useParams } from "react-router-dom";

const data = {
  chanwoong: {
    name: "찬웅",
    message: "hello",
    imgsrc: '/profile.png',
  },
  gildong: {
    name: "길동",
    message: "안녕~~",
    imgsrc: '/profile.png',
  },
};

export default function Profile() {
  const { username } = useParams();
  let profile = null;
  if (typeof username !== "undefined") {
    profile = data[username];
  }

  return (
    <div>
      <h1>User Profile</h1>
      {profile ? (
        <div>
          <h2>{profile.name}</h2>
          <p>{profile.message}</p>
          <img src={profile.imgsrc} alt="" />
        </div>
      ) : (
        <p>존재하지 않는 프로필 입니다.</p>
      )}
    </div>
  );
}
```

### 22. Zustand

[npm trend](https://npmtrends.com/jotai-vs-recoil-vs-zustand)
- 독일어로 '상태'라는 뜻, 상태 관리 라이브러리 중 하나  
- 한개의 중앙에 집중된 형식의 스토어 구조를 활용하면서 상태를 정의하고 사용하는 방법이 단순하다.
- Context API를 사용할 때와 달리 상태 변경 시 불필요한 리랜더링을 일으키지 않도록 제어하기 쉽다.
- 동작을 이해하기 위해 알아야 하는 코드 양이 아주 적다. 


#### 1. zustand 설치

```bash
npm i zustand
```

#### 2. store 생성
- 스토어를 생성하기 위해 create 함수를 사용
- 스토어는 상태 변수와 해당 상태를 업데이트하는 액션(함수)으로 구성할 수 있다.
  - 버튼을 선택하는 함수
  - count 를 증가시키는 함수
  - count를 리셋하는 함수 등과 같은...

src/stores/storeButton.jsx
```jsx
import {create} from "zustand";

const useButtonStore = create((set) => ({
  count: 0,
  selectedButton: null,

  setSelectedButton: (button) => set({ selectedButton: button }),
  incrementCount: () => set((state) => ({ count: state.count + 1 })),
  removeCount: () => set({ count: 0 }),
}));

export default useButtonStore;
```

#### 3. 상태 변수 및 액션 사용
- 상태 변수와 액션을 사용하려면 컴포넌트 내에서 useStore함수를 호출

src/components/FirstChild.jsx
```jsx
import React from "react";
import useButtonStore from "../stores/storeButton";

export default function FirstChild() {

  const { setSelectedButton, incrementCount, removeCount } = useButtonStore((state) => state);

  const handleClick = (button) => {
    setSelectedButton(button);
  };

  return (
    <div>
      <h1>FirstChild</h1>
      <div>
        <button onClick={() => handleClick("O")}>O</button>
        <button onClick={() => handleClick("X")}>X</button>
      </div>
      <div>
        <button onClick={incrementCount}>카운트 증가</button>
        <button onClick={removeCount}>카운트 리셋</button>
      </div>
    </div>
  );
}
```

src/components/SecondChild.jsx
```jsx
import React from "react";
import useButtonStore from "../stores/storeButton";

export default function SecondChild() {

  const { count, selectedButton } = useButtonStore((state) => state);

  return (
    <div>
      <h1>SecondChild</h1>
      <p>카운트: {count}</p>
      <p>선택한 버튼: {selectedButton}</p>
    </div>
  );
}
```

src/Test.jsx
```jsx
import FirstChild from "./components/FirstChild";
import SecondChild from "./components/SecondChild";

export default function Test() {
  return (
    <div>
      <FirstChild />
      <SecondChild />
    </div>
  );
}
```

src/App.jsx
```jsx
import Test from "./Test";

export default function App() {
  return (
    <div>
      <Test />
    </div>
  );
}
```

src/index.css
```css
:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;

  color-scheme: light dark;
  color: rgba(255, 255, 255, 0.87);
  background-color: #242424;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#root {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

a {
  font-weight: 500;
  color: #646cff;
  text-decoration: inherit;
}
a:hover {
  color: #535bf2;
}

body {
  margin: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
}

h1 {
  font-size: 3.2em;
  line-height: 1.1;
}

button {
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 0.5em 1.2em;
  margin-left: 1em;
  font-size: 0.7em;
  font-weight: 500;
  font-family: inherit;
  background-color: #1a1a1a;
  cursor: pointer;
  transition: border-color 0.25s;
}
button:hover {
  border-color: #e420f2;
}
button:focus,
button:focus-visible {
  outline: 4px auto -webkit-focus-ring-color;
}

@media (prefers-color-scheme: light) {
  :root {
    color: #213547;
    background-color: #ffffff;
  }
  a:hover {
    color: #747bff;
  }
  button {
    background-color: #f9f9f9;
  }
}

p{
  background-color: #f9f9f9;
  height: 2.5em;
  line-height : 2.5em;
}
```
#### 4. prop사용과 비교

##### prop 사용
src/components/Form.jsx
```jsx
const Form = (props) => {
  return (
    <>
      <form onSubmit={props.onSubmit}>
        <input type='text' onChange={props.onAdd} value={props.memo} />
        <button type='submit'>작성완료</button>
      </form>
    </>
  );
};

export default Form
```

src/components/Memos.jsx
```jsx
const Memos = (props) => {
  return (
    <div>
      {props.memos.map((memo,index) => {
        return <p key={index}>{memo}</p>;
      })}
    </div>
  );
};
export default Memos
```

src/Test1.jsx
```jsx
import { useState } from 'react'
import Form from './components/Form';
import Memos from './components/Memos';

export default function Test1() {
  const [memo, setMemo] = useState('');
  const [memos, setMemos] = useState([]);

  const handleWriteMemo = (e) => {
    setMemo(e.target.value);
  };

  const handleAddMemo = (e) => {
    e.preventDefault();
    setMemos((prevMemos) => [...prevMemos, memo]);
    setMemo('');
  };

  return (
    <div>
      <h1>메모 작성하기</h1>
      <Form onAdd={handleWriteMemo} onSubmit={handleAddMemo} memo={memo} />
      <Memos memos={memos} />
    </div>
  );
}
```

src/App.jsx
```jsx
import Test1 from "./Test1";

export default function App() {
  return (
    <div>
      <Test1 />
    </div>
  );
}
```

##### zustand 사용

src/stores/storeMemos.jsx
```jsx
import {create} from 'zustand';

const useMemosStore = create((set) => ({
  memo: '',
  setMemo: (text) => set({ memo: text }),
  memos: [],
  setMemos: (newMemo) =>
    set((prev) => ({
      memos: [...prev.memos, newMemo],
    })),
}));

export default useMemosStore;
```

src/components/Form1.jsx
```jsx
import useMemosStore from '../stores/storeMemos';

const Form1 = () => {
  const { memo, setMemo, setMemos } = useMemosStore();

  const handleWriteMemo = (e) => {
    setMemo(e.target.value);
  };

  const handleAddMemo = (e) => {
    e.preventDefault();
    setMemos(memo);
    setMemo('');
  };

  return (
    <>
      <form onSubmit={handleAddMemo}>
        <input type='text' onChange={handleWriteMemo} value={memo} />
        <button type='submit'>작성완료</button>
      </form>
    </>
  );
};
export default Form1
```

src/components/Memos1.jsx
```jsx
import useMemosStore from '../stores/storeMemos';

const Memos1 = () => {
  const { memos } = useMemosStore();

  return (
    <div>
      {memos.map((memo,index) => {
        return <p key={index}>{memo}</p>;
      })}
    </div>
  );
};
export default Memos1
```

src/Test2.jsx
```jsx
import Form1 from './components/Form1';
import Memos1 from './components/Memos1';

export default function Test2() {
  return (
    <div>
      <h1>메모 작성하기</h1>
      <Form1 />
      <Memos1 />
    </div>
  );
}
```

src/App.jsx
```jsx
import Test2 from "./Test2";

export default function App() {
  return (
    <div>
      <Test2 />
    </div>
  );
}
```

### 23. Supabase Auth with React
#### github
Github -> Settings -> Developer Settings -> OAuth Apps -> New OAuth App
로 생성  
Authorization callback URL항목은 Supabase에서 복사하여 붙여넣기 한다.
![](/assets/img/react/auth000.png)

Supabase -> Authentication -> Providers에서 Github 항목을 Enabled 시킨다.  
Github에서 발급받은 Client ID, Client Secret를 복사해서 입력한다.
Callback URL(for OAuth)를 Copy해서 Github의 Authorization callback URL항목에 붙여넣기 한다.
![](/assets/img/react/auth001.png)

![](/assets/img/react/auth002.png)

src/23/GithubLogin.jsx
```jsx
import { createClient } from '@supabase/supabase-js'
import { useEffect, useState } from 'react';

export default function GithubLogin(){
  const supabaseUrl = 'https://qcvohuicddgcbzonedtt.supabase.co';
  const supabaseKey = '발급받은키'
  const supabase = createClient(supabaseUrl, supabaseKey);

  const [user,setUser] = useState();


  async function signInWithGithub(){
    let { data, error } = await supabase.auth.signInWithOAuth({
      provider: 'github'
    })
}

  async function logoutWithGithub(){
    let { error } = await supabase.auth.signOut()
  }
  return(
    <>
      <input type="button" onClick={signInWithGithub} value="로그인" />
      <input type="button" onClick={logoutWithGithub} value="로그아웃" />
    </>
  )
}
```

src/App.jsx
```jsx
import Login from "./23/GithubLogin"

export default function App() {
  return ( 
    <> 
      <Login />
    </> 
  )
}
```