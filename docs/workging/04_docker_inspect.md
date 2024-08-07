---
layout: default
# title: 404
# permalink: /404
nav_exclude: true
search_exclude: true
---
# docker 조사하기
## docker history
- 이미지 히스토리 확인
```
# Dockerfile_history 파일명으로 다음과 같이 작성
FROM ubuntu:18.04
LABEL maintainer="seonjo@site.org"
LABEL version="1.0.0"
LABEL description="docker test"

# 패키지(프로그램) 정보 업데이트
RUN apt-get update

# apache2 패키지(프로그램) 설치, 중간에 y/n 묻는 단계가 나오면 모두 Yes로 하고 설치
RUN apt-get install -y apache2

# apache2 디폴트 웹서버 설정은 /var/www/html/ 폴더의 웹페이지를 보여줌
COPY ./webtest /var/www/html/

# apache2 웹서버 구동 명령은 다음과 같음
ENTRYPOINT ["/usr/sbin/apache2ctl","-D","FOREGROUND"]
```
```
# 이미지 생성 (각 명령이 실행되며, layer를 작성함)
$ docker build --tag myweb_history -f Dockerfile_history .

# 이미지 히스토리 확인
$ docker history myweb_history

IMAGE          CREATED          CREATED BY                                       SIZE      COMMENT
7a1ea73c5d9f   31 seconds ago   ENTRYPOINT ["/usr/sbin/apache2ctl" "-D" "FOR…   0B        buildkit.dockerfile.v0
<missing>      31 seconds ago   COPY ./webtest /var/www/html/ # buildkit         8.21MB    buildkit.dockerfile.v0
<missing>      31 seconds ago   RUN /bin/sh -c apt-get install -y apache2 # …   102MB     buildkit.dockerfile.v0
<missing>      52 seconds ago   RUN /bin/sh -c apt-get update # buildkit         45.3MB    buildkit.dockerfile.v0
<missing>      52 seconds ago   LABEL description=docker test                    0B        buildkit.dockerfile.v0
<missing>      52 seconds ago   LABEL version=1.0.0                              0B        buildkit.dockerfile.v0
<missing>      52 seconds ago   LABEL maintainer=seonjo@site.org                 0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      /bin/sh -c #(nop)  CMD ["/bin/bash"]             0B
<missing>      2 weeks ago      /bin/sh -c #(nop) ADD file:47682dd3869ca8e57…   63.2MB
<missing>      2 weeks ago      /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
<missing>      2 weeks ago      /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
<missing>      2 weeks ago      /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH      0B
<missing>      2 weeks ago      /bin/sh -c #(nop)  ARG RELEASE                   0B
```
- 위와 같이 FROM, RUN, COPY, ENTRYPOINT 등 명령에 따라 layer가 생성됨을 확인할 수 있음

## docker cp
- 컨테이너에서 특정 파일을 호스트 pc로 가져오는(꺼내오는) 명령
- 특정 파일 확인을 위해 활용
```
# 컨테이너 작성
$ docker run -dit -p 9999:80 --name httpd_history --rm myweb_history
```
```
# apache2 설정 파일 가져오기
$ docker cp httpd_history:/etc/apache2/sites-available/000-default.conf ./
```
- 반대로 호스트 pc에서 컨테이너에 특정 파일을 넣을 수도 있음
```
# 000-default.conf 파일의 다음 부분을
DocumentRoot /var/www/html

# 다음과 같이 변경 및 저장
DocumentRoot /var/www/html/xxx
```
```
# 컨테이너에 넣기
$ docker cp ./000-default.conf httpd_history:/etc/apache2/sites-available/000-default.conf

# 컨테이너 접속하기
$ docker exec -it httpd_history /bin/bash

# 컨테이너 안에서 다음 명령으로 변경된 파일이 들어갔음을 확인하기
$ cd /etc/apache2/sites-available/
$ cat 000-default.conf 

# apache2 재실행(에러가 나는 듯한 부분은 경고이며, 정상동작)
# 해당 경고를 삭제하는 설정은 ServerName localhost를 /etc/apache2/apache2.conf에 추가하면 되지만, 맥락에 맞지 않은 부분이므로 별도로 진행하지는 않기로 함
$  apache2ctl restart

# localhost:9999 접속후 Not Found 에러 확인
$ exit
```

## docker commit
- 컨테이너 변경사항을 이미지 파일로 생성
```
docker commit 옵션 컨테이너ID_또는_이름 이미지이름[:태그]
```
```
# 이미 있는 이미지 이름을 넣으면, 덮어 씌워짐(태그가 없기 때문에, latest 기준)
# 다른 이미지명을 넣으면 해당 이미지명으로 별도로 생성됨
# 보통 Dockerfile-dev, Dockerfile-prod 같은 형태로 개발용/서비스용으로 나눌때 사용하기도 함
$ docker commit -m "add vim" httpd_history myweb_history

# 이미지 history 확인 (ENTRYPOINT 상단에 layer가 추가된 것을 확인할 수 있음)
$ docker history myweb_history
```
```
$ docker exec -it httpd_history /bin/bash
$ cd /etc/apache2/sites-available/
$  vi 000-default.conf 
bash: vi: command not found

$ apt-get update
$ apt-get install vim -y
$ vi 000-default.conf 
$ exit

$ docker commit -m "add vim" httpd_history myweb_history
$ docker history myweb_history

IMAGE          CREATED             CREATED BY                                       SIZE      COMMENT
156ff1e5e29e   10 seconds ago                                                       49.6MB    add vim
7a1ea73c5d9f   About an hour ago   ENTRYPOINT ["/usr/sbin/apache2ctl" "-D" "FOR…   0B        buildkit.dockerfile.v0

# 현재 모든 컨테이너 중지 및 삭제
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

# 새로운 이미지로 컨테이너 실행
$ docker run -dit -p 9999:80 --name httpd_history --rm myweb_history
$ docker exec -it httpd_history /bin/bash
$ cd /var/log/apache2/

# localhost:9999접속 후, access.log 확인
$ cat access.log

# 종료
$ exit
```

## docker diff
- 컨테이너가 실행되면 본래의 이미지와 비교해서 변경된 파일 목록 출력

| 기호 | 설명|
| --- | --- |
| A | 파일 또는 디렉토리 추가 |
| D | 파일 또는 디렉토리 삭제 |
| C | 파일 또는 디렉토리 수정 | 

```
# myweb_history 이미지로부터 생성된 httpd_history가 실행되면서, 지금까지 변경된 내역을 보여줌
$ docker diff httpd_history
C /root
C /root/.bash_history
C /var
C /var/log
C /var/log/apache2
C /var/log/apache2/access.log
C /var/log/apache2/error.log
C /run
C /run/apache2
C /run/apache2/apache2.pid
```

## docker inspect
- 이미지와 컨테이너 세부 정보 확인

## docker logs
- 컨테이너의 출력결과(STDOUT)를 확인
