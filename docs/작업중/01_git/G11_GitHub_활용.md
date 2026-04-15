---
title: 11. GitHub 활용
layout: default
parent: Git (리뉴얼)
nav_order: 11
permalink: /git-new/github-features
---

{% raw %}

## 학습 목표

- GitHub Pages로 내 웹사이트를 무료로 배포할 수 있다
- Issues로 버그와 할 일을 체계적으로 관리할 수 있다
- README.md를 작성해 프로젝트의 첫인상을 만들 수 있다
- GitHub 프로필 페이지를 꾸밀 수 있다
- GitHub Actions가 무엇인지 개념을 이해할 수 있다

<a id="toc"></a>

## 진행 순서

1. [GitHub Pages](#pages) — 내 웹사이트를 무료로 호스팅
2. [GitHub Issues](#issues) — 할 일 목록 + 버그 신고
3. [README.md 작성](#readme) — 프로젝트의 첫인상
4. [GitHub 프로필 꾸미기](#profile) — 개발자 자기소개 페이지
5. [GitHub Actions 맛보기](#actions) — 자동화의 시작
6. [실습](#practice) — GitHub Pages로 자기소개 페이지 배포
7. [정리](#summary)

---

# 11장. GitHub 활용 — Pages, Issues, README

<a id="pages"></a>

## 1️⃣ GitHub Pages — 내 웹사이트를 무료로 호스팅 [↑](#toc)

> GitHub Pages는 "GitHub가 운영하는 무료 웹 호스팅 서비스"입니다.
> 내 리포지토리에 HTML 파일을 올리면, GitHub가 그것을 웹사이트로 만들어 줍니다.
> 도메인도, 서버 비용도 필요 없습니다.

### 사용자 사이트 만들기 (User Site)

사용자 사이트는 `username.github.io` 주소로 접속할 수 있는 개인 페이지입니다.
만드는 방법은 단순합니다.

**1단계 — 리포지토리 생성**

GitHub에서 새 리포지토리를 만들 때, 이름을 정확히 아래와 같이 지정합니다.

```
username.github.io
```

`username` 자리에 자신의 GitHub 아이디를 넣으세요.
예를 들어 GitHub 아이디가 `hong-gildong`이라면, 리포지토리 이름은 `hong-gildong.github.io`입니다.

> ⚠️ 이름이 정확히 일치해야 합니다. 대소문자도 확인하세요.

**2단계 — index.html 만들기**

로컬에서 리포지토리를 clone한 후, `index.html` 파일을 만듭니다.

```bash
git clone https://github.com/username/username.github.io
cd username.github.io
```

`index.html`을 만들고 내용을 작성합니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>내 첫 번째 GitHub Pages</title>
</head>
<body>
  <h1>안녕하세요!</h1>
  <p>GitHub Pages로 만든 제 페이지입니다.</p>
</body>
</html>
```

**3단계 — 커밋하고 push**

```bash
git add index.html
git commit -m "첫 번째 페이지 추가"
git push
```

> 💡 push 후 몇 분(보통 1~3분) 기다리면 `https://username.github.io`에서 사이트를 확인할 수 있습니다.
> 바로 보이지 않는다면 브라우저를 새로 고침하거나, 조금 더 기다려 보세요.

---

### 프로젝트 사이트 만들기 (Project Site)

사용자 사이트와 달리, 어떤 리포지토리든 GitHub Pages로 배포할 수 있습니다.
주소는 `https://username.github.io/리포지토리이름` 형태가 됩니다.

**설정 방법**

1. 리포지토리의 **Settings** 탭을 클릭합니다.
2. 왼쪽 메뉴에서 **Pages**를 선택합니다.
3. **Branch** 항목에서 배포할 브랜치(보통 `main`)를 선택합니다.
4. **Save**를 클릭합니다.

```
Settings → Pages → Branch: main → Save
```

> 💡 `docs` 폴더만 배포하고 싶다면, Branch 설정 옆의 폴더 선택에서 `/docs`를 고를 수 있습니다.

---

<a id="issues"></a>

## 2️⃣ GitHub Issues — 할 일 목록 + 버그 신고 [↑](#toc)

> Issues는 "프로젝트의 할 일 목록이자 대화창"입니다.
> 버그를 발견했을 때, 새 기능을 제안할 때, 팀원과 논의할 때 모두 사용합니다.
> 이메일이나 메신저 대신 Issues를 쓰면 대화 내용이 코드와 함께 남습니다.

### Issue 만들기

리포지토리의 **Issues** 탭 → **New issue** 버튼을 클릭합니다.

| 항목 | 설명 |
|------|------|
| Title | 무엇이 문제인지 한 줄로 요약 |
| Description | 상세 내용, 재현 방법, 스크린샷 등 |
| Labels | 분류 태그 (bug, enhancement, question 등) |
| Assignees | 이 이슈를 담당할 사람 지정 |
| Milestone | 어느 버전에서 해결할지 |

**예시 Issue 제목**:
- `로그인 버튼 클릭 시 오류 발생`
- `메인 페이지 반응형 레이아웃 추가 필요`
- `README에 설치 방법 설명 추가`

> ⚠️ Issue 제목은 구체적으로 씁니다. "버그 있음"보다 "Chrome에서 로그인 버튼 클릭 시 404 오류"가 훨씬 도움이 됩니다.

---

### Issue와 PR 연결하기

커밋 메시지나 PR 설명에 특별한 키워드를 넣으면, PR이 머지될 때 연결된 Issue가 자동으로 닫힙니다.

```
Closes #3
Fixes #7
Resolves #12
```

**예시**:

```bash
git commit -m "로그인 버튼 오류 수정 - Closes #3"
```

PR 설명에도 같은 방식으로 넣을 수 있습니다.

```
이 PR은 로그인 버튼 클릭 시 발생하는 404 오류를 수정합니다.

Closes #3
```

> 💡 이렇게 하면 PR이 머지되는 순간 Issue #3이 자동으로 닫힙니다.
> 팀원이 "이 PR이 어떤 문제를 해결하는지" 한눈에 알 수 있어 편리합니다.

---

### Issue 템플릿 (간단 소개)

팀 프로젝트에서는 Issue를 작성할 때 항상 같은 형식을 맞추고 싶을 때가 있습니다.
리포지토리에 Issue 템플릿을 만들어 두면, 누가 Issue를 생성해도 동일한 양식이 나타납니다.

```
Settings → Features → Issues → Set up templates
```

> 💡 혼자 작업할 때는 필요 없지만, 팀 프로젝트에서는 템플릿이 소통을 훨씬 매끄럽게 만들어 줍니다.

---

<a id="readme"></a>

## 3️⃣ README.md 작성 — 프로젝트의 첫인상 [↑](#toc)

> README는 "리포지토리의 표지"입니다.
> 도서관에서 책을 고를 때 표지와 목차를 먼저 보듯이,
> 개발자들은 README를 보고 "이 프로젝트를 쓸지 말지" 결정합니다.

### README에 담아야 할 것들

| 항목 | 설명 |
|------|------|
| 프로젝트 이름 | 무엇을 만들었는가 |
| 설명 | 이 프로젝트가 어떤 문제를 해결하는가 |
| 설치 방법 | 어떻게 실행하는가 |
| 사용 방법 | 어떻게 쓰는가 |
| 기여 방법 | 기여하고 싶은 사람은 어떻게 하면 되는가 |
| 라이선스 | 이 코드를 어떻게 써도 되는가 |

---

### Markdown 기초

README는 Markdown 형식으로 작성합니다.
몇 가지만 알아도 깔끔한 README를 만들 수 있습니다.

**제목 (Headings)**

```markdown
# 가장 큰 제목
## 두 번째 제목
### 세 번째 제목
```

**목록 (Lists)**

```markdown
- 항목 1
- 항목 2
  - 하위 항목

1. 첫 번째
2. 두 번째
```

**코드 블록 (Code blocks)**

````markdown
```bash
git clone https://github.com/username/project
cd project
```
````

**이미지 (Images)**

```markdown
![대체 텍스트](./img/screenshot.png)
```

**배지 (Badges)**

```markdown
![GitHub stars](https://img.shields.io/github/stars/username/repo)
```

> 💡 Shields.io (https://shields.io) 에서 다양한 배지를 무료로 만들 수 있습니다.
> "빌드 통과", "라이선스", "최신 버전" 같은 정보를 한눈에 보여줄 수 있습니다.

---

### 좋은 README 예시

```markdown
# 나의 포트폴리오 사이트

GitHub Pages로 호스팅되는 개인 포트폴리오 페이지입니다.

## 미리보기

![스크린샷](./img/preview.png)

## 실행 방법

1. 이 리포지토리를 clone합니다.
   ```bash
   git clone https://github.com/username/portfolio
   ```
2. `index.html`을 브라우저에서 엽니다.

## 사용 기술

- HTML5
- CSS3
- GitHub Pages

## 기여 방법

버그 신고나 개선 제안은 Issues를 이용해 주세요.

## 라이선스

MIT License
```

---

<a id="profile"></a>

## 4️⃣ GitHub 프로필 꾸미기 [↑](#toc)

> GitHub 프로필 페이지는 "개발자의 자기소개 페이지"입니다.
> 채용 담당자나 협업 상대가 여러분의 GitHub 주소를 열었을 때 가장 먼저 보이는 곳입니다.

### 프로필 README 만들기

GitHub에는 특별한 리포지토리가 있습니다.
`username`이라는 이름의 리포지토리를 만들면, 그 안의 README.md가 프로필 페이지에 표시됩니다.

**1단계 — 리포지토리 생성**

리포지토리 이름을 자신의 GitHub 아이디와 동일하게 만듭니다.
예를 들어 아이디가 `hong-gildong`이라면, 리포지토리 이름도 `hong-gildong`입니다.

> 💡 생성 화면에서 GitHub가 "이것은 특별한 리포지토리입니다"라는 안내 메시지를 보여줍니다.

**2단계 — README.md 작성**

```markdown
# 안녕하세요, 홍길동입니다 👋

비전공자 출신 예비 개발자입니다.
HTML, CSS, Python을 공부하고 있습니다.

## 현재 배우는 것들

- Git & GitHub
- 웹 기초 (HTML, CSS)
- Python 기초

## 연락처

- Email: hong@example.com
- Blog: https://hong-gildong.github.io
```

**3단계 — push**

```bash
git add README.md
git commit -m "프로필 README 추가"
git push
```

GitHub 프로필 페이지 (`https://github.com/username`)에 접속하면 README가 표시됩니다.

> 💡 프로필 README는 첫인상에 큰 영향을 줍니다.
> 자신이 무엇을 배우고 있는지, 어떤 사람인지 간결하게 적어 두세요.
> 완벽하지 않아도 됩니다. 있는 것이 없는 것보다 훨씬 낫습니다.

---

<a id="actions"></a>

## 5️⃣ GitHub Actions 맛보기 [↑](#toc)

> GitHub Actions는 "코드를 push하면 자동으로 무언가를 실행하는 로봇"입니다.
> 예를 들어, 코드를 push할 때마다 자동으로 테스트를 실행하거나,
> 특정 브랜치에 머지되면 자동으로 서버에 배포할 수 있습니다.
> 이것을 **CI/CD** (지속적 통합/지속적 배포)라고 부릅니다.

### 가장 간단한 예시

리포지토리에 `.github/workflows/hello.yml` 파일을 만들면 됩니다.

```yaml
name: Hello
on: [push]
jobs:
  say-hello:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello, GitHub Actions!"
```

이 파일을 push하면, GitHub은 코드를 받을 때마다 이 워크플로우를 자동으로 실행합니다.
리포지토리의 **Actions** 탭에서 실행 결과를 확인할 수 있습니다.

| 항목 | 설명 |
|------|------|
| `name` | 워크플로우의 이름 |
| `on: [push]` | push 이벤트가 발생할 때 실행 |
| `jobs` | 실행할 작업 목록 |
| `runs-on` | 어떤 환경에서 실행할지 (ubuntu, windows, macos) |
| `steps` | 작업 안에서 순서대로 실행할 단계들 |

> 💡 이것이 CI/CD의 시작입니다.
> 지금은 "push하면 자동으로 뭔가 실행된다"는 개념만 이해하면 충분합니다.
> 심화 과정에서 자동 테스트, 자동 배포 등을 자세히 배웁니다.

> ⚠️ Actions는 무료 플랜에서도 매달 일정 시간까지 무료로 사용할 수 있습니다.
> 개인 프로젝트 수준에서는 거의 비용이 발생하지 않습니다.

---

<a id="practice"></a>

## 6️⃣ 실습 — GitHub Pages로 자기소개 페이지 배포 [↑](#toc)

### 기본 실습

> 목표: `username.github.io` 주소에 자기소개 HTML 페이지를 배포합니다.

**1단계 — 리포지토리 생성**

GitHub에서 `username.github.io` 이름으로 새 리포지토리를 만듭니다.
(Public으로 설정해야 GitHub Pages가 활성화됩니다.)

**2단계 — 로컬에 clone**

```bash
git clone https://github.com/username/username.github.io
cd username.github.io
```

**3단계 — index.html 작성**

아래 내용을 참고하여 자신만의 자기소개 페이지를 만드세요.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>홍길동 - 포트폴리오</title>
  <style>
    body {
      font-family: 'Noto Sans KR', sans-serif;
      max-width: 600px;
      margin: 50px auto;
      padding: 0 20px;
      line-height: 1.8;
    }
    h1 { color: #2c3e50; }
    .skills { background: #f8f9fa; padding: 15px; border-radius: 8px; }
  </style>
</head>
<body>
  <h1>안녕하세요, 홍길동입니다</h1>
  <p>비전공자 출신 예비 개발자입니다. 현재 Git과 웹 개발을 공부하고 있습니다.</p>

  <div class="skills">
    <h2>배우고 있는 것들</h2>
    <ul>
      <li>Git &amp; GitHub</li>
      <li>HTML / CSS</li>
      <li>Python</li>
    </ul>
  </div>

  <h2>연락처</h2>
  <p>GitHub: <a href="https://github.com/username">@username</a></p>
</body>
</html>
```

**4단계 — 커밋 + push**

```bash
git add index.html
git commit -m "자기소개 페이지 추가"
git push
```

**5단계 — 확인**

2~3분 후 `https://username.github.io`에 접속해서 페이지가 보이는지 확인합니다.

> 💡 배포가 진행 중일 때는 리포지토리 → Settings → Pages에서 상태를 확인할 수 있습니다.
> 초록색 체크 표시가 나타나면 배포가 완료된 것입니다.

---

### 중급 실습

> 목표: 자기소개 페이지에 Issue를 연동하고, 개선 사항을 PR로 반영합니다.

1. `username.github.io` 리포지토리에 Issue를 하나 만듭니다.
   - 제목: `스킬 섹션에 링크 추가 필요`
   - 내용: "배우고 있는 기술 항목에 학습 자료 링크를 추가하면 좋겠다."

2. `feature/add-links` 브랜치를 만들어 `index.html`에 링크를 추가합니다.

   ```bash
   git switch -c feature/add-links
   ```

3. 변경사항을 커밋합니다.

   ```bash
   git commit -m "스킬 섹션에 학습 자료 링크 추가 - Closes #1"
   ```

4. push 후 PR을 만들고 머지합니다.

5. GitHub Pages에서 변경사항이 반영되었는지 확인합니다.

---

### 심화 실습

> 목표: GitHub Actions 워크플로우를 추가해 push할 때마다 배포 메시지를 출력합니다.

1. `.github/workflows/deploy-check.yml` 파일을 만듭니다.

   ```yaml
   name: Deploy Check
   on: [push]
   jobs:
     notify:
       runs-on: ubuntu-latest
       steps:
         - run: echo "사이트가 배포되었습니다. https://username.github.io 를 확인하세요!"
   ```

2. 커밋 후 push합니다.

   ```bash
   git add .github/workflows/deploy-check.yml
   git commit -m "배포 확인 워크플로우 추가"
   git push
   ```

3. 리포지토리의 **Actions** 탭에서 워크플로우가 실행되는 것을 확인합니다.

> ⚠️ `.github` 폴더는 숨겨진 폴더처럼 보이지만 GitHub에 정상적으로 push됩니다.
> 이 폴더는 GitHub 관련 설정 파일을 담는 표준 폴더입니다.

---

<a id="summary"></a>

## 7️⃣ 정리 [↑](#toc)

### 이 장에서 배운 것들

| 기능 | 핵심 내용 | 바로 써보기 |
|------|-----------|------------|
| GitHub Pages | 리포지토리 → 웹사이트 무료 배포 | `username.github.io` 리포지토리 생성 |
| GitHub Issues | 버그·할 일·논의를 코드와 함께 관리 | `Closes #번호`로 PR과 연결 |
| README.md | 프로젝트의 표지, 마크다운으로 작성 | 이름·설명·설치방법·사용방법 포함 |
| 프로필 README | GitHub 프로필에 표시되는 자기소개 | `username/username` 리포지토리 생성 |
| GitHub Actions | push 등 이벤트에 반응하는 자동화 | `.github/workflows/*.yml` 파일 생성 |

### 자주 쓰는 Issue 키워드

```
Closes #번호    → PR 머지 시 Issue 자동 닫힘
Fixes #번호     → 버그 수정 Issue에 주로 사용
Resolves #번호  → 일반적인 Issue 해결
```

---

> 💡 **마무리**: GitHub의 다양한 기능을 활용할 수 있게 되었습니다.
> 이제 코드를 작성하고, 버전을 관리하고, 웹에 배포하고, 팀원과 소통하는 모든 흐름을 GitHub 안에서 처리할 수 있습니다.
> 마지막 장에서는 지금까지 배운 모든 것을 합쳐 실전 팀 워크플로우를 시뮬레이션합니다.

{% endraw %}
