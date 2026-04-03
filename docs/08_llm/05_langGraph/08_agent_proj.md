---
title: 8. LangGraph 프로젝트 정의서
layout: default
grand_parent: LLM
parent: LangGraph
nav_order: 8
permalink: /llm/langgraph/agent_proj
--- 

# 📘 프로젝트 정의서: 아, 뭐 먹지? 뭐 하지?

---

## ✅ 프로젝트 개요

**"아, 뭐 먹지? 뭐 하지?"**는 GPT 및 LangGraph를 기반으로 사용자의 자연어 입력을 분석하고,  
현재 시간, 계절, 날씨를 고려하여 적절한 **음식 또는 활동을 추천**하는 스마트 개인 비서형 AI 서비스입니다.

사용자는 단순히 `"배고파"`, `"심심해"`, `"뭐하지?"` 와 같은 자연어를 입력하면,  
GPT가 이를 이해하고 추천 흐름을 자동으로 제어합니다.

---

## 🎯 목표

- 자연어 기반 상황 분석 및 의도 분류
- 실시간 조건(날씨, 시간대, 계절)에 맞춘 개인화 추천
- 음식/활동 → 장소 검색 → 감성 요약까지 완결된 추천 서비스 구현
- 초급자도 이해할 수 있는 LangGraph 기반 구조 실습 지원

---

## 🧩 기술 스택

| 항목 | 사용 기술 |
|------|-----------|
| LLM 기반 추천 | GPT-4o (via `langchain-openai`)  
| 흐름 제어 | LangGraph  
| 웹 UI | Streamlit (옵션)  
| 외부 API | Kakao Local API, OpenWeather API  
| 환경 구성 | Python 3.12, `.env`, `python-dotenv`  

---

## 🧠 주요 기능

| 기능 | 설명 |
|------|------|
| Intent 분류 | 입력 문장을 `food`, `activity`, `unknown` 으로 분류  
| 시간대 감지 | 현재 시각 → `"아침", "점심", "저녁", "야간"`  
| 계절 감지 | 현재 월 → `"봄", "여름", "가을", "겨울"`  
| 날씨 확인 | OpenWeather API를 통해 날씨 (`Rain`, `Clear` 등) 추출  
| 음식/활동 추천 | 조건 기반으로 GPT 추천 2가지 생성  
| 장소 검색 | Kakao API로 추천 항목 기반 장소 추천  
| 감성 메시지 생성 | 최종 결과를 요약 문장으로 생성해 사용자에게 출력  

---

## 🗂 에이전트 구성

| 에이전트 | 설명 |
|----------|------|
| `classify_intent` | 입력 문장 분석 → 추천 흐름 분기  
| `get_time_slot` | 시간대 추출 (5~11: 아침 등)  
| `get_season` | 월 기준 계절 추출  
| `get_weather` | 날씨 API 호출 → 현재 날씨 추출  
| `recommend_food` | GPT로 음식 추천 2개 생성  
| `recommend_activity` | GPT로 활동 추천 2개 생성  
| `generate_search_keyword` | 검색 키워드 (예: 한식, 북카페 등) 생성  
| `search_place` | Kakao API로 장소 추천  
| `summarize_message` | 최종 안내 문장 생성  
| `intent_unsupported_handler` | 추천 불가 시 graceful 종료 메시지 제공  

---

## 🧪 테스트 방법

- 터미널 실행: `python test_runner.py`
- Pytest 실행: `pytest test_graph.py`
- Web UI: `streamlit run app.py`

---

## 📂 프로젝트 구성 파일 예시

```
📦 ah-mwo-meokji
├── agents/
│   ├── intent.py
│   ├── time.py
│   ├── season.py
│   ├── weather.py
│   ├── food.py
│   ├── activity.py
│   ├── keyword.py
│   ├── place.py
│   ├── summary.py
│   └── intent_unsupported.py
├── run_graph.py
├── app.py
├── test_runner.py
├── test_graph.py
├── .env
```

---

## ✨ 확장 아이디어

- `"다른 음식 추천해줘"` → 대화형 흐름 확장
- 지도 시각화 / 추천 기록 저장
- 사용자 피드백(👍/👎) 수집 및 반영
- 대화형 Web UI 구성 (Streamlit Chat)

