---
title: PLANT
layout: default
parent: AI
nav_order: 1
permalink: /ai/plant
# nav_exclude: true
# search_exclude: true
---
# 작물 잎 사진으로 질병 분류
이미지 분류 모델을 활용하여 작물 잎 사진의 종류와 질병 유무를 분류하는 프로젝트.     
프로젝트에서 사용하는 총 데이터의 수는 약 40,000개  
각 클래스의 이름은 작물의 종류와 질병 종류를 나타냄.   
질병 이름이 ‘healthy’인 경우는 해당 작물이 건강함을 의미.   
예를 들어, Potato의 경우 세 가지 클래스 Potato_Early_ blight, Potato_Late_blight, Potato_healthy  
이 중에서 Potato_healthy로 분류된 경우가 질병이 없는 Potato를 의미.  

#### 분류 클래스와 각 클래스별 데이터수, 데이터 예시
![](/assets/img/plant/plant001.png)

> 두 가지의 모델을 구축한 후 성능 평가
> CNN 기본 구조를 이용한 베이스 라인 모델
> 미리 학습된 모델을 이용한 전이학습(Transfer Learning)

## 1. 데이터 준비

#### 학습 데이터 이해
학습에 사용할 데이터는 각 이미지의 분류 클래스가 폴더로 구분되어 있는 형태로 각 폴더 안에는 Train, Validation, Test 데이터가 구별되지 않은 상태로 저장되어 있음.
![](/assets/img/plant/plant002.png)

#### 데이터 분리
Train, Validation, Test 데이터로 나누고 각각의 클래스에 해당하는 폴더에 저장
![](/assets/img/plant/plant003.png)

```py
import gdown
import zipfile
import os
import shutil

def download_and_unzip_from_google_drive(file_id, output_dir, output_zip_name="downloaded.zip"):
    # 다운로드할 경로
    zip_file_path = os.path.join(output_dir, output_zip_name)

    # Google Drive 파일 다운로드
    gdown.download(f"https://drive.google.com/uc?id={file_id}", zip_file_path, quiet=False)

    # ZIP 파일 압축 해제
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
        print(f"파일이 {output_dir}에 성공적으로 압축 해제되었습니다.")

    # ZIP 파일 삭제 (원한다면)
    os.remove(zip_file_path)
    print(f"ZIP 파일이 삭제되었습니다: {zip_file_path}")

def create_or_replace_directory(directory_path):
    # 디렉토리가 존재하는지 확인
    if os.path.exists(directory_path):
        # 디렉토리가 존재하면 삭제
        shutil.rmtree(directory_path)
        print(f"기존 디렉토리가 삭제되었습니다: {directory_path}")

    # 새로운 디렉토리 생성
    os.makedirs(directory_path)
    print(f"새로운 디렉토리가 생성되었습니다: {directory_path}")

# 사용 예시
file_id = "1uBY-JbXcPd-tikzFJcbwSR9_zEjYHHor"  # Google 드라이브 파일 ID
output_dir = "dataset"  # 압축을 풀 디렉토리 경로
create_or_replace_directory(output_dir)
download_and_unzip_from_google_drive(file_id, output_dir)
```

```py
original_dataset_dir = './dataset'
classes_list = os.listdir(original_dataset_dir)

base_dir = './splitted'
create_or_replace_directory(base_dir)

train_dir = os.path.join(base_dir, 'train')
os.mkdir(train_dir)
validation_dir = os.path.join(base_dir, 'val')
os.mkdir(validation_dir)
test_dir = os.path.join(base_dir, 'test')
os.mkdir(test_dir)

for cls in classes_list:
    os.mkdir(os.path.join(train_dir, cls))
    os.mkdir(os.path.join(validation_dir, cls))
    os.mkdir(os.path.join(test_dir, cls))
```

![](/assets/img/plant/plant004.png)

#### 데이터 분할과 클래스별 데이터 수 확인

```py
import math

for cls in classes_list:
    path = os.path.join(original_dataset_dir, cls)
    fnames = os.listdir(path)

    train_size = math.floor(len(fnames) * 0.6)
    validation_size = math.floor(len(fnames) * 0.2)
    test_size = math.floor(len(fnames) * 0.2)

    train_fnames = fnames[:train_size]
    print("Train size(",cls,"): ", len(train_fnames))
    for fname in train_fnames:
        src = os.path.join(path, fname)
        dst = os.path.join(os.path.join(train_dir, cls), fname)
        shutil.copyfile(src, dst)

    validation_fnames = fnames[train_size:(validation_size + train_size)]
    print("Validation size(",cls,"): ", len(validation_fnames))
    for fname in validation_fnames:
        src = os.path.join(path, fname)
        dst = os.path.join(os.path.join(validation_dir, cls), fname)
        shutil.copyfile(src, dst)

    test_fnames = fnames[(train_size+validation_size):(validation_size + train_size +test_size)]

    print("Test size(",cls,"): ", len(test_fnames))
    for fname in test_fnames:
        src = os.path.join(path, fname)
        dst = os.path.join(os.path.join(test_dir, cls), fname)
        shutil.copyfile(src, dst)
```

