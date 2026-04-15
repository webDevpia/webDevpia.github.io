---
title: 7-부록. Dogs vs Cats 코드 상세 설명
layout: default
parent: DeepLearning
nav_order: 7.1
permalink: /deeplearning/DogsVsCats-code-guide
nav_exclude: true
---

# 7-부록. Dogs vs Cats 코드 한 줄씩 상세 설명

> 이 문서는 [7. 전이학습 - Dogs vs Cats 실전 분류](/deeplearning/DogsVsCats) 교안의 모든 코드를 한 줄씩 해설합니다.

---

## 0. import와 환경 설정

```python
import os, time, random, shutil, zipfile
```
- `os`: 파일 경로, 환경 변수 등 운영체제 관련 기능
- `time`: 학습 시간 측정용 (`time.time()`)
- `random`: 데이터 셔플 시 랜덤 시드 고정
- `shutil`: 파일 복사(`shutil.copy2`) 및 폴더 삭제(`shutil.rmtree`)
- `zipfile`: train.zip 압축 해제

```python
from copy import deepcopy
```
- 모델 가중치를 완전히 독립적으로 복사하는 함수
- `best_state = deepcopy(model.state_dict())` 에서 사용
- 얕은 복사(=)를 하면 모델이 학습을 계속할 때 best 시점의 가중치도 같이 바뀌므로, 깊은 복사가 필요

```python
from pathlib import Path
```
- 파일/폴더 경로를 객체로 다루는 클래스
- `Path('a') / 'b' / 'c'`처럼 `/` 연산자로 경로 조합
- `.glob()`, `.exists()`, `.mkdir()` 등 편리한 메서드 제공

```python
import numpy as np
```
- 수치 연산 라이브러리. 정확도 계산, confusion matrix 결과 처리 등에 사용

```python
import pandas as pd
```
- 데이터프레임 라이브러리. split별 이미지 수 표, classification_report 결과 표시에 사용

```python
import torch
```
- PyTorch 핵심 라이브러리. 텐서 연산, GPU 제어, 모델 저장/로드

```python
import torch.nn as nn
```
- 신경망 레이어 모듈 (`nn.Conv2d`, `nn.Linear`, `nn.Sequential` 등)

```python
import torch.optim as optim
```
- 옵티마이저 모듈 (`optim.Adam`, `optim.SGD` 등)

```python
from torch.utils.data import DataLoader
```
- 데이터셋을 배치 단위로 묶어서 모델에 공급하는 도구
- `shuffle=True`면 매 에폭마다 순서를 섞음

```python
from torchvision import datasets, transforms, models
```
- `datasets`: `ImageFolder` 등 이미지 데이터셋 클래스
- `transforms`: 이미지 전처리/증강 (Resize, Normalize, RandomFlip 등)
- `models`: **사전학습된 모델** (ResNet18, VGG16 등) — 이 수업의 핵심

```python
from sklearn.metrics import confusion_matrix, classification_report
```
- `confusion_matrix`: 혼동 행렬 생성 (TP, FP, FN, TN)
- `classification_report`: precision, recall, f1-score를 한 번에 계산

### 시드 고정

```python
SEED = 42
random.seed(SEED)           # Python 내장 random 모듈의 시드 고정
np.random.seed(SEED)        # NumPy의 시드 고정
torch.manual_seed(SEED)     # PyTorch CPU 시드 고정
```
- 모든 난수 생성기의 시드를 42로 고정하여 **실행할 때마다 같은 결과**를 보장
- 42는 관례적으로 많이 쓰는 시드값 (어떤 숫자든 상관없음)

