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
- 객체: {{ "intent": ["food"] }}
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
## 📦 1. 라이브러리 및 모듈 불러오기

```python
# 필요한 라이브러리 및 에이전트 함수 불러오기
from agents.intent import classify_intent
```

## ✍️ 2. 샘플 입력 준비

```python
# 예시 입력을 딕셔너리로 구성합니다.
test_input_1 = {"user_input": "배고파"}
test_input_2 = {"user_input": "뭐 하지?"}
test_input_3 = {"user_input": "배가 아파요..."}
```

## 🚀 3. Intent 분류 함수 실행

```python
# classify_intent는 state 딕셔너리를 입력받아 intent를 판단해 반환합니다.
print("입력1:", test_input_1["user_input"])
print("결과:", classify_intent(test_input_1)["intent"])

print("입력2:", test_input_2["user_input"])
print("결과:", classify_intent(test_input_2)["intent"])

print("입력3:", test_input_3["user_input"])
print("결과:", classify_intent(test_input_3)["intent"])
```

## ✏️ 4. 직접 입력해보고 테스트해 보세요

```python
# 아래에 원하는 문장을 입력해보고 intent가 어떻게 분류되는지 확인해 보세요.
my_input = {"user_input": "비 오는 날 뭐 먹을까?"}
print("입력:", my_input["user_input"])
print("결과:", classify_intent(my_input)["intent"])
```


# 02. Time Agent 실습 노트북

현재 시각을 기준으로 시간대를 자동 분류하는 Time Agent의 동작을 실습합니다.

시간대는 아침(5-11시), 점심(11-16시), 저녁(16-22시), 야간(22-5시) 중 하나로 분류됩니다.
LangGraph 내에서 조건 분기를 위한 중요한 컨텍스트입니다.

`agents/time.py`

```py
from datetime import datetime

def get_time_slot(state: dict) -> dict:
    """현재 시각을 기준으로 시간대를 분류하여 상태에 추가합니다.

    시간대는 다음과 같이 분류됩니다:
    - 05:00 ~ 11:00 -> '아침'
    - 11:00 ~ 16:00 -> '점심'
    - 16:00 ~ 22:00 -> '저녁'
    - 22:00 ~ 05:00 -> '야간'
    """
    hour = datetime.now().hour  # 현재 시간의 시(hour) 정보를 가져옵니다.

    # 시간에 따라 적절한 시간대를 반환합니다.
    if 5 <= hour < 11:
        return {**state, "time_slot": "아침"}
    elif 11 <= hour < 16:
        return {**state, "time_slot": "점심"}
    elif 16 <= hour < 22:
        return {**state, "time_slot": "저녁"}
    else:
        return {**state, "time_slot": "야간"}  # 22시 이후 또는 5시 이전은 야간으로 처리
        
```

## 📦 1. 라이브러리 및 모듈 불러오기

```python
# 시간대 추출 에이전트 함수 불러오기
from agents.time import get_time_slot
```

## ✍️ 2. 샘플 상태 구성

```python
# 최소 입력: 아무 값 없이 빈 딕셔너리도 가능 (내부적으로 datetime.now 사용)
state = {}
```

## 🕒 3. 시간대 추출 실행

```python
result = get_time_slot(state)
print("현재 시간에 따른 분류된 시간대:", result["time_slot"])
```

## 🔁 4. 직접 테스트해보세요

```python
# 실제 시각 확인 (현재 실행되는 환경 기준)
from datetime import datetime
print("현재 시각 (기준):", datetime.now().strftime("%Y-%m-%d %H:%M"))
```

# 03. Season Agent 실습 노트북

현재 날짜를 기준으로 계절을 자동 분류하는 Season Agent의 동작을 실습합니다.

계절은 봄(3~5월), 여름(6~8월), 가을(9~11월), 겨울(12~2월) 중 하나로 분류되며,
LangGraph 내에서는 음식/활동 추천 시 조건 컨텍스트로 사용됩니다.

`agents/season.py`

```py
from datetime import datetime

def get_season(state: dict) -> dict:
    """현재 월(month)을 기준으로 계절을 분류하여 상태에 추가합니다.

    분류 기준:
    - 3월 ~ 5월   : 봄
    - 6월 ~ 8월   : 여름
    - 9월 ~ 11월  : 가을
    - 12월, 1월, 2월 : 겨울
    """
    month = datetime.now().month  # 현재 월(1~12)을 가져옵니다

    # 월에 따라 계절을 분류합니다
    if 3 <= month <= 5:
        season = "봄"
    elif 6 <= month <= 8:
        season = "여름"
    elif 9 <= month <= 11:
        season = "가을"
    else:
        season = "겨울"  # 12월, 1월, 2월

    # 상태에 계절 정보를 추가해서 반환합니다
    return {**state, "season": season}
    
```

