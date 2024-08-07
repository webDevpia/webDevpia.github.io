---
title: Git & GitHub
layout: default
parent: Git
# nav_order: 2
# permalink: /git/GitStart
---
# Git & GitHub

## 1. git 시작하기
- 다운로드 :  https://git-scm.com/downloads
> windows에서 GitHub에 한글 깨질때
> - cmd"명령프롬프트"> chcp 65001  

#### git default branch명 수정  

```
# git 버전 확인 2.28.0 이상일때 기본 브랜치 변경
git version

# default branch 수정
git config --global init.defaultBranch main

# 혹은 전역설정파일을 수정
code ~/.gitconfig

#  [init]
#      defaultBranch = main

# 현재 사용하는 branch 이름만 수정
git branch -m main
```

## 2. github 회원가입
- 아이디,이메일 체크

## 3. git 작업순서
![git](/assets/img/git/git_3_1.png)
![git](/assets/img/git/git_3_2.png)

## 4. git 환경설정
```
# 설정정보 확인
git config --list
git config -l

# 전역으로 설정
git config --global user.name <github-name>
git config --global user.email <github 등록 email>

# Repository마다 다른 사용자 계정 사용
git config --local user.name <github-name>
git config --local user.email <github 등록 email>

# 설정된 계정 정보 삭제
# global
git config --unset --global user.name
git config --unset --global user.email

# local
git config --unset user.name
git config --unset user.email

# vscode를 기본 에디터로 설정
git config --global core.editor "code --wait --disable-extensions"
```

## 5. 로컬 저장소 만들고 github를 리모트 저장소로 등록하기
```
# 작업디렉토리로 위치 이동
cd <작업디렉토리>

# 초기화(.git 폴더 생생)
git init

# 파일 작성 후 스테이지에 추가
git add .

# 커밋 작업(메시지 필수)
git commit -m "first commit"

# github의 리파지토리 생성 후 원격저장소로 등록
# git-remote-url
# https://github.com/<사용자이름>/<저장소명>.git

git remote add origin <git-remote-url>

# remote 등록여부 확인
git remote -v 

# remote 제거
git remote rm origin

# -u 옵션은 처음 한번만 사용함
git push -u origin main

# 커밋 내역을 확인(옵션 --graph --oneline )
git log

# git 상태 확인
git status
```

## 6. git clone 
이미 github 리파지토리가 있고, 내컴퓨터로 코드 전체 복사 할 경우  

```
# 현재 위치에 리파지토리 이름의 폴더를 만들고 파일을 가져온다
git clone <git-remote-url>

# <디렉토리>위치에 파일을 가져온다.
git clone <git-remote-url> <디렉토리>
```


## 7. git pull 
내 컴퓨터로 github쪽 변경 내용만 내려받을 경우 
github의 최신 변경내용을 내려 받고 수정 작업을 한다

```
git pull
# 파일 수정 작업 진행
git add .
git commit -m "커밋 메시지"
git push
```

## 8. .gitignore 파일
작업 디렉토리 최상위에 위치하게 한다.  
.gitignore 파일을 작성하고, 제외하고자 하는 파일에 대한 내용을 기재한다.
- 경로는 상관없이 특정파일 제외하기
  > filename.txt  

- 현재 경로에 있는 파일만 제거
  > /filename.txt  

- 특정 폴더에 있는 파일 제외
  > 폴더명/  

- 특정 경로의 특정 파일 제외
  > 폴더명/filename.txt  

- 특정 경로 아래 특정 파일 제외
  > 폴더명/**/filename.txt
 
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


## 10. reset
```bash
git log
git log --oneline
git reset --soft 커밋아이디

// 스테이지에 올리지 않은 파일 정리
git clean -f     

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
![git](/img/git/git_6_1.png)
![git](/img/git/git_6_3.png)
![git](/img/git/git_6_2.png)

<b>github push 이후에 되돌리기</b>
![git](/img/git/git_6_4.png)
![git](/img/git/git_6_5.png)
![git](/img/git/git_6_7.png)
![git](/img/git/git_6_6.png)

## 11. reflog
로컬 저장소에서  HEAD의 업데이트 기록을 확인
```bash
git reflog

