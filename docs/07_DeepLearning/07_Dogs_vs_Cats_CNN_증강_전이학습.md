---
title: 7. 전이학습 - Dogs vs Cats 실전 분류
layout: default
parent: DeepLearning
nav_order: 7
permalink: /deeplearning/DogsVsCats
# nav_exclude: true
# search_exclude: true
---
# 7. 전이학습 - Dogs vs Cats 실전 분류

## 학습 목표
1. Kaggle 데이터셋을 PyTorch ImageFolder 형식으로 준비할 수 있다
2. 기본 CNN, 이미지 증강 CNN, 전이학습 모델의 성능을 비교할 수 있다
3. 이미지 증강이 학습에 미치는 영향을 설명할 수 있다
4. 사전학습된 모델을 활용한 전이학습의 원리와 효과를 설명할 수 있다
5. Feature extraction과 fine-tuning의 차이를 실험으로 비교할 수 있다
6. 오분류 샘플을 시각적으로 분석하고 모델의 약점을 해석할 수 있다
7. 학습된 모델을 저장하고 Streamlit 웹 서비스로 배포할 수 있다

<a id="toc"></a>

## 진행 순서

1. [데이터 준비](#part1) - Google Drive 또는 직접 업로드로 train.zip 준비
2. [교육용 split 만들기](#part2) - ImageFolder용 train / val / test 폴더 재구성
3. [Transform과 DataLoader](#part3) - 기본/증강 transform 정의 및 시각화
4. [모델과 손실 함수](#part3b) - SimpleCNN 구조와 BCEWithLogitsLoss 이해
5. [훈련 도구 정의](#part3c) - 학습/평가/시각화 헬퍼 함수
6. [기본 CNN 학습](#part4) - 증강 없이 처음부터 학습 및 평가
7. [이미지 증강 CNN 학습](#part5) - 증강 적용 후 재학습 및 비교
8. [전이학습이란?](#part6-concept) - 사전학습 모델의 원리와 활용 전략
9. [전이학습 실험](#part6) - ResNet18 feature extraction
10. [Fine-tuning](#part7) - ResNet18 layer4 + fc 미세 조정 (선택 확장)
11. [성능 비교와 오분류 분석](#part8) - 네 모델 비교 + 오분류 시각화
12. [모델 저장과 웹 서비스 배포](#part-deploy) - Streamlit Cloud로 배포
13. [통합 정리](#part9) - 해석 가이드와 확장 과제

### 이 노트북의 중요한 원칙

- Kaggle competition의 unlabeled test 파일은 교육용 평가에 직접 쓰지 않습니다.
- 대신 labeled train 이미지를 train / val / test로 직접 나눕니다.
- 증강은 train 데이터에만 적용하고, val / test에는 적용하지 않습니다.
- 비교의 공정성을 위해 같은 split을 재사용합니다.

```python
import os, time, random, shutil, zipfile
from copy import deepcopy
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from sklearn.metrics import confusion_matrix, classification_report

# 재현성을 위한 시드 고정
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)
    torch.backends.cudnn.benchmark = True  # 입력 크기 고정 시 속도 향상

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 작업 디렉터리
BASE_DIR = Path('/content/dogs_vs_cats')
RAW_DIR  = BASE_DIR / 'raw'
SPLIT_DIR = BASE_DIR / 'prepared_data'
for d in [BASE_DIR, RAW_DIR, SPLIT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

print(f'device: {device}  |  torch: {torch.__version__}')
```

---

<a id="part1"></a>

## 1. 데이터 준비 [↑](#toc)

**학습목표**: Kaggle Dogs vs Cats 데이터를 Colab 환경에 올리고 사용 가능하게 준비할 수 있다.

Google Drive에 공유해 둔 `train.zip`을 `gdown`으로 자동 다운로드합니다. 별도의 Kaggle 가입이나 수동 업로드 없이, 아래 셀을 실행하기만 하면 됩니다.

> **참고**: `test1.zip`은 라벨이 없으므로 이 노트북에서는 사용하지 않습니다. labeled train 이미지만 사용합니다.

```python
!pip install -q gdown

import gdown

# ── Google Drive 공유 링크 설정 ──────────────────────────────
# 아래 FILE_ID를 Google Drive 공유 링크의 파일 ID로 바꾸세요.
# 예: https://drive.google.com/file/d/1AbCdEfGhIjKlMnOp/view?usp=sharing
#     → FILE_ID = '1AbCdEfGhIjKlMnOp'
GDRIVE_FILE_ID = 'YOUR_FILE_ID_HERE'
# ─────────────────────────────────────────────────────────────

train_zip = BASE_DIR / 'train.zip'
raw_train_dir = RAW_DIR / 'train'

# 이미 다운로드된 경우 건너뜁니다
if raw_train_dir.exists():
    print('이미 raw/train 폴더가 존재합니다. 다운로드를 건너뜁니다.')
else:
    if not train_zip.exists():
        print('Google Drive에서 train.zip 다운로드 중...')
        gdown.download(
            id=GDRIVE_FILE_ID,
            output=str(train_zip),
            quiet=False
        )
    else:
        print(f'이미 다운로드된 파일을 사용합니다: {train_zip}')

    print('train.zip 압축 해제 중...')
    with zipfile.ZipFile(train_zip) as zf:
        zf.extractall(RAW_DIR)

if not raw_train_dir.exists():
    raise FileNotFoundError(
        'raw/train 폴더를 찾지 못했습니다. '
        'GDRIVE_FILE_ID가 올바른지 확인하세요.'
    )

print(f'raw image count: {len(list(raw_train_dir.glob("*.jpg"))):,}')
```

**핵심**: 공유된 Google Drive 링크에서 `gdown`으로 데이터를 자동 다운로드한다. 경쟁용 test 데이터는 라벨이 없으므로, labeled train 이미지만 사용한다.

---

<a id="part2"></a>

## 2. 교육용 split 만들기 [↑](#toc)

**학습목표**: Dogs vs Cats 데이터를 ImageFolder 형식의 train / val / test로 나눌 수 있다.

Dogs vs Cats competition의 `train` 폴더는 파일명에 라벨이 들어 있습니다.

예시:

- `cat.0.jpg`
- `dog.1234.jpg`

PyTorch `ImageFolder`는 다음 구조를 기대합니다.

```text
prepared_data/
  train/
    cat/
    dog/
  val/
    cat/
    dog/
  test/
    cat/
    dog/
```

아래 셀은 이 구조를 자동으로 만듭니다.
기본값은 subset 모드라서, 무료 Colab에서도 비교 실험 3개를 끝낼 수 있게 설계했습니다.

```python
from IPython.display import display

USE_SMALL_SUBSET = True
MAX_IMAGES_PER_CLASS = 1500
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15
IMG_SIZE = 224
BATCH_SIZE = 32
NUM_WORKERS = min(2, os.cpu_count() or 2)
EPOCHS_SCRATCH = 5
EPOCHS_TRANSFER = 5
REBUILD_SPLIT = False


def prepare_dogs_vs_cats_split(
    raw_train_dir, output_dir,
    train_ratio=0.7, val_ratio=0.15, test_ratio=0.15,
    max_per_class=None, seed=42, rebuild=False
):
    if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-9:
        raise ValueError('train/val/test 비율의 합은 1이어야 합니다.')

    if rebuild and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    existing_images = list(output_dir.glob('*/*/*.jpg'))
    if existing_images:
        print('이미 준비된 split이 있으므로 재사용합니다.')
        return

    rng = random.Random(seed)

    for class_name in ['cat', 'dog']:
        files = sorted(raw_train_dir.glob(f'{class_name}.*.jpg'))
        if max_per_class is not None:
            files = files[:max_per_class]
        rng.shuffle(files)

        n_total = len(files)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)
        split_map = {
            'train': files[:n_train],
            'val': files[n_train:n_train + n_val],
            'test': files[n_train + n_val:]
        }

        for split_name, split_files in split_map.items():
            target_dir = output_dir / split_name / class_name
            target_dir.mkdir(parents=True, exist_ok=True)
            for src in split_files:
                shutil.copy2(src, target_dir / src.name)


def count_images_by_split(base_dir):
    rows = []
    for split_name in ['train', 'val', 'test']:
        for class_name in ['cat', 'dog']:
            rows.append({
                'split': split_name,
                'class': class_name,
                'count': len(list(
                    (base_dir / split_name / class_name).glob('*.jpg')
                ))
            })
    return pd.DataFrame(rows)

max_per_class = MAX_IMAGES_PER_CLASS if USE_SMALL_SUBSET else None
prepare_dogs_vs_cats_split(
    raw_train_dir=RAW_DIR / 'train',
    output_dir=SPLIT_DIR,
    train_ratio=TRAIN_RATIO,
    val_ratio=VAL_RATIO,
    test_ratio=TEST_RATIO,
    max_per_class=max_per_class,
    seed=SEED,
    rebuild=REBUILD_SPLIT
)

count_df = count_images_by_split(SPLIT_DIR)
display(count_df.pivot(index='split', columns='class', values='count'))
print(f'IMG_SIZE={IMG_SIZE}, BATCH_SIZE={BATCH_SIZE}, USE_SMALL_SUBSET={USE_SMALL_SUBSET}')
```

Colab에서 matplotlib 한글 깨짐을 방지하기 위해 나눔고딕 폰트를 설치합니다.

```bash
!apt-get -qq install -y fonts-nanum > /dev/null
!fc-cache -f
```

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from PIL import Image

# 나눔고딕 폰트 설정 (Colab 한글 깨짐 방지)
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    pass

def show_examples(split_name='train', n=4):
    fig, axes = plt.subplots(2, n, figsize=(3 * n, 6))
    for row, class_name in enumerate(['cat', 'dog']):
        paths = sorted(
            (SPLIT_DIR / split_name / class_name).glob('*.jpg')
        )[:n]
        for ax, path in zip(axes[row], paths):
            ax.imshow(Image.open(path).convert('RGB'))
            ax.set_title(f'{class_name}: {path.name}')
            ax.axis('off')
    plt.tight_layout()
    plt.show()

show_examples('train', n=4)
```

**핵심**: ImageFolder가 기대하는 폴더 구조로 데이터를 나누면 PyTorch가 자동으로 라벨을 인식한다. 비교 실험의 공정성을 위해 같은 split을 재사용한다.

---

<a id="part3"></a>

## 3. Transform과 DataLoader [↑](#toc)

**학습목표**: 기본 transform과 증강 transform을 구분하여 DataLoader를 구성할 수 있다.

여기서 중요한 점은 다음입니다.

- 기본 CNN 실험: `Resize + Normalize`
- 증강 CNN 실험: `RandomResizedCrop + RandomHorizontalFlip + ColorJitter + Normalize`
- 검증 / 테스트: 항상 `Resize + Normalize`만 사용

즉, 성능이 좋아졌다면 그것은 train 단계의 다양한 시각 노출 덕분이라고 해석할 수 있습니다.

> **증강 강도에 대해**: 이 실습에서는 효과를 명확히 관찰할 수 있도록 비교적 약한 증강을 선택했습니다. 실전에서는 `RandomRotation`, `RandomAffine`, `GaussianBlur`, `RandomErasing` 등 더 강한 증강도 자주 사용합니다. 확장 과제에서 직접 비교해 보세요.

```python
# ImageNet 데이터셋의 평균/표준편차 — 사전학습 모델과 동일한 정규화를 적용합니다
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

# 기본 transform: 크기 변환 + 정규화만 적용
train_transform_base = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])

# 증강 transform: 학습 데이터에만 적용하는 다양한 변형
train_transform_aug = transforms.Compose([
    transforms.RandomResizedCrop(IMG_SIZE, scale=(0.8, 1.0)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])

# 평가 transform: val/test에는 증강 없이 동일한 전처리만 적용
eval_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])

train_ds_base = datasets.ImageFolder(
    SPLIT_DIR / 'train', transform=train_transform_base
)
train_ds_aug = datasets.ImageFolder(
    SPLIT_DIR / 'train', transform=train_transform_aug
)
val_ds = datasets.ImageFolder(
    SPLIT_DIR / 'val', transform=eval_transform
)
test_ds = datasets.ImageFolder(
    SPLIT_DIR / 'test', transform=eval_transform
)

class_names = train_ds_base.classes
print('classes:', class_names)

# ImageFolder는 폴더 이름을 알파벳 순으로 정렬하여 인덱스를 부여합니다
# cat=0, dog=1 → 나중에 sigmoid >= 0.5이면 dog으로 예측한다는 뜻입니다
print('class_to_idx:', train_ds_base.class_to_idx)

train_loader_base = DataLoader(
    train_ds_base, batch_size=BATCH_SIZE,
    shuffle=True, num_workers=NUM_WORKERS,
    pin_memory=torch.cuda.is_available()
)
train_loader_aug = DataLoader(
    train_ds_aug, batch_size=BATCH_SIZE,
    shuffle=True, num_workers=NUM_WORKERS,
    pin_memory=torch.cuda.is_available()
)
val_loader = DataLoader(
    val_ds, batch_size=BATCH_SIZE,
    shuffle=False, num_workers=NUM_WORKERS,
    pin_memory=torch.cuda.is_available()
)
test_loader = DataLoader(
    test_ds, batch_size=BATCH_SIZE,
    shuffle=False, num_workers=NUM_WORKERS,
    pin_memory=torch.cuda.is_available()
)


def denormalize(tensor, mean=IMAGENET_MEAN, std=IMAGENET_STD):
    mean = torch.tensor(mean).view(3, 1, 1)
    std = torch.tensor(std).view(3, 1, 1)
    return torch.clamp(tensor.cpu() * std + mean, 0, 1)

sample_path = sorted((SPLIT_DIR / 'train' / 'cat').glob('*.jpg'))[0]
sample_img = Image.open(sample_path).convert('RGB')

fig, axes = plt.subplots(1, 5, figsize=(18, 4))
axes[0].imshow(sample_img.resize((IMG_SIZE, IMG_SIZE)))
axes[0].set_title('original')
axes[0].axis('off')

for i in range(4):
    aug_tensor = train_transform_aug(sample_img)
    axes[i + 1].imshow(denormalize(aug_tensor).permute(1, 2, 0))
    axes[i + 1].set_title(f'augmented {i + 1}')
    axes[i + 1].axis('off')

plt.suptitle('증강은 train 데이터에만 적용합니다', fontsize=14)
plt.tight_layout()
plt.show()
```

**핵심**: 증강은 train 데이터에만 적용하고, val / test는 항상 동일한 전처리를 사용해야 공정한 비교가 가능하다.

---

<a id="part3b"></a>

## 4. 모델과 손실 함수 [↑](#toc)

**학습목표**: 이진 분류에 적합한 모델 출력 구조와 손실 함수를 이해할 수 있다.

#### 왜 BCEWithLogitsLoss를 쓰는가?

이전 장(MNIST)에서는 10개 클래스를 분류했기 때문에 출력이 10개인 모델 + `CrossEntropyLoss`를 사용했습니다.

이번에는 개 vs 고양이, 즉 **2개 클래스(이진 분류)**입니다. 이진 분류에서는 두 가지 방식이 가능합니다.

| 방식 | 출력 뉴런 수 | 손실 함수 | 예측 방법 |
|------|------------|----------|----------|
| 다중 클래스 스타일 | 2개 | `CrossEntropyLoss` | `argmax` |
| **이진 분류 스타일** | **1개** | **`BCEWithLogitsLoss`** | **`sigmoid >= 0.5`** |

이 노트북에서는 이진 분류 스타일을 사용합니다. 출력이 1개이므로 모델이 더 단순하고, 이진 분류의 원리를 직접 체험할 수 있습니다.

- 모델 출력값(logit)이 **0보다 크면** → sigmoid > 0.5 → **dog(1)**으로 예측
- 모델 출력값(logit)이 **0보다 작으면** → sigmoid < 0.5 → **cat(0)**으로 예측

> **참고**: `BCEWithLogitsLoss`는 내부적으로 sigmoid를 포함하고 있어서, 모델 출력에 sigmoid를 직접 적용하지 않고 raw logit을 바로 넣습니다. 이 방식이 수치적으로 더 안정적입니다.

```python
class SimpleCNN(nn.Module):
    """
    간단한 3-layer CNN.
    Conv2d(3→32→64→128) + AdaptiveAvgPool + Dropout + Linear(128→1)
    """
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),  # 224→224
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),                              # 224→112
            nn.Conv2d(32, 64, kernel_size=3, padding=1),  # 112→112
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),                              # 112→56
            nn.Conv2d(64, 128, kernel_size=3, padding=1), # 56→56
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),                              # 56→28
            nn.AdaptiveAvgPool2d((1, 1))                  # 28→1
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.3),   # 과적합 방지를 위해 30% 뉴런을 랜덤하게 끔
            nn.Linear(128, 1)  # 이진 분류이므로 출력 1개
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)


def count_trainable_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
```

> **실전 팁**: 실무에서는 Conv 뒤에 `BatchNorm2d`를 넣는 Conv-BN-ReLU 패턴이 표준입니다. 이 노트북에서는 구조를 단순하게 유지하기 위해 생략했습니다. 확장 과제에서 BatchNorm을 추가해 보세요.

**핵심**: 이진 분류에서는 출력 1개 + `BCEWithLogitsLoss`를 사용한다. 모델의 raw 출력(logit)이 0보다 크면 dog, 작으면 cat으로 예측한다.

---

<a id="part3c"></a>

## 5. 훈련 도구 정의 [↑](#toc)

**학습목표**: 학습/평가/시각화에 사용할 헬퍼 함수를 이해하고 활용할 수 있다.

아래 함수들은 이후 모든 실험에서 재사용됩니다. 구조를 간단히 정리하면:

| 함수 | 역할 |
|------|------|
| `accuracy_from_logits` | sigmoid 적용 후 정확도 계산 |
| `run_epoch` | 1 에폭 학습 또는 평가 실행 |
| `train_model` | 여러 에폭 반복 + best model 저장 |
| `evaluate_model` | test 세트 평가 + 예측 결과 수집 |
| `plot_history` | 학습 곡선(loss/accuracy) 시각화 |
| `plot_confusion` | 혼동 행렬 시각화 |

```python
def accuracy_from_logits(logits, labels):
    """sigmoid >= 0.5 기준으로 예측하고 정확도를 계산합니다."""
    preds = (torch.sigmoid(logits) >= 0.5).long().view(-1)
    return (preds == labels.long()).sum().item()


def run_epoch(model, loader, criterion, optimizer=None):
    """1 에폭을 실행합니다. optimizer가 None이면 평가 모드입니다."""
    is_train = optimizer is not None
    model.train() if is_train else model.eval()

    running_loss = 0.0
    running_corrects = 0
    total = 0

    # 예측 결과를 함께 수집합니다
    all_preds = []
    all_labels = []

    for inputs, labels in loader:
        inputs = inputs.to(device)
        # BCEWithLogitsLoss는 타겟을 float 형태의 (N, 1)로 기대합니다
        labels_bce = labels.float().unsqueeze(1).to(device)

        if is_train:
            optimizer.zero_grad()

        with torch.set_grad_enabled(is_train):
            outputs = model(inputs)
            loss = criterion(outputs, labels_bce)
            if is_train:
                loss.backward()
                optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        running_corrects += accuracy_from_logits(
            outputs, labels_bce.view(-1)
        )
        total += inputs.size(0)

        # 평가 모드일 때 예측 결과를 수집합니다
        if not is_train:
            preds = (
                torch.sigmoid(outputs) >= 0.5
            ).long().view(-1).cpu().numpy()
            all_preds.extend(preds.tolist())
            all_labels.extend(labels.numpy().tolist())

    result = (running_loss / total, running_corrects / total)
    if not is_train:
        return result, np.array(all_labels), np.array(all_preds)
    return result


def train_model(model, train_loader, val_loader, criterion, optimizer, epochs):
    """여러 에폭을 반복하며 best model을 저장합니다."""
    best_state = deepcopy(model.state_dict())
    best_val_acc = 0.0
    history = {
        'train_loss': [], 'train_acc': [],
        'val_loss': [], 'val_acc': []
    }

    for epoch in range(epochs):
        start = time.time()
        train_loss, train_acc = run_epoch(
            model, train_loader, criterion, optimizer=optimizer
        )
        (val_loss, val_acc), _, _ = run_epoch(
            model, val_loader, criterion, optimizer=None
        )

        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_state = deepcopy(model.state_dict())

        print(
            f'Epoch {epoch + 1}/{epochs} | '
            f'train_loss={train_loss:.4f}, train_acc={train_acc:.4f}, '
            f'val_loss={val_loss:.4f}, val_acc={val_acc:.4f}, '
            f'time={time.time() - start:.1f}s'
        )

    model.load_state_dict(best_state)
    return model, history


@torch.no_grad()
def evaluate_model(model, loader, criterion):
    """test 세트를 한 번 순회하여 loss, accuracy, 예측 결과를 모두 반환합니다."""
    model.eval()
    (loss, acc), all_labels, all_preds = run_epoch(
        model, loader, criterion, optimizer=None
    )
    return {'loss': loss, 'accuracy': acc}, all_labels, all_preds


def plot_history(history, title):
    """학습 곡선(loss/accuracy)을 시각화합니다."""
    epochs = range(1, len(history['train_loss']) + 1)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(epochs, history['train_loss'], marker='o', label='train')
    axes[0].plot(epochs, history['val_loss'], marker='o', label='val')
    axes[0].set_title(f'{title} - Loss')
    axes[0].set_xlabel('epoch')
    axes[0].legend()

    axes[1].plot(epochs, history['train_acc'], marker='o', label='train')
    axes[1].plot(epochs, history['val_acc'], marker='o', label='val')
    axes[1].set_title(f'{title} - Accuracy')
    axes[1].set_xlabel('epoch')
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def plot_confusion(y_true, y_pred, class_names, title):
    """혼동 행렬을 시각화합니다."""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(4, 4))
    im = ax.imshow(cm, cmap='Blues')
    ax.set_xticks(range(len(class_names)))
    ax.set_yticks(range(len(class_names)))
    ax.set_xticklabels(class_names)
    ax.set_yticklabels(class_names)
    ax.set_xlabel('predicted')
    ax.set_ylabel('true')
    ax.set_title(title)
    for i in range(len(class_names)):
        for j in range(len(class_names)):
            ax.text(j, i, cm[i, j],
                    ha='center', va='center', color='black')
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.show()


results = {}
```

**핵심**: 모델 구조와 헬퍼 함수를 미리 정의해 두면, 이후 실험에서 코드 중복 없이 비교할 수 있다.

---

<a id="part4"></a>

## 6. 기본 CNN 학습 [↑](#toc)

**학습목표**: 데이터 증강 없이 작은 CNN을 처음부터 학습하고, 과적합 경향을 관찰할 수 있다.

여기서는 데이터 증강 없이, 작은 CNN을 처음부터 학습합니다.

#### 과적합 관찰 가이드

학습이 끝난 후 출력되는 그래프에서 다음을 확인해 보세요.

- **Loss 그래프**: train_loss는 계속 내려가는데 val_loss가 올라가기 시작하면 → 과적합 신호
- **Accuracy 그래프**: train_acc - val_acc 차이가 10%p 이상이면 → 명확한 과적합
- **에폭별 추이**: 초반에는 둘 다 좋아지다가, 어느 시점부터 train만 좋아지고 val은 정체/악화하는 패턴을 찾아보세요

```python
baseline_model = SimpleCNN().to(device)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(baseline_model.parameters(), lr=1e-3)

print(f'Baseline CNN trainable params: {count_trainable_params(baseline_model):,}')
baseline_model, baseline_history = train_model(
    baseline_model,
    train_loader_base,
    val_loader,
    criterion,
    optimizer,
    epochs=EPOCHS_SCRATCH
)

baseline_metrics, y_true_base, y_pred_base = evaluate_model(
    baseline_model, test_loader, criterion
)
plot_history(baseline_history, 'Baseline CNN')
plot_confusion(
    y_true_base, y_pred_base, class_names,
    'Baseline CNN - Test Confusion Matrix'
)

display(pd.DataFrame(
    classification_report(
        y_true_base, y_pred_base,
        target_names=class_names, output_dict=True
    )
).T)
results['Baseline CNN'] = {
    'test_loss': baseline_metrics['loss'],
    'test_accuracy': baseline_metrics['accuracy'],
    'trainable_params': count_trainable_params(baseline_model)
}
print(results['Baseline CNN'])
```

**핵심**: 작은 데이터에서 scratch CNN은 과적합되기 쉽다. train accuracy는 높지만 val / test는 상대적으로 낮을 수 있다. 이 결과가 이후 증강과 전이학습의 비교 기준선이 된다.

> **확인 질문**: 위 그래프에서 train_acc와 val_acc의 차이는 얼마인가요? 이 차이가 과적합의 증거가 될 수 있을까요?

---

<a id="part5"></a>

## 7. 이미지 증강 CNN 학습 [↑](#toc)

**학습목표**: 모델 구조는 그대로 두고 train transform만 바꿔서, 증강 효과를 분리하여 해석할 수 있다.

이번에는 모델 구조는 그대로 두고, train transform만 바꿉니다.

즉, 좋아지거나 나빠진 이유를 `증강 효과`로 해석할 수 있게 만듭니다.

```python
aug_model = SimpleCNN().to(device)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(aug_model.parameters(), lr=1e-3)

print(f'Augmented CNN trainable params: {count_trainable_params(aug_model):,}')
aug_model, aug_history = train_model(
    aug_model,
    train_loader_aug,
    val_loader,
    criterion,
    optimizer,
    epochs=EPOCHS_SCRATCH
)

aug_metrics, y_true_aug, y_pred_aug = evaluate_model(
    aug_model, test_loader, criterion
)
plot_history(aug_history, 'Augmented CNN')
plot_confusion(
    y_true_aug, y_pred_aug, class_names,
    'Augmented CNN - Test Confusion Matrix'
)

display(pd.DataFrame(
    classification_report(
        y_true_aug, y_pred_aug,
        target_names=class_names, output_dict=True
    )
).T)
results['Augmented CNN'] = {
    'test_loss': aug_metrics['loss'],
    'test_accuracy': aug_metrics['accuracy'],
    'trainable_params': count_trainable_params(aug_model)
}
print(results['Augmented CNN'])
```

**핵심**: 모델 구조가 동일하고 train transform만 바꿨으므로, 성능 차이는 순수하게 증강 효과로 해석할 수 있다. 증강은 데이터를 실제로 늘리지 않지만, 매 에폭마다 다른 변형을 보여 줌으로써 일반화 성능을 높인다.

> **확인 질문**: Baseline CNN과 비교하여 train_acc - val_acc 차이(과적합 정도)는 어떻게 변했나요? 증강이 과적합을 줄이는 데 도움이 되었나요?

---

<a id="part6-concept"></a>

## 8. 전이학습이란? [↑](#toc)

지금까지 우리는 모델을 **처음부터(scratch)** 학습했습니다. 이번 파트에서는 완전히 다른 접근 방식인 **전이학습(Transfer Learning)**을 사용합니다.

#### 핵심 아이디어

사람은 고양이를 처음 배울 때 눈, 코, 귀의 형태를 완전히 새로 배우지 않습니다. 이미 다른 동물을 보면서 익힌 "눈이란 이런 것", "털의 질감은 이런 것"이라는 **기본적인 시각 지식**을 가지고 있기 때문입니다.

전이학습도 같은 원리입니다.

```text
[ImageNet 120만장으로 학습한 ResNet18]
        ↓
  이미 알고 있는 것:
  - 초기 레이어: 가장자리, 질감, 색상 패턴
  - 중간 레이어: 눈, 코, 귀, 발 같은 부분 형태
  - 깊은 레이어: 얼굴 구조, 몸체 형태 등 복합 특징
        ↓
  우리가 할 일:
  - 이 지식을 그대로 가져오고 (freeze)
  - 마지막 분류기만 "개 vs 고양이"로 교체 (새로 학습)
```

#### 두 가지 전이학습 전략

| 전략 | 방법 | 학습 파라미터 | 적합한 상황 |
|------|------|-------------|-----------|
| **Feature Extraction** | 사전학습 레이어 전체를 freeze하고 마지막 분류기만 학습 | 매우 적음 | 데이터가 적거나, 도메인이 ImageNet과 유사할 때 |
| **Fine-tuning** | 일부 레이어를 unfreeze하고 낮은 학습률로 미세 조정 | 적당히 많음 | 데이터가 충분하거나, 도메인이 약간 다를 때 |

#### 왜 효과적인가?

- **데이터 효율**: 1500장으로도 높은 성능 — ImageNet 120만장의 지식을 재활용하기 때문
- **학습 속도**: 분류기만 학습하므로 학습 가능한 파라미터가 극히 적어 빠르게 수렴
- **일반화**: 대규모 데이터에서 학습한 범용 특징이 다양한 이미지 과제에 전이됨

---

<a id="part6"></a>

## 9. 전이학습 실험 - Feature Extraction [↑](#toc)

**학습목표**: 사전학습된 ResNet18의 특징 표현을 활용하여, 적은 파라미터로 높은 성능을 얻을 수 있다.

이번에는 `ResNet18`의 사전학습 가중치를 불러와서 마지막 분류기만 새로 학습합니다.

여기서는 전이학습 효과를 분명히 보기 위해, 기본 train transform과 같은 입력 분포를 사용합니다.

즉:

- baseline vs transfer: `사전학습된 특징 표현`의 차이
- baseline vs augmented: `데이터 표현 다양화`의 차이

로 해석할 수 있습니다.

```python
# ResNet18_Weights.DEFAULT: 최신 torchvision API로 사전학습 가중치를 불러옵니다
weights = models.ResNet18_Weights.DEFAULT
transfer_model = models.resnet18(weights=weights)

# 모든 파라미터를 freeze — 사전학습된 특징을 그대로 사용합니다
for param in transfer_model.parameters():
    param.requires_grad = False

# 마지막 fc 레이어만 새로 교체 — 이 부분만 학습됩니다
transfer_model.fc = nn.Linear(transfer_model.fc.in_features, 1)
transfer_model = transfer_model.to(device)

criterion = nn.BCEWithLogitsLoss()
# fc 파라미터만 optimizer에 전달합니다
optimizer = optim.Adam(transfer_model.fc.parameters(), lr=1e-3)

print(f'Transfer model trainable params: {count_trainable_params(transfer_model):,}')
transfer_model, transfer_history = train_model(
    transfer_model,
    train_loader_base,
    val_loader,
    criterion,
    optimizer,
    epochs=EPOCHS_TRANSFER
)

transfer_metrics, y_true_transfer, y_pred_transfer = evaluate_model(
    transfer_model, test_loader, criterion
)
plot_history(transfer_history, 'Transfer Learning - ResNet18')
plot_confusion(
    y_true_transfer, y_pred_transfer, class_names,
    'Transfer Learning - Test Confusion Matrix'
)

display(pd.DataFrame(
    classification_report(
        y_true_transfer, y_pred_transfer,
        target_names=class_names, output_dict=True
    )
).T)
results['Transfer Learning (ResNet18)'] = {
    'test_loss': transfer_metrics['loss'],
    'test_accuracy': transfer_metrics['accuracy'],
    'trainable_params': count_trainable_params(transfer_model)
}
print(results['Transfer Learning (ResNet18)'])
```

**핵심**: 사전학습된 특징 표현을 활용하면, 학습 가능한 파라미터가 fc 레이어뿐이어도 scratch CNN보다 높은 성능을 얻을 수 있다. ImageNet에서 학습한 범용 시각 특징이 개/고양이 분류에도 유효하기 때문이다.

> **확인 질문**: 전이학습 모델의 학습 가능한 파라미터 수를 Baseline CNN과 비교해 보세요. 파라미터가 훨씬 적은데도 성능은 어떻게 다른가요? 이것이 의미하는 바는 무엇일까요?

---

<a id="part7"></a>

## 10. Fine-tuning (선택 확장) [↑](#toc)

**학습목표**: Feature extraction과 fine-tuning의 차이를 실험으로 비교할 수 있다.

위의 전이학습은 `feature extraction` 방식이었습니다.

이번 확장 셀에서는:

- `layer4`와 `fc`만 학습 가능하게 풀고
- 낮은 학습률로 미세 조정(fine-tuning)합니다.

즉, 사전학습 지식을 너무 크게 망가뜨리지 않으면서, 우리 데이터셋에 조금 더 맞게 조정하는 실험입니다.

실전에서는 fine-tuning에서도 보통 약한 증강을 함께 쓰므로, 여기서는 `train_loader_aug`를 사용합니다.

> **주의: 변수 통제에 대해**: 이 실험에서는 파트 9(Feature Extraction)과 비교할 때 **두 가지가 동시에 바뀝니다**: (1) layer4 unfreeze, (2) 증강 적용. 따라서 성능 차이가 순수하게 "unfreeze 효과"만은 아닙니다. 이전 파트까지의 "변수 하나씩 바꾸기" 원칙과 달리, 실전에서 흔히 쓰는 조합을 보여주는 것이 목적입니다. 순수한 unfreeze 효과만 보고 싶다면 `train_loader_base`로도 실험해 보세요.

```python
finetune_model = models.resnet18(weights=weights)
for param in finetune_model.parameters():
    param.requires_grad = False

# layer4만 학습 가능하게 풀기
for param in finetune_model.layer4.parameters():
    param.requires_grad = True

finetune_model.fc = nn.Linear(finetune_model.fc.in_features, 1)
finetune_model = finetune_model.to(device)

criterion = nn.BCEWithLogitsLoss()
# 차등 학습률: 사전학습된 layer4는 낮게, 새 fc는 높게
optimizer = optim.Adam([
    {'params': finetune_model.layer4.parameters(), 'lr': 1e-4},
    {'params': finetune_model.fc.parameters(), 'lr': 1e-3}
], weight_decay=1e-4)

print(f'Fine-tuning model trainable params: {count_trainable_params(finetune_model):,}')
finetune_model, finetune_history = train_model(
    finetune_model,
    train_loader_aug,
    val_loader,
    criterion,
    optimizer,
    epochs=EPOCHS_TRANSFER
)

finetune_metrics, y_true_finetune, y_pred_finetune = evaluate_model(
    finetune_model, test_loader, criterion
)
plot_history(finetune_history, 'Fine-tuning - ResNet18 layer4 + fc')
plot_confusion(
    y_true_finetune, y_pred_finetune, class_names,
    'Fine-tuning - Test Confusion Matrix'
)

display(pd.DataFrame(
    classification_report(
        y_true_finetune, y_pred_finetune,
        target_names=class_names, output_dict=True
    )
).T)
results['Fine-tuning (ResNet18 layer4+fc)'] = {
    'test_loss': finetune_metrics['loss'],
    'test_accuracy': finetune_metrics['accuracy'],
    'trainable_params': count_trainable_params(finetune_model)
}
print(results['Fine-tuning (ResNet18 layer4+fc)'])
```

**핵심**: layer4를 함께 학습하면 우리 데이터에 더 맞는 특징을 얻을 수 있지만, 학습률을 낮춰 사전학습 지식을 보존해야 한다. feature extraction보다 항상 좋은 것은 아니며, 데이터 양과 도메인 유사도에 따라 달라진다.

---

<a id="part8"></a>

## 11. 성능 비교와 오분류 분석 [↑](#toc)

**학습목표**: 세 모델의 성능을 정량적으로 비교하고, 오분류 원인을 시각적으로 분석할 수 있다.

```python
comparison_df = pd.DataFrame(results).T
comparison_df['test_accuracy_pct'] = (
    comparison_df['test_accuracy'] * 100
).round(2)
comparison_df['trainable_params'] = (
    comparison_df['trainable_params'].astype(int)
)
display(comparison_df.sort_values('test_accuracy', ascending=False))

plot_df = comparison_df.sort_values('test_accuracy_pct')
colors = ['#94A3B8', '#60A5FA', '#34D399', '#F59E0B'][:len(plot_df)]
fig, ax = plt.subplots(figsize=(8, 4))
plot_df['test_accuracy_pct'].plot(kind='barh', ax=ax, color=colors)
ax.set_xlabel('test accuracy (%)')
ax.set_title('모델별 Test Accuracy 비교')
plt.tight_layout()
plt.show()

best_model_name = comparison_df['test_accuracy'].idxmax()
print(f'가장 높은 test accuracy를 기록한 모델: {best_model_name}')

if 'Baseline CNN' in results and 'Augmented CNN' in results:
    delta_aug = 100 * (
        results['Augmented CNN']['test_accuracy']
        - results['Baseline CNN']['test_accuracy']
    )
    print(f'증강 효과: {delta_aug:+.2f}%p')

if 'Baseline CNN' in results and 'Transfer Learning (ResNet18)' in results:
    delta_transfer = 100 * (
        results['Transfer Learning (ResNet18)']['test_accuracy']
        - results['Baseline CNN']['test_accuracy']
    )
    print(f'전이학습 효과: {delta_transfer:+.2f}%p')

if 'Baseline CNN' in results and 'Fine-tuning (ResNet18 layer4+fc)' in results:
    delta_finetune = 100 * (
        results['Fine-tuning (ResNet18 layer4+fc)']['test_accuracy']
        - results['Baseline CNN']['test_accuracy']
    )
    print(f'Fine-tuning 효과: {delta_finetune:+.2f}%p')
```

#### 오분류 이미지 시각화

정확도 숫자만 보면 왜 틀렸는지 알기 어렵습니다.

아래 셀은:

- 가장 성능이 높은 모델을 자동으로 선택하고
- test 세트에서 틀린 이미지를 최대 9장 보여 줍니다.

이 셀을 통해 `사람이 봐도 헷갈리는 경우인지`, `배경이나 자세에 끌려간 것인지`, `고양이/강아지 특징을 잘못 본 것인지`를 토론할 수 있습니다.

```python
def collect_misclassified_samples(
    model, dataset, class_names, max_items=9
):
    """
    오분류 샘플을 수집합니다.
    DataLoader 대신 개별 접근하는 이유: 오분류 이미지의 원본을
    인덱스와 함께 보존하기 위해서입니다.
    """
    model.eval()
    samples = []
    for idx in range(len(dataset)):
        image, label = dataset[idx]
        with torch.no_grad():
            logit = model(image.unsqueeze(0).to(device))
            pred = int((torch.sigmoid(logit).item()) >= 0.5)
        if pred != int(label):
            samples.append({
                'image': image,
                'true_label': class_names[int(label)],
                'pred_label': class_names[pred],
                'index': idx
            })
        if len(samples) >= max_items:
            break
    return samples


def show_misclassified_images(
    model, dataset, class_names, title, max_items=9
):
    samples = collect_misclassified_samples(
        model, dataset, class_names, max_items=max_items
    )
    if not samples:
        print('오분류 샘플이 없습니다.')
        return

    cols = 3
    rows = (len(samples) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows))
    axes = np.array(axes).reshape(-1)

    for ax, sample in zip(axes, samples):
        ax.imshow(denormalize(sample['image']).permute(1, 2, 0))
        ax.set_title(
            f"true={sample['true_label']}\n"
            f"pred={sample['pred_label']}\n"
            f"idx={sample['index']}"
        )
        ax.axis('off')

    for ax in axes[len(samples):]:
        ax.axis('off')

    plt.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()


model_registry = {
    'Baseline CNN': baseline_model,
    'Augmented CNN': aug_model,
    'Transfer Learning (ResNet18)': transfer_model
}
if 'finetune_model' in globals():
    model_registry['Fine-tuning (ResNet18 layer4+fc)'] = finetune_model

selected_model_name = (
    best_model_name
    if 'best_model_name' in globals()
    else 'Transfer Learning (ResNet18)'
)
selected_model = model_registry[selected_model_name]
show_misclassified_images(
    selected_model,
    test_ds,
    class_names,
    title=f'{selected_model_name} - 오분류 샘플',
    max_items=9
)
```

**핵심**: 숫자만 보는 것이 아니라, 오분류 샘플을 시각적으로 확인하면 모델의 약점을 더 깊이 이해할 수 있다. 사람이 봐도 헷갈리는 이미지인지, 모델만 헷갈리는 이미지인지를 구분하는 것이 중요하다.

---

<a id="part-deploy"></a>

## 12. 모델 저장과 웹 서비스 배포 [↑](#toc)

**학습목표**: 학습된 모델을 저장하고 Streamlit 웹 서비스로 배포하여, 누구나 이미지를 업로드해 개/고양이를 분류할 수 있게 만들 수 있다.

> **선수 학습**: Streamlit의 실행 모델, 위젯, 캐싱 등 기본 개념은 [6-2. Streamlit 기초](/deeplearning/streamlit-basics)를, 배포 방법은 [6-3. 웹서비스 배포: MNIST](/deeplearning/streamlit-mnist-deploy)를 참고하세요.

지금까지 학습한 모델 중 가장 성능이 좋은 모델을 저장하고, Streamlit으로 웹 서비스를 만들어 **Streamlit Community Cloud에 무료 배포**합니다.

### 12-1. 모델 저장

가장 성능이 좋은 모델(보통 Fine-tuning 또는 Transfer Learning)의 가중치를 저장합니다.

```python
import torch

# 가장 성능이 좋은 모델 선택
best_name = comparison_df['test_accuracy'].idxmax()
best_model_obj = model_registry[best_name]
print(f'저장할 모델: {best_name}')

# state_dict 저장 (모델 구조는 별도로 정의해야 로드 가능)
torch.save(best_model_obj.state_dict(), 'best_model.pt')
print(f'모델 저장 완료: best_model.pt ({os.path.getsize("best_model.pt") / 1e6:.1f} MB)')
```

Google Drive에 백업합니다.

```python
from google.colab import drive
drive.mount('/content/drive')

import shutil
save_dir = '/content/drive/MyDrive/dogs_vs_cats_deploy'
os.makedirs(save_dir, exist_ok=True)
shutil.copy('best_model.pt', save_dir)
print(f'Google Drive 백업 완료: {save_dir}/best_model.pt')
```

### 12-2. 저장된 모델로 단일 이미지 예측 테스트

배포 전에, 저장된 모델을 새로 로드하여 정상 작동하는지 확인합니다.

```python
# 모델 구조를 다시 정의하고 가중치 로드
test_model = models.resnet18(weights=None)
test_model.fc = nn.Linear(test_model.fc.in_features, 1)
test_model.load_state_dict(torch.load('best_model.pt', map_location='cpu'))
test_model.eval()

# 테스트 이미지 1장으로 예측
sample_path = sorted((SPLIT_DIR / 'test' / 'cat').glob('*.jpg'))[0]
sample_img = Image.open(sample_path).convert('RGB')
input_tensor = eval_transform(sample_img).unsqueeze(0)

with torch.no_grad():
    logit = test_model(input_tensor)
    prob = torch.sigmoid(logit).item()
    if prob >= 0.5:
        pred_label = 'dog'
        confidence = prob
    else:
        pred_label = 'cat'
        confidence = 1 - prob

print(f'예측: {pred_label} ({confidence:.1%})')
plt.imshow(sample_img)
plt.title(f'pred: {pred_label} ({confidence:.1%})')
plt.axis('off')
plt.show()
```

### 12-3. Streamlit 앱 코드

아래 코드를 `app.py`로 저장합니다. 이미지를 업로드하면 모델이 개/고양이를 분류하고 확률을 표시합니다.

```python
# app.py — Dogs vs Cats 분류 웹 서비스
import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import gdown
import os

# ── 모델 로드 (앱 시작 시 1회만 실행) ──────────────────────
MODEL_URL = "https://drive.google.com/uc?id=여기에_파일ID_입력"
MODEL_PATH = "best_model.pt"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 1)
    model.load_state_dict(
        torch.load(MODEL_PATH, map_location='cpu', weights_only=True)
    )
    model.eval()
    return model

model = load_model()

# ── 이미지 전처리 (학습 시 eval_transform과 동일) ──────────
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

# ── 페이지 설정 ───────────────────────────────────────────
st.set_page_config(page_title="Dogs vs Cats 분류기", page_icon="🐾")
st.title("🐾 Dogs vs Cats 분류기")
st.caption("이미지를 업로드하면 개인지 고양이인지 분류합니다.")

# ── 이미지 업로드 ─────────────────────────────────────────
uploaded = st.file_uploader(
    "이미지를 선택하세요", type=["jpg", "jpeg", "png"]
)

if uploaded is not None:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="업로드된 이미지", use_container_width=True)

    # ── 예측 ──────────────────────────────────────────────
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        logit = model(input_tensor)
        prob = torch.sigmoid(logit).item()

    # ── 결과 표시 ─────────────────────────────────────────
    is_dog = prob >= 0.5
    label = "🐶 Dog" if is_dog else "🐱 Cat"
    confidence = prob if is_dog else 1 - prob

    st.markdown(f"### 예측 결과: {label}")
    st.metric("확신도", f"{confidence:.1%}")

    # 확률 바 시각화
    col1, col2 = st.columns(2)
    with col1:
        st.write("🐱 Cat")
        st.progress(1 - prob)
    with col2:
        st.write("🐶 Dog")
        st.progress(prob)
