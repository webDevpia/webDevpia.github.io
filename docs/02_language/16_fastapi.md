---
title: FastAPI
layout: default
parent: Language
nav_order: 16
permalink: /language/fastapi
has_children: false
# nav_exclude: true
# search_exclude: true
---
# FastAPI
{: .no_toc }

## Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
## FastAPI 소개

### 왜 FastAPI인가?

**탁월한 성능**
- ASGI 표준을 따르는 FastAPI는 비동기 방식으로 요청을 처리하여, 파이썬 웹 프레임워크 중에서도 단연 최상의 속도를 제공합니다.
- 빠른 응답 속도는 오늘날 수많은 사용자를 동시에 수용해야 하는 대규모 애플리케이션에 필수적인 요소입니다.

**개발자를 위한 직관적인 설계**
- FastAPI는 개발자가 더욱 효율적이고 생산적으로 작업할 수 있도록 설계되었습니다. 
- 직관적인 내부 API, Dependency Injection 기능, 일원화된 타입 힌트(type hint), 그리고 자동으로 생성되는 OpenAPI 문서는 개발 과정에서 오류를 최소화하고, 프로젝트의 속도를 비약적으로 높여줍니다.

**편리한 데이터 처리와 검증**
- FastAPI는 Pydantic과 완벽하게 통합되어, 데이터 검증과 직렬화, 파싱 과정을 안전하고 정밀하게 처리합니다. 
- 이로 인해 개발자는 더욱 효율적이고 신뢰할 수 있는 코드를 작성할 수 있으며, 복잡한 데이터 구조도 손쉽게 다룰 수 있습니다.

**비동기 처리의 무한한 가능성**
- FastAPI는 비동기 프로그래밍을 통해 동시에 다수의 작업을 처리하는 능력을 제공합니다.
- 특히, 데이터베이스와 외부 API와 같은 I/O 바운드 작업에서 빛을 발하며, 빠르고 반응성이 뛰어난 애플리케이션을 구축할 수 있습니다.

### 성능 비교

**BMT를 현실에 반영해 보기**
- 대부분의 Benchmark 성능 테스트는 다양한 현실 Application을 잘 반영하지 못함
- 대부분의 현실 Application은 초당 수천건의 Request를 요청하지 않음(많으면 초당 수십건 정도)
- DB와 연계된 웹 애플리케이션의 Response Time 대부분은 DB 수행 속도에 좌우됨
- DB 연계 웹 애플리케이션의 경우 비동기가 아닌 동기 방식으로 DB와 인터페이스 해야 한다면 FastAPI와 타 프레임워크 간의 성능 차이는 크지 않을 수 있음

**그럼에도 불구하고 FastAPI가 우수한 경우**
- DB를 사용하지 않고, 대량의 동시 접속 요청이 많은 시스템일 경우 FastAPI가 훨씬 뛰어난 성능
- DB 연계 시스템에서 비동기로 DB 인터페이스를 한다면, FastAPI는 훨씬 더 많은 동시 접속을 수용 가능
- I/O 기반 처리나, 타 API에 요청, 머신러닝/딥러닝 추론 요청 등을 FastAPI는 비동기로 처리하면서 더 많은 동시 접속 처리를 빠르게 수행 가능

### 개발 편의성 측면

**장점**
- 모던하고 직관적인 내부 API, Dependency Injection 기능, 일원화된 타입 힌트(type hint)
- 편리한 문서 자동화
- 내재화된 Pydantic 통합을 통한 편리한 검증 및 직렬화
- 범용 API 개발을 편리하게 지원

**단점**
- 아직 Community가 타 Python 웹 프레임워크 대비 많지 않음
- Pydantic과 너무 강하게 결합되어 검증 오류 발생 시 한글 등으로 Customization이 어려움

## 실습 환경 구축

### 가상환경 생성 및 라이브러리 설치

```bash
conda create --name fastapi
conda activate fastapi
pip install fastapi
```

### 동작 테스트

`welcome/main.py`
```py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    """
    루트 경로('/')에 대한 GET 요청을 처리하는 함수입니다.
    간단한 JSON 응답을 반환합니다.
    """
    return {"message": "Hello World"}
```
- Path는 domain 명을 제외하고 / 로 시작하는 URL 부분
- 만약 url이 https://example.com/items/foo 라면 path는 /items/foo
- Operation은 GET, POST, PUT/PATCH, DELETE 등의 HTTP 메소드

🧪 실행 방법

```bash
uvicorn Welcome.main:app --port=8081 --reload
```
uvicorn은 ASGI 서버로, FastAPI 애플리케이션을 실행.  
--reload 옵션은 코드 변경 시 자동으로 서버를 재시작  
브라우저에서 http://127.0.0.1:8081에 접속하면 {"message": "Hello World"}라는 응답을 확인할 수 있음.
http://127.0.0.1:8081/docs에 접속하면 Swagger UI를 통해 자동 생성된 API 문서를 확인할 수 있음.

### FastAPI와 클라이언트 간 동작 흐름 이해가기

![](./img/fastapi/fastapi001.png)

	**GET**은 데이터를 요청할 때,
	**POST**는 데이터를 생성할 때,
	**PUT**, **PATCH**는 데이터를 수정할 때,
	**DELETE**는 데이터를 삭제할 때,
	**HEAD**는 데이터의 존재 여부만 확인.


### Swagger UI를 이용한 동작 확인

api들을 브라우저 기반에서 편리하게 관리 및 문서화, 테스트 할 수 있는 기능을 제공  
http://127.0.0.1:8081/docs로 접속해서 결과 확인  

![](./img/fastapi/fastapi002.png)


## FastAPI Request

FastAPI는 Path Parameter, Query Parameter, Request Body, Form Fields, Header, Cookie, File 등의 다양한 Request 들을 다룰 수 있게 지원함.

![](./img/fastapi/fastapi003.png)

![](./img/fastapi/fastapi004.png)

![](./img/fastapi/fastapi005.png)


### Path 파라미터

`requests/main_path.py`

```py
from fastapi import FastAPI

app = FastAPI()

# http://localhost:8081/items/3
# decorator에 path값으로 들어오는 문자열중에 
# format string { }로 지정된 변수가 path parameter

@app.get("/items/{item_id}")
# 수행 함수 인자로 path parameter가 입력됨. 
# 함수 인자의 타입을 지정하여 path parameter 타입 지정.
async def read_item(item_id: int):
    return {"item_id": item_id} 

# Path parameter값과 특정 지정 Path가 충돌되지 않도록 endpoint 작성 코드 위치에 주의 
# 아래쪽에 있을 경우 오류발생  /items/all로 요청시  /items/3으로인식됨
@app.get("/items/all")
# 수행 함수 인자로 path parameter가 입력됨. 함수 인자의 타입을 지정하여 path parameter 타입 지정.  
async def read_all_items():
    return {"message": "all items"}
```

```bash
uvicorn Requests.main_path:app --port=8081 --reload
```

### Query 파라미터

`requests/main_query.py`

