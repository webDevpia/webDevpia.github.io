---
title: 3. 쇼핑몰 만들기
layout: default
grand_parent: Language
parent: React 쇼핑몰 제작
nav_order: 3
has_children: false
permalink: /language/react1/react_3
---

## 1. 쇼핑몰 만들기

### 1.  프로젝트 생성

```sh
npx create-react-app shop
```

### 2.  앱실행

```sh
cd shop
npm start
```
React 앱은 웹브라우저에서 http://localhost:3000 확인

### 3. App.js 수정
import logo from './logo.svg';  
로고 삭제 App 사이에 있는거 다 삭제 -> <div className="App"> </div> 사이 삭제

**src/App.js**
```js
import './App.css';

function App() {
  return (
    <div className="App">
      
    </div>
  );
}

export default App;
```

### 4. 터미널에서 React-Bootstrap 라이브러리를 설치
구글에서 react bootstrap 검색 [https://react-bootstrap.netlify.app/](https://react-bootstrap.netlify.app/) 가서 get started 버튼클릭  

```sh
npm install react-bootstrap bootstrap
```

### 5. react bootstrap cdn link  걸기

public  > index.html  > <head> 태그 사이에 넣기

**public/index.html**
```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/css/bootstrap.min.css"
  integrity="sha384-SgOJa3DmI69IUzQ2PVdRZhwQ+dy64/BUtbMJw1MZ8t5HZApcHrRKUc4W0kG879m7"
  crossorigin="anonymous"
/>
```

### 6. 네비게이션바 추가

react bootstrap > 왼쪽 서치창 > navbar 검색 해서 코드 참고해서 추가

**src/App.css**
```js
import './App.css';
import { Navbar, Container, Nav} from 'react-bootstrap'
function App() {
  return (
    <div className="App">
        <Navbar bg="dark" data-bs-theme="dark">
        <Container>
          <Navbar.Brand href="#home">Navbar</Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link href="#home">Home</Nav.Link>
            <Nav.Link href="#features">Features</Nav.Link>
            <Nav.Link href="#pricing">Pricing</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </div>
  );
}

export default App;
```

### 7. 슬라이드 넣기

[이미지데이터](./data/img.zip) 다운로드 후 **public**폴더에 img 폴더 넣기
**public/img** 안에 이미지파일 있어야 함.

App.js 파일에서 navbar 밑에 

**src/App.js**
```js
<div className="slider"></div>
```

index.css 파일에 추가

```css
  .slider {
    height:500px; 
    background-image: url('../public/img/slider.jpg'); background-size: cover;
    background-position: center;
    margin-bottom: 30px;
  }
```

### 8. Slider 아래쪽 상품을 가로로 화면을 3등분해서 추가

App.js  파일 안에 (slider 아래쪽에)

```js{%raw%}
<div className="container" style={{textAlign:"center"}}> 
  <div className="row">
    <div className="col-md-4">1</div>
    <div className="col-md-4">2</div>
    <div className="col-md-4">3</div>
  </div>
</div> {%endraw%}
```

3등분 안에 컨텐츠 넣기

```js
<div className="row">
  <div className="col-md-4">
    <img src="/img/fruit1.jpg" width="80%" alt=""/> <h4>상품명</h4>
    <p>상품정보</p>
    <span>가격</span>
  </div>
  <div className="col-md-4">
    <img src="/img/fruit2.jpg" width="80%" alt=""/> <h4>상품명</h4>
    <p>상품정보</p>
    <span>가격</span>
  </div>
  <div className="col-md-4">
    <img src="/img/fruit3.jpg" width="80%" alt=""/> <h4>상품명</h4>
    <p>상품정보</p>
    <span>가격</span>
  </div>
</div>
```

### 9. 코드가 길어지면 객체 데이터 import/export 처리 → 상품 컴포넌트 만들기
src폴더 > db 폴더만들고> fruit.js 만들기

`let data =  [ { }, { }, { } ] `

**src/db/fruit.js**
```js
let data = [
    {
      id: 1,
      title: "수박",
      imgUrl: "img/fruit1.jpg",
      content: "당도선별 프리미엄 고당도 하우스수박 5~6kg",
      price: 29000,
    },
    {
      id: 2,
      title: "참외",
      imgUrl: "img/fruit2.jpg",
      content: "산지직송 성주 달콤참외 3kg",
      price: 16900,
    },
    {
      id: 3,
      title: "사과",
      imgUrl: "img/fruit3.jpg",
      content: "고씨네농장 고당도 청송사과, 햇부사 5kg",
      price: 13000,
    },
    {
      id: 4,
      title: "바나나",
      imgUrl: "img/fruit4.jpg",
      content: "델몬트 필리핀 바나나 6kg",
      price: 15000,
    },
    {
      id: 5,
      title: "딸기",
      imgUrl: "img/fruit5.jpg",
      content: "설향 딸기, 킹스베리 1박스",
      price: 14500,
    },
    {
      id: 6,
      title: "오렌지",
      imgUrl: "img/fruit6.jpg",
      content: "캘리포니아 네이블 오렌지 4kg",
      price: 17000,
    },
    {
      id: 7,
      title: "토마토",
      imgUrl: "img/fruit7.jpg",
      content: "행복한 농부 완숙찰토마토 5kg",
      price: 20000,
    },
    {
      id: 8,
      title: "포도",
      imgUrl: "img/fruit8.jpg",
      content: "팜앤프룻 프리미엄 아삭한 애플청포도",
      price: 25000,
    },
    {
      id: 9,
      title: "망고",
      imgUrl: "img/fruit9.jpg",
      content: "프리미엄 제주애플망고 1박스",
      price: 18500,
    },
  ];
  
  export default data;
  
```

App.js 파일에서import  fruit.js useState 만들기

**src/App.js**
```js
import data from './db/fruit'; 
import { useState } from 'react';

function App(){
  let [fruit] = useState(data); 
  console.log(fruit[0].price);
}
```

**src/App.js**
```js{%raw%}
<div className="container" style={{textAlign:"center"}}> 
  <div className="row">
    <div className="col-md-4">
      <img src="/img/fruit1.jpg" width="80%" alt=""/> <h4>{fruit[0].title}</h4>
      <p>{fruit[0].content}</p> 
      <span>{fruit[0].price}</span>
    </div>
    <div className="col-md-4">
      <img src="/img/fruit2.jpg" width="80%" alt=""/> <h4>{fruit[1].title}</h4>
      <p>{fruit[1].content}</p> 
      <span>{fruit[1].price}</span>
    </div>
    <div className="col-md-4">
      <img src="/img/fruit3.jpg" width="80%" alt=""/> <h4>{fruit[2].title}</h4>
      <p>{fruit[2].content}</p> 
      <span>{fruit[2].price}</span>
    </div>
  </div>
</div>{%endraw%}
```
브라우저에서 확인 : 상품잘나오는지 App.js에서 콘솔로 데이터 오는지 확인

### 10. 제품 컴포넌트 Products.js 파일로 만들기 넣기

컴포넌트는 첫글자를 대문자로하기로 약속했음. 첫 글자가 대문자여야 React가 사용자 정의 컴포넌트라고 인식함

**src/components/Products.js**
```js{%raw%}
import React from "react";
const Products = (props) => {
  return (
    <div className="col-md-4" style={{marginBottom:"50px"}}> 
      <img src={props.fruit.imgUrl} width="80%" alt=""/>
      <h5 style={{marginTop:"10px"}}>{props.fruit.title}</h5> 
      <p>{props.fruit.content}</p> <span>{props.fruit.price}</span>
    </div>
  );
};
export default Products;{%endraw%}
```

아래의 코드 해당 위치에 추가  
맨 위쪽에 추가  -> `import Products from './components/Products';`  
`<div className="row">` 의 자식태그 내용 제거하고 넣기 -> `<Products fruit={fruit[0]}/>`    

**src/App.js**
```js{%raw%}
import Products from './components/Products';

function App() {
   return (
     <div className="container" style={{textAlign:"center"}}> 
        <div className="row">
         <Products fruit={fruit[0]}/>
        </div> 
      </div>
      );
}

export default App;{%endraw%}
```
브라우저에서 확인 : 상품잘나오는지 App.js에서 콘솔로 데이터 오는지 확인

**클린코드**  
Products.js 수정  
바뀐뒤에도 동일하게 나오는지 확인

```js{%raw%}
import React from "react";
const Products = (props) => {
  const { id, title, price, imgUrl, content} = props.fruit;
  return (
    <div className="col-md-4" style={{ marginBottom: "50px" }}> 
      <img src={imgUrl} width="80%" alt=""/>
      <h5 style={{ marginTop: "10px" }}>{title}</h5> 
      <p>{content}</p>
      <span>{price}</span>
    </div>
  );
};
export default Products;{%endraw%}
```
브라우저에서 확인 : 상품잘나오는지 App.js에서 콘솔로 데이터 오는지 확인

**src/App.js**
```js{%raw%}
     <div className="container" style={{textAlign:"center"}}> 
        <div className="row">
         {
            fruit.map((ele,i)=>{
            return(
            <Products fruit={fruit[i]}  i={i} key={data[i].id} /> )
            })
          }
        </div> 
      </div>{%endraw%}
```
