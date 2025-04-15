---
title: Ollama
layout: default
parent: LLM
nav_order: 1
permalink: /llm/ollama
# nav_exclude: true
# search_exclude: true
--- 
# Ollama

## Ollama 설치
[Ollama](https://ollama.com/)

### 1. 다운로드 클릭
![](./img/ollama/ollama001.png)

### 2. 운영체제에 맞춰 다운로드
![](./img/ollama/ollama002.png)

### 3. 설치 후 터미널에서 설치 확인 후, 모델 실행
#### 설치확인
```bash
ollama serve
```
웹브라우저에서 127.0.0.1:11434 접속해서  Ollama is running 나오면 실행중임.



```bash
ollama list
ollama run llama3.2
```
![](./img/ollama/ollama003.png)
