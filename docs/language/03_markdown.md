---
title: Markdown
layout: default
parent: Language
nav_order: 3
permalink: /language/md
# nav_exclude: true
# search_exclude: true
---


## readme.md 파일 사용
Markdown 문법으로 작성한다.  
Markdown은 텍스트 기반의 마크업언어로 2004년 존그루버에 의해 만들어졌으며 쉽게 쓰고 읽을 수 있으며 HTML로 변환이 가능하다.  특수기호와 문자를 이용한 매우 간단한 구조의 문법을 사용하여 웹에서도 보다 빠르게 컨텐츠를 작성하고 보다 직관적으로 인식할 수 있다.

### 제목
```
# title
## title
### title
#### title
##### title
###### title
```

### 소스코드
백틱(`) 3개를 사용하여 가능

> \`\`\`  
> 사이에 코드 작성  
> \`\`\`  

### 줄바꿈
빈칸 2개(스페이스바)

### 인용구문
```
> 인용구문 작성
```
> 인용구문 작성

### Badge(뱃지)
> 공식 로고 이름 , 색상 확인
> https://simpleicons.org/

방법 1
https://shields.io/ 에서 직접 작성

방법 2 
```
<img src="https://img.shields.io/badge/이름-색상코드?style=flat-square&logo=로고명&logoColor=로고색"/>
```
- 이름 : 뱃지에 쓸 이름(내용)
- 색상 : 16진수 RGB코드 (#은 제외하고)
- 로고명 : 아이콘 이름(https://simpleicons.org/ 확인)
- 로고색 : 로고의 색상

예시
```
<img src="https://img.shields.io/badge/shimseonjo-FFCA28?style=flat-square&logo=apple&logoColor=000000"/>
<img src="https://img.shields.io/badge/DOCKER-2496ED?style=flat&logo=Docker&logoColor=white"/>
```
<img src="https://img.shields.io/badge/shimseonjo-FFCA28?style=flat-square&logo=apple&logoColor=000000"/>
<img src="https://img.shields.io/badge/DOCKER-2496ED?style=flat&logo=Docker&logoColor=white"/>


### 링크
```
[표시내용](url)
[네이버](hhttps://www.naver.com/)
```
[네이버](hhttps://www.naver.com/)

### 이미지
```
# 사이즈 조절 기능은 없음
![이미지가 안보일때 표시할 글자](이미지 경로)

![git](https://git-scm.com/images/logo@2x.png)

# 사이즈 조절 img 태그를 이용
<img width="" height=""></img>
```
![git](https://git-scm.com/images/logo@2x.png)

### 수평선
```
***
---
```
***
---

### 강조
```
*single asterisks*
_single underscores_
**double asterisks**
__double underscores__
~~cancelline~~
```
*single asterisks*  
_single underscores_  
**double asterisks**  
__double underscores__  
~~cancelline~~  
