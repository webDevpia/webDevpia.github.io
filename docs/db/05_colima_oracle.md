---
title: Colima Oracle
layout: default
parent: DataBase
nav_order: 5
permalink: /db/colima_oracle
---
# oracle

## 1. 맥북에서 Docker로 oracle DB 설치 (colima 사용)

### 1) colima를 설치합니다.

```bash
brew install colima
```

### 2) docker 설치
- docker가 아직 설치되어 있지 않았다면 본 항목을 확인하며 설치 진행
- 기존에 이미 설치되어있다면 실행중인 Docker desktop을 종료만 하고 아래의 Colima 실행 단계 진행.

```bash
# 터미널에서 docker desktop을 설치할 수 있습니다.
brew install --cask docker

# docker 엔진만 설치하는 방법입니다.
# docker desktop 설치 했으면 이 과정은 필요 없습니다.
brew install docker
```

### 3) docker context목록 확인 및 변경(필수아님)

```bash
docker context ls
docker context use desktop-linux
docker context use colima
```

### 4) colima 실행

```bash
colima start --memory 4 --arch x86_64
```

### 5) 컨테이너 리스트를 확인

```bash
docker ps
```

### 6) 컨테이너 실행

```bash
docker run -e ORACLE_PASSWORD=pass -p 1521:1521 -d gvenzl/oracle-xe
docker ps
```

### 7) 로그확인

```bash
docker logs -f fervent_williamson // => 이름 확인 필수!!!!
```

### 8) 컨테이너 이름 변경

```bash
docker rename {현재컨테이너이름} {변경할이름}
```

### 9) sqlplus 터미널 연결 테스트
- 아이디는 system을 입력해주세요.
- 비밀번호는 pass를 입력해주세요.
```bash
docker exec -it oracle sqlplus
```

### 10) user를 생성

```bash
SQL> CREATE USER {사용할이름} IDENTIFIED BY {사용할비밀번호};
SQL> GRANT RESOURCE, CONNECT TO {사용할이름};
SQL> grant create session, create table, create procedure to {사용할이름};
SQL> ALTER USER {사용할이름} quota unlimited on USERS;
SQL> exit
```

### 11) SQL Developer 연결 테스트
- Name에는 원하는 이름을 입력해주시면 됩니다.
- 데이터베이스 유형은 Oracle입니다.
- 사용자 초기 이름은 system, 비밀번호는 pass로 설정하였습니다.
- 호스트 이름은 localhost입니다.
- 포트는 1521입니다.
- SID는 xe 입니다.
- 테스트를 누르면 상태에 성공이라고 뜨는 것을 확인할 수 있습니다.
- 아까 생성해줬던 사용자도 접속 추가
