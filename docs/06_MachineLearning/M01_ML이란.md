---
title: 01. ML이란?
layout: default
parent: Machine Learning
nav_order: 1
permalink: /machinelearning/intro
---

{% raw %}

## 학습 목표

- AI, ML, DL의 관계를 벤다이어그램으로 설명할 수 있다
- 지도학습, 비지도학습, 강화학습의 차이를 비유로 구분할 수 있다
- scikit-learn의 fit/predict/score 패턴을 처음 실행해볼 수 있다

<a id="toc"></a>

## 진행 순서

1. [AI vs ML vs DL](#part1) - "AI > ML > DL" 관계와 벤다이어그램
2. [머신러닝이란?](#part2) - 데이터에서 패턴을 찾아 미래를 예측하는 것
3. [학습 유형 3가지](#part3) - 지도학습, 비지도학습, 강화학습
4. [회귀 vs 분류](#part4) - 연속 값 예측 vs 범주 분류
5. [ML 작업 흐름](#part5) - 데이터 수집부터 예측까지의 전체 과정
6. [scikit-learn 소개](#part6) - 통일된 API 패턴: fit/predict/score
7. [Google Colab 시작하기](#part7) - 브라우저에서 파이썬 실행 환경 설정
8. [정리](#part8) - 핵심 개념 요약

---

# 01장. 머신러닝이란? — AI, ML, DL의 관계

<a id="part1"></a>

## 1️⃣ AI vs ML vs DL [↑](#toc)

> 지도학습 = 선생님이 채점하는 숙제 — 정답이 있는 데이터로 패턴을 학습합니다.

뉴스에서 "AI", "머신러닝", "딥러닝"이라는 단어가 혼용됩니다.  
이 세 가지는 실제로 **포함 관계**를 가집니다.

### 벤다이어그램

```
┌─────────────────────────────────────────┐
│                                         │
│   AI (인공지능)                          │
│   "컴퓨터가 인간처럼 지능적으로 행동"    │
│                                         │
│   ┌───────────────────────────────┐     │
│   │                               │     │
│   │   ML (머신러닝)                │     │
│   │   "데이터로 스스로 학습"        │     │
│   │                               │     │
│   │   ┌───────────────────┐       │     │
│   │   │                   │       │     │
│   │   │  DL (딥러닝)       │       │     │
│   │   │  "뇌의 신경망 모방"│       │     │
│   │   │                   │       │     │
│   │   └───────────────────┘       │     │
│   └───────────────────────────────┘     │
└─────────────────────────────────────────┘
```

### 세 가지 비유

| 용어 | 설명 | 비유 |
|------|------|------|
| **AI (인공지능)** | 컴퓨터가 지능적으로 행동하는 모든 기술 | "지능" 그 자체 |
| **ML (머신러닝)** | 데이터에서 스스로 규칙을 찾아내는 AI | "경험에서 배우기" |
| **DL (딥러닝)** | 사람의 뇌(신경망)를 모방한 ML 기법 | "뇌 구조를 흉내 내기" |

- **AI 없이 ML 없고**, ML 없이 DL 없습니다
- 모든 DL은 ML이지만, 모든 ML이 DL은 아닙니다
- 이 과정에서는 **ML (scikit-learn)** 에 집중합니다. DL은 다음 과정(PyTorch/TensorFlow)에서 다룹니다

---

<a id="part2"></a>

## 2️⃣ 머신러닝이란? [↑](#toc)

> 규칙을 직접 프로그래밍하는 것이 아니라, **데이터를 보여주고 컴퓨터가 스스로 규칙을 찾게 하는 것**입니다.

### 전통적 프로그래밍 vs 머신러닝

| | 전통적 프로그래밍 | 머신러닝 |
|---|-----------------|----------|
| **입력** | 규칙 + 데이터 | 데이터 + 정답 |
| **출력** | 결과 | 규칙(모델) |
| **사람의 역할** | 모든 규칙을 직접 코딩 | 좋은 데이터를 준비 |
| **예시** | `if 이메일에 "돈을버세요" 포함 → 스팸` | 수백만 개 이메일을 학습 → 스스로 스팸 규칙 발견 |

### 실생활 속 머신러닝 예시

- **스팸 필터**: 수십만 개의 스팸/정상 메일을 학습해 새 메일을 자동 분류
- **유튜브 추천**: 시청 기록 패턴을 학습해 다음에 볼 영상을 예측
- **번역기**: 수십억 개의 번역 문장 쌍을 학습해 새 문장을 번역
- **얼굴 인식**: 수백만 개의 얼굴 사진을 학습해 새 사진에서 사람을 식별
- **금융 사기 탐지**: 정상/이상 거래 패턴을 학습해 의심 거래를 자동 감지

### 핵심 정의

> **머신러닝** = 데이터에서 패턴을 찾아, 한 번도 본 적 없는 새로운 데이터에 대해 예측하는 것

---

<a id="part3"></a>

## 3️⃣ 학습 유형 3가지 [↑](#toc)

> 어떤 종류의 데이터를 주느냐에 따라 학습 방법이 달라집니다.

### 지도학습 (Supervised Learning)

> 선생님이 채점해주는 숙제처럼, **정답(레이블)이 붙은 데이터**로 학습합니다.

```
데이터: [스팸 메일, 정상 메일, 스팸 메일, ...] ← 정답 레이블 있음
학습 후: 새 메일 → "스팸인지 아닌지" 예측 가능
```

- **예시**: 이메일 스팸 분류, 주택 가격 예측, 의료 진단, 이미지 분류
- **이 과정의 메인 파트**: Part 2, Part 3 전체

### 비지도학습 (Unsupervised Learning)

> 정답 없이 데이터만 줬을 때, 사서가 책을 분류하는 것처럼 **스스로 그룹을 찾아냅니다**.

```
데이터: [고객 구매 기록들] ← 정답 레이블 없음
학습 후: 비슷한 구매 패턴의 고객을 자동으로 4개 그룹으로 묶어줌
```

- **예시**: 고객 세분화, 이상 탐지, 문서 토픽 분류, 이미지 압축
- **이 과정에서**: Part 4 (클러스터링, 차원 축소)

### 강화학습 (Reinforcement Learning)

> 게임에서 시행착오를 반복하며 점수를 높이듯, **상(보상)과 벌(패널티)로 스스로 전략을 학습**합니다.

```
에이전트가 바둑을 둠 → 이기면 +보상, 지면 -패널티 → 이기는 수를 더 많이 선택하도록 학습
```

- **예시**: AlphaGo, 자율주행, 게임 AI, 로봇 제어
- 이 과정에서는 다루지 않습니다 (별도 과정 필요)

### 요약 비교

| 유형 | 정답 레이블 | 비유 | 대표 예시 |
|------|-----------|------|----------|
| 지도학습 | 있음 | 선생님이 채점하는 숙제 | 스팸 분류, 집값 예측 |
| 비지도학습 | 없음 | 정리 기준 없이 책 분류하는 사서 | 고객 세분화 |
| 강화학습 | 없음 (보상만 있음) | 게임에서 시행착오로 배우기 | AlphaGo |

---

<a id="part4"></a>

## 4️⃣ 회귀 vs 분류 [↑](#toc)

> 지도학습은 예측하려는 값의 종류에 따라 회귀와 분류로 나뉩니다.

### 핵심 차이

| | 회귀 (Regression) | 분류 (Classification) |
|---|-----------------|----------------------|
| **예측하는 값** | 연속적인 숫자 | 정해진 카테고리 |
| **질문 형태** | "얼마나?" "몇 개?" | "어느 것?" "맞냐 틀리냐?" |
| **예시** | 내일 기온, 아파트 가격, 주식 가격 | 스팸/정상, 합격/불합격, 꽃 종류 |
| **출력** | 23.5도, 5억 원, 1,200원 | 스팸, 합격, Iris Setosa |

### 실제 예시

```
회귀 문제:
  - 이 아파트의 가격은 얼마일까? → 4억 3,500만 원
  - 내일 서울의 최고 기온은? → 28.3도
  - 이번 달 전기 사용량은? → 312 kWh

분류 문제:
  - 이 이메일은 스팸인가? → 스팸 / 정상
  - 이 환자는 당뇨병인가? → 양성 / 음성
  - 이 꽃은 어떤 종인가? → Setosa / Versicolor / Virginica
```

{::nomarkdown}
<details>
<summary>📐 더 알아보기 — 회귀와 분류의 수학적 차이</summary>
<p><strong>회귀</strong>: 출력값 y가 실수 전체 범위 (y ∈ ℝ)</p>
<p>예: 집값 = w₁×면적 + w₂×층수 + b</p>
<p><strong>분류</strong>: 출력값 y가 클래스 레이블 {0, 1} 또는 {0, 1, 2, ...}</p>
<p>이진 분류: P(y=1|X) = σ(wᵀX + b), 여기서 σ는 시그모이드 함수</p>
<p>이 차이가 손실 함수 선택에도 영향을 줍니다.</p>
<p>- 회귀: 평균 제곱 오차(MSE)</p>
<p>- 분류: 교차 엔트로피(Cross-Entropy)</p>
</details>
{:/nomarkdown}

---

<a id="part5"></a>

## 5️⃣ ML 작업 흐름 [↑](#toc)

> 요리에도 레시피가 있듯, ML에도 정해진 작업 순서가 있습니다.

### 전체 파이프라인

```
1. 문제 정의        "무엇을 예측할 것인가? 회귀? 분류?"
        ↓
2. 데이터 수집      "어떤 데이터가 필요한가? 어디서 구할 것인가?"
        ↓
3. EDA              "데이터에 어떤 패턴이 있는가? 이상치는 없는가?"
  (탐색적 분석)
        ↓
4. 전처리           "스케일링, 결측치 처리, 범주형 인코딩"
        ↓
5. 모델 선택 & 학습  "어떤 알고리즘을 쓸 것인가? model.fit(X_train, y_train)"
        ↓
6. 평가             "모델이 얼마나 잘 예측하는가? model.score(X_test, y_test)"
        ↓
7. 튜닝 & 반복      "성능을 더 높이려면? 다시 3번으로"
        ↓
8. 배포             "실제 서비스에 적용"
```

### 현실에서의 시간 배분

| 단계 | 비율 | 이유 |
|------|------|------|
| 데이터 수집/정제 | ~40% | 현실 데이터는 항상 지저분합니다 |
| EDA | ~20% | 이해 없이 좋은 모델 없음 |
| 전처리 | ~15% | 모델 성능의 80%는 전처리에서 결정 |
| 모델링 | ~15% | scikit-learn으로 3줄이면 됩니다 |
| 평가/튜닝 | ~10% | 반복적인 개선 |

> "데이터 과학자의 80%는 데이터 청소부다" — 현업 데이터 과학자들의 흔한 농담

---

<a id="part6"></a>

## 6️⃣ scikit-learn 소개 [↑](#toc)

> scikit-learn의 천재적인 설계: 알고리즘이 뭐든 **항상 같은 3줄 패턴**입니다.

### 통일 API 패턴

```python
# 1단계: 모델 선택 (알고리즘 이름만 바꾸면 됨)
from sklearn.linear_model import LinearRegression
model = LinearRegression()

# 2단계: 학습 (훈련 데이터를 넣으면 패턴을 찾음)
model.fit(X_train, y_train)

# 3단계: 예측 (새로운 데이터에 적용)
predictions = model.predict(X_test)

# 4단계: 평가 (모델이 얼마나 잘 맞추는지)
score = model.score(X_test, y_test)
print(f"정확도: {score:.2f}")
```

### 알고리즘이 바뀌어도 패턴은 같습니다

```python
# 선형 회귀 → 의사결정 나무로 바꿀 때
from sklearn.tree import DecisionTreeClassifier  # 이 줄만 바꿈
model = DecisionTreeClassifier()                 # 이 줄만 바꿈
model.fit(X_train, y_train)                      # 동일
predictions = model.predict(X_test)              # 동일
score = model.score(X_test, y_test)              # 동일
```

이 설계 덕분에 여러 알고리즘을 빠르게 비교할 수 있습니다.

### 첫 번째 scikit-learn 예제 (Colab에서 실행해보세요)

```python
# 패키지 불러오기
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# 데이터 로드
iris = load_iris()
X, y = iris.data, iris.target

# 훈련/테스트 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# 모델 학습
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# 평가
score = model.score(X_test, y_test)
print(f"정확도: {score:.2f}")
```

```
실행 결과:
정확도: 1.00
```

Iris 데이터는 매우 깨끗한 데이터라 거의 100% 정확도가 나옵니다.  
실제 데이터에서는 70~90%가 좋은 성능입니다.

---

<a id="part7"></a>

## 7️⃣ Google Colab 시작하기 [↑](#toc)

> Colab = 구글이 제공하는 무료 Jupyter Notebook 클라우드 환경.  
> Python, scikit-learn, pandas 등이 모두 설치되어 있어 바로 사용 가능합니다.

### Colab 열기

1. [colab.research.google.com](https://colab.research.google.com) 접속
2. Google 계정으로 로그인
3. 새 노트북 → `파일 > 새 노트북`
4. 상단에 노트북 이름 클릭 → `ML_Chapter01.ipynb`로 변경

### 핵심 단축키

| 단축키 | 동작 |
|--------|------|
| `Shift + Enter` | 현재 셀 실행 후 다음 셀로 이동 |
| `Ctrl + Enter` | 현재 셀만 실행 |
| `Esc + B` | 아래에 새 셀 추가 |
| `Esc + M` | 현재 셀을 마크다운으로 변경 |
| `Esc + Y` | 현재 셀을 코드로 변경 |

### 설치 확인 셀

```python
# scikit-learn 버전 확인
import sklearn
import pandas
import numpy
import matplotlib
import seaborn

print(f"scikit-learn: {sklearn.__version__}")
print(f"pandas:       {pandas.__version__}")
print(f"numpy:        {numpy.__version__}")
print(f"matplotlib:   {matplotlib.__version__}")
print(f"seaborn:      {seaborn.__version__}")
```

```
실행 결과:
scikit-learn: 1.3.2
pandas:       2.0.3
numpy:        1.25.2
matplotlib:   3.7.1
seaborn:      0.13.0
```

### 한글 폰트 설정 (그래프에서 한글 깨짐 방지)

```python
# Colab에서 한글 폰트 설정
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 나눔고딕 폰트 설치
import subprocess
subprocess.run(['apt-get', 'install', '-y', 'fonts-nanum'], capture_output=True)

# 폰트 캐시 갱신
fm._load_fontmanager(try_read_cache=False)

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

print("한글 폰트 설정 완료!")

# 테스트
fig, ax = plt.subplots(figsize=(6, 3))
ax.set_title("한글 제목 테스트 — 이제 한글이 잘 보입니다")
ax.plot([1, 2, 3], [1, 4, 9])
ax.set_xlabel("X축 레이블")
ax.set_ylabel("Y축 레이블")
plt.show()
```

```
실행 결과:
한글 폰트 설정 완료!
[그래프가 출력됩니다 — 한글이 정상적으로 표시됩니다]
```

> 이 셀은 매 노트북의 첫 번째 셀로 항상 실행하세요. 세션이 재시작되면 다시 실행해야 합니다.

---

<a id="part8"></a>

## 8️⃣ 정리 [↑](#toc)

### 핵심 개념 요약

| 개념 | 설명 | 비유 |
|------|------|------|
| AI | 컴퓨터가 지능적으로 행동하는 모든 기술의 총칭 | 지능 그 자체 |
| ML | 데이터에서 스스로 규칙을 찾아 예측하는 AI 기법 | 경험으로 배우기 |
| DL | 인간 뇌의 신경망 구조를 모방한 ML 기법 | 뇌 구조 흉내 내기 |
| 지도학습 | 정답 레이블이 있는 데이터로 학습 | 채점받는 숙제 |
| 비지도학습 | 정답 없이 데이터 패턴을 스스로 발견 | 기준 없이 책 분류하는 사서 |
| 강화학습 | 보상/패널티로 최적 행동 전략을 학습 | 게임에서 시행착오로 배우기 |
| 회귀 | 연속적인 숫자 값 예측 | "얼마나?" 질문 |
| 분류 | 정해진 카테고리 중 하나로 예측 | "어느 것?" 질문 |
| scikit-learn | ML 알고리즘 파이썬 라이브러리 | ML 도구 상자 |
| fit/predict/score | scikit-learn의 통일 API 패턴 | 모든 알고리즘의 공통 언어 |

---

### 다음 장 미리보기

| 장 | 내용 |
|---|---|
| 2장 | 데이터 다루기 — NumPy로 행렬 연산, Pandas로 데이터 분석, matplotlib/seaborn으로 시각화 |
| 3장 | 데이터 전처리 — 스케일링, 인코딩, 훈련/테스트 분할, Pipeline으로 데이터 누수 방지 |

---

### 실습 과제

**기본**: Colab에서 새 노트북을 만들고, 한글 폰트 설정 셀과 scikit-learn 버전 확인 셀을 실행해보세요.

**중급**: 이 장의 "첫 번째 scikit-learn 예제"를 실행한 뒤, `LogisticRegression`을 `DecisionTreeClassifier`로 바꿔서 실행해보세요. 정확도가 달라지나요?

**심화**: 일상에서 머신러닝이 사용될 것 같은 서비스를 3가지 찾아보세요. 각각 지도학습인지 비지도학습인지 판단하고 이유를 설명해보세요.

{% endraw %}


→ **다음 장**: [02. 데이터 다루기](/machinelearning/data-tools)
