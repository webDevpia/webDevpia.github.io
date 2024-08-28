---
title: spring
layout: default
parent: Language
nav_order: 13
permalink: /language/spring
# nav_exclude: true
# search_exclude: true
---

# 1. 환경설정
## 1. IntelliJ(인텔리제이) 롬복(Lombok) 설정

![](/assets/img/spring/spring001.png)

### 설치
File - Setting - Plugins 에서 lombok install  
설치가 완료되면 인텔리제이 재실행

### 설정
File - Setting - Compiler - annotation processors에서   
Enable annotation processing 활성화 - OK


## 2. IntelliJ(인텔리제이) Spring Boot DevTools 적용하기

### build.gradle 파일에
```
dependencies {
	developmentOnly 'org.springframework.boot:spring-boot-devtools'
}
```

File > Settings
Build, Exeution, Deployment > Compiler > Build project autiomaically 체크

File > Settings
Advanced Settings > Allow auto-make to start even if developed application is currently running 체크

