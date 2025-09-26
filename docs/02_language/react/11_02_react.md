---
title: React 기본구조
layout: default
grand_parent: Language
parent: React
nav_order: 2
has_children: false
permalink: /language/react/react_2
---

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
