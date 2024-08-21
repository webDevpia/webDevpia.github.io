---
title: Docker
layout: default
parent: Cloud
nav_order: 4
permalink: /cloud/docker
nav_exclude: true
search_exclude: true
---

# 1.  Docker

다양한 운영체제와 시스템 환경상에서, 서버 셋업을 위한 작업이 각각 다르고 복잡함. 도커는 컨테이너 기반의 가상화 플랫폼으로, 컨테이너 상에 서버를 셋업해 놓을 수  있음. 따라서 기반 환경이 다르더라도, 언제든 해당 컨테이너를 실행만 하면 동일한 서버 셋업이 가능함.

# 2. Docker 주요 구성 요소

## docker 엔진

- docker는 서버/클라이언트 구조로 이루어짐

## docker image

- docker 컨테이너를 생성하기 위한 명령들을 가진 템플릿
- 여러 이미지들을 layer로 쌓아서 원하는 형태의 이미지를 만드는 것이 일반적임
    - ex : ubuntu 이미지에 apache 웹서버 이미지를 얹어서 웹서버 이미지를 만듬 

## docker container

- docker image가 리눅스 컨테이너 형태로 실행한 상태(instance)를 의미함
- docker daemon에 있는 커널에서 LXC(linux container : 리눅스 컨테이너)로 리눅스 컨테이너를 생성한 후 해당 컨테이너에 docker image에 포함된 명령을 실행하여 docker container를 만들고 실행함
- docker container는 분리된 공간이므로, docker daemon process를 통해 접속할수도 있고 내부에 들어가서 코드 수정, 재실행 등도 가능함

# 3. Docker image 주요 명령

- docker명령은 CLI(Command Line Interface)로 키보드로 직접 명령을 작성하는 형태로 수행하며 명령 형식은 크게 다음과 같은 형태이다.

```bash
docker 명령 옵션 선택자(이미지ID/컨테이너등)
```

- docker는 image와 container명령이 각각 별도로 존재
- 다음과 같이 image를 다루는지 container를 다루는지를 명시적으로 이해하기 위해 docker 다음에 image 또는 container를 기재해줌
    - 명령어는 어차피 다르므로 굳이 image 또는 container를 붙이지 않아도 되지만 최근에는 해당 키워드를 붙여 주는 경향이 있음

```bash
docker image 명령 옵션
docker container 명령 옵션
```    

## 1. docker 서버에 로그인/로그아웃

```bash
docker login
docker logout
```

## 2. 다운로드 받을 이미지 검색

```bash
docker search ubuntu
```

- docker 이미지는 크게 이미지명[:태그]로 이루어질 수 있음
- 태그는 보통 버전 정보를 넣는 경우가 많음
- 이미지명에 태그를 넣지 않으면 최신 버전의 이미지를 의미하며 최신 버전 이미지에서 가장 최신이라는 의미의 태그인 latest가 붙음
- ubuntu로 검색하면 다양한 이미지 리스트를 볼 수 있음. 이 중에서 OFFICIAL 항목이 [OK]라고 씌여 있으면 공식 이미지임
- 결과가 많을 경우 --limit 옵션을 사용

```bash
docker search --limit=5 ubuntu
```

## 3. 이미지 다운로드

- 태그를 안붙이면 디폴트로 latest(최신버전)을 다운로드 받음

```bash
docker pull ubuntu
```

- 특정 태그에 해당하는 버전을 다운로드

```bash
docker pull ubuntu:22.04
```

- docker pull 명령은 이미지를 다루는 명령이므로 docker image pull로 사용 가능

## 4. 다운로드 받은 이미지 목록 확인

- docker images 명령과 docker image ls 명령으로 확인

```bash
docker images

REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       latest    3f5ef9003cef   3 weeks ago   69.2MB

# docker IMAGE ID만 표시(다른 명령과 조합해서 사용)
docker images -q

3f5ef9003cef
```

- docker image ls 명령

