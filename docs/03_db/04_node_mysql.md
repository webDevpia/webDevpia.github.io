---
title: Node Mysql 연동하기
layout: default
parent: DataBase
nav_order: 4
permalink: /db/node_mysql
# nav_exclude: true
# search_exclude: true
---
# Node.js 로 mysql 사용하기
## 1. package.json 파일 작성
```bash
npm init -y
```

## 2. mysql 패키지 설치
```bash
npm install mysql
```

## 3. mysql 서버에 데이터베이스 작성
터미널를 이용해서 mysql 데이터베이스에 접속  
mysql는 mysql이 설치된 폴더 안에 bin폴더에 있음  
환경변수 설정이 안되어 있으면 실행되지 않을 수 있다.  

```bash
mysql -h localhost -u root -p
```
접속 후 터미널을 통해 데이터베이스를 생성, 혹은 워크벤치를 이용해서 생성
```sql
create database todoapp;
```
## 4. .env 구성파일 생성
.env 파일을 작업폴더의 root에 작성한다.
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=qwer1234
DB_NAME=todoapp
```

## 5. node.js에서 mysql 서버에 연결
connect.js 작성
```js
let mysql = require('mysql');

// process.env.를 이용한 .env파일 접근은 Node.js v20.6.0부터 사용가능
let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

connection.connect((err) => {
  if (err) return console.error(err.message);

  console.log('Connected to the MySQL server.');
});

```

## 6. 프로그램 실행 연결 확인
```bash
 node --env-file .env connect.js
```

## 7. package.json 파일의 속성을 변경하여 더 편하게 실행
```js
...
  "scripts": {
    "start": " node --env-file .env connect.js"
  },
...
```
```bash
npm start
```

## 8. MySQL 8.0 이상에 연결하면 다음과 같은 오류 메시지가 나타날 수 있습니다.
```bash
error: ER_NOT_SUPPORTED_AUTH_MODE: Client does not support authentication protocol requested by server; consider upgrading MySQL client
```
### 사용자의 mysql_native_password를 명시적으로 활성화해야함.
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'qwer1234';
```
### 혹은 mysql2를 설치해서 사용
```bash
npm install mysql2 
```

## 9. 연결 close
```js
let mysql = require('mysql');

let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

connection.connect((err) => {
  if (err) return console.error(err.message);

  console.log('Connected to the MySQL server.');
});
// 추가
connection.end((err) => {
  if (err) return console.error(err.message);

  console.log('Close the database connection.');
});

```

## 10. 테이블 생성
create_table.js 작성
```js
let mysql = require('mysql');

let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

// connect to the MySQL server
connection.connect((err) => {
  if (err) return console.error(err.message);

  const createTodosTable = `create table if not exists todos(
                          id int primary key auto_increment,
                          title varchar(255) not null,
                          completed bool not null default false
                      )`;

  connection.query(createTodosTable, (err, results, fields) => {
    if (err) return console.log(err.message);
  });

  // close the connection
  connection.end((err) => {
    if (err) return console.log(err.message);
  });
});
```
run:
```bash
node --env-file .env create_table.js
```

## 11. 데이터 입력
insert.js
```js
let mysql = require('mysql');

let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

connection.connect((err) => {
  if (err) return console.error(err.message);

  // insert statment
  let sql = `INSERT INTO todos(title,completed)
           VALUES('Learn how to insert a new row',true)`;

  // execute the insert statment
  connection.query(sql);

  // close the database connection
  connection.end();
});
```
run:
```bash
node --env-file .env insert.js
```

## 12. insert 처리 후 리턴값 확인
insert_return.js
```js
let mysql = require('mysql');

let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

connection.connect((err) => {
  if (err) return console.error(err.message);

  // insert statment
  let sql = `INSERT INTO todos(title,completed)
             VALUES(?,?)`;

  let todo = ['Insert a new row with placeholders', false];

  // execute the insert statment
  connection.query(sql, todo, (err, results, fields) => {
    if (err) return console.error(err.message);

    console.log('Todo Id:' + results.insertId);
  });

  // close the database connection
  connection.end();
});

```
run:
```bash
node --env-file .env insert_return.js
```

## 13. 한번에 여러건 입력
insert_multiple.js
```js
let mysql = require('mysql');

let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

connection.connect((err) => {
  if (err) return console.error(err.message);

  // insert statment
  let sql = 'INSERT INTO todos(title, completed) VALUES ?';

  let todos = [
    ['Master Node.js MySQL', false],
    ['Build Node.js / MySQL App', true],
  ];

  // execute the insert statment
  connection.query(sql, [todos], (err, results, fields) => {
    if (err) return console.error(err.message);

    console.log(`Inserted Rows: ${results.affectedRows}`);
  });

  // close the database connection
  connection.end();
});

```
run:
```bash
node --env-file .env insert_multiple.js
```