## 📦 1. 라이브러리 및 모듈 불러오기

```python
# 계절 분류 에이전트 함수 불러오기
from agents.season import get_season
```

## ✍️ 2. 샘플 상태 구성

```python
# 계절 분류는 현재 월을 기준으로 자동 판단됩니다.
state = {}
```

## 🍃 3. 계절 분류 실행

```python
result = get_season(state)
print("현재 날짜에 따른 분류된 계절:", result["season"])
```

## 🗓 4. 오늘 날짜 확인

```python
from datetime import datetime
print("오늘 날짜:", datetime.now().strftime("%Y-%m-%d"))
```

# 04. Weather Agent 실습 노트북

OpenWeather API를 활용하여 현재 지역의 날씨 정보를 가져오는 Weather Agent의 동작을 실습합니다.

LangGraph 내에서는 음식 및 활동 추천 시 조건을 구성하는 중요한 컨텍스트입니다.

`agents/weather.py`

```py
import os
import requests
from config import WEATHER_API_KEY

def get_weather(state: dict) -> dict:
    """OpenWeather API를 통해 현재 날씨 정보를 가져와서 상태에 추가합니다.

    현재는 location이 '서울' 기준으로 고정되어 있으며,
    반환되는 날씨 상태는 'Clear', 'Clouds', 'Rain', 'Snow' 등입니다.
    """

    # OpenWeather API 호출 URL과 파라미터 설정
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "Seoul",
        "appid": WEATHER_API_KEY,
        "lang": "kr",
        "units": "metric"
    }

    # API 요청 전 로그 출력
    print(">>> OpenWeather API 호출 시작 (서울 기준)")

    # GET 요청을 통해 날씨 정보 요청
    response = requests.get(url, params=params)

    # 응답 코드가 실패일 경우 예외 발생
    response.raise_for_status()

    # 응답에서 날씨 상태 추출
    weather_data = response.json()
    weather = weather_data["weather"][0]["main"]  # 예: 'Clear', 'Rain', 'Clouds'

    # 상태에 날씨 정보 추가 후 반환
    return {**state, "weather": weather}
```
## 📦 1. 라이브러리 및 모듈 불러오기

```python
# 날씨 정보를 불러오는 Weather Agent 함수
from agents.weather import get_weather
```

## ✍️ 2. 샘플 입력 구성

```python
# 지역 정보가 포함된 상태 구성 (현재는 'Seoul'로 고정되어 있음)
state = {
    "location": "홍대"  # 내부적으로 'Seoul'로 요청됩니다.
}
```

## 🌦 3. 날씨 정보 가져오기

```python
# OpenWeather API를 호출하여 날씨 정보를 받아옵니다.
result = get_weather(state)
print("날씨 상태:", result.get("weather"))
```

## ℹ️ 참고 사항
- 날씨는 OpenWeather에서 가져오며, `weather_main` 값을 사용합니다 (예: Clear, Rain, Snow 등)
- 실제 요청은 기본 설정된 'Seoul'에 대해 수행되며, 향후 확장을 위해 location별 좌표 기반 API도 사용할 수 있습니다.


# 05. Food Agent 실습

사용자의 의도(`food`)에 따라 GPT를 통해 음식 추천을 생성하는 흐름을 실습합니다.

LangGraph 내에서 `intent == food`인 경우 실행되며, 추천 음식 리스트를 생성합니다.

