---
title: 4. Router 설정
layout: default
grand_parent: Language
parent: React 쇼핑몰 제작
nav_order: 4
has_children: false
permalink: /language/react1/react_4
---

## 1. Router 설정
라우팅이란, 사용자가 요청한 URL 경로에 따라 알맞은 페이지나 컴포넌트를 보여주는 기능

### 1.  프로젝트 생성
기존 파일에서 계속 작업을 진행하거나, [코드](./data/shop1.zip) 다운로드 후 압축풀고, 작업경로로 이동해서 라이브러리 설치해서 진행

```sh
npm i
```

### 2.  앱실행

```sh
cd shop
npm start
```
React 앱은 웹브라우저에서 http://localhost:3000 확인

### 3. 라이브러리 설치
```sh
npm install react-router-dom
```

### 4. 라이브러리 사용

**src/index.js**
```js
// import 추가
import { BrowserRouter } from 'react-router-dom';

// <React.StrictMode>  주석으로 하면 렌더링이 한번만 된다.
  <BrowserRouter> 
    <App /> 
  </BrowserRouter>
// </React.StrictMode>
```

라이브러리 import하기  
**src/App.js**
```js
import { Routes, Route, Link } from 'react-router-dom'
```

navbar 아래에 라우터 태그넣기. 
**src/App.js**
```js
<Routes>
  <Route path="/" element={<div>메인페이지임</div>} /> 
  <Route path="detail" element={<div>상세페이지임</div>} /> 
</Routes>
```
웹브라우저에서   
http://localhost:3000/  
http://localhost:3000/detail  
접속해서 메뉴바 밑에 내용확인

메인페이지임 자리로 slider와 상품내역 이동

**src/App.js**
```js
<Routes>
  <Route path="/" element={<div>
    //아래의 코드를 떼서 메인페이지임 자리에 넣기
    <div className="slider"></div>

    <div className="container"> 
      <div className="row">
        {
          fruit.map((ele,i)=>{
              return(
                <Products fruit={fruit[i]}  i={i} key={data[i].id} /> 
              )
            }
          )
        } 
      </div> 
    </div>
</div>} /> 
  <Route path="detail" element={<div>상세페이지임</div>} /> 
</Routes>
```

href속성값을 수정하고 확인

**src/App.js**
```js
  <Nav.Link href="/">Home</Nav.Link>
  <Nav.Link href="/detail">상세페이지</Nav.Link>
```

### 5. 상세 페이지 컴포넌트 만들기

**src/components/Detail.js** 만들기   
**rfce** 입력 후 enter, tab 하고  
아래의 코드를 작성

**src/components/Detail.js** 
```js
import React from 'react';
function Detail() {
  return (
    <div className="container">
      <div className="row">
        <div className="col-md-6">
          <img src="img/fruit1.jpg" width="100%" alt=""/>
        </div>
        <div className="col-md-6">
          <h4 className="pt-5">상품명</h4>
          <p>상품설명</p>
          <p>12000원</p>
          <button className="btn btn-danger">주문하기</button> 
        </div>
      </div>
    </div>
  )
}
export default Detail;
```

**src/App.js**

`<Route path="detail" element={<div>상세페이지임</div>} />` 코드를 상세페이지임 대신에 `<Detail/>` 수정
```js
<Route path="detail" element={<Detail/>} />
```

컴포넌트 import 확인
```js
import Detail from './components/Detail';
```

App.js 상단에 추가  
전체 페이지 새로고침 없이 컴포넌트만 전환
useNavigate, Outlet 사용  
상단에 있는곳 라우터 돔에서 추가하기(기존코드에서 추가된 것만 확인)   
`import { Routes, Route, Link, useNavigate, Outlet } from 'react-router-dom'`  

**여기에 추가**위치에 `let navigate = useNavigate();` 코드 추가 

**src/App.js**
```js
function App(){
  let [fruit] = useState(data); 
  // 여기에 추가
  let navigate = useNavigate();
}
```