```py
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# http://localhost:8081/items?skip=0&limit=2
@app.get("/items")
# 함수에 개별 인자값이 들어가 있는 경우 path parameter가 아닌 모든 인자는 query parameter
# query parameter의 타입과 default값을 함수인자로 설정할 수 있음.
# fake_items_db에서 데이터 슬라이딩해서 리턴
async def read_item(skip: int = 0, limit: int = 2):
    return fake_items_db[skip: skip + limit]

@app.get("/items_nd/")
# 함수 인자값에 default 값이 주어지지 않으면 반드시 query parameter에 해당 인자가 주어져야 함.  
async def read_item_nd(skip: int, limit: int):
    return fake_items_db[skip : skip + limit]

@app.get("/items_op/")
# 함수 인자값에 default 값이 주어지지 않으면 None으로 설정. 
# limit: Optional[int] = None 또는 limit: int | None = None 과 같이 Type Hint 부여  
async def read_item_op(skip: int, limit: int = None ):
    # return fake_items_db[skip : skip + limit]
    if limit:
        return fake_items_db[skip : skip + limit]
    else:
        return {"limit is not provided"}
    
# Path와 Query Parameter를 함께 사용.
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}   
```

```bash
uvicorn Requests.main_query:app --port=8081 --reload
```

### Request Body

`requests/main_rbody.py`

```py
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, Annotated

app = FastAPI()

#Pydantic Model 클래스는 반드시 BaseModel을 상속받아 생성. 
class Item(BaseModel):
    name: str
    description: str | None = None
    #description: Optional[str] = None
    price: float
    tax: float | None = None
    #tax: Optional[float] = None


#수행 함수의 인자로 Pydantic model이 입력되면 Json 형태의 Request Body 처리
@app.post("/items")
async def create_item(item: Item):
    print("###### item type:", type(item))
    print("###### item:", item)
    return item


# Request Body의 Pydantic model 값을 Access하여 로직 처리
@app.post("/items_tax/")
async def create_item_tax(item: Item):
    item_dict = item.model_dump()
    print("#### item_dict:", item_dict)
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict   

# Path, Query, Request Body 모두 함께 적용. 
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    
    if q:
        result.update({"q": q})
    print("#### result:", result)
    return result

class User(BaseModel):
    username: str
    full_name: str | None = None
    #full_name: Optional[str] = None


# 여러개의 request body parameter 처리. 
# json 데이터의 이름값과 수행함수의 인자명이 같아야 함.  
@app.put("/items_mt/{item_id}")
async def update_item_mt(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    print("results:", results)
    return results
```

```bash
uvicorn Requests.main_rbody:app --port=8081 --reload
```

```json
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

```json
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

javascript기반 Requests Body 적용. 

`static/rbody.html`

```py
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Display JSON Response</title>
</head>
<body>
    <h1>JSON Response Data</h1>
    <pre id="jsonOutput"></pre> <!-- A <pre> tag to display JSON data -->
    <script>
        // The URL to which the request is sent
        const url = 'http://localhost:8081/items';

        // The data you want to send in JSON format
        const data = {
            name: "Foo",
            description: "An optional description",
            price: 45.2,
            tax: 3.5
        };

        // Options for the fetch request
        //const options = ;

        // Making the request
        fetch(url, {
        method: 'POST', // The HTTP method to use
        headers: {
            'Content-Type': 'application/json' // The type of content to send
        },
        body: JSON.stringify(data) // The actual data to send, in JSON string format
        })
        .then(response => response.json()) // Parsing the response as JSON
        .then(data => {
            console.log('Success:', data); // Handling the response data
            const outputElement = document.getElementById('jsonOutput');
            // Set the text content of the <pre> element to the formatted JSON string
            outputElement.textContent = JSON.stringify(data, null, 2);
        })
        .catch((error) => {
            console.error('Error:', error); // Handling any errors
        });

    </script>
</body>
</html>
```

`Requests/main_rbody_js.py`

```py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=-1,  # Only for the sake of the example. Remove this in your own project.
)

#Pydantic Model 클래스는 반드시 BaseModel을 상속받아 생성. 
class Item(BaseModel):
    name: str
    #description: str | None = None
    description: Optional[str] = None
    price: float
    #tax: float | None = None
    tax: Optional[float] = None


#수행 함수의 인자로 Pydantic model이 입력되면 Json 형태의 Request Body 처리
@app.post("/items/")
async def create_item(item: Item):
    print("###### item")
    return item

# Request Body의 Pydantic model 값을 Access하여 로직 처리
@app.post("/items_tax/")
async def create_item_tax(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Path, Query, Request Body 모두 함께 적용. 
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, q: str | None = None):
#     result = {"item_id": item_id, **item.dict()}
#     if q:
#         result.update({"q": q})
#     return result

class User(BaseModel):
    username: str
    #full_name: str | None = None
    full_name: Optional[str] = None

# 여러개의 request body parameter 처리. 
# json 데이터의 이름값과 수행함수의 인자명이 같아야 함.  
@app.put("/items_mt/{item_id}")
async def update_item_mt(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

```

```bash
uvicorn Requests.main_rbody_js:app --port=8081 --reload
```


### Form

HTML Form Element를 이용해서 Post로 Request Body를 전송하는 경우 FastAPI에서 Form()으로 처리  
개별 input값 별로 Form()을 이용해서 처리
여러 개의 input 값들을 한번에 처리할 수도 있지만, 이를 위해서는 Form()과 Pydantic을 classmethod로 결합해야 함  

 ![](./img/fastapi/fastapi006.png)

 ![](./img/fastapi/fastapi007.png)


`Requests/main_form.py`

```py
from pydantic import BaseModel
from typing import Optional, Annotated

from fastapi import FastAPI, Form

app = FastAPI()

# 개별 Form data 값을 Form()에서 처리하여 수행함수 적용. 
# Form()은 form data값이 반드시 입력되어야 함. Form(None)과 Annotated[str, Form()] = None은 Optional
@app.post("/login")
async def login(username: str = Form(),
                email: str = Form(),
                country: Annotated[str, Form()] = None):
    return {"username": username, 
            "email": email,
            "country": country}

# ellipsis(...) 을 사용하면 form data값이 반드시 입력되어야 함. 
@app.post("/login_f/")
async def login(username: str = Form(...), 
                email: str = Form(...),
                country: Annotated[str, Form()] = None):
    return {"username": username, 
            "email": email, 
            "country": country}

# path, query parameter와 함께
@app.post("/login_pq/{login_gubun}")
async def login(login_gubun: int, q: str | None = None, 
                username: str = Form(), 
                email: str = Form(),
                country: Annotated[str, Form()] = None):
    return {"login_gubun": login_gubun,
            "q": q,
            "username": username, 
            "email": email, 
            "country": country}

#Pydantic Model 클래스는 반드시 BaseModel을 상속받아 생성. 
class Item(BaseModel):
    name: str
    description: str | None = None
    #description: Optional[str] = None
    price: float
    tax: float | None = None
    #tax: Optional[float] = None

# json request body용 end point
@app.post("/items_json/")
async def create_item_json(item: Item):
    return item

# form tag용 end point
@app.post("/items_form/")
async def create_item_json(name: str = Form(),
                           description: Annotated[str, Form()] = None,
                           price: str = Form(),
                           tax: Annotated[int, Form()] = None
                           ):
    return {"name": name, "description": description, "price": price, "tax": tax}
```

```bash
uvicorn Requests.main_rbody_js:app --port=8081 --reload
```

### Request 객체

FastAPI의 Request 객체는 HTTP Request에 대한 대부분의 정보를 다 가지고 있음. 

 ![](./img/fastapi/fastapi008.png)

 ![](./img/fastapi/fastapi009.png)

