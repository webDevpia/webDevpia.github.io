---
title: Koyeb
layout: default
parent: Site
nav_order: 1
permalink: /site/koyeb
nav_exclude: true
search_exclude: true
---

# Koyeb으로 배포하기
## 1. github에 코드 올리기
코드를 github에 올린다.   
.env 파일과 node_modules 폴더는 제외한다.

## 2. Koyeb 회원가입하고 배포하기
Starter   
$0/월  

신용카드 없이 시작*  
- 1x 무료 웹 서비스
- 1x 무료 Postgres 데이터베이스(50시간)
- 웹 앱, API, 작업자 실행
- Git 푸시로 배포
- SSL 및 10개의 무료 사용자 정의 도메인
- 사용자 3명 포함

### 1. 해당 사이트로 접속하고 "GET STARTED - FREE" 클릭
![](/assets/img/koyeb/koyeb01.png)

### 2. "SIGN UP WITH GITHUB" 클릭  
![](/assets/img/koyeb/koyeb02.png)

### 3. github 계정으로 로그인  
![](/assets/img/koyeb/koyeb03.png)

### 4. "Authorize Koyeb" 클릭  
![](/assets/img/koyeb/koyeb04.png)

### 5. Organization 이름 입력 후 설문 내용 기입  
![](/assets/img/koyeb/koyeb05.png)

### 6. 가입완료 후 기본 화면으로 이동된다.
![](/assets/img/koyeb/koyeb06.png)

### 7. "Apps" 클릭하고, "Create App +" 버튼 클릭  
![](/assets/img/koyeb/koyeb07.png)

### 8. "GitHub" 선택  
![](/assets/img/koyeb/koyeb08.png)

### 9. "install GitHub App" 클릭  
![](/assets/img/koyeb/koyeb09.png)

### 10 "install" 클릭  
![](/assets/img/koyeb/koyeb10.png)

### 11. 배포할 repository 선택  
![](/assets/img/koyeb/koyeb11.png)

### 12. 브랜치 선택
![](/assets/img/koyeb/koyeb12.png)

### 13. app name 입력
![](/assets/img/koyeb/koyeb13.png)

### 14. "Build and deployment settings" 클릭하고 Run command 내용 입력
![](/assets/img/koyeb/koyeb14.png)

### 15. "Advanced" 클릭, 환경변수 등 필요한 내용 추가  
![](/assets/img/koyeb/koyeb15.png)

### 16. "Deploy" 버튼 클릭

배포가 진행되고 완료되면 service가 healthy 상태가 되면 성공.
![](/assets/img/koyeb/koyeb16.png)

### 17. Overview에서 Log를 확인해 본다.
![](/assets/img/koyeb/koyeb17.png)

![](/assets/img/koyeb/koyeb18.png)
![](/assets/img/koyeb/koyeb19.png)