App.js 안에 
nav 태그안에 추가
Nav.Link를 이용해 페이지 이동을 구현(네비게이션 링크 추가)
라우터를 만들고 링크를 걸어야함

**src/App.js**
```js
<Nav className="me-auto">
  <Nav.Link onClick={()=>{ navigate('/')}}>홈으로</Nav.Link>
  <Nav.Link onClick={()=>{ navigate('/detail')}}>상세페이지</Nav.Link>
  <Nav.Link onClick={() => { navigate('/cart') }}>장바구니</Nav.Link> 
  <Nav.Link onClick={() => { navigate('/about') }}>회사소개</Nav.Link> 
</Nav>
```

**src/App.js**
```js
<Route path="detail" element={<Detail />} />  
// 여기에 추가
<Route path="*" element={<div>없는 페이지입니다.</div>} />
```

| 코드 | 설명 |
|------|------|
| `<Nav.Link onClick={()=>{ navigate(1)}}>Home</Nav.Link>` | 앞으로 한페이지 이동 |
| `<Nav.Link onClick={()=>{ navigate(-1)}}>Home</Nav.Link>` | 뒤로 한페이지 이동 |
| `<Route path="*" element={<div>없는 페이지입니다.</div>} />` | 404 페이지 |

nested routes (태그안에 태그) Outlet (보여줄 자리를 정함)
- 여러 유사한 페이지가 필요할 때- 모달이나  tap 페이지를 만들 때 중첩 라우트는 부모 컴포넌트에 <Outlet />이 있어야 자식 컴포넌트가 보임

App.js에서  Route  `<Detail/>` 아래에 코드 3줄 추가

**src/App.js**
```js
<Route path="detail" element={<Detail/>} />
<Route path="/about" element={<About/>} />
<Route path="/about/member" element={<Member/>} /> 
<Route path="/about/location" element={<Location/>} />
```
**src/App.js**
```js{%raw%}
//app 아래, export default App; 위에 추가
function About(){
  return(
    <>
      <h4 style={{textAlign:'center'}}>회사정보</h4> 
    </>
  );
}
function Member(){
  return(
    <>
      <h4 style={{textAlign:'center'}}>Member</h4> 
    </>
  );
}
function Location(){
  return(
    <>
      <h4 style={{textAlign:'center'}}>Location</h4> 
    </>
  );
}{%endraw%}
```

nested route (태그안에 태그가 들어감)  - Outlet

**src/App.js**
```js
<Route path="/about" element={<About/>} >
  <Route path="member" element={<Member/>} /> 
  <Route path="location" element={<Location/>} />
</Route>
```

**src/App.js**
```js
//About 안에 하위 컴포넌트 넣고 싶은 위치에 <Outlet></Outlet> 추가
function About(){
  return(
    <> 
      <h4>회사정보</h4> 
      <Outlet></Outlet> 
    </>
  );
}
```

about안에 Outlet을 넣어서 url 요청하면 element  2 개가 보임

| 회사정보 | /about |
| 멤버     | /about/member |
| 위치     | /about/location |

### 6. React Router의 URL 파라미터(param) 기능을 이용해 상세 페이지 생성


**src/App.js**
```js
<Route path="/detail" element={<Detail fruit={fruit}/>} />
```


**src/components/Detail.js**
```js
import React from 'react';

function Detail(props) {
  return (
    <div className="container">
      <div className="row">
        <div className="col-md-6">
          <img src={props.fruit[0].imgUrl} width="100%" alt=""/>
        </div>
        <div className="col-md-6">
          <h5 className="pt-5">{props.fruit[0].title}</h5> 
          <p>{props.fruit[0].content}</p> 
          <p>{props.fruit[0].price}</p>
          <button className="btn btn-danger">주문하기</button> 
        </div>
      </div>
    </div>
  )
}
export default Detail;
```