`Requests/main_request.py`

 ```py
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/items")
async def read_item(request: Request):
    client_host = request.client.host
    headers = request.headers
    query_params = request.query_params
    url = request.url
    path_params = request.path_params
    http_method = request.method
    
    return {
            "client_host": client_host,
            "headers": headers,
            "query_params": query_params,
            "path_params": path_params,
            "url": str(url),
            "http_method":  http_method
        }


@app.get("/items/{item_group}")
async def read_item_p(request: Request, item_group: str):
    client_host = request.client.host
    headers = request.headers 
    query_params = request.query_params
    url = request.url
    path_params = request.path_params
    http_method = request.method

    return {
        "client_host": client_host,
        "headers": headers,
        "query_params": query_params,
        "path_params": path_params,
        "url": str(url),
        "http_method":  http_method
    }


@app.post("/items_json/")
async def create_item_json(request: Request):
    data =  await request.json()  # Parse JSON body
    print("received_data:", data)
    return {"received_data": data}

@app.post("/items_form/")
async def create_item_form(request: Request):
    data = await request.form() # Parse Form body
    print("received_data:", data)
    return {"received_data": data}
 ```

```bash
uvicorn Requests.main_request:app --port=8081 --reload
```

테스트는 Thunder Client로 진행

 ![](./img/fastapi/fastapi010.png)

 ![](./img/fastapi/fastapi011.png)


## FastAPI Response
http Response는 clinet Request에 따른 serve에서 내려 보내는 메시지   
요청 Request의 처리 상태, 여러 메타정보, 그리고 Content 데이터를 담고 있음

 ![](./img/fastapi/fastapi012.png)

 FastAPI Response Class 유형

 ![](./img/fastapi/fastapi013.png)

`Responses/main_response.py`

```py
from fastapi import FastAPI, Form, status
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    RedirectResponse
)

from pydantic import BaseModel

app = FastAPI()

#response_class는 default가 JSONResponse. response_class가 HTMLResponse일 경우 아래 코드는?
@app.get("/resp_json/{item_id}", response_class=JSONResponse)
async def response_json(item_id: int, q: str | None = None):
    return JSONResponse(content={"message": "Hello World", 
                                 "item_id": item_id,
                                 "q": q}, status_code=status.HTTP_200_OK)


# HTML Response
@app.get("/resp_html/{item_id}", response_class=HTMLResponse)
async def response_html(item_id: int, item_name: str | None = None):
    html_str = f'''
    <html>
    <body>
        <h2>HTML Response</h2>
        <p>item_id: {item_id}</p>
        <p>item_name: {item_name}</p>
    </body>
    </html>
    '''
    return HTMLResponse(html_str, status_code=status.HTTP_200_OK)


# Redirect(Get -> Get)
@app.get("/redirect")
async def redirect_only(comment: str | None = None):
    print(f"redirect {comment}")
    
    return RedirectResponse(url=f"/resp_html/3?item_name={comment}")

# Redirect(Post -> Get)
@app.post("/create_redirect")
async def create_item(item_id: int = Form(), item_name: str = Form()):
    print(f"item_id: {item_id} item name: {item_name}")

    return RedirectResponse(url=f"/resp_html/{item_id}?item_name={item_name}"
                            , status_code=status.HTTP_302_FOUND)


class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None

# Pydantic model for response data
class ItemResp(BaseModel):
    name: str
    description: str
    price_with_tax: float

# reponse_model
@app.post("/create_item/", response_model=ItemResp
          , status_code=status.HTTP_201_CREATED)
async def create_item_model(item: Item):
    item_dict = item.model_dump
    if item.tax:
        price_with_tax = item.price + item.tax
    else:
        price_with_tax = item.price
    
    item_resp = ItemResp(
        name=item.name,
        description=item.description,
        price_with_tax=price_with_tax
    )
    # 반드시 response_model로 정의된 pydantic model을 반환. 
    return item_resp
```


```bash
uvicorn Responses.main_response:app --port=8081 --reload
```

```json
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

## 템플릿 엔진과 정적 파일(Static file) 다루기

### 템플릿 엔진

html 등의 태그 기반의 마크업등은 다양한 표현 방식을 제공하면서 길고 복잡한 형태의 파일로 구성.  
Template 엔진은 표현을 위한 Frontend, 로직과 데이터 핸들링을 위한 Backend 처리를 쉽게 분리할 수 있게 해줌.  
유연한 동적 Content 생성, 개발팀과 Designer의 역활을 분리, 소스코드 모듈화 및 재사용성 증대등의 다양한 장점을 지원

![](./img/fastapi/fastapi014.png)

[jinja 문법 기본](17_jinja-template-guide.md)

`Templates/main.py`

```py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# jinja2 Template 생성. 인자로 directory 입력
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str
    price: float

# response_class=HTMLResponse를 생략하면 application/json으로 Swagger UI에서 인식(별 문제는 없음)
@app.get("/items/{id}", response_class=HTMLResponse)
# template engine을 사용할 경우 반드시 Request 객체가 인자로 입력되어야 함. 
async def read_item(request: Request, id: str, q: str | None = None):
    # 내부에서 pydantic 객체 생성. 
    item = Item(name="test_item", price=10)
    # pydantic model값을 dict 변환. 
    item_dict = item.model_dump()

    return templates.TemplateResponse(
        request=request,
        name="item.html",
        context={"id": id, "q_str": q, "item": item, "item_dict": item_dict}
    )
    
    # FastAPI 0.108 이하 버전에서는 아래와 같이 TemplateResponse() 인자 호출
    # return templates.TemplateResponse(name="item.html",
    #                                   {"request": request
    #                                    , "id": id, "q_str": q, "item": item, "item_dict": item_dict})


@app.get("/item_gubun")
async def read_item_by_gubun(request: Request, gubun: str):
    item = Item(name="test_item_02", price=4.0)
    
    return templates.TemplateResponse(
        request=request, 
        name="item_gubun.html", 
        context={"gubun": gubun, "item": item}
    )



@app.get("/all_items", response_class=HTMLResponse)
async def read_all_items(request: Request):
    all_items = [Item(name="test_item_" +str(i), price=i) for i in range(5) ]
    print("all_items:", all_items)
    return templates.TemplateResponse(
        request=request, 
        name="item_all.html", 
        context={"all_items": all_items}
    )


# safe read
@app.get("/read_safe", response_class=HTMLResponse)
async def read_safe(request: Request):
    html_str = '''
    <ul>
    <li>튼튼</li>
    <li>저렴</li>
    </ul>
    '''
    return templates.TemplateResponse(
        request=request, 
        name="read_safe.html", 
        context={"html_str": html_str}
    )

```

`Templates/templates/item.html`

```html
{% raw %}<html>
<head>
    <title>Item Details</title>
</head>
<body>
    <h1>Item id: {{ id }}</h1>
    <h1>query: {{ q_str}} </h1>
    <h3>{{item}}</h3>
    <h5>item name: {{item.name}}, item price: {{item.price}}</h5>
    <p>item_dict[name]: {{item_dict['name']}} </p>
</body>
</html>{% endraw %}
```

`Templates/templates/item_gubun.html`

```html
{% raw %}<html>
<head>
    <title>Item Details</title>
</head>
<body>
    {% if gubun == "admin" %}
    <p>이것은 어드민용 item입니다.</p>
    {% else %}
    <p> 이것은 일반용 item 입니다. </p>
    {% endif %}
    <h3>{{item}}</h3>
</body>
</html>{% endraw %}
```

`Templates/templates/item_all.html`

```html
{% raw %}<html>
<head>
    <title>Item Details</title>
