---
title: React 기본설정
layout: default
grand_parent: Language
parent: React
nav_order: 1
has_children: false
permalink: /language/react/react_1
---

## 1. 기본설정

### 1.  node.js 설치

설치 후 버전 확인
```bash
node -v
npm -v
```

### 2. 프로젝트 생성
[vite+react+tailwindcss 프로젝트 생성](https://tailwindcss.com/docs/guides/vite#react)  

- vite로 리액트 프로젝트 생성
```bash
npm create vite@latest
```

- 워킹디렉토리로 이동하고 필요한 라이브러리 설치 후 실행
```bash
cd my-react-app
npm i
npm run dev
```

### 3. tailwind css 사용시 셋팅

- tailwind 설치 및 초기화

```bash
npm install tailwindcss @tailwindcss/vite
```

- vite.config.ts 파일 설정

```js{% raw %}
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
}){% endraw %}
```

- index.css에 @tailwindcss의 각 레이어에 대한 지시문을 파일에 추가

```css
@import "tailwindcss";
```

- 빌드 프로세스 시작

```bash
npm run dev
```

### 4. 프로젝트에서 Tailwind 사용

src/App.js
```js
import './App.css'
import CardBox from './01/CardBox'

function App() {
  return (
    <>
    <CardBox/> 
    </>
  )
}

export default App
```

src/01/CardBox.js
```js
function CardBox() {
  return (
    <>
      <div class="flex flex-col items-center gap-6 p-7 md:flex-row md:gap-8 rounded-2xl">
        <div>
          <img class="size-48 shadow-xl/30 rounded-md" alt="" src="src/assets/cover.png" />
        </div>
        <div class="flex flex-col gap-2 items-center md:items-start">
          <span class="text-2xl font-medium">Class Warfare</span>
          <span class="font-medium text-sky-500">The Anti-Patterns</span>
          <div class="flex gap-2 font-medium text-gray-400">
            <span>No. 4</span>
            <span>·</span>
            <span>2025</span>
          </div>
        </div>
      </div>
      </>
  )
}
export default CardBox
```

