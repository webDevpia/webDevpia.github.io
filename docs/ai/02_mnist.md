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

### 2. 모델 생성

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

학습과 평가에 사용할 MNIST 데이터를 다운로드 받아서 저장
```py
train_data = datasets.MNIST(root=root_dir+'/data',
                            train=True,
                            download = True,
                            transform=transforms.ToTensor())
test_data = datasets.MNIST(root=root_dir+'/data',
                            train=False,
                            transform=transforms.ToTensor())
```

다운로드 받은 데이터 건수 확인
```py
print(len(train_data),len(test_data))
```

다운로드 받은 데이터의 타입 확인
```py
print(type(train_data))
```

이미지와 레이블 저장 형태 확인
```py
image,label = train_data[0]
print(label.shape)
print(image.shape)
```

이미지 출력
```py
plt.imshow(image.squeeze(),cmap='gray')
```

모델에 배치 사이즈 만큼 읽어서 제공할 DataLoader 생성
```py
train_loader = torch.utils.data.DataLoader(dataset=train_data,
                                           batch_size=batch_size,
                                           shuffle = True)
test_loader = torch.utils.data.DataLoader(dataset=test_data,
                                           batch_size=batch_size,
                                           shuffle = True)
```

DataLoader 로더해서 형태 파악
```py
first_batch = train_loader.__iter__().__next__()

print(type(first_batch))
print(len(first_batch))

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
| name | type | size |
num of batch | | 1200
first_batch     | <class 'list'>            | 2
first_batch[0]  | <class 'torch.Tensor'>    | torch.Size([50, 1, 28, 28])
first_batch[1]  | <class 'torch.Tensor'>    | torch.Size([50])

모델 정의
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

모델 생성및 옵티마이저, 오차함수 생성
```py
model = CNN().to(device)
optimizer = optim.Adam(model.parameters(),lr = learning_rate)
criterion = nn.CrossEntropyLoss()

print(model)
```

### 3. 모델 학습

생성된 모델 학습모드로 설정하고 학습 진행
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

### 4. 모델 평가 및 모델 저장

테스트 데이터로 모델 평가
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

결과값의 형태 파악
```py
print(output.shape)

print(output.max(1))
```

정확도 계산해서 출력
```py
print(100*correct/len(test_loader.dataset))
```

모델 저장
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
    image = Image.open(img_path).convert('RGB')

    # 전처리: 흑백으로 변환, 크기 조정, 텐서 변환, 정규화
    preprocess = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),  # 흑백 변환
        transforms.Resize((28, 28)),  # 크기 조정
        transforms.ToTensor(),  # 텐서로 변환
    ])

    # 이미지 반전 (검은 바탕에 흰 글씨로 만들기)
    image = TF.invert(image)

    # 전처리 적용
    image_tensor = preprocess(image).unsqueeze(0)  # 배치 차원 추가 (1, 1, 28, 28)

    return image_tensor
```

```py
import glob

# 이미지 파일 불러오기 및 전처리
img_path = root_dir+'/myimg/*.png'  # 테스트할 이미지 경로

files = glob.glob(img_path)

model = CNN()
model.load_state_dict(torch.load(root_dir+'/model/mnist_cnn.pt',map_location=torch.device('cpu')))

model.eval()

for path in files:
  image = preprocess_image(path)
  output = model(image)
  pred = torch.argmax(output,dim=1)
  print(pred)
  plt.imshow(image.squeeze(),cmap='gray')
  plt.show()
```

## 3. 웹으로 서비스 하기

model.py
```py
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from PIL import Image
from torchvision import transforms
import torchvision.transforms.functional as TF

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

    
# 이미지 전처리 (MNIST와 동일하게 처리하고 색상 반전 추가)
def preprocess_image(img_path):
    # 이미지 불러오기
    image = Image.open(img_path)

    # 전처리: 흑백으로 변환, 크기 조정, 텐서 변환, 정규화
    preprocess = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),  # 흑백 변환
        transforms.Resize((28, 28)),  # 크기 조정
        transforms.ToTensor(),  # 텐서로 변환
    ])
    
    # 이미지 반전 (검은 바탕에 흰 글씨로 만들기)
    image = TF.invert(image)

    # 전처리 적용
    image_tensor = preprocess(image).unsqueeze(0)  # 배치 차원 추가 (1, 1, 28, 28)
    
    return image_tensor

```

