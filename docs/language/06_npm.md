---
title: npm
layout: default
parent: Language
nav_order: 7
permalink: /language/npm
# nav_exclude: true
# search_exclude: true
---

# npm(node package manager)
자바스크립트용 패키지 매니저, node 설치할 때 설치됨.  
[NPM 공식 사이트](https://www.npmjs.com/)

p : 인기도(popularity)   
q : 품질(quality)   
m : 유지보수(maintenance)  

## package.json 파일 만들기
작업폴더의 root에서 작업  
해당 경로에 node_modules폴더와 package.json파일이 생성된다.
```bash
npm init -y
```

## package.json에 포함된 의존성 패키지를 일괄 설치
package.json파일이 있는 경로에서 실행
```bash
npm install
npm i
```

## 특정 패키지 설치 시
-P : dependencies 목록에 추가(기본값)  
-D : devDependencies 목록에 추가  
-g : 패키지를 프로젝트 폴더가 아닌 시스템 node_modules 폴더에  

```bash
npm install -P express
```

## package.json의 구성 요소
<table>
<tr><td> 항목 </td><td> 설명 </td></tr> 
<tr><td> name </td><td> 필수, 패키지명. 214자 글자수 제한, 밑줄 또는 점으로 시작할 수 없음. 대문자 사용할수 없음. </td></tr>
<tr><td>  version </td><td> 필수, 패키지 버전 "1.0.0" [Major][Minor][Patch] </td></tr>
<tr><td>  description </td><td> npm에서 serch로 검색했을 때 나타나는 패키지 설명 </td></tr>
<tr><td>  main </td><td> 패키지의 진입점(entry point)이 되는 모듈의 ID. 패키지 root의 상대경로로 지정해야 한다. 지정하지 않은 경우 root폴더의 index.js로 기본값이 설정</td></tr>
<tr><td>  scripts </td><td> command의 alias(별칭)을 정의해 놓고 간단하게 호출할수 있다. </td></tr>
<tr><td>  keywords </td><td> description과 마찬가지로 npm에서 검색되었을 때 리스트에 표시되어 사람들이 패키지를 찾아내고 이해할수 있는데 도움을 준다. </td></tr>
<tr><td>  author </td><td> 배포자 </td></tr>
<tr><td> license </td><td> 배포한 패키지에 대해 어떤 권한과 제한 사항에 대해 명시 </td></tr>
<tr><td>  dependencies </td><td> 해당 패키지, 프로젝트가 어떤 외부 라이브러리에 의존성을 가지는지 명시 </td></tr>
<tr><td>  devDependencies </td><td> 개발시에만 필요한 의존 패키지들을 명시 </td></tr>
</table>

## 설치한 패키지 확인
```bash
npm ls
```

## 패키지 업데이트
```bash
npm update express
```

## 패키지 삭제
```bash
npm uninstall express
```

## node_modules의 위치를 알려줌
```bash
npm root
```

## 패키지에 오류가 있을경우 캐시삭제 후 재설치
```bash
npm cache clean --force
npm rebuild
```

## package.json의 scripts에 있는 start 명령어를 실행, 중지
```bash
npm start
npm stop
```