```bash
docker image ls

REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       latest    3f5ef9003cef   3 weeks ago   69.2MB

# docker IMAGE ID만 표시(다른 명령과 조합해서 사용)
docker image ls -q

3f5ef9003cef
```

## 5. 다운로드 받은 이미지 삭제하기

- docker rmi 명령과 docker image rm 명령으로 동일한 기능을 수행할 수 있음

```bash
docker rmi 이미지ID(또는 이미지 REPOSITORY 이름)

docker image rm 이미지ID(또는 이미지 REPOSITORY 이름)
```

> 일괄적으로 이미지 및 컨테이너 전체를 삭제하는 명령은 컨테이너 명령 이후에 정리

# 4. Docker Container 관련 주요 명령

## 1. 컨테이너 생성

- 각 이미지는 컨테이너로 만들어야 실행 가능
- 이미지와 컨테이너는 각각 따로 관리한다
- 컨테이너 생성시 이름을 설정하지 않으면 docker 프로그램에서 이름이 자동 부여된다

```bash
docker create ubuntu
```

- 컨테이너 관리를 위해 컨테이너 이름을 내가 원하는 이름으로 생성

```bash
docker create --name 컨테이너이름 이미지이름
# 예
docker create --name myubuntu ubuntu
```

## 2. 생성된 컨테이너 확인

```bash
# 실행중인 컨테이너만 보임
docker ps

# 전체 컨테이너 목록을 확인
docker ps -a

# 출력
CONTAINER ID   IMAGE     COMMAND       CREATED          STATUS    PORTS     NAMES
81e0d512ec47   ubuntu    "/bin/bash"   10 seconds ago   Created             practical_solomon
```

항목 | 설명
CONTAINER ID | 컨테이너 이름  
IMAGE | 이미지 이름
COMMAND | 컨테이너 실행시 실행되는 프로세스 이름
CREATED | 컨테이너 생성 후 경과시간
STATUS | 컨테이너 실행상태    (Created:생성,Up:실행중,Pause:중지,Existed:종료)
PORTS | 호스트와 컨테이너 포트 연결관계
NAMES | 컨테이너 이름   

> 각 이미지마다 컨테이너 생성 시 실행되는 프로세스 기재할 수 있다. ubuntu의 경우 bash 쉘 프로그램이 실행되며 이를 COMMAND 항목에서 확인할 수 있음  (실제 실행 파일은 리눅스 시스템에서 bin 디렉토리에 bash 프로그램을 실행하기 때문에 /bin/bash로 표기됨)


- 실행중이지 않은 컨테이너 포함해서 전체 컨테이너 ID 만 출력하기

```bash
docker ps -a -q
```

## 3. 컨테이너 삭제

```bash
docker rm 삭제할컨테이너이름(혹은 컨테이너id)

docker rm myubuntu
```

## 4. 컨테이너 실행

```bash
docker start 컨테이너이름
```

- 위 예에서 다운로드 받고 생성한 myubuntu 컨테이너를 실행하면 바로 중지됨
    - docker start myubuntu 명령 후에, docker ps를 실행하면 myubuntu 컨테이너를 볼 수 없음
    - docker는 컨테이너를 하나의 응용프로그램으로 다루고 있음
        - 즉, 운영체제가 아니라 운영체제 상에서 실행하는 응용 프로그램을 포함해서 하나의 프로그램을 실행하고 중지하는 것으로 처리됨
        - 따라서, 컨테이너에서 실행하게끔 설정된 응용 프로그램의 실행이 끝나면 해당 컨테이너는 중지됨
        - 이미지 세부 정보를 알수 있는 docker inspect
            - Cmd 항목에 해당 컨테이너 실행 시, 실행하는 명령(응용프로그램)이 기재되어 있음

            ```bash
            docker inspect ubuntu

            # 내용중 Config의 Cmd 내용 확인
             "Cmd": [
                "/bin/bash"
            ],
            ```

            - 해당 명령은 /bin/bash, bash라는 쉘 프로그램(리눅스의 기본 쉘 프로그램)
            - 명령은 터미널을 통해 키보드 입력을 표준 스트림 중 표준 입력(STDIN)으로 받을 수 있는 상태이어야 대기상태로 계속 실행되며, 그렇치 않다면 입력을 받을 수 없기 때문에 종료됨
            - 따라서 단순히 docker start myubuntu와 같이 별도 터미널 및 표준 입력 연결 설정 없이 실행 시, 실행하자마자 끝나고, 이에 따라 해당 컨테이너도 바로 중지 상태가 됨

