---
title: 2. Next.js 프로젝트에 테스트 환경 설정하기
layout: default
grand_parent: SDD
parent: speckit
nav_order: 2
permalink: /sdd/speckit/lab02
# nav_exclude: true
# search_exclude: true
--- 
# Lab 02: Next.js 프로젝트에 테스트 환경 설정하기

## 🎯 학습 목표

이 실습에서는 Next.js 프로젝트에 테스트 환경을 구축하는 방법을 배웁니다:
- Vitest를 사용한 유닛/컴포넌트 테스트 환경 구축
- Playwright를 사용한 E2E 테스트 환경 구축
- 테스트 폴더 구조 설계
- 테스트 작성 및 실행

## 📋 사전 준비사항

- Node.js 설치
- Next.js 프로젝트가 준비되어 있어야 합니다
- 기본적인 React 및 TypeScript 지식

## 🚀 실습 단계

### 1단계: Vitest 및 관련 패키지 설치

유닛 테스트와 컴포넌트 테스트를 위한 패키지들을 설치합니다:

```bash
npm install -D vitest @vitejs/plugin-react @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

**설치되는 패키지 설명:**
- `vitest`: 빠른 테스트 러너
- `@vitejs/plugin-react`: React 컴포넌트 지원
- `@testing-library/react`: React 컴포넌트 테스트 유틸리티
- `@testing-library/jest-dom`: DOM 관련 매처(matcher) 제공
- `@testing-library/user-event`: 사용자 이벤트 시뮬레이션
- `jsdom`: 브라우저 환경 시뮬레이션

### 2단계: Playwright 설치

E2E 테스트를 위한 Playwright를 설치합니다:

```bash
npm install -D @playwright/test
```

브라우저 바이너리를 다운로드합니다:

```bash
npx playwright install
```

### 3단계: Vitest 설정 파일 생성

프로젝트 루트에 `vitest.config.ts` 파일을 생성합니다:

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
    include: ['tests/unit/**/*.{test,spec}.{js,ts,jsx,tsx}'],
    exclude: ['**/node_modules/**', '**/dist/**', 'tests/e2e/**'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '*.config.*',
        '.next/',
      ],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './'),
    },
  },
})
```

**주요 설정 설명:**
- `environment: 'jsdom'`: 브라우저 환경 시뮬레이션
- `globals: true`: describe, it, expect 등을 전역으로 사용
- `setupFiles`: 테스트 실행 전 로드되는 설정 파일
- `include/exclude`: 테스트 파일 패턴 지정

### 4단계: Playwright 설정 파일 생성

프로젝트 루트에 `playwright.config.ts` 파일을 생성합니다:

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

**주요 설정 설명:**
- `testDir`: E2E 테스트 파일 위치
- `webServer`: 테스트 전 자동으로 개발 서버 실행
- `projects`: 여러 브라우저에서 테스트 실행

### 5단계: 테스트 폴더 구조 생성

다음과 같은 폴더 구조를 생성합니다:

```
tests/
├── unit/          # 유닛/컴포넌트 테스트
├── component/     # 컴포넌트 테스트
├── integration/   # 통합 테스트
├── e2e/           # E2E 테스트(종단간 테스트)
└── setup.ts       # Vitest 설정
```

`tests/setup.ts` 파일을 생성합니다:

```typescript
import '@testing-library/jest-dom'
```

### 6단계: 예제 유닛 테스트 작성

`tests/unit/page.test.tsx` 파일을 생성합니다:

```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import Home from '@/app/page'

describe('Home Page', () => {
  it('renders the main heading', () => {
    render(<Home />)
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toBeInTheDocument()
    expect(heading).toHaveTextContent(/get started/i)
  })

  it('renders the Next.js logo', () => {
    render(<Home />)
    const logo = screen.getByAltText('Next.js logo')
    expect(logo).toBeInTheDocument()
  })

  it('contains links to templates and learning center', () => {
    render(<Home />)
    const templatesLink = screen.getByRole('link', { name: /templates/i })
    const learningLink = screen.getByRole('link', { name: /learning/i })
    
    expect(templatesLink).toBeInTheDocument()
    expect(learningLink).toBeInTheDocument()
  })
})
```