## 14. select
select.js
```js
let mysql = require('mysql');

let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

connection.connect((err) => {
  if (err) return console.error(err.message);

  let sql = `SELECT * FROM todos`;

  connection.query(sql, [true], (error, results, fields) => {
    if (error) return console.error(error.message);
    console.log(results);
  });

  // close the database connection
  connection.end();
});
```
run:
```bash
node --env-file .env select.js
```
output:
```bash
[
  RowDataPacket { id: 1, title: 'Learn how to insert a new row', completed: 1},
  RowDataPacket { id: 2, title: 'Insert a new row with placeholders', completed: 0
  RowDataPacket { id: 3, title: 'Master Node.js MySQL', completed: 0 },
  RowDataPacket { id: 4, title: 'Build Node.js / MySQL App', completed: 1 }
]
```
## 15. select
select_completed.js
```js
let mysql = require('mysql');

let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

connection.connect((err) => {
  if (err) return console.error(err.message);

  let sql = `SELECT * FROM todos WHERE completed=?`;

  connection.query(sql, [true], (error, results, fields) => {
    if (error) return console.error(error.message);
    console.log(results);
  });

  // close the database connection
  connection.end();
});
```
run:
```bash
node --env-file .env select_completed.js
```
output:
```bash
[
  RowDataPacket { id: 1, title: 'Learn how to insert a new row', completed: 1 },
  RowDataPacket { id: 4, title: 'Build Node.js / MySQL App', completed: 1}
]
```

## 16. 파일 실행 시 인자값으로 전달 
```js
...
let id = process.argv[2]; // pass argument to query

connection.connect((err) => {
  if (err) return console.error(err.message);

  let sql = `SELECT * FROM todos WHERE id=` + id;
...

});

```

run:
```bash
 node --env-file .env select_by_id.js 1
```

output:
```bash
[ RowDataPacket { id: 1, title: 'Learn how to insert a new row', completed: 1 } ]
```
## 17. update
update.js
```js
let mysql = require('mysql');

let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

connection.connect((err) => {
  if (err) return console.error(err.message);

  let sql = `UPDATE todos
           SET completed = ?
           WHERE id = ?`;

  let data = [false, 1];

  connection.query(sql, data, (error, results, fields) => {
    if (error) return console.error(error.message);
    console.log('Rows affected:', results.affectedRows);
  });

  // close the database connection
  connection.end();
});
```

run:
```bash
node --env-file .env update.js
```

## 18. delete

delete.js
```js
let mysql = require('mysql');

let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

connection.connect((err) => {
  if (err) return console.error(err.message);

  let sql = `DELETE FROM todos WHERE id = ?`;

  let data = [1];

  connection.query(sql, data, (error, results, fields) => {
    if (error) return console.error(error.message);
    console.log('Rows affected:', results.affectedRows);
  });

  // close the database connection
  connection.end();
});

```
run:
```bash
node --env-file .env delete.js
```

## 19. 저장프로시저
stored_procedure.js
```js
let mysql = require('mysql');

let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

connection.connect((err) => {
  if (err) return console.error(err.message);

  let sql = `CALL filterTodo(?)`;

  connection.query(sql, [false], (error, results, fields) => {
    if (error) return console.error(error.message);

    console.log(results);
  });

  // close the database connection
  connection.end();
});

```
run:
```bash
node --env-file .env stored_procedure.js
```

## 20. 간단한 터미널 프로그램 작성

userInput.js
```js
const readline = require('readline');

// input과 output을 사용하기 위해서 다음과 같이 정의
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function getUserInput() {
    return new Promise((resolve, reject) => {
      // 첫번째 인자 : "close","line" 등
        rl.on('line', (line) => {
            resolve(line);
        })
        // .on('close',()=>{
        //     process.exit();
        // });
    });
}
// module.exports를 이용하여 함수를 외부로 보낸다.
// 다른 파일에서 require()를 이용하여 호출해서 사용
module.exports = {getUserInput};
```

program.js
```js
const Input = require('./userInput');
let mysql = require('mysql');

let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

async function main(){
  console.clear();
  connection.connect();
  while(true){
    console.log(`1. 데이터입력 2.데이터수정 3.데이터삭제 4.목록  5.종료`);
    let menu = await Input.getUserInput();
    if(menu==='1') {
      console.log('제목입력>');
      let title = await Input.getUserInput();
      console.log('');
      let sql = `INSERT INTO todos(title,completed) VALUES(?,false)`;
      connection.query(sql,[title]);
    }else if(menu==='2'){
      console.log('수정');
    }else if(menu==='3'){    
      console.log('삭제');
    }else if(menu==='4'){ 
      console.log('목록');
    }else if(menu==='5'){ 
      console.log('프로그램 종료~');
      connection.end();
      process.exit();
    }else{ 
        console.log('메뉴를 잘못 선택하셨습니다.');
    };
    await wait(1000);
    console.clear();
  };
  
};

main();

const wait = (timeToDelay) => new Promise((resolve) => setTimeout(resolve, timeToDelay));
```