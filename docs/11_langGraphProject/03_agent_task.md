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

# 01. Intent Agent 실습

사용자의 자연어 입력을 GPT를 통해 `food`, `activity`, `unknown` 중 하나로 분류하는 의도 판단 에이전트를 실습합니다.

LangGraph 흐름에서 가장 첫 번째로 실행되는 노드이며, 입력이 어떤 추천 경로로 이어질지 결정하는 중요한 단계입니다.

`agents/intent.py`

```py
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
import json

# GPT 기반 의도 분류 에이전트 설정
# 사용자의 입력 문장을 기반으로 food / activity / unknown 중 하나로 분류합니다.
llm = ChatOpenAI(
    model=OPENAI_MODEL,          # 사용할 OpenAI 모델 (예: gpt-4o)
    api_key=OPENAI_API_KEY,      # 환경변수에서 불러온 OpenAI API 키
    temperature=0.3,             # 창의성 제어 (낮을수록 일관성 ↑)
    model_kwargs={               # OpenAI에 전달할 추가 옵션
        "response_format": {"type": "json_object"}  # 반드시 JSON 객체로 응답
    }
)
# 노드로 사용할 함수는 반드시 독스트링이 반드시 있어야 합니다.
# 독스트링이 없으면 에러가 발생합니다.
# 독스트링은 반드시 함수의 첫 번째 줄에 작성해야 합니다.
def classify_intent(state: dict) -> dict:
    """사용자의 입력 문장을 기반으로 GPT를 호출하여 food, activity, unknown 중 하나의 intent를 분류합니다."""
    user_input = state.get("user_input", "")  # 사용자의 입력 문장 추출

    # GPT에게 의도를 분류하도록 요청할 프롬프트
    prompt = f"""
당신은 사용자의 자연어 입력을 food / activity / unknown 중 하나로 분류하는 AI입니다.

입력: "{user_input}"

분류 기준:
- 음식 관련 표현 → "food" (예: 배고파, 뭐 먹지, 야식 추천해줘 등)
- 활동 관련 표현 → "activity" (예: 심심해, 뭐 하지, 놀고 싶어 등)
- 증상, 감정, 질문, 애매한 표현 → "unknown"

조금 애매한 표현이라도 의미가 보이면 food 또는 activity로 분류하세요.

출력은 반드시 다음 중 하나의 JSON 배열 또는 객체로 작성하세요:
- 배열: ["food"]
- 객체: \{{ "intent": ["food"] \}}
"""

    # GPT 호출
    response = llm.invoke([{"role": "user", "content": prompt.strip()}])

    # GPT의 응답 원문을 출력 (디버깅용)
    intent_raw = response.content.strip()
    print(">>> GPT intent 응답:", intent_raw)

    try:
        # 응답을 JSON으로 파싱
        parsed = json.loads(intent_raw)

        # case 1: 응답이 배열 형태일 경우 (예: ["food"])
        if isinstance(parsed, list) and parsed and parsed[0] in ["food", "activity"]:
            return {**state, "intent": parsed[0]}

        # case 2: 응답이 딕셔너리 형태일 경우 (예: {"intent": ["activity"]})
        if isinstance(parsed, dict):
            if "intent" in parsed:
                inner = parsed["intent"]
                if isinstance(inner, list) and inner and inner[0] in ["food", "activity"]:
                    return {**state, "intent": inner[0]}
            # fallback: GPT가 "food": [] 또는 "activity": [] 형식으로 응답했을 경우
            for key in ["food", "activity"]:
                if key in parsed:
                    return {**state, "intent": key}

    except Exception as e:
        print(">>> intent 분류 파싱 실패:", str(e))

    # 모든 조건 실패 시 unknown으로 처리
    return {**state, "intent": "unknown"}
    
```
