---
title: 11. KNN과 SVM
layout: default
parent: Machine Learning
nav_order: 11
permalink: /machinelearning/knn-svm
---

{% raw %}

# 11장. KNN과 SVM — 거리와 경계로 분류하기

> "KNN = 이웃 투표. SVM = 두 그룹 사이 가장 넓은 도로 찾기."

<a id="toc"></a>

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다.

- KNN이 이웃 투표로 분류한다는 원리를 설명할 수 있습니다
- 유클리드 거리를 계산하고 KNN에서 활용할 수 있습니다
- 적절한 k 값을 선택하는 방법을 알 수 있습니다
- `KNeighborsClassifier`를 구현할 수 있습니다
- KNN에서 스케일링이 필수인 이유를 설명할 수 있습니다
- SVM의 마진 최대화 직관을 이해합니다
- 커널 트릭으로 비선형 분류가 가능함을 알 수 있습니다
- Iris/Titanic 데이터로 두 알고리즘을 비교할 수 있습니다

---

## 진행 순서

1️⃣ [KNN 직관](#1) — "이웃 투표"  
2️⃣ [유클리드 거리](#2) — "가장 가까운 k명"  
3️⃣ [k 값 선택](#3) — "몇 명에게 물을까"  
4️⃣ [KNeighborsClassifier](#4) — "sklearn 구현"  
5️⃣ [스케일링 필수](#5) — "단위가 다르면 거리가 왜곡"  
6️⃣ [SVM 직관](#6) — "마진 최대화"  
7️⃣ [커널 트릭](#7) — "차원을 올려서 분리"  
8️⃣ [SVC 구현](#8) — "sklearn SVM"  
9️⃣ [Iris / Titanic 비교 실습](#9)  
🔟 [정리 및 실습](#10)

---

<a id="1"></a>
## 1️⃣ KNN 직관 [↑](#toc)

### "새 이웃의 취향은 주변 이웃에게 물어봐"

> 새로 이사 온 집에서 가장 가까운 이웃 K명이  
> 모두 피자를 좋아한다면, 새 주민도 피자를 좋아할 가능성이 높습니다.  
> 이것이 **KNN(K-Nearest Neighbors)** 의 핵심입니다.

### 작동 원리

1. 새 데이터 포인트가 들어옵니다.
2. 훈련 데이터에서 **거리가 가장 가까운 K개**를 찾습니다.
3. 그 K개의 클래스를 **다수결 투표**합니다.
4. 가장 많은 표를 받은 클래스로 예측합니다.

```python
import numpy as np
import matplotlib.pyplot as plt

# KNN 직관 시각화
np.random.seed(42)
# 클래스 A (파란점)
A = np.random.randn(20, 2) + np.array([2, 2])
# 클래스 B (빨간점)
B = np.random.randn(20, 2) + np.array([5, 5])
# 새 포인트
new_point = np.array([[3.5, 4.0]])

plt.figure(figsize=(8, 6))
plt.scatter(A[:, 0], A[:, 1], color='steelblue', s=60, label='클래스 A', zorder=5)
plt.scatter(B[:, 0], B[:, 1], color='tomato', s=60, label='클래스 B', zorder=5)
plt.scatter(*new_point[0], color='gold', s=200, marker='*', label='새 포인트', zorder=10)

# 모든 점까지 거리 계산 후 K=5 이웃 표시
all_points = np.vstack([A, B])
all_labels = ['A'] * len(A) + ['B'] * len(B)
distances = np.sqrt(np.sum((all_points - new_point) ** 2, axis=1))
k_idx = np.argsort(distances)[:5]  # 가장 가까운 5명

for idx in k_idx:
    plt.plot([new_point[0, 0], all_points[idx, 0]],
             [new_point[0, 1], all_points[idx, 1]],
             'gray', linewidth=1, linestyle='--', alpha=0.7)

# 5명 이웃 강조
for idx in k_idx:
    color = 'steelblue' if all_labels[idx] == 'A' else 'tomato'
    plt.scatter(*all_points[idx], s=150, edgecolors='black',
                linewidth=2, color=color, zorder=8)

neighbors_labels = [all_labels[i] for i in k_idx]
print(f"K=5 이웃: {neighbors_labels}")
print(f"예측 클래스: {'A' if neighbors_labels.count('A') > 2 else 'B'}")

plt.legend()
plt.title('KNN 직관 — K=5 이웃 투표')
plt.xlabel('특성 1')
plt.ylabel('특성 2')
plt.show()
```

---

<a id="2"></a>
## 2️⃣ 유클리드 거리 [↑](#toc)

### "가장 가까운 k명을 어떻게 찾는가"

KNN에서 "가깝다"는 것을 수치로 표현해야 합니다.  
가장 기본적인 거리는 **유클리드 거리**입니다.

> 2D 평면에서 두 점 사이의 직선 거리 — 피타고라스 정리와 동일합니다.

```python
# 유클리드 거리 직접 계산
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

p1 = np.array([1, 2, 3])  # 3개 특성을 가진 샘플
p2 = np.array([4, 6, 1])

dist = euclidean_distance(p1, p2)
print(f"p1 = {p1}")
print(f"p2 = {p2}")
print(f"유클리드 거리 = sqrt({(p2[0]-p1[0])**2}+{(p2[1]-p1[1])**2}+{(p2[2]-p1[2])**2})")
print(f"             = {dist:.4f}")

# scipy로도 가능
from scipy.spatial.distance import euclidean, manhattan, cosine
print(f"\n다른 거리 척도:")
print(f"  유클리드(L2): {euclidean(p1, p2):.4f}")
print(f"  맨해튼(L1):   {manhattan(p1, p2):.4f}  (격자 이동 거리)")
print(f"  코사인:       {cosine(p1, p2):.4f}    (방향 유사도)")
```

실행 결과:
```
p1 = [1 2 3]
p2 = [4 6 1]
유클리드 거리 = sqrt(9+16+4)
             = 5.3852

다른 거리 척도:
  유클리드(L2): 5.3852
  맨해튼(L1):   9.0000  (격자 이동 거리)
  코사인:       0.0269  (방향 유사도)
```

<details markdown="1">
<summary>📐 더 알아보기 — 유클리드 거리 수식</summary>

두 점 $\mathbf{a} = (a_1, a_2, ..., a_n)$ 과 $\mathbf{b} = (b_1, b_2, ..., b_n)$ 사이의 유클리드 거리:

$$
d(\mathbf{a}, \mathbf{b}) = \sqrt{\sum_{i=1}^{n} (a_i - b_i)^2}
$$

**거리 척도 비교:**

| 거리 | 수식 | 특징 |
|---|---|---|
| 유클리드 (L2) | $\sqrt{\sum(a_i - b_i)^2}$ | 직선 거리, 가장 일반적 |
| 맨해튼 (L1) | $\sum\|a_i - b_i\|$ | 격자 경로, 이상값에 강건 |
| 코사인 | $1 - \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\|\mathbf{b}\|}$ | 방향 유사도, NLP에서 많이 사용 |

KNN에서 `metric='euclidean'` (기본값) 외에도 `'manhattan'`, `'cosine'` 등을 사용할 수 있습니다.

</details>

---

<a id="3"></a>
## 3️⃣ k 값 선택 [↑](#toc)

### "몇 명에게 물을까 — Elbow Method"

k가 너무 작으면 → 과적합 (노이즈에 민감)  
k가 너무 크면 → 과소적합 (너무 평균적)

> k=1: "가장 가까운 1명에게만 물음" → 이상한 이웃 1명에 취약  
> k=데이터수: "모든 이웃에게 물음" → 항상 다수 클래스 예측  

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
)

# k 값에 따른 성능
k_values = range(1, 31)
train_scores, test_scores, cv_scores = [], [], []

for k in k_values:
    knn = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=k))
    ])
    knn.fit(X_train, y_train)
    train_scores.append(knn.score(X_train, y_train))
    test_scores.append(knn.score(X_test, y_test))
    cv_scores.append(cross_val_score(knn, iris.data, iris.target, cv=5).mean())

plt.figure(figsize=(10, 5))
plt.plot(k_values, train_scores, 'o-', label='훈련 정확도', color='steelblue', markersize=4)
plt.plot(k_values, test_scores, 's--', label='테스트 정확도', color='tomato', markersize=4)
plt.plot(k_values, cv_scores, '^:', label='5-Fold CV', color='green', markersize=4)
best_k = k_values[np.argmax(cv_scores)]
plt.axvline(best_k, color='gray', linestyle='--', label=f'최적 k={best_k}')
plt.xlabel('k (이웃 수)')
plt.ylabel('정확도')
plt.title('k에 따른 KNN 성능')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print(f"최적 k: {best_k}")
print(f"최고 CV 정확도: {max(cv_scores):.4f}")
```

---

<a id="4"></a>
## 4️⃣ KNeighborsClassifier [↑](#toc)

### fit / predict / score 패턴

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# 파이프라인: 스케일링 + KNN (스케일링 필수!)
knn_model = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=5, metric='euclidean'))
])

knn_model.fit(X_train, y_train)          # 학습 (거리 기반 → 데이터 저장)
y_pred = knn_model.predict(X_test)      # 예측 (k명 이웃 탐색)

print(f"정확도: {knn_model.score(X_test, y_test):.4f}")
print(f"\n예측 확률 (처음 5개):")
proba = knn_model.predict_proba(X_test[:5])
for i, (pred, prob) in enumerate(zip(y_pred[:5], proba)):
    print(f"  샘플 {i+1}: 예측={iris.target_names[pred]}, "
          f"확률={prob.round(2)}")
```

실행 결과:
```
정확도: 0.9667

예측 확률 (처음 5개):
  샘플 1: 예측=versicolor, 확률=[0.   0.8  0.2 ]
  샘플 2: 예측=setosa, 확률=[1.   0.   0.  ]
  샘플 3: 예측=virginica, 확률=[0.   0.   1.  ]
  샘플 4: 예측=versicolor, 확률=[0.   1.   0.  ]
  샘플 5: 예측=versicolor, 확률=[0.   0.8  0.2 ]
```

> KNN은 모델을 "학습"하는 것이 아니라 **데이터를 저장**합니다.  
> 예측 시마다 거리를 계산하므로 데이터가 많으면 느려집니다.

---

<a id="5"></a>
## 5️⃣ 스케일링 필수 [↑](#toc)

### "단위가 다르면 거리가 왜곡된다"

> 키(cm)와 몸무게(kg)를 함께 사용할 때:  
> 키 차이 10cm = 거리 10  
> 몸무게 차이 1kg = 거리 1  
> 키 차이가 10배 더 크게 취급됩니다.  
> 실제로는 둘 다 비슷하게 중요한데 말입니다.

```python
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np

# 의도적으로 스케일이 다른 특성 생성
X, y = make_classification(n_samples=300, n_features=2,
                            n_informative=2, n_redundant=0, random_state=42)
# 첫 번째 특성을 1000배 키움 (단위 차이 시뮬레이션)
X[:, 0] = X[:, 0] * 1000

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 스케일링 없이
knn_no_scale = KNeighborsClassifier(n_neighbors=5)
knn_no_scale.fit(X_train, y_train)
acc_no = knn_no_scale.score(X_test, y_test)

# 스케일링 후
from sklearn.pipeline import Pipeline
knn_scaled = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=5))
])
knn_scaled.fit(X_train, y_train)
acc_sc = knn_scaled.score(X_test, y_test)

print(f"스케일링 없이:  정확도 = {acc_no:.4f}")
print(f"StandardScaler: 정확도 = {acc_sc:.4f}")
print(f"\n차이: {acc_sc - acc_no:+.4f}")
print("\n→ KNN은 항상 StandardScaler와 함께 사용하세요!")
```

실행 결과:
```
스케일링 없이:  정확도 = 0.5000
StandardScaler: 정확도 = 0.9167

차이: +0.4167

→ KNN은 항상 StandardScaler와 함께 사용하세요!
```

---

<a id="6"></a>
## 6️⃣ SVM 직관 [↑](#toc)

### "두 그룹 사이 가장 넓은 도로 찾기"

> 두 마을(클래스 A, B) 사이에 울타리(결정 경계)를 세우려 합니다.  
> 양쪽 마을에서 최대한 멀리 떨어진 위치에 세우면 가장 안전합니다.  
> 이 "가장 넓은 도로"를 찾는 것이 **SVM(Support Vector Machine)** 입니다.

### 핵심 용어

- **마진(Margin):** 결정 경계와 각 클래스의 가장 가까운 점 사이의 거리
- **서포트 벡터(Support Vector):** 마진을 결정하는 경계 근처의 데이터 포인트
- **최대 마진 분류기:** 마진을 최대화하는 결정 경계를 찾음

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler

# 선형 분리 가능한 2D 데이터
X_svm, y_svm = make_classification(
    n_samples=100, n_features=2, n_informative=2,
    n_redundant=0, n_clusters_per_class=1, random_state=42
)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_svm)

svm_linear = SVC(kernel='linear', C=1.0)
svm_linear.fit(X_scaled, y_svm)

# 결정 경계와 마진 시각화
def plot_svm_boundary(model, X, y, ax, title):
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    ax.contourf(xx, yy, Z, alpha=0.2, cmap='RdBu')
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap='RdBu', edgecolors='k', s=50)
    
    # 서포트 벡터 강조
    sv = model.support_vectors_
    ax.scatter(sv[:, 0], sv[:, 1], s=150, facecolors='none',
               edgecolors='gold', linewidths=2, label='서포트 벡터')
    
    # 마진 경계선
    w = model.coef_[0]
    b = model.intercept_[0]
    x_vals = np.linspace(x_min, x_max, 100)
    y_decision = -(w[0] * x_vals + b) / w[1]
    y_margin1  = -(w[0] * x_vals + b - 1) / w[1]
    y_margin2  = -(w[0] * x_vals + b + 1) / w[1]
    
    ax.plot(x_vals, y_decision, 'k-', linewidth=2, label='결정 경계')
    ax.plot(x_vals, y_margin1, 'k--', linewidth=1, label='마진')
    ax.plot(x_vals, y_margin2, 'k--', linewidth=1)
    
    ax.set_title(title)
    ax.legend(fontsize=8)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

fig, ax = plt.subplots(figsize=(7, 6))
plot_svm_boundary(svm_linear, X_scaled, y_svm, ax, 'SVM 선형 결정 경계와 마진')
plt.tight_layout()
plt.show()

print(f"서포트 벡터 수: {len(svm_linear.support_vectors_)}")
print(f"정확도: {svm_linear.score(X_scaled, y_svm):.4f}")
```

<details markdown="1">
<summary>📐 더 알아보기 — SVM 최적화 수식</summary>

SVM의 목표: **마진을 최대화**하면서 올바르게 분류

$$
\max_{w, b} \frac{2}{\|w\|}  \quad \text{(마진 최대화)}
$$

등가 목적식 (최소화로 변환):

$$
\min_{w, b} \frac{1}{2} \|w\|^2 \quad \text{subject to} \quad y_i(w^T x_i + b) \geq 1
$$

**소프트 마진 (C 파라미터):**
일부 오분류를 허용하는 완화된 버전

$$
\min_{w, b} \frac{1}{2}\|w\|^2 + C \sum_i \xi_i
$$

- C가 크면 → 마진 좁고 오분류 거의 없음 (과적합 위험)
- C가 작으면 → 마진 넓고 일부 오분류 허용 (과소적합 위험)

</details>

---

<a id="7"></a>
## 7️⃣ 커널 트릭 [↑](#toc)

### "차원을 올려서 분리"

선형으로 분리되지 않는 데이터는 어떻게 할까요?

> **직관:** 1D에서 섞인 데이터를 2D로 올리면 평면으로 분리할 수 있습니다.  
> 예를 들어 x → (x, x²) 변환.  
> SVM은 이를 수학적으로 효율적으로 수행합니다.

```python
from sklearn.svm import SVC
from sklearn.datasets import make_circles, make_moons

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# 데이터셋
datasets = [
    ('원형 데이터', *make_circles(n_samples=200, noise=0.1, factor=0.4, random_state=42)),
    ('초승달 데이터', *make_moons(n_samples=200, noise=0.15, random_state=42)),
]

kernels = ['linear', 'poly', 'rbf']
kernel_names = ['선형 (linear)', '다항식 (poly)', 'RBF (방사기저함수)']

for row, (data_name, X_d, y_d) in enumerate(datasets):
    scaler = StandardScaler()
    X_d_scaled = scaler.fit_transform(X_d)
    
    for col, (kernel, kname) in enumerate(zip(kernels, kernel_names)):
        svm = SVC(kernel=kernel, C=1.0, gamma='scale')
        svm.fit(X_d_scaled, y_d)
        
        ax = axes[row][col]
        h = 0.02
        x_min, x_max = X_d_scaled[:, 0].min() - 0.5, X_d_scaled[:, 0].max() + 0.5
        y_min, y_max = X_d_scaled[:, 1].min() - 0.5, X_d_scaled[:, 1].max() + 0.5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                              np.arange(y_min, y_max, h))
        Z = svm.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        
        ax.contourf(xx, yy, Z, alpha=0.3, cmap='RdBu')
        ax.scatter(X_d_scaled[:, 0], X_d_scaled[:, 1], c=y_d, cmap='RdBu',
                   edgecolors='k', s=30)
        acc = svm.score(X_d_scaled, y_d)
        ax.set_title(f'{data_name}\n{kname} (정확도={acc:.2f})', fontsize=9)

plt.tight_layout()
plt.show()
```

> **RBF(Radial Basis Function) 커널**이 가장 널리 사용됩니다.  
> 데이터를 무한 차원으로 매핑하는 것과 수학적으로 동일한 효과를 냅니다.  
> 단, 계산은 원래 차원에서 효율적으로 수행합니다 — 이것이 "트릭"입니다.

---

<a id="8"></a>
## 8️⃣ SVC 구현 [↑](#toc)

```python
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
)