</head>
<body>
    {% for item in all_items %} 
    <h3>item name:{{ item.name }} item price: {{ item.price }}</h3>
    {% endfor %}
</body>
</html>{% endraw %}
```

`Templates/templates/read_safe.html`

```html
{% raw %}<html>
<body>
    <h1> 우리 상품은 </h1>
    {{ html_str | safe }}
</body>
</html>{% endraw %}
```
### 정적 파일(Static file) 다루기
결과값을 동적으로 반환하는 endpoint path와 달리 css, javascript, image, 정적 html 파일들은 그 내용이 변경되지 않는 정적 파일임  
FastAPI는 이들 Static File들은 Endpoint로 별도로 관리하지 않으며 정적 파일들을 위한 별도의 ASGI서버를 생성하여 관리하며 이를 위하여 StaticFiles클래스를 제공  

`Templates/main_static.py`

```py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# /static은 url path, StaticFiles의 directory는 directory명, name은 url_for등에서 참조하는 이름 
app.mount("/static", StaticFiles(directory="static"), name="static")

# jinja2 Template 생성. 인자로 directory 입력
templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str, q: str | None = None):
    html_name = "item_static.html"
    #html_name = "item_urlfor.html"
    return templates.TemplateResponse(
        request=request, name=html_name, context={"id": id, "q_str": q}
    )
```

`Templates/templates/read_static.html`

```html
{% raw %}<html>
<head>
    <title>Item Details</title>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <h1>Item id: {{ id }}</h1>
    <h3><a href="/static/link_tp.html">another link</a></h3>
</body>
</html>{% endraw %}
```

`Templates/templates/read_urlfor.html`

```html
{% raw %}<html>
<head>
    <title>Item Details</title>
    <link rel="stylesheet" href="{{ url_for('static', path='css/styles.css') }}">
</head>
<body>
    <h1>Item id: {{ id }}</h1>
    <h3><a href="{{ url_for('static', path='link_tp.html') }}">another link</a></h3>
</body>
</html>{% endraw %}
```

`Templates/static/css/styles.css`

```css
h1 {
    color: green;
}
```

`Templates/static/link_tp.html`

```html
<html>
<head>
    <title>link tp</title>
    <link rel="stylesheet" href="/static/css/styles.css">

</head>
<body>
    <h1>Another Result</h1>
</body>
</html>
```

## FastAPI의 APIRouter

`Router/main_org.py`

```py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/item")
async def create_item(item: Item):
    return item

@app.put("/item/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

@app.get("/users/")
async def read_users():
    return [{"username": "Rickie"}, {"username": "Martin"}]


@app.get("/users/me")
async def read_user_me():
    return {"username": "currentuser"}


@app.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}
```

`Router/main.py`

```py
from fastapi import FastAPI
from routes import item, user

app = FastAPI()

app.include_router(item.router)
app.include_router(user.router)
```

`Router/routes/item.py'

```py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/item", tags=["item"])

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@router.get("/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@router.post("/")
async def create_item(item: Item):
    return item

@router.put("/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}
```

`Router/routes/user.py`

```py
from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def read_users():
    return [{"username": "Rickie"}, {"username": "Martin"}]

@router.get("/me")
async def read_user_me():
    return {"username": "currentuser"}

@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
```

## Pydantic

**다양하고 빠른 Validation 수행**  
데이터 타입 검증 및 데이터 값에 대한 검증 수행    
정규식 지원 및 다양한 내장 검증 로직 제공  
Core 검증 로직은 Rust로 제작되어 가장 빠른 파이썬 데이터 검증 라이브러리  

**Serialization 지원**  
쉽게 Json이나 Dict 형태로 Serialization 수행  

**다양한 Echo 시스템에서 활용되며 문서화 시스템에서 지원**  
FastAPI, HuggingFace, LangChain

`Pydantic/pydantic_01.py`
```py
from pydantic import BaseModel, ValidationError
from typing import List, Optional
import json

# Pydantic Model
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None # Optional[int] = None

# 일반 클래스 선언
class UserClass:
    def __init__(self, id: int, name: str, email: str, age: int):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

    def get_info(self):
        return f"id: {self.id}, name: {self.name}"
    
    def __str__(self):
        return f"id: {self.id}, name: {self.name}, email: {self.email}, age: {self.age}"

userobj = UserClass(10, 'test_name', 'tname@example.com', 40)
print("userobj:", userobj, userobj.id)

# Pydantic Model 객체화. 
#User(10, 'test_name', 'tname@example.com', 40) 하지 않도록 유의
user = User(id=10, name="test_name", email="tname@example.com", age=40)
print("user:", user, user.id)

# dict keyword argument(kwargs)로 Pydantic Model 객체화
user_from_dict = User(**{"id": 10, "name": "test_name", "email": "tname@example.com", "age": 40})
print("user_from_dict:", user_from_dict, user_from_dict.id)

# json 문자열 기반 Pydantic Model 객체화. 
json_string = '{"id": 10, "name": "test_name", "email": "tname@example.com", "age": 40}'
json_dict = json.loads(json_string)
#print("json_dict type:", type(json_dict))
user_from_json = User(**json_dict)
print("user_from_json:", user_from_json, user_from_json.id)

# Pydantic Model의 상속
class AdvancedUser(User):
    advanced_level: int

#AdvancedUser(10, 'test_name', 'tname@example.com', 40, 10) 하지 않도록 유의
adv_user = AdvancedUser(id=10, name="test_name", email="tname@example.com", age=40, advanced_level=9)
print("adv_user:", adv_user)


# 내포된(Nested 된 Json) 데이터 기반 Pydantic Model 생성. 
class Address(BaseModel):
    street: str
    city: str

class UserNested(BaseModel):
    name: str
    age: int
    address: Address

# 내포된 Json 문자열에서 생성. 
json_string_nested = '{"name": "John Doe", "age": 30, "address": {"street": "123 Main St", "city": "Anytown"}}'
json_dict_nested = json.loads(json_string_nested)

user_nested_01 = UserNested(**json_dict_nested)
print("user_nested_01:", user_nested_01, user_nested_01.address, user_nested_01.address.city)

# 인자로 전달 시 Nested 된 값을 dict 형태로 전달하여 생성.
user_nested_02 = UserNested(
    name="test_name", age=40, address = {"street": "123 Main St", "city": "Anytown"}
)
print("user_nested_02:", user_nested_02, user_nested_02.address, user_nested_02.address.city)

# python 기반으로 pydantic serialization
user_dump_01 = user.model_dump()
print(user_dump_01, type(user_dump_01))

# json 문자열 기반으로 pydantic serialization
user_dump_02 = user.model_dump_json()
print(user_dump_02, type(user_dump_02))

```


`Pydantic/pydantic_02.py`
```py
from pydantic import BaseModel, ValidationError, ConfigDict, Field, Strict
from typing import List, Annotated

class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    # 문자열->숫자값 자동 파싱을 허용하지 않을 경우 Strict 모드로 설정. 
    #model_config = ConfigDict(strict=True)

    id: int
    name: str
    email: str
    addresses: List[Address]
    age: int | None = None # Optional[int] = None
    #개별 속성에 Strict 모드 설정 시 Field나 Annotated 이용. None 적용 시 Optional
    #age: int = Field(None, strict=True)
    #age: Annotated[int, Strict()] = None

#Pydantic Model 객체화 시 자동으로 검증 수행 수행하고, 검증 오류 시 ValidationError raise 
try:
    user = User(
        id=123,
        name="John Doe",
        email="john.doe@example.com",
        addresses=[{"street": "123 Main St", "city": "Hometown", "country": "USA"}],
        age="29" # 문자열 값을 자동으로 int 로 파싱함.
    )
    print(user)
except ValidationError as e:
    print("validation error happened")
    print(e)

```

