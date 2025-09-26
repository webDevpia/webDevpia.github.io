---
title: React 4
layout: default
grand_parent: Language
parent: React
nav_order: 4
has_children: false
permalink: /language/react/react_4
---

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
      {/* <Student name="이정인" age="20" isStudent={true} /> */}
      <Student/>
    </>
  )
}

export default StudentList
```

propTypes을 이용하여 값의 타입을 지정, 오류의 확인은 웹브라우저의 콘솔창에서 확인할 수 있다.  
prop-types는 React의 타입 검사를 위한 별도의 패키지입니다.  
React 16.4 버전 이후부터는 별도로 설치해야 합니다.  

```bash
npm install prop-types
```

src/04/Student.jsx
```jsx
import PropTypes from 'prop-types'
import './Student.css'
function Student({name="Guest", age=0, isStudent=false}){
  return(
    <div className="student">
      <p>Name : {name}</p>
      <p>Age : {age}</p>
      <p>Student : {isStudent ? "Yes" : "No" }</p>
    </div>
  )
}
// 타입이 안맞을경우 웹브라우저 콘솔에서 오류확인, 실행은 됨.
// PropTypes 정의
Student.propTypes = {
  name: PropTypes.string,       // 문자열
  age: PropTypes.number,        // 숫자
  isStudent: PropTypes.bool,    // 불리언
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