**src/App.js**
```js
<Route path="/detail/:paramId" element={<Detail fruit={fruit}/>} />
```

**src/components/Detail.js**
```js
import React from 'react';
import { useParams } from "react-router-dom";

function Detail(props) {

  let {paramId} = useParams();
  console.log(paramId);
  const { imgUrl, title, content, price } = props.fruit[paramId];

  return (
    <div className="container">
      <div className="row">
        <div className="col-md-6">
          <img src={'/' + imgUrl} width="100%" alt={title} />
          {/* <img src={process.env.PUBLIC_URL + '/' + imgUrl} width="100%" alt={title} /> */} 
        </div>
        <div className="col-md-6">
          <h5 className="pt-5">{title}</h5>
          <p>{content}</p>
          <p>{price}</p>
          <button className="btn btn-danger">주문하기</button>
        </div>
      </div>
    </div>
  )
}

export default Detail;
```

| 브라우저에서 확인,  URL 작성, 크롬창에서 콘솔(F12),  paramId 값 확인 |
| http://localhost:3000/detail/1 |
| http://localhost:3000/detail/3 |

### 7. 메인페이지에서 상품 상세페이지 네비게이션 (링크 연결)

App.js
slider 아래쪽에 상품 컴포넌트 수정 및 확인(스타일 추가) 메뉴바와 간격 추가   
`{%raw%}style={{marginTop:'30px'}}{%endraw%}` 추가

**src/App.js**
```js{%raw%}
<div className="container"  style={{marginTop:'30px'}}> 
  <div className="row">
    {
    fruit.map((ele,i)=>{
      return(
        <Products fruit={fruit[i]}  i={i} key={data[i].id} />
      ) } )
    } 
  </div>
</div>{%endraw%}
```

**src/components/Products.js**
```js{%raw%}
import React from "react";
import { useNavigate } from "react-router-dom";
import { Nav } from "react-bootstrap";
const Products = (props) => {
  const { id, title, price, imgUrl, content} = props.fruit;
  let navigate = useNavigate();
  return (
    <div className="col-md-4" style={{ marginBottom: "50px" }}>
      <Nav.Link   onClick={() => { navigate("/detail/" +(id-1)) }}  className="c1"> 
        <img src={imgUrl} width="80%" />
        <h5 style={{ marginTop: "10px" }}>{title}</h5>
        <p>{content}</p>
        <span>{price}</span>
      </Nav.Link>
    </div>
  );
};
export default Products;
{%endraw%}
```

**index.css**
```css
.c1 {text-decoration: none; color:#000; text-align: center;} .c1:hover {color: green;}
```

메인에서 상품 클릭하면 사과-> 사과 상품으로 잘 가는지 확인, 다른 상품도 맞게 잘 가는지 체크

### 8. title과 버튼 배치

**src/components/Title.js**
```js{%raw%}
import React from "react";
const Title = () => {
  let csst1 = {
    marginTop: "70px",
    textAlign: "center",
  };
  return (
    <>
    <h3 style={csst1}>햇과일 BEST</h3>
      <p style={{ textAlign: "center" }}>
        {" "}
      농부가 추천하는 제철과일을 만나보세요. </p>
    </>
  );
};
export default Title;{%endraw%}
```

App.js 안에 slide 아래 배치  `<Title/>` 추가하고 컴포넌트 import 여부 확인

App.js 상단에 확인

**src/App.js**
```js
import { useState } from 'react';
import { Button, Navbar, Container, Nav } from 'react-bootstrap'
```

App.js 리턴위에 추가

**src/App.js**
```js
let [fruit, setFruit] = useState(data);
  const sortByName = () => {
  let sortedFruit = [...fruit].sort((a, b) => (a.title > b.title ? 1 : -1)); 
  setFruit(sortedFruit);
  console.log(sortedFruit);
};
const sortByPriceLowToHigh = () => {
  let sortedFruit = [...fruit].sort((a, b) => a.price - b.price); 
  setFruit(sortedFruit);
  console.log(sortedFruit);
};
const sortByPriceHighToLow = () => {
  let sortedFruit = [...fruit].sort((a, b) => b.price - a.price); 
  setFruit(sortedFruit);
  console.log(sortedFruit);
};
```

