---
title: 2. React 페이지 만들기
layout: default
grand_parent: Language
parent: React 쇼핑몰 제작
nav_order: 2
has_children: false
permalink: /language/react1/react_2
---

## 1. React 페이지 만들기

### 1.  프로젝트 생성

```sh
npx create-react-app blog1
cd blog1
npm start
```
React 앱은 웹브라우저에서 http://localhost:3000 확인

### 2. 컴포넌트 파일 생성

**src/components/Header.js**
```js
import React from 'react';
const Header = () => { return (
  <div>
    헤더
  </div>
);
};
export default Header;
```

**src/components/Slider.js**
```js
import React from 'react';
const Slider = () => { return (
  <div> 
    슬라이더
  </div>
);
};
export default Slider;
```

**src/components/Main.js**
```js
import React from 'react'
function Main() { return (
  <div>
    메인
  </div>
)
}
export default Main
```

**src/components/Footer.js**
```js
import React from 'react'
function Footer() { return (
  <div>
    풋터
  </div>
)
}
export default Footer
```

**src/App.js**
```js
import Header from './components/Header'; 
import Slider from './components/Slider'; 
import Main from './components/Main'; 
import Footer from './components/Footer';
function App() {
  return (
    <> 
      <Header></Header> 
      <Slider></Slider> 
      <Main/>
      <Footer/>
    </> 
  );
}
export default App;
```

### 3. Style 입히기 
#### 1. 인라인 스타일  

{% raw %}style={{}} 머스테치(Mustache){% endraw %}

**src/components/Header.js**
```js{% raw %}
import React from 'react';
const Header = () => {
return (
    <div style={{width:"100%", color:"white", height:"50px", backgroundColor:"green"}}> 
      헤더
    </div>
  );
};
export default Header;{% endraw %}
```
{% raw %}style={{ ... }} {% endraw %} → JavaScript 객체를 표현하는 JSX 문법  
바깥 { ... } → JSX 안에서 JavaScript 표현식을 넣기 위한 괄호.  
안쪽 { ... } → JavaScript의 객체 리터럴 (스타일 정의용) JSX 안에 객체를 넣는다.  

#### 2. props로 스타일 적용하기

**src/App.js**
```js{% raw %}
import Header from './components/Header'; 
import Slider from './components/Slider'; 
import Main from './components/Main'; 
import Footer from './components/Footer';
function App() {
  return (
    <> 
      <Header></Header> 
      <Slider style={{width:"100%", color:"white", height:"200px", backgroundColor:"gold"}}></Slider>
      <Main/>
      <Footer/>
    </> 
  );
}
export default App;{% endraw %}
```

**src/components/Slider.js**
```js
import React from 'react';
const Slider = (props) => { return (
  <div style={props.style}> 
    슬라이더
  </div>
);
};
export default Slider;
```

| 내용 | 설명 |
|---|---|
| {% raw %}style={{ ... }} {% endraw %}| 부모 컴포넌트(App)에서 스타일을 자식(Slider)에게 전달함 |
| props | 자식 컴포넌트가 전달받은 속성을 담는 객체 |
| rops.style | 부모가 보낸 스타일 객체를 꺼내어 <div>에 적용함 |
| props란 | props는 properties(속성)의 줄임말로, 부모 컴포넌트가 자식 컴포넌트에게 값을 전달할 때 사용하는 객체props는 자식 컴포넌트가 외부 데이터를 전달받는 방법 |

#### 3. 스타일 변수

**src/components/Main.js**
```js
import React from 'react'
function Main() {
  //라인 스타일을 객체 형태로 정의
  const style2 = {
  width: '100%',
  height: '200px', backgroundColor: 'skyblue', color: '#fff'
}
  return (
    <div style={style2}>
      메인
    </div>
  )
}
export default Main
```
style={style2} → style={객체} 구조는 JSX에서 인라인 스타일을 적용하는 기본 문법 (JSX에서 style에 객체를 넣는 방식)

#### 4. 외부 CSS 클래스 적용하기

**src/App.css**
```css
.footerStyle { 
  background-color: tomato; 
  color:#fff;
  height: 100px;
}
```

**src/components/Footer.js**
```js
import React from 'react'
import '../App.css';

function Footer() { return (
  <div className="footerStyle">
    풋터
  </div>
)
}
export default Footer
```
Footer 컴포넌트에서 외부 CSS 파일(App.css)의 클래스를 불러와서, className 속성을 통해 JSX 요소에 스타일을 적용하는 방식

### 4. 코드 전달하기

**node_modules** 폴더를 제외하고 전달

**package.json** 파일에 설치해야할 라이브러리 목록 등 정보가 있으므로 코드를 받아서 루트 디렉토리에서 설치하면 된다.

```sh
npm i
```
