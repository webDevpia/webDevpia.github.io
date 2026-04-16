---
title: Font Awesome
layout: default
parent: HTML
nav_order: 5
permalink: /language/html/fontawesome
# nav_exclude: true
# search_exclude: true
---

### 회원가입
[<svg xmlns="http://www.w3.org/2000/svg" height="16" width="14" viewBox="0 0 448 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M448 48V384c-63.1 22.5-82.3 32-119.5 32c-62.8 0-86.6-32-149.3-32c-20.6 0-36.6 3.6-51.2 8.2v-64c14.6-4.6 30.6-8.2 51.2-8.2c62.7 0 86.5 32 149.3 32c20.4 0 35.6-3 55.5-9.3v-208c-19.9 6.3-35.1 9.3-55.5 9.3c-62.8 0-86.6-32-149.3-32c-50.8 0-74.9 20.6-115.2 28.7V448c0 17.7-14.3 32-32 32s-32-14.3-32-32V64C0 46.3 14.3 32 32 32s32 14.3 32 32V76.7c40.3-8 64.4-28.7 115.2-28.7c62.7 0 86.5 32 149.3 32c37.1 0 56.4-9.5 119.5-32z"/></svg> 폰트어썸](https://fontawesome.com/)

### 무료 사용 가능한 타입
Classic Family 에서 Solid : __fa-solid__ or __fas__  
Brands Family 에서 Brands : __fa-brands__ or __fab__ 

### 사용방법
#### 1. cdn을 이용
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.0/css/all.min.css" integrity="sha512-10/jx2EXwxxWqCLX/hHth/vu2KY3jCF70dCQB8TSgNjbCVAC/8vai53GfMDrO2Emgwccf2pJqxct9ehpzG+MTw==" crossorigin="anonymous" referrerpolicy="no-referrer" />
```
#### 2. 직접 다운로드 받아서 이용
```html
<link rel="stylesheet" href="all.min.css"  />
<script src="all.min.js"></script>
```
#### 3. kit을 발급받아서 이용
```html
<script src="https://kit.fontawesome.com/개인키.js" crossorigin="anonymous"></script>
```
### html 문서에서 사용
__i__ 태그나 __span__ 태그를 이용


```html
<head>
<script src="https://kit.fontawesome.com/개인키.js" crossorigin="anonymous"></script>
</head>

<body>
  <!--  -->
  <i class="fa-brands fa-twitter"></i>
  <span class="fab fa-twitter"></span>
  
  <!-- Relative Sizing Class : browsers' default font-size 16px , 
       fa-2xs(0.625em 10px),fa-xs(0.75em 12px),fa-sm(0.875em 14px),fa-lg(1.25em 20px),fa-xl(1.5em 24px),fa-2xl(2em 32px) -->
  <i class="fa-solid fa-user fa-2xs"></i>
  
  <!-- Literal Sizing : fa-1x ~ fa-10x  fa-1x:1em fa-10x:10em -->
  <i class="fas fa-user fa-2xs"></i>

  <!-- color -->
  <span style="font-size: 3em; color: Tomato;">
    <i class="fa-solid fa-camera"></i>
  </span>
  
</body>
```