```python
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)    # GPU 시드도 고정
    torch.backends.cudnn.benchmark = True  # 입력 크기가 고정일 때 속도 최적화
```
- `manual_seed_all`: 멀티 GPU 환경에서도 모든 GPU의 시드를 고정
- `cudnn.benchmark = True`: cuDNN이 입력 크기에 맞는 최적 알고리즘을 자동 선택. 이미지 크기가 224x224로 고정이므로 속도가 약 10~20% 향상

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```
- GPU가 있으면 `cuda`, 없으면 `cpu`를 사용
- 이후 모든 모델과 데이터를 `.to(device)`로 이 장치에 올림

### 작업 디렉터리

```python
BASE_DIR = Path('/content/dogs_vs_cats')
RAW_DIR  = BASE_DIR / 'raw'
SPLIT_DIR = BASE_DIR / 'prepared_data'
```
- `BASE_DIR`: 프로젝트 루트 폴더
- `RAW_DIR`: 원본 이미지 저장 (다운로드한 train.zip 해제 위치)
- `SPLIT_DIR`: train/val/test로 나눈 이미지 저장
- `/` 연산자: `Path('a') / 'b'` → `Path('a/b')` (pathlib의 경로 조합)

```python
for d in [BASE_DIR, RAW_DIR, SPLIT_DIR]:
    d.mkdir(parents=True, exist_ok=True)
```
- 3개 폴더를 순회하며 생성
- `parents=True`: 중간 폴더(dogs_vs_cats)도 없으면 자동 생성
- `exist_ok=True`: 이미 존재해도 에러 안 남

---

## 1. 데이터 준비

```python
!pip install -q gdown
```
- `!`: Colab에서 셸 명령어 실행
- `-q`: quiet 모드 (설치 로그 최소화)
- `gdown`: Google Drive에서 파일을 다운로드하는 패키지

```python
GDRIVE_FILE_ID = 'YOUR_FILE_ID_HERE'
```
- Google Drive 공유 링크에서 추출한 파일 ID
- 예: `https://drive.google.com/file/d/1AbCd.../view` → `1AbCd...` 부분

```python
train_zip = BASE_DIR / 'train.zip'
raw_train_dir = RAW_DIR / 'train'
```
- `train_zip`: 다운로드할 zip 파일 경로
- `raw_train_dir`: 압축 해제 후 원본 이미지가 위치할 폴더

```python
if raw_train_dir.exists():
    print('이미 raw/train 폴더가 존재합니다. 다운로드를 건너뜁니다.')
```
- 이미 다운로드한 경우 중복 작업 방지

```python
gdown.download(id=GDRIVE_FILE_ID, output=str(train_zip), quiet=False)
```
- `id`: Google Drive 파일 ID
- `output`: 저장할 로컬 경로 (Path 객체를 str로 변환)
- `quiet=False`: 다운로드 진행률 표시

```python
with zipfile.ZipFile(train_zip) as zf:
    zf.extractall(RAW_DIR)
```
- `with`문: 파일을 열고 자동으로 닫는 안전한 방식
- `extractall(RAW_DIR)`: RAW_DIR 아래에 모든 파일 해제

```python
print(f'raw image count: {len(list(raw_train_dir.glob("*.jpg"))):,}')
```
- `.glob("*.jpg")`: 폴더 안의 모든 jpg 파일을 찾음
- `list(...)`: 제너레이터를 리스트로 변환하여 `len()` 적용
- `:,`: 천 단위 쉼표 포매팅 (25,000)

---

## 2. 교육용 split 만들기

### 하이퍼파라미터

```python
USE_SMALL_SUBSET = True
MAX_IMAGES_PER_CLASS = 1500
```
- `True`면 클래스당 1,500장만 사용 (무료 Colab에서 실험 가능)
- `False`로 바꾸면 전체 12,500장 사용

```python
TRAIN_RATIO = 0.70    # 학습용 70%
VAL_RATIO = 0.15      # 검증용 15% (학습 중간에 성능 확인)
TEST_RATIO = 0.15     # 테스트용 15% (최종 평가)
```

```python
IMG_SIZE = 224
```
- 모든 이미지를 224x224로 통일
- ResNet18이 ImageNet에서 224x224로 학습되었으므로, 전이학습 시 같은 크기를 사용

```python
BATCH_SIZE = 32
```
- 한 번에 32장씩 묶어서 모델에 입력

