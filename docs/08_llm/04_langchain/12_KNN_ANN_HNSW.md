---
title: 12. KNN, ANN, HNSW
layout: default
grand_parent: LLM
parent: LangChain
nav_order: 12
permalink: /llm/langchain/knn-ann-hnsw
---


## 학습 목표

- KNN, ANN, HNSW 알고리즘의 차이를 설명할 수 있다
- FAISS를 사용한 벡터 검색을 구현할 수 있다

<a id="toc"></a>

## 진행 순서

1. [벡터 검색이란?](#part1) - 의미 검색 개념과 벡터 공간 이해
2. [최근접 탐색 (KNN)](#part2) - 전수 거리 계산 방식과 거리 척도
3. [근사 최근접 탐색 (ANN)](#part3) - 속도와 정확도의 트레이드오프 및 대표 알고리즘
4. [HNSW](#part4) - 그래프 기반 ANN 알고리즘과 FAISS 실습


---

# KNN, ANN, HNSW 이해하기

> 11장에서 Pinecone으로 벡터 검색을 체험해 보았습니다. "내부적으로 어떻게 가장 비슷한 벡터를 찾아내는 걸까?" 이 장에서는 그 원리를 알아봅니다.

벡터 검색은 **텍스트·이미지 등 비정형 데이터를 수치 벡터로 변환해 유사도를 기반으로 검색하는 기술**입니다. 이는 기존의 키워드 기반 검색과 달리, **의미적으로 유사한 문장을 찾아주는 "의미 검색(Semantic Search)"**을 가능하게 합니다.

> **비유로 이해하기**: 도서관에서 책을 찾을 때, 키워드 검색은 "제목에 '요리'가 들어간 책"을 찾는 것이고, 벡터 검색은 "맛있는 음식 만드는 방법에 대한 책"처럼 의미가 비슷한 책을 찾아주는 것입니다.

---

<a id="part1"></a>

## 1️⃣ 벡터 검색이란? [↑](#toc)

벡터 공간에 여러 개의 점(=데이터)이 있을 때,
어떤 쿼리 벡터에 가장 가까운 점을 찾는 것을 말합니다.

---

<a id="part2"></a>

## 2️⃣ 최근접 탐색 (KNN : K-Nearest Neighbors) [↑](#toc)

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

<a id="part3"></a>

## 3️⃣ 근사 최근접 탐색 (ANN : Approximate Nearest Neighbor) [↑](#toc)

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

<a id="part4"></a>

## 4️⃣ HNSW (Hierarchical Navigable Small World) [↑](#toc)

> **HNSW는 그래프 기반 ANN 알고리즘으로, 현재 가장 널리 사용되는 방식입니다.**

- 상위 레벨: 대표 벡터 (적게 존재)
- 하위 레벨: 실제 모든 데이터 (가득 존재)

> **비유: 고속도로 → 국도 → 골목길**
> HNSW의 계층 탐색은 길 찾기와 비슷합니다. 먼저 **고속도로(상위 레벨)**에서 대략적인 방향을 잡고, **국도(중간 레벨)**에서 좁혀가며, 마지막으로 **골목길(최하위 레벨)**에서 정확한 목적지를 찾습니다. 상위 레벨에서는 멀리 떨어진 노드끼리 연결되어 있어 빠르게 이동하고, 하위 레벨에서는 가까운 노드끼리 연결되어 있어 정밀하게 탐색합니다.

### ⚙️ 코드 예시 (FAISS)

> ⚠️ 참고
    FAISS는 내부적으로 "거리(distance)"를 반환합니다.  
    즉, 값이 작을수록 더 유사함을 의미합니다.  
    (Cosine Similarity가 아닌 L2 거리 기반이기 때문.)  

```bash
# uv 사용 시
uv add faiss-cpu
```

```py
# ─── 필요한 라이브러리(도구 모음)들을 불러옵니다 ───
import faiss                                          # Facebook이 만든 초고속 벡터 검색 라이브러리
from langchain_openai import OpenAIEmbeddings         # 텍스트를 숫자 벡터로 변환해주는 OpenAI 임베딩 도구
from langchain_community.vectorstores import FAISS    # LangChain에서 FAISS를 편리하게 쓸 수 있도록 감싼 클래스
from langchain_community.docstore.in_memory import InMemoryDocstore  # 문서를 메모리(RAM)에 임시 저장하는 저장소
from langchain_core.documents import Document         # LangChain의 문서 단위 객체 (내용 + 출처 정보를 함께 담는 그릇)
import numpy as np                                    # 수치 계산용 라이브러리 (벡터를 배열로 다루기 위해 사용)
from dotenv import load_dotenv                        # .env 파일에서 API 키 등 민감한 설정값을 읽어오는 도구

# ─── .env 파일에 저장된 API 키를 환경변수로 등록합니다 ───
# 이 줄이 없으면 OpenAI API 키를 찾지 못해 오류가 납니다
load_dotenv()

# 1️⃣ OpenAI 임베딩 초기화
# "text-embedding-3-small": 텍스트를 1536차원 숫자 배열(벡터)로 바꿔주는 OpenAI 모델
# 이 객체를 통해 이후 모든 텍스트를 벡터로 변환합니다
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 2️⃣ 샘플 문서 생성
# Document: 본문(page_content)과 출처 정보(metadata)를 함께 저장하는 단위
# 나중에 검색 결과로 이 문서들이 반환됩니다
documents = [
    Document(page_content="LangChain을 이용해 AI 프로젝트를 구축 중입니다.", metadata={"source": "tweet"}),
    Document(page_content="내일 날씨는 맑고 따뜻할 예정입니다.", metadata={"source": "news"}),
    Document(page_content="오늘은 팬케이크와 커피를 먹었어요.", metadata={"source": "personal"}),
]

# 3️⃣ 샘플 벡터로 차원(dimension) 확인
# HNSW 인덱스를 만들려면 벡터의 크기(차원 수)를 미리 알아야 합니다
# "hello world"를 벡터로 변환해서 그 길이를 재는 방식으로 차원을 확인합니다
# dtype="float32": FAISS가 요구하는 32비트 실수형으로 변환
sample_vec = np.array(embeddings.embed_query("hello world"), dtype="float32")
dim = len(sample_vec)  # 예: 1536 (text-embedding-3-small 모델의 벡터 크기)

print(f"✅ 벡터 차원: {dim}")

# 4️⃣ HNSW 인덱스(검색 구조물) 생성
# IndexHNSWFlat: 계층적 그래프를 사용하는 HNSW 방식의 FAISS 인덱스
#   - 첫 번째 인자 dim: 벡터 차원 수 (위에서 구한 값)
#   - 두 번째 인자 32: 각 노드(벡터)가 그래프에서 연결할 이웃(neighbor)의 수
#     → 클수록 검색 정확도 ↑, 메모리 사용 ↑ / 작을수록 그 반대
# 이 인덱스가 실제로 빠른 유사도 검색을 담당합니다
index = faiss.IndexHNSWFlat(dim, 32)  # 32개의 neighbor 링크
print("✅ HNSW Index 생성 완료!")

# 5️⃣ LangChain용 VectorStore(벡터 저장소) 초기화
# FAISS 인덱스만으로는 "어떤 벡터가 어떤 문서인지" 알 수 없습니다
# LangChain의 FAISS 클래스가 벡터 인덱스 + 문서 저장소를 연결해줍니다
#   - embedding_function: 텍스트를 벡터로 변환할 때 사용하는 임베딩 객체
#   - index: 위에서 만든 HNSW 검색 구조
#   - docstore: 벡터 ID에 해당하는 원본 문서를 메모리에 저장하는 저장소
#   - index_to_docstore_id: FAISS 내부 정수 번호 → 문서 ID 매핑 테이블 (처음엔 비어 있음)
vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

# 6️⃣ 문서를 벡터로 변환하여 저장소에 추가
# add_documents가 내부적으로: 텍스트 → 벡터 변환 → HNSW 인덱스에 등록 → docstore에 원본 문서 저장
# 이 과정을 거쳐야 비로소 검색이 가능해집니다
# (numpy 직접 사용 X → LangChain이 변환을 알아서 처리)
vector_store.add_documents(documents)
print("✅ 문서가 HNSW 기반 벡터 DB에 추가되었습니다!")

# 7️⃣ 유사도 검색 테스트
# "랭체인"이라는 쿼리를 벡터로 변환한 뒤, 가장 가까운 벡터 3개를 찾습니다
# similarity_search_with_score: 문서와 함께 거리(유사도 점수)를 반환
#   - k=3: 상위 3개 결과를 반환 (K-Nearest Neighbors에서 K에 해당)
# 반환되는 score는 L2 거리 → 값이 작을수록 더 유사한 문서입니다
query = "랭체인"
results = vector_store.similarity_search_with_score(query, k=3)

# 결과 출력: [거리 점수] 문서 내용 (출처 정보)
# 첫 번째 결과가 score가 가장 낮으므로 가장 유사한 문서입니다
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

> **참고: FAISS 저수준 API 설명**
> - `InMemoryDocstore()`: FAISS 인덱스의 벡터 ID와 실제 문서를 매핑하는 메모리 내 저장소입니다. FAISS 자체는 벡터만 저장하므로, 원본 문서 내용을 보관하는 역할을 합니다.
> - `index_to_docstore_id={}`: FAISS 내부의 정수 인덱스를 문서 ID로 변환하는 딕셔너리입니다. 문서가 추가되면 자동으로 채워집니다.
> - 이 두 가지는 `FAISS.from_documents()`를 사용하면 내부적으로 자동 처리되지만, 여기서는 HNSW 인덱스를 직접 지정하기 위해 수동으로 설정합니다.