app.py
```py
from flask import Flask, redirect, render_template,request
import os
from PIL import Image
import model as m
import torch

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mnist',methods=['get'])
def mnist():
    return render_template('mnist_upload.html')


@app.route('/mnist',methods=['post'])
def fileupload():
    f = request.files['filename']
    img_path=os.path.dirname(__file__)+'/uploads/'+f.filename
    f.save(img_path)
    
    # 이미지 전처리 및 예측
    image_tensor = m.preprocess_image(img_path)

    # 모델 불러오기
    model = m.CNN()
    # model.load_state_dict(torch.load('/mnist_model.pth',weights_only=True))
    model.load_state_dict(torch.load('mnist_model.pth',map_location='cpu'))

    # 모델 재평가
    model.eval()
    # 예측
    with torch.no_grad():  # 기울기 계산 비활성화 (평가 모드)
        output = model(image_tensor)
        predicted = torch.argmax(output, dim=1)  # 가장 높은 확률을 가진 클래스를 예측

    # 예측 결과 출력
    print(f'Predicted class: {predicted.item()}')
    return render_template('mnist_result.html',data=predicted.item())

if __name__ == '__main__':
    app.run(debug=True,port=8088)
```
/templates/default.html
```html
<!DOCTYPE html>
<html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
        <title>
            {% raw %}
            {% block title %}{% endblock %}
            {% endraw %}
        </title>
    </head>
    <body>
    {% raw %}
        {% include 'menu.html' %} 
        {% block content %}{% endblock %}
    {% endraw %}
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js" integrity="sha384-q2kxQ16AaE6UbzuKqyBE9/u/KzioAlnx2maXQHiDX9d4/zp8Ok3f+M7DPm+Ib6IU" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.min.js" integrity="sha384-pQQkAEnwaBkjpqZ8RU1fF1AKtTcHJwFl3pblpTlHXybJjHpMYo79HY3hIi4NKxyj" crossorigin="anonymous"></script>
    </body>
</html>
```
/templates/menu.html
```html
<nav class="navbar navbar-expand-lg" style="background-color: #036dd6;">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">부경대학교 디지털 스마트 5기</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/mnist">숫자인식</a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Dropdown
          </a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">Action</a></li>
            <li><a class="dropdown-item" href="#">Another action</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">Something else here</a></li>
          </ul>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" aria-disabled="true">Disabled</a>
        </li>
      </ul>
      <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>
```

/templates/index.html
```html
{% raw %}
{% extends "default.html" %}
{% block title %}홈페이지{% endblock %}
{% block content %}
{% endraw %}
<h1>홈페이지</h1>
{% raw %}
{% endblock %}
{% endraw %}
```

/templates/mnist_upload.html
```html
{% raw %}
{% extends "default.html" %}
{% block title %}숫자 이미지 입력{% endblock %}
{% block content %}
{% endraw %}
<br>
<br>
<br>
<div class="container">
  <form action="/mnist" method="post" enctype="multipart/form-data">
    <div>
      <label for="formFileLg" class="form-label">판독할 숫자 이미지를 선택하세요</label>
      <input class="form-control form-control-lg" id="formFileLg" name="imgfile" type="file">
    </div>
    <br>
    <div class="col-auto">
      <button type="submit" class="btn btn-primary mb-3">숫자판독시작</button>
    </div>
  </form>
</div>
{% raw %}{% endblock %}{% endraw %}
```

/templates/mnist_result.html
```html
{% raw %}
{% extends "default.html" %}
{% block title %}숫자 분석 결과 페이지{% endblock %}
{% block content %}
{% endraw %}
<br>
<br>
<br>
<div class="container">
<h1>숫자 판독 결과는 {% raw %}{{data}}{% endraw %}입니다.</h1>
<img width="100" height="100"  
  src="/static/upload/{{img_path}}" alt="">
</div>
{% raw %}{% endblock %}{% endraw %}
```