`<Title />` 아래 옆의 코드전체 추가

**src/App.js**
```js{%raw%}
<div className="container">
  <div className="row">
    <div style={{ textAlign: "center" }}>
      <Button variant="outline-primary" onClick={sortByName}> 이름순 정렬 </Button>
      {" "}
      <Button variant="outline-secondary" onClick={sortByPriceLowToHigh}>낮은가격순 정렬</Button>
      {" "} 
      <Button variant="outline-success" onClick={sortByPriceHighToLow}>높은가격순 정렬</Button>
      {" "} 
    </div>
  </div>
</div>{%endraw%}
```

상품 정렬 후 링크가 올바르게 작동하도록 하기

App.js 과일 데이터 map 수정

**src/App.js**
```js{%raw%}
<div className="container" style={{marginTop:'30px'}}>
  <div className="row">
    {
      fruit.map((ele, i) => {
          return (
            <Products fruit={fruit[i]} i={i}  key={fruit[i].id} /> 
          );
        }
      )
    }
  </div> 
</div>{%endraw%}
```

**src/components/Title.js**
```js{%raw%}
import React from "react";
import { useNavigate } from "react-router-dom"; import { Nav } from "react-bootstrap";
const Products = (props) => {
  const { id, title, price, imgUrl, content} = props.fruit; 
  let navigate = useNavigate();
  return (
    <div className="col-md-4" style={{ marginBottom: "50px" }}>
      <Nav.Link   onClick={() => { navigate("/detail/" +id) }}  className="c1"> 
        <img src={imgUrl} width="80%" />
        <h5 style={{ marginTop: "10px" }}>{title}</h5>
        <p>{content}</p>
        <span>{price}</span>
      </Nav.Link>
    </div>
  );
};
export default Products;{%endraw%}
```

**src/components/Detail.js**
```js{%raw%}
import React from 'react';
import { useParams } from "react-router-dom"; 

function Detail(props) {
  let {paramId} = useParams();
  console.log(paramId);
  //const { id, imgUrl, title, content, price } = props.fruit[paramId];
  // props.fruit 배열에서 id가 paramId와 일치하는 상품을 찾아 item 변수에 저장
  // paramId는 문자열이므로 parseInt를 사용해 숫자로 변환

  let item = props.fruit.find(f => f.id === parseInt(paramId));
  const { imgUrl, title, content, price } = item;
  return (
    <div className="container">
      <div className="row">
        <div className="col-md-6">
         <img src={'/' + imgUrl} width="100%" alt={title} />
        </div>
        <div className="col-md-6">
          <h5 className="pt-5">{title}</h5>
          <p>{content}</p>
          <p>{price}</p>
          <button className="btn btn-danger">주문하기</button> 
        </div>
      </div>
    </div>
  )
}
export default Detail;
{%endraw%}
```

브라우저에서 확인

title2만들기 src폴더 > components >Title2.js만들기

```js
import React from "react";
const Title2 = () => {
  let csst1 = {
    marginTop: "70px",
  };
  return (
    <>
      <h3 style={csst1}>채소.야채 TOP</h3> 
      <p>청정지역, 황토밭에서 자란 건강식품</p> 
    </>
  );
};
export default Title2;
```

App.js
3개 상품 아래 `<div className="container"></div>` 아래 Product 위에 상품 9개 밑에 배치
`import Title2 from './components/Title2'` import 여부 확인
```js{%raw%}
<div className="container">
  <div className="row">
    <div style={{ textAlign: "center" }}> 
      <Title2 />
    </div>
  </div>
</div>{%endraw%}
```

