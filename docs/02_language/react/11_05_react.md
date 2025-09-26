---
title: React 5
layout: default
grand_parent: Language
parent: React
nav_order: 5
has_children: false
permalink: /language/react/react_5
---

### 5. conditional rendering(조건부 랜더링)

src/App.jsx
```jsx
import UserList from './05/UserList'
export default function App() {
  return (
    <>
      <UserList/>
    </>
  )
}
```

src/05/UserList.jsx
```jsx
import UserGreeting from "./UserGreeting"

export default function UserList() {
  return (
    <>
      <UserGreeting isLoggedIn={true} username="hong"/>
      <UserGreeting isLoggedIn={false}/>
      <UserGreeting/>
    </>
  )
}
```

#### **if/else**

src/05/UserGreeting.jsx
```jsx
export default function UserGreeting({isLoggedIn = false, username = "Guest"}){
  if (isLoggedIn){
    return <h2 className="text-4xl bg-lime-400 rounded-full p-7 m-8">Welcome {username}</h2>
  }else{
    return <h2 className="text-4xl bg-pink-500 rounded-full p-7 m-8">Please log in to continue {username}</h2>
  }
```

#### **삼항연산자**

src/05/UserGreeting.jsx
```jsx
export default function UserGreeting({isLoggedIn = false, username = "Guest"}){
  return(isLoggedIn ? <h2 className="text-4xl bg-lime-400 rounded-full p-7 m-8">Welcome {username}</h2> :
                      <h2 className="text-4xl bg-pink-500 rounded-full p-7 m-8">Please log in to continue {username}</h2>)
}
```

src/05/UserGreeting.jsx
```jsx
export default function UserGreeting({isLoggedIn = false, username = "Guest"}){
  const welcomeMessage =  <h2 className="text-4xl bg-lime-400 rounded-full p-7 m-8">Welcome {username}</h2>
  const loginPrompt = <h2 className="text-4xl bg-pink-500 rounded-full p-7 m-8">Please log in to continue {username}</h2>
  return(isLoggedIn ? welcomeMessage : loginPrompt)
}
```
#### **논리연산자를 이용한 단축평가**

src/05/UserGreeting.jsx
```jsx
export default function UserGreeting({isLoggedIn = false, username = "Guest"}){
  const welcomeMessage =  <h2 className="text-4xl bg-lime-400 rounded-full p-7 m-8">Welcome {username}</h2>
  const loginPrompt = <h2 className="text-4xl bg-pink-500 rounded-full p-7 m-8">Please log in to continue {username}</h2>

   return(
    <>
      {isLoggedIn && welcomeMessage} 
      {isLoggedIn || loginPrompt}
    </>
  )
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

src/05/Profile.jsx
```jsx {%raw%}
export default function Profile({user,key}) {
  return (
    <>  
    <div className="flex flex-col items-center justify-center">
      <h1>{user.name}</h1>
      <img
        className="rounded-full m-10 "
        src={user.imageUrl}
        alt={'Photo of ' + user.name}
        style={{
          width: user.imageSize,
          height: user.imageSize
        }}
      />
      </div>
    </>
  );
} {%endraw%}
```

src/05/ConditionTest.jsx
```jsx
import Profile from './Profile';
const user = [
  {
    id: '1',
    name: "Hedy Lamarr",
    imageUrl: "https://i.imgur.com/yXOvdOSs.jpg",
    imageSize: 120
  },
  {
    id: "2",
    name: "placehold",
    imageUrl: "https://placehold.co/800",
    imageSize: 120
  }
];

export default function ConditionTest() {
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
