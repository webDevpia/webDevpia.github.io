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

## 실습 환경 구축

### 가상환경 생성 및 라이브러리 설치

```bash
conda create --name fastapi
conda activate fastapi
pip install fastapi
```

### 동작 테스트

```py
# FastAPI import
from fastapi import FastAPI

# FastAPI instance 생성. 
app = FastAPI()

# Path 오퍼레이션 생성. Path는 도메인명을 제외하고 / 로 시작하는 URL 부분
# 만약 url이 https://example.com/items/foo 라면 path는 /items/foo 
# Operation은 GET, POST, PUT/PATCH, DELETE등의 HTTP 메소드임. 
@app.get("/")
async def root():
    """
    루트 경로('/')에 대한 GET 요청을 처리하는 함수입니다.
    간단한 JSON 응답을 반환합니다.
    """
    return {"message": "Hello World"}
```

```bash
uvicorn Welcome.main:app --port=8081 --reload
```
### FastAPI와 클라이언트 간 동작 흐름 이해가기
![](./img/fastapi/fastapi001.png)

### Swagger UI를 이용한 동작 확인
api들을 브라우저 기반에서 편리하게 관리 및 문서화, 테스트 할 수 있는 기능을 제공  
http://127.0.0.1:8081/docs로 접속해서 결과 확인  

![](./img/fastapi/fastapi002.png)

## FastAPI Request

### HTTP Request Message 구성 및 HTTP 메소드 개요

### Path 파라미터 이해

### FastAPI Path 파라미터 다루기

### Query 파라미터 이해

### FastAPI Query 파라미터 다루기

### Request Body와 Form 이해

### Request Body

### Form


## FastAPI Response


## 템플릿 엔진과 정적 파일(Static file) 다루기


## FastAPI의 APIRouter


## Pydantic


## FastAPI의 Async, 멀티 Thread, 멀티 Process 이해


## RDBMS 다루기 - SQLAlchemy 활용


## Blog 애플리케이션 개발하기


## Blog 애플리케이션 개발하기 - 리팩토링


## Blog 애플리케이션 개발하기 - Bootstrap 적용 및 File Upload



```py

```

```py

```

```py

```

```py

```

```py

```

```py

```

```py

```

```py

```

```py

```

```py

```

```py

```

```py

```

```py

```