> **표준스트림(standard streams)**   

> 리눅스(유닉스 계열)에서 동작하는 프로그램은 실행 시, 세 개의 스트림(streams)이 오픈됨
> - STDIN : standard input(표준 입력)
> - STDOUT : standard output(표준 출력)
> - STDERR : standard error(표준 에러)   
> 보통 터미널을 오픈하고 명령을 실행하면 터미널 표준 스트림이 명령에 해당하는 프로세스에 상속되고, 해당 프로세스는 터미널의 표준 입출력을 사용할 수 있게 된다.
>   - 터미널 실행시, 보통 쉘 프로그램이 실행되고, 쉘 프로그램을 통해 명령을 실행하면 명령에 해당하는 프로그램을 쉘 프로그램이 실행함
>   - 이 때, 내부적으로 쉘 프로그램은 fork() 시스템콜을 사용해서, 명령에 해당하는 프로그램을 실행시킴
>   - fork() 시스템콜을 사용할 경우, 해당 함수를 호출하는 프로그램은 부모 프로세스가 되고, fork()를 통해 실행되는 프로그램은 자식 프로세스가 됨

## 5. docker run 명령

ubuntu 자체만 컨테이너를 만들 경우, 다음 명령으로 터미널 및 입력(STDIN)을 연결해줘야 함.
- ubuntu 컨테이너의 입력(STDIN)(-i 옵션)을 가상 터미널(-t옵션)에 할당해주어, 결과적으로 PC 상에서의 입력이 ubuntu 컨테이너 입력에 들어갈 수 있도록 해줌
- 이를 통해 ubuntu 컨테이너의 bash 쉘은 입력을 받을 수 있는 상태로, 종료되지 않고, 실행 중인 상태가 됨

### **docker run 주요 옵션**

옵션 | 설명
-i | 컨테이너 입력(STDIN)을 열어놓은 옵션   (주로 -it로 -t옵션과 함께 사용)
-t | 가상 터미널(tty)을 할당하는 옵션
- - name | 컨테이너 이름을 설정하는 옵션
-d | 컨테이너를 백그라운드에서 실행하는 옵션
- - rm | 컨테이너 종료시 컨테이너를 자동으로 삭제하는 옵션
-p | 호스트와 컨테이너 포트를 연결하는 옵션 [호스트 포트]:[컨테이너 포트]
-v | 호스트와 컨테이너 디렉토리를 연결하는 옵션

### **-it옵션의 의미**

- docker 컨테이너에 표준 입력을 오픈해놓고 (-i)
- pseudo tty를 만들어서 (-t옵션) 해당 표준 입력을 pseudo tty 에 연결해 놓음
- 따라서 키보드 입력을 pseudo tty를 통해 컨테이너의 표준 입력으로 전달할 수 있도록 하는 것임

### **pseudo tty**

- tty는 teletypewriter의 약자로, 리눅스(유닉스 계열)에서는 콘솔 또는 터미널을 의미함
- tty를 통해 리눅스에 키보드 입력을 전달할 수 있으며, 하나의 tty 이외에 다양한 터미널에서 접속을 지원하기 위해 두번째 tty부터 가상(pseudo)이라는 말이 붙어서 pseudo tty라고 함

```bash
# 컨테이너 실행 후, 해당 ubuntu 내로 들어가서, 터미널로 명령을 실행할 수 있음
docker run -it ubuntu

# ubuntu 내 터미널로 진입
root@6d2c54e81f08:/#

# ubuntu 내 터미널에서 exit 명령으로 종료시 컨테이너도 중지됨
root@6d2c54e81f08:/# exit

docker run -it ubuntu --name myubuntu ubuntu

docker ps -a
```

