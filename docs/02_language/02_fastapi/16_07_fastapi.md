---
title: 7. FastAPI Async
layout: default
grand_parent: Language
parent: FastAPI
nav_order: 7
permalink: /language/fastapi/fastapi_async
has_children: false
---

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
    
@app.get("/async_task")
async def run_async_task():
    result = await long_running_task()
    return result

@app.get("/sync_task")
async def run_sync_task():
    time.sleep(20)
    return {"status": "long_running task completed"}

@app.get("/quick")
async def quick_response():
    return {"status": "quick response"}
```

