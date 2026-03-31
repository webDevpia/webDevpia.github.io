---
title: 9-2. YOLO26 비전 태스크
layout: default
parent: DeepLearning
nav_order: 9.5
permalink: /deeplearning/yolo26-vision-tasks
nav_exclude: true
search_exclude: true
---
# 9-2. Detection을 넘어서 — YOLO26의 5가지 비전 태스크

## 학습 목표

1. YOLO26이 지원하는 5가지 비전 태스크의 차이를 설명할 수 있다
2. Detection의 한계를 이해하고, Segmentation이 필요한 상황을 판단할 수 있다
3. Pose Estimation으로 사람의 관절 좌표를 추출하고 활용할 수 있다
4. OBB(회전 경계 상자)가 필요한 도메인을 이해할 수 있다
5. Classification이 다른 태스크와 어떻게 다른지 이해할 수 있다
6. 문제 상황에 맞는 적절한 비전 태스크를 선택할 수 있다

> **선수 지식**: 이 수업은 [9. 객체 탐지와 YOLO](/deeplearning/objectdetection) 수업을 완료한 것을 전제합니다. Detection, Bounding Box, 신뢰도(confidence), NMS의 개념을 알고 있어야 합니다.
>
> **사용 모델**: 이전 수업에서는 YOLO11(`yolo11n.pt`)을 사용했습니다. 이 수업에서는 최신 모델인 **YOLO26**(`yolo26n.pt`)을 사용합니다. 코드 구조는 완전히 동일하며, 모델 파일명만 다릅니다. YOLO26은 YOLO11 대비 CPU에서 약 30% 빠르고, NMS 후처리가 불필요한 end-to-end 구조입니다.

<a id="toc"></a>
## 진행 순서