- 컨테이너 종료시 자동으로 컨테이너까지 삭제하는 옵션

```bash
docker run -it --rm --name myubuntu2 ubuntu

# ubuntu 내 터미널에서 exit 명령으로 종료시 컨테이너도 자동 삭제됨
root@6d2c54e81f08:/# exit

# 목록에서 myubuntu2가 없음
docker ps -a
```

- 컨테이너를 백그라운드로 실행하기 (실행중인 상태이지만 터미널로 입력은 받지 않은 상태)

```bash
# -d 옵션은 컨테이너 프로세스를 백그라운드로 실행, 
docker run -it -d --name myubuntu3 ubuntu

# 실제 컨테이너ID가 출력됨
6f34b395d72e7d1d9017ded2bfcd84dc2b53609f96a14f7c476a357e3e6b73b5

# 실행 내용 확인하면 컨테이너ID 12자리 표시됨
docker ps

CONTAINER ID   IMAGE     COMMAND       CREATED              STATUS              PORTS     NAMES
6f34b395d72e   ubuntu    "/bin/bash"   About a minute ago   Up About a minute             myubuntu3
```

## 6. 실행 중인 컨테이너 종료하기

- 이전에 백그라운드로 실행한 myubuntu3를 중지

```bash
docker stop myubuntu3

docker ps

# 컨테이 종료 확인
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

- 중지한 컨테이너는 docker start 명령으로 재실행

```bash
docker start myubuntu3
```

> 실행 중인 컨테이너의 실행 상태를 잠깐 멈추는 명령은 docker pause 이며, docker unpause로 다시 실행

## 7. 웹서버로 docker run 옵션 테스트

- 웹서버는 크게 두가지 프로그램 많이 사용
    - apache
    - nginx

### 7.1 apache 웹서버 공식 docker 찾기

- 각 docker 마다 공식 이름이 프로그램명과 동일한 경우가 일반적이지만 apache는 httpd 를 사용함.

```bash
docker search httpd
```

- 너무 길면 다음과 같이 --limit 옵션을 사용할 수 있음

```bash
docker search httpd --limit=5
```

### 7.2 이미지 다운로드 받고 바로 컨테이너로 만들어 실행시키기 (-p 옵션 이해하기)

다음과 같이 명령하면 몇가지 문제점이 눈에 뜀

```bash
docker run httpd

# 처음에 다음과 같은 메세지가 나오는 것은 문제가 안됨. 자신의 pc에 해당 이미지가 없다라는 의미로 바로 이후에 해당 이미지 이름을 Docker Hub에서 찾아서 다운로드함

Unable to find image 'httpd:latest' locally
```

- 커멘드 라인에 다음 명령을 할 수 없음(해당 컨테이너가 foreground로 실행되고 있기 때문임)
- apache 웹서버가 실행된 상태로 해당 프로그램 로그만 화면에 보여짐
    
```bash
[Sun May 21 11:06:41.205539 2023] [mpm_event:notice] [pid 1:tid 281473553653776] AH00489: Apache/2.4.57 (Unix) configured -- resuming normal operations
[Sun May 21 11:06:41.205596 2023] [core:notice] [pid 1:tid 281473553653776] AH00094: Command line: 'httpd -D FOREGROUND'
```

- Ctrl+C로 강제 중단시킨 후, 관련 컨테이너는 중지 상태이므로 삭제해도 됨
- -d 옵션을 주어 background로 해당 컨테이너를 실행하면 해결됨

```bash
docker run -d --name apacheweb httpd
```

- 이번에는 해당 웹서버에 어떻게 접속해야 할지 알 수 없음
    - 포트 포워딩이 필요함
    - docker를 실행한 PC를 Host PC(호스트 PC)라고 함
    - docker 컨테이너가 실행되면 Private IP가 할당
    - 호스트 PC IP에 특정 Port로 access 시, 해당 Port를 docker 컨테이너의 특정 Private IP의 특정 포트로 변환해 줄 수 있음. 이를 NAPT(Network Address Port Traslation) 기술이라고 함
    - 이를 지원해 주는 옵션이 -p 옵션임

```bash
docker run -d -p 9999:80 --name apacheweb2 httpd

