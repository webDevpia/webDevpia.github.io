---
title: 05. 웹서버(Nginx)와 MySQL 설치
layout: default
parent: Cloud
nav_order: 5
permalink: /cloud/nginx-mysql
---


## 학습 목표

- Nginx 웹서버를 설치하고 브라우저에서 확인할 수 있다
- MySQL 데이터베이스를 설치하고 기본 설정을 완료할 수 있다

<a id="toc"></a>

## 진행 순서

1. [Nginx 웹서버 설치](#part1) - apt로 설치 및 상태 확인
2. [웹서버 동작 확인](#part2) - 브라우저에서 퍼블릭 IP 접속
3. [MySQL 설치](#part3) - apt로 MySQL 서버 설치
4. [MySQL 초기 설정](#part4) - 보안 마법사 실행 및 접속 테스트
5. [데이터베이스와 테이블 생성](#part5) - SQL 기본 명령어 실습
6. [정리](#part6) - 설치 확인 체크리스트 및 SQL 요약

---

# 05장. 웹서버(Nginx)와 MySQL 설치

<a id="part1"></a>

## 1️⃣ Nginx 웹서버 설치 [↑](#toc)

**Nginx(엔진엑스)**는 전 세계에서 가장 많이 사용되는 웹서버 소프트웨어 중 하나입니다.
브라우저가 요청을 보내면 서버에 저장된 HTML 파일을 찾아 응답합니다.

### 안내 데스크 비유

> 방문자(브라우저)가 건물(서버)에 들어오면,
> **Nginx는 안내 데스크** — 어떤 파일을 요청했는지 확인하고 적절한 문서를 찾아 전달합니다.

---

```bash
sudo apt update
sudo apt install nginx -y     # -y: "설치할까요?" 질문에 자동으로 Yes 응답
sudo systemctl status nginx   # 설치 후 실행 상태 확인
```

`apt install` 실행 시 여러 줄의 설치 로그가 출력됩니다. 완료되면 자동으로 Nginx가 시작됩니다.

`systemctl status nginx` 실행 결과에서 아래 내용이 보이면 성공입니다.

```
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2026-01-01 09:05:00 UTC; 10s ago
```

> `Active: active (running)` — 이 한 줄이 보이면 Nginx가 정상 실행 중입니다.

---

### Nginx 기본 파일 경로

설치 후 알아두면 유용한 경로입니다.

| 경로 | 설명 |
|------|------|
| `/var/www/html/` | 웹 파일을 저장하는 기본 폴더 (여기 있는 파일이 브라우저에 표시) |
| `/etc/nginx/nginx.conf` | Nginx 메인 설정 파일 |
| `/etc/nginx/sites-available/default` | 기본 사이트 설정 파일 |
| `/var/log/nginx/access.log` | 접속 기록 로그 |
| `/var/log/nginx/error.log` | 오류 로그 |

---

<a id="part2"></a>

## 2️⃣ 웹서버 동작 확인 [↑](#toc)

> "이 순간이 가장 신나는 순간입니다!"

### 브라우저에서 확인하기

1. AWS EC2 대시보드로 이동합니다.
2. 실행 중인 인스턴스를 클릭합니다.
3. **퍼블릭 IPv4 주소**를 복사합니다. (예: `43.200.xxx.xxx`)
4. 브라우저 주소창에 `http://퍼블릭IP`를 입력합니다.
5. **"Welcome to nginx!"** 페이지가 보이면 성공!

```
http://43.200.xxx.xxx
```

> ⚠️ **페이지가 안 보이면 체크리스트:**
>
> 1. **보안 그룹에 HTTP(80번 포트)가 열려 있는가?**
>    - EC2 > 보안 그룹 > 인바운드 규칙에 `HTTP / 80 / 0.0.0.0/0` 이 있어야 합니다.
> 2. **`http://`로 접속했는가?** (`https://`가 아닌 `http://`로!)
>    - HTTPS는 별도 인증서 설정이 필요합니다. 지금은 HTTP만 사용합니다.
> 3. **Nginx가 실행 중인가?**
>    ```bash
>    sudo systemctl status nginx
>    ```
>    `active (running)`이 아니면 `sudo systemctl start nginx`로 시작하세요.

---

<a id="part3"></a>

## 3️⃣ MySQL 설치 [↑](#toc)

**MySQL(마이에스큐엘)**은 전 세계에서 가장 널리 사용되는 오픈소스 관계형 데이터베이스(RDBMS)입니다.

### 데이터 창고 비유

> **MySQL은 데이터 창고** — 회원 정보, 상품 목록, 주문 내역 등
> 방대한 데이터를 체계적인 표(테이블) 형태로 저장하고, 필요할 때 빠르게 검색합니다.

| 개념 | 비유 | MySQL 용어 |
|------|------|-----------|
| 창고 전체 | 건물 | 데이터베이스 서버 |
| 창고 구역 | 방 | 데이터베이스 (Database) |
| 선반 | 철재 선반 | 테이블 (Table) |
| 선반 위 물건 | 박스 | 행 (Row / Record) |
| 박스 분류 기준 | 라벨 | 열 (Column / Field) |

---

```bash
sudo apt install mysql-server -y
sudo systemctl status mysql    # active (running) 확인
```

설치가 완료되면 MySQL 서버가 자동으로 시작됩니다.

```
● mysql.service - MySQL Community Server
     Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2026-01-01 09:15:00 UTC; 5s ago
```

---

<a id="part4"></a>

## 4️⃣ MySQL 초기 설정 [↑](#toc)

설치 직후에는 보안 설정이 되어 있지 않습니다. 보안 설정 마법사를 실행하여 기본 보안을 적용합니다.

```bash
# MySQL 보안 설정 마법사 실행
sudo mysql_secure_installation
```

마법사가 순서대로 질문합니다. 아래 안내에 따라 입력하세요.

| 질문 | 입력값 | 설명 |
|------|--------|------|
| Validate Password component? | `y` | 비밀번호 복잡도 검사 활성화 |
| Password validation policy | `0` | LOW (수업용으로 낮게 설정) |
| New password | `Cloud2026!` | 강사와 통일 (실무에서는 강력한 비밀번호 사용) |
| Re-enter new password | `Cloud2026!` | 동일하게 재입력 |
| Remove anonymous users? | `y` | 익명 사용자 제거 |
| Disallow root login remotely? | `y` | 외부 root 접속 차단 |
| Remove test database? | `y` | 테스트 DB 제거 |
| Reload privilege tables? | `y` | 변경사항 즉시 적용 |

모든 질문에 응답하면 `All done!` 메시지가 나타납니다.

---

### MySQL 접속 테스트

```bash
sudo mysql -u root -p
# 비밀번호 입력: Cloud2026!
```

아래와 같은 프롬프트가 나타나면 성공입니다.

```
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.xx-ubuntu Ubuntu

mysql>
```

> `mysql>` 프롬프트가 보이면 이제 SQL 명령을 입력할 수 있습니다.
> MySQL에서 나가려면 `EXIT;`를 입력하세요.

---

<a id="part5"></a>

## 5️⃣ 데이터베이스와 테이블 생성 [↑](#toc)

MySQL에 접속한 상태 (`mysql>` 프롬프트)에서 실행합니다.

### 데이터베이스 생성

```sql
-- 데이터베이스 생성 (우리 웹사이트용 저장소)
CREATE DATABASE mywebsite;
```

실행 결과:

```
Query OK, 1 row affected (0.01 sec)
```

```sql
-- 현재 존재하는 데이터베이스 목록 확인
SHOW DATABASES;
```

실행 결과:

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mywebsite          |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

방금 만든 `mywebsite`가 목록에 나타납니다.

---

### 데이터베이스 선택 및 테이블 생성

```sql
-- 작업할 데이터베이스 선택
USE mywebsite;
```

실행 결과:

```
Database changed
```

```sql
-- 방명록 테이블 생성
CREATE TABLE guestbook (
    id INT AUTO_INCREMENT PRIMARY KEY,   -- 자동 증가하는 고유 번호 (1, 2, 3 ...)
    name VARCHAR(100) NOT NULL,          -- 이름 (최대 100자, 비워둘 수 없음)
    message TEXT,                        -- 메시지 내용 (긴 텍스트)
    created_at TIMESTAMP DEFAULT NOW()   -- 작성 시간 (자동으로 현재 시각 기록)
);
```

실행 결과:

```
Query OK, 0 rows affected (0.03 sec)
```

---

### 데이터 입력

```sql
-- 테스트 데이터 입력 (INSERT: 새 행 추가)
INSERT INTO guestbook (name, message) VALUES ('심선조', '안녕하세요! 첫 번째 방명록입니다.');
INSERT INTO guestbook (name, message) VALUES ('홍길동', '클라우드 수업 재밌어요!');
```

실행 결과:

```
Query OK, 1 row affected (0.01 sec)
Query OK, 1 row affected (0.00 sec)
```

---

### 데이터 조회

```sql
-- 테이블의 모든 데이터 조회 (* 는 모든 열을 의미)
SELECT * FROM guestbook;
```

실행 결과:

```
+----+-----------+------------------------------------+---------------------+
| id | name      | message                            | created_at          |
+----+-----------+------------------------------------+---------------------+
|  1 | 심선조    | 안녕하세요! 첫 번째 방명록입니다.  | 2026-01-01 09:20:00 |
|  2 | 홍길동    | 클라우드 수업 재밌어요!            | 2026-01-01 09:20:01 |
+----+-----------+------------------------------------+---------------------+
2 rows in set (0.00 sec)
```

입력한 데이터가 정확하게 저장된 것을 확인할 수 있습니다.

---

### MySQL 종료

```sql
-- MySQL 접속 종료
EXIT;
```

실행 결과:

```
Bye
```

다시 리눅스 터미널 프롬프트 (`ubuntu@ip-xxx:~$`)로 돌아옵니다.

---

<a id="part6"></a>

## 6️⃣ 정리 [↑](#toc)

### 설치 확인 체크리스트

| 항목 | 확인 방법 | 정상 상태 |
|------|----------|----------|
| Nginx 설치 | `sudo systemctl status nginx` | `active (running)` |
| Nginx 동작 | 브라우저에서 `http://퍼블릭IP` | "Welcome to nginx!" 페이지 |
| MySQL 설치 | `sudo systemctl status mysql` | `active (running)` |
| MySQL 접속 | `sudo mysql -u root -p` | `mysql>` 프롬프트 |
| DB 생성 | `SHOW DATABASES;` | `mywebsite` 항목 존재 |
| 테이블 생성 | `SELECT * FROM guestbook;` | 2개 행 출력 |

---

### SQL 명령어 요약

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `CREATE DATABASE` | 데이터베이스 생성 | `CREATE DATABASE mywebsite;` |
| `SHOW DATABASES` | 데이터베이스 목록 | `SHOW DATABASES;` |
| `USE` | 데이터베이스 선택 | `USE mywebsite;` |
| `CREATE TABLE` | 테이블 생성 | `CREATE TABLE guestbook (...);` |
| `INSERT INTO` | 데이터 삽입 | `INSERT INTO guestbook (...) VALUES (...);` |
| `SELECT` | 데이터 조회 | `SELECT * FROM guestbook;` |
| `EXIT` | MySQL 종료 | `EXIT;` |

> SQL 명령어는 대소문자를 구분하지 않지만, 관례적으로 **키워드는 대문자**로 씁니다.
> 모든 SQL 명령은 **세미콜론(`;`)으로 끝납니다.**

---

### 다음 장 미리보기

06장에서는 지금까지 구축한 환경 위에 **직접 만든 HTML 페이지를 배포**합니다.
`nano`로 HTML을 편집하고, 브라우저를 새로고침하면 전 세계에서 접속 가능한 나만의 웹 페이지가 완성됩니다!

```bash
sudo nano /var/www/html/index.html
# 내용 작성 후 저장하면 즉시 반영됩니다.
```

그리고 수업 마지막에는 **반드시** AWS 리소스를 정리(Terminate)하여 과금을 방지합니다.
