---
title: LangGraph 프로젝트
layout: default
parent: LangGraph Project
nav_order: 3
permalink: /langgraph_prj/agent_task
# nav_exclude: true
# search_exclude: true
--- 

# 00. 환경설정 파일 작성

`.env`

```py
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
TAVILY_API_KEY=
KAKAO_API_KEY=
WEATHER_API_KEY=
```

`config.py`

```py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
```

