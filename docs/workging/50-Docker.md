---
layout: default
# title: 404
# permalink: /404
nav_exclude: true
search_exclude: true
---

## ssh 설정
apt-get update
apt-get install systemd net-tools vim openssh-server

4. ssh config 변경
vi /etc/ssh/sshd_config파일 가운데의
PermitRootLogin을 yes로 바꿈

(선택) root password 변경
passwd root: root의 비밀번호를 바꾼다. 초기 container 생성 시 비밀번호가 설정되어 있지 않으므로 이 작업을 해야한다.5. ssh 서비스 시작service ssh start: container에서 ssh를 시작한다.

서비스 시작

# service 서비스명 start


서비스 재시작

# service 서비스명 restart


서비스 종료

# service 서비스명 stop


서비스 상태확인

# service 서비스명 status


