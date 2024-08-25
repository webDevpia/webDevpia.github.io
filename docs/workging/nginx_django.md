---
layout: default
# title: 404
# permalink: /404
nav_exclude: true
search_exclude: true
---
# 1. Django 배포
## 1. 가상환경 설정 및 프로젝트 생성
```
# apt-get 업데이트
apt-get update

# 파이썬 설치
sudo apt-get install python3.9

# pip 설치
sudo apt install python3-pip

# pip 업그레이드
pip install --upgrade pip

# 가상환경 라이브러리 설치
sudo apt-get install python3-venv

# 작업폴더 생성
mkdir web

# 작업폴더로 이동
cd web

# 가상환경 만들기
python3 -m venv .venv

# 가상환경 활성화
source .venv/bin/activate

# django설치
pip3 install django
```
## 2. project 구성
```
#
django-admin startproject django_prj .
```

## 3. 사용 라이브러리 목록 생성
```
# django 개발환경에서 사용하는 라이브러리 목록 만들기
pip freeze > requirements.txt
# 가끔 다음과 같이 @ file 형식으로 버전이 저장되는 경우는 아래와 같이 해결
pip list --format=freeze > requirements.txt
```
## 4. Dockerfile 생성
- Dockerfile 작성
```
# Dockerfile 작성

FROM python:3.9.16-slim-buster

# 프로젝트의 작업 폴더를 /usr/src/app로 지정
WORKDIR /usr/src/app

# 파이썬은 소스 코드를 컴파일해서 확장자가 .pyc인 파일을 생성합니다. 도커를 이용할때는 .pyc파일이 필요하지 않으므로 파일을 생성하지 않도록 합니다.

ENV PYTHONDONTWRITEBYTECODE 1

# 파이썬 로그가 버퍼링 없이 즉각적으로 출력되게 합니다.

ENV PYTHONBUFFERED 1

# 호스트 pc의 현재폴더의 모든 파일을 /usr/src/app/로 복사합니다.

COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

```
## 5. docker-compose 생성
- docker-compose.yml 작성
```
version: '3'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./:/usr/src/app/
    ports:
      - '8000:8000'
#    env_file:
#      - ./.env.dev
```
## 6. Django에 settings.py 에서 설정값 수정
```
# 외부에서 접속할 수 있도록 가상서버 ip 등을 등록해 준다.
ALLOWED_HOSTS = ['192.168.65.101','127.0.0.1','localhost']
```
## 7. docker-compose 빌드
```
sudo apt-get install docker-compose

# 도커컴포즈로 이미지 만들기
docker-compose build

# 도커컴포즈로 컨테이너 데몬으로 올리기
docker-compose up -d

# 도커컴포즈로 컴포즈 파일을 지정해서 데몬으로 컨테이너 올릴수도 있다.
docker-compose -f docker-compose-local.yml up -d

# 생성된 이미지 확인
docker images

# 생성된 컨테이너 확인
docker ps -a

# 도커컴포즈로 올린 컨테이너 중 web 에 manage.py test를 실행함
docker-compose exec web python manage.py test

# 도커컴포즈로 올린 컨테이너 내리기
docker-compose down

# 컨테이너 목록 확인
docker ps -a
```
## 8. Django에 settings.py 에서 설정값 분리
- docker-compose file 수정
```
# docker-compose file 수정
version: '3'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./:/usr/src/app/
    ports:
      - '8000:8000'
    env_file:
      - ./.env.dev
```
- settings.py 수정
```
DEBUG = os.environ.get('DEBUG',1)

SECRET_KEY = os.environ.get('SECRET_KEY',****************************)
if os.environ.get(DJANGO_ALLOWED_HOSTS):
    DJANGO_ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(' ')
else:
    DJANGO_ALLOWED_HOSTS = ['10.211.55.15','127.0.0.1','localhost']
```
- 작업경로에 .env.dev 파일 생성
```
DEBUG = 1
SECRET_KEY = ****************************
DJANGO_ALLOWED_HOSTS = 10.211.55.15 localhost 127.0.0.1 [::1]
```

# 2. Gunicorn과 Nginx 연동
- docker-compose.yml file 수정
```
version: '3'

services:
  web:
    build: .
    #command: python manage.py runserver 0.0.0.0:8000
    command: gunicorn django_prj.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ./:/usr/src/app/
    ports:
      - '8000:8000'
    env_file:
      - ./.env.dev
```

- pip로 Gunicorn을 설치한 후 requirements.txt를 업데이트하고, 도커 이미지에 반영
```
pip install gunicorn
pip freeze > requirements.txt
# 빌드해서 up 함
docker-compose up --build
docker-compose down
```