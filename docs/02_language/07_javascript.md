---
title: javascript
layout: default
parent: Language
nav_order: 8
permalink: /language/js
# nav_exclude: true
# search_exclude: true
---

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