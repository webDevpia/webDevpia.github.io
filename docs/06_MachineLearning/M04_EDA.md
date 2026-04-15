---
title: 04. 탐색적 데이터 분석
layout: default
parent: Machine Learning
nav_order: 4
permalink: /machinelearning/eda
---

{% raw %}

## 학습 목표

- 단변량/이변량/다변량 분석의 차이를 설명하고 적절한 그래프를 선택할 수 있다
- IQR 방법으로 이상치를 탐지하고 처리 방향을 결정할 수 있다
- Titanic 데이터에 EDA를 적용해 생존에 영향을 준 요소를 데이터로 근거를 들어 설명할 수 있다

<a id="toc"></a>

## 진행 순서

1. [EDA란?](#part1) - 데이터를 눈으로 이해하는 과정
2. [단변량 분석](#part2) - 히스토그램, 박스플롯, 왜도/첨도
3. [이변량 분석](#part3) - 산점도, 상관관계, 그룹별 비교
4. [다변량 분석](#part4) - pairplot, 다중 heatmap
5. [이상치 탐지](#part5) - IQR 방법과 박스플롯
6. [상관관계 분석](#part6) - Pearson 상관계수, seaborn heatmap
7. [실습: Titanic EDA](#part7) - 완전한 EDA 워크플로우
8. [정리](#part8) - 핵심 개념 요약 + 다음 장 브릿지

---

# 04장. 탐색적 데이터 분석(EDA) — 데이터 탐정이 되기

<a id="part1"></a>

## 1️⃣ EDA란? [↑](#toc)

> EDA = 탐정 수사 — 데이터에 숨겨진 단서(패턴, 이상치, 관계)를 찾아라!  
> 셜록 홈즈가 범죄 현장을 꼼꼼히 살피듯, 모델을 만들기 전에 데이터를 철저히 들여다봅니다.

### EDA가 중요한 이유

| 단계 없이 바로 모델링하면 | EDA를 먼저 하면 |
|------------------------|----------------|
| 결측치 때문에 모델이 오류 | 결측치 파악 후 처리 전략 수립 |
| 이상치 때문에 성능 급락 | 이상치 발견 후 제거/변환 결정 |
| 중요하지 않은 특성 과다 학습 | 중요한 특성 미리 파악 |
| 왜 틀렸는지 설명 불가 | 데이터 이해 기반으로 설명 가능 |

> 현업 데이터 과학자들은 전체 프로젝트 시간의 **50~80%를 EDA와 전처리에 씁니다.**  
> "머신러닝 = 모델 구축" 이라는 오해는 여기서 깨집니다.

### EDA의 3단계

```
1️⃣ 단변량 분석      하나의 변수를 깊이 파기
        ↓
2️⃣ 이변량 분석      두 변수의 관계 찾기
        ↓
3️⃣ 다변량 분석      전체 그림 보기
```

---

<a id="part2"></a>

## 2️⃣ 단변량 분석 [↑](#toc)

> 하나의 변수를 집중적으로 들여다봅니다 — "이 변수는 어떻게 분포되어 있는가?"

### 히스토그램 — 분포 모양 확인

```python
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 나이 분포
axes[0].hist(df['age'].dropna(), bins=30, color='steelblue',
             edgecolor='white', alpha=0.8)
axes[0].set_title("나이 분포")
axes[0].set_xlabel("나이")
axes[0].set_ylabel("빈도")
axes[0].axvline(df['age'].mean(), color='red', linestyle='--',
                label=f"평균: {df['age'].mean():.1f}")
axes[0].axvline(df['age'].median(), color='orange', linestyle='--',
                label=f"중앙값: {df['age'].median():.1f}")
axes[0].legend()

# 요금 분포
axes[1].hist(df['fare'], bins=50, color='coral', edgecolor='white', alpha=0.8)
axes[1].set_title("요금 분포 (오른쪽 꼬리 주목)")
axes[1].set_xlabel("요금")
axes[1].set_ylabel("빈도")

plt.tight_layout()
plt.show()

# 기초 통계
print("=== 나이 기초 통계 ===")
print(df['age'].describe().round(2))
print(f"\n왜도(skewness): {df['age'].skew():.3f}")
print(f"첨도(kurtosis): {df['age'].kurtosis():.3f}")
```

```
실행 결과:
[나이 히스토그램 — 종 모양, 오른쪽 약간 치우침]
[요금 히스토그램 — 대부분 낮은 요금, 소수의 매우 높은 요금 → 오른쪽 긴 꼬리]

=== 나이 기초 통계 ===
count    714.00
mean      29.70
std       14.53
min        0.17
25%       20.12
50%       28.00
75%       38.00
max       80.00

왜도(skewness): 0.389
첨도(kurtosis): 0.179
```

### 왜도(Skewness)와 첨도(Kurtosis) 해석

| 값 | 의미 |
|----|------|
| 왜도 ≈ 0 | 좌우 대칭 (정규분포) |
| 왜도 > 0 | 오른쪽 꼬리가 긺 (고소득자처럼 소수 극단값이 오른쪽) |
| 왜도 < 0 | 왼쪽 꼬리가 긺 |
| 첨도 > 0 | 뾰족한 분포 (극단값이 많음) |
| 첨도 < 0 | 납작한 분포 |

> `fare`(요금)의 왜도가 크면 → 로그 변환(`np.log1p`)을 고려합니다.

### 박스플롯 — 5가지 통계값 한눈에

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')

fig, ax = plt.subplots(figsize=(8, 4))
ax.boxplot(df['age'].dropna(), vert=False, patch_artist=True,
           boxprops=dict(facecolor='lightblue', color='navy'),
           medianprops=dict(color='red', linewidth=2))
ax.set_title("나이 박스플롯")
ax.set_xlabel("나이")

# 각 선이 의미하는 것
ax.annotate("최솟값(이상치 제외)", xy=(0.17, 1), xytext=(5, 1.3),
            arrowprops=dict(arrowstyle='->', color='gray'), fontsize=8)
ax.annotate("Q1 (25%)", xy=(20, 1), xytext=(15, 0.65),
            arrowprops=dict(arrowstyle='->', color='gray'), fontsize=8)
ax.annotate("중앙값", xy=(28, 1), xytext=(28, 0.65),
            arrowprops=dict(arrowstyle='->', color='gray'), fontsize=8)
ax.annotate("Q3 (75%)", xy=(38, 1), xytext=(42, 0.65),
            arrowprops=dict(arrowstyle='->', color='gray'), fontsize=8)

plt.tight_layout()
plt.show()
```

```
실행 결과:
[박스플롯: 상자(IQR), 수염(정상 범위), 점(이상치)이 표시됩니다]
```

```
박스플롯 해석:
│─── 수염 ───│  Q1 │─── 상자 ───│ 중앙값 │─── 상자 ───│ Q3  │─── 수염 ───│  ● 이상치
```

---

<a id="part3"></a>

## 3️⃣ 이변량 분석 [↑](#toc)

> 두 변수의 관계를 분석합니다 — "A가 높으면 B도 높은가?"

### 수치형 vs 수치형: 산점도

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 나이 vs 요금 (생존 여부 색상 구분)
scatter = axes[0].scatter(df['age'], df['fare'],
                          c=df['survived'], cmap='RdYlGn',
                          alpha=0.5, s=30)
plt.colorbar(scatter, ax=axes[0], label='생존(1)/사망(0)')
axes[0].set_title("나이 vs 요금 (생존 여부)")
axes[0].set_xlabel("나이")
axes[0].set_ylabel("요금")

# seaborn regplot: 회귀선 포함 산점도
sns.regplot(data=df, x='age', y='fare', ax=axes[1],
            scatter_kws={'alpha': 0.3, 's': 20}, line_kws={'color': 'red'})
axes[1].set_title("나이 vs 요금 (회귀선 포함)")
axes[1].set_xlabel("나이")
axes[1].set_ylabel("요금")

plt.tight_layout()
plt.show()
```

```
실행 결과:
[좌: 나이×요금 산점도 (생존자=녹색, 사망자=빨강)]
[우: 회귀선이 추가된 산점도 — 나이와 요금은 약한 양의 상관관계]
```

### 범주형 vs 수치형: 박스플롯과 바이올린 플롯

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 생존 여부별 나이 분포 — boxplot
sns.boxplot(data=df, x='survived', y='age', palette='Set3', ax=axes[0])
axes[0].set_title("생존 여부별 나이 분포")
axes[0].set_xticklabels(['사망(0)', '생존(1)'])
axes[0].set_xlabel("생존 여부")
axes[0].set_ylabel("나이")

# 생존 여부별 나이 분포 — violinplot (분포 형태까지 확인)
sns.violinplot(data=df, x='survived', y='age', palette='pastel', ax=axes[1])
axes[1].set_title("생존 여부별 나이 분포 (바이올린)")
axes[1].set_xticklabels(['사망(0)', '생존(1)'])
axes[1].set_xlabel("생존 여부")
axes[1].set_ylabel("나이")

plt.tight_layout()
plt.show()

# 그룹별 평균 비교
print("=== 생존 여부별 평균 나이 ===")
print(df.groupby('survived')['age'].mean().round(1))
```

```
실행 결과:
[boxplot과 violinplot이 나란히 출력됩니다]

=== 생존 여부별 평균 나이 ===
survived
0    30.6
1    28.3
```

### 범주형 vs 범주형: countplot with hue

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 성별 × 생존 여부
sns.countplot(data=df, x='sex', hue='survived', palette='RdYlGn', ax=axes[0])
axes[0].set_title("성별 × 생존 여부")
axes[0].legend(title='생존', labels=['사망', '생존'])

# 객실 등급 × 생존 여부
sns.countplot(data=df, x='pclass', hue='survived', palette='RdYlGn', ax=axes[1])
axes[1].set_title("객실 등급 × 생존 여부")
axes[1].legend(title='생존', labels=['사망', '생존'])

plt.tight_layout()
plt.show()

# 그룹별 생존율
print("=== 성별 생존율 ===")
print(df.groupby('sex')['survived'].mean().round(3))
print("\n=== 객실 등급별 생존율 ===")
print(df.groupby('pclass')['survived'].mean().round(3))
```

```
실행 결과:
[성별 × 생존, 객실 × 생존 countplot이 나란히 출력됩니다]

=== 성별 생존율 ===
sex
female    0.742
male      0.189

=== 객실 등급별 생존율 ===
pclass
1    0.630
2    0.473
3    0.242
```

> **발견**: 여성 생존율(74%)이 남성(19%)보다 훨씬 높습니다. 1등석 생존율(63%)이 3등석(24%)의 2.6배입니다.

---

<a id="part4"></a>

## 4️⃣ 다변량 분석 [↑](#toc)

> 여러 변수를 동시에 봐서 전체 그림을 파악합니다.

### pairplot — 모든 특성 쌍의 관계

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')

# 주요 수치형 변수만 선택
cols = ['survived', 'pclass', 'age', 'sibsp', 'parch', 'fare']
df_subset = df[cols].dropna()

sns.pairplot(df_subset, hue='survived', palette='RdYlGn',
             diag_kind='hist',
             plot_kws={'alpha': 0.4, 's': 15})
plt.suptitle("Titanic 주요 변수 pairplot (생존 여부 구분)", y=1.01)
plt.tight_layout()
plt.show()
```

```
실행 결과:
[6×6 격자의 pairplot — 대각선은 히스토그램, 나머지는 산점도]
[fare 열에서 생존자(녹색)와 사망자(빨강)의 분리가 어느 정도 보입니다]
```

### 다중 박스플롯 — 3차원 관계

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')

# pclass × sex × age 의 관계를 한 그래프에
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df, x='pclass', y='age', hue='sex',
            palette='Set2', ax=ax)
ax.set_title("객실 등급 × 성별별 나이 분포")
ax.set_xlabel("객실 등급")
ax.set_ylabel("나이")
plt.tight_layout()
plt.show()
```

```
실행 결과:
[3개 객실 등급 × 2개 성별로 구분된 박스플롯 6개가 나란히 출력됩니다]
```

---

<a id="part5"></a>

## 5️⃣ 이상치 탐지 [↑](#toc)

> 이상치 = 수상한 용의자 — 데이터에서 다른 값들과 크게 동떨어진 값.  
> 이상치를 무시하면 모델이 잘못된 패턴을 학습합니다.

### IQR 방법으로 이상치 탐지

```python
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')

# IQR (사분위 범위) 계산
Q1 = df['fare'].quantile(0.25)
Q3 = df['fare'].quantile(0.75)
IQR = Q3 - Q1

# 이상치 경계: Q1 - 1.5×IQR ~ Q3 + 1.5×IQR
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"Q1: {Q1:.2f}")
print(f"Q3: {Q3:.2f}")
print(f"IQR: {IQR:.2f}")
print(f"이상치 경계: {lower_bound:.2f} ~ {upper_bound:.2f}")

# 이상치 식별
outliers = df[(df['fare'] < lower_bound) | (df['fare'] > upper_bound)]
print(f"\n이상치 개수: {len(outliers)}개 ({len(outliers)/len(df)*100:.1f}%)")
print(f"이상치 요금 범위: {outliers['fare'].min():.2f} ~ {outliers['fare'].max():.2f}")
```

```
실행 결과:
Q1: 7.91
Q3: 31.00
IQR: 23.09
이상치 경계: -26.73 ~ 65.64

이상치 개수: 116개 (13.0%)
이상치 요금 범위: 69.55 ~ 512.33
```

```python
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')
Q1 = df['fare'].quantile(0.25)
Q3 = df['fare'].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR

# 시각화 — 이상치 강조
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 히스토그램 — 이상치 경계 표시
axes[0].hist(df['fare'], bins=50, color='lightblue', edgecolor='white')
axes[0].axvline(upper_bound, color='red', linestyle='--', linewidth=2,
                label=f'이상치 경계 ({upper_bound:.1f})')
axes[0].set_title("요금 분포 (이상치 경계 표시)")
axes[0].set_xlabel("요금")
axes[0].legend()

# 박스플롯 — 이상치를 점으로 표시
axes[1].boxplot(df['fare'].dropna(), patch_artist=True,
                boxprops=dict(facecolor='lightblue'))
axes[1].set_title("요금 박스플롯 (이상치=점)")
axes[1].set_ylabel("요금")

plt.tight_layout()
plt.show()
```

```
실행 결과:
[이상치 경계가 표시된 히스토그램과 박스플롯]
```

### 이상치 처리 방법

```python
import seaborn as sns
import numpy as np

df = sns.load_dataset('titanic')
Q1 = df['fare'].quantile(0.25)
Q3 = df['fare'].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR

print("이상치 처리 방법 3가지:\n")

# 방법 1: 제거
df_removed = df[df['fare'] <= upper_bound]
print(f"1. 제거: {len(df)} → {len(df_removed)}행")

# 방법 2: 상한값으로 대체 (Capping/Winsorizing)
df_capped = df.copy()
df_capped['fare'] = df_capped['fare'].clip(upper=upper_bound)
print(f"2. Capping: 최댓값 {df['fare'].max():.1f} → {df_capped['fare'].max():.1f}")

# 방법 3: 로그 변환 (오른쪽 긴 꼬리 분포에 효과적)
df_log = df.copy()
df_log['fare_log'] = np.log1p(df['fare'])  # log(1+x) — 0에 대해 안전
print(f"3. 로그 변환: 왜도 {df['fare'].skew():.2f} → {df_log['fare_log'].skew():.2f}")

print("\n어떤 방법을 쓸지는 EDA 후 도메인 지식으로 결정합니다.")
print("고액 요금은 실제 존재할 수 있음(1등석) → 제거보다 Capping 권장")
```

```
실행 결과:
이상치 처리 방법 3가지:

1. 제거: 891 → 775행
2. Capping: 최댓값 512.3 → 65.6
3. 로그 변환: 왜도 4.79 → 0.60

어떤 방법을 쓸지는 EDA 후 도메인 지식으로 결정합니다.
고액 요금은 실제 존재할 수 있음(1등석) → 제거보다 Capping 권장
```

<details>
<summary>📐 더 알아보기 — IQR 방법의 수학적 근거</summary>

**IQR (Interquartile Range, 사분위 범위)**:
```
IQR = Q3 - Q1 (75번째 백분위수 - 25번째 백분위수)
```

**Tukey의 Fence 규칙** (1977):
```
이상치: x < Q1 - 1.5×IQR  또는  x > Q3 + 1.5×IQR
극단 이상치: x < Q1 - 3×IQR  또는  x > Q3 + 3×IQR
```

**정규분포에서의 의미**:  
정규분포를 따르는 데이터에서 이 경계 밖에 있을 확률은 약 0.7%입니다.  
즉, 100개 중 0.7개 정도만 이상치로 분류됩니다.

**z-score 방법과 차이**:  
z-score (|z| > 3)는 평균과 표준편차를 사용하므로 이상치 자체에 영향받습니다.  
IQR은 중앙값 기반이라 이상치에 더 강건(robust)합니다.

</details>

---

<a id="part6"></a>

## 6️⃣ 상관관계 분석 [↑](#toc)

> "어떤 특성이 생존과 가장 관련이 깊은가?" — 상관관계로 특성의 중요도를 1차 판단합니다.

### Pearson 상관계수

```python
import seaborn as sns
import pandas as pd

df = sns.load_dataset('titanic')

# 수치형 열만 선택
numeric_df = df[['survived', 'pclass', 'age', 'sibsp', 'parch', 'fare']].dropna()

# 상관관계 행렬
corr = numeric_df.corr()

# survived와의 상관관계만 출력
print("=== survived와의 상관관계 ===")
print(corr['survived'].sort_values(ascending=False).round(3))
```

```
실행 결과:
=== survived와의 상관관계 ===
survived    1.000
fare        0.264    ← 요금 높을수록 생존 확률 높음
parch       0.082    ← 부모/자녀 수는 약한 양의 관계
age        -0.058    ← 나이 많을수록 생존 확률 약간 낮음
sibsp      -0.035    ← 형제/배우자 수는 약한 음의 관계
pclass     -0.338    ← 등급 높을수록(숫자 낮을수록) 생존 확률 높음
```

### 상관관계 heatmap

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')
numeric_df = df[['survived', 'pclass', 'age', 'sibsp', 'parch', 'fare']].dropna()
corr = numeric_df.corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr,
            annot=True,
            fmt='.2f',
            cmap='RdBu_r',
            vmin=-1, vmax=1,
            square=True,
            linewidths=0.5,
            ax=ax)
ax.set_title("Titanic 수치형 변수 상관관계 행렬")
plt.tight_layout()
plt.show()
```

```
실행 결과:
[상관관계 히트맵 — pclass와 survived 간의 음의 상관관계(-0.34)가 가장 두드러집니다]
```

### 상관관계 해석 기준

| |r| 범위 | 해석 |
|----------|------|
| 0.9 ~ 1.0 | 매우 강한 상관관계 |
| 0.7 ~ 0.9 | 강한 상관관계 |
| 0.5 ~ 0.7 | 보통 상관관계 |
| 0.3 ~ 0.5 | 약한 상관관계 |
| 0.0 ~ 0.3 | 거의 없거나 매우 약한 상관관계 |

> **주의**: 상관관계 ≠ 인과관계. `pclass`와 `survived`의 상관관계는  
> "1등석이 생존시킨다"가 아니라 "구조 우선순위와 좋은 위치 등 여러 요인"이 복합된 결과입니다.

<details>
<summary>📐 더 알아보기 — Pearson 상관계수 수식</summary>

**Pearson 상관계수 r**:
```
r(X, Y) = Σ[(Xi - X̄)(Yi - Ȳ)] / √[Σ(Xi - X̄)² × Σ(Yi - Ȳ)²]
```

- r = 1: 완벽한 양의 선형 관계
- r = -1: 완벽한 음의 선형 관계
- r = 0: 선형 관계 없음 (비선형 관계는 있을 수 있음!)

**한계**: Pearson은 선형 관계만 측정합니다.  
비선형 관계(U자형, 지수형 등)는 r이 0에 가까워도 강한 관계가 있을 수 있습니다.  
이럴 때는 Spearman 순위 상관계수를 사용합니다: `df.corr(method='spearman')`

</details>

---

<a id="part7"></a>

## 7️⃣ 실습: Titanic EDA [↑](#toc)

> 지금까지 배운 EDA 기법을 총동원해 Titanic 데이터를 분석합니다.  
> "이 데이터에서 생존에 가장 큰 영향을 준 요소는 무엇인가?"

### Step 1: 데이터 개요 파악

```python
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')

print("=== 1. 기본 정보 ===")
print(f"행 × 열: {df.shape}")
print(f"\n열 목록:\n{df.dtypes}")

print("\n=== 2. 결측치 현황 ===")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(1)
missing_info = pd.DataFrame({'결측 개수': missing, '결측 비율(%)': missing_pct})
print(missing_info[missing_info['결측 개수'] > 0])

print("\n=== 3. 수치형 변수 기초 통계 ===")
print(df[['survived', 'age', 'fare', 'pclass']].describe().round(2))
```

```
실행 결과:
=== 1. 기본 정보 ===
행 × 열: (891, 15)

=== 2. 결측치 현황 ===
         결측 개수  결측 비율(%)
age         177       19.9
embarked      2        0.2
deck        688       77.2
embark_town   2        0.2

=== 3. 수치형 변수 기초 통계 ===
       survived      age     fare   pclass
count    891.00   714.00   891.00   891.00
mean       0.38    29.70    32.20     2.31
std        0.49    14.53    49.69     0.84
...
```

### Step 2: 생존율 파악

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 전체 생존율
survival_rate = df['survived'].mean()
axes[0].bar(['사망', '생존'], [1 - survival_rate, survival_rate],
            color=['salmon', 'steelblue'])
axes[0].set_title(f"전체 생존율: {survival_rate:.1%}")
axes[0].set_ylabel("비율")
for i, (label, val) in enumerate(zip(['사망', '생존'],
                                      [1 - survival_rate, survival_rate])):
    axes[0].text(i, val + 0.01, f"{val:.1%}", ha='center', fontsize=11)

# 성별 생존율
sex_survival = df.groupby('sex')['survived'].mean()
axes[1].bar(sex_survival.index, sex_survival.values,
            color=['steelblue', 'coral'])
axes[1].set_title("성별 생존율")
axes[1].set_ylabel("생존율")
for i, (idx, val) in enumerate(sex_survival.items()):
    axes[1].text(i, val + 0.01, f"{val:.1%}", ha='center', fontsize=11)

# 객실 등급별 생존율
pclass_survival = df.groupby('pclass')['survived'].mean()
axes[2].bar(pclass_survival.index, pclass_survival.values,
            color=['gold', 'silver', '#cd7f32'])
axes[2].set_title("객실 등급별 생존율")
axes[2].set_xlabel("객실 등급")
axes[2].set_ylabel("생존율")
for i, (idx, val) in enumerate(pclass_survival.items()):
    axes[2].text(i, val + 0.01, f"{val:.1%}", ha='center', fontsize=11)

plt.tight_layout()
plt.show()
```

```
실행 결과:
[전체 생존율 38.4%, 여성 74.2% vs 남성 18.9%, 1등석 62.9% → 3등석 24.2% 바 차트]
```

### Step 3: 나이와 생존의 관계 — "어린이 우선?"

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')

# 나이 구간 생성
df['나이_구간'] = pd.cut(df['age'],
                        bins=[0, 12, 18, 35, 60, 100],
                        labels=['어린이\n(0-12)', '청소년\n(13-18)',
                                '성인\n(19-35)', '중년\n(36-60)', '노년\n(61+)'])

# 나이 구간별 생존율
age_survival = df.groupby('나이_구간', observed=True)['survived'].mean()

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 나이 구간별 생존율
axes[0].bar(age_survival.index, age_survival.values,
            color=['#2ecc71', '#3498db', '#e74c3c', '#e67e22', '#9b59b6'])
axes[0].set_title("나이 구간별 생존율")
axes[0].set_ylabel("생존율")
axes[0].set_ylim(0, 0.8)
for i, val in enumerate(age_survival.values):
    if not pd.isna(val):
        axes[0].text(i, val + 0.01, f"{val:.1%}", ha='center', fontsize=10)

# 생존/사망별 나이 분포 비교
df[df['survived'] == 1]['age'].dropna().hist(
    bins=30, alpha=0.6, color='green', label='생존', ax=axes[1])
df[df['survived'] == 0]['age'].dropna().hist(
    bins=30, alpha=0.6, color='red', label='사망', ax=axes[1])
axes[1].set_title("생존/사망별 나이 분포")
axes[1].set_xlabel("나이")
axes[1].set_ylabel("인원 수")
axes[1].legend()

plt.tight_layout()
plt.show()

print("\n=== 나이 구간별 생존율 ===")
print(age_survival.round(3))
```

```
실행 결과:
[나이 구간별 생존율 바 차트와 생존/사망 나이 분포 히스토그램]

=== 나이 구간별 생존율 ===
나이_구간
어린이(0-12)     0.590
청소년(13-18)    0.362
성인(19-35)     0.368
중년(36-60)     0.419
노년(61+)       0.091
```

### Step 4: 종합 분석 — "Women and Children First"

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset('titanic')

# 성별 × 객실 등급 × 생존율 교차 분석
pivot = df.pivot_table(values='survived', index='sex', columns='pclass', aggfunc='mean')

fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(pivot, annot=True, fmt='.1%', cmap='RdYlGn',
            vmin=0, vmax=1, ax=ax,
            annot_kws={'size': 13})
ax.set_title("성별 × 객실 등급별 생존율")
ax.set_xlabel("객실 등급")
ax.set_ylabel("성별")
plt.tight_layout()
plt.show()

print("\n=== 성별 × 객실 등급별 생존율 ===")
print(pivot.round(3))
```

```
실행 결과:
[성별×등급 생존율 heatmap — 1등석 여성 97%, 3등석 남성 14%]

=== 성별 × 객실 등급별 생존율 ===
pclass     1      2      3
sex
female  0.968  0.921  0.500
male    0.369  0.157  0.135
```

### Step 5: EDA 결론 정리

```python
print("""
╔══════════════════════════════════════════════════════════════╗
║           Titanic EDA 결론 — 생존에 영향을 준 요소들         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  1. 성별 (가장 강력한 요소)                                   ║
║     • 여성 생존율 74.2% vs 남성 18.9%                        ║
║     • "여성과 어린이 먼저" 원칙이 실제로 작동했음             ║
║                                                              ║
║  2. 객실 등급 (경제적 지위)                                   ║
║     • 1등석 62.9% vs 3등석 24.2%                            ║
║     • 상위 갑판 위치 + 우선 대피 등 복합 요인                 ║
║                                                              ║
║  3. 나이                                                     ║
║     • 어린이(0-12세) 생존율 59%로 높음                       ║
║     • 노년(61+) 생존율 9%로 가장 낮음                        ║
║                                                              ║
║  4. 요금                                                     ║
║     • 상관계수 0.26 — 등급과 연동된 간접 효과                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
```

```
실행 결과:
╔══════════════════════════════════════════════════════════════╗
║           Titanic EDA 결론 — 생존에 영향을 준 요소들         ║
...
```

---

<a id="part8"></a>

## 8️⃣ 정리 [↑](#toc)

### 핵심 개념 요약

| 개념 | 설명 | 비유 |
|------|------|------|
| EDA | 모델링 전 데이터를 시각화하고 통계로 이해하는 과정 | 탐정의 현장 수사 |
| 단변량 분석 | 하나의 변수의 분포와 특성 파악 | 용의자 한 명씩 조사 |
| 이변량 분석 | 두 변수 간의 관계 파악 | 두 용의자의 관계 파악 |
| 다변량 분석 | 여러 변수를 동시에 고려한 관계 파악 | 사건 전체 그림 보기 |
| 왜도 | 분포의 비대칭 정도 | 저울이 한쪽으로 기울어진 정도 |
| IQR | 데이터의 중간 50% 범위 (Q3-Q1) | 중간 절반의 폭 |
| 이상치 | 다른 값들과 크게 다른 극단적인 값 | 수상한 용의자 |
| Pearson 상관계수 | 두 변수의 선형 관계 강도 (-1~1) | 두 변수가 함께 움직이는 정도 |

---

### 다음 장 미리보기

데이터를 충분히 이해했습니다. 이제 첫 번째 ML 모델을 만들 차례입니다!

| 장 | 내용 |
|---|---|
| **5장** | 선형 회귀 — y = wx + b 라는 직선으로 연속값을 예측. EDA에서 발견한 패턴을 수식으로 표현합니다 |
| **7장** | 로지스틱 회귀 — Titanic EDA에서 발견한 생존 패턴을 분류 모델로 구현합니다 |

> EDA에서 발견한 것들 — "성별, 등급, 나이가 생존에 중요" — 이것이 모델의 특성(Feature)이 됩니다.  
> EDA 없이 만든 모델은 눈 감고 운전하는 것입니다.

---

### 실습 과제

**기본**: `sns.load_dataset('iris')`로 Iris 데이터를 로드하고, 각 특성(sepal_length, sepal_width, petal_length, petal_width)의 히스토그램을 4개 나란히 그려보세요.

**중급**: Titanic 데이터에서 `embarked`(탑승 항구)와 생존율의 관계를 countplot과 groupby로 분석해보세요. 어느 항구에서 탑승한 사람이 가장 높은 생존율을 보였나요? 이유를 추론해보세요.

**심화**: Titanic의 `sibsp`(형제/배우자 수), `parch`(부모/자녀 수)를 합쳐 `family_size` 열을 만들고, family_size별 생존율을 분석해보세요. 혼자 탄 사람(family_size=0)과 가족과 함께 탄 사람 중 누가 더 높은 생존율을 보였나요?

{% endraw %}


→ **다음 장**: [05. 선형 회귀](/machinelearning/linear-regression)
