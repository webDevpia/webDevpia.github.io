---
title: React 7
layout: default
grand_parent: Language
parent: React
nav_order: 7
has_children: false
permalink: /language/react/react_7
---

### 7. click events

src/App.jsx
```jsx
import Button from "./07/Button"

export default function App() {

  return (
    <>
      <Button/>
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
      <button onClick={(e) => handleClick4(e)}>Click me 😊</button>
      {/* <button onDoubleClick={(e) => handleClick4(e)}>Click me 😊</button> */}
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
  const handleClick1 = (e) => {
    document.getElementById("image").style.display = "block"
  }
  
  return(
    <img src={imgurl} onClick={(e)=>handleClick(e)}></img>
    <button onClick={() => handleClick1()}>Click me 😁</button>
  )
}
```
