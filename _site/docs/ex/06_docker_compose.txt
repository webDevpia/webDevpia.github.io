
# Docker Compose 란?
- Docker Compose 는 여러 컨테이너를 모아서 관리하기 위한 툴
- 웹서비스는 프론트엔드 서버, 데이터베이스 서버, 백엔드 서버로 이루어저 있는 경우가 많음
    - 각각을 docker 컨테이너로 작성하고 연결하여 동작하기 때문에 Docker compose와 같은 컨테이너 관리 툴이 필요함
- 더 나아가 서비스 규모가 커지면 복수의 컨테이너를 유지하고 관리해야 하며, 이를 위해 쿠버네티스 등의 관리 툴이 사용됨
    - docker와 docker compose를 잘 다룰수 있으면 기본적인 서비스 구현이 가능
    - docker와 docker compose에 대한 탄탄한 이해가 바탕이 되어야 추후 필요시 쿠버네티스도 원활하게 익히고 활용할 수 있음

## 1. Docker Compose 작성 기본
- Docker Compose는 docker-compose.yml 파일을 작성하여 실행할 수 있음
- docker-compose.yml 파일은 YAML(야물)형식으로 작성함
### YAML 문법
- IT에서는 데이터 구조화하는 다양한 문법이 있음
- 대표적인 데이터 구조화 문법은 JSON, XML, CSV등이 있음
- YAML 기본문법
    - \# : 해당라인 주석철
    - \--- : 문서 시작을 나타냄(옵션)
    - \... : 문서 끝을 나타냄(옵션)
    - key:value : key에 대한 값(value)
    - 자료형
        - int, string, boolean 지원
            - int_type : 1
            - strig_type : "문자열"
            - boolean_type : true 또는 false
    - 데이터 표현
        - JSON 포맷과 비교하며 익히면 쉽게 이해할 수 있음
    ```
    # JSON 포맷
    {
    "develee": [
        "name" : "dave lee",
        "job" : ["softwear engineer","author"]
    ],
    "code":{
        "com" : false,
        "tech" : {
            "web-front":["flutter","vue"]
        }
    }
    }
    ```
    - 리스트는 들여쓰기 (보통 스페이스 2칸 또는 4칸)로 표시
    ```
    ---
    # 문서 시작 (보통은 문서 시작/끝은 표시 안하는 경우가 많음)
    develee:
      - name: dave lee
      - job:
        - softwear engineer
        - author
    code:
      com: false
      tech:
        - web-front
          - flutter
          - vue
    ```
### 줄바꿈
- 줄바꿈 표시 : | 는 마지막 줄바꿈 포함
```
{
  "newline": "1라인\n\n2라인\n\n3라인\n"
}

newline: |
            1라인

            2라인

            3라인
```
- 줄바꿈 표시 : |- 는 마지막 줄바꿈 제외
```
{
  "newline": "1라인\n\n2라인\n\n3라인"
}

newline: |-
            1라인

            2라인

            3라인
```
- 줄바꿈 표시 : ">"는 중간에 있는 줄바꿈을 아예 무시함(마지막 줄바꿈은 포함)
    - 따라서 다음과 같이 YAML로 작성하면 그 다음과 같이 JSON으로 작성한 것과 동일하게 됨
```
{
  "newline": "1라인\n2라인\n3라인\n"
}

newline: >
            1라인

            2라인

            3라인
```
## 2. docker-compose.yml 예로 이해하는 Docker Compose 사용법 1
- Docker Compose 명령은 기본적으로 Dockerfile 에서 익힌 명령에 기반하고 있음
```
version: "3"

services:
  db:
    image: mysql:5.7
    restart: always
    volumes:
      - ./mysqldata:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=funcoding
      - MYSQL_DATABASE=fundb
    ports:
      - "3306:3306"    
```
- 기본적으로 다음과 같은 4가지의 큰 카테고리로 작성하며, 이 중에서 보통 version 과 services 만 설정하여 많이 사용함
    - volumes는 각 컨테이너 설정에서의 volumes로 선언할 수 있고, networks는 컨테이너간 네트워크 분리를 위한 추가 설정 부분임
