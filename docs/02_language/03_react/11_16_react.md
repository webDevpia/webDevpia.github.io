---
title: 16. React Router
layout: default
grand_parent: Language
parent: React
nav_order: 16
has_children: false
permalink: /language/react/react_16
---
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