`agents/food.py`
```py
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
import json

# GPT 기반 음식 추천 에이전트 구성
llm = ChatOpenAI(
    model=OPENAI_MODEL,                     # 사용할 GPT 모델 이름
    api_key=OPENAI_API_KEY,                # .env에서 불러온 API 키
    temperature=0.5,                       # 결과 다양성 조절
    model_kwargs={
        "response_format": {"type": "json_object"}  # JSON 형식 강제
    }
)

def recommend_food(state: dict) -> dict:
    """
    사용자의 입력과 계절, 날씨, 시간대 정보를 기반으로
    GPT를 통해 음식 추천을 생성하는 함수입니다.
    """

    # 상태에서 필요한 정보 추출
    user_input = state.get("user_input", "")
    season = state.get("season", "봄")
    weather = state.get("weather", "Clear")
    time_slot = state.get("time_slot", "점심")

    # GPT에게 보낼 프롬프트 정의 (f-string 내부 문자열은 안전하게 작성) 페르소나는 디테일하게 작성하는것이 좋음.
    prompt = f"""당신은 음식 추천 AI입니다.

사용자 입력: "{user_input}"
현재 조건:
- 계절: {season}
- 날씨: {weather}
- 시간대: {time_slot}

이 조건에 어울리는 음식 2가지를 추천해 주세요.

사용자가 특정 음식을 언급한 경우(예: "피자")에는 그 음식을 포함하거나,
관련된 음식 또는 어울리는 음식으로 추천해도 좋습니다.

결과는 반드시 JSON 배열 형식으로 출력하세요.
예: ["피자", "떡볶이"]
"""  # f-string 끝

    # GPT 호출 실행
    response = llm.invoke([{"role": "user", "content": prompt.strip()}])

    # 응답 내용을 JSON으로 파싱
    items = json.loads(response.content)

    # 응답이 딕셔너리일 경우 → 값만 추출
    if isinstance(items, dict):
        items = [i for sub in items.values() for i in (sub if isinstance(sub, list) else [sub])]
    elif not isinstance(items, list):
        items = [str(items)]  # 리스트가 아니면 리스트로 감싸기

    # 추천 음식 리스트를 상태에 추가하여 반환
    return {**state, "recommended_items": items}
    
```

## 📦 1. 라이브러리 및 모듈 불러오기

```python
# GPT 기반 음식 추천 에이전트 함수 불러오기
from agents.food import recommend_food
```

## ✍️ 2. 샘플 입력 구성

```python
# 음식 추천에 필요한 최소 상태를 정의합니다.
state = {
    "user_input": "비오는 날 뜨끈한 거 뭐 없을까",
    "season": "봄",
    "weather": "Rain",
    "time_slot": "야간"
}
```

## 🚀 3. 음식 추천 실행 및 결과 확인

```python
# GPT가 조건에 맞는 음식 리스트를 생성합니다.
result = recommend_food(state)
print("추천된 음식 리스트:", result["recommended_items"])
```

## ✏️ 4. 다른 조건으로도 테스트해보세요

```python
# 여기에 다른 계절/날씨/시간대를 넣어보며 실습해보세요.
state2 = {
    "user_input": "출출해",
    "season": "겨울",
    "weather": "Clear",
    "time_slot": "야간"
}
result2 = recommend_food(state2)
print("추천된 음식:", result2["recommended_items"])
```

# 06. Activity Agent 실습

사용자의 의도(`activity`)에 따라 GPT를 통해 활동 추천을 생성하는 흐름을 실습합니다.

LangGraph 내에서 `intent == activity`인 경우 실행되며, 날씨, 계절, 시간대 정보를 활용해 활동 리스트를 생성합니다.

`agents/activity.py`

```py
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
import json

# GPT 기반 활동 추천 에이전트 구성
llm = ChatOpenAI(
    model=OPENAI_MODEL,                    # 사용할 GPT 모델 이름
    api_key=OPENAI_API_KEY,               # OpenAI API 키 (환경변수에서 불러옴)
    temperature=0.5,                      # 창의성 제어 (중간값)
    model_kwargs={                        # 응답 형식 명시
        "response_format": {"type": "json_object"}
    }
)

def recommend_activity(state: dict) -> dict:
    """
    GPT를 사용하여 사용자의 상황과 입력을 기반으로
    추천할 활동 2가지를 생성하는 함수입니다.
    """

    # 입력 상태에서 정보 추출
    user_input = state.get("user_input", "")
    season = state.get("season", "봄")
    weather = state.get("weather", "Clear")
    time_slot = state.get("time_slot", "점심")

    # GPT에게 활동 추천을 요청할 프롬프트 작성
    prompt = f"""당신은 활동 추천 AI입니다.

사용자 입력: "{user_input}"
현재 조건:
- 계절: {season}
- 날씨: {weather}
- 시간대: {time_slot}

이 조건과 입력에 어울리는 활동 2가지를 추천해 주세요.
실내 활동이 포함되면 더 좋습니다.

결과는 반드시 JSON 배열 형식으로 출력하세요.
예: ["북카페 가기", "실내 보드게임"]
"""  # 안전한 f-string

    # GPT 호출
    response = llm.invoke([{"role": "user", "content": prompt.strip()}])

    # GPT 응답 파싱
    items = json.loads(response.content)

    # dict 형태 응답 → 값만 리스트로 추출
    if isinstance(items, dict):
        items = [i for sub in items.values() for i in (sub if isinstance(sub, list) else [sub])]
    elif not isinstance(items, list):
        items = [str(items)]  # 단일 문자열을 리스트로 감싸기

    # 추천 활동을 상태에 추가하여 반환
    return {**state, "recommended_items": items}
    
```

