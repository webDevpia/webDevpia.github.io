# RAG 학습 시리즈 (11~15장) 교육 콘텐츠 개선 계획

**작성일:** 2026-04-07
**대상 파일:** 6개 (11장, 12장, 13장, 14장, 14_2장, 15장)
**우선순위:** P0 → P1 → P2 → P3 순서로 진행

---

## Task 1: P0 즉시 수정 사항 (작업량: 소)

### 1-1. 13장 — 검색 결과 순서 오류 및 score 의미 명확화

**파일:** `docs/08_llm/04_langchain/13.임베딩 모델과 인덱스 구축.md`
**위치:** 7장 "임베딩 생성 및 Pinecone 업서트" 하단의 검색 결과 출력 부분 (라인 236~257)

**현재 문제:**
- "가난과 부유함의 차이를 다룬 영화" 쿼리에서 기생충(0.6398)이 응답하라 1988(0.2984)보다 뒤에 출력됨
- Pinecone은 코사인 유사도를 사용하므로 높을수록 유사한데, 결과 순서가 뒤집혀 있음
- "유사도 점수"라고 표기했으나 순서가 오름차순으로 되어 있어 독자가 혼란스러움

**수정 내용:**
1. 검색 결과 출력 순서를 **유사도 내림차순으로** 수정 (기생충 먼저, 응답하라 1988 나중에)
2. year 출력에서 `2015.0` → `2015`, `2019.0` → `2019`로 변경 (P3 #15 포함 처리)
3. 검색 결과 앞에 score 해석 안내 추가

**수정 전:**
```
🔍 검색 결과:
🎬 응답하라 1988 (2015.0)
💬 1988년 서울 쌍문동 이웃들의 우정과 가족애를 그린 드라마.
🔢 유사도 점수: 0.2984

🎬 기생충 (2019.0)
💬 가난한 가족과 부유한 가족의 계급 격차를 다룬 영화.
🔢 유사도 점수: 0.6398
```

**수정 후:**
```
🔍 검색 결과:
🎬 기생충 (2019)
💬 가난한 가족과 부유한 가족의 계급 격차를 다룬 영화.
🔢 유사도 점수: 0.6398

🎬 응답하라 1988 (2015)
💬 1988년 서울 쌍문동 이웃들의 우정과 가족애를 그린 드라마.
🔢 유사도 점수: 0.2984
```

검색 결과 출력 코드 블록의 `doc.metadata['year']` 부분도 `int(doc.metadata['year'])`로 수정:
```python
print(f"🎬 {doc.metadata['title']} ({int(doc.metadata['year'])})")
```

검색 결과 블록 바로 위에 설명 추가:
```markdown
> 💡 Pinecone의 코사인 유사도(cosine similarity)는 **값이 클수록 더 유사**합니다 (0~1 범위). 아래 결과에서 기생충(0.6398)이 응답하라 1988(0.2984)보다 높으므로 쿼리와 더 유사합니다.
```

**검증 기준:** 기생충이 먼저 출력되고, score 해석 안내가 추가되었는지 확인

---

### 1-2. gpt-4o-mini → gpt-4.1-mini 모델명 업데이트

**대상 파일 및 위치:**

| 파일 | 수정 위치 | 현재 값 | 변경 값 |
|------|-----------|---------|---------|
| `14_2장` 라인 263 | `ChatOpenAI(model="gpt-4o-mini"...)` | `gpt-4o-mini` | `gpt-4.1-mini` |
| `14_2장` 라인 581 | `ChatOpenAI(model="gpt-4o-mini"...)` (Streamlit) | `gpt-4o-mini` | `gpt-4.1-mini` |
| `15장` 라인 47 | 프로젝트 개요 본문 "GPT-4o-mini" | `GPT-4o-mini` | `GPT-4.1-mini` |
| `15장` 라인 62~66 | 서비스 시나리오 본문 "GPT-4o-mini" (2회) | `GPT-4o-mini` | `GPT-4.1-mini` |
| `15장` 라인 85 | 외부 서비스 "GPT-4o-mini" | `GPT-4o-mini` | `GPT-4.1-mini` |
| `15장` 라인 108 | 모델 목록 "gpt-4o-mini" | `gpt-4o-mini` | `gpt-4.1-mini` |
| `15장` 라인 122 | .env 예시 `OPENAI_LLM_MODEL=gpt-4o-mini` | `gpt-4o-mini` | `gpt-4.1-mini` |
| `15장` 라인 193 | step1 .env 예시 `gpt-4o-mini` | `gpt-4o-mini` | `gpt-4.1-mini` |
| `15장` 라인 601 | `sommelier.py` default값 `"gpt-4o-mini"` | `gpt-4o-mini` | `gpt-4.1-mini` |

**수정 방법:** 각 파일에서 `gpt-4o-mini` 를 `gpt-4.1-mini`로 일괄 교체 (replace_all)

**검증 기준:** 모든 파일에서 `gpt-4o-mini` 검색 시 0건

---

### 1-3. 15장 — st.image deprecated 파라미터 교체

**파일:** `docs/08_llm/04_langchain/15.AI 소믈리에 RAG 서비스 프로젝트.md`
**위치:** `app.py` 코드 블록 내 라인 709

**수정 전:**
```python
st.image(uploaded_image, caption="업로드된 요리 이미지", use_container_width=True)
```

**수정 후:**
```python
st.image(uploaded_image, caption="업로드된 요리 이미지", width="stretch")
```

**검증 기준:** `use_container_width` 문자열이 파일에서 사라졌는지 확인

---

## Task 2: P1 품질 개선 (작업량: 중)

### 2-1. 15장 — 난이도 완화

**파일:** `docs/08_llm/04_langchain/15.AI 소믈리에 RAG 서비스 프로젝트.md`

#### (A) 학습 목표 장번호 수정 (라인 14)

**수정 전:**
```markdown
- 10~13장에서 배운 임베딩, 벡터 검색을 실전 프로젝트에 적용할 수 있다
```

**수정 후:**
```markdown
- 11~14장에서 배운 임베딩, 벡터 검색을 실전 프로젝트에 적용할 수 있다
```

#### (B) 신규 개념 설명 추가

step2 섹션 시작 부분(라인 358~359 사이)에 아래 개념 설명 박스 추가:

```markdown
> **이 단계에서 처음 등장하는 개념 정리**
>
> | 개념 | 설명 |
> |------|------|
> | **base64** | 이미지를 텍스트 문자열로 인코딩하는 방식입니다. API로 이미지를 전송할 때 바이너리 대신 base64 문자열을 사용합니다. |
> | **CSVLoader** | LangChain이 제공하는 CSV 파일 로더입니다. CSV의 각 행을 하나의 `Document` 객체로 변환합니다. |
> | **RunnableLambda** | 일반 Python 함수를 LangChain의 체인(chain)에 연결할 수 있도록 감싸는 래퍼입니다. `함수A | 함수B` 형태로 파이프라인을 구성할 수 있게 합니다. |
> | **tiktoken** | OpenAI가 만든 토크나이저 라이브러리입니다. 텍스트가 몇 개의 토큰으로 변환되는지 계산하여 비용을 예측할 수 있습니다. |
> | **HumanMessagePromptTemplate** | 멀티모달 입력(텍스트+이미지)을 포함하는 프롬프트 템플릿입니다. 텍스트와 이미지를 함께 LLM에 전달할 때 사용합니다. |
> | **Vision LLM** | 이미지를 입력으로 받아 분석할 수 있는 LLM입니다. GPT-4.1-mini는 텍스트와 이미지를 모두 처리할 수 있는 멀티모달 모델입니다. |
```

#### (C) 13만건 업로드 예상 시간/비용 안내

step1의 배치 업서트 코드(라인 320~341) 바로 위에 추가:

```markdown
> **참고: 129,971건 전체 업로드 예상**
> - **시간:** 배치 300건 기준 약 430회 반복, 네트워크 상태에 따라 30분~1시간 소요
> - **비용:** `text-embedding-3-small` 기준 약 $0.02~0.05 (토큰 수에 따라 변동)
> - 처음 실행 시 시간이 오래 걸리므로, 이미 업로드한 인덱스가 있다면 이 단계를 건너뛸 수 있습니다
```

#### (D) step1/step2 파일 구조 명시

step1 시작(라인 186~188) 바로 뒤에 추가:

```markdown
> **파일 구조 안내**
> - **step1**: Jupyter Notebook 또는 단일 `.py` 파일에서 진행합니다. 데이터 로드, 임베딩 생성, Pinecone 업서트까지 수행합니다.
> - **step2**: step1과 같은 환경에서 이어서 진행합니다. 함수 정의와 체인 구성을 학습합니다.
> - **최종 프로젝트**: `sommelier.py`(백엔드) + `app.py`(Streamlit UI) 두 파일로 분리합니다.
```

#### (E) describe_dish_flavor / recommend_dishes 함수 패턴 통일

step2의 `recommend_dishes` 함수(라인 383~416)와 `describe_dish_flavor` 함수(라인 447~474) 모두 `chain`을 반환하는 패턴인데, 최종 `sommelier.py`에서는 `chain.invoke({})`로 결과를 직접 반환합니다.

step2 함수들의 `return chain` 부분 뒤에 안내 추가:

```markdown
> **참고:** 여기서는 학습 목적으로 `chain`을 반환하여 `RunnableLambda`로 연결하는 패턴을 사용합니다. 최종 `sommelier.py`에서는 함수 안에서 `chain.invoke({})`를 호출하여 결과 문자열을 직접 반환하는, 더 간결한 패턴으로 변경됩니다.
```

**검증 기준:** 장번호 참조가 "11~14장"으로 수정되었고, 개념 설명 표와 안내 문구가 추가되었는지 확인

---

### 2-2. 12장 — 개선

**파일:** `docs/08_llm/04_langchain/12_KNN_ANN_HNSW.md`

#### (A) 장 서두 동기 부여 문장 (라인 29 아래)

**수정 전:**
```markdown
벡터 검색은 **텍스트·이미지 등 비정형 데이터를 수치 벡터로 변환해 유사도를 기반으로 검색하는 기술**입니다.
```

**수정 후:**
```markdown
> 11장에서 Pinecone으로 벡터 검색을 체험해 보았습니다. "내부적으로 어떻게 가장 비슷한 벡터를 찾아내는 걸까?" 이 장에서는 그 원리를 알아봅니다.

벡터 검색은 **텍스트·이미지 등 비정형 데이터를 수치 벡터로 변환해 유사도를 기반으로 검색하는 기술**입니다.
```

#### (B) HNSW 계층 탐색 비유 추가 (라인 100~103 사이)

현재:
```markdown
- 상위 레벨: 대표 벡터 (적게 존재)
- 하위 레벨: 실제 모든 데이터 (가득 존재)
```

수정 후:
```markdown
- 상위 레벨: 대표 벡터 (적게 존재)
- 하위 레벨: 실제 모든 데이터 (가득 존재)

> **비유: 고속도로 → 국도 → 골목길**
> HNSW의 계층 탐색은 길 찾기와 비슷합니다. 먼저 **고속도로(상위 레벨)**에서 대략적인 방향을 잡고, **국도(중간 레벨)**에서 좁혀가며, 마지막으로 **골목길(최하위 레벨)**에서 정확한 목적지를 찾습니다. 상위 레벨에서는 멀리 떨어진 노드끼리 연결되어 있어 빠르게 이동하고, 하위 레벨에서는 가까운 노드끼리 연결되어 있어 정밀하게 탐색합니다.
```

#### (C) FAISS 설치 방법 추가 (라인 113~115)

**수정 전:**
```bash
conda install -c pytorch faiss-cpu
```

**수정 후:**
```bash
# conda 사용 시
conda install -c pytorch faiss-cpu

# pip 사용 시
pip install faiss-cpu

# uv 사용 시
uv add faiss-cpu
```

#### (D) InMemoryDocstore, index_to_docstore_id 설명 추가 (라인 149~155 부근)

현재 코드에서 `InMemoryDocstore()`와 `index_to_docstore_id={}`가 설명 없이 사용됩니다. 코드 블록 바로 아래에 설명 추가:

```markdown
> **참고: FAISS 저수준 API 설명**
> - `InMemoryDocstore()`: FAISS 인덱스의 벡터 ID와 실제 문서를 매핑하는 메모리 내 저장소입니다. FAISS 자체는 벡터만 저장하므로, 원본 문서 내용을 보관하는 역할을 합니다.
> - `index_to_docstore_id={}`: FAISS 내부의 정수 인덱스를 문서 ID로 변환하는 딕셔너리입니다. 문서가 추가되면 자동으로 채워집니다.
> - 이 두 가지는 `FAISS.from_documents()`를 사용하면 내부적으로 자동 처리되지만, 여기서는 HNSW 인덱스를 직접 지정하기 위해 수동으로 설정합니다.
```

**검증 기준:** 동기 부여 문장, HNSW 비유, 설치 방법 3가지, 저수준 API 설명이 모두 추가되었는지 확인

---

### 2-3. 13장 → 14장 데이터 연속성 안내

**파일:** `docs/08_llm/04_langchain/14.벡터 검색.md`
**위치:** 라인 30 (제목 바로 아래)

추가:
```markdown
> **참고:** 이 장에서는 13장과는 다른 인덱스(`movie-vector-index`)와 더 많은 영화 데이터(7편)를 사용합니다. 13장에서 만든 `movie-index`는 기본 개념 학습용이었고, 이 장에서는 다양한 검색 방법을 실습하기 위해 새로운 데이터로 시작합니다.
```

### 2-4. 13장 .env에서 PINECONE_ENVIRONMENT 제거

**파일:** `docs/08_llm/04_langchain/13.임베딩 모델과 인덱스 구축.md`
**위치:** 라인 78~82

**수정 전:**
```
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=us-east-1-aws
```

**수정 후:**
```
OPENAI_API_KEY=본인의_OpenAI_API키
PINECONE_API_KEY=본인의_Pinecone_API키
```

추가 안내:
```markdown
> 💡 11장에서 설명한 것처럼, `PINECONE_ENVIRONMENT`는 Serverless 인덱스에서는 불필요합니다.
```

### 2-5. Pinecone 초기화 코드 통일 (13장)

**파일:** `docs/08_llm/04_langchain/13.임베딩 모델과 인덱스 구축.md`
**위치:** 라인 92~118

**수정 전:**
```python
import pinecone, os
from dotenv import load_dotenv

# ...
pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# ...
        spec=pinecone.ServerlessSpec(
```

**수정 후:**
```python
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import os

# ...
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# ...
        spec=ServerlessSpec(
```

이렇게 하면 11장, 14장, 14_2장, 15장과 동일한 `from pinecone import Pinecone, ServerlessSpec` 패턴이 됩니다.

**검증 기준:** 13장에서 `import pinecone` 패턴이 사라지고 `from pinecone import Pinecone, ServerlessSpec`으로 통일되었는지 확인

---

## Task 3: P2 콘텐츠 보강 (작업량: 중)

### 3-1. 유사도 점수 해석 가이드 비교표

**파일:** `docs/08_llm/04_langchain/14.벡터 검색.md`
**위치:** 6장 "실습 요약" 앞 (라인 235~236 사이)

추가:
```markdown
---

### 유사도 점수 해석 가이드

VectorDB마다 반환하는 점수의 의미가 다르므로 주의가 필요합니다.

| VectorDB | 점수 종류 | 범위 | 해석 |
|----------|-----------|------|------|
| **Pinecone** (cosine) | 코사인 유사도 | 0 ~ 1 | **높을수록 유사** (1 = 완전 일치) |
| **Pinecone** (dotproduct) | 내적 | -1 ~ 1 | **높을수록 유사** |
| **FAISS** (기본 Flat/HNSW) | L2 거리 | 0 ~ ∞ | **낮을수록 유사** (0 = 완전 일치) |

> 이 실습에서 Pinecone은 `metric="cosine"`으로 생성했으므로, **점수가 높을수록 더 유사한 결과**입니다.
> 반면 12장에서 사용한 FAISS는 L2 거리를 반환하므로, **값이 작을수록 더 유사**합니다.
```

### 3-2. 비용 안내 추가

**파일:** `docs/08_llm/04_langchain/11.검색 증강 생성(RAG) 개요 및 VectorDB, 임베딩 모델.md`
**위치:** 임베딩 모델 섹션 말미, 라인 142 뒤

추가:
```markdown
> **비용 참고 (2026년 기준)**
> - **OpenAI 임베딩:** `text-embedding-3-small`은 100만 토큰당 약 $0.02로 매우 저렴합니다
> - **Pinecone 무료 티어:** 인덱스 5개까지, 총 벡터 수 제한이 있으므로 실습 후 불필요한 인덱스는 삭제하는 것을 권장합니다
> - **비용 비교:** 임베딩 비용보다 LLM 호출 비용이 훨씬 높으므로, 임베딩 비용은 크게 걱정하지 않아도 됩니다
```

### 3-3. 텍스트 분할(Chunking) 설명 보강

**파일:** `docs/08_llm/04_langchain/11.검색 증강 생성(RAG) 개요 및 VectorDB, 임베딩 모델.md`
**위치:** Indexing 설명 (라인 86~91) 뒤, Part 3 시작 전

추가:
```markdown
> **청크 분할(Chunking)이란?**
> 긴 문서를 통째로 임베딩하면 의미가 희석되어 검색 정확도가 떨어집니다. 그래서 문서를 적절한 크기의 조각(청크)으로 나누는 과정이 필요합니다. 예를 들어 100페이지 PDF를 500자씩 잘라서 각각 임베딩하면, "3장의 내용"을 정확히 검색할 수 있습니다. 이 실습에서는 짧은 문장을 사용하므로 분할이 필요 없지만, 실제 서비스에서는 반드시 고려해야 하는 단계입니다.
```

### 3-4. "차원"에 대한 직관적 설명

**파일:** `docs/08_llm/04_langchain/11.검색 증강 생성(RAG) 개요 및 VectorDB, 임베딩 모델.md`
**위치:** 임베딩 모델 표 아래 (라인 138 뒤)

추가:
```markdown
> **"1536차원"이란?**
> 차원이란 문장의 의미를 표현하는 숫자의 개수입니다. `text-embedding-3-small`이 1536차원이라는 것은, 하나의 문장을 1536개의 숫자로 표현한다는 뜻입니다. 마치 사람을 설명할 때 "키, 몸무게, 나이, ..."처럼 여러 특성으로 나타내는 것과 같습니다. 차원이 높을수록 더 세밀하게 의미를 구분할 수 있지만, 저장 공간과 계산 비용도 늘어납니다.
```

**검증 기준:** 유사도 비교표, 비용 안내, 청킹 설명, 차원 설명이 각각 올바른 위치에 추가되었는지 확인

---

## Task 4: P3 디테일 수정 (작업량: 소~중)

### 4-1. 14_2장 — import time 위치 이동 (#12)

**파일:** `docs/08_llm/04_langchain/14_2_RAG 통합실습.md`
**위치:** 라인 474의 `import time`을 제거하고, 라인 117 부근(파일 상단 import 블록)에 추가

터미널 챗봇 코드의 while 루프 안에 있는 `import time` (라인 474)을 파일 상단 import 영역으로 이동:

코드 블록 상단의 import문들:
```python
from dotenv import load_dotenv
load_dotenv()

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
```

수정 후:
```python
from dotenv import load_dotenv
load_dotenv()

import time
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
```

그리고 while 루프 안의 `import time`(라인 474) 제거.

### 4-2. 각 장 말미 Pinecone 인덱스 삭제 안내 (#13)

아래 파일들의 마지막 섹션에 추가:

**11장** (정리 섹션 뒤, 실습 과제 뒤):
```markdown
> **실습 후 정리:** Pinecone 무료 티어는 인덱스 수가 제한되어 있습니다. 실습이 끝나면 아래 코드로 인덱스를 삭제하세요.
> ```python
> pc.delete_index("example-index")
> ```
```

**13장** (정리 섹션 뒤):
```markdown
> **실습 후 정리:**
> ```python
> pc.delete_index("movie-index")
> ```
```

**14장** (실습 요약 뒤):
```markdown
> **실습 후 정리:**
> ```python
> pc.delete_index("movie-vector-index")
> ```
```

### 4-3. 15장 API키 예시 통일 (#14)

**파일:** `docs/08_llm/04_langchain/15.AI 소믈리에 RAG 서비스 프로젝트.md`

**수정 대상:**
- 라인 121: `OPENAI_API_KEY=sk-...` → `OPENAI_API_KEY=본인의_OpenAI_API키`
- 라인 124: `PINECONE_API_KEY=pcsk_...` → `PINECONE_API_KEY=본인의_Pinecone_API키`
- 라인 192: `OPENAI_API_KEY = sk-p****` → `OPENAI_API_KEY=본인의_OpenAI_API키`
- 라인 195: `PINECONE_API_KEY = pcsk_*******` → `PINECONE_API_KEY=본인의_Pinecone_API키`

### 4-4. 14장 year 출력 int() 변환 (#15)

**파일:** `docs/08_llm/04_langchain/14.벡터 검색.md`

**수정 대상:** 3, 4, 5장의 코드 출력 결과에서 `2019.0` → `2019`, `2013.0` → `2013` 등

코드에서 year 출력 부분:
```python
print(match["metadata"]["title"], match["metadata"]["year"],match["metadata"]["genre"])
```
→
```python
print(match["metadata"]["title"], int(match["metadata"]["year"]), match["metadata"]["genre"])
```

그리고 출력 결과 예시도 변경:
- `기생충 2019.0 드라마` → `기생충 2019 드라마`
- `7번방의 선물 2013.0 드라마` → `7번방의 선물 2013 드라마`
- `범죄도시 2017.0 범죄` → `범죄도시 2017 범죄`
- 등 모든 결과에서 `.0` 제거

### 4-5. 14장 인덱스 삭제 후 재생성 패턴 경고 (#16)

**파일:** `docs/08_llm/04_langchain/14.벡터 검색.md`
**위치:** 라인 125~137 (delete_index + create_index)

코드 블록 위에 경고 추가:
```markdown
> **주의:** 아래 코드는 인덱스가 이미 존재하면 삭제 후 새로 생성합니다. 기존 데이터가 모두 삭제되므로, 보존이 필요한 인덱스에는 사용하지 마세요. 이 실습에서는 매번 깨끗한 상태에서 시작하기 위해 이 패턴을 사용합니다.
```

### 4-6. 14_2장 FAISS 내부 인덱스 주석 수정 (#17)

**파일:** `docs/08_llm/04_langchain/14_2_RAG 통합실습.md`
**위치:** 라인 230

**수정 전:**
```python
# [13장] 임베딩 + [12장] FAISS 인덱싱 (내부적으로 HNSW/ANN 사용)
```

**수정 후:**
```python
# [13장] 임베딩 + [12장] FAISS 인덱싱 (기본 Flat 인덱스 사용, 12장에서 배운 HNSW는 별도 지정 시 사용)
```

### 4-7. 15장 배치 업서트 패턴 개선 안내 (#18)

**파일:** `docs/08_llm/04_langchain/15.AI 소믈리에 RAG 서비스 프로젝트.md`
**위치:** 배치 업서트 코드 (라인 323~341) 뒤

추가:
```markdown
> **참고:** `PineconeVectorStore.from_documents()`는 호출할 때마다 새 VectorStore 객체를 생성합니다. 대량 데이터 업서트 시에는 한 번 생성한 VectorStore에 `add_documents()`를 반복 호출하는 것이 더 효율적입니다.
> ```python
> vector_store = PineconeVectorStore(index_name=PINECONE_INDEX_NAME, embedding=embeddings)
> for i in range(0, len(docs), BATCH_SIZE):
>     batch = docs[i:i + BATCH_SIZE]
>     vector_store.add_documents(batch)
>     print(f"Indexed documents {i} to {i + len(batch) - 1}")
> ```
```

### 4-8. 15장 image_to_base64_url에 raise_for_status 추가 (#19)

**파일:** `docs/08_llm/04_langchain/15.AI 소믈리에 RAG 서비스 프로젝트.md`
**위치:** 라인 424~428

**수정 전:**
```python
def image_to_base64_url(image_url: str):
    response = requests.get(image_url)
    mime_type = response.headers.get("Content-Type", "image/png")
```

**수정 후:**
```python
def image_to_base64_url(image_url: str):
    response = requests.get(image_url)
    response.raise_for_status()  # 이미지 다운로드 실패 시 에러 발생
    mime_type = response.headers.get("Content-Type", "image/png")
```

### 4-9. 14_2장 Streamlit foods 데이터 중복 안내 (#20)

**파일:** `docs/08_llm/04_langchain/14_2_RAG 통합실습.md`
**위치:** Streamlit 코드 내 foods 정의 시작 부분 (라인 550~551)

**수정 전:**
```python
# ===== 지식 베이스 (food_rag.py와 동일) =====
foods = [
```

**수정 후:**
```python
# ===== 지식 베이스 (food_rag.py와 동일 데이터) =====
# Streamlit은 별도 프로세스로 실행되므로 food_rag.py의 데이터를 직접 공유할 수 없습니다.
# 실제 서비스에서는 데이터를 별도 파일(JSON/CSV)로 분리하여 공통으로 로드합니다.
foods = [
```

**검증 기준:** 모든 P3 항목이 수정되었는지 파일별로 확인

---

## 작업량 요약

| Task | 우선순위 | 작업량 | 예상 소요 |
|------|----------|--------|-----------|
| Task 1 (P0) | 즉시 | 소 | 15~20분 |
| Task 2 (P1) | 품질 | 중 | 30~45분 |
| Task 3 (P2) | 보강 | 중 | 20~30분 |
| Task 4 (P3) | 디테일 | 소~중 | 25~35분 |
| **합계** | | | **~2시간** |

---

## 수정 파일별 변경 요약

| 파일 | 변경 항목 수 | 주요 변경 |
|------|-------------|-----------|
| 11장 | 3 | 비용 안내, 청킹 설명, 차원 설명 추가 |
| 12장 | 4 | 동기 부여, HNSW 비유, 설치 방법, 저수준 API 설명 |
| 13장 | 4 | 검색 순서 수정, score 설명, .env 정리, import 통일 |
| 14장 | 4 | 데이터 연속성 안내, 유사도 비교표, year int(), 삭제 경고 |
| 14_2장 | 4 | 모델명, import time, FAISS 주석, foods 중복 안내 |
| 15장 | 8 | 모델명, deprecated 파라미터, 장번호, 개념 설명, 비용, 패턴 통일 등 |

---

## 성공 기준

1. 모든 P0 항목이 반영되어 학습자가 혼란을 느끼지 않는다
2. 13장 검색 결과가 유사도 내림차순으로 정렬되어 있다
3. gpt-4o-mini가 모든 파일에서 gpt-4.1-mini로 교체되었다
4. deprecated API가 최신 API로 교체되었다
5. 12장~15장에 추가된 설명이 학습 흐름을 방해하지 않고 자연스럽게 녹아들어 있다
6. 코드의 import 패턴이 장 간에 일관성 있게 통일되었다