### 7단계: 예제 E2E 테스트 작성

`tests/e2e/home.spec.ts` 파일을 생성합니다:

```typescript
import { test, expect } from '@playwright/test'

test.describe('Home Page E2E', () => {
  test('should display the main heading and logo', async ({ page }) => {
    await page.goto('/')
    
    const logo = page.getByAltText('Next.js logo')
    await expect(logo).toBeVisible()
    
    const heading = page.getByRole('heading', { level: 1 })
    await expect(heading).toBeVisible()
    await expect(heading).toContainText('get started')
  })

  test('should have working links to templates and learning center', async ({ page }) => {
    await page.goto('/')
    
    const templatesLink = page.getByRole('link', { name: /templates/i })
    await expect(templatesLink).toBeVisible()
    await expect(templatesLink).toHaveAttribute('href', /vercel.com\/templates/)
    
    const learningLink = page.getByRole('link', { name: /learning/i })
    await expect(learningLink).toBeVisible()
    await expect(learningLink).toHaveAttribute('href', /nextjs.org\/learn/)
  })

  test('should have a deploy button', async ({ page }) => {
    await page.goto('/')
    
    const deployLink = page.getByRole('link', { name: /vercel logomark/i })
    await expect(deployLink).toBeVisible()
  })
})
```

### 8단계: package.json 스크립트 추가

`package.json` 파일의 `scripts` 섹션에 테스트 명령어를 추가합니다:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:report": "playwright show-report"
  }
}
```

## 🧪 테스트 실행하기

### 유닛 테스트 실행

```bash
# 기본 실행
npm test

# UI 모드 (인터랙티브)
npm run test:ui

# 커버리지 리포트 생성
npm run test:coverage
```

### E2E 테스트 실행

```bash
# 모든 브라우저에서 테스트
npm run test:e2e

# UI 모드 (인터랙티브)
npm run test:e2e:ui

# 테스트 결과 리포트 보기
npm run test:e2e:report
```

## 📝 주요 개념

### Vitest vs Jest
- **Vitest**: Vite 기반, 빠른 속도, 현대적인 기능
- **Jest**: 성숙한 에코시스템, 풍부한 플러그인

### Testing Library
- 사용자 관점에서 테스트 작성
- 구현 세부사항이 아닌 동작에 집중
- 접근성 고려한 쿼리 제공

### E2E vs 유닛 테스트
- **유닛 테스트**: 개별 컴포넌트/함수 검증, 빠른 피드백
- **E2E 테스트**: 전체 사용자 시나리오 검증, 실제 환경 테스트

## ✅ 체크리스트

- [ ] Vitest 및 관련 패키지 설치 완료
- [ ] Playwright 설치 및 브라우저 다운로드 완료
- [ ] vitest.config.ts 설정 파일 생성
- [ ] playwright.config.ts 설정 파일 생성
- [ ] tests 폴더 구조 생성 (unit, e2e)
- [ ] 예제 유닛 테스트 작성 및 실행
- [ ] 예제 E2E 테스트 작성 및 실행
- [ ] package.json 스크립트 추가

## 🔍 문제 해결

### 유닛 테스트가 실행되지 않는 경우
- `tests/setup.ts` 파일이 있는지 확인
- `vitest.config.ts`의 경로 설정 확인
- `jsdom` 패키지 설치 확인

### E2E 테스트가 실패하는 경우
- 개발 서버가 실행 중인지 확인 (`npm run dev`)
- `playwright.config.ts`의 `baseURL` 확인
- 브라우저가 설치되었는지 확인 (`npx playwright install`)

## 📚 추가 학습 자료

- [Vitest 공식 문서](https://vitest.dev)
- [Playwright 공식 문서](https://playwright.dev)
- [Testing Library 문서](https://testing-library.com/docs/react-testing-library/intro/)
- [Next.js Testing 가이드](https://nextjs.org/docs/testing)

## 💡 팁

- 테스트는 코드 작성과 동시에 진행하세요 (TDD)
- 의미 있는 테스트 이름을 사용하세요
- 테스트는 독립적이어야 합니다
- E2E 테스트는 중요한 사용자 흐름에 집중하세요
- 테스트 커버리지보다 테스트 품질이 중요합니다
