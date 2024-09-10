---
title: Git Pull Request
layout: default
parent: Git
permalink: /git_PR
# nav_exclude: true
# search_exclude: true
---
# Pull Request ( pr 발행 )

### 1. fork

자신의 github 계정으로 로그인하고,  
협업하는 리파지토리(upstream으로 지칭)로 url을 이동  
fork를 클릭한다.

![git](/assets/img/git/git_pr_01.png)

리파지토리 이름이 자신의 기존에 사용하는 리파지토리 이름과 같다면 중복되지 않게 수정하고 'Create fork' 버튼을 클릭하여 자신의  github 계정으로 fork한다.(자신계정의 리파지토리는 origin으로 지칭)

![git](/assets/img/git/git_pr_02.png)

![git](/assets/img/git/git_pr_03.png)

upstream 쪽 내용이 수정이 되면

![git](/assets/img/git/git_pr_04.png)
![git](/assets/img/git/git_pr_05.png)
![git](/assets/img/git/git_pr_06.png)

origin 쪽에서 커밋내용을 확인할 수 있다.   
*This branch is 1 commit behind real_origin이름.*  
(링크를 클릭하면 비교화면으로 이동) 

![git](/assets/img/git/git_pr_07.png)

비교화면에서 내용의 변경사항을 확인할 수 있다.

![git](/assets/img/git/git_pr_08.png)

'Update branch'를 클릭하여 upstream의 변경사항을 update

![git](/assets/img/git/git_pr_09.png)

![git](/assets/img/git/git_pr_10.png)

### local 컴퓨터에 fork 리파지토리 clone

![git](/assets/img/git/git_pr_11.png)

![git](/assets/img/git/git_pr_12.png)

### 코드 작성 및 add, commit, push(필요시 branch로 작성)

![git](/assets/img/git/git_pr_13.png)

![git](/assets/img/git/git_pr_14.png)

*This branch is 1 commit ahead of upstream이름.*  

![git](/assets/img/git/git_pr_15.png)

### pull request

'Contribute'(혹은 'Pull requests')를 클릭하고, 'Open pull request' 클릭

![git](/assets/img/git/git_pr_16.png)

'Create pull request'를 클릭

![git](/assets/img/git/git_pr_17.png)

pull request 요청은 한 후 merge 될때까지 다시 요청할 수 없지만 요청이후 add, commit, push 되는 내용은 upstream쪽으로 자동으로 갱신된다.

![git](/assets/img/git/git_pr_17_1.png)

pull request가 생성되면 제목, 설명 부분을 작성한 후 'Create pull request'버튼을 클릭한다.

![git](/assets/img/git/git_pr_18.png)

![git](/assets/img/git/git_pr_19.png)

upstream 쪽에 Pull request 항목에 요청이 들어온게 확인된다.

![git](/assets/img/git/git_pr_20.png)

요청된 pull request 항목에서 merge 처리할 항목의 제목 부분을 클릭하면 머지 할수 있는 화면으로 이동한다.

![git](/assets/img/git/git_pr_21.png)

![git](/assets/img/git/git_pr_22.png)

### merge 혹은 close
![git](/assets/img/git/git_pr_23.png)

pull request 요청 이후 내용을 수정하고 add, commit, push 하면 pull request 요청이 머지되거나 혹은 close 되기전까지 자동으로 upstream 쪽으로 자동 갱신된다.
![git](/assets/img/git/git_pr_24.png)
![git](/assets/img/git/git_pr_25.png)
![git](/assets/img/git/git_pr_26.png)

### 변경내용 적용하기

### github에서 지원되는 Merge 방식
#### Merge
하나의 브랜치와 다른 브랜치의 모든 변경 이력을 합치는 방식으로 Merge Commit에서부터 뒤로 돌아가면서 부모를 찾고 브랜치를 구성
![git](/assets/img/git/git_pr_merge_01.png)

#### Sueash and Merge
각각 commit 되었던 a, b, c를 합쳐서 하나의 새로운 commit을 생성하고 브랜치에 추가  
새롭게 생성된 a, b, c통합 commit은 부모를 init 하나만 가지게 된다.
![git](/assets/img/git/git_pr_merge_02.png)

#### Rebase and Merge
이전에 수행되었던 commit a, b, c 간의 관계를 그대로 유지하면서 메인 브랜치에 추가하게 된다.  
commit a는 메인 브랜치의 이전 커밋인 commit e를 부모로 가지게 되고, rebase and merge작업 이후에는 이전에 존재했던 브랜치의 a,b,c commit과 메인 브랜치의 init, d, e, a, b, c commit과 연관을 가지지 않게 된다.
![git](/assets/img/git/git_pr_merge_03.png)

#### 위의 3가지 방식 중 원하는 방식으로 Merge 
merge 이후 upstream, origin, local의 코드를 일치시키는 작업을 진행 
origin쪽 github에서 synk fork -> discard 하고 local에서
```bash
git pull --rebase
```
로 가져온다.
혹은 upstream을 local에서 직접 추가하고 pull 해서 코드 상태를 일치시키기도 한다.

#### upstream 추가
```bash
git remote add upstream 'upstream url 주소'
git pull upstream main --rebase
git reset --hard '커밋코드'
git push -f
```
