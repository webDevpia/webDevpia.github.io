---
title: 8. FastAPI RDBMS
layout: default
grand_parent: Language
parent: FastAPI
nav_order: 8
permalink: /language/fastapi/fastapi_rdbms
has_children: false
---

## RDBMS 다루기 - SQLAlchemy 활용

```bash
 pip install sqlalchemy
 pip install mysql-connector-python
```

`MySqlWorkBench에서 실행`

```
/* sample db 및 데이터 생성 */

DROP DATABASE if exists blog_db;

CREATE DATABASE blog_db;

use blog_db;

DROP TABLE if exists blog;

CREATE TABLE blog (
  id int(11) NOT NULL AUTO_INCREMENT,
  title varchar(200) NOT NULL,
  author varchar(100) NOT NULL,
  content varchar(4000) NOT NULL,
  image_loc varchar(300) DEFAULT NULL,
  modified_dt datetime NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO blog_db.blog(title, author, content, modified_dt) values('테스트 title 1', '둘리', '테스트 컨텐츠 1', now());
INSERT INTO blog_db.blog(title, author, content, modified_dt) values('테스트 title 2', '길동', '테스트 컨텐츠 2', now());
INSERT INTO blog_db.blog(title, author, content, modified_dt) values('테스트 title 3', '도넛', '테스트 컨텐츠 3', now());
INSERT INTO blog_db.blog(title, author, content, modified_dt) values('테스트 title 4', '희동', '테스트 컨텐츠 4', now());

COMMIT;
```

`DB_Fundamentals/db_basic.py`

```py
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

# database connection URL
# dialect+driver://username:password@host:port/database
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@127.0.0.1:3306/blog_db"
# Engine 생성
engine = create_engine(DATABASE_CONN, poolclass=QueuePool,
            pool_size=10, max_overflow=0)

try: 
    # Connection 얻기
    conn = engine.connect()
    # SQL 선언 및 text로 감싸기
    query = "select id, title from blog"
    stmt = text(query)
    
    # SQL 호출하여 CursorResult 반환.
    result = conn.execute(stmt)
    print("type result:", result)

    rows = result.fetchall()
    print(rows)

    # print(type(rows[0]))
    # print(rows[0].id, rows[0].title)
    # print(rows[0][0], rows[0][1])
    # print(rows[0]._key_to_index)

    result.close()
except SQLAlchemyError as e:
    print(e)
finally: 
    # close() 메소드 호출하여 connection 반환.
    conn.close()

```

`DB_Fundamentals/pool_practice.py`

```py
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool

# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"

# engine = create_engine(DATABASE_CONN)
engine = create_engine(DATABASE_CONN, 
                    poolclass=QueuePool,
                    #poolclass=NullPool, # Connection Pool 사용하지 않음. 
                    pool_size=10, max_overflow=2
                    )
print("#### engine created")

def direct_execute_sleep(is_close: bool = False):
    conn = engine.connect()
    query = "select sleep(5)"
    # text()는 SQLAlchemy에서 SQL 문자열을 안전하게 실행 가능한 객체로 감싸는 함수
    result = conn.execute(text(query))
    # rows = result.fetchall()
    # print(rows)
    result.close()

    # 인자로 is_close가 True일 때만 connection close()
    if is_close:
        conn.close()
        print("conn closed")
# is_close=True 값이 True, False 일때 비교
for ind in range(20):
    print("loop index:", ind)
    direct_execute_sleep(is_close=True)

print("end of loop")
```

`MYSQL Workbench의 root 계정으로 접속해서 확인`

```
/* connection 모니터링 스크립트. root로 수행 필요. */
select * from sys.session where db='blog_db' order by conn_id;
```
**is_close=True**
![](./img/fastapi015.png)

**is_close=False**
![](./img/fastapi016.png)

`DB_Fundamentals/context_practice.py`

```py
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool

# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"

engine = create_engine(DATABASE_CONN, 
                    echo=True, # 내부적으로 동작하는 sql문을 보여줌
                    poolclass=QueuePool,
                    #poolclass=NullPool,
                    pool_size=10, max_overflow=0)

# conn.close() 하지 않아도 with절을 빠져나가면 자동으로 close() 처리
def context_execute_sleep():
    with engine.connect() as conn:
        query = "select sleep(5)"
        result = conn.execute(text(query))
        result.close()
        #conn.close()

for ind in range(20):
    print("loop index:", ind)
    context_execute_sleep()

print("end of loop")
```