+3개 상품 더보기 버튼만들기

App.js의 `<Title2 />` 아래 

```js
<Button variant="outline-success"> 
  + 3개 상품 더 보기 
</Button>
{' '}  
```

9개상품 밑에 
veggie 야채,채소 카테리고리 만들어야 하니까 준비

1 야채 상품 3개 데이터 준비
src폴더 > db폴더 > veggie.js 만들기


```js
let veggie = [
  {
    id: 1,
    title: "당근",
    imgUrl: "img/veggie/veggie1.jpg",
    content: "국내산 햇당근 1kg",
    price: 11900,
  },
  {
    id: 2,
    title: "옥수수",
    imgUrl: "img/veggie/veggie2.jpg",
    content: "쫀득쫀득 찰옥수수 250g",
    price: 29000,
  },
  {
    id: 3,
    title: "감자",
    imgUrl: "img/veggie/veggie3.jpg",
    content: "강원도 두백산 수미 감자 33kg", price: 30000,
  },
];
export default veggie;
```

2 App.js에 배치
```js
import data2 from "./db/veggie";
```
```js
let [veggie, setVeggie] = useState(data2);
```
```js{%raw%}
<div className="container" style={{ marginTop: "30px" }}>
  <div className="row">
    {
      veggie.map((ele, i) => {
        return <ComVeggie veggie={veggie[i]} key={veggie[i].id} />; 
      }
    )
    }
  </div>
</div>{%endraw%}
```

2 src폴더 > components > ComVeggie.js 만들기

**src/components/ComVeggie.js**
```js{%raw%}
import React from "react";
const ComVeggie = (props) => {
  const { imgUrl, title, content, price } = props.veggie; console.log(props);
  return (
    <div className="col-md-4" style={{marginBottom:"50px"}}> 
      <img src={imgUrl} width="80%" alt=""/>
      <h5 style={{marginTop:"10px"}}>{title}</h5> 
      <span>{content}</span>
      <p>{price}</p>
    </div>
  );
};
export default ComVeggie;{%endraw%}
```
App.js 상단 
```js
import ComVeggie from "./components/ComVeggie";
```

footer만들기

**src/components/Detail.js**
```js
import React from "react";
const Footer = () => {
  let foo = {
  color: "#fff",
  backgroundColor: "#000",
  padding: "20px 0px",
  marginTop: "80px",
  };
  return (
    <>
      <p style={foo}>COPYRIGHT(C) 2025 과일농장, Inc. All Rights Reserved</p> 
    </>
  );
};
export default Footer;
```

App.js 상단 
```js
import Footer from './components/Footer'
```

App.js 하단
```js
<Footer/>
```

라우터 확인
네비 링크 걸기 -> 로고에 메인화면 , 상세페이지에 detail/1

App.js
```js
<Navbar.Brand onClick={()=>{ navigate('/')}}>과일농장</Navbar.Brand> 
<Nav className="me-auto">
  <Nav.Link onClick={()=>{ navigate('/')}}>홈으로</Nav.Link>
  <Nav.Link onClick={()=>{ navigate('/detail/1')}}>상세페이지</Nav.Link> 
  <Nav.Link onClick={() => { navigate('/cart') }}>장바구니</Nav.Link> 
  <Nav.Link onClick={() => { navigate('/about') }}>회사소개</Nav.Link> 
</Nav>
```