--- 


# 📘 LangGraph 에이전트 함수 설명서

"아, 뭐 먹지? 뭐 하지?" 프로젝트에서 사용되는 10개의 에이전트 함수들에 대한 상세한 설명을 제공합니다.
각 함수는 LangGraph의 상태 흐름 안에서 특정 역할을 수행하며, 입력과 출력 구조도 함께 설명되어 있습니다.

---

## 1. `classify_intent(state)`

### 📌 역할
사용자의 자연어 입력(`user_input`)을 바탕으로 GPT를 사용하여 의도를 분류합니다.

### 📥 입력
- `state["user_input"]`: 예) `"배고파"`, `"심심해"`, `"운동 추천해줘"`

### 📤 출력
- `state["intent"]`: `"food"`, `"activity"`, `"unknown"` 중 하나

---

## 2. `get_time_slot(state)`

### 📌 역할
현재 시각(`datetime.now()`)을 기준으로 시간대를 자동 분류합니다.

### 분류 기준
- 05~11시: `"아침"`
- 11~16시: `"점심"`
- 16~22시: `"저녁"`
- 22~05시: `"야간"`

### 📤 출력
- `state["time_slot"]`

---

## 3. `get_season(state)`

### 📌 역할
현재 월을 기준으로 계절을 분류합니다.

### 분류 기준
- 3~5월: `"봄"` / 6~8월: `"여름"` / 9~11월: `"가을"` / 12~2월: `"겨울"`

### 📤 출력
- `state["season"]`

---

## 4. `get_weather(state)`

### 📌 역할
OpenWeather API를 호출하여 현재 날씨 상태를 가져옵니다.

### 📥 입력
- `state["location"]` (현재는 내부적으로 `"Seoul"`로 고정)

### 📤 출력
- `state["weather"]`: 예) `"Rain"`, `"Clear"`, `"Snow"`

---

## 5. `recommend_food(state)`

### 📌 역할
GPT를 사용하여 조건(계절, 시간대, 날씨, 사용자 입력)에 따라 음식 2가지를 추천합니다.

### 📥 입력
- `user_input`, `season`, `weather`, `time_slot`

### 📤 출력
- `state["recommended_items"]`: 예) `["김치찌개", "된장찌개"]`

---

## 6. `recommend_activity(state)`

### 📌 역할
GPT를 사용하여 사용자의 활동 의도에 맞는 추천 활동 2가지를 생성합니다.

### 📥 입력
- `user_input`, `season`, `weather`, `time_slot`

### 📤 출력
- `state["recommended_items"]`: 예) `["책 읽기", "영화 보기"]`

---

## 7. `generate_search_keyword(state)`

### 📌 역할
추천된 음식 또는 활동을 기반으로 장소 검색용 키워드를 GPT로 생성합니다.

### 📥 입력
- `state["recommended_items"]`
- `state["intent"]`

### 📤 출력
- `state["search_keyword"]`: 예) `"한식"`, `"북카페"`

---

## 8. `search_place(state)`

### 📌 역할
`location + search_keyword` 조합으로 Kakao 장소 검색 API를 호출해 근처 장소를 추천합니다.

### 📥 입력
- `state["location"]`, `state["search_keyword"]`

### 📤 출력
- `state["recommended_place"]`: 이름, 주소, URL을 포함한 장소 정보

---

## 9. `summarize_message(state)`

### 📌 역할
모든 정보를 종합하여 사용자가 보기 좋은 감성적 요약 메시지를 GPT로 생성합니다.

### 📥 입력
- 추천 항목, 장소, intent, 시간/날씨 등 전체 상태

### 📤 출력
- `state["final_message"]`: 사용자에게 보여줄 최종 문장

---

## 10. `intent_unsupported_handler(state)`

### 📌 역할
intent가 `unknown`일 경우 실행되어 사용자에게 정중한 안내 메시지를 반환합니다.

### 📥 입력
- `state["intent"] == "unknown"`

### 📤 출력
- `state["final_message"]`: `"죄송해요! 음식이나 활동만 추천할 수 있어요 😊"`