---
title: 5. 모델 성능 평가
layout: default
parent: DeepLearning
nav_order: 5
permalink: /deeplearning/evaluation
# nav_exclude: true
# search_exclude: true
---
# 5. 모델 성능 평가

## 학습 목표

1. 이진분류, 다중분류, 회귀에 사용하는 평가 방법을 구별하여 사용할 수 있다.
2. 분류에서는 정확도만으로는 모델 성능을 충분히 설명할 수 없음을 불균형 데이터 사례로 설명할 수 있다.
3. Accuracy, Precision, Recall, F1 Score, Confusion Matrix, ROC-AUC, MAE, MSE, RMSE, R² 의 역할을 구분할 수 있다.


<a id="toc"></a>

## 진행 순서

1. [기본 환경 확인 및 한글 폰트 셋팅](#part1)
2. [평가 지표](#part2)
3. [분류 모델 평가](#part3)
4. [회귀 모델 평가](#part4)
5. [종합 정리](#part5)

---
<a id="part1"></a>

## 1. 기본 환경 확인 및 한글 폰트 셋팅 [↑](#toc)

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, random_split
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import os, subprocess

torch.manual_seed(42)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Colab 한글 폰트 설정
if 'COLAB_RELEASE_TAG' in os.environ:
    subprocess.run(['apt-get', '-qq', '-y', 'install', 'fonts-nanum'],
                   capture_output=True)
    import matplotlib.font_manager as fm
    for f in fm.findSystemFonts(['/usr/share/fonts/truetype/nanum']):
        fm.fontManager.addfont(f)
    plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

print("PyTorch version:", torch.__version__)
print("Device:", device)
```

**출력:**
```
PyTorch version: 2.10.0+cpu
Device: cpu
```

---

<a id="part2"></a>

## 2. 평가 지표 [↑](#toc)

| 문제 유형 | 핵심 질문 | 주요 지표 |
|----------|----------|----------|
| **분류** | 정답 클래스를 맞혔는가? | Accuracy, Precision, Recall, F1, Confusion Matrix, ROC-AUC |
| **회귀** | 예측값이 실제값에 얼마나 가까운가? | MAE, MSE, RMSE, R² |

### 왜 Accuracy만으로는 부족한가?

1,000명 중 암 환자 10명인 데이터에서 "모두 정상"이라고 예측하면:
- **Accuracy = 99.0%** → 숫자만 보면 훌륭해 보인다
- **암 환자 발견율(Recall) = 0%** → 실제로는 쓸모없는 모델이다

높은 Accuracy가 좋은 모델을 의미하지 않습니다. 이것이 **다양한 평가 지표가 필요한 이유**입니다.

---

<a id="part3"></a>

## 3. 분류 모델 평가 [↑](#toc)

**FashionMNIST** 데이터셋을 사용합니다.

- **B1. 다중 분류 (10클래스)**: Accuracy, Per-class Recall, Confusion Matrix
- **B2. 이진 분류 (2클래스)**: Precision, Recall, F1, Threshold 분석, ROC-AUC

```python
# ===== FashionMNIST 데이터 로드 =====
transform = transforms.ToTensor()  # [0, 255] -> [0.0, 1.0]

train_full = datasets.FashionMNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.FashionMNIST(root='./data', train=False, download=True, transform=transform)

# Train / Val 분할 (50,000 / 10,000)
cls_train, cls_val = random_split(
    train_full, [50000, 10000],
    generator=torch.Generator().manual_seed(42)
)

cls_train_loader = DataLoader(cls_train, batch_size=128, shuffle=True)
cls_val_loader = DataLoader(cls_val, batch_size=256, shuffle=False)
cls_test_loader = DataLoader(test_dataset, batch_size=256, shuffle=False)

class_names = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

print(f"Train: {len(cls_train)}, Val: {len(cls_val)}, Test: {len(test_dataset)}")

# 클래스별 샘플 이미지
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
for i, ax in enumerate(axes.flat):
    idx = (train_full.targets == i).nonzero(as_tuple=True)[0][0].item()
    image, label = train_full[idx]
    ax.imshow(image.squeeze(), cmap='gray')
    ax.set_title(class_names[label])
    ax.axis('off')
plt.suptitle('FashionMNIST Classes', fontsize=14)
plt.tight_layout()
plt.show()
```

**출력:**
```
Train: 50000, Val: 10000, Test: 10000
```

---

### B1. 다중 분류 평가 (10클래스)

FashionMNIST 전체 10개 클래스를 분류하는 MLP를 학습하고 평가합니다.

```python
# ===== 다중 분류 모델 정의 =====
cls_model = nn.Sequential(
    nn.Flatten(),                         # (N, 1, 28, 28) -> (N, 784)
    nn.Linear(784, 256), nn.ReLU(),       # 은닉층 1
    nn.Linear(256, 128), nn.ReLU(),       # 은닉층 2
    nn.Linear(128, 10)                    # 출력층 (10클래스)
).to(device)

cls_loss_fn = nn.CrossEntropyLoss()
cls_optimizer = torch.optim.Adam(cls_model.parameters(), lr=0.001)

# ===== 학습 =====
cls_history = {'train_loss': [], 'val_loss': [], 'val_acc': []}

for epoch in range(1, 11):
    # --- 학습 ---
    cls_model.train()
    train_loss, train_count = 0.0, 0
    for xb, yb in cls_train_loader:
        xb, yb = xb.to(device), yb.to(device)
        cls_optimizer.zero_grad()
        logits = cls_model(xb)
        loss = cls_loss_fn(logits, yb)
        loss.backward()
        cls_optimizer.step()
        train_loss += loss.item() * len(xb)
        train_count += len(xb)

    # --- 검증 ---
    cls_model.eval()
    val_loss, val_count, val_correct = 0.0, 0, 0
    with torch.inference_mode():
        for xb, yb in cls_val_loader:
            xb, yb = xb.to(device), yb.to(device)
            logits = cls_model(xb)
            loss = cls_loss_fn(logits, yb)
            val_loss += loss.item() * len(xb)
            val_count += len(xb)
            val_correct += (logits.argmax(1) == yb).sum().item()

    cls_history['train_loss'].append(train_loss / train_count)
    cls_history['val_loss'].append(val_loss / val_count)
    cls_history['val_acc'].append(val_correct / val_count)

    if epoch % 2 == 0:
        print(f"Epoch {epoch:2d} | "
              f"train_loss={train_loss/train_count:.4f} "
              f"val_loss={val_loss/val_count:.4f} "
              f"val_acc={val_correct/val_count:.4f}")
```

**출력:**
```
Epoch  2 | train_loss=0.4015 val_loss=0.3758 val_acc=0.8660
Epoch  4 | train_loss=0.3271 val_loss=0.3403 val_acc=0.8770
Epoch  6 | train_loss=0.2900 val_loss=0.3049 val_acc=0.8859
Epoch  8 | train_loss=0.2655 val_loss=0.3191 val_acc=0.8815
Epoch 10 | train_loss=0.2423 val_loss=0.2893 val_acc=0.8946
```

```python
# ===== 학습 곡선 =====
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

epochs = range(1, len(cls_history['train_loss']) + 1)
ax1.plot(epochs, cls_history['train_loss'], 'b-o', label='Train Loss')
ax1.plot(epochs, cls_history['val_loss'], 'r-o', label='Val Loss')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.set_title('Loss Curve')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(epochs, cls_history['val_acc'], 'g-o', label='Val Accuracy')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy')
ax2.set_title('Validation Accuracy')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

#### 다중 분류 평가 지표

| 지표 | 수식 | 의미 |
|------|------|------|
| **Accuracy** | 맞힌 수 / 전체 수 | 전체 정답률 |
| **Per-class Recall** | TP_c / (TP_c + FN_c) | 클래스 c의 실제 데이터 중 맞힌 비율 |
| **Macro Recall** | 클래스별 Recall의 평균 | 모든 클래스를 동등하게 반영 |
| **Confusion Matrix** | (i, j) = 실제 i를 j로 예측한 횟수 | 모델의 혼동 패턴을 한눈에 파악 |

> **Accuracy가 높아도 특정 클래스의 Recall이 낮을 수 있습니다.** Confusion Matrix로 어떤 클래스끼리 혼동하는지 확인해야 합니다.

```python
# ===== 다중 분류 테스트 평가 =====
cls_model.eval()
all_logits, all_targets = [], []

with torch.inference_mode():
    for xb, yb in cls_test_loader:
        xb = xb.to(device)
        logits = cls_model(xb)
        all_logits.append(logits.cpu())
        all_targets.append(yb)

all_logits = torch.cat(all_logits)
all_targets = torch.cat(all_targets)
all_preds = all_logits.argmax(dim=1)

# --- Accuracy ---
accuracy = (all_preds == all_targets).float().mean().item()
print(f"Test Accuracy: {accuracy:.4f}")

# --- Confusion Matrix ---
num_classes = 10
cm = torch.zeros(num_classes, num_classes, dtype=torch.int64)
for t, p in zip(all_targets, all_preds):
    cm[t.long(), p.long()] += 1

# --- Per-class Precision / Recall / F1 ---
print(f"\nMacro Recall: {(cm.diag().float() / cm.sum(dim=1).clamp(min=1).float()).mean().item():.4f}")
print(f"\n{'Class':<12} {'Precision':>10} {'Recall':>10} {'F1':>10} {'Support':>10}")
print("-" * 57)

for c in range(num_classes):
    tp = cm[c, c].item()
    fn = (cm[c, :].sum() - tp).item()
    fp = (cm[:, c].sum() - tp).item()
    support = cm[c, :].sum().item()
    prec = tp / max(tp + fp, 1)
    rec  = tp / max(tp + fn, 1)
    f1   = 2 * prec * rec / max(prec + rec, 1e-8)
    print(f"{class_names[c]:<12} {prec:>10.4f} {rec:>10.4f} {f1:>10.4f} {support:>10.0f}")
```

**출력:**
```
Test Accuracy: 0.8878

Macro Recall: 0.8878

Class         Precision     Recall         F1    Support
---------------------------------------------------------
T-shirt          0.8455     0.8540     0.8498       1000
Trouser          0.9949     0.9690     0.9818       1000
Pullover         0.7759     0.8310     0.8025       1000
Dress            0.8813     0.9060     0.8935       1000
Coat             0.8215     0.7730     0.7965       1000
Sandal           0.9746     0.9600     0.9673       1000
Shirt            0.7117     0.7060     0.7088       1000
Sneaker          0.9340     0.9620     0.9478       1000
Bag              0.9856     0.9600     0.9726       1000
Ankle boot       0.9618     0.9570     0.9594       1000
```

```python
# ===== Confusion Matrix 시각화 =====
fig, ax = plt.subplots(figsize=(9, 7))
im = ax.imshow(cm.float(), cmap='Blues')

ax.set_xticks(range(num_classes))
ax.set_yticks(range(num_classes))
ax.set_xticklabels(class_names, rotation=45, ha='right')
ax.set_yticklabels(class_names)
ax.set_xlabel('Predicted')
ax.set_ylabel('True')
ax.set_title('FashionMNIST Confusion Matrix')

for i in range(num_classes):
    for j in range(num_classes):
        val = cm[i, j].item()
        color = 'white' if val > cm.max().item() * 0.5 else 'black'
        ax.text(j, i, str(val), ha='center', va='center', color=color, fontsize=8)

plt.colorbar(im)
plt.tight_layout()
plt.show()
```

---

#### 다중 분류 해석 가이드

**Confusion Matrix 읽는 법:**
- **대각선 (진한 칸)**: 정확하게 분류한 데이터
- **비대각선 (밝은 칸 중 값이 큰 곳)**: 모델이 자주 혼동하는 쌍

**FashionMNIST에서 자주 나타나는 혼동 패턴:**
- Shirt ↔ T-shirt ↔ Pullover ↔ Coat : 상의류끼리 시각적으로 유사
- Sneaker ↔ Ankle boot : 신발류끼리 유사

> 특정 클래스의 Recall이 낮다면, 해당 클래스 데이터를 더 수집하거나 모델 구조를 개선하는 방향을 검토합니다.

---

### B2. 이진 분류 평가

FashionMNIST에서 시각적으로 유사한 **Sneaker(7)**와 **Ankle boot(9)**만 추출하여 이진 분류기를 학습합니다.

#### Precision / Recall / F1 Score

| 지표 | 수식 | 의미 | 중요한 경우 |
|------|------|------|-----------|
| **Precision** | TP / (TP + FP) | 양성이라 한 것 중 실제 양성 비율 | FP 비용이 클 때 (스팸 필터) |
| **Recall** | TP / (TP + FN) | 실제 양성 중 찾아낸 비율 | FN 비용이 클 때 (암 진단) |
| **F1** | 2 × P × R / (P + R) | Precision과 Recall의 조화평균 | 둘 다 중요할 때 |

**직관적 비유:**
- **Precision** = 잡은 물고기 중 먹을 수 있는 비율 (쓰레기를 많이 건지면 낮아짐)
- **Recall** = 바다의 먹을 수 있는 물고기 중 실제로 잡은 비율 (많이 놓치면 낮아짐)
- **F1** = 종합 낚시 실력

```python
# ===== 이진 분류 데이터 준비 =====
# FashionMNIST에서 Sneaker(7)와 Ankle boot(9)만 추출

# train_full.data / .targets 로 raw 텐서에 직접 접근
mask_train = (train_full.targets == 7) | (train_full.targets == 9)
bin_x_all = train_full.data[mask_train].float().unsqueeze(1) / 255.0
bin_y_all = (train_full.targets[mask_train] == 9).long()  # Sneaker=0, Ankle boot=1

mask_test = (test_dataset.targets == 7) | (test_dataset.targets == 9)
bin_x_test = test_dataset.data[mask_test].float().unsqueeze(1) / 255.0
bin_y_test = (test_dataset.targets[mask_test] == 9).long()

# Train / Val 분할 (80 / 20)
n = len(bin_x_all)
idx = torch.randperm(n, generator=torch.Generator().manual_seed(42))
n_train = int(n * 0.8)

bin_train_loader = DataLoader(
    TensorDataset(bin_x_all[idx[:n_train]], bin_y_all[idx[:n_train]]),
    batch_size=128, shuffle=True)
bin_val_loader = DataLoader(
    TensorDataset(bin_x_all[idx[n_train:]], bin_y_all[idx[n_train:]]),
    batch_size=256, shuffle=False)
bin_test_loader = DataLoader(
    TensorDataset(bin_x_test, bin_y_test),
    batch_size=256, shuffle=False)

print(f"Sneaker(0): {(bin_y_all == 0).sum().item()}, Ankle boot(1): {(bin_y_all == 1).sum().item()}")
print(f"Train: {n_train}, Val: {n - n_train}, Test: {len(bin_x_test)}")

# ===== 이진 분류 모델 =====
class BinaryMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(784, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 1)
        )
    def forward(self, x):
        return self.net(x).squeeze(1)  # (N,) logits

bin_model = BinaryMLP().to(device)
bin_loss_fn = nn.BCEWithLogitsLoss()
bin_optimizer = torch.optim.Adam(bin_model.parameters(), lr=0.001)

# ===== 학습 =====
bin_history = {'train_loss': [], 'val_loss': []}

for epoch in range(1, 11):
    bin_model.train()
    train_loss, train_count = 0.0, 0
    for xb, yb in bin_train_loader:
        xb, yb = xb.to(device), yb.to(device).float()
        bin_optimizer.zero_grad()
        logits = bin_model(xb)
        loss = bin_loss_fn(logits, yb)
        loss.backward()
        bin_optimizer.step()
        train_loss += loss.item() * len(xb)
        train_count += len(xb)

    bin_model.eval()
    val_loss, val_count = 0.0, 0
    with torch.inference_mode():
        for xb, yb in bin_val_loader:
            xb, yb = xb.to(device), yb.to(device).float()
            logits = bin_model(xb)
            loss = bin_loss_fn(logits, yb)
            val_loss += loss.item() * len(xb)
            val_count += len(xb)

    bin_history['train_loss'].append(train_loss / train_count)
    bin_history['val_loss'].append(val_loss / val_count)

    if epoch % 2 == 0:
        print(f"Epoch {epoch:2d} | "
              f"train_loss={train_loss/train_count:.4f} "
              f"val_loss={val_loss/val_count:.4f}")
```

**출력:**
```
Sneaker(0): 6000, Ankle boot(1): 6000
Train: 9600, Val: 2400, Test: 2000
Epoch  2 | train_loss=0.1294 val_loss=0.1257
Epoch  4 | train_loss=0.1000 val_loss=0.1142
Epoch  6 | train_loss=0.0971 val_loss=0.1094
Epoch  8 | train_loss=0.0790 val_loss=0.1075
Epoch 10 | train_loss=0.0785 val_loss=0.1131
```

```python
# ===== 이진 분류 학습 곡선 =====
plt.figure(figsize=(6, 3))
epochs = range(1, len(bin_history['train_loss']) + 1)
plt.plot(epochs, bin_history['train_loss'], 'b-o', label='Train Loss')
plt.plot(epochs, bin_history['val_loss'], 'r-o', label='Val Loss')
plt.xlabel('Epoch')
plt.ylabel('BCE Loss')
plt.title('Binary Classification Loss Curve')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

```python
# ===== 이진 분류 테스트 평가 =====
bin_model.eval()
bin_all_logits, bin_all_targets = [], []

with torch.inference_mode():
    for xb, yb in bin_test_loader:
        xb = xb.to(device)
        logits = bin_model(xb)
        bin_all_logits.append(logits.cpu())
        bin_all_targets.append(yb)

bin_all_logits = torch.cat(bin_all_logits)
bin_all_targets = torch.cat(bin_all_targets)
bin_all_probs = torch.sigmoid(bin_all_logits)

# --- 이진 분류 지표 계산 함수 ---
def binary_metrics(probs, targets, threshold=0.5):
    preds = (probs >= threshold).long()
    tp = ((preds == 1) & (targets == 1)).sum().item()
    tn = ((preds == 0) & (targets == 0)).sum().item()
    fp = ((preds == 1) & (targets == 0)).sum().item()
    fn = ((preds == 0) & (targets == 1)).sum().item()

    accuracy  = (tp + tn) / max(tp + tn + fp + fn, 1)
    precision = tp / max(tp + fp, 1)
    recall    = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-8)
    return {'accuracy': accuracy, 'precision': precision,
            'recall': recall, 'f1': f1,
            'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn}

# --- 기본 threshold 평가 ---
m = binary_metrics(bin_all_probs, bin_all_targets, threshold=0.5)
print(f"Accuracy:  {m['accuracy']:.4f}")
print(f"Precision: {m['precision']:.4f}")
print(f"Recall:    {m['recall']:.4f}")
print(f"F1 Score:  {m['f1']:.4f}")
print(f"\nTP={m['tp']}  FP={m['fp']}  FN={m['fn']}  TN={m['tn']}")

# --- Threshold별 비교 ---
print(f"\n{'Threshold':>10} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1':>10}")
print("-" * 55)
for t in [0.3, 0.4, 0.5, 0.6, 0.7]:
    m = binary_metrics(bin_all_probs, bin_all_targets, threshold=t)
    print(f"{t:>10.1f} {m['accuracy']:>10.4f} {m['precision']:>10.4f} "
          f"{m['recall']:>10.4f} {m['f1']:>10.4f}")
```

**출력:**
```
Accuracy:  0.9645
Precision: 0.9567
Recall:    0.9730
F1 Score:  0.9648

TP=973  FP=44  FN=27  TN=956

 Threshold   Accuracy  Precision     Recall         F1
-------------------------------------------------------
       0.3     0.9580     0.9370     0.9820     0.9590
       0.4     0.9630     0.9495     0.9780     0.9635
       0.5     0.9645     0.9567     0.9730     0.9648
       0.6     0.9680     0.9652     0.9710     0.9681
       0.7     0.9675     0.9717     0.9630     0.9674
```

---

#### Threshold(임계값) 해석

모델은 확률값을 출력하고, Threshold를 기준으로 양성/음성을 판정합니다. Threshold를 바꾸면 Precision과 Recall의 균형이 달라집니다.

| Threshold | 효과 | 적합한 상황 |
|-----------|------|-----------|
| **낮음** (0.3) | Recall ↑, Precision ↓ | FN 비용이 클 때 (암 진단: 환자를 놓치면 위험) |
| **기본** (0.5) | 균형 | 일반적인 경우 |
| **높음** (0.7) | Precision ↑, Recall ↓ | FP 비용이 클 때 (스팸 필터: 정상 메일을 차단하면 안 됨) |

> **핵심**: Threshold는 기술적 선택이 아니라 **비즈니스 의사결정**입니다. "놓치는 것(FN)과 오판하는 것(FP) 중 어느 쪽이 더 비싼가?"에 따라 조절합니다.

---

#### ROC-AUC

- **ROC 곡선**: Threshold를 0에서 1까지 바꾸면서 **TPR(= Recall)**과 **FPR**의 변화를 그린 그래프
  - FPR = FP / (FP + TN) : 실제 음성을 양성으로 잘못 예측한 비율
- **AUC (Area Under the Curve)**: ROC 곡선 아래 면적
  - **1.0** = 완벽한 분류
  - **0.5** = 랜덤 수준 (동전 던지기)
  - **0.9 이상** = 우수한 모델

> Threshold에 독립적인 단일 수치로 모델의 전체 판별력을 비교할 수 있습니다.

```python
# ===== ROC-AUC 계산 (순수 PyTorch) =====

def compute_roc_auc(probs, targets, n_thresholds=500):
    """ROC 곡선과 AUC를 계산합니다."""
    thresholds = torch.linspace(1.0, 0.0, n_thresholds)
    num_pos = (targets == 1).sum().float()
    num_neg = (targets == 0).sum().float()
    tprs, fprs = [], []

    for t in thresholds:
        preds = (probs >= t).long()
        tp = ((preds == 1) & (targets == 1)).sum().float()
        fp = ((preds == 1) & (targets == 0)).sum().float()
        tprs.append((tp / num_pos).item() if num_pos > 0 else 0.0)
        fprs.append((fp / num_neg).item() if num_neg > 0 else 0.0)

    # AUC (사다리꼴 공식)
    auc = 0.0
    for i in range(1, len(fprs)):
        auc += (fprs[i] - fprs[i-1]) * (tprs[i] + tprs[i-1]) / 2
    return fprs, tprs, auc

fprs, tprs, auc_score = compute_roc_auc(bin_all_probs, bin_all_targets)

plt.figure(figsize=(6, 6))
plt.plot(fprs, tprs, 'b-', linewidth=2, label=f'ROC (AUC = {auc_score:.4f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random (AUC = 0.5)')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR = Recall)')
plt.title('ROC Curve: Sneaker vs Ankle Boot')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"AUC: {auc_score:.4f}")
```

---

### 분류 평가 정리

| 상황 | 확인할 지표 | 이유 |
|------|-----------|------|
| 클래스가 균형 잡힌 경우 | Accuracy + Confusion Matrix | Accuracy가 신뢰할 만함 |
| 클래스 불균형인 경우 | Recall, F1, Per-class metrics | Accuracy는 다수 클래스에 치우침 |
| 양성/음성 구분이 중요한 경우 | Precision + Recall + Threshold 분석 | 비즈니스 비용에 맞는 임계값 설정 |
| 모델 전체 판별력 비교 | ROC-AUC | Threshold에 독립적인 단일 수치 |

---

<a id="part4"></a>

## 4. 회귀 모델 평가 [↑](#toc)

**California Housing** 데이터셋으로 주택 가격(중간값)을 예측합니다.

> 데이터 로드에만 `sklearn.datasets`를 사용합니다 (Colab에 기본 설치됨). 평가 지표는 모두 PyTorch로 직접 계산합니다.

```python
# ===== California Housing 데이터 로드 =====
from sklearn.datasets import fetch_california_housing

data = fetch_california_housing()
X = torch.tensor(data.data, dtype=torch.float32)
y = torch.tensor(data.target, dtype=torch.float32)

# 특성 정규화 (StandardScaler를 PyTorch로 직접 구현)
X_mean = X.mean(dim=0)
X_std  = X.std(dim=0)
X = (X - X_mean) / (X_std + 1e-8)

# Train / Val / Test 분할 (60 / 20 / 20)
n = len(X)
idx = torch.randperm(n, generator=torch.Generator().manual_seed(42))
n_train = int(n * 0.6)
n_val   = int(n * 0.2)

reg_train_loader = DataLoader(
    TensorDataset(X[idx[:n_train]], y[idx[:n_train]]),
    batch_size=128, shuffle=True)
reg_val_loader = DataLoader(
    TensorDataset(X[idx[n_train:n_train+n_val]], y[idx[n_train:n_train+n_val]]),
    batch_size=256, shuffle=False)
reg_test_loader = DataLoader(
    TensorDataset(X[idx[n_train+n_val:]], y[idx[n_train+n_val:]]),
    batch_size=256, shuffle=False)

print(f"Features: {X.shape[1]}  ({', '.join(data.feature_names)})")
print(f"Target: median house value ($100,000 units)")
print(f"Target range: {y.min().item():.2f} ~ {y.max().item():.2f}")
print(f"Train: {n_train}, Val: {n_val}, Test: {n - n_train - n_val}")
```

**출력:**
```
Features: 8  (MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude)
Target: median house value ($100,000 units)
Target range: 0.15 ~ 5.00
Train: 12384, Val: 4128, Test: 4128
```

```python
# ===== 회귀 모델 정의 =====
class RegressionMLP(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64), nn.ReLU(),
            nn.Linear(64, 32), nn.ReLU(),
            nn.Linear(32, 1)
        )
    def forward(self, x):
        return self.net(x).squeeze(1)  # (N,)

reg_model = RegressionMLP(input_dim=8).to(device)
reg_loss_fn = nn.MSELoss()
reg_optimizer = torch.optim.Adam(reg_model.parameters(), lr=0.001)

# ===== 학습 =====
reg_history = {'train_loss': [], 'val_loss': []}

for epoch in range(1, 51):
    reg_model.train()
    train_loss, train_count = 0.0, 0
    for xb, yb in reg_train_loader:
        xb, yb = xb.to(device), yb.to(device)
        reg_optimizer.zero_grad()
        preds = reg_model(xb)
        loss = reg_loss_fn(preds, yb)
        loss.backward()
        reg_optimizer.step()
        train_loss += loss.item() * len(xb)
        train_count += len(xb)

    reg_model.eval()
    val_loss, val_count = 0.0, 0
    with torch.inference_mode():
        for xb, yb in reg_val_loader:
            xb, yb = xb.to(device), yb.to(device)
            preds = reg_model(xb)
            loss = reg_loss_fn(preds, yb)
            val_loss += loss.item() * len(xb)
            val_count += len(xb)

    reg_history['train_loss'].append(train_loss / train_count)
    reg_history['val_loss'].append(val_loss / val_count)

    if epoch % 10 == 0:
        print(f"Epoch {epoch:2d} | "
              f"train_mse={train_loss/train_count:.4f} "
              f"val_mse={val_loss/val_count:.4f}")
```

**출력:**
```
Epoch 10 | train_mse=0.3701 val_mse=0.3721
Epoch 20 | train_mse=0.3235 val_mse=0.3311
Epoch 30 | train_mse=0.2985 val_mse=0.3136
Epoch 40 | train_mse=0.2900 val_mse=0.3013
Epoch 50 | train_mse=0.2781 val_mse=0.2966
```

```python
# ===== 회귀 학습 곡선 =====
plt.figure(figsize=(7, 4))
epochs = range(1, len(reg_history['train_loss']) + 1)
plt.plot(epochs, reg_history['train_loss'], 'b-', label='Train MSE')
plt.plot(epochs, reg_history['val_loss'], 'r-', label='Val MSE')
plt.xlabel('Epoch')
plt.ylabel('MSE')
plt.title('Regression Loss Curve')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

#### 회귀 평가 지표

| 지표 | 수식 | 의미 | 단위 |
|------|------|------|------|
| **MAE** | mean(\|y - ŷ\|) | 평균 절대 오차 | 타겟과 동일 |
| **MSE** | mean((y - ŷ)²) | 평균 제곱 오차 | 타겟의 제곱 |
| **RMSE** | √MSE | MSE에 루트를 씌운 값 | 타겟과 동일 |
| **R²** | 1 - SS_res / SS_tot | 모델이 설명하는 분산의 비율 | 없음 (0 ~ 1) |

- **R² = 1.0**: 완벽한 예측
- **R² = 0.0**: 평균값만 예측하는 것과 동일
- **R² < 0**: 평균값보다 못한 모델

```python
# ===== 회귀 테스트 평가 =====
reg_model.eval()
reg_all_preds, reg_all_targets = [], []

with torch.inference_mode():
    for xb, yb in reg_test_loader:
        xb = xb.to(device)
        preds = reg_model(xb)
        reg_all_preds.append(preds.cpu())
        reg_all_targets.append(yb)

reg_all_preds = torch.cat(reg_all_preds)
reg_all_targets = torch.cat(reg_all_targets)

# --- 지표 계산 ---
mae  = torch.abs(reg_all_preds - reg_all_targets).mean().item()
mse  = ((reg_all_preds - reg_all_targets) ** 2).mean().item()
rmse = mse ** 0.5
ss_res = ((reg_all_targets - reg_all_preds) ** 2).sum()
ss_tot = ((reg_all_targets - reg_all_targets.mean()) ** 2).sum()
r2 = (1 - ss_res / ss_tot).item()

print(f"MAE  : {mae:.4f}  (평균 ${mae * 100000:,.0f} 오차)")
print(f"MSE  : {mse:.4f}")
print(f"RMSE : {rmse:.4f}  (평균 ${rmse * 100000:,.0f} 오차)")
print(f"R²   : {r2:.4f}  (분산의 {r2*100:.1f}%를 설명)")
```

**출력:**
```
MAE  : 0.3602  (평균 $36,016 오차)
MSE  : 0.2788
RMSE : 0.5280  (평균 $52,802 오차)
R²   : 0.7967  (분산의 79.7%를 설명)
```

---

#### MAE vs RMSE: 언제 무엇을 볼 것인가?

| 상황 | 선택 | 이유 |
|------|------|------|
| 이상치(outlier)가 많은 데이터 | **MAE** | 큰 오차에 과도한 페널티를 주지 않음 |
| 큰 오차가 치명적인 경우 | **RMSE** | 큰 오차를 더 강하게 반영 |
| 비즈니스 보고 | **MAE** | "평균적으로 X만큼 틀린다"고 직관적으로 설명 가능 |
| 모델 학습 중 loss | **MSE** | 미분이 연속적이어서 경사하강법 최적화에 유리 |

> **RMSE ≥ MAE**는 항상 성립합니다. 둘의 차이가 클수록 오차의 분산이 크다(큰 오차가 섞여 있다)는 신호입니다.

```python
# ===== 잔차(Residual) 분석 =====
residuals = (reg_all_preds - reg_all_targets).numpy()
targets_np = reg_all_targets.numpy()
preds_np = reg_all_preds.detach().numpy()

fig, axes = plt.subplots(1, 3, figsize=(16, 4))

# 1. True vs Predicted
axes[0].scatter(targets_np, preds_np, alpha=0.3, s=10)
val_min = min(targets_np.min(), preds_np.min())
val_max = max(targets_np.max(), preds_np.max())
axes[0].plot([val_min, val_max], [val_min, val_max], 'r-', linewidth=2)
axes[0].set_xlabel('True')
axes[0].set_ylabel('Predicted')
axes[0].set_title('True vs Predicted')
axes[0].grid(True, alpha=0.3)

# 2. Residual vs Predicted
axes[1].scatter(preds_np, residuals, alpha=0.3, s=10)
axes[1].axhline(0, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Predicted')
axes[1].set_ylabel('Residual')
axes[1].set_title('Residual Plot')
axes[1].grid(True, alpha=0.3)

# 3. Residual Distribution
axes[2].hist(residuals, bins=50, edgecolor='black', alpha=0.7)
axes[2].axvline(0, color='red', linestyle='--', linewidth=2)
axes[2].set_xlabel('Residual')
axes[2].set_ylabel('Count')
axes[2].set_title('Residual Distribution')

plt.tight_layout()
plt.show()
```

---

#### 잔차 분석 해석 가이드

| 그래프 | 이상적인 모습 | 문제 신호 |
|--------|-------------|----------|
| **True vs Predicted** | 점들이 대각선(빨간 선)에 밀집 | 특정 구간에서 대각선과 크게 벗어남 |
| **Residual Plot** | 0 주변에 무작위로 분포 | 패턴이 보임 (곡선, 부채꼴 형태) |
| **Residual Distribution** | 0 중심의 대칭 분포 | 한쪽으로 치우침, 긴 꼬리 |

**문제가 보이면:**
- 잔차에 **곡선 패턴** → 모델이 놓치는 비선형 관계 존재 → 모델 복잡도 증가
- 잔차가 **부채꼴 형태** → 예측값이 커질수록 오차 증가 → 타겟 로그 변환 검토
- 잔차가 **한쪽으로 치우침** → 체계적 과대/과소 예측 → 데이터 전처리 확인

---

<a id="part5"></a>

## 5. 종합 정리 [↑](#toc)

### 분류 vs 회귀 지표 비교

| | 분류 | 회귀 |
|---|------|------|
| **핵심 질문** | 클래스를 맞혔는가? | 값이 얼마나 가까운가? |
| **기본 지표** | Accuracy | MAE / RMSE |
| **세부 지표** | Precision, Recall, F1 | R² |
| **시각화** | Confusion Matrix, ROC Curve | True vs Pred, Residual Plot |
| **주의점** | 불균형 데이터에서 Accuracy 함정 | RMSE ≫ MAE이면 이상치 의심 |

### 학습 곡선 해석

| 패턴 | 의미 | 대응 |
|------|------|------|
| train_loss ↓, val_loss ↓ | 정상 학습 | 계속 학습 |
| train_loss ↓, val_loss → | 학습 수렴 | 학습 중단 |
| train_loss ↓, val_loss ↑ | **과적합** | 조기 종료, 정규화, 데이터 보강 |
| train_loss →, val_loss → | **과소적합** | 모델 복잡도 증가, 학습률 조정 |

### 정리 질문

1. Accuracy 95%인 모델이 있다. 바로 서비스에 배포해도 되는가? 어떤 추가 지표를 확인해야 하는가?
2. Precision과 Recall 중 하나만 높일 수 있다면, 암 진단에서는 어느 쪽을 택하겠는가?
3. MAE가 0.5이고 RMSE가 1.5인 모델이 있다. 이 차이가 알려주는 것은 무엇인가?
4. 학습 곡선에서 train_loss는 계속 줄어드는데 val_loss가 올라간다면 어떻게 대응하겠는가?


