---
title: 14. useRef hook
layout: default
grand_parent: Language
parent: React
nav_order: 14
has_children: false
permalink: /language/react/react_14
---
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