`Pydantic/pydantic_03.py`
```py
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

class User(BaseModel):
    username: str = Field(..., description="The user's username", example="john_doe")
    email: str = Field(..., description="The user's email address", example="john.doe@example.com")
    password: str = Field(..., min_length=8, description="The user's password")
    age: Optional[int] = Field(None, ge=0, le=120, description="The user's age, must be between 0 and 120", example=30)
    is_active: bool = Field(default=True, description="Is the user currently active?", example=True)

# Example usage
try:
    user = User(username="john_doe", email="john.doe@example.com", password="Secret123")
    print(user)
except ValidationError as e:
    print(e.json())

'''
https://docs.pydantic.dev/2.8/concepts/fields/

gt - greater than
lt - less than
ge - greater than or equal to
le - less than or equal to
multiple_of - a multiple of the given number
allow_inf_nan - allow 'inf', '-inf', 'nan' values
'''

class Foo(BaseModel):
    positive: int = Field(gt=0)
    non_negative: int = Field(ge=0)
    negative: int = Field(lt=0)
    non_positive: int = Field(le=0)
    even: int = Field(multiple_of=2)
    love_for_pydantic: float = Field(allow_inf_nan=True)


foo = Foo(
    positive=1,
    non_negative=0,
    negative=-1,
    non_positive=0,
    even=2,
    love_for_pydantic=float('inf'),
)
print(foo)

'''
https://docs.pydantic.dev/2.8/concepts/fields/

min_length: 문자열 최소 길이
max_length: 문자열 최대 길이
pattern: 문자열 정규 표현식
'''

class Foo(BaseModel):
    short: str = Field(min_length=3)
    long: str = Field(max_length=10)
    regex: str = Field(pattern=r'^\d*$')  


foo = Foo(short='foo', long='foobarbaz', regex='123')
print(foo)
#> short='foo' long='foobarbaz' regex='123'
'''
max_digits: Decimal 최대 숫자수. 소수점 앞에 0만 있는 경우나, 소수점값의 맨 마지막 0는 포함하지 않음. 
decimal_places: 소수점 자리수 . 소수점값의 맨 마지막 0는 포함하지 않음
'''

from decimal import Decimal

class Foo(BaseModel):
    precise: Decimal = Field(max_digits=5, decimal_places=2)


foo = Foo(precise=Decimal('123.45'))
print(foo)
#> precise=Decimal('123.45')
```

`Pydantic/pydantic_04.py`
```py
from pydantic import BaseModel, EmailStr, Field

'''
EmailStr: Validate Email Address
https://docs.pydantic.dev/2.8/api/networks/#pydantic.networks.EmailStr
'''

class UserEmail(BaseModel):
    email: EmailStr # 문자열 Email 검증. 
    #email: EmailStr = Field(..., max_length=40) #Field와 함께 사용.
    #email: EmailStr = Field(None, max_length=40, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$') 

try:
    user_email = UserEmail(email="user@examples.com")
    print(user_email)
except ValueError as e:
    print(e)

'''
https://docs.pydantic.dev/2.8/api/networks/

1. HttpUrl: http 또는 https만 허용. TLD(top-level domain)와 host명 필요. 최대 크기 2083
- valid: https://www.example.com, http://www.example.com, http://example.com
- invalid: ftp://example.com

2. AnyUrl: http, https, ftp 등 어떤 프로토콜도 다 허용. host 명 필요하며 TLD 필요 없음. 
- valid: http://www.example.com ftp://example.com, ksp://example.com ftp://example
- invalid: ftp//example.com

3. AnyHttpUrl: http 또는 https만 허용, TLD는 필요하지 않고 host명은 필요.
- valid: https://www.example.com, http://www.example.com, http://example.com
- invalid: ftp://example.com

4. FileUrl: 파일 프로토콜만 허용. host 명이 필요하지 않음. 
- valid: file:///path/to/file.txt
'''
from pydantic import HttpUrl, AnyUrl, AnyHttpUrl, FileUrl

class UserResource(BaseModel):
    http_url: HttpUrl
    any_url: AnyUrl
    any_http_url: AnyHttpUrl
    file_url: FileUrl
    
try:
    user_resource = UserResource(
        http_url="https://www.example.com",
        any_url="ftp://example.com",
        any_http_url="http://www.example.com",
        file_url="file:///path/to/file.txt"
    )

    print(user_resource, user_resource.http_url)
except ValueError as e:
    print(f"Validation error: {e}")

# '''
# IP Addresses
# https://docs.pydantic.dev/2.8/api/networks/

# IPvAnyAddress:  IPv4Address or an IPv6Address.

# * valid: 192.168.1.1, 192.168.56.101
# * invalid: 999.999.999.999

# IPvAnyNetwork: IPv4Network or an IPv6Network.
# * valid: 192.168.1.0/24
# * invalid: 192.168.1.0/33

# IPvAnyInterface: IPv4Interface or an IPv6Interface.
# * valid: 192.168.1.1/24
# * invalid: 192.168.1.1/33

# '''
from pydantic import IPvAnyAddress, IPvAnyNetwork, IPvAnyInterface

class Device(BaseModel):
    ip_address: IPvAnyAddress
    network: IPvAnyNetwork
    interface: IPvAnyInterface

# Example usage
try:
    device = Device(
        ip_address="192.168.1.1",
        network="192.168.1.0/24",
        interface="192.168.1.0/24")
    print(device)
except ValueError as e:
    print(e)

# pip install pydantic-extra-types pycountry
# https://docs.pydantic.dev/latest/api/pydantic_extra_types_color/
from pydantic_extra_types.country import CountryAlpha3

class Product(BaseModel):
    made_in: CountryAlpha3

product = Product(made_in="USA")
print(product)
#> made_in='USA'

```

`Pydantic/pydantic_05.py`
```py
from pydantic import BaseModel,  ValidationError, field_validator, model_validator
from typing import Optional


class User(BaseModel):
    username: str
    password: str
    confirm_password: str
    
    @field_validator('username')
    def username_must_not_be_empty(cls, value: str):
        if not value.strip():
            raise ValueError("Username must not be empty")
        return value

    @field_validator('password')
    def password_must_be_strong(cls, value: str):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in value):
            raise ValueError('Password must contain at least one letter')
        return value
    
    @model_validator(mode='after')
    def check_passwords_match(cls, values):
        password = values.password
        confirm_password = values.confirm_password
        if password != confirm_password:
            raise ValueError("Password do not match")
        return values
 
    
# 검증 테스트    
try:
    user = User(username="john_doe", password="Secret123", confirm_password="Secret123")
    print(user)
except ValidationError as e:
    print(e)
```

``Pydantic/main.py``