1. [왜 Detection만으로는 부족한가?](#part1)
2. [5가지 비전 태스크 개요](#part2)
3. [실습 1: Detection vs Segmentation 비교](#part3)
4. [실습 2: Pose Estimation — AI 자세 분석](#part4)
5. [더 알아보기: OBB와 Classification](#part5)
6. [태스크 선택 가이드](#part6)
7. [통합 정리](#part7)

---

<a id="part1"></a>
## 1. 왜 Detection만으로는 부족한가? [↑](#toc)

**학습목표**: Detection의 한계를 이해하고, 다른 태스크가 필요한 상황을 판단할 수 있다

지난 시간에 YOLO로 객체를 탐지(Detection)했습니다. 그런데 다음 상황을 생각해 봅시다.

### 상황 1: 자율주행 — "보행자가 도로 어디까지 차지하고 있는가?"

Detection은 사각형 박스만 제공합니다. 하지만 자율주행에서는 보행자의 **정확한 윤곽**을 알아야 안전 거리를 계산할 수 있습니다.

```
Detection:  [────────────]     ← 박스 안에 배경도 포함
            │  🧑  빈공간  │
            [────────────]

Segmentation: 🧑 ← 사람 픽셀만 정확히 분리
```

→ **Instance Segmentation**이 필요합니다.

### 상황 2: 피트니스 앱 — "스쿼트 자세가 올바른가?"

사람이 있다는 것은 Detection으로 알 수 있지만, **무릎 각도가 90도인지, 허리가 굽었는지**는 알 수 없습니다.

→ **Pose Estimation**이 필요합니다.

### 상황 3: 위성 영상 — "활주로와 비행기의 방향"

비행기나 항구의 선박은 **기울어져** 있습니다. 수평 박스로는 객체 방향을 표현할 수 없고, 빈 공간이 너무 많이 포함됩니다.

→ **OBB(Oriented Bounding Box)**가 필요합니다.

**핵심**: Detection(사각형 박스)은 범용적이지만, 정밀한 윤곽·자세·방향이 필요한 문제에서는 다른 태스크가 더 적합하다.

> **확인**: 의료 영상에서 종양을 탐지할 때, Detection과 Segmentation 중 어떤 것이 더 적합할까요? 왜 그런가요?

---

<a id="part2"></a>
## 2. 5가지 비전 태스크 개요 [↑](#toc)

**학습목표**: YOLO26이 지원하는 5가지 비전 태스크의 차이를 설명할 수 있다

YOLO26은 하나의 프레임워크(`ultralytics`)에서 5가지 태스크를 모두 지원합니다.

### 태스크 비교

| 태스크 | 출력 | 모델 파일 | 사전학습 데이터 | 핵심 질문 |
|--------|------|----------|-----------------|-----------|
| **Detection** | 사각형 박스 + 클래스 | `yolo26n.pt` | COCO (80클래스) | "무엇이 어디에 있는가?" |
| **Segmentation** | 픽셀 마스크 + 클래스 | `yolo26n-seg.pt` | COCO (80클래스) | "객체의 정확한 윤곽은?" |
| **Classification** | 이미지 전체 클래스 | `yolo26n-cls.pt` | ImageNet (1000클래스) | "이 이미지는 무엇인가?" |
| **Pose** | 17개 관절 키포인트 | `yolo26n-pose.pt` | COCO-Keypoints | "사람의 자세는?" |
| **OBB** | 회전된 박스 + 클래스 | `yolo26n-obb.pt` | DOTA-v1 (15클래스) | "객체의 방향은?" |

> **중요**: 사전학습 모델은 위 표의 데이터셋에 포함된 클래스만 인식합니다. 예를 들어 Detection 모델은 COCO 80 클래스(사람, 자동차, 개 등)만 탐지합니다. 이 목록에 없는 객체(예: 포트홀, 특수 부품)를 탐지하려면 [이전 수업](/deeplearning/objectdetection)에서 실습한 커스텀 학습(Fine-tuning)이 필요합니다.

### 시각적 비교

```
원본 이미지: 🖼️ 도로 위의 버스

Detection:      [━━━━━━━]  "bus 0.95"        ← 사각형 박스
Segmentation:   🟦🟦🟦🟦🟦  "bus 0.95"        ← 버스 모양 그대로 색칠
Classification: "bus"                         ← 이미지 전체를 하나의 클래스로
Pose:           (사람에게만 적용)  👤 + 관절 17개  ← 뼈대 그림
OBB:            [━━━/] 45°  "bus 0.95"       ← 기울어진 박스
```

### 코드 구조는 동일 (추론 시)

**추론(예측) 시** 5가지 태스크 모두 같은 패턴으로 실행됩니다. **모델 파일만 바꾸면 됩니다.**

> **참고**: "모델 파일만 바꾸면 된다"는 **추론(예측)**에 해당합니다. 커스텀 데이터로 학습할 때는 태스크별로 데이터 형식과 라벨링 방식이 다릅니다. 학습 방법은 [이전 수업](/deeplearning/objectdetection)의 포트홀 실습을 참고하세요.

```python
from ultralytics import YOLO

# Detection
model = YOLO("yolo26n.pt")

# Segmentation — 모델 파일만 다름!
model = YOLO("yolo26n-seg.pt")

# Pose
model = YOLO("yolo26n-pose.pt")

# 추론은 모두 동일
results = model("image.jpg")
results[0].show()
```

### COCO 키포인트 맵 (Pose)

Pose 모델은 사람의 17개 관절을 아래 순서로 출력합니다.

| 인덱스 | 키포인트 | 인덱스 | 키포인트 |
|--------|---------|--------|---------|
| 0 | 코(nose) | 9 | 왼손목(left_wrist) |
| 1 | 왼눈(left_eye) | 10 | 오른손목(right_wrist) |
| 2 | 오른눈(right_eye) | 11 | 왼엉덩이(left_hip) |
| 3 | 왼귀(left_ear) | 12 | 오른엉덩이(right_hip) |
| 4 | 오른귀(right_ear) | 13 | 왼무릎(left_knee) |
| 5 | 왼어깨(left_shoulder) | 14 | 오른무릎(right_knee) |
| 6 | 오른어깨(right_shoulder) | 15 | 왼발목(left_ankle) |
| 7 | 왼팔꿈치(left_elbow) | 16 | 오른발목(right_ankle) |
| 8 | 오른팔꿈치(right_elbow) | | |

**핵심**: YOLO26은 모델 파일을 바꾸는 것만으로 Detection, Segmentation, Classification, Pose, OBB 5가지 태스크를 수행한다. 코드 구조가 동일하므로 하나만 알면 나머지도 바로 사용할 수 있다.

> **확인**: COCO 데이터셋에는 80개 클래스가 있습니다. Pose 모델은 이 중 어떤 클래스에만 적용될까요?

---

<a id="part3"></a>
## 3. 실습 1: Detection vs Segmentation 비교 [↑](#toc)

**학습목표**: 같은 이미지에 Detection과 Segmentation을 적용하여 결과 차이를 비교할 수 있다

> 이 실습은 Colab 노트북 `07b_yolo26_vision_tasks.ipynb`에서 진행합니다.

### 실습 흐름

1. **Detection 결과 시각화** — 기본 plot, 좌표 이해, 객체 크롭, 임계값 조정
2. **Segmentation 결과 시각화** — 마스크 데이터 3단계 이해, 컬러코딩 시각화
3. **결과 활용** — 면적 계산, 배경 제거, 클래스별 집계

### Detection 결과

```python
from ultralytics import YOLO

det_model = YOLO("yolo26n.pt")
results = det_model("https://ultralytics.com/images/bus.jpg")
```

출력: 사각형 박스 → `results[0].boxes`에 좌표 저장

### 바운딩 박스 좌표 이해하기

`boxes.xyxy`는 각 객체의 위치를 **(x1, y1, x2, y2)** 형태로 저장합니다.

- **(x1, y1)**: 좌상단 좌표 (빨간 점)
- **(x2, y2)**: 우하단 좌표 (파란 점)
- **width** = x2 - x1, **height** = y2 - y1

노트북에서 좌표 포인트, 바운딩 박스, 너비/높이를 직접 그려서 확인합니다.

### 탐지된 객체 크롭 & 클래스별 집계

`xyxy` 좌표로 각 객체를 잘라내고(crop), 클래스별 개수를 집계합니다.

```python
# 객체 크롭 — xyxy 좌표의 실용적 활용
x1, y1, x2, y2 = boxes[i]
crop = orig_img[y1:y2, x1:x2]  # 이미지에서 y1~y2행, x1~x2열 영역을 잘라냄

# 클래스별 집계 — 재고 관리, 교통량 분석 등에 활용
from collections import Counter
# [names[c] for c in classes]는 아래를 한 줄로 쓴 것입니다:
# class_list = []
# for c in classes:
#     class_list.append(names[c])  # 클래스 번호 → 이름 변환
class_counts = Counter([names[c] for c in classes])
```

> **참고**: 위 코드는 핵심 부분만 발췌한 것입니다. 전체 코드는 노트북에서 확인하세요.

### 신뢰도 임계값(conf)에 따른 결과 변화

`conf` 파라미터는 실무에서 가장 자주 조정하는 값입니다.

```python
results = det_model("bus.jpg", conf=0.5)   # 0.5 이상만 탐지
results = det_model("bus.jpg", conf=0.75)  # 0.75 이상만 탐지 (엄격)
```

- **conf를 높이면**: 확실한 것만 남김 (정밀도 UP, 재현율 DOWN)
- **conf를 낮추면**: 더 많이 탐지하지만 오탐 증가 (정밀도 DOWN, 재현율 UP)

> **복습**: 정밀도와 재현율은 [이전 수업](/deeplearning/objectdetection)에서 배웠습니다. 쉽게 말해, conf를 높이면 "확실한 것만 골라서 틀리는 경우는 줄지만, 놓치는 객체가 늘어남"이고, conf를 낮추면 "가능한 많이 잡아서 놓치는 건 줄지만, 잘못 탐지하는 경우가 늘어남"입니다.

노트북에서 0.25 / 0.50 / 0.75 세 가지 임계값의 결과를 나란히 비교합니다.

> **Detection 정리**: 여기까지가 Detection의 결과 구조입니다. Bounding Box 좌표로 위치를 파악하고, 크롭, 집계, 임계값 조정이 가능합니다.
>
> 이제 같은 이미지에 Segmentation을 적용하여 어떤 차이가 있는지 비교해 봅시다.

---

### Segmentation 결과

```python
seg_model = YOLO("yolo26n-seg.pt")
results = seg_model("https://ultralytics.com/images/bus.jpg")
```

출력: 픽셀 마스크 → `results[0].masks`에 마스크 저장

### 마스크 데이터 구조 단계별 이해

마스크(mask)가 실제로 어떤 데이터인지 3단계로 확인합니다.

> **용어 설명**
> - **마스크(mask)**: 이미지와 같은 크기의 데이터로, 각 픽셀이 "객체인지 아닌지"를 숫자로 표현한 것
> - **컬러맵(colormap)**: 숫자 값을 색상으로 변환하는 규칙. `hot`은 낮은 값=검정, 높은 값=빨강/노랑으로 표시
> - **이진(binary)**: 0과 1, 두 가지 값만 가지는 것. "객체다(1) / 아니다(0)"

1. **확률 마스크**: 각 픽셀이 객체일 확률 (0~1, `hot` 컬러맵으로 시각화)
2. **이진 마스크**: 0.5 기준으로 객체/배경 구분 (흰색=객체, 검정=배경)
3. **오버레이**: 원본 이미지 위에 마스크를 겹쳐서 위치 확인

> **참고**: `masks.data`의 크기는 원본 이미지와 다를 수 있습니다(예: 160×160). 원본 크기로 사용하려면 `cv2.resize()`로 복원해야 합니다. 노트북에서 이 과정을 실습합니다.

### 핵심 차이

| 항목 | Detection | Segmentation |
|------|-----------|-------------|
| 출력 형태 | `boxes.xyxy` (좌표 4개) | `masks.data` (픽셀 맵) |
| 정보량 | 위치 + 클래스 | 위치 + 클래스 + **윤곽** |
| 속도 | 빠름 | 약간 느림 |
| 용도 | 개수 세기, 위치 파악 | 면적 계산, 배경 분리, 정밀 분석 |

### 객체별 마스크 컬러코딩 시각화

각 객체를 고유한 색상으로 구분하면, 같은 클래스(예: person)라도 개별 마스크가 분리되어 있는 것을 확인할 수 있습니다. 이것이 바로 **Instance Segmentation**입니다.

### 응용: 배경 제거

Segmentation 마스크를 활용하면 배경을 제거하고 객체만 추출할 수 있습니다. 노트북에서 실습합니다.

**핵심**: Segmentation은 Detection의 사각형 박스를 넘어 객체의 정확한 윤곽을 픽셀 단위로 제공한다. 면적 계산, 배경 분리 등 정밀한 분석이 필요할 때 사용한다.

> **확인**: 주차장에서 각 차량의 면적을 계산하려면 Detection과 Segmentation 중 어떤 것을 사용해야 할까요? 왜 그런가요?

---

<a id="part4"></a>
## 4. 실습 2: Pose Estimation — AI 자세 분석 [↑](#toc)

**학습목표**: Pose Estimation으로 사람의 관절 좌표를 추출하고 각도를 계산할 수 있다

> 이 실습은 Colab 노트북 `07b_yolo26_vision_tasks.ipynb`에서 진행합니다.

### 실습 흐름

1. **이미지에서 Pose 추출** — 17개 키포인트 시각화
2. **관절별 신뢰도 분석** — 히트맵으로 어떤 관절이 잘 잡히는지 확인
3. **키포인트 좌표 활용** — 관절 각도 계산
4. **커스텀 시각화** — 뼈대(skeleton) 직접 그리기
5. **웹캠 Pose** — 실시간 자세 분석

### Pose 결과 구조

```python
pose_model = YOLO("yolo26n-pose.pt")
results = pose_model("people.jpg")

# 키포인트 접근
keypoints = results[0].keypoints  # 모든 사람의 키포인트
xy = keypoints.xy                  # (N, 17, 2) — 사람 N명, 관절 17개, x/y 좌표
conf = keypoints.conf              # (N, 17) — 각 관절의 신뢰도
```

### 관절별 탐지 신뢰도 히트맵

각 관절이 얼마나 정확하게 탐지되었는지 히트맵으로 확인합니다.

- **초록**: 신뢰도 높음 (잘 보이는 관절)
- **빨강**: 신뢰도 낮음 (가려지거나 찾기 어려운 관절)

노트북에서 (사람 수 x 17개 관절) 매트릭스를 `RdYlGn` 컬러맵으로 시각화합니다. 이를 통해 어떤 관절이 잘 잡히고, 어떤 관절이 어려운지(예: 가려진 손목, 뒤를 향한 귀) 패턴을 파악할 수 있습니다.

### 응용: 팔꿈치 각도 계산

어깨(5), 팔꿈치(7), 손목(9) 세 점으로 팔의 각도를 계산할 수 있습니다.

```python
import numpy as np

def calc_angle(a, b, c):
    """세 점(a, b, c)에서 b를 꼭짓점으로 하는 각도를 구합니다."""
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)  # 1e-6 = 0.000001, 분모가 0이 되는 것을 방지
    return np.degrees(np.arccos(np.clip(cosine, -1, 1)))

# 왼쪽 어깨(5), 왼쪽 팔꿈치(7), 왼쪽 손목(9)
# .cpu().numpy(): GPU의 텐서 데이터를 CPU의 numpy 배열로 변환
# (numpy는 GPU 데이터를 직접 다룰 수 없기 때문에 필요한 과정)
shoulder = xy[0][5].cpu().numpy()
elbow = xy[0][7].cpu().numpy()
wrist = xy[0][9].cpu().numpy()

angle = calc_angle(shoulder, elbow, wrist)
print(f"왼쪽 팔꿈치 각도: {angle:.1f}°")
```

### 실무 활용 사례

| 분야 | 활용 | 사용하는 키포인트 |
|------|------|-----------------|
| 피트니스 | 스쿼트 자세 교정 | 엉덩이(11,12) + 무릎(13,14) + 발목(15,16) |
| 재활 의학 | 관절 가동 범위 측정 | 어깨(5,6) + 팔꿈치(7,8) + 손목(9,10) |
| 스포츠 분석 | 투구 폼 분석 | 전신 17개 |
| 안전 관리 | 넘어짐 감지 | 코(0) + 엉덩이(11,12) 높이 비교 |

**핵심**: Pose Estimation은 사람의 17개 관절 좌표를 제공한다. 이 좌표로 각도 계산, 자세 판별, 동작 분석 등 다양한 응용이 가능하다.

> **확인**: 넘어짐을 감지하려면 어떤 키포인트들의 y좌표를 비교하면 될까요?

---

<a id="part5"></a>
## 5. 더 알아보기: OBB와 Classification [↑](#toc)

### OBB (Oriented Bounding Box)

일반 Detection의 박스는 항상 수평/수직입니다. 그런데 위성 영상의 비행기, 항구의 선박, 문서의 텍스트 영역은 **기울어져** 있습니다.

```
일반 Detection:              OBB:
┌─────────────┐           ╱─────────╲
│  ✈️  빈공간   │          ╱    ✈️      ╲
│     빈공간   │          ╲            ╱
└─────────────┘           ╲─────────╱
→ 빈 공간이 많음            → 객체에 딱 맞음
```

**OBB 출력**: `[x_center, y_center, width, height, angle]` — 기존 4개 좌표 + **회전 각도** 1개

> **용어 설명**: **라디안(radian)**은 각도를 나타내는 또 다른 단위입니다. 우리가 익숙한 360°(도) 대신, 한 바퀴를 약 6.28(2π)로 표현합니다. 변환: `도 = 라디안 × 180 ÷ π` (Python: `np.degrees(라디안값)`)

```python
obb_model = YOLO("yolo26n-obb.pt")
results = obb_model("aerial_image.jpg")

# 회전된 박스 접근
obb = results[0].obb
print(obb.xywhr)  # x, y, w, h, rotation(라디안)
```

**주요 활용 분야**: 위성/항공 영상 분석, 문서 텍스트 영역 탐지, 산업 부품 방향 검출

**사전학습 데이터(DOTA-v1)의 15개 클래스**: 비행기, 선박, 탱크, 야구장, 테니스코트, 농구코트, 항구, 다리, 차량, 헬리콥터, 원형교차로, 축구장, 수영장, 소형차, 대형차

### OBB 회전 방향 시각화

노트북에서 회전 각도(radian)를 화살표와 꼭짓점으로 시각화합니다.

- **초록 화살표**: 객체의 주 방향 (회전 각도를 `cos`/`sin`으로 변환)
- **노란 사각형**: OBB의 4개 꼭짓점 (`obb.xyxyxyxy` 포맷)

```python
# OBB의 두 가지 좌표 포맷
obb.xywhr    # (x중심, y중심, 너비, 높이, 회전각도) — 요약 형태
obb.xyxyxyxy # (x1,y1, x2,y2, x3,y3, x4,y4) — 4개 꼭짓점 좌표
```

일반 Detection의 수평 박스와 달리, 객체 방향에 맞춰 기울어진 박스가 생성되는 것을 시각적으로 확인합니다.

### Classification

이미지 전체를 하나의 클래스로 분류합니다. 이전 CNN 수업(`07_Dogs_vs_Cats`)에서 배운 것과 같은 태스크입니다.

```python
cls_model = YOLO("yolo26n-cls.pt")
results = cls_model("cat.jpg")

# 분류 결과
print(results[0].probs.top5)      # 상위 5개 클래스 인덱스
print(results[0].probs.top5conf)  # 상위 5개 신뢰도
```

**CNN 분류와의 차이**: YOLO-cls는 ImageNet 1000 클래스로 사전학습 되어 있어 별도 학습 없이 바로 사용 가능합니다. 커스텀 학습 시에는 CNN 수업에서 배운 전이학습과 동일한 원리로 Fine-tuning합니다.

> **확인**: Classification은 "이미지 전체"를 분류하고, Detection은 "이미지 안의 각 객체"를 탐지합니다. 편의점 CCTV에서 "진열대에 어떤 상품이 몇 개 있는지" 파악하려면 어떤 태스크가 더 적합할까요?

---

<a id="part6"></a>
## 6. 태스크 선택 가이드 [↑](#toc)

### 의사결정 플로우

```
이미지가 들어왔다!
    │
    ├─ "이 이미지가 뭔지만 알면 된다" → Classification
    │
    ├─ "어디에 뭐가 있는지 알아야 한다"
    │       │
    │       ├─ "위치만 알면 된다" → Detection
    │       │
    │       ├─ "정확한 윤곽이 필요하다" → Segmentation
    │       │
    │       ├─ "객체가 기울어져 있다" → OBB
    │       │
    │       └─ "사람의 자세를 알아야 한다" → Pose
    │
    └─ "객체의 면적/비율을 계산해야 한다" → Segmentation
```

### 실전 시나리오 퀴즈

| 시나리오 | 정답 태스크 | 이유 |
|---------|-----------|------|
| 마트 재고 관리 — 진열대 제품 개수 세기 | Detection | 위치와 개수만 필요 |
| 의료 — CT 영상에서 종양 크기 측정 | Segmentation | 정확한 면적 필요 |
| 스포츠 — 선수 부상 방지 모니터링 | Pose | 관절 각도 분석 |
| 드론 — 주차장 차량 방향 분석 | OBB | 차량이 다양한 각도로 주차 |
| 품질 검사 — 불량품/양품 구분 | Classification | 전체 이미지 분류 |

---

<a id="part7"></a>
## 7. 통합 정리 [↑](#toc)

### 5가지 태스크 최종 비교

| | Detection | Segmentation | Classification | Pose | OBB |
|---|---|---|---|---|---|
| **출력** | 박스 | 마스크 | 클래스 | 키포인트 | 회전 박스 |
| **대상** | 모든 객체 | 모든 객체 | 이미지 전체 | 사람만 | 기울어진 객체 |
| **정보** | 위치+클래스 | 윤곽+클래스 | 클래스 | 관절 좌표 | 위치+방향 |
| **속도** | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★☆ | ★★★★☆ |
| **난이도** | ★★☆☆☆ | ★★★☆☆ | ★☆☆☆☆ | ★★★☆☆ | ★★★★☆ |

### YOLO26 모델 크기별 성능 참고

| 모델 | mAP 50-95 | CPU 속도(ms) | 파라미터 | 권장 환경 |
|------|:---------:|:----------:|:-------:|----------|
| yolo26n (nano) | 40.9 | 38.9 | 2.4M | 모바일, 엣지, Colab 무료 |
| yolo26s (small) | 48.6 | 87.2 | 9.5M | 웹 서비스, 일반 서버 |
| yolo26m (medium) | 53.1 | 220 | 20.4M | GPU 서버 |
| yolo26l (large) | 55.0 | 286 | 24.8M | 고정확도 필요 시 |

> **nano vs small**: nano는 small보다 2.2배 빠르지만 mAP가 7.7 낮습니다. 이 실습에서는 Colab 환경에서 빠르게 실행할 수 있는 **nano(n)** 모델을 사용합니다. 서비스 배포 시에는 정확도-속도 요구사항에 따라 적절한 크기를 선택하세요.

### 복습 질문

1. Detection과 Segmentation의 출력은 어떻게 다른가?
2. Pose 모델이 출력하는 17개 키포인트 중, 스쿼트 자세를 판별하려면 어떤 키포인트를 사용해야 하는가?
3. 일반 Detection 대신 OBB를 사용해야 하는 상황은 언제인가?
4. YOLO26에서 태스크를 바꾸려면 코드의 어떤 부분만 변경하면 되는가?
5. 의료 영상에서 종양 크기를 측정하려면 어떤 태스크가 가장 적합한가? 그 이유는?

### 심화 과제

- Segmentation 마스크로 객체별 면적(픽셀 수)을 계산하고, 가장 큰 객체를 찾아보기
- Pose 키포인트로 "손을 든 사람"을 자동 감지하는 조건문 만들어 보기
- 자신의 이미지/영상으로 5가지 태스크를 모두 실행하고 결과 비교하기
- nano(n) 모델과 small(s) 모델의 속도·정확도 차이를 측정해 보기 (위 벤치마크 표와 비교)

### 참고 자료

- [Ultralytics YOLO26 공식 문서](https://docs.ultralytics.com/models/yolo26/) — YOLO26 아키텍처와 성능 벤치마크
- [Ultralytics Tasks 가이드](https://docs.ultralytics.com/tasks/) — 5가지 태스크별 공식 사용법
- [Instance Segmentation 가이드](https://docs.ultralytics.com/tasks/segment/) — 마스크 활용 심화
- [Pose Estimation 가이드](https://docs.ultralytics.com/tasks/pose/) — 키포인트 커스텀 학습 방법
- [OBB Detection 가이드](https://docs.ultralytics.com/tasks/obb/) — 회전 박스 학습 데이터 준비
- [COCO Dataset](https://cocodataset.org/) — Detection/Segmentation/Pose 사전학습 데이터셋 정보
- [DOTA Dataset](https://captain-whu.github.io/DOTA/) — OBB 사전학습 데이터셋 정보 (항공/위성 영상)
