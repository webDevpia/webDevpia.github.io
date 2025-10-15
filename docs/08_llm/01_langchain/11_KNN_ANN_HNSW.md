---
title: 11. KNN, ANN, HNSW
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 11
permalink: /llm/langchain/knn-ann-hnsw
---

# KNN, ANN, HNSW 이해하기

벡터 검색은 **텍스트·이미지 등 비정형 데이터를 수치 벡터로 변환해 유사도를 기반으로 검색하는 기술**입니다. 이는 기존의 키워드 기반 검색과 달리, **의미적으로 유사한 문장을 찾아주는 “의미 검색(Semantic Search)”**을 가능하게 합니다.

---

## 1️⃣ 벡터 검색이란?

| 구분 | 키워드 검색 | 벡터 검색 |
|------|---------------|------------|
| 기준 | 단어 일치 | 의미적 유사도 (cosine similarity 등) |
| 예시 | “AI 강의” → AI 포함된 문서 | “인공지능 교육” → 의미적으로 유사한 문서 |
| 핵심 기술 | TF-IDF, BM25 | Embedding, Vector Similarity |

> 💡 **비유:** 키워드 검색은 “정확히 같은 단어를 찾는 것”, 벡터 검색은 “비슷한 뜻을 가진 친구를 찾는 것”입니다.

---

## 2️⃣ KNN (K-Nearest Neighbors)

> **KNN은 ‘모든 점과의 거리를 직접 계산’하여 가장 가까운 K개를 찾는 방식입니다.**

### 🔹 동작 원리
1. 쿼리 벡터를 하나 받음.
2. 데이터셋의 모든 벡터와 거리 계산 (L2 거리 또는 코사인 유사도).
3. 거리순으로 정렬하여 상위 K개 반환.

```python
from sklearn.neighbors import NearestNeighbors
import numpy as np

X = np.random.random((100, 5))  # 100개의 5차원 벡터
query = np.random.random((1, 5))

knn = NearestNeighbors(n_neighbors=3, metric="cosine")
knn.fit(X)
distances, indices = knn.kneighbors(query)
print(indices)
```

### ⚖️ 특징
- **정확도:** 100%
- **속도:** 매우 느림 (데이터 전체 비교)
- **적합한 상황:** 소규모 데이터, 실험용, 정확도 최우선인 경우

---

## 3️⃣ ANN (Approximate Nearest Neighbor)

> **ANN은 “속도를 위해 일부 정확도를 희생”하는 근사 최근접 탐색 알고리즘입니다.**

### 🔹 왜 필요할까?
KNN은 1억 개의 벡터가 있을 때 모든 벡터를 비교해야 합니다 → **검색 시간이 너무 오래 걸림.**

ANN은 다음 세 가지 접근으로 이를 개선합니다:

| 유형 | 방식 | 대표 알고리즘 |
|------|------|---------------|
| 해싱 기반 | 비슷한 벡터를 같은 버킷에 저장 | LSH (Locality Sensitive Hashing) |
| 클러스터 기반 | 유사한 벡터끼리 묶어 탐색 | IVF, PQ (FAISS) |
| 그래프 기반 | 벡터 간 연결 관계를 그래프로 표현 | HNSW |

### ⚖️ 특징
- **정확도:** 90~99%
- **속도:** 매우 빠름 (100~1000배 향상)
- **적합한 상황:** 대규모 실시간 검색 서비스

---

## 4️⃣ HNSW (Hierarchical Navigable Small World)

> **HNSW는 그래프 기반 ANN 알고리즘으로, 현재 가장 널리 사용되는 방식입니다.**

### 🔹 핵심 아이디어
벡터를 **계층적 그래프(hierarchical graph)**로 구성하여, **멀리서 시작해 점점 가까운 이웃으로 탐색**합니다.

```
Level 3: ●───●
           │   \
Level 2:  ●──●──●
           │   │
Level 1: ●──●──●──●──●
```

- **상위 레벨:** 전체 공간을 거칠게 훑음 (빠른 시작점 탐색)
- **하위 레벨:** 세밀한 지역 탐색 (정확한 최근접 검색)

### 🔹 주요 파라미터
| 파라미터 | 설명 | 권장값 |
|-----------|------|--------|
| `M` | 각 노드가 연결할 최대 이웃 수 | 16~64 |
| `efConstruction` | 인덱스 구축 시 탐색 폭 | 100~200 |
| `efSearch` | 검색 시 탐색 폭 | 50~100 |

### ⚙️ 코드 예시 (FAISS)

```python
import faiss
import numpy as np

# 128차원 벡터 10만 개
data = np.random.random((100000, 128)).astype('float32')

index = faiss.IndexHNSWFlat(128, 32)  # HNSW 인덱스 생성
index.hnsw.efConstruction = 200
index.add(data)

query = np.random.random((1, 128)).astype('float32')
D, I = index.search(query, 5)
print(I)
```

---

## 5️⃣ KNN, ANN, HNSW 비교표

| 항목 | KNN | ANN | HNSW |
|------|-----|-----|------|
| **정확도** | 100% | 90~99% | 95~99% |
| **속도** | 매우 느림 | 빠름 | 매우 빠름 |
| **메모리 사용량** | 적음 | 중간 | 많음 |
| **인덱스 필요** | ❌ | ✅ | ✅ |
| **적합한 규모** | 소규모 | 중~대규모 | 대규모 (100만+) |
| **대표 구현체** | scikit-learn | FAISS, ScaNN | FAISS, Milvus, Pinecone |

---

## 6️⃣ LangChain + Pinecone 연동 예시

```python
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import os

# 1. Pinecone 클라이언트 설정
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# 2. 임베딩 모델 설정
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 3. 벡터스토어 생성
index_name = "semantic-search-demo"
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

# 4. 질의 및 검색
query = "인공지능의 윤리적 문제는?"
docs = vectorstore.similarity_search(query, k=3)

for i, doc in enumerate(docs, 1):
    print(f"{i}. {doc.page_content}")
```

> ✅ LangChain은 내부적으로 HNSW 기반의 ANN 검색을 수행합니다.  
> Pinecone, Weaviate, FAISS 모두 HNSW 인덱스를 기반으로 빠른 의미 검색을 지원합니다.

---

## 7️⃣ 실무 선택 가이드

| 상황 | 추천 알고리즘 | 이유 |
|------|----------------|------|
| 데이터가 작고 정확도가 중요 | **KNN** | 구현 단순, 100% 정확도 |
| 대규모 데이터, 실시간 검색 | **ANN (HNSW)** | 빠른 검색 속도, 확장성 높음 |
| GPU 사용 환경, 벡터 압축 필요 | **FAISS IVF+PQ** | 고차원 벡터 효율적 관리 |
| 클라우드 환경 (SaaS) | **Pinecone, Milvus, Weaviate** | 관리형 벡터 데이터베이스 |

---

## 💬 정리
- **KNN** → 정확하지만 느림. (모든 점과 거리 계산)
- **ANN** → 빠르지만 근사값 사용. (정확도 약간 손실)
- **HNSW** → 그래프 기반 ANN으로 현재 가장 많이 사용됨.

> 💡 **요약:**  
> HNSW는 “빠른 근사 이웃 검색의 사실상 표준 알고리즘”으로,  
> LangChain, Pinecone, FAISS 등 대부분의 최신 LLM 검색 엔진이 채택하고 있습니다.
