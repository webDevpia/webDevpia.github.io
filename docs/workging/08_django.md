---
layout: default
# title: 404
# permalink: /404
nav_exclude: true
search_exclude: true
---
# Django + Dockerfile
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

# 설치후 확인
pip list

```

### 2. 프로젝트 생성
```
django-admin startproject <프로젝트명> <프로젝트 생성 경로>

# 장고 프로젝트 생성
django-admin startproject django_prj .  

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
### 4. settings.py에 ALLOWED_HOSTS=[]에 내용추가
```
ALLOWED_HOSTS = ['192.168.56.102', 'localhost','127.0.0.1']
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
docker build --tag django .

# docker 컨테이너 생성
docker run -d -p 8000:8000 --name djangotest django

# 연결테스트
curl http://127.0.0.1:8000/

# bash셀을 실행해서 확인
docker exec -it djangotest bash
```
## 3. aws EC2
### 1. aws 가입

### 2. aws EC2 인스턴스 생성

### 3. ssh 설정
- git bash 실행
```
# 파일 모드 변경
chmod 400 aws_키페어.pem

# 키페어 이용 ssh 접속
ssh -i *.pem 계정@퍼블릭ip
```
### 4. ec2에 docker 설치
https://docs.docker.com/engine/install/ubuntu/
```
sudo apt-get update

sudo apt-get install ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo docker run hello-world

sudo usermod -aG docker $USER
```
### 5. host컴퓨터 작업
- 위와 동일

### 6. aws port 인바운드
- 인스턴스 - 보안 그룹 - 인바운드 규칙 추가
- 사용자 지정 TCP , 8000 추가

# Django + docker-compose
## 1. 로컬 컴퓨터에서 작업(windows 환경)
### 1. 가상환경 만들기
```
# 가상환경만들기
conda create -n django_compose python=3.9 

# 가상환경 목록 보기
conda env list

# 가상환경 활성화
conda activate django_compose

# 가상환경 비활성화
# conda deactivate

# 가상환경내에서 설치 목록 확인
pip list

# django설치
pip install django

# 설치후 확인
pip list

```

### 2. 프로젝트 생성
```
django-admin startproject <프로젝트명> <프로젝트 생성 경로>

# 장고 프로젝트 생성
django-admin startproject django_prj .  

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
### 4. settings.py에 ALLOWED_HOSTS=[]에 내용추가
```
ALLOWED_HOSTS = ['192.168.56.102', 'localhost','127.0.0.1']
```
### 5. github에 올리기
```
# git 리파지토리 생성하고 github에 올리기
# .gitignore에 필요없는 파일 등록

git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/shimseonjo1/django_compose.git
git push -u origin main
```
## 2. host 컴퓨터에서 작업(리눅스 환경)
### 1. docker-compose로 장고 서비스 올리기
```
mkdir djangocompose
cd djangocompose
vi Dockerfile # 아래 내용 작성하고 저장
```
```
# Dockerfile 
FROM python:3.9.16-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt update  && apt install -y git

# git clone
RUN git clone https://github.com/shimseonjo1/django_compose.git .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# 설치가 되지않는 패키지는 뛰어넘고, 설치가능한 패키지만 모두 설치하기
# cat requirements.txt | xargs -n 1 pip install
RUN python manage.py makemigrations
RUN python manage.py migrate

#CMD python manage.py runserver 0.0.0.0:8000
```
```
# docker-compose.yml
version: '3'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - 8000:8000
#env_file:
#  - ./.env.dev

```

```
# 도커 컨테이너 실행
docker-compose build --no-cache
docker-compose up -d

# 연결테스트
curl http://127.0.0.1:8000/

docker images
docker ps -a 

# bash셀을 실행해서 확인
docker-compose exec web bash

# 컨테이너 중단
docker-compose down
docker images
docker ps -a 
```
### 2. Gunicorn
- 웹서버 Nginx와 Django를 연결하기 위해 필요한 WSGI(Web Server Gateway Interface)중 하나인 Gunicorn을 설정
- 로컬 작업컴퓨터에서 gunicorn을 설치하고 requirements.txt를 다시 작성
```
pip install gunicorn
# requiremnets.txt 생성
pip list --format=freeze > requirements.txt

# github에 push
git add .
git commit -m "gunicorn 설치"
git push
```
- host 컴퓨터에서 docker-compose.yml 수정
```
# docker-compose.yml
version: '3'

services:
  web:
    build: .
    #command: python manage.py runserver 0.0.0.0:8000
    command: gunicorn django_prj.wsgi:application --bind 0.0.0.0:8000
    ports:
      - 8000:8000
#env_file:
#  - ./.env.dev
```
```
docker-compose build --no-cache
docker-compose up -d
docker-compose logs
docker-compose exec web bash
docker-compose down
```
### 3. Nginx
- static,media폴더 설정
- templates/index.html 생성
```

# settings.py 추가
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR,'_static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'_media')
```
```
# urls.py 추가
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
```

```
# docker-compose.yml
version: '3'

services:
  nginx:
    build:
      context: .
      dockerfile: Dockerfile2
    volumes:
      - static_volume:/usr/src/app/_static
      - media_volume:/usr/src/app/_media
    ports:
      - 80:80
    depends_on:
      - web
  web:
    build:
      context: .
      dockerfile: Dockerfile
    #command: python manage.py runserver 0.0.0.0:8000
    command: gunicorn django_prj.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/usr/src/app/_static
      - media_volume:/usr/src/app/_media
    expose:
      - 8000  
volumes:
  static_volume:
  media_volume:
#env_file:
#  - ./.env.dev
```
```
# Dockerfile2
FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
```
```
# nginx.conf
upstream django_prj {
  server web:8000;
}

server {
  listen 80;
  location / {
    proxy_pass http://django_prj;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $host;
    proxy_redirect off;
  }
  location /static/ {
    alias /usr/src/app/_static/;
  }
  location /media/ {
    alias /usr/src/app/_media/;
  }
}
```
```
docker-compose build --no-cache
docker-compose up -d
docker-compose logs
docker-compose exec web bash
docker-compose down
```

## 3. aws 
- 해당 port 인바운드 규칙 추가
- http, 80 추가
