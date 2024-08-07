---
layout: default
# title: 404
# permalink: /404
nav_exclude: true
search_exclude: true
---
# Dockerfile 이란?
- docker 이미지를 작성할 수 있는 기능임
- Dockerfile 문법으로 이미지 생성을 위한 스크립트를 작성할 수 있고, 이를 기반으로 이미지를 생성할 수 있다.
- 나만의 이미지를 생성할 수 있고, 배포를 위해서도 많이 할용하는 기능임

## 1. Dockerfile 기본 문법
- Dockerfile은 텍스트 파일 형식이므로, 각자 사용하는 어떤 에디터로든 작성할 수 있음
- Dockerfile 기본 문법
    - 기본적으로는 간단히 **명령**과 **인자**로 이루어짐
    - 명령은 통상적으로는 대문자로 작성함(소문자로 작성해도 문제없지만, 명령임을 구별하기 위해 일반적으로 대문자로 작성함
    ```bash
    명령 인자
    ```

### 1. Dockerfile 주요 명령
- Dockerfile 주요 명령에 대한 요약을 통해 큰 그림을 이해한 후, 각 명령에 대해 상세히 이해하기로 함.

| 명령 | 설명 |
|---|---|
| FROM | 베이스 이미지 지정 명령</br>(예:FROM httpd:alpine) |
| LABEL | 버전 정보, 작성자와 같은 이미지 설명을 작성하기 위한 명령</br>(예:LABEL version="1.0.0" |
| CMD | docker 컨테이너가 시작할 때, 실행하는 쉘 명령을 지정하는 명령, RUN과 비슷하지만 Run은 이미지 작성시 실행하는 명령이고, CMD는 컨테이너를 시작할 때 실행하는 명령임</br>(예:CMD ['python','app.py']) |
| RUN | 쉘 명령을 실행하는 명령</br>(예:RUN ['apt-get','install','nginx]), </br>RUN은 이미지 작성시 실행되며 일종의 새로운 이미지 layer 를 만드는 역활은 함 |
| ENTRYPOINT | docker 컨테이너가 시작할 때, 실행하는 쉘 명령을 지정하는 명령. docker run 커맨드 실행시, 별도 명령어도 넣을 수 있는데 이때 CMD 명령은 해당 명령으로 덮어 씌워짐. ENTRYPOINT로 지정한 명령은 docker run 커멘드 실행 시 함께 넣어진 별도 명령어가 있더라도 덮어씌워지지 않고 실행됨(구체적인 테스트는 상세 내용을 익힐 때 보기로 함) |
| EXPOSE | docker 컨테이너 외부에 오픈할 포트 섫정</br>(예:EXPOSE 8080) |
| ENV | docker 컨테이너 내부에서 사용할 환경 변수 지정</br>(예 : ENV PATH /usr/bin:$PATH) |
| WORKDIR | docker 컨테이너에서 작업 디렉토리 설정 |
| COPY | 파일 또는 디렉토리를 docker 컨테이너에 복사. ADD와 달리 URL은 지정할 수 없으며, 압축 파일을 자동으로 풀어주지 않음</br>(예:COPY test.sh /root/test.sh |

- 다음 명령도 참고로는 알아두기로 함

| 명령 | 설명 |
|---|---|
| ADD | ADD와 COPY 명령은 유사하지만, COPY 명령이 보다 명시적이므로, COPY 명령을 사용하도록 함(ADD 명령은 참고로만 알아둠) </br> 파일,디렉토리, 또는 특정 URL 의 데이터를 docker 이미지에 추가</br>(예:ADD file /var/www/html)</br>추가할 파일이 tar 압축 파일일 경우 자동으로 압축을 풀어줌(이 기능이 압축파일을 그대로 넣고 싶을 때가 문제가 되었음)</br>동일한 이름의 파일 또는 디렉토리가 이미 docker 이미지에 있을 시에는 덮어 씌우지 않음</br>(예:ADD test.sh /root/test.sh) |
| SHELL | 쉘 프로그램 지정 명령이지만, CMD 등으로 대체 가능</br>(예:SHELL ['/bin/bash','-c']) |
| ARG | dockerfile 내에서 필요한 변수 설정. docker 이미지/컨테이터에서 사용하는 환경 변수를 설정하는 ENV와 달리 dockerfile 스크립트 작성을 위해 필요한 변수를 설정</br>(예:ARG env=dev) |
| USER | docker 이미지 및 컨테이너에서 작업을 하는 사용자 ID를 지정함</br>(예:USER dave) |
| ONBUILD | 생성한 이미지를 기반으로 새로운 이미지를 생성시 실행하는 명령을 지정</br>(예:ONBUILD ADD mybes.tar /var/www/html) |
| VOLUME | 이미지를 위한 볼륨 생성 |

- Dockerfile에서도 주석을 사용할 수 있음
```bash
# Dockerfile 주석은 #을 쓰면 해당 라인은 주석처리됨
```
#### 1. FROM
- 베이스 이미지 지정 명령
- 반드시 Dockerfile에 작성해야 하는 명령
```bash
# Dockerfile 파일명으로 다음과 같이 작성
FROM alpine
```

#### 2. Dockerfile로 이미지 작성
```bash
docker build 옵션 Dockerfile_경로
```
- 주요 옵션

| 옵션 | 설명 |
|---|---|
| -t</br>또는</br>--tag | 이미지 이름 설정. 이미지 이름은 저장소(DockerHub ID)/이미지이름:태그와 같이 작성할 수 있음</br>(저장소 이름 및 태그 이름은 작성안해도 되면, 태그 이름이 없을 경우, 디폴트로 latest) |
| -f | 이미지 빌드시 디폴트로 Dockerfile 파일명으로 된 파일을 찾아서 이미지를 빌드함.</br>그 외의 파일명으로 이미지를 빌드할 경우 해당 옵션을 사용해서 파일명을 지정할 수 있음 |
| --pull | FROM으로 지정된 이미지는 한번 다운로드 받으면 이미지 생성시 마다 새로 다운로드 받지않고 다운로드 받은 이미지를 사용함.</br>해당 옵션은 이미지 생성시마다 새로 다운로드를 받으라는 옵션임. --pull 와 같이 작성하여 사용.</br>Dockerhub에 베이스 이미지를 수시로 업데이트하고 이를 기반으로 새로운 이미지 생성시 자주 사용할 수 있는 옵션 |

- 테스트
    - Dockerfile을 작성하고 동일 경로에서 다음과 같이 명령
    - --tag test 는 이미지의 현재 이름을 test로 설정한 것이므로, 디폴트 태그가 붙어서 test:latest로 작성됨
    - 마지막의 "."은 현재 폴더를 나타내는 것이고, 즉 현재 폴더에 Dockerfile파일이 있음을 의미함 (보다 명시적인 표기를 위해 "./"와 같이 쓰는 것을 추천하기도 함)
```bash
docker build --tag myimage .
```
- -f옵션 테스트
```bash
cp Dockerfile Dockerfile2
docker build --tag myimage -f Dockerfile .

docker images

REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
myimage      latest    b89ca249cfd7   2 weeks ago   7.73MB
```

#### 3. LABEL
- LABEL은 \<key>=\<value>형식으로 메타 데이터를 넣을 수 있는 기능
- 보통 저자, 버전, 설명, 작성일자 등을 가각 key 이름을 정하고, 값을 넣는 경우가 있음
```
# Dockerfile 파일명으로 다음과 같이 작성
FROM alpine
LABEL maintainer="seonjo@site.org"
LABEL version="1.0.0"
LABEL description="Docker test"
```
```bash
# 테스트
docker build --tag myweb .
```

#### 4. COPY
- Dockerfile 생성
    - 하부 폴더 data 폴더를 생성후 이미지에 추가할 파일을 넣어놓은 상태에서 다음과 같이 Dockerfile 생성
        - FROM 에 베이스 이미지를 httpd:alpine 으로 수정
        > VOLUME 명령도 있지만 호스트 PC의 특정 폴더를 컨테이너 내부 폴더에 연결하는 옵션은 -V 옵션으로만 가능하며,</BR> VOLUME 명령은 컨테이너 내부의 특정 폴더를 위한 볼륨을 생성하기 위해서만 사용됨</BR>예1 : VOLUME /mydata</br>예2 : VOLUME ["/mydata1","/mydata2"]  
```
FROM httpd:alpine
LABEL maintainer="seonjo@site.org"
LABEL version="1.0.0"
LABEL description="docker test"

COPY ./data /usr/local/apache2/htdocs
```
- 이미지 빌드 및 실행
    - 다음과 같이 실행한 후, localhost:9999 접속해보기
```
# Dockerfile 이 있는 폴더에서 myweb 이미지 이름으로 이미지 빌드
$ docker buile --tag myweb .

# myweb 이미지를 포트를 연결한 상태로, 백그라운드로 실행(컨테이너 이름은 apacheweb)
$ docker run -d -p 9999:80 --name apacheweb myweb
```
- 이미지 조사하기
    - 다음과 같이 httpd:alpine 이미지와 직접 Dockerfile로 작성한 이미지 조사해보고
```
# 직접 Dockerfile로 작성한 이미지 조사하기
$ docker inspect myweb

 "Labels": {
                "description": "docker test",
                "maintainer": "seonjo@site.org",
                "version": "1.0.0"
            },

# 해당 컨테이너 로그 확인
$ docker logs myweb

[Thu May 25 12:42:22.787579 2023] [core:notice] [pid 1:tid 281473508192352] AH00094: Command line: 'httpd -D FOREGROUND'
172.17.0.1 - - [25/May/2023:12:42:28 +0000] "GET / HTTP/1.1" 200 51
10.211.55.2 - - [25/May/2023:12:43:19 +0000] "GET / HTTP/1.1" 200 51
10.211.55.2 - - [25/May/2023:12:44:10 +0000] "-" 408 -
```
#### 5. CMD
- 다음 세가지 형태로 CMD 명령을 작성할 수 있음
    - 명령어, 인자를 리스트처럼 작성하는 형태(해당 방식을 docker에서는 추천)
        - 다음 예에서 echo 명령만 써줄 경우, 쉘에서 실행하지 않고 직접 해당 명령이 실행되므로 쉘에서 실행할 때, 적용되는 쉘의 환경 변수등이 적용되지 않음. 따라서 가장 정확하게는 명확히 쉘까지 지정해서 명령을 실행해주는 것이 좋음
        - /bash/sh -c 명령은 /bin 디렉토리에 있는 sh 프로그램(기본 쉘 프로그램)을 실행하되,
            - -c 옵션은 쉘 명령을 터미널상에서 받지 않고, 인자로 받겠다는 의미. 따라서 /bin/sh -c echo라고 하면, echo라는 명령을 sh 프로그램 상에서 실행하겠다라는 의미
        - 쌍따옴표로 써야함(홀따옴표를 쓰면 안됨)
```
CMD ["executable","param1","param2",...]

# 예
CMD ["/bin/sh","-c","echo","Hello"]
```

- ENTRYPOINT 명령어에 인자를 리스트처럼 작성하여 넘겨주는 형태
```
CMD ["param1","param2",...]
```

- 쉘 명령처럼 작성하는 형태
```
CMD <command> <param1> <param2> ...
```
> CMD 는 하나의 Dockerfile에서 한 가지만 설정되며, 만약 CMD 설정이 여러개일 경우, 맨 마지막에 설정된 CMD 설정만 적용됨

- httpd:alpine 기반 Dockerfile 작성하기
```
# Dockerfile_httpd 파일명으로 다음과 같이 작성
FROM httpd:alpine
LABEL maintainer="seonjo@site.org"
LABEL version="1.0.0"
LABEL description="docker test"

COPY ./data /usr/local/apache2/htdocs
CMD ["/bin/sh","-c","httpd-foreground"]
```
- 이미지 작성하고 컨테이너 실행
    - 다음과 같이 작성 후에 localhost:9999로 접속
        ```
        # 이미지 생성
        $ docker build --tag myweb2 -f Dockerfile_httpd .

        # 컨테이너 생성(백그라운드 실행 및 포트 오픈, 중지시 컨테이너 바로 삭제)
        $ docker run -d -p 9999:80 --name httpdweb1 --rm myweb2
        ```

- 가끔 사용하는 docker 명령1 : 컨테이너 에러 또는 출력 결과 확인
```
# docker logs 컨테이너id_또는_이름
docker logs httpdweb1
```

- 가끔 사용하는 docker 명령2 : 컨테이너 즉시 중지하기
    - docker stop 은 즉시 컨테이너를 중단하지 않고 현재 실행중인 단계까지는 기다린 후에 중지함,
    - docker kill 즉시 컨테이너를 중지함
    ```
    $ docker kill 컨테이너id_또는_이름
    ```
- CMD 변경해보기
```
# Dockerfile_httpd2 파일명으로 다음과 같이 작성

FROM httpd:alpine
LABEL maintainer="seonjo@site.org"
LABEL version="1.0.0"
LABEL description="docker test"

COPY ./data /usr/local/apache2/htdocs
CMD ["/bin/sh"]
```

```
# 이미지 생성
$ docker build --tag myweb2 -f Dockerfile_httpd2 .

# -dit 옵션으로 터미널 붙이고, 포트 오픈, 백그라운드로 실행,컨테이너 중지시 삭제
$ docker run -dit -p 9999:80 --name httpdweb2 --rm myweb2
```
- 위와 같이 실행한 후, localhost:9999로 접속 시, 접속 실패
```
# 해당 컨테이너에 접속하기
$ docker attach httpdweb2

# COPY 가 정상적으로 됐는지 파일 확인해보기
$ cd /usr/local/apache2/htdocs
$ ls
```
- 이미지 조사하기
    - CMD가 변경된 것을 확인할 수 있음
    - 터미널에 접속할 수 있었던 것은 -dit 옵션으로 터미널은 연결된 채로 컨테이너 실행시 /bin/sh 프로그램이 실행되면서 대기 상태로 되어 있기 때문

```
"Config":{
    "Cmd":[
        "/bin/sh
    ]
}
```
- CMD 명령 덮어씌우기
```
$ docker run -dit -p 9999:80 --name httpdweb2 -rm myweb2 /bin/sh -c httpd-foreground
```
- 컨테이너와 이미지 조사하기
    -Config.Cmd 확인해보면, 명령어 덮어 씌워졌음을 확인할 수 있음
```
$ docker inspect myweb2

$ docker inspect httpdweb2
```
#### 6. ENTRYPOINT
- ENTRYPOINT는 docker run시에 함께 넣어지는 CMD 명령에 덮어씌워지지 않고, 반드시 실행해야 하는 명령을 기입할 때 사용
    - 이 때, docker run시 함께 넣어지는 명령은 ENTRYPOINT에 작성된 명령의 인자로 넣어지게 됨
    - 따라서 ENTRYPOINT에 컨테이너 실행 시, 반드시 실행되어야 하는 명령을 넣고, 별도로 각 컨테이너 생성시 필요한 인자는 docker run 에 넣는 식으로도 활용하기도 함
- ENTRYPOINT로 변경해보기
```
# Dockerfile_httpd3 파일명으로 다음과 같이 작성

FROM httpd:alpine
LABEL maintainer="seonjo@site.org"
LABEL version="1.0.0"
LABEL description="docker test"

COPY ./data /usr/local/apache2/htdocs
ENTRYPOINT ["/bin/sh"]
```
```
# 이미지 생성
$ docker build --tag myweb3 -f Dockerfile_httpd3 .

# -dit 옵션으로 터미널 붙이고, 포트 오픈, 백그라운드로 실행
$ docker run -dit -p 9999:80 --name httpdweb3 myweb2 /bin/sh -c httpd-foreground
```
- 컨테이너와 이미지 조사하기
    - 역시 localhost:9999 동작하지 않음
    - Cmd는 null 이고, Entrypoint에만 항목이 들어감
```
$ docker inspect myweb3



$ docker inspect httpdweb3



$ docker logs httpdweb3
```
- 위 에러를 조사하기 위해 다음과 같이 테스트
```
# 호스트(자신의PC)에서 터미널에서 다음과 같이 명령해봄
$ echo hello hi
hello hi
# echo 명령은 여러 인자를 그대로 화면에 출력하는 기능을 수행함
```
- 모든 이미지 컨테이너 삭제
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi -f $(docker images -q)
```
- 이미지 작성
```
# Dockerfile_httpd3 파일명으로 다음과 같이 작성

FROM httpd:alpine
LABEL maintainer="seonjo@site.org"
LABEL version="1.0.0"
LABEL description="docker test"

COPY ./data /usr/local/apache2/htdocs
ENTRYPOINT ["/bin/echo","hello"]
```
- 이미지 생성
```
# 이미지 생성
$ docker build --tag myweb3 -f Dockerfile_httpd3 .

# 컨테이너 작성
$ docker run -dit -p 9999:80 --name httpdweb3 myweb3 /bin/sh hi

# 출력(STDOUT) 확인
$ docker logs httpdweb3
hello /bin/sh hi

$ docker inspect httpdweb3



```
- 즉 CMD 의 /bin/sh hi 두 명령은 Entrypoint의 인자로 추가가 됨
    - /bin/echo hello /bin/sh hi

#### 7. RUN
- docker는 이미지 생성 시, 각 단계를 layer로 나누어 작성함
    - 이를 통해 특정 단계 변경시 전체 이미지를 다시 다운로드 받지 않아도 됨
-RUN 명령은 이미지 생성 시, 일종의 layer를 만들 수 있는 명령으로 보통 베이스 이미지에 패키지(프로그램)을 설치하여 새로운 이미지를 만들 때 많이 사용
```
$ docker pull httpd:alpine



```
- 예 : ubuntu 18.04 버전에 apache2 설치하고, 나만의 웹페이지 복사 후, 웹서버 구동
```
# Dockerfile_httpd4 파일명으로 다음과 같이 작성

FROM httpd:18.04
LABEL maintainer="seonjo@site.org"
LABEL version="1.0.0"
LABEL description="docker test"

RUN apt-get update # 패키지 정보 업데이트
# apache2 패키지 설치, 중간에 y/n 묻는 단계가 나오면 모드 Yes로 하고 설치
RUN apt-get install -y apache2 

# apache2 디폴트 웹서버 설정은 /var/www/html/ 폴더의 웹페이지를 보여줌
COPY ./data /var/www/html

# apache2 웹서버 구동 명령은 다음과 같음
ENTRYPOINT ["/usr/sbin/apache2ctl","-D","FOREGROUND"]
```
```
# 이미지 생성(각 명령이 실행되며 layer를 작성함)
$ docker build --tag myweb4 -f Dockerfile_httpd4 .

# 컨테이너 작성
$ docker run -dit -p 9999:80 --name httpdweb4 --rm myweb4
```
- 다음과 같이 Dockerfile 변경 후, 이미지 작성시 일정 단계까지는 기존에 작성된 layer를 그대로 쓰는 것을 확인할 수 있음
```
# Dockerfile 파일명으로 다음과 같이 작성

FROM httpd:18.04
LABEL maintainer="seonjo@site.org"
LABEL version="1.0.0"
LABEL description="docker test"

RUN apt-get update # 패키지 정보 업데이트
# apache2 패키지 설치, 중간에 y/n 묻는 단계가 나오면 모드 Yes로 하고 설치
RUN apt-get install -y apache2 apt-utils

# apache2 디폴트 웹서버 설정은 /var/www/html/ 폴더의 웹페이지를 보여줌
COPY ./data /var/www/html

# apache2 웹서버 구동 명령은 다음과 같음
ENTRYPOINT ["/usr/sbin/apache2ctl","-D","FOREGROUND"]
```
#### 8. EXPOSE
- docker 컨테이너의 특정 포트를 외부에 오픈하는 설정
    - docker run -p 옵션으로 설정할 수도 있음
        - docker run -p 옵션은 컨테이너의 특정 포트를 외부에 오픈하고 해당 포트를 호스트 pc의 특정 포트와 매핑시킴
    - 이에 반해, EXPOSE는 컨테이너 생성 시, 특정 포트를 외부에 오픈하는 것만 설정하는 것임
        - 따라서, 독립적으로 실행시에는 EXPOSE 옵션을 넣는다고 해서 호스트PC에서 해당 컨테이너에 포트번호로 접속할 수 있는 것음 아님
```
# Dockerfile_httpd5 파일명으로 다음과 같이 작성

FROM httpd:18.04
LABEL maintainer="seonjo@site.org"
LABEL version="1.0.0"
LABEL description="docker test"

RUN apt-get update 
RUN apt-get install -y apache2 apt-utils

EXPOSE 80
COPY ./data /var/www/html

ENTRYPOINT ["/usr/sbin/apache2ctl","-D","FOREGROUND"]
```
```
$ docker build --tag myweb -f Dockerfile_httpd5 .
```
```
$ docker inspect myweb


```
```
# -P 옵션을 쓰면, EXPOSE로 오픈된 포트에 호스트PC의 랜덤 포트가 매핑됨
$ docker run -P -d myweb
```
#### 9. ENV
- 컨테이너 내의 환경 변수 설정
- 설정한 환경변수는 RUN,CMD,ENTRYPOINT 명령에도 적용됨
```
# Dockerfile_mysql 파일명으로 다음과 같이 작성

FROM mysql:latest

# mysql 슈퍼관리자인 root ID에 대한 password 란에 원하는 패스워드 설정
ENV MYSQL_ROOT_PASSWORD=password
# dbname란에 원하는 데이터베이스 이름 설정
ENV MYSQL_DATABASE=dbname

# 필요시 다음 설정도 가능
# user란에 mysql 추가 사용자 id 설정
# ENV MYSQL_USER=user 
# pw란에 mysql 추가 사용자 id 의 패스워드 설정
# ENV MYSQL_PASSWORD=pw
```
```
# docker 이미지 작성하기
$ docker build --tag mysqldb -f Dockerfile_mysql .

# docker 백그라운드 실행
$ docker run -d --name mydb mysqldb

# 컨테이너 접속해서 쉘 실행하기
$ docker exec -it mydb /bin/bash

# 이미지에서 설정한 패스워드 입력하기
$ mysql -u root -p
패스워드 입력

# mysql 내부에서 davedb가 있음을 확인할 수 있음
mysql> show databases;

# mysql 종료
mysql> exit

# 컨테이너 접속 종료
exit
```
> **참고**
- 다음과 같은 기능도 가능함
   - 단, 해당 명령을 EC2 서버에서 진행시, 인바운드 규칙에 3306번 포트를 추가해야 함.
- mysql 컨테이너가 다운되더라도 데이터베이스 파일은 삭제되지 않고 유지될수 있도록 볼륨 설정
```
# 외부에서 mysql 컨테이너를 접속하는 경우 내부 포트 3306에 연결하고, volume 옵션 설정하기
# volume 옵션은 맥/윈도우 등에서는 절대경로로, 리눅스 상에서는 상대경로로 설정
$ docker run -d -p 3306:3306 -v /home/ubuntu/00_TEST/data:/var/lib/mysql --name mydb mysqldb
```
#### 10. WORKDIR
- RUN, CMD, ENTRYPOINT 명령이 실행될 디렉토리 설정
```
FROM httpd:alpine

WORKDIR /usr/local/apache2/htdocs

CMD /bin/cat index.html
```
```
# 이미지 생성
$ docker build --tag httpd6 -f Dockerfile_httpd6 .

# 컨테이너 생성(백그라운드로 실행)
$ docker run -d --name myhttpd6 httpd6

# 출력결과 확인(cat index.html 실행 결과를 확인할 수 있음)
$ docker logs myhttpd6
```

#### docker build시 소스파일 github에서 받아오기

```
FROM ubuntu

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive


RUN apt update  && apt install -y git
RUN apt install -y build-essential
RUN apt update  
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update && apt install -y python3.9

RUN apt-get update && apt-get install -y python3
RUN apt-get install -y python3-pip && pip install --upgrade pip

# git clone
RUN git clone https://github.com/shimseonjo1/djangotest.git .

RUN pip install -r requirements.txt
#RUN ls /usr/bin/python
#RUN python manage.py makemigrations
#RUN python manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000
```
```
docker build --tag django .
docker run -d --name djangotest django
```

```
FROM python:3.9.16-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt update && apt install -y git

# git clone
RUN git clone https://github.com/shimseonjo1/djangotest.git .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000
```