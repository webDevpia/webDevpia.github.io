---
layout: default
# title: 404
# permalink: /404
nav_exclude: true
search_exclude: true
---
# 컨테이너 활용과 연결

## docker로 jupyter notebook 띄우기
- 컨테이너 내부에서 jupyter notebook이 실행되는 폴더인 /home/jovyan폴더를 호스트 pc의 현재 폴더로 만들어서 호스트 pc에서 docker를 실행하는 폴더에 있는 주피터 노트북 파일 작업이 가능하도록 함
```
# 제공한 mysql_in_docker.ipynb파일이 있는 디렉토리에서 실행
docker run --rm -d -p 8888:8888 --name jupyter -v /home/ubuntu/learn:/home/jovyan/work jupyter/datascience-notebook
```
- 위와 같이 실행하면, 다음과 같은 메세지를 확인할 수 있음, 여기에서 token= 이후에 나오는 토큰값을 복사
- 브라우저에 호스트pc_ip:8888로 접속하고 토큰값 입력란에 복사해놓은 토큰값을 붙여넣기 한다.
```
docker logs jupyter

Or copy and paste one of these URLs:
        http://45b5f8e6f54c:8888/lab?token=5e9b99b5723fec629dc95b400291eac5a611bb9037d30ec3
        http://127.0.0.1:8888/lab?token=5e9b99b5723fec629dc95b400291eac5a611bb9037d30ec3
```

## 컨테이너와 컨테이너 연결하기
- docker run 옵션으로 --link 옵션을 사용하여 연결할 수 있음
- --link <본래의 컨테이너 이름>:<컨테이너를 가르킬 이름>
```
# Dockerfile_mysql 파일명으로 다음과 같이 작성
FROM mysql:5.7

# mysql 슈퍼관리자인 root ID에 대한 password란에 원하는 패스워드 설정
ENV MYSQL_ROOT_PASSWORD=password

# dbname란에 원하는 데이터베이스 이름 설정
ENV MYSQL_DATABASE=dbname

# 필요시 다음 설정도 가능

# user 란에 mysql 추가 사용자 ID 설정
# ENV MYSQL_USER=user

# pw 란에 mysql 추가 사용자 ID의 패스워드 설정
# ENV MYSQL_PASSWORD=pw
```
```
# docker 이미지 작성하기
$ docker build --tag mysqldb -f Dockerfile_mysql .

# 컨테이너 생성하기 3306 포트에 연결하고, volume 옵션 설정하기
# 맥과 윈도우는 다음과 같이 "" 따옴표로 절대 경로 작성(한글폴더 등 복잡한 경로는 정상 작동 안할 수도 있음)
$ docker run -d -p 3306:3306 --name mydb -v /home/ubuntu/mysqldata:/var/lib/mysql mysqldb
```

- --link 옵션 사용해서 주피터 노트북 컨테이너 실행하기
```
# 모든 컨테이너 삭제 후, 재실행

# -p 설정 없이 mysql 컨테이너 실행
$ docker run --rm -d --name mydb -v /home/ubuntu/mysqldata:/var/lib/mysql mysqldb

# --link 컨테이너이름:연결할컨테이너를지칭할이름
$ docker run --rm -d -p 8888:8888 -v /home/ubuntu/learn:/home/jovyan/work --link mydb:myjupyterdb jupyter/datascience-notebook
```

- mysql_in_docker.ipynb의 mysql docker 에 접속하기 
    - 기존 코드에서 
        - host 를 myjupyterdb(docker run시 --link옵션으로 설정한 컨테이너를 가르킬 이름)로 바꾸고 접속
        
> 컨테이너간 연결은 컨테이너를 가르킬 이름을 설정하고, 해당 이름과 컨테이너에서 오픈한 포트로 접속하면 됨