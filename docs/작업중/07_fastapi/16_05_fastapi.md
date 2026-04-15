---
title: 5. FastAPI APIRouter
layout: default
grand_parent: Language
parent: FastAPI
nav_order: 5
permalink: /language/fastapi/fastapi_router
has_children: false
---

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

`Router/routes/item.py`

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
•	APIRouter: FastAPI에서 라우트(경로)를 모듈별로 분리해서 관리할 수 있게 해주는 기능  
•	prefix="/item": 이 라우터에 등록된 모든 경로는 /item으로 시작.    
    예: /item/123, /item/
•	tags=["item"]: Swagger 문서에서 이 API들을 “item” 그룹으로 묶어서 보여줌.  (자동 문서화할 때 보기 좋게 분류됨)  

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