## 2. 베이스라인 모델 학습

#### 운영체제별 디바이스 확인

```py
def get_device():
    import platform
    # 운영체제 확인
    os_name = platform.system()

    if os_name == "Darwin":  # MacOS
        # MPS (Metal Performance Shaders) 지원 확인
        if torch.backends.mps.is_available():
            print("Using MPS (Metal Performance Shaders) on Mac")
            return torch.device("mps")
        else:
            print("MPS not available, using CPU on Mac")
            return torch.device("cpu")

    elif os_name == "Linux" or os_name == "Windows":
        # CUDA 지원 확인
        if torch.cuda.is_available():
            print(f"Using CUDA on {os_name}")
            return torch.device("cuda")
        else:
            print(f"CUDA not available, using CPU on {os_name}")
            return torch.device("cpu")

    else:
        # 기타 운영체제에서는 기본적으로 CPU 사용
        print(f"Unsupported OS: {os_name}, using CPU by default")
        return torch.device("cpu")

# 장치 자동 선택
# device = get_device()
```

#### 베이스라인 모델 학습을 위한 준비

```py
import torch
import os

USE_CUDA = torch.cuda.is_available()
# DEVICE = torch.device("cuda" if USE_CUDA else "cpu")
DEVICE = torch.device(get_device())
BATCH_SIZE = 256
EPOCH = 30
```

```py
import shutil
import os
from torchvision import datasets, transforms

# .ipynb_checkpoints 디렉토리 삭제 함수
def remove_ipynb_checkpoints(directory):
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name == ".ipynb_checkpoints":
                shutil.rmtree(os.path.join(root, dir_name))
                print(f"Removed: {os.path.join(root, dir_name)}")

# .ipynb_checkpoints 디렉토리 삭제
remove_ipynb_checkpoints('./splitted/train')
remove_ipynb_checkpoints('./splitted/val')

# 전처리 및 데이터 로드
transform_base = transforms.Compose([transforms.Resize((64,64)), transforms.ToTensor()])
train_dataset = datasets.ImageFolder(root='./splitted/train', transform=transform_base)
val_dataset = datasets.ImageFolder(root='./splitted/val', transform=transform_base)
```

```py
from torch.utils.data import DataLoader

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
```

#### 베이스라인 모델 설계하기

```py
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class Net(nn.Module):

    def __init__(self):

        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2,2)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 64, 3, padding=1)

        self.fc1 = nn.Linear(4096, 512)
        self.fc2 = nn.Linear(512, 33)

    def forward(self, x):

        x = self.conv1(x)
        x = F.relu(x)
        x = self.pool(x)
        x = F.dropout(x, p=0.25, training=self.training)

        x = self.conv2(x)
        x = F.relu(x)
        x = self.pool(x)
        x = F.dropout(x, p=0.25, training=self.training)

        x = self.conv3(x)
        x = F.relu(x)
        x = self.pool(x)
        x = F.dropout(x, p=0.25, training=self.training)

        x = x.view(-1, 4096)
        x = self.fc1(x)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.fc2(x)

        return F.log_softmax(x, dim=1)

model_base = Net().to(DEVICE)
optimizer = optim.Adam(model_base.parameters(), lr=0.001)
```

#### 모델 학습을 위한 함수

```py
def train(model, train_loader, optimizer):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(DEVICE), target.to(DEVICE)
        optimizer.zero_grad()
        output = model(data)
        loss = F.cross_entropy(output, target)
        loss.backward()
        optimizer.step()
```

#### 모델 평가를 위한 함수

```py
def evaluate(model, test_loader):
    model.eval()
    test_loss = 0
    correct = 0

    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(DEVICE), target.to(DEVICE)
            output = model(data)

            test_loss += F.cross_entropy(output,target, reduction='sum').item()


            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    test_accuracy = 100. * correct / len(test_loader.dataset)
    return test_loss, test_accuracy
```

#### 모델 학습을 실행하기