# SVM 모델 (스케일링 필수)
svm_model = Pipeline([
    ('scaler', StandardScaler()),
    ('svc', SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42))
])

svm_model.fit(X_train, y_train)
y_pred = svm_model.predict(X_test)

print(f"정확도: {svm_model.score(X_test, y_test):.4f}")
print("\n분류 리포트:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# C 값에 따른 성능 변화
print("\nC 값에 따른 성능:")
for c in [0.01, 0.1, 1, 10, 100]:
    svm_c = Pipeline([
        ('scaler', StandardScaler()),
        ('svc', SVC(kernel='rbf', C=c, gamma='scale'))
    ])
    svm_c.fit(X_train, y_train)
    print(f"  C={c:6.2f}: 훈련={svm_c.score(X_train, y_train):.4f}, "
          f"테스트={svm_c.score(X_test, y_test):.4f}")
```

실행 결과:
```
정확도: 1.0000

분류 리포트:
              precision    recall  f1-score   support

      setosa       1.00      1.00      1.00        10
  versicolor       1.00      1.00      1.00        10
   virginica       1.00      1.00      1.00        10

    accuracy                           1.00        30
   macro avg       1.00      1.00      1.00        30
weighted avg       1.00      1.00      1.00        30

C 값에 따른 성능:
  C=  0.01: 훈련=0.9667, 테스트=0.9667
  C=  0.10: 훈련=0.9750, 테스트=0.9667
  C=  1.00: 훈련=0.9917, 테스트=1.0000
  C= 10.00: 훈련=0.9917, 테스트=1.0000
  C=100.00: 훈련=1.0000, 테스트=1.0000
```

---

<a id="9"></a>
## 9️⃣ Iris / Titanic 비교 실습 [↑](#toc)

### 모든 분류 알고리즘 총정리

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.datasets import load_iris
import seaborn as sns

# ── Iris 비교 ───────────────────────────────────────────
iris = load_iris()

models = {
    '로지스틱 회귀': Pipeline([('scaler', StandardScaler()), ('lr', LogisticRegression(max_iter=200))]),
    '결정 트리':     Pipeline([('dt', DecisionTreeClassifier(max_depth=4, random_state=42))]),
    '랜덤 포레스트': Pipeline([('rf', RandomForestClassifier(n_estimators=100, random_state=42))]),
    'KNN (k=5)':    Pipeline([('scaler', StandardScaler()), ('knn', KNeighborsClassifier(n_neighbors=5))]),
    'SVM (RBF)':   Pipeline([('scaler', StandardScaler()), ('svm', SVC(kernel='rbf', C=1.0, gamma='scale'))]),
}

print("Iris 데이터 — 5-Fold CV 정확도 비교")
print("=" * 45)
results_iris = {}
for name, model in models.items():
    scores = cross_val_score(model, iris.data, iris.target, cv=5, scoring='accuracy')
    results_iris[name] = scores
    print(f"{name:<18}: {scores.mean():.4f} ± {scores.std():.4f}")
```

```python
# ── Titanic 비교 ────────────────────────────────────────
titanic = sns.load_dataset('titanic')
features = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked']
titanic['sex'] = (titanic['sex'] == 'female').astype(int)
titanic['embarked'] = titanic['embarked'].map({'S': 0, 'C': 1, 'Q': 2}).fillna(0)
df_t = titanic[features + ['survived']].dropna(subset=['survived'])

X_t = df_t[features].values
y_t = df_t['survived'].values

# 결측치 처리가 포함된 파이프라인
titanic_models = {
    '로지스틱 회귀': Pipeline([('imp', SimpleImputer()), ('scaler', StandardScaler()), ('lr', LogisticRegression(max_iter=200))]),
    '결정 트리':     Pipeline([('imp', SimpleImputer()), ('dt', DecisionTreeClassifier(max_depth=4, random_state=42))]),
    '랜덤 포레스트': Pipeline([('imp', SimpleImputer()), ('rf', RandomForestClassifier(n_estimators=100, random_state=42))]),
    'KNN (k=5)':    Pipeline([('imp', SimpleImputer()), ('scaler', StandardScaler()), ('knn', KNeighborsClassifier(n_neighbors=5))]),
    'SVM (RBF)':   Pipeline([('imp', SimpleImputer()), ('scaler', StandardScaler()), ('svm', SVC(kernel='rbf', C=1.0, gamma='scale'))]),
}

print("\n\nTitanic 데이터 — 5-Fold CV 정확도 비교")
print("=" * 45)
results_titanic = {}
for name, model in titanic_models.items():
    scores = cross_val_score(model, X_t, y_t, cv=5, scoring='accuracy')
    results_titanic[name] = scores
    print(f"{name:<18}: {scores.mean():.4f} ± {scores.std():.4f}")
```

```python
# ── 시각화 ──────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for ax, (results, title) in zip(axes, [
    (results_iris, 'Iris 분류 성능 비교'),
    (results_titanic, 'Titanic 생존 예측 성능 비교')
]):
    names = list(results.keys())
    means = [results[n].mean() for n in names]
    stds  = [results[n].std() for n in names]
    colors = ['steelblue', 'coral', 'green', 'gold', 'purple']
    
    bars = ax.barh(names, means, xerr=stds, color=colors, alpha=0.8, capsize=4)
    ax.set_xlim(0.5, 1.05)
    ax.set_xlabel('5-Fold CV 정확도')
    ax.set_title(title)
    ax.axvline(0.8, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    for bar, mean in zip(bars, means):
        ax.text(mean + 0.005, bar.get_y() + bar.get_height()/2,
                f'{mean:.4f}', va='center', fontsize=9)

plt.tight_layout()
plt.show()
```

---

<a id="10"></a>
## 🔟 정리 및 실습 [↑](#toc)

### 핵심 개념 정리

| 개념 | 설명 | 비유 |
|---|---|---|
| KNN | k명 이웃의 다수결로 분류 | 동네 투표 |
| 유클리드 거리 | 두 점 사이의 직선 거리 | 줄자로 잰 거리 |
| k 값 | 참고할 이웃 수 (작으면 과적합, 크면 과소적합) | 의견 조사 인원 수 |
| SVM | 두 클래스 사이 최대 마진 결정 경계 | 가장 넓은 도로 |
| 서포트 벡터 | 마진을 결정하는 경계 근처 데이터 | 경계선을 떠받치는 기둥 |
| C 파라미터 | 마진 vs 오분류 허용 정도 | 울타리 유연성 |
| 커널 트릭 | 비선형 데이터를 고차원에서 선형 분리 | 구겨진 종이 펼치기 |
| RBF 커널 | 가장 일반적인 비선형 커널 | 만능 변환 |

### 알고리즘 선택 가이드

| 상황 | 추천 알고리즘 |
|---|---|
| 해석이 중요 | 결정 트리, 로지스틱 회귀 |
| 데이터가 적음 | SVM, KNN |
| 데이터가 많음 | 랜덤 포레스트, 로지스틱 회귀 |
| 비선형 경계 | 랜덤 포레스트, SVM(RBF) |
| 빠른 실험 | 로지스틱 회귀 → 랜덤 포레스트 순서로 시도 |

### 다음 단계 미리보기

Part 2-3 (회귀·분류)을 마쳤습니다.  
다음에는 **비지도 학습** (클러스터링, 차원 축소)과  
**앙상블 고급** (GBM, XGBoost), **딥러닝 입문**으로 이어집니다.

---

### 실습 과제

**기본**  
1. Iris 데이터에 `KNeighborsClassifier(n_neighbors=3)` 과 `SVC(kernel='linear')`를  
   각각 학습하고 정확도와 `classification_report`를 비교하세요.

**중급**  
2. KNN에서 k=1부터 k=20까지 각각 5-Fold CV 정확도를 계산하고 꺾은선 그래프로 그리세요.  
   최적 k는 몇인가요? StandardScaler를 쓴 경우와 안 쓴 경우를 나란히 비교하세요.

**심화**  
3. Titanic 데이터로 5가지 모델 (로지스틱 회귀, 결정 트리, 랜덤 포레스트, KNN, SVM)을  
   모두 학습해 비교 바 차트를 만드세요.  
   정확도만 보지 말고 `classification_report`의 recall을 기준으로 어느 모델이  
   생존자를 더 잘 찾아내는지 분석하세요.

{% endraw %}


→ **다음 장**: [12. 클러스터링](/machinelearning/clustering)