```python
NUM_WORKERS = min(2, os.cpu_count() or 2)
```
- 데이터 로딩 병렬 워커 수
- `os.cpu_count()`: CPU 코어 수
- `or 2`: cpu_count()가 None을 반환할 경우 대비

```python
EPOCHS_SCRATCH = 5      # 처음부터 학습하는 모델의 에폭 수
EPOCHS_TRANSFER = 5     # 전이학습 모델의 에폭 수
```

```python
REBUILD_SPLIT = False
```
- `True`면 기존 split을 삭제하고 처음부터 다시 나눔
- `False`면 기존 split이 있을 경우 재사용

### prepare_dogs_vs_cats_split 함수

```python
def prepare_dogs_vs_cats_split(
    raw_train_dir, output_dir,
    train_ratio=0.7, val_ratio=0.15, test_ratio=0.15,
    max_per_class=None, seed=42, rebuild=False
):
```
- 원본 이미지를 train/val/test 폴더 구조로 나누는 함수

```python
    if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-9:
        raise ValueError('train/val/test 비율의 합은 1이어야 합니다.')
```
- 비율 합이 1.0이 아니면 에러 발생
- `1e-9`: 부동소수점 오차 허용 (0.7 + 0.15 + 0.15가 정확히 1.0이 아닐 수 있음)

```python
    rng = random.Random(seed)
```
- 시드가 고정된 **별도의** 난수 생성기 생성
- 전역 random을 오염시키지 않기 위해 독립 객체 사용

```python
    for class_name in ['cat', 'dog']:
        files = sorted(raw_train_dir.glob(f'{class_name}.*.jpg'))
```
- `f'{class_name}.*.jpg'`: cat.0.jpg, cat.1.jpg, ... 패턴 매칭
- `sorted()`: 파일 순서를 일관되게 정렬 (시드와 함께 재현성 보장)

```python
        if max_per_class is not None:
            files = files[:max_per_class]
```
- subset 모드일 때 앞에서 1,500장만 사용

```python
        rng.shuffle(files)
```
- 리스트를 랜덤으로 섞음 (rng의 시드가 고정이므로 매번 같은 순서)

```python
        n_total = len(files)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)
        split_map = {
            'train': files[:n_train],
            'val': files[n_train:n_train + n_val],
            'test': files[n_train + n_val:]
        }
```
- 리스트 슬라이싱으로 비율대로 나눔
- test는 나머지 전부 (`n_train + n_val` 이후)

```python
            shutil.copy2(src, target_dir / src.name)
```
- `copy2`: 파일을 복사하면서 메타데이터(수정 시간 등)도 보존
- `src.name`: 파일명만 추출 (예: `cat.42.jpg`)

---

## 3. Transform과 DataLoader

### ImageNet 정규화

```python
IMAGENET_MEAN = (0.485, 0.456, 0.406)   # R, G, B 채널의 평균
IMAGENET_STD = (0.229, 0.224, 0.225)    # R, G, B 채널의 표준편차
```
- ImageNet 120만 장의 통계값
- 전이학습에서 ResNet18이 이 값으로 정규화된 입력을 기대하므로, 동일하게 적용해야 함
- Baseline CNN도 같은 정규화를 써서 공정한 비교를 보장

### 기본 transform

```python
train_transform_base = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),  # 원본 크기 → 224x224
    transforms.ToTensor(),                     # PIL Image → Tensor, 0~255 → 0.0~1.0
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),  # 채널별 정규화
])
```
- `Compose`: 여러 변환을 순서대로 적용하는 파이프라인
- `Resize((224, 224))`: 어떤 크기의 이미지든 224x224로 강제 변환
- `ToTensor()`: (H, W, C) 형태의 PIL 이미지를 (C, H, W) 형태의 텐서로 변환하고, 픽셀값을 0~1로 스케일링
- `Normalize(mean, std)`: `(값 - mean) / std` → 각 채널의 평균이 ~0, 표준편차가 ~1이 됨

### 증강 transform

