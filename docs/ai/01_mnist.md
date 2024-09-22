---
title: MNIST
layout: default
parent: AI
nav_order: 1
permalink: /ai/mnist
# nav_exclude: true
# search_exclude: true
---
# CNN을 이용한 숫자 인식 모델 만들기

## 1. 모델생성 및 학습 및 평가

### 1. 구글 드라이브와 연결

데이터 파일 및 결과 파일을 구글 드라이브에 저장하기 위해 구글 드라이브를 연결 
```py
from google.colab import drive
drive.mount('/content/drive')
```

저장할 경로를 미리 선언
```py
root_dir = '/content/drive/MyDrive/Colab Notebooks/pytorch_test/mnist'
```

필요한 라이브러리 import
```py
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from matplotlib import pyplot as plt
```

현재 gpu를 사용할 수 있는지 확인
```py
is_cuda = torch.cuda.is_available()
is_cuda
```

gpu 사용 여부에 따라 device에 값을 셋팅 
```py
device = torch.device('cuda' if is_cuda else 'cpu')
device
```

하이퍼 파라미터 값을 설정
```py
batch_size = 50
epoch_num = 15
learning_rate = 0.0001
```

학습과 평과에 사용할 MNIST 데이터를 다운로드 받아서 저장
```py
train_data = datasets.MNIST(root=root_dir+'/data',
                            train=True,
                            download = True,
                            transform=transforms.ToTensor())
test_data = datasets.MNIST(root=root_dir+'/data',
                            train=False,
                            transform=transforms.ToTensor())
```

```py
print(len(train_data),len(test_data))
```

```py
print(type(train_data))
```

```py
image,label = train_data[0]
print(label.shape)
print(image.shape)
```

```py
plt.imshow(image.squeeze(),cmap='gray')
```

```py
train_loader = torch.utils.data.DataLoader(dataset=train_data,
                                           batch_size=batch_size,
                                           shuffle = True)
test_loader = torch.utils.data.DataLoader(dataset=test_data,
                                           batch_size=batch_size,
                                           shuffle = True)
```

```py
first_batch = train_loader.__iter__().__next__()
```

```py
print(type(first_batch))
print(len(first_batch))
```

```py
print(len(first_batch))
print(first_batch[0].shape)
print(first_batch[1].shape)
```

```py
print(f"{'name':15s} | {'type':<25s} | {'size'}")
print(f"{'num of batch':15s} | {'':<25s} | {len(train_loader)}")
print(f"{'first_batch':15s} | {str(type(first_batch)):<25s} | {len(first_batch)}")
print(f"{'first_batch[0]':15s} | {str(type(first_batch[0])):<25s} | {first_batch[0].shape}")
print(f"{'first_batch[1]':15s} | {str(type(first_batch[1])):<25s} | {first_batch[1].shape}")
```
name            | type                      | size
num of batch    |                           | 1200
first_batch     | <class 'list'>            | 2
first_batch[0]  | <class 'torch.Tensor'>    | torch.Size([50, 1, 28, 28])
first_batch[1]  | <class 'torch.Tensor'>    | torch.Size([50])

```py
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout2d(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output
```

```py
model = CNN().to(device)
optimizer = optim.Adam(model.parameters(),lr = learning_rate)
criterion = nn.CrossEntropyLoss()

print(model)
```

```py
model.train()
i = 0
for epoch in range(epoch_num):
  for data, target in train_loader:
    data = data.to(device)
    target = target.to(device)
    optimizer.zero_grad()
    output = model(data)
    loss = criterion(output,target)
    loss.backward()
    optimizer.step()
    if i % 1000 == 0:
      print(f"train step:{i}\tloss:{loss.item()}")
    i += 1

```

```py
model.eval()
correct = 0
for data, target in test_loader:
  data = data.to(device)
  target = target.to(device)
  output = model(data)
  prediction = output.data.max(1)[1]
  correct += prediction.eq(target.data).sum()
```

```py
output.shape
```

```py
output.data.max(1)
```

```py
100*correct/len(test_loader.dataset)
```

```py
torch.save(model.state_dict(),root_dir+'/mnist_model.pth')
```

## 2. 생성된 모델 사용하기

```py
from PIL import Image
from torchvision import transforms
import torchvision.transforms.functional as TF

# 이미지 전처리 (MNIST와 동일하게 처리하고 색상 반전 추가)
def preprocess_image(img_path):
    # 이미지 불러오기
    image = Image.open(img_path)

    # 전처리: 흑백으로 변환, 크기 조정, 텐서 변환, 정규화
    preprocess = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),  # 흑백 변환
        transforms.Resize((28, 28)),  # 크기 조정
        transforms.ToTensor(),  # 텐서로 변환
        transforms.Normalize((0.1307,), (0.3081,))  # MNIST 데이터와 동일한 정규화
    ])

    # 이미지 반전 (검은 바탕에 흰 글씨로 만들기)
    image = TF.invert(image)

    # 전처리 적용
    image_tensor = preprocess(image).unsqueeze(0)  # 배치 차원 추가 (1, 1, 28, 28)

    return image_tensor
```
```py
# 이미지 파일 불러오기 및 전처리
img_path = root_dir+'/myimg/5.png'  # 테스트할 이미지 경로

# 이미지 전처리 및 예측
image_tensor = preprocess_image(img_path)

# 모델 불러오기
model = CNN()
model.load_state_dict(torch.load(root_dir+'/mnist_model.pth',weights_only=True))

# 모델 재평가
model.eval()
# 예측
with torch.no_grad():  # 기울기 계산 비활성화 (평가 모드)
    output = model(image_tensor)
    predicted = torch.argmax(output, dim=1)  # 가장 높은 확률을 가진 클래스를 예측

# 예측 결과 출력
print(f'Predicted class: {predicted.item()}')
```
```py
# 전처리된 텐서 출력
print(image_tensor)  # 이미지 텐서 값 출력
```
```py
# image_tensor의 차원을 출력
print(image_tensor.shape)
# 1: 배치 크기 (이미지가 1개)
# 1: 채널 수 (흑백 이미지이므로 1채널)
# 28: 이미지의 높이 (28 픽셀)
# 28: 이미지의 너비 (28 픽셀)
```
```py
import matplotlib.pyplot as plt

# 전처리된 텐서를 다시 이미지로 시각화
image_to_show = image_tensor.squeeze(0)  # 배치 차원 제거 (1, 28, 28)
image_to_show = image_to_show.squeeze(0)  # 채널 차원 제거 (28, 28)

# 시각화
plt.imshow(image_to_show, cmap='gray')  # 흑백 이미지이므로 cmap='gray' 사용
plt.title('Preprocessed Image')
plt.show()
```

## 3. 웹으로 서비스 하기
```py

```
```py

```
```py

```
```py

```
```py

```
```py

```
```py

```
```py

```
```py

```
```py

```