```py
from fastapi import FastAPI, Path, Query, Form, Depends
from pydantic import BaseModel, Field, model_validator
from typing import Annotated
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: str = Field(None, max_length=500)
    price: float = Field(..., ge=0)
    tax: float = None

    @model_validator(mode='after')
    def tax_must_be_less_than_price(cls, values):
        price = values.price
        tax = values.tax
        if tax > price:
            raise ValueError("Tax must be less then price")

        return values
    
@app.put("/items/{item_id}")
async def update_item(item_id: int, q: str, item: Item=None):
#async def update_item(item_id: int = Path(...), q: str = Query(...), item: Item=None):
    return {"item_id": item_id, "q": q, "item": item}

# Path, Query, Request Body(json)
@app.put("/items_json/{item_id}")
async def update_item_json(
    item_id: int = Path(..., gt=0),
    q1: str = Query(None, max_length=50),
    #q1: Annotated[str, Query(max_length=50)] = None
    q2: str = Query(None, min_length=3),
    #q2: Annotated[str, Query(min_length=50)] = None
    item: Item = None
):
    return {"item_id": item_id, "q1": q1, "q2": q2, "item": item}

# Path, Query, Form
@app.post("/items_form/{item_id}")
async def update_item_form(
    item_id: int = Path(..., gt=0, title="The ID of the item to get"),
    q: str = Query(None, max_length=50),
    name: str = Form(..., min_length=2, max_length=50),
    description: Annotated[str, Form(max_length=500)] = None,
    #description: str = Form(None, max_length=500),
    price: float = Form(..., ge=0), 
    tax: Annotated[float, Form()] = None
    #tax: float = Form(None)
):
    return {"item_id": item_id, "q": q, "name": name, 
            "description": description, "price": price, "tax": tax}

# Path, Query, Form을 @model_validator 적용. 
@app.post("/items_form_01/{item_id}")
async def update_item_form_01(
    item_id: int = Path(..., gt=0, title="The ID of the item to get"),
    q: str = Query(None, max_length=50),
    name: str = Form(..., min_length=2, max_length=50),
    description: Annotated[str, Form(max_length=500)] = None,
    #description: str = Form(None, max_length=500),
    price: float = Form(..., ge=0), 
    tax: Annotated[float, Form()] = None
    #tax: float = Form(None)
):
    try: 
        item = Item(name=name, description=description, price=price, tax=tax)
        return item
    except ValidationError as e:
        raise RequestValidationError(e.errors())
   
def parse_user_form(
    name: str = Form(..., min_length=2, max_length=50),
    description: Annotated[str, Form(max_length=500)] = None,
    price: float = Form(..., ge=0),
    tax: Annotated[float, Form()] = None, 
) -> Item:
    try: 
        item = Item(
            name = name,
            description = description,
            price = price, 
            tax = tax
        )

        return item
    except ValidationError as e:
        raise RequestValidationError(e.errors()) 

@app.post("/items_form_02/{item_id}")
async def update_item_form_02(
    item_id: int = Path(..., gt=0, title="The ID of the item to get"),
    q: str = Query(None, max_length=50),
    item: Item = Depends(parse_user_form)
):
    return {"item_id": item_id, "q": q, "item": item}
```

``Pydantic/dataclass.py``

```py
from pydantic import BaseModel, ValidationError
from typing import List, Optional
import json

# Pydantic Model
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None 

user = User(id=10, name="test_name", 
            email="tname@example.com", 
            age=40)

# 일반 클래스 선언
class UserClass:
    def __init__(self, id: int, name: str, 
                email: str, age: int):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

    def get_info(self):
        return f"id: {self.id}, name: {self.name}"
    
    def __str__(self):
        return f"id: {self.id}, name: {self.name}, email: {self.email}, age: {self.age}"

userobj = UserClass(10, 'test_name', 
                    'tname@example.com', 40)

print("userobj:", userobj, userobj.id)

# Pydantic Model 객체화. 
# User(10, 'test_name', 'tname@example.com', 40) 하지 않도록 유의
user = User(id=10, name="test_name", email="tname@example.com", age=40)
print("user:", user, user.id)

# dict keyword argument(kwargs)로 Pydantic Model 객체화
user_from_dict = User(**{"id": 10, "name": "test_name", "email": "tname@example.com", "age": 40})
print("user_from_dict:", user_from_dict, user_from_dict.id)

# json 문자열 기반 Pydantic Model 객체화. 
json_string = '{"id": 10, "name": "test_name", "email": "tname@example.com", "age": 40}'
json_dict = json.loads(json_string)
#print("json_dict type:", type(json_dict))
user_from_json = User(**json_dict)
print("user_from_json:", user_from_json, user_from_json.id)

# Pydantic Model의 상속
class AdvancedUser(User):
    advanced_level: int

#AdvancedUser(10, 'test_name', 'tname@example.com', 40, 10) 하지 않도록 유의
adv_user = AdvancedUser(id=10, name="test_name", email="tname@example.com", age=40, advanced_level=9)
print("adv_user:", adv_user)


# 내포된(Nested 된 Json) 데이터 기반 Pydantic Model 생성. 
class Address(BaseModel):
    street: str
    city: str

class UserNested(BaseModel):
    name: str
    age: int
    address: Address

# 내포된 Json 문자열에서 생성. 
json_string_nested = '{"name": "John Doe", "age": 30, "address": {"street": "123 Main St", "city": "Anytown"}}'
json_dict_nested = json.loads(json_string_nested)

user_nested_01 = UserNested(**json_dict_nested)
print("user_nested_01:", user_nested_01, user_nested_01.address, user_nested_01.address.city)

# 인자로 전달 시 Nested 된 값을 dict 형태로 전달하여 생성.
user_nested_02 = UserNested(
    name="test_name", age=40, address = {"street": "123 Main St", "city": "Anytown"}
)
print("user_nested_02:", user_nested_02, user_nested_02.address, user_nested_02.address.city)

# python 기반으로 pydantic serialization
user_dump_01 = user.model_dump()
print(user_dump_01, type(user_dump_01))

# json 문자열 기반으로 pydantic serialization
user_dump_02 = user.model_dump_json()
print(user_dump_02, type(user_dump_02))

```
## FastAPI의 Async, 멀티 Thread, 멀티 Process 이해

`FastAPI_Async_Thread/main.py`

```py
from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

# long-running I/O-bound 작업 시뮬레이션
async def long_running_task():
    # 특정 초동안 수행 시뮬레이션
    await asyncio.sleep(20)        
    return {"status": "long_running task completed"}
    
@app.get("/task")
async def run_task():
    result = await long_running_task()
    return result

# @app.get("/task")
# async def run_task():
#     time.sleep(20)
#     return {"status": "long_running task completed"}

@app.get("/quick")
async def quick_response():
    return {"status": "quick response"}
```

## RDBMS 다루기 - SQLAlchemy 활용

```bash
 pip install sqlalchemy
 pip install mysql-connector-python
```

`MySqlWorkBench에서 실행`

```
/* sample db 및 데이터 생성 */

DROP DATABASE if exists blog_db;

CREATE DATABASE blog_db;

use blog_db;

DROP TABLE if exists blog;

CREATE TABLE blog (
  id int(11) NOT NULL AUTO_INCREMENT,
  title varchar(200) NOT NULL,
  author varchar(100) NOT NULL,
  content varchar(4000) NOT NULL,
  image_loc varchar(300) DEFAULT NULL,
  modified_dt datetime NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO blog_db.blog(title, author, content, modified_dt) values('테스트 title 1', '둘리', '테스트 컨텐츠 1', now());
INSERT INTO blog_db.blog(title, author, content, modified_dt) values('테스트 title 2', '길동', '테스트 컨텐츠 2', now());
INSERT INTO blog_db.blog(title, author, content, modified_dt) values('테스트 title 3', '도넛', '테스트 컨텐츠 3', now());
INSERT INTO blog_db.blog(title, author, content, modified_dt) values('테스트 title 4', '희동', '테스트 컨텐츠 4', now());

COMMIT;

/* connection 모니터링 스크립트. root로 수행 필요. */
select * from sys.session where db='blog_db' order by conn_id;
```