```python
train_transform_aug = transforms.Compose([
    transforms.RandomResizedCrop(IMG_SIZE, scale=(0.8, 1.0)),
```
- 이미지의 80~100% 영역을 랜덤으로 잘라서 224x224로 리사이즈
- 매번 다른 영역이 잘리므로, 모델이 객체의 일부만 봐도 인식하도록 학습

```python
    transforms.RandomHorizontalFlip(p=0.5),
```
- 50% 확률로 좌우 반전
- 개와 고양이는 좌우 반전해도 같은 동물이므로, 데이터 다양성을 무료로 2배 확보

```python
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
```
- 밝기, 대비, 채도를 각각 ±20% 범위에서 랜덤 변경
- 조명 조건이 달라져도 인식할 수 있도록 학습

```python
    transforms.ToTensor(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])
```
- 증강 후에도 동일한 텐서 변환과 정규화를 적용

### 데이터셋과 DataLoader

```python
train_ds_base = datasets.ImageFolder(
    SPLIT_DIR / 'train', transform=train_transform_base
)
```
- `ImageFolder`: 폴더 이름(cat, dog)을 자동으로 라벨로 인식
- `transform`: 이미지를 읽을 때마다 이 변환을 자동 적용
- `train_ds_base`: 기본 transform이 적용된 학습 데이터셋
- `train_ds_aug`: 증강 transform이 적용된 학습 데이터셋 (같은 이미지, 다른 변환)

```python
class_names = train_ds_base.classes        # ['cat', 'dog']
print('class_to_idx:', train_ds_base.class_to_idx)  # {'cat': 0, 'dog': 1}
```
- 알파벳 순: cat=0, dog=1
- 이 순서가 sigmoid 출력의 해석 기준: 0.5 이상이면 dog(1)

```python
train_loader_base = DataLoader(
    train_ds_base, batch_size=BATCH_SIZE,
    shuffle=True,           # 매 에폭마다 순서 섞기 (학습용)
    num_workers=NUM_WORKERS, # 병렬 데이터 로딩
    pin_memory=torch.cuda.is_available()  # GPU 전송 속도 향상
)
```
- `shuffle=True`: 학습 데이터는 매번 순서를 섞어야 모델이 순서를 외우지 않음
- `pin_memory=True`: CPU→GPU 데이터 전송을 비동기로 수행하여 속도 향상

```python
val_loader = DataLoader(
    val_ds, batch_size=BATCH_SIZE,
    shuffle=False,   # 검증/테스트는 섞지 않음 (재현성)
    ...
)
```

### 역정규화 함수

```python
def denormalize(tensor, mean=IMAGENET_MEAN, std=IMAGENET_STD):
    mean = torch.tensor(mean).view(3, 1, 1)   # (3,) → (3,1,1)로 shape 변경
    std = torch.tensor(std).view(3, 1, 1)
    return torch.clamp(tensor.cpu() * std + mean, 0, 1)
```
- Normalize의 역연산: `원래값 = 정규화된값 × std + mean`
- `.view(3, 1, 1)`: 채널별 브로드캐스팅을 위해 차원 맞춤
- `torch.clamp(..., 0, 1)`: 값을 0~1 범위로 제한 (matplotlib 표시용)
- `.cpu()`: GPU 텐서를 CPU로 이동 (시각화는 CPU에서)

---

## 4. 모델과 손실 함수

### SimpleCNN 클래스

```python
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
```
- `nn.Module`을 상속하여 PyTorch 모델 클래스 정의
- `super().__init__()`: 부모 클래스의 초기화 메서드 호출 (필수)

```python
        self.features = nn.Sequential(
```
- `nn.Sequential`: 레이어를 순서대로 쌓는 컨테이너. 입력이 순차적으로 통과

```python
            nn.Conv2d(3, 32, kernel_size=3, padding=1),  # 224→224
```
- 입력 채널 3 (RGB) → 출력 채널 32
- `kernel_size=3`: 3x3 필터
- `padding=1`: 상하좌우 1픽셀씩 패딩 → 입력과 출력 크기 동일 (224→224)

