
# Mysql

MySQL은 관계형 데이터베이스 관리를 위해 설계된 강력한 데이터베이스 관리 시스템입니다. 

# 설치
[설치 파일 다운로드](https://dev.mysql.com/downloads/)  
windows - MySQL Installer for Windows  
mac - MySQL Community Server 8.0.34, MySQL Workbench 8.0.34

# 샘플 데이터베이스 다운로드
[샘플 데이터베이스 다운로드](/assets/data/mysqlsampledatabase.sql)
MySQL 샘플 데이터베이스 스키마는 다음 테이블로 구성됩니다.

고객(customers) : 고객의 데이터를 저장합니다.  
제품(products) : 축소 모형 자동차 목록을 저장합니다.  
제품라인(productlines) : 제품 라인 목록을 저장합니다.  
주문(orders) : 고객이 주문한 판매 주문을 저장합니다.  
주문세부정보(orderdetails) : 모든 판매 주문에 대한 판매 주문 개별 항목을 저장합니다.  
지불(payments) : 고객이 자신의 계정을 기반으로 지불한 금액을 저장합니다.  
직원(employees) : 누가 누구에게 보고하는지 등 직원 정보와 조직 구조를 저장합니다.  
영업소(offices) : 영업소 데이터를 저장합니다.  
다음 그림은 샘플 데이터베이스의 ER 다이어그램을 보여줍니다.  
![git](/assets/img/mysql/mysql-sample-database.png)

```
# 샘플데이터 다운로드 받고 터미널창에서
mysql -u root -p
Enter password: ********

mysql > source c:/temp/mysqlsampledatabase.sql

mysql > show databases;

+--------------------+
| Database           |
+--------------------+
| classicmodels      |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+

# 현재 사용자 확인
mysql > SELECT USER();
```

[MySQL Tutorial ](https://www.mysqltutorial.org/)

