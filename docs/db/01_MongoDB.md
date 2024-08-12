---
title: MongoDB
layout: default
parent: DataBase
nav_order: 1
permalink: /db/MongoDB
# nav_exclude: true
# search_exclude: true
---

# MongoDB 

## 설치

### 1. On-Premises 설치
[MongoDB 공식 사이트](https://www.mongodb.com/ko-kr) 

#### windows 환경
Try Community Edition의 Download 클릭
![](/assets/img/mongodb/mongodb001.png)

Select package 버튼 클릭
![](/assets/img/mongodb/mongodb002.png)

버전, 플랫폼 등 선택 후 다운로드
![](/assets/img/mongodb/mongodb003.png)

다운로드 받은 파일 실행
![](/assets/img/mongodb/mongodb004.png)

라이센스 허용  
![](/assets/img/mongodb/mongodb005.png)

Complete 기본으로 Next
![](/assets/img/mongodb/mongodb006.png)

![](/assets/img/mongodb/mongodb007.png)

![](/assets/img/mongodb/mongodb008.png)

![](/assets/img/mongodb/mongodb009.png)

![](/assets/img/mongodb/mongodb010.png)

![](/assets/img/mongodb/mongodb011.png)

환경변수 설정으로 이동  
![](/assets/img/mongodb/mongodb012.png)

시스템 변수에 Path 선택 후 편집 클릭  
![](/assets/img/mongodb/mongodb013.png)

새로 만들기 클릭한 후,  C:\Program Files\MongoDB\Server\7.0\bin를 추가한다.
![](/assets/img/mongodb/mongodb014.png)

vscode나 터미널창이 열려있다면 닫았다가 다시 열어서 확인한다.
![](/assets/img/mongodb/mongodb015.png)

설치된 MongoDB Compass를 통해 접속 확인한다.
#### macOS
[Install Homebrew](https://brew.sh/#install)  
[mongodb 설치](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)
```bash
brew tap mongodb/brew
brew update
brew install mongodb-community@7.0
brew install --cask mongodb-compass
brew services start mongodb-community@7.0
brew services stop mongodb-community@7.0
```
### 2. Cloud
mongodb를 aws, 애저, 구글 클라우드 같은 클라우드에 올려놓고 사용할수 있다. 이 서비스를 Atlas라고 함.
![](/assets/img/mongodb/mongodb016.png)

스토리지의 사이즈등 여러 정책에 따라 무료인 Shared, 사용량에 따라 요금을 부과하는 Serverless, 매달 일정 금액을 지불하는 Dedicated 등이 있다.
![](/assets/img/mongodb/mongodb017.png)

회원 등록
![](/assets/img/mongodb/mongodb018.png)

체크하고 Submit버튼 클릭
![](/assets/img/mongodb/mongodb019.png)

Welcome화면
![](/assets/img/mongodb/mongodb020.png)

사용 목적 등 간단한 설문조사에 답 선택 
![](/assets/img/mongodb/mongodb021.png)

Free, aws, Seoul 선택하고 Create 버튼 클릭
![](/assets/img/mongodb/mongodb022.png)

사용자 이름과 비밀번호 설정하고, mongodb접속 위치를 추가
![](/assets/img/mongodb/mongodb023.png)

설정완료 화면이 나온다.
![](/assets/img/mongodb/mongodb024.png)

샘플데이터를 로드하여 볼 수 있다.
![](/assets/img/mongodb/mongodb025.png)

로컬컴퓨터의 MongoDB Compass를 통해 접속하기 위해 CONNECT를 클릭한다.
![](/assets/img/mongodb/mongodb026.png)

Compass를 선택한다.
![](/assets/img/mongodb/mongodb027.png)

connection string 을 복사한다.
![](/assets/img/mongodb/mongodb028.png)

MongoDB Compass를 실행하고 Connection URI에 붙여넣고, \<username\>과 \<password\>를 수정하고 연결 테스트 한다.
![](/assets/img/mongodb/mongodb029.png)


## MongoDB 개념 정리
### 1. 구성
데이터베이스 - 컬렉션 - 문서로 연결되는 계층적 구조를 가지고 데이터를 관리  

문서(document)
- mongodb의 기본 저장 단위, 테이블의 행과 개념이 비슷, 레코드  
- 문서는 필드이름과 필드값으로 이루어진 쌍들의 집합
- 구성 방식이 json과 비슷하여 객체지향 프로그램과 상호연계가 자연스러움
- 내부적으로 json의 이진 유형인 BSON(Binary JSON)의 형식으로 컬렉션 안에 저장

컬렉션(collection)  
- 문서들의 모임으로 여러 문서들을 포함하며 같은 컬렉션 안에도 저장되는 문서 구조가 다양할 수 있음
- 동적 스키마를 갖는 테이블과 비슷함
- 모든 문서는 고유한 값을 갖는 _id 필드를 포함

데이터베이스(database)
- 컬렉션들의 모임으로 여러 컬렉션들을 포함
- 컬렉션들의 물리적인 컨테이너, 개념적으로는 컬렉션들을 구분하는 이름공간 역활을 함.

	- admin 데이터베이스 : 인증과 권한 부여에 관한 데이터를 저장
	- local 데이터베이스 : 단일 서버에 대한 데이터를 저장
	- config 데이터베이스 : 샤딩된 클러스터에 관한 각 샤드(shard) 정보를 저장  

![](/assets/img/mongodb/mongodb30.jpg)

### 2. 문서 데이터 모델
mongodb는 문서 기반 데이터 모델을 사용
데이터의 계층적 표현이 가능, 복잡한 조인 연산 없이도 하나의 문서 안에 모두 표현 가능
![](/assets/img/mongodb/mongodb31.jpg)

### 3. JSON과 BSON 차이
json 문서를 사용하지만 내부 저장시에는 이진 포맷으로 인코딩한 BSON문서로 변환되어 저장.  
BSON 형식은 컴퓨터가 쉽게 이해할수 있는 형식이며, 검색 속도가 빠르고 json의 데이터 유형에 추가하여 날짜와 이진 데이터 유형을 지원한다.  
MongoDB가 자동으로 처리해주기는 하지만 인코딩과 디코딩이 추가로 필요하다.
![](/assets/img/mongodb/mongodb32.jpg)

### 4. MongoDB의 동적 스키마
MongoDB는 동적 스키마를 가진다. 즉 미리 정해진 스키마가 존재하지 않는다는 의미이며, 이는 급격한 변화에 능동적으로 대응할수 있다는걸 의미.  
같은 컬렉션 안에서도 서로 다른 스키마를 가질수 있다.
![](/assets/img/mongodb/mongodb33.jpg)

### 5. MongoDB의 관계 표현
관계형DB는 1:1, 1:N, M:N 관례를 외래키 참조 관계로 표현  
MongoDB는 외래키 개념이 없어 문서간의 연관관계를 다음 두가지 방식으로 표현
- 내장(embedded) 방식  
  관계를 갖는 데이터를 하나의 문서 안에 함께 저장하는 반정규화 형태  
  문서안에 내장된 서브 문서 형태로 표현
- 참조(reference) 방식  
  관계를 갖는 다른 문서의 키 필드 값을 참조키로 저장하는 정규화 형태  
  서로 다른 독립된 문서에 대한 _id 필드값을 외래키처럼 저장함으로써 관계를 표현  

![](/assets/img/mongodb/mongodb34.jpg)

### 6. MongoDB완 관계형 데이터베이스 구조 비교
![](/assets/img/mongodb/mongodb35.jpg)

## 쉘을 이용한 데이터베이스와 컬렉션 관리
명령어 입력시 대소문자 구분함.

### 1. 데이터베이스 생성 및 지정
데이터베이스 생성 명령어가 따로 없다. 대신 use 명령어를 통해 생성되지 않은 데이터베이스를 접속 대상으로 지정할 수 있다.  

```
//데이터베이스 목록 표시
show dbs 

// 접속할 데이터 베이스 지정
use <데이터베이스 이름> 

// 현재 접속한 데이터베이스 표시
db 

//현재 접속한 데이터베이스의 컬렉션 목록 확인
show collections 

// 쉘 도움말 제공
help

use mydb

// 'mydb' 현재 데이터베이스의 상세 정보 제공
db.stats()			

// 'mycollection' 컬렉션의 상세 정보 제공
db.mycollection.stats() 	

// 'mydb' 현재 데이터베이스 안의 컬렉션 정보 제공
db.getCollectionInfos()    
```
### 2. 실습 예제 데이터베이스(cinemadb:회원,영화 컬렉션)
![](/assets/img/mongodb/mongodb36.jpg)
![](/assets/img/mongodb/mongodb37.jpg)

### 3. 컬렉션 생성 및 변경 : createCollection(),renameCollection()
```
use cinemadb
//컬렉션 생성
//capped를 true로 설정하면 size인자로 정해진 크기(바이트)를 초과하게 되면 자동으로 가장 오래된 데이터 삭제한다.
db.createCollection("회원", {capped:true, size:5})  
db.createCollection("미등록회원") 
show collections 

//컬렉션 이름변경
db.미등록회원.renameCollection("비회원") 
show dbs   
show collections 

//컬렉션 삭제
db.회원.drop()
db.createCollection("회원")
```

### 4. 몽고db 데이터 유형
![](/assets/img/mongodb/mongodb38.jpg)

### 5. 컬렉션 문서 관리 명령문
![](/assets/img/mongodb/mongodb39.jpg)

### 6. 컬렉션 문서 삽입 insert문
_id필드는 명시적으로 정의하지 않으면 자동으로 ObjectId 자료형을 가진 값으로 채워진다.  
_id는 중복된 값은 입력되지 않는다.

```
//문서형식
{필드명:"값",.....필드명n:"값n"}
```

#### 한 건 입력
```
use cinemadb 
db 
// 첫 번째 문서 
db.비회원.insertOne({비회원이름:"이승기"})     

// 두 번째 문서       
db.비회원.insertOne({비회원이름:"이민기", 나이:22})   

//비회원 컬렉션에 저장된 모든 문서 보여준다
db.비회원.find() 

//컬렉션에 입력된 문서 건수 확인
db.비회원.countDocuments()
```
acknowledged : 입력 성공 여부  
insertedId : 입력에 성공한 문서의 ObjectId값 표시

#### 여러건 입력
입력 중에 오류가 발생하면 오류가 발생하는 문서는 입력되지 않는다.
```
db.회원.insertMany( [
 { _id:3, 회원이름:"홍길동", 비밀번호:"5555", 나이:22, 성별:"남" },
 { _id:4, 회원이름:"홍백합", 비밀번호:"6666", 나이:23, 성별:"여" },
 { _id:5, 회원이름:"홍나리", 비밀번호:"7777", 나이:24, 성별:"여" }
 ] )

 //pretty() 복잡한 구조를 좀더 보기편하게 정리해서 출력
db.회원.find().pretty() 	
```

```
db.createCollection("영화")

db.영화.insertMany([ 
 {영화제목:"기생충", 상영시간:{시간:3, 분:10}, 등급:"A", 개봉날짜:"2019-05-30", 
  출연배우:["송강호", "이선균", "조여정"]},
 {영화제목:"명량", 상영시간:{시간:2, 분:9}, 등급:"B", 개봉날짜:"2022-07-27", 
  출연배우:["박해일"]}
 ])

db.영화.find()

db.영화.insertOne({영화제목:"승리호", 상영시간:{시간:1, 분:50}, 등급:"A", 
 개봉날짜:"2021-02-21", 출연배우:["송중기", "김태리"],
 댓글평가:[ 
   {댓글작성자:"홍길순", 댓글내용:"좋아요"},
   {댓글작성자:"홍길동", 평점:97, 댓글내용:"좋아요", 추천여부:true},
   {댓글작성자:"홍장미", 평점:83, 댓글내용:"무난해요", 추천여부:false} 
  ] 
 })

db.영화.find()
```

### 7. 컬렉션 문서 검색 find

```
//find 형식
find({검색조건},{검색_필드목록})

//검색조건 형식
필드명:상수값,...

//검색_필드목록 형식
필드명:논리값,....필드명n:논리값n
```

```
db.회원.find() 
db.회원.find({ })	
db.회원.find({회원이름:"홍나리"}) 
db.회원.find({나이:24, 성별:"여"}) 

//나타나는 필드 목록을 정할수 있다.
//true(1),false(0)
//true와 false를 섞어서 사용은 안됨 
db.회원.find({}, {회원이름:true}) 
db.회원.find({}, {나이:false}) 
db.회원.find({나이:24}, {회원이름:1, 나이:1}) 
db.회원.find({}, {_id:false, 나이:0})	
```

### 8. 검색 비교 연산자 : $eq(=), $ne(!=), $gt(>), $gte(>=), $lt(<), $lte(<=)
```
// 검색조건 ,로 구분하면 and연산처리
필드명:{비교연산자1:"값1",비교연산자2:"값2",....}
```

```
db.영화.find({"상영시간.시간":{$gte:2, $lte:3}}) 

// $eq는 그냥 값을 적어도 동일
db.영화.find({영화제목:{$eq:"기생충"}}) 
db.영화.find({영화제목:"기생충"}) 

db.영화.find({개봉날짜:{$gt:"2020-1-1"}}) 
```

### 9. $all, $and, $or, $in, $nin
```
//송강호,이선균이 있으면 다른 배우가 더 있어도 검색
db.영화.find({출연배우:{$all:["송강호", "이선균"]}}) 

//송강호와 이선균만 있어야 검색
db.영화.find({출연배우:["송강호", "이선균"]}) 

// $and로 나열하는 것과 ,로 나열하는 것 둘다 같음
db.회원.find({$and:[{나이:24}, {회원이름:"홍나리"}]}) 
db.회원.find({회원이름:"홍나리", 나이:21}) 
db.회원.find({나이:24, 회원이름:"홍나리"})

db.회원.find({$or:[{나이:{$in:[22,23,24]}}, {회원이름:"홍나리"}]}) 
db.영화.find({등급:{$nin:["B"]}}) 
db.영화.find({등급:{$in:["A","C"]}})
```

### 10. $regex 연산자의 문자열패턴
![](/assets/img/mongodb/mongodb40.jpg)

```
//문서안에 내장된 문서에 접근시는 상위필드와 하위필드 사이 마침표(.)를 이용하여 연결
//반드시 큰따옴표로 감싼다
db.영화.find({"상영시간.시간":1, "상영시간.분":{$gte:30}} ) 
db.영화.find({"상영시간.분":{$gte:30}, "상영시간.시간":1}) 
db.영화.find({"댓글평가.댓글작성자":/^홍/, "댓글평가.평점":{$gt:80}}) 

//회원이름이 '홍'으로 시작하는 문서를 검색
db.회원.find({회원이름:{$regex:/^홍/}}) 

//하나의 필드에 검색조건이 하나이면 생략해서 사용 가능
//회원이름이 '동'으로 끝나는 문서 검색
db.회원.find({회원이름:/동$/})

//회원이름에 '길동'이 포함되어 있으면 검색 
db.회원.find({회원이름:/길동/}) 	

//회원이름이 '홍길동1' or '홍길동2' or '홍길동3'이면 검색
db.회원.find({회원이름:/홍길동[1-3]/}) 	

//회원이름이 '홍길동1' or '홍길동2' or '홍길동3' 중에 '홍길동2'는 제외
db.회원.find({회원이름:{$regex:/홍길동[1-3]/, $not:/홍길동2/}}) 
```

### 11. 검색 결과의 정렬, 생략 및 제한 : sort(), skip(), limit()
```
//나이 필드 오름차순으로 나이 값이 같다면 등급필드 내림차순으로 졍렬
db.회원.find().sort({나이:1, 등급:-1}) 

// 반환되는 결과 중 처음 5개 문서 생략
db.회원.find().skip(5) 

// 반환되는 결과 중 3개만 반환
db.회원.find().limit(3) 

// 반환되는 결과 중 하나만 반환
db.회원.findOne()
```

### 12. 컬렉션 문서 수정 update문
#### $set : 새로운 필드를 추가하거나 특정 필드 값을 변경
#### $unset : 불필요한 필드를 삭제
#### $inc : 기존의 수치값에 1만큼 수치를 증가
#### $rename : 문서의 필드 이름을 새로운 이름으로 변경

```
db.컬렉션이름.updateOne({수정_검색조건},{수정_옵션},{upsert:논리값})
db.컬렉션이름.updateMany({수정_검색조건},{수정_옵션},{upsert:논리값})
```

```
//수정옵션에 수정연산자를 사용하지 않으면 오류 발생
db.회원.updateOne({}, {회원이름:"Modified"}) 
db.회원.find({}, {_id:false}) 

//회원이름이 "홍백"으로 시작하는 문서를 찾아서 회원이름과 나이를 수정 
db.회원.updateOne({회원이름:/^홍백/}, {$set:{회원이름:"Hong Beakhap", 나이:0}})  
db.회원.find({}, {_id:false})

//성별이 "남"인 문서를 찾아서 성별을 "M", 비밀번호를 0으로 변경
db.회원.updateMany({성별:"남"}, {$set:{성별:"M", 비밀번호:0}}) 
db.회원.find({}, {_id:false}) 

//모든 문서를 가져와서 탈퇴날짜 필드가 없으므로 생성하고 해당 날짜를 생성해서 입력
db.회원.updateMany({}, {$set:{탈퇴날짜:new Date("2023-3-3")}})   
db.회원.find({}, {_id:false}) 

//모든 문서의 탈퇴날짜 필드를 삭제
db.회원.updateMany({ }, {$unset:{탈퇴날짜:""}}) 

//성별이 "M"인 문서의 나이 값이 1 증가시킴
db.회원.updateMany({성별:"M"}, {$inc:{나이:1}}) 

//성별이 "여"인 문서의 회원이름 필드명을 name 필드로 수정하고, 비밀번호 필드는 삭제 
db.회원.updateMany({성별:"여"}, {$rename:{회원이름:"name"}, $unset:{비밀번호:0}}) 

db.회원.find({}, {_id:false}) 
```

### 13. 문서 치환 replaceOne()
특정 문서를 찾아서 새로운 문서로 교체, _id값은 동일

```
db.비회원.find()
db.비회원.replaceOne({비회원이름:"이승기"}, {비회원이름:"이충기", 나이: 30, 성별:"남"}) 
db.비회원.find({비회원이름: "이승기"}) 

//검색 조건을 충족하는 문서가 없으면 세번째 인자인 upsert옵션이 적용
// true : 두번째 인자인 문서를 새로 만들어서 추가
db.비회원.replaceOne({비회원이름:"이슬기"}, {비회원이름:"이슬기", 나이:30, 성별:"여"}, {upsert: true})  
db.비회원.find({비회원이름:/이?기/})
```

### 14. 데이터베이스, 컬렉션, 문서의 삭제 drop문, delete문 

#### 문서 삭제 : deleteOne(), deleteMany()
```
db.컬렉션이름.deleteOne({삭제_검색조건})
db.컬렉션이름.deleteMany({삭제_검색조건})
```

```
db.회원.find()
db.회원.deleteOne({나이:22}) 
db.회원.find()
db.회원.deleteMany({나이:24}) 
db.회원.find()
db.회원.deleteMany({ }) 
db.회원.find()
```

#### 컬렉션 삭제 : drop()
삭제된 컬렉션은 복구할 수 없다.
```
db.컬렉션이름.drop()
```

```
db.회원.drop() 
show collections
db.영화.deleteMany({ }) 
db.영화.find()
db.영화.drop() 
db.영화.find()
```

#### 데이터베이스 삭제 : dropDatabase()
```
use cinemadb 
db 
//현재 접속 데이터베이스 삭제
db.dropDatabase() 
```