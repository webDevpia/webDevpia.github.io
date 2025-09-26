---
title: FastAPI Pydantic
layout: default
grand_parent: Language
parent: FastAPI
nav_order: 6
permalink: /language/fastapi/pydantic
has_children: false
---

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

    # 객체가 가진 여러 정보 중 특정 핵심 정보(id, name)만 간단히 보여주는 용도
    def get_info(self):
        return f"id: {self.id}, name: {self.name}"

    # 객체를 print() 하거나, 문자열로 변환하려고 할 때
    # 자동으로 호출되는 Python 특수 메서드.
    def __str__(self):
        return f"id: {self.id}, name: {self.name}, email: {self.email}, age: {self.age}"


# 일반 클래스 객체 생성 - 타입 체크, 유효성 검사 전혀 없음.
userobj = UserClass(10, 'test_name', 'tname@example.com', 40)
print("userobj:", userobj, userobj.id)


# Pydantic Model 객체화. - 필드를 명시적으로 지정해야 함, 타입 자동 검증
# User(10, 'test_name', 'tname@example.com', 40) 하지 않도록 유의
# 매개변수 첫번째 * 정의되어 있음.
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


# python 기반으로 pydantic serialization <class 'dict'>
user_dump_01 = user.model_dump()
print(user_dump_01, type(user_dump_01))


# json 문자열 기반으로 pydantic serialization <class 'str'>
user_dump_02 = user.model_dump_json()
print(user_dump_02, type(user_dump_02))

```
Python에서는
• *args : 위치 인자 (positional arguments)를 풀어서 전달.  
• **kwargs : 키워드 인자 (keyword arguments)를 풀어서 전달.  

즉, **는 딕셔너리 형태의 키-값 쌍을 풀어서 함수 인자처럼 전달할 때 사용하는 연산자.  

user = User(**data)  
✅ 동작: User(id=10, name="Alice", email="alice@example.com", age=30). 

`Pydantic/pydantic_02.py`

```py
from pydantic import BaseModel, ValidationError, ConfigDict, Field, Strict
from typing import List, Annotated

class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    # 모델 전체에 엄격한 타입 검사가 적용
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
# > precise=Decimal('123.45')
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
# > made_in='USA'

```

`Pydantic/pydantic_05.py`

```py
from pydantic import BaseModel,  ValidationError, field_validator, model_validator
from typing import Optional


class User(BaseModel):
    username: str
    password: str
    confirm_password: str

    # username 값이 공백이거나 빈 문자열이면 에러 발생, 정상 값이면 그대로 반환
    @field_validator('username')
    def username_must_not_be_empty(cls, value: str):
        if not value.strip():
            raise ValueError("Username must not be empty")
        return value

    # 비밀번호가 8자 이상, 숫자(digit)가 최소 1개, 문자(alpha)가 최소 1개 
    # 조건 중 하나라도 어기면 에러 발생
    @field_validator('password')
    def password_must_be_strong(cls, value: str):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in value):
            raise ValueError('Password must contain at least one letter')
        return value

    # 모델 전체를 본 뒤(mode='after') 
    # password와 confirm_password가 같은지 검증,
    # 일치하지 않으면 에러 발생 
    # 통과하면 모델 인스턴스를 그대로 반환
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

**종합 테스트**

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
