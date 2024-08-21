---
title: mac 셋팅
author: shimseonjo
category: Doc
layout: post
permalink: /mac_setting
nav_exclude: true
search_exclude: true
---
## finder 에서 숨긴 파일 확인하기
cmd + shift + . (토글방식으로 동작)

## git 설치하기
[Homebrew](https://brew.sh/) 설치하기
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 버전확인 
brew -version

# 오류 발생 시 path 설정 추가해야 한다. 
zsh: command not found: brew

# zshrc에 homebrew path 추가
echo 'export PATH=/opt/homebrew/bin:$PATH' >> ~/.zshrc

# zshrc 반영
source ~/.zshrc

# git 설치
brew install git
```