```python
            nn.ReLU(inplace=True),
```
- 활성화 함수: 음수를 0으로, 양수는 그대로
- `inplace=True`: 별도 메모리 할당 없이 입력 텐서를 직접 수정 (메모리 절약)

```python
            nn.MaxPool2d(2),                              # 224→112
```
- 2x2 영역에서 최대값만 선택 → 크기가 절반으로 감소
- 정보 압축 + 위치 불변성 확보

```python
            nn.Conv2d(32, 64, kernel_size=3, padding=1),  # 112→112
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),                              # 112→56
            nn.Conv2d(64, 128, kernel_size=3, padding=1), # 56→56
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),                              # 56→28
```
- 같은 패턴 반복: Conv → ReLU → MaxPool
- 채널 수 증가: 32 → 64 → 128 (더 복잡한 특징을 학습)
- 공간 크기 감소: 224 → 112 → 56 → 28

```python
            nn.AdaptiveAvgPool2d((1, 1))                  # 28→1
```
- **어떤 입력 크기든** 1x1로 압축
- 이점: Conv 출력 크기를 수동 계산할 필요 없음
- 출력: (배치, 128, 1, 1) → Flatten 후 128차원 벡터

```python
        self.classifier = nn.Sequential(
            nn.Flatten(),
```
- (배치, 128, 1, 1) → (배치, 128)로 평탄화

```python
            nn.Dropout(0.3),
```
- 학습 시 뉴런의 30%를 랜덤으로 끔 → 과적합 방지
- eval 모드에서는 자동으로 비활성화

```python
            nn.Linear(128, 1)
```
- 128차원 → 1차원 (이진 분류 출력)
- 이 1개의 값(logit)이 0보다 크면 dog, 작으면 cat

```python
    def forward(self, x):
        x = self.features(x)       # Conv + Pool 통과
        return self.classifier(x)  # Flatten + Dropout + Linear
```
- 모델에 이미지를 넣으면 이 순서로 실행됨

```python
def count_trainable_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
```
- `model.parameters()`: 모든 가중치 텐서를 순회
- `p.numel()`: 텐서의 전체 원소 수 (예: (128, 64, 3, 3) → 73,728)
- `if p.requires_grad`: 학습 가능한 파라미터만 셈 (freeze된 것은 제외)

---

## 5. 훈련 도구 정의

### accuracy_from_logits

```python
def accuracy_from_logits(logits, labels):
    preds = (torch.sigmoid(logits) >= 0.5).long().view(-1)
    return (preds == labels.long()).sum().item()
```
- `torch.sigmoid(logits)`: raw 출력값을 0~1 확률로 변환
- `>= 0.5`: 0.5 이상이면 True(1=dog), 미만이면 False(0=cat)
- `.long()`: bool → 정수(0 또는 1)
- `.view(-1)`: 어떤 shape이든 1차원으로 평탄화
- `(preds == labels.long()).sum().item()`: 맞은 개수를 Python 정수로 반환

### run_epoch

```python
def run_epoch(model, loader, criterion, optimizer=None):
    is_train = optimizer is not None
    model.train() if is_train else model.eval()
```
- `optimizer`가 있으면 학습 모드, 없으면 평가 모드
- `model.train()`: Dropout 활성화, BatchNorm은 배치 통계 사용
- `model.eval()`: Dropout 비활성화, BatchNorm은 누적 통계 사용

```python
    for inputs, labels in loader:
        inputs = inputs.to(device)
        labels_bce = labels.float().unsqueeze(1).to(device)
```
- `inputs`: (32, 3, 224, 224) 이미지 배치
- `labels`: (32,) 정수 라벨 (0=cat, 1=dog)
- `.float()`: BCEWithLogitsLoss는 float 타입의 타겟을 기대
- `.unsqueeze(1)`: (32,) → (32, 1) — 모델 출력 shape과 맞춤

```python
        if is_train:
            optimizer.zero_grad()
```
- 이전 배치의 그래디언트 초기화 (안 하면 그래디언트가 누적됨)

