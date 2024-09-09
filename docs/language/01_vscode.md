---
title: VScode Setting
layout: default
parent: Language
nav_order: 1
permalink: /language/vscode
# nav_exclude: true
# search_exclude: true
---
# VScode Setting

## 1. VScode 단축키
### 기본 설정 단축키
줄 처음 : home  
줄 끝 : end  
줄 처음까지 블럭 : shift + home  
줄 끝까지 블럭 : shift + home  
파일의 처음 : Ctrl + home  
파일의 끝 : Ctrl + end  
파일의 처음까지 블록 : Ctrl + shift + home  
파일의 끝까지 블록 : Ctrl + shift + end  


라인 복사 : shift + alt + 방향키(위,아래)  
라인 삭제 : ctrl + shift + k  


다중선택 : 처음위치커서 두고,   
         ctrl + alt + 방향키(위,아래)  
         alt + 마우스클릭   
다중선택해제: esc  

한줄주석처리 : ctrl + /  
블록주석 : 블럭잡고 alt + shift + a  
범위펴기: Ctrl + Shift + [  
범위접기: Ctrl + Shift + ]  

### 단축키 추가
터미널 <-> 에디터 간 전환하기
1. ctrl + shift + p를 누르고 Open keyboard Shortcuts (JSON) 으로 들어가 설정한다. Default가 아니다. 

2. 아래와 같이 작성(ctrl + ; 으로 전환)

```json
// 키 바인딩을 이 파일에 넣어서 기본값 재정의
[
   // Place your key bindings in this file to override the defaultsauto[]
   {
      "key": "ctrl+;",
      "command": "terminal.focus",
      "when": "editorFocus"
   },
   {
      "key": "ctrl+;",
      "command": "workbench.action.focusActiveEditorGroup",
      "when": "terminalFocus"
   }
]
```

## 2. VScode Extension
### Material Icon Theme
파일 및 폴더 아이콘 테마

### Git Graph
git의 커밋내용을 그래프로 보기 편하게 표시

### Indent-rainbow
들여쓰기를 색상으로 표시

### Highlight Matching Tag
쌍이 되는 태그를 하이라이트로 표시

### Auto Rename Tag
여는 태그와 닫는 태그 이름을 동시에 변경

### htmltagwrap
감싸고자 하는 블록을 범위를 잡고 alt + w

### Live Server
새로고침 없이 자동으로 브라우저 화면을 업데이트

### Image preview
url에 마우스 올려놓으면 프리뷰 이미지를 볼수 있음.

### Prettier - Code formatter
코드 포맷터 - 정해진 코딩 스타일을 따르도록 자동으로 변환

### CSS Initial Value
css 속성 기본값을 보여주고 MDN사이트의 레퍼런스를 볼 수도 있다.

### CSS Peek
html파일에 css와 연결된 항목을 ctrl 키를 누른 상태에서 클릭하면 css파일에서 해당 항목을 찾아줌(ctrl + html 요소 클릭 -> css 파일로 이동)

### HTML CSS Support
html 파일에서 class에서 css 선택자 요소를 쓸때 자동 완성 기능을 지원

### HTML to CSS autocompletion
CSS 파일에서 HTML에서 사용한 속성이름의 자동 완성 기능을 지원

### HTML End Tag Labels
html 태그 코드가 길어질 경우 닫힌 태그가 어떤 구문에서 사용되었는지 알려준다. 해당 태그에 사용된 클래스 값을 표시

### Font Awesome Gallery
vscode에서 Font Awesome Gallery를 바로 검색

### Font Awesome Auto-complete & Preview
클래스 값으로 fa- 입력시 자동 완성기능 활성화

### px to rem & rpx & vw (cssrem)
px(픽셀)단위를 rem 등으로 변환(px<->rem alt+z)

### code runner
단축키를 사용하여 현재 표시중인 자바스크립트를 실행할 수 있다.  
windows : Ctrl + Alt + N  
mac : control + option + N  
-> Code-runner:Executor Map 에서 언어별 실행명령 수정가능  

### Tailwind CSS IntelliSense
Tailwind css 클래스명 자동 완성 기능 제공

### Headwind
Tailwind 클래스값 자동 정렬

### Thunder Client
api 요청을 생성하고 응답을 테스트

### MongoDB for VS Code
vscode에서 MongoDB에 접속해서 사용할 수 있도록 한다.