```py
import time
import copy

def train_baseline(model ,train_loader, val_loader, optimizer, num_epochs = 30):
    best_acc = 0.0
    best_model_wts = copy.deepcopy(model.state_dict())

    for epoch in range(1, num_epochs + 1):
        since = time.time()
        train(model, train_loader, optimizer)
        train_loss, train_acc = evaluate(model, train_loader)
        val_loss, val_acc = evaluate(model, val_loader)

        if val_acc > best_acc:
            best_acc = val_acc
            best_model_wts = copy.deepcopy(model.state_dict())

        time_elapsed = time.time() - since
        print('-------------- epoch {} ----------------'.format(epoch))
        print('train Loss: {:.4f}, Accuracy: {:.2f}%'.format(train_loss, train_acc))
        print('val Loss: {:.4f}, Accuracy: {:.2f}%'.format(val_loss, val_acc))
        print('Completed in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    model.load_state_dict(best_model_wts)
    return model


base = train_baseline(model_base, train_loader, val_loader, optimizer, EPOCH)  	 #(16)
torch.save(base,'baseline.pt')
```

## 3. Transfer Learning 모델 학습

#### Transfer Learning을 위한 준비
```py
data_transforms = {
    'train': transforms.Compose([transforms.Resize([64,64]),
        transforms.RandomHorizontalFlip(), transforms.RandomVerticalFlip(),
        transforms.RandomCrop(52), transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]) ]),

    'val': transforms.Compose([transforms.Resize([64,64]),
        transforms.RandomCrop(52), transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]) ])
}
```

```py
data_dir = './splitted'
image_datasets = {x: datasets.ImageFolder(root=os.path.join(data_dir, x), transform=data_transforms[x]) for x in ['train', 'val']}
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=BATCH_SIZE, shuffle=True, num_workers=4) for x in ['train', 'val']}
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}

class_names = image_datasets['train'].classes
```

#### Pre-Trained Model 불러오기

```py
from torchvision import models

resnet = models.resnet50(pretrained=True)
num_ftrs = resnet.fc.in_features
resnet.fc = nn.Linear(num_ftrs, 33)
resnet = resnet.to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer_ft = optim.Adam(filter(lambda p: p.requires_grad, resnet.parameters()), lr=0.001)

from torch.optim import lr_scheduler
exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)
```

#### Pre-Trained Model의 일부 Layer Freeze하기
```py
ct = 0
for child in resnet.children():
    ct += 1
    if ct < 6:
        for param in child.parameters():
            param.requires_grad = False
```

#### Transfer Learning 모델 학습과 검증을 위한 함수
```py
def train_resnet(model, criterion, optimizer, scheduler, num_epochs=25):

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print('-------------- epoch {} ----------------'.format(epoch+1))
        since = time.time()
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0


            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(DEVICE)
                labels = labels.to(DEVICE)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
            if phase == 'train':
                scheduler.step()

            epoch_loss = running_loss/dataset_sizes[phase]
            # epoch_acc = running_corrects.double()/dataset_sizes[phase]
            epoch_acc = running_corrects.float() / dataset_sizes[phase]  # .double() 대신 .float()로 수정

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))


            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

        time_elapsed = time.time() - since
        print('Completed in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    model.load_state_dict(best_model_wts)

    return model
```

#### 모델 학습을 실행하기
```py
model_resnet50 = train_resnet(resnet, criterion, optimizer_ft, exp_lr_scheduler, num_epochs=EPOCH)

torch.save(model_resnet50, 'resnet50.pt')
```

##  4. 모델 평가

#### 베이스라인 모델 평가를 위한 전처리하기

```py
transform_base = transforms.Compose([transforms.Resize([64,64]),transforms.ToTensor()])
test_base = datasets.ImageFolder(root='./splitted/test',transform=transform_base)
test_loader_base = torch.utils.data.DataLoader(test_base, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
```
#### Transfer Learning모델 평가를 위한 전처리하기

```py
transform_resNet = transforms.Compose([
        transforms.Resize([64,64]),
        transforms.RandomCrop(52),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

test_resNet = datasets.ImageFolder(root='./splitted/test', transform=transform_resNet)
test_loader_resNet = torch.utils.data.DataLoader(test_resNet, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
```

#### 베이스라인 모델 성능 평가하기
```py
baseline=torch.load('baseline.pt', weights_only=False)
baseline.eval()
test_loss, test_accuracy = evaluate(baseline, test_loader_base)

print('baseline test acc:  ', test_accuracy)
```

#### Transfer Learning 모델 성능 평가하기

```py
resnet50=torch.load('resnet50.pt', weights_only=False)
resnet50.eval()
test_loss, test_accuracy = evaluate(resnet50, test_loader_resNet)

print('ResNet test acc:  ', test_accuracy)
```
