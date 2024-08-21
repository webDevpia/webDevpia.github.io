---
title: AWS
layout: default
parent: Cloud
nav_order: 2
permalink: /cloud/AWS
nav_exclude: true
search_exclude: true
---

# AWS EC2 인스턴스 생성 및 SSH로 접속
- Amazon Elastic Compute Cloud(Amazon EC2)
## 1. AWS 가입하기
- aws 무료 계정 생성 
![대시보드](/assets/img/aws/aws_ec2_img001.png)

- AWS 계정 새로 만들기
![대시보드](/assets/img/aws/aws_ec2_img005.png)

- 이메일, 계정 이름 입력하고 이메일 주소확인 클릭
![대시보드](/assets/img/aws/aws_ec2_img002.png)
- 해당 메일로 코드 확인
![대시보드](/assets/img/aws/aws_ec2_img003.png)

- 비밀번호 입력
![대시보드](/assets/img/aws/aws_ec2_img004.png)

- 지역정보 입력
![대시보드](/assets/img/aws/aws_ec2_img004-1.png)

## 2. MFA 설정
![mfa](/assets/img/aws/aws_ec2_mfa_img001.png)

## 3. AWS EC2 인스턴스 생성하기

### 1. 현지화 및 기본 지역 설정
- 계정이름 선택 - 설정 - 현지화 및 기본지역의 편집을 클릭하고 수정

### 2. EC2 콘솔 대시보드에 접속하기
- 서비스(Services) - Compute(컴퓨팅) - EC2
![대시보드](/assets/img/aws/aws_ec2_img009.png)

### 3. EC2 콘솔 대시보드에서 인스턴스 시작
- 인스턴스 시작 버튼을 클릭
![대시보드](/assets/img/aws/aws_ec2_img010.png)

### 4. 이름 및 태그(Name and tags)입력
- 인스턴스의 이름을 입력
![대시보드](/assets/img/aws/aws_ec2_img011.png)

### 5. os image 및 amazon machine image
- 호스트 운영체제를 선택
![대시보드](/assets/img/aws/aws_ec2_img012.png)


### 6. 인스턴스 유형 및 키 페어 생성
- 인스턴스 유형을 선택
- 키페이 이름 입력, RSA, .pem 을 선택
![대시보드](/assets/img/aws/aws_ec2_img013.png)

### 7. 네트워크 설정 및 스토리지 구성
- 새로운 보안그룹 생성
- 인바운드 규칙설정(ssh,tcp,22)
- 스토리지 구성은 30기가 까지 프리티어
![대시보드](/assets/img/aws/aws_ec2_img014.png)

- 인스턴스 시작 버튼 클릭해서 생성

### 8. ssh 연결

#### 1. 터미널에서 연결

```
# 키페어가 있는 경로에서 실행
chmod 400 키페어.pem
ssh -i 키페어.pem user_계정@host_ip
```
#### 2. mobaxterm 에서 연결
[프로그램 다운로드](https://mobaxterm.mobatek.net/download.html)  

Session 클릭
![](/assets/img/aws/mobaxterm_001.png)

SSH클릭
![](/assets/img/aws/mobaxterm_002.png)

Remote host, Specify username, Use private key 항목 입력 후 OK 버튼 클릭
![](/assets/img/aws/mobaxterm_004.png)

Sesstion 목록에서 더블 클릭해서 접속
![](/assets/img/aws/mobaxterm_005.png)

![](/assets/img/aws/mobaxterm_006.png)


### 9. docker 설치

[ubuntu에 docker 설치](https://docs.docker.com/engine/install/ubuntu/)

#### 1. set up Docker's apt repository
```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
#### 2. Install the Docker packages.
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
#### 3. 설치확인
```bash
sudo docker run hello-world
```

#### 4. docker 그룹에 사용자 계정 등록하기

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

### 10. 인스턴스 삭제
- 삭제할 인스턴스 선택 후, 인스턴스 종료를 실행
- 종료 후 일정시간 이후 삭제 처리된다.
![대시보드](/assets/img/aws/aws_ec2_img015.png)