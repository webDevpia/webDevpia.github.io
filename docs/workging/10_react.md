---
layout: default
# title: 404
# permalink: /404
nav_exclude: true
search_exclude: true
---
# react 환경 구축
## 1. vscode에 확장팩 설치
- Remote Development (vscdoe extension)
- docker (vscdoe extension)
## 2. SSH 관리 파일 수정 
- Ctrl+Shift+P(명령어 팔레트)
- remote-ssh:open ssh configuration file... 선택
- 내 PC의 config 파일을 선택합니다. (C:\Users\사용자명\.ssh\config)
```
Host [계정명]@[IP 주소]:[포트번호]
    HostName [IP 주소]
    User [계정명]
    Port [포트 번호]
    
Host test@192.168.0.1:22
    HostName 192.168.0.1
    Port 22
    User test
```
## 3. ssh 접속
- 명령어 팔레트에서 Remote-SSH: Connect to Host... 을 찾아서
- 등록한 host선택
- 원격 host의 os 선택하고 비밀번호 입력

## 4. SSH 접속 완료 확인

## 5. 컨테이너내의 폴더에 접근하기 (Docker)

- 오류시
https://24hours-beginner.tistory.com/415

### 1. docker 실행
```
docker run -it -d -p 3000:3000 --name npm-test -v ~/npm-docker:/npm-docker node:lts
docker exec -it npm-test /bin/bash
yarn create react-app frontend
cd frontend
yarn start
```
# django 설정
## 1. 로컬 컴퓨터에서 작업(windows 환경)
### 1. 가상환경 만들기
```
# 가상환경만들기
conda create -n djangotest python=3.9 

# 가상환경 목록 보기
conda env list

# 가상환경 활성화
conda activate djangotest

# 가상환경 비활성화
# conda deactivate

# 가상환경내에서 설치 목록 확인
pip list

# django설치
pip install django

# CORS란? (Crosss-Origin Resource Sharing) 웹 페이지 상의 제한된 리소스를 최초 자원이 서비스된 도메인 밖의 다른 도메인으로부터 요청할 수 있게 허용.
pip install django-cors-headers

# 설치후 확인
pip list

```

### 2. 프로젝트 생성
```
django-admin startproject <프로젝트명> <프로젝트 생성 경로>

# 장고 프로젝트 생성
django-admin startproject django_prj .  

# 장고 앱 생성
python manage.py startapp testapp

# 장고 프로젝트 시작
python manage.py runserver

# 데이터베이스 생성
# python manage.py makemigrations
python manage.py migrate

# 관리자계정 생성
python manage.py createsuperuser
```
### 2. 프로젝트 실행
```
# 실행해서 http://127.0.0.1/admin으로 접속 테스트
python manage.py runserver
```
### 3. requiremnets.txt 생성
```
# requiremnets.txt 생성
pip list --format=freeze > requirements.txt
```
### 4. settings.py에 INSTALLED_APPS = [], ALLOWED_HOSTS=[]에 내용추가 및 CORS 설정
```
INSTALLED_APPS = [
    # 내용추가
    'tempApp',  # APP 이름
    'corsheaders'  # CORS 추가
]

ALLOWED_HOSTS = ['192.168.56.102', 'localhost','127.0.0.1']

# MIDDLEWARE 앞부분에 추가
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS 추가
    'django.middleware.common.CommonMiddleware',  # CORS 추가
]

# CORS 추가
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8000', 'http://localhost:3000')
CORS_ALLOW_CREDENTIALS = True
```


### 5. github에 올리기
```
# git 리파지토리 생성하고 github에 올리기
# .gitignore에 필요없는 파일 등록

git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/shimseonjo1/djangotest.git
git push -u origin main
```
## 2. host 컴퓨터에서 작업(리눅스 환경)
- 폴더를 생성하고 Dockerfile을 생성한다.
```
mkdir djangotest
cd djangotest
vi Dockerfile # 아래 내용 작성하고 저장
```
```
# Dockerfile 
FROM python:3.9.16-slim-buster

WORKDIR /usr/src/app

# .pyc 파일 생성하지 않음
ENV PYTHONDONTWRITEBYTECODE 1

# 파이썬 로그가 버퍼링 없이 즉각 출력하도록 설정
ENV PYTHONBUFFERED 1

RUN apt update  && apt install -y git

# git clone
RUN git clone https://github.com/shimseonjo1/djangotest.git .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# 설치가 되지않는 패키지는 뛰어넘고, 설치가능한 패키지만 모두 설치하기
# cat requirements.txt | xargs -n 1 pip install
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000
```

```
# Dockerfile로 이미지 빌드
docker build --tag django . --no-cache

# docker 컨테이너 생성
docker run -d -p 8000:8000 --name djangotest django

# 연결테스트
curl http://127.0.0.1:8000/

# bash셀을 실행해서 확인
docker exec -it djangotest bash
```

### docker-compose로 실행
- git에 기본 파일 있을 때
```
#Dockerfile_react
FROM node

WORKDIR /app


# RUN yarn create react-app frontend
# WORKDIR /app/frontend

RUN apt update && apt install -y git
# git clone
RUN git clone https://github.com/shimseonjo1/reacttest.git .

# EXPOSE 3000

CMD [ "yarn" ,"start" ]
```
```
#Dockerfile_django
FROM python:3.9.16-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt update && apt install -y git

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# git clone
RUN git clone https://github.com/shimseonjo1/djangotest.git .
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000
```
```
#docker-compose.yml
version: "3"

# services는 컨테이너
services:
  react-app:
    # -it 옵션을 위해 사용됨 (표준입출력)
    stdin_open: true
    tty: true

    # 현재 경로에 이미지 빌드
    build:
      context: .
      dockerfile: Dockerfile_react
    
    # 포트 포워딩
    ports:
      - "3000:3000"
    
    # 호스트 디렉토리에 바인드 마운트
    # yarn create react-app frontend
    volumes:
     - ./app:/app

    # 환경 변수 설정 - opt.1(하드코딩)
    #environment:
    #  - REACT_APP_NAME=wonkook
    #  - REACT_APP_TITLE=kiwi
    # 환경 변수 설정 - opt.2(.env)
    #env_file:
    #  - ./.env
```

```
docker-compose build --no-cache
docker-compose up -d
#docker-compose up --build -d

docker-compose logs
docker-compose exec react-app bash

docker-compose down
```
```
# 컨테이너->로컬
docker cp 컨테이너이름:컨테이너안데이터경로 로컬경로
# 로컬->컨테이너
docker cp 로컬경로 컨테이너이름:컨테이너안데이터경로 
```