---
title: 1. PyTorch 기본 사용법
layout: default
parent: DeepLearning
nav_order: 1
permalink: /deeplearning/PyTorch
# nav_exclude: true
# search_exclude: true
---

# 1. PyTorch 기본 사용법

이 자료의 목표는 `PyTorch 문법 암기`가 아니라 `딥러닝 코드 흐름 이해`입니다.

## 학습 목표

- 텐서의 `shape`, `dtype`, `device`를 읽을 수 있다.
- `nn.Module`로 만든 모델이 어떻게 동작하는지 이해한다.
- `DataLoader -> Model -> Loss -> backward -> step` 흐름을 읽을 수 있다.
- `model.train()`, `model.eval()`, `torch.no_grad()`의 차이를 이해한다.


> 딥러닝 코드는 결국 텐서가 흐르는 파이썬 프로그램이다.

<a id="toc"></a>

## 진행 순서

1. [환경 확인](#part1)
2. [텐서 기초](#part2)
3. [모델은 함수다](#part3)
4. [DataLoader와 batch](#part4)
5. [가장 작은 학습 루프](#part5)
6. [평가와 추론](#part6)
7. [배운 내용 정리](#part7)

---

<a id="part1"></a>

## 1. 환경 확인 [↑](#toc)

### 실습에서 확인할 것
- 코드 셀을 실행할 수 있는가?
- Python 실행 환경이 열렸는가?
- PyTorch를 불러올 수 있는가?
- GPU 연결 여부를 확인할 수 있는가?


```mermaid
flowchart LR
    S1[Step 1 Hello 출력] --> S2[Step 2 Python 버전 확인]
    S2 --> S3[Step 3 PyTorch 확인]
    S3 --> S4[Step 4 GPU 여부 확인]
    S4 --> S5[Step 5 한 번에 환경 점검]

    classDef step fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#111827
    classDef finish fill:#ECFCCB,stroke:#65A30D,stroke-width:2px,color:#1F2937
    class S1,S2,S3,S4 step
    class S5 finish
```

### 1. 첫 코드 실행

가장 먼저, "코드 셀을 실행할 수 있다"는 성공 경험을 만드는 것이 중요합니다.
아래 셀을 실행해 보세요.


```python
print("Hello, Deep Learning!")
```

**실행 결과:**

```
Hello, Deep Learning!
```

### 2. Python 실행 환경 확인

딥러닝 실습은 결국 Python 환경에서 이루어집니다. 현재 어떤 버전의 Python이 실행되고 있는지 확인해 보겠습니다.


```python
import sys

print("Python 버전 확인")
print(sys.version)
```

**실행 결과:**

```
Python 버전 확인
3.12.12 (main, Oct 10 2025, 08:52:57) [GCC 11.4.0]
```

### 3. PyTorch 설치 여부 확인

딥러닝 실습에서 가장 자주 사용하는 라이브러리 중 하나가 **PyTorch**입니다. Colab에는 대체로 기본 설치되어 있습니다.

아래에는 같은 개념을 바로 실행할 수 있는 완성 예시 코드를 제공합니다.


```python
import torch
print(f"PyTorch 버전: {torch.__version__}")
```

**실행 결과:**

```
PyTorch 버전: 2.10.0+cpu
```

### 4. GPU 연결 여부 확인

이 실습은 CPU만으로도 충분하지만, Colab의 중요한 장점 중 하나는 **브라우저에서 GPU를 사용할 수 있다**는 점입니다.

#### GPU 켜는 방법

**방법 1) 메뉴에서 설정하기**

`런타임` > `런타임 유형 변경` > `T4 GPU` 선택 > `저장`

---

```python
import torch

if torch.cuda.is_available():
    print(f'GPU 사용 가능: True')
    print(f'현재 GPU 이름: {torch.cuda.get_device_name(0)}')
else:
    print('현재는 CPU 모드입니다.')
```

**실행 결과:**

```
현재는 CPU 모드입니다.
```

---

<a id="part2"></a>

## 2. 텐서 기초 [↑](#toc)

텐서는 딥러닝에서 숫자를 담는 기본 상자입니다.  
초심자에게 가장 중요한 습관은 `값`보다 먼저 `shape`를 보는 것입니다.

### 코드 읽기 질문

- 이 텐서는 몇 행 몇 열인가?
- 데이터 타입은 무엇인가?
- CPU에 있는가, GPU에 있는가?

```python
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
zeros = torch.zeros((2, 3))

print("x =")
print(x)
print("shape:", x.shape)
print("dtype:", x.dtype)
print("device:", x.device)
print()
print("zeros =")
print(zeros)
print("shape:", zeros.shape)
```

포인트:

- `torch.tensor(...)`로 텐서를 만든다.
- `shape`는 행과 열의 구조를 보여 준다.
- `dtype`는 데이터 타입이다.
- `device`는 CPU인지 GPU인지 알려 준다.

### 실습 미션 1

- 1차원 데이터를 2행 3열로 바꾸고 있는지 확인해 보세요.
- `dtype=torch.float32`를 지우면 어떤 타입이 되는지도 확인해 보세요.

```python
practice = torch.tensor([1, 2, 3, 4, 5, 6], dtype=torch.float32).reshape(2, 3)

print(practice)
print("shape:", practice.shape)
print("dtype:", practice.dtype)
```

### 텐서에서 꼭 더 알아야 하는 것 1: 차원과 인덱싱

초심자가 텐서를 읽을 때는 아래 순서가 가장 안전합니다.

1. `shape`를 본다.
2. `ndim`을 본다.
3. 한 칸을 꺼내면 무엇이 나오는지 본다.

딥러닝에서는 `0차원=숫자 하나`, `1차원=벡터`, `2차원=표`, `3차원 이상=여러 축을 가진 데이터` 정도로 이해해도 충분합니다.

```python
scalar = torch.tensor(3.14)
vector = torch.tensor([10, 20, 30])
matrix = torch.tensor([[1, 2, 3], [4, 5, 6]])
tensor_3d = torch.tensor([
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]],
])

print("scalar:", scalar, "| shape:", scalar.shape, "| ndim:", scalar.ndim)
print("vector:", vector, "| shape:", vector.shape, "| ndim:", vector.ndim)
print("matrix:\n", matrix)
print("shape:", matrix.shape, "| ndim:", matrix.ndim)
print()
print("tensor_3d:\n", tensor_3d)
print("shape:", tensor_3d.shape, "| ndim:", tensor_3d.ndim)
print()
print("matrix[0] ->", matrix[0])
print("matrix[0, 1] ->", matrix[0, 1])
print("matrix[:, 1] ->", matrix[:, 1])
```

> 3D 텐서는 `표가 여러 장 쌓인 구조`입니다. 딥러닝에서는 `(배치, 시퀀스 길이, 임베딩 차원)` 같은 3D 이상의 텐서가 자주 등장합니다.

### 텐서에서 꼭 더 알아야 하는 것 2: 모양 바꾸기

딥러닝 코드에서는 텐서 값을 바꾸는 것보다 `모양을 바꾸는 코드`가 더 자주 등장합니다.

- `reshape` : 모양 다시 만들기
- `unsqueeze` : 차원 하나 추가하기
- `squeeze` : 크기가 1인 차원 제거하기

특히 `batch 차원`을 맞추기 위해 `unsqueeze(0)`가 자주 나옵니다.

```python
a = torch.tensor([1.0, 2.0, 3.0, 4.0])

print("원본 a:", a)
print("shape:", a.shape)
print()

reshaped = a.reshape(2, 2)
print("reshape(2, 2):\n", reshaped)
print("shape:", reshaped.shape)
print()

with_batch = a.unsqueeze(0)
print("unsqueeze(0):", with_batch)
print("shape:", with_batch.shape)
print()

back_to_1d = with_batch.squeeze(0)
print("squeeze(0):", back_to_1d)
print("shape:", back_to_1d.shape)
```

### 텐서에서 꼭 더 알아야 하는 것 3: dtype와 device

입문자가 가장 자주 만나는 오류는 사실 모델 구조보다 `dtype`과 `device`에서 나옵니다.

- 입력값은 보통 `float32`
- 분류 정답 라벨은 보통 정수형 `int64` (`torch.long`)
- CPU 텐서와 GPU 텐서를 섞어 쓰면 오류가 난다

즉, 텐서를 보면 `shape` 다음으로 `dtype`, `device`를 확인하는 습관이 중요합니다.

```python
features = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
labels = torch.tensor([0, 1], dtype=torch.long)

print("features dtype:", features.dtype)
print("labels dtype:", labels.dtype)
print()

features_on_device = features.to(device)
labels_on_device = labels.to(device)

print("features device:", features_on_device.device)
print("labels device:", labels_on_device.device)
```

### 텐서에서 꼭 더 알아야 하는 것 4: 브로드캐스팅 감각

PyTorch는 모양이 조금 다른 텐서끼리도 규칙에 맞으면 자동으로 계산해 줍니다. 이것을 `브로드캐스팅`이라고 합니다.

입문 단계에서는 규칙을 외우기보다, `작은 텐서가 큰 텐서 크기에 맞춰 늘어난 것처럼 계산된다` 정도로 이해해도 충분합니다.

```python
scores = torch.tensor([[80.0, 90.0, 100.0], [70.0, 85.0, 95.0]])
bonus = torch.tensor([5.0, 5.0, 5.0])

print("scores shape:", scores.shape)
print("bonus shape:", bonus.shape)
print()
print("scores + bonus =")
print(scores + bonus)
```

### 텐서 실습에서 추가하면 좋은 질문

- `shape`와 `ndim`은 어떻게 다른가?
- `matrix[0]`과 `matrix[:, 0]`은 각각 무엇을 꺼내는가?
- 왜 `unsqueeze(0)`를 하면 batch 차원이 생긴다고 말하는가?
- 입력은 왜 `float32`, 라벨은 왜 정수형을 많이 쓰는가?
- 두 텐서가 계산이 안 될 때 가장 먼저 무엇을 확인해야 하는가?

### 질문 설명

**1. `shape`와 `ndim`은 어떻게 다른가?**

- `shape`는 텐서가 각 축마다 몇 개의 값을 가지는지 보여 줍니다.
- `ndim`은 축이 몇 개인지, 즉 차원이 몇 개인지를 보여 줍니다.
- 예를 들어 `shape = (2, 3)`이면 2행 3열 구조이고, `ndim = 2`입니다.
- 즉 `shape`는 자세한 구조 정보이고, `ndim`은 차원의 개수를 요약한 값입니다.

**2. `matrix[0]`과 `matrix[:, 0]`은 각각 무엇을 꺼내는가?**

- `matrix[0]`은 0번째 행 전체를 꺼냅니다.
- `matrix[:, 0]`은 모든 행에서 0번째 열만 꺼냅니다.
- 하나는 `행 선택`, 다른 하나는 `열 선택`이라는 점이 핵심입니다.
- 이 구분이 익숙해져야 나중에 배치 텐서나 이미지 텐서도 읽기 쉬워집니다.

**3. 왜 `unsqueeze(0)`를 하면 batch 차원이 생긴다고 말하는가?**

- `unsqueeze(0)`은 맨 앞에 크기 1인 축을 추가합니다.
- 예를 들어 `(4,)`가 `(1, 4)`가 되면, 맨 앞의 `1`을 보통 `샘플 1개짜리 배치`로 해석합니다.
- 딥러닝 모델은 입력을 보통 `[batch_size, feature]` 형태로 받기 때문에, 단일 샘플도 배치처럼 맞춰 주는 경우가 많습니다.

**4. 입력은 왜 `float32`, 라벨은 왜 정수형을 많이 쓰는가?**

- 입력 데이터는 곱셈, 덧셈, 미분 계산이 반복되므로 실수형이 필요합니다.
- 그래서 보통 `float32`를 많이 씁니다.
- 반면 분류 라벨은 `0번 클래스`, `1번 클래스`처럼 번호 역할을 하므로 정수형으로 표현합니다.
- 특히 `CrossEntropyLoss`는 라벨을 클래스 인덱스로 받기 때문에 보통 `torch.long` 타입을 사용합니다.

**5. 두 텐서가 계산이 안 될 때 가장 먼저 무엇을 확인해야 하는가?**

- 가장 먼저 `shape`를 확인합니다. 모양이 안 맞아서 생기는 오류가 가장 흔합니다.
- 다음으로 `dtype`를 확인합니다. 실수형과 정수형이 섞여 문제가 날 수 있습니다.
- 마지막으로 `device`를 확인합니다. CPU 텐서와 GPU 텐서를 섞으면 오류가 납니다.
- 입문 단계에서는 `shape -> dtype -> device` 순서로 확인하는 습관이 가장 실용적입니다.

### 배치(batch) 관점으로 shape 보기

딥러닝에서는 데이터를 하나씩보다 **묶음(batch)** 으로 처리하는 경우가 많습니다.

예를 들어:

- 학생 64명의 점수 벡터가 길이 256이면 shape는 `(64, 256)`
- 문장 32개, 문장 길이 10, 임베딩 차원 128이면 shape는 `(32, 10, 128)`
- 이미지 16장, 높이 28, 너비 28이면 shape는 `(16, 28, 28)`

즉 shape는 데이터가 어떤 축으로 정리되어 있는지 알려주는 지도입니다.

```python
tabular_batch = torch.randn(64, 256)
nlp_batch = torch.randn(32, 10, 128)
vision_batch = torch.randn(16, 28, 28)

print('tabular batch shape:', tabular_batch.shape)
print('nlp batch shape    :', nlp_batch.shape)
print('vision batch shape :', vision_batch.shape)
```

강의 포인트:

- shape의 첫 번째 숫자가 보통 `배치 크기(batch_size)`이다.
- 도메인(표, 텍스트, 이미지)에 따라 shape 구조가 다르다.
- shape만 보고 "이 데이터는 어떤 형태인가"를 읽는 습관이 중요하다.

### NumPy로 감각 잡기

PyTorch를 보기 전에 NumPy 감각을 먼저 잡아두면 훨씬 쉽습니다.

핵심 체크 포인트:

- `ndim`: 몇 차원인지
- `shape`: 각 축의 길이가 얼마인지
- 인덱싱과 슬라이싱은 파이썬 리스트와 비슷하지만 더 강력함

```python
import numpy as np

t1 = np.array([0., 1., 2., 3., 4., 5., 6.])
t2 = np.array([
    [1., 2., 3.],
    [4., 5., 6.],
    [7., 8., 9.],
    [10., 11., 12.],
])

print('1D array:', t1)
print('ndim:', t1.ndim, '| shape:', t1.shape)
print('t1[0], t1[1], t1[-1] =', t1[0], t1[1], t1[-1])
print('t1[2:5] =', t1[2:5])
print('t1[:2]  =', t1[:2])
print('t1[3:]  =', t1[3:])
print()
print('2D array:\n', t2)
print('ndim:', t2.ndim, '| shape:', t2.shape)
print('두 번째 열:', t2[:, 1])
print('마지막 열 제외:', t2[:, :-1])
```

강의 포인트:

- NumPy와 PyTorch의 인덱싱/슬라이싱 문법은 거의 같다.
- `t2[:, 1]`처럼 `콤마` 기준으로 축을 구분하는 문법에 익숙해지면 PyTorch도 쉬워진다.

### dim()과 size() 보충

PyTorch 코드에서는 `shape` 외에도 `dim()`, `size()`를 자주 만납니다. 세 가지가 거의 같은 정보를 보여 주지만 쓰임새가 조금 다릅니다.

```python
t = torch.FloatTensor([0., 1., 2., 3., 4., 5., 6.])
print('1D tensor:', t)
print('dim  :', t.dim())
print('shape:', t.shape)
print('size :', t.size())
print('index:', t[0], t[1], t[-1])
print('slice:', t[2:5], t[:2], t[3:])
print()

m = torch.FloatTensor([
    [1., 2., 3.],
    [4., 5., 6.],
    [7., 8., 9.],
    [10., 11., 12.],
])
print('2D tensor:\n', m)
print('dim  :', m.dim())
print('shape:', m.shape)
print('두 번째 열:', m[:, 1])
print('마지막 열 제외:\n', m[:, :-1])
```

강의 포인트:

- `shape`는 속성이고 `size()`는 메서드이다. 결과는 같다.
- `dim()`은 축이 몇 개인지 알려 준다. `ndim`과 같다.
- 다른 사람의 코드를 읽을 때 `shape`, `size()`, `dim()` 중 아무거나 나와도 당황하지 않으면 된다.

### 행렬 곱셈과 원소별 곱셈은 다릅니다

둘은 이름이 비슷하지만 완전히 다른 연산입니다.

- `matmul` 또는 `@` : 선형대수의 행렬 곱
- `mul` 또는 `*` : 같은 위치의 원소끼리 곱하는 연산

딥러닝 모델에서는 둘 다 자주 등장하므로 구분이 매우 중요합니다.

```python
m1 = torch.FloatTensor([[1, 2], [3, 4]])
m2 = torch.FloatTensor([[1], [2]])
m3 = torch.FloatTensor([[1, 2], [3, 4]])

print('matrix multiplication:')
print(m1.matmul(m2))
print('shape:', m1.matmul(m2).shape)
print()

print('element-wise multiplication:')
print(m1 * m3)
print('shape:', (m1 * m3).shape)
```

강의 포인트:

- `matmul`은 shape가 바뀐다. `(2, 2) @ (2, 1) → (2, 1)`.
- `*`는 shape가 그대로다. `(2, 2) * (2, 2) → (2, 2)`.
- `nn.Linear` 내부에서 일어나는 연산이 바로 행렬 곱셈이다.

### 평균, 합계, 최대값 읽기

집계 연산에서는 `dim`이 특히 중요합니다.

- `dim=0`은 첫 번째 축을 줄인다.
- `dim=1`은 두 번째 축을 줄인다.
- 축을 줄인다는 말은, 그 축 방향으로 계산해서 없앤다는 뜻입니다.

처음에는 헷갈리기 쉬우니 실제 결과 shape까지 같이 보세요.

```python
t = torch.FloatTensor([[1, 2], [3, 4]])

print('t =\n', t)
print('mean()      =', t.mean())
print('mean(dim=0) =', t.mean(dim=0))
print('mean(dim=1) =', t.mean(dim=1))
print()
print('sum()       =', t.sum())
print('sum(dim=0)  =', t.sum(dim=0))
print('sum(dim=1)  =', t.sum(dim=1))
print()
print('max()       =', t.max())
max_values, argmax_indices = t.max(dim=0)
print('max(dim=0) values =', max_values)
print('max(dim=0) index  =', argmax_indices)
```

강의 포인트:

- `dim`을 지정하지 않으면 전체 원소에 대해 계산한다.
- `dim=0`이면 행 방향(위→아래)으로 줄인다. 결과는 열 개수만큼 남는다.
- `dim=1`이면 열 방향(왼→오)으로 줄인다. 결과는 행 개수만큼 남는다.
- `max(dim=)`은 값과 인덱스를 함께 반환한다. 분류에서 `argmax`로 예측 클래스를 뽑을 때 사용한다.

### 타입 캐스팅과 텐서 연결하기

실무에서는 데이터 타입과 shape를 같이 맞춰야 하는 경우가 많습니다.

- 정수 라벨은 보통 `long`
- 실수 입력은 보통 `float`
- 여러 텐서를 합칠 때는 `cat`, 새 축을 만들어 쌓을 때는 `stack`

```python
lt = torch.LongTensor([1, 2, 3, 4])
bt = torch.ByteTensor([True, False, False, True])

print('lt dtype       :', lt.dtype)
print('lt.float()     :', lt.float(), lt.float().dtype)
print('bt dtype       :', bt.dtype)
print('bt.long()      :', bt.long(), bt.long().dtype)
print('bt.float()     :', bt.float(), bt.float().dtype)
print()

x = torch.FloatTensor([[1, 2], [3, 4]])
y = torch.FloatTensor([[5, 6], [7, 8]])

print('cat dim=0 ->\n', torch.cat([x, y], dim=0))
print('cat dim=1 ->\n', torch.cat([x, y], dim=1))
print()

v1 = torch.FloatTensor([1, 4])
v2 = torch.FloatTensor([2, 5])
v3 = torch.FloatTensor([3, 6])

print('stack default ->\n', torch.stack([v1, v2, v3]))
print('stack dim=1   ->\n', torch.stack([v1, v2, v3], dim=1))
```

강의 포인트:

- `.float()`, `.long()` 등으로 타입을 바꿀 수 있다.
- `cat`은 기존 축을 따라 이어 붙인다. `dim=0`이면 행 방향으로 늘어난다.
- `stack`은 새 축을 만들어서 쌓는다. `cat`과 달리 차원이 하나 늘어난다.

### ones_like, zeros_like, in-place 연산

`ones_like`, `zeros_like`는 **shape를 그대로 따라가면서 값만 채우는** 함수입니다.

in-place 연산은 이름 끝에 `_`가 붙는 경우가 많습니다. 예를 들어 `mul_()`는 원래 텐서를 직접 바꿉니다.

편리하지만, 학습 그래프나 디버깅에서 헷갈릴 수 있으니 의미를 분명히 알고 쓰는 것이 좋습니다.

```python
base = torch.FloatTensor([[0, 1, 2], [2, 1, 0]])
print('base =\n', base)
print('ones_like =\n', torch.ones_like(base))
print('zeros_like =\n', torch.zeros_like(base))
print()

x = torch.FloatTensor([[1, 2], [3, 4]])
print('x.mul(2.) ->\n', x.mul(2.))
print('원본 x ->\n', x)
print()
print('x.mul_(2.) ->\n', x.mul_(2.))
print('덮어쓴 뒤 x ->\n', x)
```

강의 포인트:

- `ones_like(t)`은 `t`와 같은 shape이면서 값이 모두 1인 텐서를 만든다.
- `mul(2.)`은 원본을 바꾸지 않고, `mul_(2.)`은 원본을 직접 바꾼다.
- 이름 끝에 `_`가 붙으면 in-place 연산이라는 PyTorch 관례를 기억하면 된다.

### 미니 실습: 배치 텐서 shape 읽기

아래 예제는 자연어 처리에서 자주 보는 3D 텐서 상황을 단순화한 것입니다.

가정:

- 문장 수: 2개
- 문장 길이: 3개 토큰
- 각 토큰 벡터 차원: 4

이런 데이터는 shape가 `(batch_size, length, dim)` 형태가 됩니다.

```python
mini_batch = torch.tensor([
    [[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8], [0.9, 1.0, 1.1, 1.2]],
    [[1.3, 1.4, 1.5, 1.6], [1.7, 1.8, 1.9, 2.0], [2.1, 2.2, 2.3, 2.4]],
], dtype=torch.float32)

print('shape:', mini_batch.shape)
print('첫 번째 문장 shape:', mini_batch[0].shape)
print('첫 번째 문장의 두 번째 토큰:', mini_batch[0, 1])
print('모든 문장의 첫 번째 토큰들 shape:', mini_batch[:, 0, :].shape)
print(mini_batch[:, 0, :])
```

강의 포인트:

- `mini_batch[0]`은 첫 번째 문장 전체를 꺼낸다.
- `mini_batch[0, 1]`은 첫 번째 문장의 두 번째 토큰 벡터를 꺼낸다.
- `mini_batch[:, 0, :]`은 모든 문장에서 첫 번째 토큰만 모아서 꺼낸다.
- 이런 인덱싱에 익숙해지면 LSTM, Transformer 코드에서 텐서 흐름을 읽기가 훨씬 쉬워진다.

---

<a id="part3"></a>

## 3. 모델은 함수다 [↑](#toc)

PyTorch에서는 보통 모델을 `nn.Module`을 상속받는 클래스로 만듭니다.

- `__init__` : 모델의 부품을 정의하는 곳
- `forward` : 입력 데이터가 실제로 지나가는 길

핵심은 `model(sample)`을 호출하면 내부적으로 `forward(sample)`이 실행된다는 점입니다.

```python
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(2, 4)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(4, 2)

    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        return x

model = SimpleNet().to(device)

sample = torch.tensor([[1.0, 2.0]], device=device)
output = model(sample)

print(model)
print()
print("output =")
print(output)
print("output shape:", output.shape)
```

강의 포인트:

- `__init__`은 모델 부품을 정의하는 곳이다.
- `forward`는 입력이 실제로 지나가는 경로다.
- `model(sample)`을 호출하면 내부적으로 `forward`가 실행된다.
- 출력 shape를 보며 `입력 1개 -> 클래스 점수 2개` 구조를 설명할 수 있다.

---

<a id="part4"></a>

## 4. DataLoader와 batch [↑](#toc)

실제 딥러닝에서는 데이터를 한 번에 모두 넣지 않고, `batch`라는 작은 묶음으로 나눠서 넣습니다.

- `Dataset` : 원본 데이터를 담는 곳
- `DataLoader` : 배치로 나눠서 꺼내 주는 도구

이 패턴은 실무 코드에서도 매우 자주 등장합니다.

```python
X = torch.tensor([
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
])

y = torch.tensor([0, 1, 1, 1])

dataset = TensorDataset(X, y)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

for batch_x, batch_y in dataloader:
    print("batch_x =")
    print(batch_x)
    print("batch_x shape:", batch_x.shape)
    print("batch_y =", batch_y)
    print("batch_y shape:", batch_y.shape)
    print("-" * 30)
```

강의 포인트:

- `TensorDataset`은 입력과 정답을 하나의 데이터셋처럼 묶는다.
- `DataLoader`는 데이터를 한 번에 조금씩 꺼내 준다.
- `batch_size=2`이면 한 번에 2개씩 가져온다.
- 실제 딥러닝 코드에서 `for batch_x, batch_y in dataloader:` 패턴이 매우 자주 나온다.

---

<a id="part5"></a>

## 5. 가장 작은 학습 루프 [↑](#toc)

이제 딥러닝 코드에서 가장 중요한 흐름을 봅니다.

```python
pred = model(batch_x)
loss = loss_fn(pred, batch_y)
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

이 다섯 줄이 보이면, 아래처럼 읽으면 됩니다.

- 모델이 예측한다.
- 틀린 정도를 계산한다.
- 이전 기울기를 비운다.
- 오차를 뒤로 전파한다.
- 가중치를 수정한다.

```python
model = SimpleNet().to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

for epoch in range(30):
    model.train()
    total_loss = 0.0

    for batch_x, batch_y in dataloader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        pred = model(batch_x)
        loss = loss_fn(pred, batch_y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    if (epoch + 1) % 5 == 0:
        print(f"epoch={epoch + 1:02d}, loss={total_loss:.4f}")
```

강의 포인트:

- `pred = model(batch_x)`는 예측이다.
- `loss = loss_fn(pred, batch_y)`는 틀린 정도를 계산한다.
- `optimizer.zero_grad()`는 이전 기울기를 비운다.
- `loss.backward()`는 오차를 뒤로 전파한다.
- `optimizer.step()`은 가중치를 수정한다.

### 실습 미션 2

- `batch_size=2`를 `4`로 바꾸면 어떤 차이가 있나요?
- `lr=0.1`을 `0.01`로 바꾸면 loss가 어떻게 달라지나요?
- `nn.Linear(2, 4)`를 `nn.Linear(2, 8)`로 바꾸면 어떤 점이 달라지나요?
- `ReLU`를 지우면 성능이 어떻게 변하나요?

---

<a id="part6"></a>

## 6. 평가와 추론 [↑](#toc)

학습과 예측은 목적이 다릅니다.

- `model.train()` : 학습 모드
- `model.eval()` : 평가 모드
- `torch.no_grad()` : gradient 계산 비활성화

추론에서는 보통 `model.eval()`과 `torch.no_grad()`를 함께 사용합니다.

```python
model.eval()

correct = 0
total = 0

with torch.no_grad():
    for batch_x, batch_y in dataloader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        logits = model(batch_x)
        predicted = torch.argmax(logits, dim=1)

        correct += (predicted == batch_y).sum().item()
        total += batch_y.size(0)

print(f"training set accuracy: {correct / total:.2f}")

test_input = torch.tensor([[1.0, 0.0]], device=device)

with torch.no_grad():
    logits = model(test_input)
    predicted_class = torch.argmax(logits, dim=1)

print("test input:", test_input)
print("logits:", logits)
print("predicted class:", predicted_class.item())
```

강의 포인트:

- `model.eval()`은 평가 모드 전환이다.
- `torch.no_grad()`는 gradient 계산을 끈다.
- 추론에서는 보통 둘을 함께 쓴다.
- `argmax`는 가장 큰 점수의 클래스를 고른다.

---

<a id="part7"></a>

## 7. 배운 내용 정리 [↑](#toc)

### 꼭 기억할 것

- 텐서를 보면 먼저 `shape`를 확인한다.
- 모델은 입력을 출력으로 바꾸는 함수다.
- 학습 루프 핵심 3단계는 `zero_grad -> backward -> step`이다.
- 추론에서는 `model.eval()`과 `torch.no_grad()`를 함께 자주 사용한다.

### 말로 설명해 보기

- `pred = model(batch_x)`는 무슨 뜻인가?
- `loss.backward()`는 왜 필요한가?
- `DataLoader`는 왜 쓰는가?
- `train()`과 `eval()`은 어떻게 다른가?

### 공식 문서 읽기

- PyTorch Learn the Basics: https://docs.pytorch.org/tutorials/beginner/basics/index.html
- `torch.tensor`: https://docs.pytorch.org/docs/stable/generated/torch.tensor.html
- `torch.nn.Module`: https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html
- `torch.utils.data`: https://docs.pytorch.org/docs/stable/data.html
- `torch.no_grad`: https://docs.pytorch.org/docs/stable/generated/torch.no_grad.html


→ **다음 장**: [2. 신경망 기초 - 퍼셉트론에서 MLP까지](/deeplearning/neural-network-basic)