```python
        with torch.set_grad_enabled(is_train):
            outputs = model(inputs)
            loss = criterion(outputs, labels_bce)
```
- `set_grad_enabled(True)`: 그래디언트 계산 활성화 (학습 시)
- `set_grad_enabled(False)`: 비활성화 (평가 시 — 메모리/속도 절약)
- `criterion`: BCEWithLogitsLoss — 내부에서 sigmoid + BCE 계산

```python
            if is_train:
                loss.backward()    # 역전파: 각 파라미터의 그래디언트 계산
                optimizer.step()   # 그래디언트를 이용해 파라미터 업데이트
```

```python
        running_loss += loss.item() * inputs.size(0)
```
- `loss.item()`: 배치 평균 loss를 Python float으로 변환
- `* inputs.size(0)`: 배치 크기를 곱해서 전체 합으로 환산 (나중에 total로 나눔)

### train_model

```python
def train_model(model, train_loader, val_loader, criterion, optimizer, epochs):
    best_state = deepcopy(model.state_dict())
    best_val_acc = 0.0
```
- 초기 가중치를 deepcopy로 저장
- 학습 중 가장 좋은 val_acc를 기록하는 가중치를 추적

```python
    history = {
        'train_loss': [], 'train_acc': [],
        'val_loss': [], 'val_acc': []
    }
```
- 에폭별 학습/검증 결과를 기록하는 딕셔너리 (나중에 그래프용)

```python
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_state = deepcopy(model.state_dict())
```
- val_acc가 역대 최고이면 그 시점의 가중치를 저장 (Early Stopping의 변형)
- `deepcopy`가 핵심: 없으면 학습이 계속 진행되면서 best_state도 변함

```python
    model.load_state_dict(best_state)
    return model, history
```
- 학습이 끝나면 가장 좋았던 시점의 가중치로 모델을 복원

### evaluate_model

```python
@torch.no_grad()
def evaluate_model(model, loader, criterion):
```
- `@torch.no_grad()`: 이 함수 전체에서 그래디언트 계산을 비활성화
- `with torch.set_grad_enabled(False)`와 같은 효과이지만 더 깔끔

### plot_confusion

```python
def plot_confusion(y_true, y_pred, class_names, title):
    cm = confusion_matrix(y_true, y_pred)
```
- `confusion_matrix`: 실제 라벨과 예측 라벨을 비교하여 2x2 행렬 생성
- `cm[0][0]`: True Negative (cat을 cat으로 맞춤)
- `cm[0][1]`: False Positive (cat을 dog으로 틀림)
- `cm[1][0]`: False Negative (dog을 cat으로 틀림)
- `cm[1][1]`: True Positive (dog을 dog으로 맞춤)

---

## 6. 기본 CNN 학습

```python
baseline_model = SimpleCNN().to(device)
```
- SimpleCNN 인스턴스 생성 후 GPU로 이동

```python
criterion = nn.BCEWithLogitsLoss()
```
- Binary Cross Entropy + Sigmoid를 합친 손실 함수
- 모델이 raw logit을 출력하면, 이 함수가 내부적으로 sigmoid를 적용한 후 BCE를 계산
- 수치적으로 `sigmoid() + BCELoss()`보다 안정적

```python
optimizer = optim.Adam(baseline_model.parameters(), lr=1e-3)
```
- Adam 옵티마이저: SGD에 모멘텀 + 적응적 학습률을 추가한 최적화 알고리즘
- `lr=1e-3` (0.001): 학습률. 한 스텝에 가중치를 얼마나 업데이트할지

```python
baseline_model, baseline_history = train_model(
    baseline_model, train_loader_base, val_loader,
    criterion, optimizer, epochs=EPOCHS_SCRATCH
)
```
- 기본 transform + SimpleCNN으로 5 에폭 학습
- 반환: 학습된 모델 + 에폭별 기록(history)

