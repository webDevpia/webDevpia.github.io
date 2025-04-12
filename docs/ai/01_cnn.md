---
title: CNN
layout: default
parent: AI
nav_order: 1
permalink: /ai/cnn
# nav_exclude: true
# search_exclude: true
---
# CNN(Convolutional Neural Network)

## 1. Linear Layer 기반의 Image Classification 시 문제점
![](/assets/img/cnn/cnn001.png)

## 2. Feature Extraction 기반의 Image 분류 매커니즘
![](/assets/img/cnn/cnn002.png)

## 3. Deep Learning CNN 구조
![](/assets/img/cnn/cnn003.webp)

## 4. CNN Layer 별 Feature 학습
![](/assets/img/cnn/cnn004.png)

## 5. 이미지 필터
![](/assets/img/cnn/cnn005.png)

## 6. Convolution Layer Filter(kernel)
필터는 전체 너비를 파싱할 때까지 특정 보폭 값으로 오른쪽으로 이동. 계속해서 전체 이미지가 탐색될 때까지 이 과정을 반복.  
Kernel Size(크기)라고 하면 면적(가로x세로)을 의미하며 가로와 세로는 서로 다를 수 있지만 보통은 일치.(3*3,5*5,7*7). 
Deep Learning CNN은 Filter값을 사용자가 만들거나 선택할 필요 없음.  
Deep Learning Network 구성을 통해 이미지 분류 등의 목적에 부합하는 최적의 filter값을 학습을 통해 스스로 최적화 함. 
![](/assets/img/cnn/cnn006.gif)

## 7. 다중 채널 일때 Convolution Layer 
여러 채널(예: RGB)이 있는 이미지의 경우 커널은 입력 이미지의 깊이와 동일한 깊이임.  
Kn과 In 스택([K1, I1]; [K2, I2]; [K3, I3]) 사이에서 행렬 곱셈이 수행되고 모든 결과를 바이어스와 합산하여 한 개의 깊이 채널로 압축된 복잡한 특징 출력을 얻는다.
![](/assets/img/cnn/cnn007.webp)
![](/assets/img/cnn/cnn008.gif)
![](/assets/img/cnn/cnn008.png)

## 8. Stride
stride는 입력 데이터(원본 image또는 입력 feature map)에 Conv Filter를 적용할 때 Sliding Window가 이동하는 간격을 의미  
기본은 1이지만, 2를(2 pixel 단위로 Sliding window 이동) 적용하여 입력 feature map 대비 출력 feature map의 크기를 대략 절반으로 줄임.  
stride를 키우면 공간적인 feature 특성을 손실할 가능성이 높아지지만, 이것이 중요 feature들의 손실을 반드시 의미하지는 않음.  
오히려 불필요한 특성을 제거하는 효과를 가져 올 수 있음.  
또한 Convolution 연산 속도를 향상 시킴. 

Stride = 1
![](/assets/img/cnn/cnn010.gif)

Stride = 2
![](/assets/img/cnn/cnn009.gif)  

## 9.padding
Filter를 적용하여 Conv 연산 수행 시 출력 Feature Map이 입력 Feature Map 대비 계속적으로 작아지는 것을 막기 위해 적용
![](/assets/img/cnn/cnn011.png)  

## 10. Pooling
Conv 적용된 Feature map의 일정 영역 별로 하나의 값을 추출하여(주로 Max 또는 Average 적용) Feature map의 사이즈를 줄임(sub sampling).  
일반적으로 Pooling 크기와 Stride를 동일하게 부여하여 모든 값이 한번만 처리 될 수 있도록 함.   
일정 영역에서 가장 큰 값 또는 평균 값을 추출하므로 위치의 변화에 따른 feature 값의 변화를 일정 수준 중화 시킬 수 있음.   
보통은 Conv->ReLU activation 들을 연속 적용 후 Feature Map에 Pooling 적용. 
![](/assets/img/cnn/cnn012.png)  

## 11. Dropout
Fully Connected Layer의 너무 촘촘한 연결로 인한 많은 파라미터(weight) 생성은 오히려 오버 피팅을 가져 올 수 있음.   
Dropout을 통해 Layer간 연결을 줄일 수 있으며 오버 피팅 개선을 가져 올 수 있음. 
![](/assets/img/cnn/cnn013.png)  

## 12. conv 연산 적용 후 출력 피처맵의 크기(size) 구하기 
![](/assets/img/cnn/cnn014.png) 

### Stride가 1이고, padding이 없는 경우
![](/assets/img/cnn/cnn015.png)  

### Stride가 1이고, padding이 1인 경우
![](/assets/img/cnn/cnn016.png)  

### Stride가 2이고, padding이 없는 경우
![](/assets/img/cnn/cnn017.png)  

### Stride가 1이고, padding이 1인 경우
![](/assets/img/cnn/cnn018.png)   