---
title: 12. useEffect hook
layout: default
grand_parent: Language
parent: React
nav_order: 12
has_children: false
permalink: /language/react/react_12
---
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