# localhost,127.0.0.1 에 9999 포트로 접속하면 해당 컨테이너의 80포트로 연결
curl http://localhost:9999

# index.html 페이지의 내용을 가져온다.
<html><body><h1>It works!</h1></body></html>
```

- 가상머신을 실행한 컴퓨터에서 웹브라우저를 실행하고 가상머신의ip:9999 로 접속 확인

### 7.3 나만의 웹서비스 docker 만들기(-v옵션 이해)

- 'It works!'는 httpd 이미지의 apache 웹서버 기본 설정에 의해 /usr/local/apache2/htdocs폴더에 있는 index.html에 적혀 있는 html 태그의 내용임
- 해당 폴더를 내가 원하는 index.html 파일이 있다면 나의 웹이지를 보여줄수 있음 
- 호스트pc상에 나만의 index.html 파일이 있다면 -v 옵션을 사용해서 호스트 PC의 특정 폴더를 docker 컨테이너의 특정 폴더로 교체할 수 있음
    - docker는 이미지를 기반으로 컨테이너를 만들기 때문에 컨테이너 상에서 파일을 업데이트하거나 생성할 경우, 이 컨테이너가 종료되면 해당 파일은 없어지게 됨
    - 이를 보완하기 위해 특정 폴더를 -v 옵션으로 교체(공유 또는 바인딩이라는 용어를 더 많이 사용)하면 해당 폴더는 호스트 PC 상에 있기 때문에 컨테이너가 종료되더라도 파일을 유지할 수 있음
    - 호스트 PC 에 /home/ubuntu/html폴더 생성하고 index.html 파일을 작성한 후 테스트 한다.

```bash
# -v 옵션만 쓴다면 다음과 같이 작성 가능
docker run -v 호스트_pc_절대경로:도커_컨테이너_절대경로 httpd

# 다른 옵션과 함께 사용한 실제 예(호스트 pc 경로에 한글이나 띄어쓰기가 있다면 따옴표로 묶어줘야 함)
docker run -d -p 9999:80 -v /home/ubuntu/html:/usr/local/apache2/htdocs --name apacheweb3 httpd

curl http://localhost:9999
<html><body><h1>docker test!!!</h1></body></html>
```

- 가상머신이 설치된 컴퓨터에서는 웹브라우저에 http://가상머신ip:9999 로 접속 테스트 한다.

## 8. docker가 사용하고 있는 저장매체 현황 확인하기

- 추후 docker가 사용하는 저장매체 공간이 이슈가 될 수도 있으므로 관련 명령어 익혀둬야 함

```bash
docker system df
```

**docker 와 alpine**

- docker 이미지는 여러개의 이미지가 계층(layer)으로 쌓인 형태로 작성됨
    - 통상 리눅스 사용 시 다양한 기능을 가진 ubuntu 등의 리눅스 패키지를 사용하지만, docker 컨테이너의 경우는 특정 응용 프로그램 실행을 목적으로 하는 경우가 많기 때문에 다양한 기능을 모두 포함할 필요가 없음(동일한 기능을 한다면 도커 이미지/컨테이너 사이즈가 작으면 작을수록 좋음)

- 대부분의 docker 이미지에 가장 기본이 되는 이미지는 ubuntu가 아니라 alpine인 경우가 많음
    - alpine 은
        - 용량을 줄이기 위해 시스템 기본 c runtime을 glibc 대신 musl libc를 사용하며 busybox를 탑재
    - httpd도 태그 중에 alpine 기반 태그가 있음
    - httpd:alpine 실행해보기

```bash
docker run -d -p 9999:80 -v /home/ubuntu/html:/usr/local/apache2/htdocs --name apacheweb4 httpd:alpine
```

## 9. 실행중인 컨테이너 사용 리소스 확인하기

- 실행중인 컨테이너의 시스템 리소스 사용현황을 확인할 수 있음
- 종료는 CTRL + C 

```bash
docker container stats

