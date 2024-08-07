---
title: Emmet
layout: default
parent: Language
nav_order: 1
permalink: /language/emmet
# nav_exclude: true
# search_exclude: true
---

[Emmet](https://emmet.io/)  
[mdn(Mozilla Developer Network 의 약어)](https://developer.mozilla.org/ko/)

#### html 기본 생성
```html
#(항목 선택은 tab)
! or html 
```
#### 하위 요소 생성 : >
```css
nav > u l > li
```

#### 동급 요소 생성 : +
```css
div + p + bq
```

#### 반복 : *
```css
ul > li * 5
```

#### class : .
```css
li.item * 3
```

#### id : \#
```css
ul#menu > li.item * 3
```

#### 그룹 : ()
```css
.container > (header > nav > ul > li * 5 > a) + ( #content > section ) + footer
```

#### 속성 : []
```css
td[title="name" colspan="5"]
```

#### 텍스트 : {텍스트}
```css
a.button{Click Me}
```

#### 넘버링 : $
```css
ul.list > li.item $ * 5 > {$}
```
#### 의미없는 텍스트 생성(기본값 30개의 더미 텍스트로 이루어진 몇개의 문장 생성)
```css
div>lorem
ul.generic-list>lorem10.item$*4
```
