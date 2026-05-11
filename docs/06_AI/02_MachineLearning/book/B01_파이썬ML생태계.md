---
title: B01. 파이썬 ML 생태계 (넘파이 · 판다스)
layout: default
parent: Machine Learning (책 기반)
nav_order: 1
permalink: /ml-book/ch01
---

{% raw %}

> 📖 **책 1장**. 파이썬 기반의 머신러닝과 생태계 이해 (p.1 ~ p.78)
>
> 💻 **실습 노트북**:
> - `data/pymlrev2-main/1장/1.3 넘파이_colab.ipynb`
> - `data/pymlrev2-main/1장/1.4 데이터 핸들링 - 판다스_colab.ipynb`

---

## 학습 목표

- ML 기반 파이썬 생태계의 핵심 패키지(넘파이·판다스·사이킷런·시본·맷플롯립) **역할을 구분할 수 있다**
- 넘파이 `ndarray`의 **shape·dtype·차원**을 설명하고 **인덱싱/슬라이싱/팬시·불린 인덱싱**을 구현할 수 있다
- 판다스 `DataFrame`으로 CSV를 읽고 **info / describe / value_counts** 로 데이터를 탐색할 수 있다
- **`loc` vs `iloc`** 의 차이를 설명하고 상황에 맞게 선택할 수 있다
- 결측치/이상치를 식별하고 **isnull / fillna / dropna** 로 처리할 수 있다
- `groupby` + `agg` 로 그룹별 통계를 산출할 수 있다

<a id="toc"></a>

## 진행 순서