```python
baseline_metrics, y_true_base, y_pred_base = evaluate_model(
    baseline_model, test_loader, criterion
)
```
- test 세트로 최종 평가
- `y_true_base`: 실제 라벨 배열
- `y_pred_base`: 예측 라벨 배열

```python
results['Baseline CNN'] = {
    'test_loss': baseline_metrics['loss'],
    'test_accuracy': baseline_metrics['accuracy'],
    'trainable_params': count_trainable_params(baseline_model)
}
```
- 나중에 모델 간 비교를 위해 결과를 딕셔너리에 저장

---

## 7. 이미지 증강 CNN 학습

```python
aug_model = SimpleCNN().to(device)
```
- **새로운** SimpleCNN 인스턴스 — Baseline과 구조는 동일하지만 가중치가 랜덤 초기화
- 같은 모델 구조 + 다른 데이터(증강) → 성능 차이 = 순수한 증강 효과

```python
aug_model, aug_history = train_model(
    aug_model, train_loader_aug, val_loader,   # ← train_loader_aug 사용!
    criterion, optimizer, epochs=EPOCHS_SCRATCH
)
```
- `train_loader_aug`: 증강 transform이 적용된 DataLoader
- 모델 구조와 에폭은 Baseline과 동일 → 변수 하나(증강)만 다름

---

## 9. 전이학습 실험 — Feature Extraction

```python
weights = models.ResNet18_Weights.DEFAULT
transfer_model = models.resnet18(weights=weights)
```
- `ResNet18_Weights.DEFAULT`: 최신 ImageNet 사전학습 가중치
- `models.resnet18(weights=weights)`: 사전학습된 ResNet18을 가중치와 함께 로드

```python
for param in transfer_model.parameters():
    param.requires_grad = False
```
- **모든 파라미터를 freeze** — 학습 시 이 가중치들은 업데이트되지 않음
- ImageNet에서 배운 특징 추출 능력을 그대로 보존

```python
transfer_model.fc = nn.Linear(transfer_model.fc.in_features, 1)
```
- ResNet18의 마지막 분류 레이어(원래 1000 클래스용)를 **새 레이어로 교체**
- `in_features`: 이전 레이어의 출력 차원 (512)
- 출력 1개: 이진 분류 (개/고양이)
- 새로 만든 레이어는 `requires_grad=True`가 기본 → 이것만 학습됨

```python
optimizer = optim.Adam(transfer_model.fc.parameters(), lr=1e-3)
```
- **fc 파라미터만** optimizer에 전달 — 다른 레이어는 freeze 상태이므로 전달할 필요 없음
- 전체 11M 파라미터 중 513개만 학습 (512 weight + 1 bias)

---

## 10. Fine-tuning (선택 확장)

```python
finetune_model = models.resnet18(weights=weights)
for param in finetune_model.parameters():
    param.requires_grad = False
```
- Feature Extraction과 동일하게 시작: 전부 freeze

```python
for param in finetune_model.layer4.parameters():
    param.requires_grad = True
```
- **layer4만 unfreeze** — ResNet18의 가장 깊은 Conv 블록
- 깊은 층일수록 도메인 특화 특징을 학습하므로, 우리 데이터에 맞게 미세 조정

```python
finetune_model.fc = nn.Linear(finetune_model.fc.in_features, 1)
```
- fc도 새로 교체 (Feature Extraction과 동일)

```python
optimizer = optim.Adam([
    {'params': finetune_model.layer4.parameters(), 'lr': 1e-4},   # 사전학습 레이어: 낮은 lr
    {'params': finetune_model.fc.parameters(), 'lr': 1e-3}        # 새 레이어: 높은 lr
], weight_decay=1e-4)
```
- **차등 학습률**: 핵심 기법
  - layer4 (`1e-4`): 이미 좋은 가중치 → 크게 바꾸면 사전학습 지식 손상 → 10배 낮게
  - fc (`1e-3`): 새로 초기화 → 빨리 배워야 함 → 표준 학습률
- `weight_decay=1e-4`: L2 정규화 — 가중치가 너무 커지는 것을 방지

---

