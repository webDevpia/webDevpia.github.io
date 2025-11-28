---
title: 3. 컴포넌트 만들기
layout: default
grand_parent: Language
parent: React
nav_order: 3
has_children: false
permalink: /language/react/react_3
---

### 3. 컴포넌트 만들기

#### 이미지 넣고 css 적용

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
import './index.css'
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

tailwindcss를 같이 사용할 경우

src/Card.jsx
```jsx
import './index.css'
function Card(){
  return(
    <>
    <div className="card flex flex-col items-center justify-center">
       <img className="card-image w-full max-w-[600px] h-auto mx-auto" 
            src="https://placehold.co/600x600"/>
       <h2 className="card-title">Test</h2>
       <p className='card-text'>I make Youtube videos and play</p>
    </div>
    {/* <img src={profilePic}/> */}
    </>
  )

```


#### React Components with css

##### 1. external

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

##### 2. modules

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

##### 3. inline
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

