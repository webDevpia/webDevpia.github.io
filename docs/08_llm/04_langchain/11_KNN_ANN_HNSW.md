---
title: 11. KNN, ANN, HNSW
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 11
permalink: /llm/langchain/knn-ann-hnsw
---


## 학습 목표

- KNN, ANN, HNSW 알고리즘의 차이를 설명할 수 있다
- FAISS를 사용한 벡터 검색을 구현할 수 있다

<a id="toc"></a>

## 진행 순서

1. [벡터 검색이란?](#벡터-검색이란) - 의미 검색 개념과 벡터 공간 이해
2. [최근접 탐색 (KNN)](#최근접-탐색-knn--k-nearest-neighbors) - 전수 거리 계산 방식과 거리 척도
3. [근사 최근접 탐색 (ANN)](#근사-최근접-탐색-ann--approximate-nearest-neighbor) - 속도와 정확도의 트레이드오프 및 대표 알고리즘
4. [HNSW](#hnsw-hierarchical-navigable-small-world) - 그래프 기반 ANN 알고리즘과 FAISS 실습


---

# KNN, ANN, HNSW 이해하기

벡터 검색은 **텍스트·이미지 등 비정형 데이터를 수치 벡터로 변환해 유사도를 기반으로 검색하는 기술**입니다. 이는 기존의 키워드 기반 검색과 달리, **의미적으로 유사한 문장을 찾아주는 "의미 검색(Semantic Search)"**을 가능하게 합니다.

> **비유로 이해하기**: 도서관에서 책을 찾을 때, 키워드 검색은 "제목에 '요리'가 들어간 책"을 찾는 것이고, 벡터 검색은 "맛있는 음식 만드는 방법에 대한 책"처럼 의미가 비슷한 책을 찾아주는 것입니다.

---

## 1️⃣ 벡터 검색이란?

벡터 공간에 여러 개의 점(=데이터)이 있을 때,
어떤 쿼리 벡터에 가장 가까운 점을 찾는 것을 말합니다.

---

## 2️⃣ 최근접 탐색 (KNN : K-Nearest Neighbors)

> **KNN은 '모든 점과의 거리를 직접 계산'하여 가장 가까운 K개를 찾는 방식입니다.**

| ID | 임베딩(embedding) |
|----|-------------------|
| A  | [0.1, 0.2, 0.8]   |
| B  | [0.2, 0.1, 0.7]   |
| C  | [0.9, 0.8, 0.2]   |

→ 쿼리 [0.1, 0.3, 0.7] 에 가장 가까운 벡터 찾기

이때 사용하는 대표 거리 척도:
- **L2 거리(Euclidean)** → 두 점 사이의 직선 거리. 지도에서 두 장소 사이의 직선 거리를 재는 것과 같습니다
- **Cosine Similarity** → 두 벡터가 가리키는 방향이 얼마나 비슷한지. 1에 가까울수록 유사합니다


벡터가 수백만 개라면,
하나하나 거리 계산(L2 or Cosine)하는 데 시간이 너무 오래 걸립니다.
이때 등장하는 개념이 바로 ANN (Approximate Nearest Neighbor)

---

## 3️⃣ 근사 최근접 탐색 (ANN : Approximate Nearest Neighbor)

> **"정확히 가장 가까운 벡터를 찾지 않아도 되니까,대신 빠르게 '거의 비슷한 것'을 찾아줘!"**

즉,
- 정확도(Accuracy) 를 약간 포기하는 대신
- 속도(Speed) 를 엄청나게 높이는 방법입니다.


**대표 알고리즘**

| 알고리즘 | 핵심 구조 | 특징 |
|----------|-----------|------|
| HNSW (Hierarchical Navigable Small World) | 그래프 기반 | 정확도 높고 빠름 (요즘 가장 많이 사용됨) |
| IVF (Inverted File Index) | 군집 기반 | 대용량에서도 빠름 |
| PQ (Product Quantization) | 압축 기반 | 메모리 절약 |
| LSH (Locality Sensitive Hashing) | 해시 기반 | 고차원에서도 빠름, 다만 정확도 낮음 |

**HNSW 예시 (가장 인기 있는 방식)**

FAISS, Pinecone, Weaviate, Milvus 등 대부분의 벡터 DB는 HNSW 방식을 사용합니다.

---

## 4️⃣ HNSW (Hierarchical Navigable Small World)

> **HNSW는 그래프 기반 ANN 알고리즘으로, 현재 가장 널리 사용되는 방식입니다.**

- 상위 레벨: 대표 벡터 (적게 존재)
- 하위 레벨: 실제 모든 데이터 (가득 존재)


### ⚙️ 코드 예시 (FAISS)

> ⚠️ 참고
    FAISS는 내부적으로 "거리(distance)"를 반환합니다.  
    즉, 값이 작을수록 더 유사함을 의미합니다.  
    (Cosine Similarity가 아닌 L2 거리 기반이기 때문.)  

```bash
conda install -c pytorch faiss-cpu
```

```py
import faiss
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document
import numpy as np
from dotenv import load_dotenv

# 환경변수 불러오기
load_dotenv()

# 1️⃣ OpenAI 임베딩 초기화
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 2️⃣ 샘플 문서 생성
documents = [
    Document(page_content="LangChain을 이용해 AI 프로젝트를 구축 중입니다.", metadata={"source": "tweet"}),
    Document(page_content="내일 날씨는 맑고 따뜻할 예정입니다.", metadata={"source": "news"}),
    Document(page_content="오늘은 팬케이크와 커피를 먹었어요.", metadata={"source": "personal"}),
]

# 3️⃣ 샘플 벡터로 차원 확인
sample_vec = np.array(embeddings.embed_query("hello world"), dtype="float32")
dim = len(sample_vec)

print(f"✅ 벡터 차원: {dim}")

# 4️⃣ HNSW 인덱스 생성
index = faiss.IndexHNSWFlat(dim, 32)  # 32개의 neighbor 링크
print("✅ HNSW Index 생성 완료!")

# 5️⃣ LangChain용 VectorStore 초기화
vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

# 6️⃣ 문서 추가 (numpy 직접 사용 X)
vector_store.add_documents(documents)
print("✅ 문서가 HNSW 기반 벡터 DB에 추가되었습니다!")

# 7️⃣ 검색 테스트
query = "랭체인"
results = vector_store.similarity_search_with_score(query, k=3)

print("\n🔍 검색 결과:")
for r,score in results:
    print(f"•[{score:.6f}] {r.page_content} ({r.metadata})")
```

```
✅ 벡터 차원: 1536
✅ HNSW Index 생성 완료!
✅ 문서가 HNSW 기반 벡터 DB에 추가되었습니다!

🔍 검색 결과:
•[1.494898] LangChain을 이용해 AI 프로젝트를 구축 중입니다. ({'source': 'tweet'})
•[1.737423] 오늘은 팬케이크와 커피를 먹었어요. ({'source': 'personal'})
•[1.787256] 내일 날씨는 맑고 따뜻할 예정입니다. ({'source': 'news'})
```