git reflog "branch name"
```

## 12. revert
```
git revert [되돌리고 싶은 commit의 해시값 6자기까지]

# commit A -> commit B -> commit C 라면 
# 역순 commit C -> commit B -> commit A순으로 revert

# revert한 이력이 다 개별적으로 남은 위의 경우 3개의 커밋이 더 생성됨
# 이때 --no-commit 옵션을 주면 커밋은 하나만 생성되지만 명령어는 3번에 걸쳐 작성

# 한번에 명령으로 3단계를 취소하고 싶다면 HEAD~3
git revert --no-commit HEAD~3 #3단계를 취소함

# revert 후 commit하고 push하면 된다.
```

## 13. branch
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
git log --graph --all
git log --oneline --graph --all

```

![git](/img/git/git_10_1.png)

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
![git](/img/git/git_10_2.png)


## 14. 협업하기
github의 공개 저장소는 주소만 알면 누구나 접속하여 소스를 확인하고 내려받을 수 있다.  
하지만 소스를 수정하고 commit, push는 공동작업자에 추가해줘야 한다.  

### 1. 팀장 : github 리파지토리 생성
리파지토리를 이름을 입력하고, Add a README file 항목에 체크, Add .gitignore는 python을 선택하여 생성해주자.
![git](/img/git/git_13_01.png)

생성된 리파지토리를 확인한다.
![git](/img/git/git_13_02.png)

### 2. 팀장 : 팀원 초대
Settings -> Access -> Collaborators 를 선택하고, Add people 버튼을 클릭한다.
![git](/img/git/git_13_03.png)

추가할 팀원의 아이디를 검색하고 선택한다.
![git](/img/git/git_13_04.png)

Add XXX to this repository 버튼을 클릭한다.
![git](/img/git/git_13_05.png)

### 3. 팀원 : 확인메일 수락처리
github에 등록된 이메일 계정으로 로그인 후 메일을 확인하고 'View invitation' 버튼을 클릭한다.
![git](/img/git/git_13_06.png)

'Accept invitation' 버튼을 클릭한다.
![git](/img/git/git_13_07.png)

팀장의 리파지토리 사이트로 이동된다.
![git](/img/git/git_13_08.png)

### 4. 팀장, 팀원 : github 리파지토리 clone
팀장의 리파지토리 사이트의 '<>Code'를 클릭하고 url 주소를 복사한다.
![git](/img/git/git_13_10.png)

vscode의 EXPLORER 탭에서 'Clone Repository' 버튼을 클릭하고, 주소입력란이 나타나면 url 주소를 붙여넣기한다.
![git](/img/git/git_13_11_w.png)

github의 리파지토리를 어디로 복사할지 경로를 선택한다. 선택한 경로 밑으로 리파지토리 이름의 폴더가 생성된다.
![git](/img/git/git_13_12_w.png)

![git](/img/git/git_13_13_w.png)

### 5. 팀장, 팀원 : 작업 후 push 전에 반드시 변경사항 가져와서(pull) 병합한 후 push 
사용자1 : test1.txt 파일 작업 후, 변경 사항을 내려받고(pull) add, commit, push
![git](/img/git/git_13_14.png)

사용자2 : test2.txt 파일 작업 후, 변경 사항을 내려받고(pull) add, commit, push
![git](/img/git/git_13_15.png)

사용자2 : 사용자1이 작성했던 test1.txt의 내용을 수정하고, pull, add, commit, push
![git](/img/git/git_13_16.png)

사용자1 : test1.txt의 내용을 수정하고, pull, add, commit
![git](/img/git/git_13_17.png)

![git](/img/git/git_13_18.png)

![git](/img/git/git_13_19.png)

![git](/img/git/git_13_20.png)
![git](/img/git/git_13_21.png)

![git](/img/git/git_13_22.png)