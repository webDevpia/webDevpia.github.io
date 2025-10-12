---
title: 13. useContext hook
layout: default
grand_parent: Language
parent: React
nav_order: 13
has_children: false
permalink: /language/react/react_13
---
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