1. [도입 — 왜 넘파이/판다스부터?](#part1) — ML 도구 사슬에서의 위치
2. [파이썬 ML 생태계 한눈에 보기](#part2) — 5개 핵심 패키지 역할
3. [넘파이 ndarray 기초](#part3) — 생성·dtype·shape·차원
4. [넘파이 인덱싱과 슬라이싱](#part4) — 단일/슬라이스/팬시/불린
5. [넘파이 정렬과 선형대수](#part5) — sort / argsort / dot / transpose
6. [판다스 DataFrame 기초](#part6) — read_csv / head / info / describe
7. [데이터 선택 — loc vs iloc](#part7) — 라벨 vs 위치
8. [결측치/이상치/타입 변환](#part8) — info → isnull → fillna/dropna
9. [groupby + apply 워크플로](#part9) — 그룹 통계 / 데이터 가공
10. [실습 가이드 (Colab)](#part10) — 노트북 셀 단위 진행 순서
11. [정리와 체크리스트](#part11)

---

<a id="part1"></a>

## 1️⃣ 도입 — 왜 넘파이/판다스부터? [↑](#toc)

> 머신러닝은 **데이터를 다루는 능력 + 모델을 부르는 능력**의 합입니다. 사이킷런(`fit/predict`)을 한 줄로 부르기 위해, 그 입력이 되는 데이터를 만져두는 게 90%의 작업입니다.

### ML 작업 흐름과 도구 매핑

```
[ CSV/Excel/DB ]
       │  ← 📦 판다스 (read_csv, DataFrame)
       ▼
[ 탐색 · 정제 · 변환 ]
       │  ← 📊 맷플롯립 / 시본 (시각화)
       │  ← 🔢 넘파이 (벡터/행렬 연산)
       ▼
[ X (행렬) ・ y (벡터) ]
       │  ← 🤖 사이킷런 (model.fit(X, y))
       ▼
[ 예측 / 평가 ]
```

**책 1장이 가르치는 것** = 가장 왼쪽 두 단계의 도구 사용법입니다. 사이킷런 자체는 2장부터.

---

<a id="part2"></a>

## 2️⃣ 파이썬 ML 생태계 한눈에 보기 [↑](#toc)

| 패키지 | 역할 비유 | 핵심 자료구조 |
|---|---|---|
| **NumPy** | 모든 숫자 연산의 토대 (계산기) | `ndarray` |
| **Pandas** | 엑셀+SQL을 합친 데이터 정리 도구 | `DataFrame`, `Series` |
| **Matplotlib** | 종이에 직접 그리는 펜 (저수준) | `figure`, `axes` |
| **Seaborn** | 통계용으로 미리 멋있게 그려주는 도구 (고수준) | `heatmap`, `pairplot` 등 |
| **Scikit-learn** | ML 알고리즘 백과사전 | `Estimator` (fit/predict) |

> 💡 **외워 두기**: ML 모델은 결국 **숫자 행렬(`ndarray`)을 받아 숫자 결과를 뱉는 함수**입니다. 그 변환을 `pandas`가 해주고, 알고리즘은 `sklearn`이 해줍니다.

### Colab 사용 권장

책의 1.2절은 Anaconda + Jupyter 설치를 소개하지만, **본 수업은 Google Colab을 사용**합니다 (이미 모든 패키지 설치 완료, 한글 폰트만 별도 설치).

```python
# Colab 환경 확인 (Colab 첫 셀에서)
import numpy, pandas, sklearn, matplotlib, seaborn
print("numpy:", numpy.__version__)
print("pandas:", pandas.__version__)
print("sklearn:", sklearn.__version__)
print("matplotlib:", matplotlib.__version__)
print("seaborn:", seaborn.__version__)
```

---

<a id="part3"></a>

## 3️⃣ 넘파이 ndarray 기초 [↑](#toc)

> `ndarray` = **같은 타입의 숫자**가 차곡차곡 들어간 다차원 배열. 파이썬 `list`보다 훨씬 빠르고 메모리도 적게 씁니다.

### 책의 핵심 메시지

책은 *"`ndarray.shape`만 머릿속에 그릴 수 있어도 절반 끝났다"* 고 강조합니다. 머신러닝 입력 `X`는 `(샘플 수, 피처 수)`의 2차원 `ndarray`이기 때문입니다.

### 미니 코드 — 풀버전은 `1.3 넘파이_colab.ipynb`

```python
import numpy as np

a = np.array([1, 2, 3])              # 1차원 벡터
b = np.array([[1, 2, 3], [4, 5, 6]]) # 2차원 행렬

print(a.shape, a.ndim, a.dtype)      # (3,)   1  int64
print(b.shape, b.ndim, b.dtype)      # (2,3)  2  int64
```

### 핵심 함수 정리

| 함수 | 용도 | 예 |
|---|---|---|
| `np.array(list)` | 파이썬 리스트 → ndarray | `np.array([1,2,3])` |
| `np.arange(n)` | 0 ~ n-1 정수 배열 | `np.arange(10)` |
| `np.zeros(shape)` / `np.ones(shape)` | 0 또는 1로 채운 배열 | `np.zeros((3,2))` |
| `arr.reshape(r, c)` | 모양 바꾸기 (총 원소 수 동일) | `np.arange(10).reshape(2,5)` |
| `arr.astype('float64')` | dtype 변환 | `arr.astype('int32')` |

### `reshape(-1, n)` 의 `-1` 트릭

`-1`은 "다른 차원에 맞춰 알아서 채워라"는 뜻입니다. 머신러닝에서 자주 등장합니다.

```python
arr = np.arange(12)
arr.reshape(-1, 4)   # shape (3, 4) — 행 수는 자동 계산
arr.reshape(4, -1)   # shape (4, 3) — 열 수는 자동 계산
arr.reshape(-1, 1)   # shape (12, 1) — 단일 컬럼 벡터로 (사이킷런이 자주 요구)
```

📐 *더 알아보기 (수학)*: `ndarray`는 C-스타일 메모리에 1D로 저장되고 `shape`은 메타데이터. `reshape`은 데이터를 복사하지 않고 **뷰**만 바꿉니다(가능한 경우).

---

<a id="part4"></a>

## 4️⃣ 넘파이 인덱싱과 슬라이싱 [↑](#toc)

> 4가지 방식 — **단일값 · 슬라이스 · 팬시 · 불린**. 책 1.3절의 핵심.

### 비교 표

| 방식 | 예 | 결과 | 언제 쓰나 |
|---|---|---|---|
| 단일값 | `arr[2]`, `arr2d[1,0]` | 스칼라 또는 1차원 | 한 점 추출 |
| 슬라이스 | `arr[1:4]`, `arr2d[:, 0:2]` | 부분 배열 | 연속 구간 |
| 팬시 (Fancy) | `arr[[0, 3, 5]]` | 임의 위치 모음 | 불연속 선택 |
| 불린 | `arr[arr > 5]` | 조건 만족 원소 | 필터링 |

### 불린 인덱싱 = **데이터 필터링의 기본기**

```python
arr = np.arange(1, 10)        # [1 2 3 4 5 6 7 8 9]
print(arr[arr > 5])           # [6 7 8 9]
```

머신러닝에서 *"점수가 60점 넘는 학생만 뽑기"* 같은 작업이 이걸로 한 줄입니다.

### 다차원 슬라이스 — 콤마로 축 구분

```python
arr2d = np.arange(1, 10).reshape(3, 3)
arr2d[0:2, 0:2]   # 좌상단 2x2
arr2d[:, 0]       # 모든 행의 0번 열 (1차원으로 떨어짐)
arr2d[[0, 2]]     # 0행과 2행 (팬시 인덱싱)
```

---

<a id="part5"></a>

## 5️⃣ 넘파이 정렬과 선형대수 [↑](#toc)

### 정렬 API 두 가지

| 함수 | 반환 | 원본 변경? |
|---|---|---|
| `np.sort(arr)` | 정렬된 **새 배열** | ❌ |
| `arr.sort()` | `None` (제자리 정렬) | ✅ |
| `np.argsort(arr)` | 정렬했을 때의 **인덱스 순서** | ❌ |

`argsort`는 책의 *"점수 순으로 학생 이름 출력"* 예제처럼 **인덱스를 통해 다른 배열을 같이 정렬**할 때 핵심.

```python
names = np.array(['John', 'Mike', 'Sarah', 'Kate'])
scores = np.array([78, 95, 84, 98])
order = np.argsort(scores)        # [0 2 1 3]  ← 점수 오름차순 인덱스
print(names[order])               # ['John' 'Sarah' 'Mike' 'Kate']
```

### 선형대수 두 가지만 기억

| API | 의미 |
|---|---|
| `np.dot(A, B)` 또는 `A @ B` | 행렬 내적 (ML에서 가중치 곱) |
| `np.transpose(A)` 또는 `A.T` | 전치 (행/열 뒤집기) |

📐 *더 알아보기*: 선형 회귀의 핵심 식 `y_hat = X @ w` 는 결국 `np.dot(X, w)` 입니다. 5장 회귀에서 다시 봅니다.

---

<a id="part6"></a>

## 6️⃣ 판다스 DataFrame 기초 [↑](#toc)

> `DataFrame` = **열마다 이름이 붙어 있는 ndarray 묶음**. 엑셀 시트와 거의 같은 직관.

### 가장 자주 쓰는 4종 세트

```python
import pandas as pd

df = pd.read_csv('titanic_train.csv')   # CSV 로드

df.head()        # 위 5행 — "어떤 데이터인지 한눈에"
df.info()        # 컬럼별 dtype·결측치 수
df.describe()    # 수치형 컬럼의 평균/표준편차/사분위수
df.shape         # (행 수, 열 수)
```

> 💡 **수업 진행 팁**: 데이터를 처음 받으면 무조건 `head` → `info` → `describe` 세 줄을 친다. 책 1.4절도 이 흐름.

### 범주형 컬럼 빠른 분포 보기

```python
df['Sex'].value_counts()
# male      577
# female    314
```

`value_counts(normalize=True)` 로 비율도 한 번에. ML 데이터의 **클래스 불균형** 확인 필수 도구.

### Series ↔ DataFrame 변환

| 방향 | 코드 |
|---|---|
| 열 하나 꺼내기 | `df['Age']` → Series |
| 여러 열 꺼내기 | `df[['Age', 'Fare']]` → DataFrame |
| Series → DataFrame | `df['Age'].to_frame()` |
| DataFrame → ndarray | `df.values` 또는 `df.to_numpy()` |

---

<a id="part7"></a>

## 7️⃣ 데이터 선택 — loc vs iloc [↑](#toc)

| | `loc` | `iloc` |
|---|---|---|
| 의미 | **라벨**(이름)로 접근 | **위치**(정수)로 접근 |
| 행 인덱스 예 | `df.loc['kim']` | `df.iloc[0]` |
| 슬라이스 끝 | 끝값 **포함** | 끝값 **불포함** |
| 컬럼 | 이름 가능 | 정수만 |

### 패턴 정리

```python
df.loc[0, 'Age']                    # 라벨 기반 (인덱스 0의 Age)
df.iloc[0, 3]                       # 위치 기반 (0행 3열)

df.loc[df['Age'] > 30, ['Name', 'Age']]   # 조건 + 컬럼 선택 (가장 자주 씀)
df.iloc[:5, :3]                          # 처음 5행 × 처음 3열
```

> ⚠️ **자주 헷갈리는 점**: `df.loc[0:3]` 은 인덱스 0,1,2,**3** (4개). `df.iloc[0:3]` 은 0,1,2 (3개). 책에서도 강조하는 차이.

---

<a id="part8"></a>

## 8️⃣ 결측치/이상치/타입 변환 [↑](#toc)

### 결측치 식별·처리 3단계

```python
df.isnull().sum()           # 컬럼별 결측치 개수 (가장 먼저)
df.dropna(subset=['Age'])   # Age가 결측인 행 제거 (간단·과격)
df['Age'].fillna(df['Age'].mean())   # 평균으로 대치 (책 권장 시작점)
```

### 타입 변환 — `astype` 한 줄

```python
df['Pclass'] = df['Pclass'].astype('category')   # 수치 → 범주
df['Age']    = df['Age'].astype('float64')
```

> 💡 **수업 팁**: `info()`에서 `object` 로 잡힌 컬럼은 대개 문자열. 범주형이면 `astype('category')` 로 바꿔두면 메모리·속도 모두 이득.

---

<a id="part9"></a>

## 9️⃣ groupby + apply 워크플로 [↑](#toc)

> *"성별로 나눠서 평균 나이"* 같은 SQL `GROUP BY`를 한 줄로.

```python
df.groupby('Sex')['Age'].mean()
# Sex
# female    27.9
# male      30.7

df.groupby(['Sex', 'Pclass']).agg(
    avg_age=('Age', 'mean'),
    n_survived=('Survived', 'sum'),
)
```

### `apply` — 함수 한 번에 적용

```python
df['AgeGroup'] = df['Age'].apply(lambda x: '아동' if x < 15 else '성인')
```

> 📐 *내부 동작*: `apply`는 파이썬 루프라 느립니다. 가능한 한 **벡터 연산**(`np.where`, `pd.cut`) 우선. 책에서도 후반부에 같은 권고가 나옵니다.

---

<a id="part10"></a>

## 🔟 실습 가이드 (Colab) [↑](#toc)

### `1.3 넘파이_colab.ipynb`

| 셀 묶음 | 학습 포인트 | 강사 멘트 |
|---|---|---|
| 셀 0~1 (헤더) | Colab 환경 설명 | "원본은 5월 기준 sklearn 1.0.2로 작성, 우리는 1.5+ 환경" |
| 셀 2~9 | ndarray 생성·shape·dtype | shape (3,) vs (1,3) 차이 강조 |
| 셀 10~17 | arange/zeros/ones/reshape | `-1` 트릭 라이브로 시연 |
| 셀 18~26 | 인덱싱·슬라이싱 | 그림판에 2D 배열 그려가며 |
| 셀 27~33 | 팬시·불린 인덱싱 | "조건으로 필터" 흐름 |
| 셀 34~42 | sort / argsort | argsort 예제(이름·점수) 실습 |
| 셀 43~45 | 행렬 내적·전치 | 회귀 미리보기 ("y=Xw 가 곧 dot") |

### `1.4 데이터 핸들링 - 판다스_colab.ipynb`

| 셀 묶음 | 학습 포인트 |
|---|---|
| 전반부 | read_csv / head / info / describe |
| 중반부 | 컬럼 선택, loc/iloc, 불린 필터 |
| 후반부 | groupby, apply, 결측치 처리 |

> 🛠 **실습 진행 권장 흐름**: 강사가 한 셀 시연 → 학생 같이 실행 → 결과 비교 → 5분 짧은 변형 과제(컬럼 바꿔보기, 조건 바꿔보기) → 다음 셀.

---

<a id="part11"></a>

## 1️⃣1️⃣ 정리와 체크리스트 [↑](#toc)

### 한 문장 요약

> **NumPy는 빠른 숫자 배열, Pandas는 이름 붙은 표.** ML 모델은 결국 `ndarray`를 받지만, 그 전 단계 데이터 정리는 `DataFrame`이 가장 편하다.

### 자기 점검 (모두 ✅ 가 되어야 다음 장으로)

- [ ] `np.array([[1,2],[3,4]]).shape` → `(2,2)` 인 이유를 설명할 수 있다
- [ ] `arr[arr > 5]` 가 어떤 결과를 반환하는지 즉답할 수 있다
- [ ] `np.argsort` 가 왜 유용한지 한 가지 예를 든다
- [ ] `df.loc[0]` 과 `df.iloc[0]` 의 차이를 안다
- [ ] 타이타닉 데이터의 결측치 처리 코드를 5줄 안에 작성한다
- [ ] `groupby('Sex')['Age'].mean()` 의 결과 형태를 예측한다

### 다음 차시 예고

**B02 사이킷런 시작** — `fit / predict / score` 의 통일 API. 붓꽃 데이터로 첫 분류기 만들기.

### 흔한 오해 모음

| 오해 | 사실 |
|---|---|
| "리스트랑 ndarray는 사실상 같다" | 메모리 구조·연산 속도·브로드캐스트 모두 다름 |
| "DataFrame은 항상 .values로 ndarray 만들고 시작" | 컬럼 이름을 잃어버려 추적이 어려워짐. sklearn 1.2+ 는 DataFrame 직접 지원 |
| "loc은 라벨, iloc은 정수면 끝" | **슬라이스 끝값 포함 여부**가 다른 게 가장 큰 함정 |
| "groupby 결과는 DataFrame이다" | 단일 컬럼 집계는 Series. `agg` 로 명시하면 DataFrame |

{% endraw %}