else:
    st.info("왼쪽 위의 업로드 버튼을 눌러 이미지를 선택하세요.")
```

### 12-4. Streamlit Community Cloud 배포

#### Step 1: GitHub 저장소 준비

아래 3개 파일을 GitHub 저장소에 올립니다.

```
dogs-vs-cats-app/
├── app.py              ← 위의 Streamlit 코드
└── requirements.txt    ← 아래 내용
```

> **모델 파일(`best_model.pt`)은 GitHub에 올리지 않습니다.** Google Drive에 업로드한 뒤, 앱이 시작할 때 자동으로 다운로드합니다.

`requirements.txt`:

```text
streamlit
torch
torchvision
Pillow
gdown
```

#### Step 2: Streamlit Cloud 연결

1. [share.streamlit.io](https://share.streamlit.io/) 접속
2. GitHub 계정 연결
3. **New app** 클릭
4. 저장소, 브랜치, 메인 파일(`app.py`) 선택
5. **Deploy** 클릭

약 2~3분 후 `https://your-app-name.streamlit.app` 형태의 **영구 URL**이 생성됩니다.

#### Step 3: 배포 확인

배포된 URL에 접속하여 테스트 이미지를 업로드하고 분류 결과를 확인합니다.

| 항목 | 내용 |
|------|------|
| 무료 플랜 제한 | RAM 1GB, 앱 슬립(7일 미접속 시) |
| 모델 크기 | ResNet18 ~45MB → 제한 내 |
| 깨어나기 | 슬립 후 접속하면 자동 재시작 (~30초) |