`DB_Fundamentals/db_basic.py`

```py
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@127.0.0.1:3306/blog_db"
# Engine 생성
engine = create_engine(DATABASE_CONN, poolclass=QueuePool,
            pool_size=10, max_overflow=0)

try: 
    # Connection 얻기
    conn = engine.connect()
    # SQL 선언 및 text로 감싸기
    query = "select id, title from blog"
    stmt = text(query)
    
    # SQL 호출하여 CursorResult 반환.
    result = conn.execute(stmt)
    print("type result:", result)

    rows = result.fetchall()
    print(rows)

    # print(type(rows[0]))
    # print(rows[0].id, rows[0].title)
    # print(rows[0][0], rows[0][1])
    # print(rows[0]._key_to_index)

    result.close()
except SQLAlchemyError as e:
    print(e)
finally: 
    # close() 메소드 호출하여 connection 반환.
    conn.close()

```

## Blog 애플리케이션 개발하기
  
**API 명세서**  
![](./img/fastapi/fastapi015.png)

**Application 모듈 디렉토리 구조**  

![](./img/fastapi/fastapi016.png)

```sql
create database blog_db;

drop table if exists blog;

create table blog_db.blog
(id integer auto_increment primary key,
title varchar(200) not null,
author varchar(100) not null,
content varchar(4000) not null,
image_loc varchar(300) null,
modified_dt datetime not null
);

truncate table blog;

insert into blog(title, author, content, modified_dt)
values ('FastAPI는 어떤 장점이 있는가?', '둘리', 
'FastAPI는 Python을 사용한 웹 애플리케이션 및 API 개발을 위한 현대적인 프레임워크로, 빠른 성능과 쉬운 사용성, 자동 문서화, 그리고 모던한 설계가 주요 장점입니다. \n
비동기 I/O 기능을 활용하여 높은 성능을 자랑하며, Python의 타입 힌트를 적극 활용해 타입 검사와 코드 자동 완성이 뛰어나 개발자가 실수를 줄이고 생산성을 높일 수 있습니다. \n
또한, 자동으로 API 문서를 생성하고 유지해주어 개발자가 인터랙티브한 문서를 쉽게 제공할 수 있습니다. \n
최신 웹 표준과 기술을 반영한 설계로 확장성과 유지보수성이 뛰어나며, 빠르게 성장하는 커뮤니티와 생태계를 통해 다양한 플러그인과 확장 기능을 지원받을 수 있습니다.'
, now());

insert into blog(title, author, content, modified_dt)
values ('FastAPI 주요 요소는 무엇인가', '고길동', 
'FastAPI의 주요 구성 요소에는 클라이언트로부터 받은 HTTP 요청을 처리하는 Request 객체와 서버에서 클라이언트로 보내는 HTTP 응답을 생성하는 Response 객체가 포함됩니다.\n
 또한, 경로와 경로 동작을 정의하여 API 엔드포인트를 설정하고, 의존성 주입을 통해 코드의 모듈화와 재사용성을 높일 수 있습니다.\n
 요청 바디는 Pydantic 모델을 사용해 자동으로 유효성 검사되며, 경로 및 쿼리 매개변수로 API 요청에서 전달되는 데이터를 처리합니다. \n
 FastAPI는 OpenAPI와 JSON Schema를 기반으로 API 문서를 자동 생성하며, Swagger UI와 ReDoc을 통해 실시간으로 API를 탐색하고 테스트할 수 있는 기능을 제공합니다.\n
 템플릿 렌더링 기능을 통해 HTML 페이지를 동적으로 생성할 수 있어, API뿐만 아니라 전체 웹 애플리케이션도 쉽게 구축할 수 있습니다.'
, now());

insert into blog(title, author, content, modified_dt)
values ('FastAPI를 어떻게 사용하면 좋을까요?', '도우넛', 
'FastAPI는 빠른 성능과 간단한 사용성 덕분에 다양한 분야에서 널리 사용되고 있습니다.\n
FastAPI는 고성능 API 서버 구축, 머신 러닝 모델 서빙, 마이크로서비스 아키텍처, 실시간 데이터 처리 애플리케이션, 백엔드 API 서버, 그리고 CRUD 애플리케이션 개발 등 다양한 분야에서 사용됩니다.\n
특히, 비동기 처리를 통한 빠른 성능과 자동 문서화 기능 덕분에 실시간 데이터 처리나 챗봇, IoT 애플리케이션 같은 응답 속도가 중요한 프로젝트에 적합합니다.\n
또한, 웹 애플리케이션의 백엔드 API 서버로 사용되거나, Pydantic과 SQLAlchemy 같은 라이브러리와 결합해 CRUD 애플리케이션을 빠르고 효율적으로 개발할 수 있습니다.\n
FastAPI는 다양한 규모와 유형의 프로젝트에서 성능과 개발 효율성을 높이는 데 큰 역할을 합니다.'
, now());

COMMIT;

/* connection 모니터링 스크립트. root로 수행 필요. */
select * from sys.session where db='blog_db' order by conn_id;
```

`Blog_DB_Handling/.env`

```env
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"

```
`Blog_DB_Handling/main.py`

```py
from fastapi import FastAPI
from routes import blog

app = FastAPI()
app.include_router(blog.router)
```

`Blog_DB_Handling/utils/util.py`

```py
def truncate_text(text, limit=150) -> str:
    if text is not None:
        if len(text) > limit:
            truncated_text = text[:limit] + "...."
        else:
            truncated_text = text
        return truncated_text
    return None

def newline_to_br(text_newline: str) -> str:
    if text_newline is not None:
        return text_newline.replace('\n', '<br>')
    return None
```

`Blog_DB_Handling/routes/blog.py`