## 📦 1. 라이브러리 및 모듈 불러오기

```python
# GPT 기반 활동 추천 에이전트 함수 불러오기
from agents.activity import recommend_activity
```

## ✍️ 2. 샘플 입력 구성

```python
# 활동 추천에 필요한 최소 상태 정보를 입력합니다.
state = {
    "user_input": "심심해",
    "season": "봄",
    "weather": "Rain",
    "time_slot": "야간"
}
```

## 🚀 3. 활동 추천 실행 및 결과 확인

```python
# GPT가 조건에 맞는 활동 리스트를 생성합니다.
result = recommend_activity(state)
print("추천된 활동 리스트:", result["recommended_items"])
```

## ✏️ 4. 다른 조건으로도 테스트해보세요

```python
# 여기에 다른 입력을 설정해서 테스트할 수 있습니다.
state2 = {
    "user_input": "뭔가 하고 싶어",
    "season": "겨울",
    "weather": "Snow",
    "time_slot": "야간"
}
result2 = recommend_activity(state2)
print("추천된 활동:", result2["recommended_items"])
```

# 07. Intent Unsupported Agent 실습 노트북

사용자 입력이 음식/활동 추천과 관련되지 않았을 경우,
그에 대한 대응 메시지를 생성하는 Intent Unsupported Agent의 동작을 실습합니다.

LangGraph에서는 분류된 intent가 'food', 'activity' 외의 'unknown'일 경우에만 실행되며,
사용자에게 자연스럽고 친절한 종료 메시지를 제공합니다.

`agents/intent_unsupported.py`

```py
def intent_unsupported_handler(state: dict) -> dict:
    """
    사용자의 입력이 'food'나 'activity'로 분류되지 않은 경우에 실행되는 에이전트입니다.

    의도가 'unknown'으로 판단되면 추천을 수행하지 않고,
    대신 사용자에게 정중한 안내 메시지를 전달합니다.
    """

    # 안내 메시지를 상태에 추가
    return {
        **state,
        "final_message": "죄송해요! 저는 음식이나 활동 추천만 도와드릴 수 있어요 😊"
    }
    
```

## 📦 1. 라이브러리 및 모듈 불러오기

```python
# 의도를 분류할 수 없을 때 실행되는 종료 메시지 함수 불러오기
from agents.intent_unsupported import intent_unsupported_handler
```

## ✍️ 2. 샘플 입력 구성

```python
# 사용자의 입력이 추천 불가능한 경우 상태 예시
state = {
    "user_input": "아이구 배야!",
    "intent": "unknown"
}
```

## 🛑 3. graceful 종료 메시지 출력

```python
# 종료 메시지 생성
result = intent_unsupported_handler(state)
print("메시지:", result["final_message"])
```

# 08. Keyword Agent 실습 노트북

음식 또는 활동 추천 결과를 바탕으로, 장소 검색에 사용할 키워드를 생성하는 흐름을 실습합니다.

GPT를 활용하여 추천 항목(예: 김치찌개, 책 읽기 등)을 검색 가능한 장소 키워드(예: 한식, 북카페 등)로 변환합니다.

`agents/keyword.py`

