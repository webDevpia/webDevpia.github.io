---
title: 3. Cache
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 3
permalink: /llm/langchain/cache
--- 
# LangChain 모델 비용 & 캐싱 (v0.3.x 기준)

---

## 1. 왜 캐싱(Caching)이 필요한가?

LLM을 여러 번 호출하면 API 비용이 급격히 늘어납니다.  
LangChain은 동일한 요청에 대해 결과를 **자동으로 저장(Cache)** 하고,  
다음에 같은 입력이 들어올 때 API를 다시 호출하지 않도록 합니다.

> 💡 **핵심 개념:** "같은 질문에 같은 답변이면, 굳이 모델을 다시 부를 필요가 없다!"

---

## 2. LangChain의 캐싱 구조

LangChain의 캐싱은 `langchain_community.cache` 모듈에 구현되어 있습니다.

| 캐시 클래스 | 설명 | 저장 위치 |
|--------------|------|-------------|
| **InMemoryCache** | 가장 간단한 형태의 캐시 | 프로그램 메모리 내부 |
| **SQLiteCache** | 파일 기반 캐시 | 로컬 SQLite DB |
| **RedisCache** | 서버 기반 캐시 | Redis 서버 |

---

## 3. 기본 사용 예제

### ✅ (1) InMemoryCache 예시
```python
from langchain.globals import set_llm_cache, get_llm_cache
from langchain_community.cache import InMemoryCache
from langchain_openai import ChatOpenAI
import time

# ✅ 전역 캐시 설정
cache = InMemoryCache()
set_llm_cache(cache)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = "서울의 수도는 어디인가요?"

# 1️⃣ 첫 번째 호출 (API 요청 발생)
start = time.time()
response_1 = llm.invoke(prompt)
print(f"① 첫 번째 응답: {response_1.content}")
print(f"   (소요 시간: {time.time() - start:.2f}초)")

# 2️⃣ 두 번째 호출 (캐시에서 불러옴)
start = time.time()
response_2 = llm.invoke(prompt)
print(f"② 두 번째 응답: {response_2.content}")
print(f"   (소요 시간: {time.time() - start:.2f}초)")

# 3️⃣ 캐시 히트 여부 판별
if get_llm_cache():
    print("✅ LangChain 전역 캐시 활성화됨")
else:
    print("❌ 캐시 비활성 상태")

print("내용 동일 여부:", response_1.content == response_2.content)
```

> 🧠 **포인트:** 같은 입력이라면 두 번째 호출은 실제 모델을 부르지 않습니다.

---

### ✅ (2) SQLiteCache 예시

```python
import time
from langchain.globals import set_llm_cache, get_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_openai import ChatOpenAI

# ✅ SQLite 캐시 파일 설정
cache = SQLiteCache(database_path=".langchain_cache.db")
set_llm_cache(cache)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = "서울의 수도는 어디인가요?"

# 1️⃣ 첫 번째 호출 (API 요청 발생)
start = time.time()
response_1 = llm.invoke(prompt)
print(f"① 첫 번째 응답: {response_1.content}")
print(f"   (소요 시간: {time.time() - start:.2f}초)")

# 2️⃣ 두 번째 호출 (캐시에서 불러옴)
start = time.time()
response_2 = llm.invoke(prompt)
print(f"② 두 번째 응답: {response_2.content}")
print(f"   (소요 시간: {time.time() - start:.2f}초)")

# 3️⃣ 캐시 확인
if get_llm_cache():
    print("✅ LangChain 전역 캐시 활성화됨")
else:
    print("❌ 캐시 비활성 상태")

print("내용 동일 여부:", response_1.content == response_2.content)

# 4️⃣ SQLite 파일 확인 안내
print("\n🗄️ '.langchain_cache.db' 파일이 현재 디렉토리에 생성되었습니다.")
print("   이 파일을 열어보면 동일한 프롬프트가 캐시에 저장된 것을 확인할 수 있습니다.")
```

> ✅ `.langchain_cache.db` 파일이 생성되어 결과가 저장됩니다.

---

## 4. LangChain 캐시의 동작 원리

1️⃣ 입력(프롬프트)을 문자열로 변환 →  
2️⃣ 해당 문자열을 해시(Hash) 처리 →  
3️⃣ 캐시 저장소(InMemory / SQLite / Redis)에 Key-Value 형태로 저장 →  
4️⃣ 동일한 입력이 들어오면 저장된 결과를 즉시 반환

📊 **흐름 요약:**
```
입력 → 해시 생성 → 캐시 확인 → 결과 반환 (있으면 스킵, 없으면 LLM 호출)
```

---

## 5. 고급 사용법: 사용자 정의 캐시

직접 커스텀 캐시를 구현하려면 `BaseCache` 클래스를 상속합니다.

```python
from langchain.globals import set_llm_cache
from langchain_core.caches import BaseCache
from langchain_openai import ChatOpenAI

# 🧩 1️⃣ BaseCache를 상속받아 나만의 캐시 클래스 정의
class MyCache(BaseCache):
    def __init__(self):
        self.data = {}

    def lookup(self, prompt, llm_string):
        key = (prompt, llm_string)
        value = self.data.get(key)
        if value:
            print(f"✅ 캐시 히트! → {key}")
        else:
            print(f"❌ 캐시 미스! → {key}")
        return value

    def update(self, prompt, llm_string, value):
        key = (prompt, llm_string)
        self.data[key] = value
        print(f"💾 캐시 저장 완료 → {key}")

    def clear(self):
        """캐시 전체를 초기화하는 메서드"""
        self.data.clear()
        print("🧹 캐시 전체 초기화 완료")

# 🧠 2️⃣ 전역 캐시로 등록
set_llm_cache(MyCache())

# 🔹 테스트용 LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = "서울의 수도는 어디인가요?"

# 🔸 첫 번째 호출 → API 요청 + 캐시에 저장
response_1 = llm.invoke(prompt)
print("① 응답:", response_1.content)

# 🔸 두 번째 호출 → 캐시에서 불러옴
response_2 = llm.invoke(prompt)
print("② 응답:", response_2.content)

# 🔸 캐시 작동 여부 확인
print("내용 동일 여부:", response_1.content == response_2.content)
```

> ⚙️ 이 방식으로 로컬 파일, 데이터베이스, Redis 등 원하는 저장소를 자유롭게 연결할 수 있습니다.

---

## 6. 캐싱의 효과

| 항목 | 캐싱 사용 전 | 캐싱 사용 후 |
|------|----------------|----------------|
| API 호출 횟수 | 100회 | 10회 |
| 평균 응답 속도 | 느림 (1~2초) | 빠름 (0.1초 내외) |
| 비용 | 높음 | 절감 |

✅ **효과:** 반복적인 질문, 동일한 입력, 테스트 환경 등에서 API 비용 절감 효과가 큼.

---

## 7. 정리 요약

| 키워드 | 설명 |
|---------|------|
| **set_llm_cache()** | LangChain 전역 캐시 설정 함수 |
| **InMemoryCache** | 메모리 기반 캐시, 간단한 실습용 |
| **SQLiteCache** | 파일 기반 캐시, 실제 환경에 적합 |
| **RedisCache** | 서버 캐시, 다중 사용자 환경에 적합 |
| **효과** | API 호출 감소, 속도 향상, 비용 절감 |

✅ **한 줄 요약:**  
LangChain의 캐싱 기능은 *같은 질문엔 더 이상 요금이 청구되지 않게 만드는 강력한 절약 장치*입니다.
