---
title: PLANT
layout: default
parent: AI
nav_order: 3
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

두 가지의 모델을 구축한 후 성능 평가
CNN 기본 구조를 이용한 베이스 라인 모델
미리 학습된 모델을 이용한 전이학습(Transfer Learning)

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