## 11. 성능 비교와 오분류 분석

### 비교 테이블

```python
comparison_df = pd.DataFrame(results).T
```
- `results` 딕셔너리를 DataFrame으로 변환
- `.T`: 전치(행↔열) — 모델이 행, 지표가 열이 되도록

### 오분류 샘플 수집

```python
def collect_misclassified_samples(model, dataset, class_names, max_items=9):
    model.eval()
    samples = []
    for idx in range(len(dataset)):
        image, label = dataset[idx]
```
- DataLoader가 아닌 **dataset을 직접 인덱싱** — 개별 이미지의 인덱스를 보존하기 위해

```python
        with torch.no_grad():
            logit = model(image.unsqueeze(0).to(device))
```
- `unsqueeze(0)`: (3, 224, 224) → (1, 3, 224, 224) — 배치 차원 추가 (모델은 배치 입력을 기대)

```python
            pred = int((torch.sigmoid(logit).item()) >= 0.5)
```
- sigmoid 적용 → 0.5 기준으로 이진 분류 → Python int로 변환

```python
        if pred != int(label):
            samples.append({...})
```
- 예측이 틀린 경우만 수집

---

## 12. 모델 저장과 웹 서비스 배포

### 모델 저장

```python
torch.save(best_model_obj.state_dict(), 'best_model.pt')
```
- `state_dict()`: 모델의 모든 학습된 가중치를 딕셔너리로 반환
- `.pt` 파일로 저장 — 모델 구조는 저장되지 않음 (로드 시 구조를 다시 정의해야 함)

### 저장된 모델 로드 테스트

```python
test_model = models.resnet18(weights=None)
```
- `weights=None`: 사전학습 가중치 없이 빈 ResNet18 구조만 생성

```python
test_model.fc = nn.Linear(test_model.fc.in_features, 1)
```
- 학습 시와 동일하게 fc 레이어를 교체 — **구조가 같아야 state_dict 로드 가능**

```python
test_model.load_state_dict(torch.load('best_model.pt', map_location='cpu'))
```
- 저장된 가중치를 모델에 로드
- `map_location='cpu'`: GPU에서 저장한 가중치를 CPU에서도 로드 가능하게

```python
test_model.eval()
```
- 평가 모드로 전환 (Dropout 비활성화)

### Streamlit 앱 코드

```python
@st.cache_resource
def load_model():
```
- Streamlit의 리소스 캐싱 — 앱이 재실행되어도 모델을 **한 번만** 로드
- 없으면 이미지 업로드할 때마다 모델을 매번 다시 로드 (~수 초 지연)

```python
    if not os.path.exists(MODEL_PATH):
        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
```
- 최초 실행 시 Google Drive에서 모델 파일 자동 다운로드
- 이후에는 로컬 파일이 있으므로 건너뜀

```python
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 1)
    model.load_state_dict(
        torch.load(MODEL_PATH, map_location='cpu', weights_only=True)
    )
```
- `weights_only=True`: 보안 옵션 — 가중치만 로드하고 임의 코드 실행 방지 (PyTorch 2.6+ 권장)

```python
    prob = torch.sigmoid(logit).item()
```
- 모델의 raw 출력(logit)을 0~1 확률로 변환
- `.item()`: 텐서 → Python float

```python
    is_dog = prob >= 0.5
    label = "🐶 Dog" if is_dog else "🐱 Cat"
    confidence = prob if is_dog else 1 - prob
```
- `prob >= 0.5`: dog 확률이 50% 이상이면 dog
- `confidence`: dog이면 prob 그대로, cat이면 `1 - prob`이 cat 확률

```python
    col1, col2 = st.columns(2)
    with col1:
        st.write("🐱 Cat")
        st.progress(1 - prob)    # cat 확률을 프로그레스 바로 표시
    with col2:
        st.write("🐶 Dog")
        st.progress(prob)        # dog 확률을 프로그레스 바로 표시
```
- 2단 컬럼 레이아웃으로 cat/dog 확률을 나란히 시각화