```
# Docker Compose 파일 포맷 버전 지정
version: "3"

# 컨테이너  설정
services:

# 컨테이너에서 사용하는 volume 설정으로 대체 가능(옵션)
volumes:

# 컨테이너간 네트워크 분리를 위한 추가 설정 부분(옵션)
networks:
```
### version
- Docker Compose 파일 포맷 버전 지정
- docker 버전에 따라 지원하는 Docker Compose 버전이 있으며, 기본적으로는 버전 3으로 사용하는 것이 일반적인
    - 예를 들어 3.8과 같이 가장 최신 버전을 사용할 경우, 최신 docker 버전에서만 지원이 됨
    - 3.8과 같은 최신 버전에서만 지원하는 Docker Compose 특수 문법까지 사용할 일은 많지 않기 때문
    - [버전별 호환성 확인 사이트](https://docs.docker.com/compose/compose-file/compose-versioning/)

### services
- 위 항목 아래에서 여러개 또는 하나의 컨테이너를 설정함

### image
- 다음 코드에서 db는 컨테이너 이름을 정의한 것임
- db라는 이름의 컨테이너 작성시 Docker Hub에 있는 이미지를 사용할 경우 image를 설정하면 됨
  - mysql 이라는 Docker Hub에 있는 이미지를 사용할 경우 image를 설정하면 됨
    - mysql이라는 Docker Hub 에 있는 이미지를 사용하겠다는 의미임
```
services:
  db:
    image: mysql:5.7
```
### restart
- 컨테이너가 다운되었을 경우, 항상 재시작하라는 설정
```
services:
  db:
    image: mysql:5.7
    restart: always
```
### volumes
- docker run 옵션중 -v 옵션과 동일한 역활
- 여러 volume을 지정할 수 있기 때문에 리스트 처럼 작성
> -v옵션과 달리 상대경로로 작성 가능
```
services:
  db:
    image: mysql:5.7
    restart: always
    volumes:
      - ./mysqldata:/var/lib/mysql
```
### environment
- Dockerfile의 ENV옵션과 동일한 역활
```
services:
  db:
    image: mysql:5.7
    restart: always
    volumes:
      - ./mysqldata:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=funcoding
      - MYSQL_DATABASE=fundb
```
- 다음 env_file옵션으로 환경 변수값이 들어가 있는 파일을 읽어들일 수도 있음
  - 패스워드 등 보안이 필요한 부분을 docker compose 보다는 별도 파일로 작성하여, env_file옵션으로 읽어들이는 방식을 쓰는 경우도 많음
```
services:
  db:
    image: mysql:5.7
    restart: always
    volumes:
      - ./mysqldata:/var/lib/mysql
    env_file:
      - ./mysql.env
```
- env_file 파일 포맷
```
$ cat mysql.env
MYSQL_ROOT_PASSWORD=funcoding
MYSQL_DATABASE=fundb
```
### ports
- docker run의 -p 옵션과 동일한 역할
- YAML 문법에서 11:22(숫자로 작성한 경우)와 같이 작성하면, 시간으로 해석하기 때문에 쌍따옴표를 붙여줘야 함
```
services:
  db:
    image: mysql:5.7
    restart: always
    volumes:
      - ./mysqldata:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=funcoding
      - MYSQL_DATABASE=fundb
    ports:
      - "3306:3306"
```

## 3. Docker Compose 실행/중지하기
- 앞의 코드를 작업 폴더에 docker-compose.yml파일로 작성 후
#### Docker Compose 실행 명령
- 보통 -d 옵션을 사용하며, -d 옵션은 백그라운드 실행을 의미함
```
docker-compose up -d
```
- 이미지 재빌드가 필요하면 --build 옵션을 추가해야함, 그렇치 않으면 이미 작성된 이미지를 사용하게 됨
```
docker-compose up --build -d
```
#### Docker Compose 중지 명령
```
docker-compose stop
```
#### Docker Compose 에서 사용하는 컨테이너 삭제 명령
- docker-compose up으로 생성된 컨테이너 삭제
```
docker-compose down
```
#### 테스트
```
# Docker Compose 실행
$ docker-compose up -d

# 실행중인 컨테이너 확인
$ docker ps

# 컨테이너 삭제
$ docker-compose down

# 컨테이너 확인(삭제되어서 없음)
$ docker ps
```
## 4. docker-compose.yml 예로 이해하는 Docker Compose 사용법 2
- 기존에 작성한 docker-compose.yml에 컨테이너를 추가하여 추가 문법 이해하기
```
version: "3"
services:
  app:
    build:
      context: ./01_flask_docker
      dockerfile: Dockerfile
    links:
      - "db:mysqldb"
    ports:
      - "80:8080"
    container_name: appcontainer
    depends_on:
      - db

  db:
    image: mysql:5.7
    restart: always
    volumes:
      - ./mysqldata:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=funcoding
      - MYSQL_DATABASE=fundb
    ports:
      - "3306:3306"
    container_name: dbcontainer
```

#### build
- 이미지를 Dockerfile을 기반으로 작성시 사용
  - context : Dockerfile 이 있는 디렉토리
  - dockerfile : Dockerfile 파일명

#### links
- 컨테이너 내부에서 다른 컨테이너를 접속하고 싶을 때 사용
- 다음 YAML 코드에서 db 컨테이너를 app 컨테이너에서 사용하고 싶을때
```
services:
  app:
    build:
      context: ./01_flask_docker
      dockerfile: Dockerfile
    links:
      - "db:mysqldb"
    ports:
      - "8080:8080"
    container_name: appcontainer

  db:
    image: mysql
```
- 다음과 같이 작성하면 db라는 이름으로 컨테이너 접속 가능
```
services:
  app:
    build:
      context: ./01_flask_docker
      dockerfile: Dockerfile
    links:
      - "db"
    ports:
      - "8080:8080"
    container_name: appcontainer

  db:
    image: mysql
```
- 다음과 같이 작성하면 mysqldb 또는 db 이름으로(둘다 가능) 컨테이너 접속 가능
  - 각 명령(키)의 값에 해당하는 부분을 "" 쌍따옴표로 묶어서 명확히 값임을 표기해도 됨(단, 안해도 대부분 정상 동작함)
```
services:
  app:
    build:
      context: ./01_flask_docker
      dockerfile: Dockerfile
    links:
      - "db:mysqldb"
    ports:
      - "8080:8080"
    container_name: appcontainer

  db:
    image: mysql
```
- 테스트 환경 셋업(flask Dockerfile)
  - 다음과 같이 flask Dockerfile 작성
    - 아나콘다 도커로 continuumio/miniconda 이미지 사용
    - 아나콘다 풀 패키지에 포함된 프로그램이 많기 때문에 기본 패키지만 설치
    - flask, pymysql을 위해 필요한 라이브러리 설치
```
FROM continuumio/miniconda
COPY ./ /app
WORKDIR /app
RUN pip install flask pymysql cryptography

CMD ['python','main.py']
```
- main.py 작성
  - 제공한 01_flask_docker 폴더 내의 main.py 파일 사용
- Docker Compose 실행
  - 크롬 브라우저를 통해 localhost:8080 으로 접속 가능하면 성공
  - main.py에서 3306 포트와 mysqldb 호스트 이름을 사용한 것을 확인할 수 있음

#### dockerignore
- 위 flask Dockerfile 작성시 COPY ./ /app 구문은 현재 폴더에 있는 모든 파일을 컨테이너 내의 /app폴더에 복사
- 현재 폴더에는 Dockerfile도 있으며, 작업 환경에 따라서 예상치 못한 파일들이 있을 수 있음(예:vscode폴더)
- COPY시 특정 파일/폴더는 제외하도록 현재 폴더에 .dockerignore 파일을 작성(.gitignore 파일과 같은 방식임)
- .dockerignore 파일 포맷
```
# 주석
# */flask* : 현재 폴더의 어떤 하위 폴더든(*/) flask로 시작하는 폴더나 파일명은 제외
*/flask*

# 현재 폴더의 하위 폴더의 하위 폴더에서 flask로 시작하는 폴더나 파일명은 제외
*/*/flask*

# 하위 폴더의 깊이에 관계 없이 flask로 시작하는 폴더나 파일명은 제외
**/flask*

# 물음표는 한글자
flask?

# 별표는 0개 이상
flask*

# 현재 폴더의 모든 .txt 로 끝나는 파일 제외하되, flask.txt는 제외하지 말라는 뜻(!는 해당 조건은 제외조건에서 제외함)
*.txt
!flask.txt
```

#### container_name
- 컨테이너 이름 설정
```
docker-compose up --build -d

docker ps
```

#### depends_on
- 여러 컨테이너를 Docker Compose로 실행할 경우, 각 컨테이너가 실행을 시작하는 시점이 미묘하게 다를 수 있음
- 따라서 특정 컨테이너가 시작하자마자 바로 다른 컨테이너를 접속하도록 코드를 작성하면 시점에 따라 접속 불가 에러가 날 수 있음
- 이를 위한 옵션으로 depends_on 옵션이 있지만 해당 옵션도 컨테이너 실행 순서만 제어하고 컨테이너가 ready 상태가 될 때까지를 명확히 제어하는 것은 아니므로 depends_on 옵션이 기대한대로 동작하지 않을 수 있음
- 예를 들어 다음과 같이 작성하면 db 컨테이너가 app 컨테이너보다 먼저 실행되지만, ready상태는 어느 컨테이너가 먼저 될지는 알수 없음
  - 각 컨테이너 설정마다 실제 프로세스가 실행되는 시점은 다를 수 있기 때문
```
version: "3"

services:
  app:
    build:
      context: ./00_flask
      dockerfile: Dockerfile_flask
    links:
      - "db:mysqldb"
    ports:
      - "8080:8080"
    container_name: appcontainer
    depends_on:
    - db

  db:
    image: mysql
```

#### docker-compose logs
- 각 컨테이너의 모든 로그(출력결과) 확인

#### docker-compose config
- 실행중인 Docker Compose의 docker-compose.yml 설정 확인

#### docker-compose exec 컨테이너이름 명령
- 실행 중인 컨테이너에 명령어 실행