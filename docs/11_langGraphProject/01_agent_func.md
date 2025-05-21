---
title: LangGraph 에이전트 함수 설명서
layout: default
parent: LangGraph Project
nav_order: 1
permalink: /langgraph_prj/agent_func
# nav_exclude: true
# search_exclude: true
--- 


# 📘 LangGraph 에이전트 함수 설명서

이 문서는 "아, 뭐 먹지? 뭐 하지?" 프로젝트에서 사용되는 10개의 에이전트 함수들에 대한 상세한 설명을 제공합니다.
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



