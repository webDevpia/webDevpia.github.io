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

<a id="toc"></a>

## 진행 순서

1. [데이터 준비](#part1) - Google Drive 또는 직접 업로드로 train.zip 준비
2. [교육용 split 만들기](#part2) - ImageFolder용 train / val / test 폴더 재구성
3. [Transform과 DataLoader](#part3) - 기본/증강 transform, 모델, 헬퍼 함수 정의
4. [기본 CNN 학습](#part4) - 증강 없이 처음부터 학습 및 평가
5. [이미지 증강 CNN 학습](#part5) - 증강 적용 후 재학습 및 비교
6. [전이학습](#part6) - ResNet18 feature extraction
7. [Fine-tuning](#part7) - ResNet18 layer4 + fc 미세 조정 (선택 확장)
8. [성능 비교와 오분류 분석](#part8) - 세 모델 비교 + 오분류 시각화
9. [통합 정리](#part9) - 해석 가이드와 확장 과제

### 이 노트북의 중요한 원칙

- Kaggle competition의 unlabeled test 파일은 교육용 평가에 직접 쓰지 않습니다.
- 대신 labeled train 이미지를 train / val / test로 직접 나눕니다.
- 증강은 train 데이터에만 적용하고, val / test에는 적용하지 않습니다.
- 비교의 공정성을 위해 같은 split을 재사용합니다.

```python
import os
import time
import random
import shutil
import zipfile
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

IN_COLAB = 'COLAB_RELEASE_TAG' in os.environ

SEED = 42

def seed_everything(seed=SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

seed_everything(SEED)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if torch.cuda.is_available():
    torch.backends.cudnn.benchmark = True

BASE_DIR = Path('/content/dogs_vs_cats')
COMP_DIR = BASE_DIR / 'competition_files'
RAW_DIR = BASE_DIR / 'raw'
SPLIT_DIR = BASE_DIR / 'prepared_data'
for d in [BASE_DIR, COMP_DIR, RAW_DIR, SPLIT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

print(f'device: {device}')
print(f'torch: {torch.__version__}')
print(f'base dir: {BASE_DIR}')
```

---

<a id="part1"></a>

## 1. 데이터 준비 [↑](#toc)

**학습목표**: Kaggle Dogs vs Cats 데이터를 Colab 환경에 올리고 사용 가능하게 준비할 수 있다.

이 셀을 실행하기 전에 준비할 것:

1. Kaggle Dogs vs Cats competition 페이지에서 규칙을 수락합니다.
2. 브라우저에서 `train.zip`을 직접 다운로드합니다.
3. Google Drive에 `train.zip`을 올려두거나, Colab 왼쪽 파일 패널에서 직접 업로드합니다.

실습 노트:

- 가장 편한 방법은 Google Drive에 `train.zip`을 미리 올려두고 자동 복사 셀을 쓰는 것입니다.
- 가장 간단한 수동 방법은 `train.zip` 하나만 직접 업로드하는 것입니다.
- 이미 `/content`, `/content/dogs_vs_cats`, `/content/dogs_vs_cats/competition_files`에 파일을 올려둔 경우 아래 셀이 자동으로 찾아 재사용합니다.
- 실수로 전체 competition 압축파일(`dogs-vs-cats.zip`)을 올려도 내부의 `train.zip`을 자동으로 꺼냅니다.
- `train.zip`은 파일 크기가 크므로 업로드에 시간이 걸릴 수 있습니다.
- `test1.zip`은 라벨이 없으므로 이 노트북에서는 사용하지 않습니다.

#### 선택 옵션: Google Drive에서 자동 복사

Colab 업로드가 불안정하거나 느리면, `train.zip`을 Google Drive에 미리 올려두고 아래 셀을 실행하세요.

- 기본 탐색 경로: `/content/drive/MyDrive/train.zip`
- 추가 탐색 경로: `/content/drive/MyDrive/dogs_vs_cats/train.zip`, `/content/drive/MyDrive/datasets/dogs_vs_cats/train.zip`
- 다른 위치에 두었다면 `DRIVE_ARCHIVE_PATH`에 직접 경로를 적으면 됩니다.
- 이 셀에서 파일을 찾지 못하면, 다음 셀에서 직접 업로드 방식으로 계속 진행하면 됩니다.

```python
USE_GOOGLE_DRIVE = True
DRIVE_ARCHIVE_PATH = ''  # 예: /content/drive/MyDrive/dogs_vs_cats/train.zip

drive_candidates = [
    Path(DRIVE_ARCHIVE_PATH) if DRIVE_ARCHIVE_PATH else None,
    Path('/content/drive/MyDrive/train.zip'),
    Path('/content/drive/MyDrive/dogs_vs_cats/train.zip'),
    Path('/content/drive/MyDrive/datasets/dogs_vs_cats/train.zip'),
    Path('/content/drive/MyDrive/Colab Notebooks/train.zip'),
    Path('/content/drive/MyDrive/dogs-vs-cats.zip'),
    Path('/content/drive/MyDrive/dogs_vs_cats/dogs-vs-cats.zip'),
]

if USE_GOOGLE_DRIVE:
    if not IN_COLAB:
        print('Colab 환경이 아니므로 Google Drive 마운트를 건너뜁니다.')
    else:
        from google.colab import drive

        drive.mount('/content/drive', force_remount=False)
        selected_drive_file = None
        seen = set()
        for candidate in drive_candidates:
            if candidate is None:
                continue
            candidate = Path(candidate)
            candidate_str = str(candidate)
            if candidate_str in seen:
                continue
            seen.add(candidate_str)
            if candidate.exists():
                selected_drive_file = candidate
                break

        if selected_drive_file is None:
            print('Google Drive에서 train.zip 또는 dogs-vs-cats.zip을 찾지 못했습니다. 다음 셀에서 직접 업로드하세요.')
        else:
            target_path = COMP_DIR / selected_drive_file.name
            if selected_drive_file.resolve() != target_path.resolve():
                shutil.copy2(selected_drive_file, target_path)
            print(f'Google Drive에서 파일을 복사했습니다: {selected_drive_file} -> {target_path}')
```

```python
train_zip = COMP_DIR / 'train.zip'
competition_zip = COMP_DIR / 'dogs-vs-cats.zip'


def find_candidate_archives():
    candidates = [
        train_zip,
        competition_zip,
        BASE_DIR / 'train.zip',
        BASE_DIR / 'dogs-vs-cats.zip',
        Path('/content/train.zip'),
        Path('/content/dogs-vs-cats.zip'),
    ]

    for search_dir in [COMP_DIR, BASE_DIR, Path('/content')]:
        if search_dir.exists():
            for zip_path in sorted(search_dir.glob('*.zip')):
                if zip_path not in candidates:
                    candidates.append(zip_path)

    existing = []
    seen = set()
    for candidate in candidates:
        if candidate.exists() and candidate not in seen:
            existing.append(candidate)
            seen.add(candidate)
    return existing


candidates = find_candidate_archives()

if not candidates:
    if not IN_COLAB:
        raise FileNotFoundError(
            f'train.zip 또는 dogs-vs-cats.zip 파일을 {COMP_DIR} 또는 /content 에 직접 배치한 뒤 다시 실행하세요.'
        )

    print('train.zip 또는 dogs-vs-cats.zip 업로드가 필요합니다.')
    print('권장: Kaggle 사이트에서 train.zip만 직접 다운로드해 업로드하세요.')
    from google.colab import files
    uploaded = files.upload()
    if not uploaded:
        raise FileNotFoundError('업로드된 파일이 없습니다.')

    for name, data in uploaded.items():
        target = COMP_DIR / Path(name).name
        target.write_bytes(data)
        print(f'업로드 완료: {target}')

    candidates = find_candidate_archives()

if not candidates:
    raise FileNotFoundError('업로드 후에도 사용할 압축 파일을 찾지 못했습니다.')

archive_path = candidates[0]
print(f'사용할 압축 파일: {archive_path}')

if archive_path.name == 'train.zip':
    if archive_path.resolve() != train_zip.resolve():
        shutil.copy2(archive_path, train_zip)
        print(f'train.zip을 작업 폴더로 복사했습니다: {train_zip}')
elif archive_path.suffix == '.zip':
    print('업로드한 압축 파일에서 train.zip 또는 train/ 폴더를 확인합니다...')
    with zipfile.ZipFile(archive_path) as zf:
        member_names = zf.namelist()
        basename_map = {Path(name).name: name for name in member_names}

        if 'train.zip' in basename_map:
            with zf.open(basename_map['train.zip']) as src, open(train_zip, 'wb') as dst:
                shutil.copyfileobj(src, dst)
            print('압축 내부의 train.zip을 추출했습니다.')
        elif any(Path(name).parts and Path(name).parts[0] == 'train' for name in member_names):
            if not (RAW_DIR / 'train').exists():
                zf.extractall(RAW_DIR)
                print('압축 내부의 train/ 폴더를 raw 디렉터리에 바로 풀었습니다.')
        else:
            raise FileNotFoundError('업로드한 zip 파일 안에서 train.zip 또는 train/ 폴더를 찾지 못했습니다.')
else:
    raise ValueError(f'지원하지 않는 파일 형식입니다: {archive_path.name}')

if not (RAW_DIR / 'train').exists():
    print('train.zip 압축 해제 중...')
    with zipfile.ZipFile(train_zip) as zf:
        zf.extractall(RAW_DIR)
else:
    print('이미 raw/train 폴더가 존재합니다.')

raw_train_dir = RAW_DIR / 'train'
if not raw_train_dir.exists():
    raise FileNotFoundError('raw/train 폴더를 찾지 못했습니다. 업로드한 파일을 다시 확인하세요.')

print(f'raw image count: {len(list(raw_train_dir.glob("*.jpg"))):,}')
```

**핵심**: Google Drive 또는 직접 업로드로 `train.zip`을 Colab에 가져온다. 경쟁용 test 데이터는 라벨이 없으므로, labeled train 이미지만 사용한다.

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


def prepare_dogs_vs_cats_split(raw_train_dir, output_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, max_per_class=None, seed=42, rebuild=False):
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
                'count': len(list((base_dir / split_name / class_name).glob('*.jpg')))
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

```python
import matplotlib.pyplot as plt
from PIL import Image

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    pass

def show_examples(split_name='train', n=4):
    fig, axes = plt.subplots(2, n, figsize=(3 * n, 6))
    for row, class_name in enumerate(['cat', 'dog']):
        paths = sorted((SPLIT_DIR / split_name / class_name).glob('*.jpg'))[:n]
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

```python
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

train_transform_base = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])

train_transform_aug = transforms.Compose([
    transforms.RandomResizedCrop(IMG_SIZE, scale=(0.8, 1.0)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])

eval_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])

train_ds_base = datasets.ImageFolder(SPLIT_DIR / 'train', transform=train_transform_base)
train_ds_aug = datasets.ImageFolder(SPLIT_DIR / 'train', transform=train_transform_aug)
val_ds = datasets.ImageFolder(SPLIT_DIR / 'val', transform=eval_transform)
test_ds = datasets.ImageFolder(SPLIT_DIR / 'test', transform=eval_transform)

class_names = train_ds_base.classes
print('classes:', class_names)

train_loader_base = DataLoader(train_ds_base, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS, pin_memory=torch.cuda.is_available())
train_loader_aug = DataLoader(train_ds_aug, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS, pin_memory=torch.cuda.is_available())
val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=torch.cuda.is_available())
test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=torch.cuda.is_available())


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

```python
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.3),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)


def count_trainable_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def accuracy_from_logits(logits, labels):
    preds = (torch.sigmoid(logits) >= 0.5).long().view(-1)
    return (preds == labels.long()).sum().item()


def run_epoch(model, loader, criterion, optimizer=None):
    is_train = optimizer is not None
    model.train() if is_train else model.eval()

    running_loss = 0.0
    running_corrects = 0
    total = 0

    for inputs, labels in loader:
        inputs = inputs.to(device)
        labels = labels.float().unsqueeze(1).to(device)

        if is_train:
            optimizer.zero_grad()

        with torch.set_grad_enabled(is_train):
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            if is_train:
                loss.backward()
                optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        running_corrects += accuracy_from_logits(outputs, labels.view(-1))
        total += inputs.size(0)

    return running_loss / total, running_corrects / total


def train_model(model, train_loader, val_loader, criterion, optimizer, epochs):
    best_state = deepcopy(model.state_dict())
    best_val_acc = 0.0
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

    for epoch in range(epochs):
        start = time.time()
        train_loss, train_acc = run_epoch(model, train_loader, criterion, optimizer=optimizer)
        val_loss, val_acc = run_epoch(model, val_loader, criterion, optimizer=None)

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
    model.eval()
    loss, acc = run_epoch(model, loader, criterion, optimizer=None)

    all_preds = []
    all_labels = []
    for inputs, labels in loader:
        outputs = model(inputs.to(device))
        preds = (torch.sigmoid(outputs) >= 0.5).long().view(-1).cpu().numpy()
        all_preds.extend(preds.tolist())
        all_labels.extend(labels.numpy().tolist())

    return {'loss': loss, 'accuracy': acc}, np.array(all_labels), np.array(all_preds)


def plot_history(history, title):
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
            ax.text(j, i, cm[i, j], ha='center', va='center', color='black')
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.show()


results = {}
```

**핵심**: 증강은 train 데이터에만 적용하고, val / test는 항상 동일한 전처리를 사용해야 공정한 비교가 가능하다. 모델 구조와 헬퍼 함수를 미리 정의해 두면, 이후 실험에서 코드 중복 없이 비교할 수 있다.

---

<a id="part4"></a>

## 4. 기본 CNN 학습 [↑](#toc)

**학습목표**: 데이터 증강 없이 작은 CNN을 처음부터 학습하고, 과적합 경향을 관찰할 수 있다.

여기서는 데이터 증강 없이, 작은 CNN을 처음부터 학습합니다.

해석 포인트:

- train 성능은 빨리 올라가는데 val / test 성능이 기대만큼 안 오를 수 있습니다.
- 이것은 작은 데이터에서 scratch 학습이 과적합되기 쉽다는 신호일 수 있습니다.

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

baseline_metrics, y_true_base, y_pred_base = evaluate_model(baseline_model, test_loader, criterion)
plot_history(baseline_history, 'Baseline CNN')
plot_confusion(y_true_base, y_pred_base, class_names, 'Baseline CNN - Test Confusion Matrix')

display(pd.DataFrame(classification_report(y_true_base, y_pred_base, target_names=class_names, output_dict=True)).T)
results['Baseline CNN'] = {
    'test_loss': baseline_metrics['loss'],
    'test_accuracy': baseline_metrics['accuracy'],
    'trainable_params': count_trainable_params(baseline_model)
}
print(results['Baseline CNN'])
```

**핵심**: 작은 데이터에서 scratch CNN은 과적합되기 쉽다. train accuracy는 높지만 val / test는 상대적으로 낮을 수 있다. 이 결과가 이후 증강과 전이학습의 비교 기준선이 된다.

---

<a id="part5"></a>

## 5. 이미지 증강 CNN 학습 [↑](#toc)

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

aug_metrics, y_true_aug, y_pred_aug = evaluate_model(aug_model, test_loader, criterion)
plot_history(aug_history, 'Augmented CNN')
plot_confusion(y_true_aug, y_pred_aug, class_names, 'Augmented CNN - Test Confusion Matrix')

display(pd.DataFrame(classification_report(y_true_aug, y_pred_aug, target_names=class_names, output_dict=True)).T)
results['Augmented CNN'] = {
    'test_loss': aug_metrics['loss'],
    'test_accuracy': aug_metrics['accuracy'],
    'trainable_params': count_trainable_params(aug_model)
}
print(results['Augmented CNN'])
```

**핵심**: 모델 구조가 동일하고 train transform만 바꿨으므로, 성능 차이는 순수하게 증강 효과로 해석할 수 있다. 증강은 데이터를 실제로 늘리지 않지만, 매 에폭마다 다른 변형을 보여 줌으로써 일반화 성능을 높인다.

---

<a id="part6"></a>

## 6. 전이학습 [↑](#toc)

**학습목표**: 사전학습된 ResNet18의 특징 표현을 활용하여, 적은 파라미터로 높은 성능을 얻을 수 있다.

이번에는 `ResNet18`의 사전학습 가중치를 불러와서 마지막 분류기만 새로 학습합니다.

여기서는 전이학습 효과를 분명히 보기 위해, 기본 train transform과 같은 입력 분포를 사용합니다.

즉:

- baseline vs transfer: `사전학습된 특징 표현`의 차이
- baseline vs augmented: `데이터 표현 다양화`의 차이

로 해석할 수 있습니다.

```python
weights = models.ResNet18_Weights.DEFAULT
transfer_model = models.resnet18(weights=weights)
for param in transfer_model.parameters():
    param.requires_grad = False
transfer_model.fc = nn.Linear(transfer_model.fc.in_features, 1)
transfer_model = transfer_model.to(device)

criterion = nn.BCEWithLogitsLoss()
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

transfer_metrics, y_true_transfer, y_pred_transfer = evaluate_model(transfer_model, test_loader, criterion)
plot_history(transfer_history, 'Transfer Learning - ResNet18')
plot_confusion(y_true_transfer, y_pred_transfer, class_names, 'Transfer Learning - Test Confusion Matrix')

display(pd.DataFrame(classification_report(y_true_transfer, y_pred_transfer, target_names=class_names, output_dict=True)).T)
results['Transfer Learning (ResNet18)'] = {
    'test_loss': transfer_metrics['loss'],
    'test_accuracy': transfer_metrics['accuracy'],
    'trainable_params': count_trainable_params(transfer_model)
}
print(results['Transfer Learning (ResNet18)'])
```

**핵심**: 사전학습된 특징 표현을 활용하면, 학습 가능한 파라미터가 fc 레이어뿐이어도 scratch CNN보다 높은 성능을 얻을 수 있다. ImageNet에서 학습한 범용 시각 특징이 개/고양이 분류에도 유효하기 때문이다.

---

<a id="part7"></a>

## 7. Fine-tuning (선택 확장) [↑](#toc)

**학습목표**: Feature extraction과 fine-tuning의 차이를 실험으로 비교할 수 있다.

위의 전이학습은 `feature extraction` 방식이었습니다.

이번 확장 셀에서는:

- `layer4`와 `fc`만 학습 가능하게 풀고
- 낮은 학습률로 미세 조정(fine-tuning)합니다.

즉, 사전학습 지식을 너무 크게 망가뜨리지 않으면서, 우리 데이터셋에 조금 더 맞게 조정하는 실험입니다.

실전에서는 fine-tuning에서도 보통 약한 증강을 함께 쓰므로, 여기서는 `train_loader_aug`를 사용합니다.

```python
finetune_model = models.resnet18(weights=weights)
for param in finetune_model.parameters():
    param.requires_grad = False
for param in finetune_model.layer4.parameters():
    param.requires_grad = True
finetune_model.fc = nn.Linear(finetune_model.fc.in_features, 1)
finetune_model = finetune_model.to(device)

criterion = nn.BCEWithLogitsLoss()
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

finetune_metrics, y_true_finetune, y_pred_finetune = evaluate_model(finetune_model, test_loader, criterion)
plot_history(finetune_history, 'Fine-tuning - ResNet18 layer4 + fc')
plot_confusion(y_true_finetune, y_pred_finetune, class_names, 'Fine-tuning - Test Confusion Matrix')

display(pd.DataFrame(classification_report(y_true_finetune, y_pred_finetune, target_names=class_names, output_dict=True)).T)
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

## 8. 성능 비교와 오분류 분석 [↑](#toc)

**학습목표**: 세 모델의 성능을 정량적으로 비교하고, 오분류 원인을 시각적으로 분석할 수 있다.

```python
comparison_df = pd.DataFrame(results).T
comparison_df['test_accuracy_pct'] = (comparison_df['test_accuracy'] * 100).round(2)
comparison_df['trainable_params'] = comparison_df['trainable_params'].astype(int)
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
    delta_aug = 100 * (results['Augmented CNN']['test_accuracy'] - results['Baseline CNN']['test_accuracy'])
    print(f'증강 효과: {delta_aug:+.2f}%p')

if 'Baseline CNN' in results and 'Transfer Learning (ResNet18)' in results:
    delta_transfer = 100 * (results['Transfer Learning (ResNet18)']['test_accuracy'] - results['Baseline CNN']['test_accuracy'])
    print(f'전이학습 효과: {delta_transfer:+.2f}%p')

if 'Baseline CNN' in results and 'Fine-tuning (ResNet18 layer4+fc)' in results:
    delta_finetune = 100 * (results['Fine-tuning (ResNet18 layer4+fc)']['test_accuracy'] - results['Baseline CNN']['test_accuracy'])
    print(f'Fine-tuning 효과: {delta_finetune:+.2f}%p')
```

#### 오분류 이미지 시각화

정확도 숫자만 보면 왜 틀렸는지 알기 어렵습니다.

아래 셀은:

- 가장 성능이 높은 모델을 자동으로 선택하고
- test 세트에서 틀린 이미지를 최대 9장 보여 줍니다.

이 셀을 통해 `사람이 봐도 헷갈리는 경우인지`, `배경이나 자세에 끌려간 것인지`, `고양이/강아지 특징을 잘못 본 것인지`를 토론할 수 있습니다.

```python
def collect_misclassified_samples(model, dataset, class_names, max_items=9):
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


def show_misclassified_images(model, dataset, class_names, title, max_items=9):
    samples = collect_misclassified_samples(model, dataset, class_names, max_items=max_items)
    if not samples:
        print('오분류 샘플이 없습니다.')
        return

    cols = 3
    rows = (len(samples) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows))
    axes = np.array(axes).reshape(-1)

    for ax, sample in zip(axes, samples):
        ax.imshow(denormalize(sample['image']).permute(1, 2, 0))
        ax.set_title(f"true={sample['true_label']}\npred={sample['pred_label']}\nidx={sample['index']}")
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

selected_model_name = best_model_name if 'best_model_name' in globals() else 'Transfer Learning (ResNet18)'
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

<a id="part9"></a>

## 9. 통합 정리 [↑](#toc)

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

#### 참고

- PyTorch Transfer Learning Tutorial
- Torchvision ImageFolder
- Torchvision RandomHorizontalFlip / RandomResizedCrop
- Kaggle Dogs vs Cats competition data
