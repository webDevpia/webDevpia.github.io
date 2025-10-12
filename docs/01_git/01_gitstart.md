---
title: Git & GitHub
layout: default
parent: Git
# nav_order: 2
permalink: /gitStart
# nav_exclude: true
# search_exclude: true
---
# Git & GitHub
CLI 방식으로 진행  
Command Line Interface(CLI)는 터미널 창에 명령을 직접 입력해서 사용하는 방식을 말함.  

## 1. git 시작하기

### 1) git 프로그램 설치(windows)
[git 다운로드](https://git-scm.com/)

### git 설치시 체크항목 

##### 1) git에서 사용할 기본 편집기 선택
Choosing the default editer used by Git 에서  
**[Use Visual Studio Code as Git's default editor]선택**  
기본값으로 Vim이 선택되어 있음.  

##### 2) 기본 브랜치의 이름 변경
Adjusting the name of the initial branch in new repositories에서   
**[Override the default branch anme for new repositories]**  
의 내용을 'main'으로 변경한다.

![](./img/git/git_001.png)

![](./img/git/git_002.png)

![](./img/git/git_003.png)

![](./img/git/git_004.png)

![](./img/git/git_005.png)

![](./img/git/git_006.png)

![](./img/git/git_007.png)

![](./img/git/git_008.png)

![](./img/git/git_009.png)

![](./img/git/git_010.png)

### 2) git 프로그램 설치(mac)

#### HomeBrew(미설치시 설치)
[Homebrew](https://brew.sh/ko/)
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```sh
brew install git
```

### 설치 후 버전 확인  

```
git -v
git --version
```

## 2. github 회원가입
- 가입 **아이디** , **이메일** 확인  
[github 사이트](https://github.com/)

## 3. git 작업순서

### 1) git init으로 초기화했을때 
![](./img/git/git_3_1.png)

### 2) 스테이지에 추가
![](./img/git/git_3_2.png)

### 3) 커밋
![](./img/git/git_3_3.png)

## 4. git으로 소스 관리 
### 1) 로컬 컴퓨터에서 처음으로 소스코드를 작성하고 github의 리모트 저장소와 연결할 경우
```bash
## 로컬 컴퓨터에 gitbash에서

# 먼저 작업디렉토리로 이동(경로 꼭 확인!!!)
cd 작업디렉토리경로

# git 초기화
git init

# git 사용자계정 및 이메일 등록
git config user.name <github-name>
git config user.email <github 등록 email>

# 설정정보 확인하고 user.name user.email 항목이 등록되어 있는지 확인
git config list

# 늘 git의 현재 상태를 확인하면서 작업한다.
git status

# 스테이지 올림
git add .

# 저장소에 저장
git commit -m "first commit"

# 커밋 내용을 확인
git log    (기본화면으로 돌아갈려면 q)
#-----------------------------------------
## 웹브라우저 github사이트에 로그인 후 작업
# 리파지토리생성 - 리파지토리 이름만 입력하고 만든다. 

#-----------------------------------------
## 로컬 컴퓨터에 gitbash에서
# 리모트 등록정보 확인
git remote -v

# 리모트 등록
git remote add origin 리파지토리주소

# 리모트 리파지토리로 데이터 올리기
git push -u origin main
```

기타 설정 및 필요한 명령어
```bash
# 전역 설정정보만 확인해 볼 경우
git config --global --list

# 전역으로 설정
git config --global user.name <github-name>
git config --global user.email <github 등록 email>

# 설정된 계정 정보 삭제해야 할 경우
# global
git config --unset --global user.name
git config --unset --global user.email

# local
git config --unset user.name
git config --unset user.email

# Remote 리파지토리 설정 삭제
git remote rm 리모트이름

# vscode를 기본 에디터로 설정
# --wait 에디터를 열어서 사용하는동안 터미널에서 대기
# --disable-extensions : VS Code 실행 시 모든 확장 기능을 비활성화함
git config --global core.editor "code --wait --disable-extensions"


# 운영체제별 줄바꿈 방식
# Windows: CRLF (\r\n) 사용
# Linux/macOS: LF (\n) 사용

git config --global core.autocrlf true
git config --global core.autocrlf input


# 브랜치명 초기값 변경
git config --global init.defaultBranch main  

# 현재 브랜치명 수정
git branch -M main

# 스테이징과 커밋 한꺼번에
git commit -am "브랜치에서 작업완료1"

# 방금 커밋한 메시지를 수정하려면
git commit --amend "커밋 메시지 수정"
```
### 2) github에 저장소에 작업하던 소스 코드가 있고 로컬 컴퓨터에 처음 받을 경우

```bash
# 현재 경로에 리파지토리 이름의 폴더를 생성하고 그 밑에 소스 받음.
git clone 리파지토리주소

# 현재 경로에 소스 받음.
git clone 리파지토리주소 .

# git 사용자계정 및 이메일 등록
git config user.name <github-name>
git config user.email <github 등록 email>

# 코딩 작업진행후
git add .
git commit -m "커밋메시지"
git push
```

### 3) 로컬에 git으로 관리하고 있는 경우

```bash
git pull origin main

# 코딩 작업진행후
git add .
git commit -m "커밋메시지"
git push

```


### 4) 기본적으로 알아둬야할 리눅스 명령어

```bash

# print working directory
pwd

# 파일및 디렉토리 목록 확인
ls -al

# 터미널 정리
clear

# 상위 디렉토리 이동
cd ..

# 하위 디렉토리 이동
cd 하위디렉토리명

# 홈 디렉토리 이동
cd ~

# 디렉토리 생성
mkdir test

# 디렉토리 삭제(-r 하위디렉토리 및 파일)

rm -rf test
```

## 4. branch

```
# 브랜치 목록보기
git branch

# 브랜치 생성
git branch test01

# 브랜치 이동
git switch test01

# 브랜치에서 작업 후 완료
git add .
git commit -m "브랜치에서 작업완료"

# 커밋 내용확인
git log --graph 
git log --oneline --graph 

```

![git](./img/git/git_10_1.png)

```
# 브랜치 병합(main에서 작업해야함)
git merge 브랜치명

# 충돌내용 처리 후, 커밋까지 처리 
git add .
git commit -m "test01 병합"

# 브랜치 충돌 - 각각 다른 브랜치에서 같은 파일 편집했을 경우
# git merge -> 충돌내용 수정 후 -> 다시 add, commit

# 이후 test01 브랜치 필요없으면 삭제
git branch -d 브랜치명

# 삭제후 복구
git branch 브랜치명 커밋값(ffa3169)

```
![git](./img/git/git_10_2.png)


```
# github에 개인 작업 브랜치 올리기
git push origin test01

# github에 개인 작업 브랜치 지우기
git push origin --delete test01
```

## 5. .gitignore 파일
작업 디렉토리 최상위에 위치하게 한다.  
.gitignore 파일을 작성하고, 제외하고자 하는 파일에 대한 내용을 기재한다.
- 경로는 상관없이 특정파일 제외하기
  > filename.txt  

- 현재 경로에 있는 파일만 제거
  > /filename.txt  

- 특정 폴더에 있는 파일 제외
  > /폴더명/  

- 특정 경로의 특정 파일 제외
  > /폴더명/filename.txt  

- 특정 경로 아래 특정 파일 제외
  > /폴더명/**/filename.txt
 
- 특정 확장자를 가진 파일 제거
  > *.png

- 예외
  > !filename.txt

    ```
    # git의 캐시값 때문에 적용이 안될 수 있다
    # 캐시 삭제하고 진행
    git rm -r --cached .
    git add .
    git commit -m "캐시 삭제"
    ```


## 6. reset

```bash
git log
git log --oneline

git reset --soft 커밋아이디

# 스테이지에 올라온 정보 제거
git restore --stated .

# 워킹 디렉토리에 있는 정보 제거
git restore .

// github와 로컬 컴퓨터 내용이 일치하지 않을 경우 로컬 컴퓨터 내용으로 push 함.
git push -f           
```

옵션  
--soft: 커밋을 취소하지만 스테이징 영역에는 그대로 남겨둡니다.  
워킹 디렉토리의 변경 사항은 그대로 유지됩니다.  
스테이징 영역의 변경 사항은 그대로 유지됩니다.  
커밋 기록은 변경되지 않습니다.  

--mixed: 커밋을 취소하고 스테이징 영역을 비웁니다.  
워킹 디렉토리의 변경 사항은 그대로 유지됩니다.  
스테이징 영역은 비워집니다.  
커밋 기록은 변경되지 않습니다.  

--hard: 커밋을 취소하고 스테이징 영역과 워킹 디렉토리를 모두 이전 상태로 되돌립니다.  
워킹 디렉토리의 변경 사항은 모두 삭제됩니다.  
스테이징 영역은 비워집니다.  
커밋 기록은 변경됩니다.  

<b>github push 이전에 되돌리기</b>
![git](./img/git/git_6_1.png)
![git](./img/git/git_6_3.png)
![git](./img/git/git_6_2.png)

<b>github push 이후에 되돌리기</b>
![git](./img/git/git_6_4.png)
![git](./img/git/git_6_5.png)
![git](./img/git/git_6_7.png)
![git](./img/git/git_6_6.png)

## 7. reflog
로컬 저장소에서  HEAD의 업데이트 기록을 확인
```bash
git reflog

git reflog "branch name"
```

## 8. revert
```
git revert [되돌리고 싶은 commit의 7자리까지]

# commit A -> commit B -> commit C 라면 
# 역순 commit C -> commit B -> commit A순으로 revert

# revert한 이력이 다 개별적으로 남은 위의 경우 3개의 커밋이 더 생성됨

# 이때 --no-commit 옵션을 주면 커밋은 하나만 생성되지만 명령어는 3번에 걸쳐 작성

# 한번에 명령으로 3단계를 취소하고 싶다면 HEAD~3
git revert --no-commit HEAD~3 #3단계를 취소함

# 충돌에 대한 처리는 해야함.

# 충돌 처리후 계속진행하거나 
git revert --continue

# 중단
git revert --abort

# revert 후 commit하고 push하면 된다.

# 단순히 커밋 메시지를 수정하거나 할 경우는 
# --amend 옵션을 활용한다.
# 기존의 마지막 커밋을 수정하기 때문에 커밋의 해시 값이 변경
# 만약 이 커밋이 다른 사람과 공유된 상태라면, 
# 그 커밋을 수정하는 것은 히스토리의 일관성을 깨뜨릴 수 있어 충돌을 유발할 수 있다. 
# 따라서 로컬에서만 작업 중이거나, 아직 리모트로 푸시하지 않은 커밋에서 사용하는 것이 안전.
git commit --amend -m "메시지 수정내용기재"
```


## 13. 협업하기
github의 공개 저장소는 주소만 알면 누구나 접속하여 소스를 확인하고 내려받을 수 있다.  
하지만 소스를 수정하고 commit, push는 공동작업자에 추가해줘야 한다.  

### 1) 팀장 : github 리파지토리 생성
리파지토리를 이름을 입력하고, Add a README file 항목에 체크, Add .gitignore는 python을 선택하여 생성해주자.
![git](./img/git/git_13_01.png)

생성된 리파지토리를 확인한다.
![git](./img/git/git_13_02.png)

### 2) 팀장 : 팀원 초대
Settings -> Access -> Collaborators 를 선택하고, Add people 버튼을 클릭한다.
![git](./img/git/git_13_03.png)

추가할 팀원의 아이디를 검색하고 선택한다.
![git](./img/git/git_13_04.png)

Add XXX to this repository 버튼을 클릭한다.
![git](./img/git/git_13_05.png)

### 3) 팀원 : 확인메일 수락처리
github에 등록된 이메일 계정으로 로그인 후 메일을 확인하고 'View invitation' 버튼을 클릭한다.
![git](./img/git/git_13_06.png)

'Accept invitation' 버튼을 클릭한다.
![git](./img/git/git_13_07.png)

팀장의 리파지토리 사이트로 이동된다.
![git](./img/git/git_13_08.png)

### 4) 팀장, 팀원 : github 리파지토리 clone
팀장의 리파지토리 사이트의 '<>Code'를 클릭하고 url 주소를 복사한다.
![git](./img/git/git_13_10.png)

vscode의 EXPLORER 탭에서 'Clone Repository' 버튼을 클릭하고, 주소입력란이 나타나면 url 주소를 붙여넣기한다.
![git](./img/git/git_13_11_w.png)

github의 리파지토리를 어디로 복사할지 경로를 선택한다. 선택한 경로 밑으로 리파지토리 이름의 폴더가 생성된다.
![git](./img/git/git_13_12_w.png)

![git](./img/git/git_13_13_w.png)

### 5) 팀장, 팀원 : 작업 후 push 전에 반드시 변경사항 가져와서(pull) 병합한 후 push 
사용자1 : test1.txt 파일 작업 후, 변경 사항을 내려받고(pull) add, commit, push
![git](./img/git/git_13_14.png)

사용자2 : test2.txt 파일 작업 후, 변경 사항을 내려받고(pull) add, commit, push
![git](./img/git/git_13_15.png)

사용자2 : 사용자1이 작성했던 test1.txt의 내용을 수정하고, pull, add, commit, push
![git](./img/git/git_13_16.png)

사용자1 : test1.txt의 내용을 수정하고, pull, add, commit
![git](./img/git/git_13_17.png)

![git](./img/git/git_13_18.png)

![git](./img/git/git_13_19.png)

![git](./img/git/git_13_20.png)
![git](./img/git/git_13_21.png)

![git](./img/git/git_13_22.png)
