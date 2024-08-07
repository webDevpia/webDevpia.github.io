---
title: Tailwind
layout: default
parent: Language
# nav_order: 1
# permalink: /language/emmet
# nav_exclude: true
# search_exclude: true
---

[Tailwind CSS](https://tailwindcss.com/)

##  vscode extensions 설치
- Tailwind CSS IntelliSense
- Headwind

## CDN 사용
```html
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  <h1 class="text-3xl font-bold underline">
    Hello world!
  </h1>
</body>
</html>
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <title>Document</title>
</head>
<body>
  <nav class="flex p-3 bg-gray-800 justyfy-start">
    <img class="w-10 px-1" src="icon.png">
    <a class="p-3 text-gray-300" href="#">Team</a>
    <a class="p-3 text-gray-300" href="#">Project</a>
    <a class="p-3 text-gray-300" href="#">Calendar</a>
  </nav>
</body>
</html>
```

## Tailwind CLI
### node.js 설치
[Node.js](https://nodejs.org/en)
```bash
node -v
npm -v
```

### 작업폴더 생성 후, 폴더안에 package.json 파일 생성
```bash
mkdir project
cd project

npm init -y
```

### tailwindcss 설치 및 설정파일 생성

```bash
# 관리자 권한 필요 시 sudo
npm install -D tailwindcss
npx tailwindcss init 
# npx tailwindcss init --full  전체 설정내용 확인시
```
tailwind.config.js  파일 생성됨   

### tailwind.config.js  파일에 모든 템플릿 파일에 대한 경로 추가

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 기본 css file 작성

```css
<!-- src/input.css -->
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### package.json에 명령어 등록

```js
  "scripts": {
    "build": "tailwindcss -i ./src/input.css -o ./src/output.css",
    "watch": "tailwindcss -i ./src/input.css -o ./src/output.css --watch"
  },
```

```bash
npm run build
npm run watch
```
아직 사용한 내용이 없으므로  
warn - No utility classes were detected in your source files.라고 뜬다.
/src/output.css파일은 생성된 것을 확인할 수 있다.

### html파일에 적용하여 확인하기
내용이 추가된 output.css를 이용하여 적용된 스타일을 확인
```html
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="output.css" rel="stylesheet">
</head>
<body>
  <h1 class="font-bold underline text-mammoth">
    Hello world!
  </h1>
</body>
</html>
```

### tailwind.config.js  파일에 새로운 설정 추가

```js
<!-- tailwind.config.js  -->
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    screens:{
      sm: '480px', // 480px~767px
      md: '768px',
      lg: '976px',
      xl: '1440px'
    },
    extend: {
      colors: {
        brightRed: 'hsl(12, 88%, 59%)',
        brightRedLight: 'hsl(12, 88%, 69%)',
        brightRedSupLight: 'hsl(12, 88%, 95%)',
        darkBlue: 'hsl(228, 39%, 23%)',
        darkGrayishBlue: 'hsl(227, 12%, 61%)',
        veryDarkBlue: 'hsl(233, 12%, 13%)',
        veryPaleRed: 'hsl(13, 100%, 96%)',
        veryLightGray: 'hsl(0, 0%, 98%)',
      },
    },
  },
  plugins: [],
}
```
###  input.css에 추가후 html 적용
```css
.card{
  @apply bg-brightRedSupLight rounded
}
```

```html
  <div class="card" >card</div>
```