### 9. JSON 파일 생성 후 Git 서버에 업로드해두기
veggie2.json
```json
[
  {
    "id" : 4,
    "title" : "고추",
    "imgUrl" : "img/veggie/veggie4.jpg", "content" : "혈당조절 청양고추, 300g", "price" : 21000
  },
  {
    "id" : 5,
    "title" : "밤",
    "imgUrl" : "img/veggie/veggie5.jpg", "content" : "아산율림 햇 약단밤", "price" : 14500
  },
  {
    "id" : 6,
    "title" : "고구마",
    "imgUrl" : "img/veggie/veggie6.jpg", "content" : "늘해랑 꿀고구마 10kg", "price" : 19800
  }
]
```
veggie3.json
```json
[
  {
    "id" : 7,
    "title" : "열무",
    "imgUrl" : "img/veggie/veggie7.jpg",
    "content" : "어린열무 싱싱 국내산 수확 4kg", "price" : 15000
  },
  {
    "id" : 8,
    "title" : "무",
    "imgUrl" : "img/veggie/veggie8.jpg", "content" : "제주 세척 월동무",
    "price" : 21000
  },
  {
    "id" : 9,
    "title" : "오이",
    "imgUrl" : "img/veggie/veggie9.jpg", "content" : "경북상주 백다다기 흑침오이", "price" : 17800
}
]
```

git 에 올리기 본인 깃에 올려서 URL이 필요

https://dino-21.github.io/react_data/veggie2.json  
https://dino-21.github.io/react_data/veggie3.json

### 10. App.js에서 더보기버튼 누르면 상품을 3개씩 가져오기 (비동기통신 Axios)

```bash
npm install axios
```

App.js  상단에
```js
import axios from 'axios'
```

App.js 리턴위에 
```js
let [count, setCount] = useState(1);
```

+3개 더 보기 버튼 안에 onClick
버튼1번 클릭하면 3개 상품이 보이고
버튼2번 클릭하면 3개 상품이 또 보이고
버튼3번 클릭하면 alert창으로 더 이상 상품이 없다고 나옴
- 콘솔창에서 버튼을 누르면 데이터가 오는지 확인하면서 작업하기

`<Button variant="outline-success"> + 3개 상품 더 보기 </Button>{' '}`   이코드를 수정

```js
<Button variant="outline-success" 
        count = {count} 
        onClick={() => {
                  if(count==1){ 
                    axios.get('https://dino-21.github.io/react_data/veggie2.json')
                    .then(
                      (result)=>{ 
                        let copy10 =[...veggie, ...result.data];
                        setVeggie(copy10);
                        setCount(count + 1);
                      }
                    )
                  }else if(count==2){ 
                    axios.get('https://dino-21.github.io/react_data/veggie3.json')
                    .then(
                      (result)=>{ 
                        let copy11 =[...veggie, ...result.data];
                        setVeggie(copy11);
                        setCount(count + 1);
                      }
                    )   
                  }
                  if(count===3){
                    alert("더이상 상품이 없습니다.");  
                  }
                }
              }
> 
  + 3개 상품 더 보기 
</Button>
{' '}   
```

### 11. 상세페이지 하단 sub 탭 UI 만들기
**src/components/Detail.js**
```js
import { Nav } from 'react-bootstrap' 
import { useState } from 'react';
```

return 앞에
```js
let [tap, setTap] = useState(0);   
```

`return <div className="container"> 안에</div>` 추가코드 작성
```js{%raw%}
<Nav variant="tabs"  defaultActiveKey="link0" style={{marginTop:"50px"}}> 
  <Nav.Item>
    <Nav.Link  onClick={()=>{ setTap(0) }} eventKey="link0">버튼0</Nav.Link> 
  </Nav.Item>
  <Nav.Item>
    <Nav.Link onClick={()=>{ setTap(1) }} eventKey="link1">버튼1</Nav.Link> 
  </Nav.Item>
  <Nav.Item>
    <Nav.Link  onClick={()=>{ setTap(2) }} eventKey="link2">버튼2</Nav.Link> 
  </Nav.Item>
</Nav>
<TabContent tap={tap}/>{%endraw%}
```

`export default Detail;`  바로 위에 추가
```js
function TabContent({tap}){
  return [ <div>내용0</div>, <div>내용1</div>, <div>내용2</div> ][tap]
}
```

### 12 상세페이지 클릭시,  하단 sub 탭 UI 클릭 시 애니메이션(Transition) 넣기