**DB엔진 모듈화**

`DB_Fundamentals/database.py`

```py
from sqlalchemy import create_engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import contextmanager


# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"

engine = create_engine(DATABASE_CONN,
                    poolclass=QueuePool,
                    #poolclass=NullPool, # Connection Pool 사용하지 않음. 
                    pool_size=10, max_overflow=0)

def direct_get_conn():
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise e


@contextmanager
def context_get_conn():
    try:
        conn = engine.connect()
        yield conn
    except SQLAlchemyError as e:
        print(e)
        raise e
    finally: 
        conn.close()
    
```


`DB_Fundamentals/module_direct.py`

```py
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import direct_get_conn

def execute_query(conn: Connection):
    query = "select * from blog"
    stmt = text(query)
    # SQL 호출하여 CursorResult 반환. 
    result = conn.execute(stmt)

    rows = result.fetchall()
    print(rows)
    result.close()

def execute_sleep(conn: Connection):
    query = "select sleep(5)"
    result = conn.execute(text(query))
    result.close()

for ind in range(20):
    try: 
        conn = direct_get_conn()
        execute_sleep(conn)
        print("loop index:", ind)
    except SQLAlchemyError as e:
        print(e)
    finally: 
        conn.close()
        print("connection is closed inside finally")

print("end of loop")
```


`DB_Fundamentals/module_context.py`

```py
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import context_get_conn

def execute_query(conn: Connection):
    query = "select * from blog"
    stmt = text(query)
    # SQL 호출하여 CursorResult 반환. 
    result = conn.execute(stmt)

    rows = result.fetchall()
    print(rows)
    result.close()

def execute_sleep(conn: Connection):
    query = "select sleep(5)"
    result = conn.execute(text(query))
    result.close()


for ind in range(20):
    try: 
        with context_get_conn() as conn:
            execute_sleep(conn)
            print("loop index:", ind)
    except SQLAlchemyError as e:
        print(e)
    finally: 
        #conn.close()
        #print("connection is closed inside finally")
        pass


print("end of loop")
```


`DB_Fundamentals/cursor_fetch.py`

```py
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import direct_get_conn

try:
    # Connection 얻기
    conn = direct_get_conn()

    # SQL 선언 및 text로 감싸기
    query = "select id, title from blog"
    stmt = text(query)

    # SQL 호출하여 CursorResult 반환. 
    result = conn.execute(stmt)
    rows = result.fetchall() # row Set을 개별 원소로 가지는 List로 반환. 
    #rows = result.fetchone() # row Set 단일 원소 반환
    #rows = result.fetchmany(2) # row Set을 개별 원소로 가지는 List로 반환.
    # rows = [row for row in result] # List Comprehension으로 row Set을 개별 원소로 가지는 List로 반환
    print(rows)
    print(type(rows))

    
    # 개별 row를 컬럼명를 key로 가지는 dict로 반환하기
    # row_dict = result.mappings().fetchall()
    # print(row_dict)

    # 코드레벨에서 컬럼명 명시화
    # row = result.fetchone()
    # print(row._key_to_index)
    # rows = [(row.id, row.title) for row in result]
    # print(rows)

    result.close()
except SQLAlchemyError as e:
    print("############# ", e)
    #raise e
finally:
    # close() 메소드 호출하여 connection 반환.
    conn.close()
```


`DB_Fundamentals/bind_variable.py`

```py
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import direct_get_conn
from datetime import datetime

try:
    # Connection 얻기
    conn = direct_get_conn()

    # SQL 선언 및 text로 감싸기
    # 1, 2, 3, 4 | '둘리', '길동'
    query = '''select id, title, author from blog where id = :id and author = :author 
            and modified_dt < :modified_dt'''
    stmt = text(query)
    bind_stmt = stmt.bindparams(id=1, author='둘리', modified_dt=datetime.now())

    # SQL 호출하여 CursorResult 반환. 
    result = conn.execute(bind_stmt)
    rows = result.fetchall() # row Set을 개별 원소로 가지는 List로 반환. 
    print(rows)
    result.close()
except SQLAlchemyError as e:
    print("############# ", e)
    #raise e
finally:
    # close() 메소드 호출하여 connection 반환.
    conn.close()
```
