---
title: Python MongoDB 연동하기
layout: default
parent: DataBase
nav_order: 4
permalink: /db/python_mongodb
# nav_exclude: true
# search_exclude: true
---
# Python MongoDB 연동하기

## 1. 라이브러리 설치
```bash
pip install pymongo
```

## 2. 연결 테스트
```python
import pymongo
from pymongo import MongoClient

# db 커넥션
client = MongoClient('mongodb+srv://sseonjo:1yJaNQRqIMxidqQs@cluster0.x8dde.mongodb.net/')
print('db 연결')
```

```python
# db 얻기
db = client.cinemadb

# 컬렉션 가져오기
cinema = db.영화    #collection = db['영화']

# 문서

# 문서삽입
data = {"영화제목":"파일럿", 
        "상영시간": {"시간":1, "분":51}, 
        "등급":"A", 
        "개봉날짜":"2024-07-31", 
        "출연배우":["조정석"]}
# data_id = cinema.insert_one(data).inserted_id
# print(data_id)

# 데이터베이스에 있는 모든 컬렉션을 나열
print(db.list_collection_names())

# 문서 가져오기
# for item in cinema.find():
#   print(item)

for item in cinema.find({'등급': 'B'}):
  print(item)

# 단일 문서 가져오기
# print(cinema.find_one())

# print(cinema.find_one({"영화제목":"파일럿"}))

# ObjectId로 쿼리하기 
# id = cinema.find_one({"영화제목":"파일럿"})['_id'] 
# print(cinema.find_one({"_id": id}))

#쿼리와 일치하는 문서의 수 체크
print(cinema.count_documents({}))
```