```py
from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from db.database import direct_get_conn, context_get_conn
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import Blog, BlogData
from utils import util



# router 생성
router = APIRouter(prefix="/blogs", tags=["blogs"])
# jinja2 Template 엔진 생성
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_all_blogs(request: Request):
    conn = None
    try:
        conn = direct_get_conn()
        query = """
        SELECT id, title, author, content, image_loc, modified_dt FROM blog;
        """
        result = conn.execute(text(query))
        all_blogs = [BlogData(id=row.id,
            title=row.title,
            author=row.author,
            content=util.truncate_text(row.content),
            image_loc=row.image_loc, 
            modified_dt=row.modified_dt) for row in result]
        
        result.close()
        return templates.TemplateResponse(
            request = request,
            name = "index.html",
            context = {"all_blogs": all_blogs}
        )
    
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="알수없는 이유로 서비스 오류가 발생하였습니다")
    finally:
        if conn:
            conn.close()

@router.get("/show/{id}")
def get_blog_by_id(request: Request, id: int,
                conn: Connection = Depends(context_get_conn)):
    try:
        query = f"""
        SELECT id, title, author, content, image_loc, modified_dt from blog
        where id = :id
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = conn.execute(bind_stmt)
        # 만약에 한건도 찾지 못하면 오류를 던진다. 
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")

        row = result.fetchone()
        blog = BlogData(id=row[0], title=row[1], author=row[2], content=util.newline_to_br(row[3]),
                image_loc=row[4], modified_dt=row[5])
        
        result.close()
        return templates.TemplateResponse(
            request = request,
            name="show_blog.html",
            context = {"blog": blog})
    
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="알수없는 이유로 서비스 오류가 발생하였습니다")


@router.get("/new")
def create_blog_ui(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "new_blog.html",
        context = {}
    )

@router.post("/new")
def create_blog(request: Request
                , title = Form(min_length=2, max_length=200)
                , author = Form(max_length=100)
                , content = Form(min_length=2, max_length=4000)
                , conn: Connection = Depends(context_get_conn)):
    try:
        query = f"""
        INSERT INTO blog(title, author, content, modified_dt)
        values ('{title}', '{author}', '{content}', now())
        """
        conn.execute(text(query))
        conn.commit()

        return RedirectResponse("/blogs", status_code=status.HTTP_302_FOUND)
    except SQLAlchemyError as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="요청데이터가 제대로 전달되지 않았습니다.")

@router.get("/modify/{id}")
def update_blog_ui(request: Request, id: int, conn = Depends(context_get_conn)):
    try:
        query = f"""
        select id, title, author, content from blog where id = :id
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = conn.execute(bind_stmt)
        # 해당 id로 데이터가 존재하지 않으면 오류를 던진다.
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")
        row = result.fetchone()
    
        return templates.TemplateResponse(
            request = request,
            name="modify_blog.html",
            context = {"id": row.id, "title": row.title,
                    "author": row.author, "content": row.content}
        )
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="요청데이터가 제대로 전달되지 않았습니다.")

@router.post("/modify/{id}")
def update_blog(request: Request, id: int
                , title = Form(min_length=2, max_length=200)
                , author = Form(max_length=100)
                , content = Form(min_length=2, max_length=4000)
                , conn: Connection = Depends(context_get_conn)):
    
    try:
        query = f"""
        UPDATE blog 
        SET title = :title , author= :author, content= :content
        where id = :id
        """
        bind_stmt = text(query).bindparams(id=id, title=title, 
                                        author=author, content=content)
        result = conn.execute(bind_stmt)
        # 해당 id로 데이터가 존재하지 않아 update 건수가 없으면 오류를 던진다.
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")
        conn.commit()
        return RedirectResponse(f"/blogs/show/{id}", status_code=status.HTTP_302_FOUND)
    except SQLAlchemyError as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="요청데이터가 제대로 전달되지 않았습니다. ")

@router.post("/delete/{id}")
def delete_blog(request: Request, id: int
                , conn: Connection = Depends(context_get_conn)):
    try:
        query = f"""
        DELETE FROM blog
        where id = :id
        """

        bind_stmt = text(query).bindparams(id=id)
        result = conn.execute(bind_stmt)
        # 해당 id로 데이터가 존재하지 않아 delete 건수가 없으면 오류를 던진다.
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")
        conn.commit()
        return RedirectResponse("/blogs", status_code=status.HTTP_302_FOUND)

    except SQLAlchemyError as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
```

`Blog_DB_Handling/schemas/blog_schema.py`

```py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Annotated
from pydantic.dataclasses import dataclass

class BlogInput(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    author: str = Field(..., max_length=100)
    content: str = Field(..., min_length=2, max_length=4000)
    image_loc: Optional[str] = Field(None, max_length=400)
    #image_loc: Annotated[str, Field(None, max_length=400)] = None

class Blog(BlogInput):
    id: int
    modified_dt: datetime

@dataclass
class BlogData:
    id: int
    title: str
    author: str
    content: str
    modified_dt: datetime
    image_loc: str | None = None
```

`Blog_DB_Handling/db/database.py`

```py
from sqlalchemy import create_engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import contextmanager
from fastapi import status
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import os

# database connection URL
# DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"
load_dotenv()

DATABASE_CONN = os.getenv("DATABASE_CONN")

engine = create_engine(DATABASE_CONN, #echo=True,
                    poolclass=QueuePool,
                    #poolclass=NullPool, # Connection Pool 사용하지 않음. 
                    pool_size=10, max_overflow=0,
                    pool_recycle=300)

def direct_get_conn():
    conn = None
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")

def context_get_conn():
    conn = None
    try:
        conn = engine.connect()
        yield conn
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    finally:
        if conn:
            conn.close()

```

`Blog_DB_Handling/templates/index.html`

```html
{% raw %}<!DOCTYPE html>
<html>
<head>
    <title>블로그에 오신걸 환영합니다</title>
</head>
<body>
    <h1>모든 블로그 리스트</h1>
    <div><a href="/blogs/new">새로운 Blog 생성</a></div>
    {% for blog in all_blogs %}
        <div>
            <h3><a href="/blogs/show/{{ blog.id }}">{{ blog.title }}</a></h3>
            <p><small>Posted on {{ blog.modified_dt }} by {{ blog.author }} </small> </p>
            <p> {{ blog.content }} </p>
        </div>
    {% endfor %}
</body>
</html>{% endraw %}
```

`Blog_DB_Handling/templates/show_blog.html`

```html
{% raw %}<!DOCTYPE html>
<html>
<head>
    <title>블로그에 오신걸 환영합니다</title>
</head>
<body>
    <div>
        
        <h1>{{ blog.title }} </h1>
        <h5>Posted on {{ blog.modified_dt }} by {{ blog.author }} </small> </p>
        <h3>{{ blog.content | safe }}</h3>
    </div>
    <div>
        <a href="/blogs">Home으로 돌아가기</a>
        <a href="/blogs/modify/{{ blog.id }}">수정하기</a>
        <form action="/blogs/delete/{{ blog.id }}" method="POST">
            <button>삭제하기</button>
        </form>
        
    </div>
</body>
</html>{% endraw %}
```

`Blog_DB_Handling/templates/new_blog.html`

```html
{% raw %}<html>
<head>
    <title>새로운 블로그 생성</title>
</head>
<body>
    <form action="/blogs/new" method="POST">
        <div style="margin-bottom: 20px">
            <label for="title">제목:</label>
            <input type="text" id="title" name="title" style="width: 20rem;">
        </div>
        <div style="margin-bottom: 20px">
            <label for="author">작성자:</label>
            <input type="text" id="author" name="author" style="width: 10rem;">
        </div>
        <div style="margin-bottom: 20px">
            <label for="content">내용:</label>
            <textarea name="content" rows="5" cols="50"></textarea>
        </div>
        <button>신규 블로그 생성</button>
    </form>
    
</body>
</html>{% endraw %}
```

`Blog_DB_Handling/templates/modify_blog.html`

```html
<html>
<head>
    <title>블로그 수정</title>
</head>
<body>
    <form action="/blogs/modify/{{ id }}" method="POST">
        <div style="margin-bottom: 20px">
            <label for="title">제목:</label>
            <input type="text" id="title" name="title" value="{{ title }}" style="width: 20rem;">
        </div>
        <div style="margin-bottom: 20px">
            <label for="author">작성자:</label>
            <input type="text" id="author" name="author" value="{{ author }}"style="width: 10rem;">
        </div>
        <div style="margin-bottom: 20px">
            <label for="content">내용:</label>
            <textarea name="content" rows="5" cols="50">{{ content }}</textarea>
        </div>
        <button>블로그 수정</button>
    </form>
    
</body>
</html>
```


## Blog 애플리케이션 개발하기 - 리팩토링

```py

```

## Blog 애플리케이션 개발하기 - Bootstrap 적용 및 File Upload

```py

```

## Blog 애플리케이션 개발하기 - 비동기(Asynchronous) DB처리

```py

```

## FastAPI Exception Handler

```py

```