```py
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
import json

# GPT 기반 검색 키워드 생성 에이전트
# 음식 또는 활동 추천 결과를 바탕으로 장소 검색에 적합한 키워드를 추출합니다.
llm = ChatOpenAI(
    model=OPENAI_MODEL,                     # 사용할 GPT 모델
    api_key=OPENAI_API_KEY,                # 환경변수에서 불러온 OpenAI API 키
    temperature=0.3,                       # 창의성 낮게 (정확성 위주)
    model_kwargs={
        "response_format": {"type": "json_object"}  # 응답 형식 강제: JSON 객체
    }
)

def generate_search_keyword(state: dict) -> dict:
    """
    GPT를 사용하여 추천 항목을 바탕으로 장소 검색용 키워드를 생성하는 함수입니다.
    예: 김치찌개 → 한식, 책 읽기 → 북카페
    """

    # 추천 항목 리스트 추출 (음식 또는 활동)
    items = state.get("recommended_items", ["추천"])
    if isinstance(items, dict):
        # 딕셔너리인 경우 → 값만 추출 (중첩 flatten)
        items = [i for sub in items.values() for i in (sub if isinstance(sub, list) else [sub])]
    elif not isinstance(items, list):
        items = [str(items)]  # 문자열인 경우 → 리스트로 변환

    item = items[0]  # 첫 번째 추천 항목을 기반으로 키워드 생성

    user_input = state.get("user_input", "")      # 사용자 입력
    intent = state.get("intent", "food")          # food 또는 activity

    # GPT 프롬프트 작성
    prompt = f"""사용자의 입력: "{user_input}"
추천 항목: "{item}"
의도: "{intent}"

이 항목을 장소에서 검색하려고 합니다.
음식이라면 음식 종류(예: 김치찌개 → 한식),
활동이라면 장소 유형(예: 책 읽기 → 북카페)으로 변환하세요.

결과는 반드시 JSON 배열로 출력하세요.
예: ["한식"]
"""  # f-string 끝

    # GPT 호출
    response = llm.invoke([{"role": "user", "content": prompt.strip()}])

    # GPT 응답 파싱
    keywords = json.loads(response.content)

    # dict 형태 응답 → 값 추출
    if isinstance(keywords, dict):
        keywords = [i for sub in keywords.values() for i in (sub if isinstance(sub, list) else [sub])]
    elif not isinstance(keywords, list):
        keywords = [str(keywords)]

    # 생성된 키워드 중 첫 번째를 상태에 추가
    return {**state, "search_keyword": keywords[0] if keywords else item}
    
```

## 📦 1. 라이브러리 및 모듈 불러오기

```python
# GPT 기반 장소 검색 키워드 생성 함수 불러오기
from agents.keyword import generate_search_keyword
```

## ✍️ 2. 샘플 입력 구성

```python
# 음식 또는 활동 추천 결과를 기반으로 키워드를 생성합니다.
state = {
    "user_input": "피자",
    "intent": "food",
    "recommended_items": ["피자"]
}
```

## 🚀 3. 키워드 생성 실행 및 결과 확인

```python
# GPT가 추천 항목을 바탕으로 장소 검색 키워드를 생성합니다.
result = generate_search_keyword(state)
print("생성된 장소 검색 키워드:", result["search_keyword"])
```

## ✏️ 4. 다른 추천 항목으로도 실습해보세요

```python
# 아래 예시처럼 활동 추천 결과로 테스트해볼 수도 있습니다.
state2 = {
    "user_input": "책 읽기",
    "intent": "activity",
    "recommended_items": ["책 읽기"]
}
result2 = generate_search_keyword(state2)
print("추천 활동 기반 장소 키워드:", result2["search_keyword"])
```
# 09. Place Agent 실습 노트북

장소 검색 키워드를 기반으로 Kakao Local API를 이용해 실제 장소를 검색하는 흐름을 실습합니다.

LangGraph 내에서는 음식 또는 활동에 대한 추천 키워드를 받아 실제 장소 정보를 가져오게 됩니다.

`agents/place.py`

```py
{% raw %}
import requests
from config import KAKAO_API_KEY

def search_place(state: dict) -> dict:
    """
    사용자의 지역 정보(location)와 검색 키워드(search_keyword)를 바탕으로
    Kakao Local API를 호출하여 근처 장소 정보를 가져오는 함수입니다.
    """

    # 상태에서 검색 키워드 및 지역 정보 추출
    location = state.get("location", "홍대")               # 예: "홍대"
    keyword = state.get("search_keyword", "추천")          # 예: "한식", "북카페"

    # 검색어는 '지역 + 키워드' 조합으로 구성
    query = f"{location} {keyword}"
    print(">>> GPT 생성 키워드 검색:", query)  # 디버깅용 로그

    # Kakao Local Search API endpoint
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": f"KakaoAK {KAKAO_API_KEY}"  # API 키 인증
    }
    params = {
        "query": query,   # 검색어
        "size": 5         # 최대 5개의 결과 요청
    }

    # API 요청 전송
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()  # 요청 실패 시 예외 발생

    # 응답 결과 중 첫 번째 장소만 사용
    docs = res.json()["documents"]

    if docs:
        top = docs[0]  # 가장 관련성 높은 장소
        place = {
            "name": top["place_name"],               # 장소 이름
            "address": top["road_address_name"],     # 도로명 주소
            "url": top["place_url"]                  # 지도 링크
        }
    else:
        # 검색 결과 없을 경우 기본 메시지
        place = {
            "name": "추천 장소 없음",
            "address": "",
            "url": ""
        }

    # 추천 장소 정보를 상태에 추가하여 반환
    return {**state, "recommended_place": place}
    {% endraw %}
    
```