CONTAINER ID   NAME         CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O        PIDS
db5ea4516252   apacheweb4   0.01%     7.227MiB / 1.921GiB   0.37%     8.18kB / 1.66kB   53.2kB / 4.1kB   109
^C
```

## 10. 실행중인 컨테이너에 명령 실행하기

- 컨테이너가 실행중일 때에만 다음 명령을 실행할 수 있음

```bash
docker exec 옵션 컨테이너_id 명령 인자
```

- 테스트
    - -it : docker run에서 -i(표준입력), 터미널(-t)옵션이며, docker exec 에서도 사용 가능
    - 다음과 같이 명령하면 /bin/sh 쉘 프로그램을 실행하면서 터미널에 연결되므로 컨테이너 안으로 들어갈 수 있음
        - /bin/bash가 아닌 /bin/sh 를 쓴 이유는 /bin/bash 는 alpine 리눅스에는 들어있지 않기 때문(꼭 필요한 프로그램만 들어가므로)

```bash
docker exec -it apacheweb2 /bin/sh
```

## 11. 실행중인 컨테이너에 연결하기

- docker run으로 다음과 같이 터미널을 연결해 놓은 상태로 백그라운드로 실행 시
    - 여러 옵션은 -dit 와 같이 한번에 붙여써도 되고 다음과 같이 나누어 써도 됨

```bash
docker run -it -d --name myubuntu3 ubuntu
```

- 다음과 같이 실행하면 해당 컨테이너에 연결되어 컨테이너 내에서 쉘 프로그램을 사용하여 명령을 내릴 수 있다

```bash
docker attach myubuntu3 # docker attach 컨테이너_ID
```

> exec 명령은 해당 컨테이너에 신규 명령을 실행하는 명령이고, attach는 컨테이너에 연결하는 명령임

## 12. dockerhub에 저장하기

### 1. dockerhub에 회원가입

docker hub 사이트에 회원 가입한다.

### 2. 터미널에서 로그인

```bash
docker login
```

### 3. 현재 작업중인 컨테이너 이미지로 저장

```bash
docker ps -a
docker images

# 형식
docker commit [CONTAINER ID] [dockerhub ID/저장할 이미지이름:태그]

docker commit bb5 shimseonjo/simple_nginx:test

```

### 4. docker hub에 올리기

```bash
# 형식
docker push [dockerhub ID/저장할 이미지이름:태그]

docker push shimseonjo/simple_nginx:test
```

## 13. 모든 컨테이너 삭제하기(+ 모든 docker 이미지 삭제하기)

- docker run 명령을 가장 많이 사용할 수밖에 없는 상황이지만 docker run 사용시 항상 컨테이너가 별도로 생성됨
- 따라서 모든 컨테이너를 한번에 지우고 싶은 경우 일때 다음과 같은 명령 조합으로 가능함

```bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

- 추가로 모든 docker 이미지 삭제 명령

```bash
docker rmi -f $(docker images -q)
```

- 한번에 컨테이너 중지, 삭제, 이미지 삭제 하기

```bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi -f $(docker images -q)
```

- 다음 명령은 실행중인 container 또는 실행 중인 컨테이너의 image 등은 삭제하지 않음. 

```bash
# 도커 용량 확인
docker system df --verbose
# 정지된 켄테이너 삭제
docker container prune 
# 실행중인 컨테이너 image 외의 이미지 삭제
docker image prune 
# 정지된 컨테이너, 실행중인 컨테이너 이미지 외의 이미지, 볼륨, 네트워크 삭제
docker system prune 
#도커 미사용 볼륨 삭제
docker volume prune
```