**핵심**: 학습된 모델을 `torch.save()`로 저장하고, Streamlit 앱으로 감싸서 Streamlit Community Cloud에 배포하면 누구나 접근 가능한 웹 분류기를 무료로 운영할 수 있다.

> **확인**: 배포된 URL에서 개 사진과 고양이 사진을 각각 업로드해 보세요. 확신도가 어떻게 다른가요? 오분류 분석에서 봤던 "헷갈리는 이미지"를 업로드하면 어떤 결과가 나오나요?

---

<a id="part9"></a>

## 13. 통합 정리 [↑](#toc)

아래 질문에 답해 보세요.

1. 기본 CNN은 어떤 오분류를 자주 만들었나요?
2. 이미지 증강은 val / test 성능을 얼마나 바꾸었나요?
3. 전이학습 모델은 왜 적은 학습 파라미터로도 높은 성능을 낼 수 있었나요?
4. fine-tuning은 feature extraction보다 얼마나 나아졌나요? 그 차이가 항상 클까요?
5. 오분류 이미지는 사람이 봐도 헷갈리나요, 아니면 모델만 헷갈리나요?
6. 만약 강아지 / 고양이가 아니라 의료 영상처럼 도메인이 크게 다르면, 같은 전이학습 전략이 그대로 통할까요?

