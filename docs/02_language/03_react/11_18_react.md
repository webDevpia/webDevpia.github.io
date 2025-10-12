---
title: 18. Supabase Auth with React
layout: default
grand_parent: Language
parent: React
nav_order: 18
has_children: false
permalink: /language/react/react_18
---

### 23. Supabase Auth with React
#### github
Github -> Settings -> Developer Settings -> OAuth Apps -> New OAuth App
로 생성  
Authorization callback URL항목은 Supabase에서 복사하여 붙여넣기 한다.
![](/img/auth000.png)

Supabase -> Authentication -> Providers에서 Github 항목을 Enabled 시킨다.  
Github에서 발급받은 Client ID, Client Secret를 복사해서 입력한다.
Callback URL(for OAuth)를 Copy해서 Github의 Authorization callback URL항목에 붙여넣기 한다.
![](/img/auth001.png)

![](/img/auth002.png)

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