#### 선택 확장 과제

- `USE_SMALL_SUBSET = False` 로 바꾸고 전체 데이터로 실험해 보기
- 전이학습에서도 증강 강도를 조금씩 바꿔 보기
- ResNet18 대신 MobileNetV3나 EfficientNet 계열로 바꿔 보기
- 오분류 샘플 옆에 예측 확률까지 함께 표시해 보기
- SimpleCNN에 `BatchNorm2d`를 추가해서 Conv-BN-ReLU 패턴을 적용해 보기
- Fine-tuning을 `train_loader_base`로도 실험하여 순수 unfreeze 효과를 분리해 보기
- 학습률 스케줄러(`CosineAnnealingLR` 등)를 추가해서 성능 변화를 관찰해 보기
- 배포된 Streamlit 앱에 "예측 히스토리" 기능을 추가해 보기 (업로드한 이미지와 결과를 리스트로 표시)
- Streamlit 앱에서 여러 모델(Baseline, Augmented, Transfer)을 선택하여 비교할 수 있게 만들어 보기

#### 참고

- [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [Torchvision ImageFolder](https://pytorch.org/vision/stable/generated/torchvision.datasets.ImageFolder.html)
- [Torchvision Transforms](https://pytorch.org/vision/stable/transforms.html)
- [Kaggle Dogs vs Cats competition](https://www.kaggle.com/c/dogs-vs-cats)
- [Streamlit Community Cloud](https://share.streamlit.io/)
- [Streamlit 공식 문서](https://docs.streamlit.io/)
