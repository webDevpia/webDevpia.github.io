---
title: Node Mongodb 연동하기
layout: default
parent: DataBase
nav_order: 2
permalink: /db/Node_Mongodb
# nav_exclude: true
# search_exclude: true
---

# MongoDB Node.js연동

## 1. 연결하기
### 작업환경 만들기 
- 작업폴더를 생성  
- package.json 파일을 생성
- mongodb 라이브러리 설치

```bash
mkdir mongodb
cd mongodb
npm init -y
npm install mongodb@6.3
```

## 1. .env 파일 생성
- .env파일 작성 워킹디렉토리 루트에 저장

```bash
DB_LOCAL_URL = mongodb://localhost:27017/
DB_ATLAS_URL = mongodb+srv://<username>:<password>@mongodbtest.4itmroo.mongodb.net/?retryWrites=true&w=majority
```

## 2. db연결

connection.js
```js
const { MongoClient } = require('mongodb');

const uri = process.env.DB_LOCAL_URL;
// const uri = process.env.DB_ATLAS_URL;
// console.log(uri);

const client = new MongoClient(uri);
const dbName = 'myProject';

async function main() {
   await client.connect();
   console.log('Connected successfully to server');
   const db = client.db(dbName);
   const collection = db.collection('documents');
   return 'done.';
}

main()
.then(console.log)
.catch(console.error)
.finally(() => client.close());
```

```bash
node --env-file .env connection.js
```

## 2. 데이터베이스 목록 확인
list_db.js
```js
const { MongoClient } = require('mongodb');

async function main() {    
  const uri = process.env.DB_LOCAL_URL;
  const client = new MongoClient(uri);
  try {
    await client.connect();
    await listDatabases(client);
  } catch (e) {
    console.error(e);
  } finally {
    await client.close();
  }
}

main().catch(console.error);

async function listDatabases(client) {
   databasesList = await client.db().admin().listDatabases();
   console.log("Databases:");
   console.log(typeof(databasesList));
   console.log(databasesList);
   databasesList.databases.forEach(db => console.log(` - ${db.name}`));
};
```

```bash
node --env-file .env list_db.js
```

## 3. 데이터베이스 생성
create_db.js
```js
//적어도 하나 이상의 컬렉션이 생성되어야 데이터베이스가 물리적으로 생성된다.
const {MongoClient} = require('mongodb');

async function main(){
  const uri = process.env.DB_LOCAL_URL;
  // const uri = process.env.DB_ATLAS_URL;
  // console.log(uri);
   const client = new MongoClient(uri);

   try {
      await client.connect();
      await createdb(client, "mydatabase");       
   } finally {
      await client.close();
   }
}

main().catch(console.error);

async function createdb(client, dbname){
   const dbobj = await client.db(dbname);
   console.log("Database created");
   console.log(dbobj);
};
```

```bash
node --env-file .env create_db.js
```

## 4. 컬렉션 생성
create_collection.js
```js
const {MongoClient} = require('mongodb');

async function main(){

  const uri = process.env.DB_LOCAL_URL;
  // const uri = process.env.DB_ATLAS_URL;
  // console.log(uri);

   const client = new MongoClient(uri);

   try {
      await client.connect();
      await newcollection(client, "mydatabase");
   } finally {
      await client.close();
   }
};

main().catch(console.error);

async function newcollection (client, dbname){
   const dbobj = await client.db(dbname);
   const collection = await dbobj.createCollection("MyCollection");
   console.log("Collection created");
   console.log(collection);
};
```

```bash
node --env-file .env create_collection.js
```

## 5. 데이터 한 건 입력
insert.js
```js
const {MongoClient} = require('mongodb');

async function main(){
  const uri = process.env.DB_LOCAL_URL;
  // const uri = process.env.DB_ATLAS_URL;
  // console.log(uri);
   const client = new MongoClient(uri);

   try {
      await client.connect();
      await createdoc(client, "mydatabase", "products", {
         "ProductID":1, "Name":"Laptop", "Price":25000
      });
       
   } finally {
      await client.close();
   }
};

main().catch(console.error);

async function createdoc(client, dbname, colname, doc){
   const dbobj = await client.db(dbname);
   const col = dbobj.collection(colname);
   const result = await col.insertOne(doc);
   console.log(`New document created with the following id: ${result.insertedId}`);
};
```

```bash
node --env-file .env insert.js
```

## 6. 여러건 데이터 입력하기
insert_many.js
```js
const {MongoClient} = require('mongodb');

async function main(){

  const uri = process.env.DB_LOCAL_URL;
  // const uri = process.env.DB_ATLAS_URL;
  // console.log(uri);
   
   const client = new MongoClient(uri);

   try {
      await client.connect();
      await createdocs(client, [
         {'ProductID':1, 'Name':'Laptop', 'price':25000},
         {'ProductID':2, 'Name':'TV', 'price':40000},
         {'ProductID':3, 'Name':'Router', 'price':2000},
         {'ProductID':4, 'Name':'Scanner', 'price':5000},
         {'ProductID':5, 'Name':'Printer', 'price':9000}
      ]);  
   } finally {
      await client.close();
   }
};

main().catch(console.error);

async function createdocs(client, docs){
   const result = await client.db("mydb").collection("products").insertMany(docs);
   console.log(`${result.insertedCount} new document(s) created with the following id(s):`);
   console.log(result.insertedIds);
};
```

```bash
node --env-file .env insert_many.js
```

## 7. 데이터 검색(find) 및 특정필드만 출력(project)
find.js
```js
const {MongoClient} = require('mongodb');

async function main(){

  const uri = process.env.DB_LOCAL_URL;
  // const uri = process.env.DB_ATLAS_URL;
  // console.log(uri);

   const client = new MongoClient(uri);

   try {
      await client.connect();
      await listall(client, "mydb", "products");
   } finally {
      await client.close();
   }
};

main().catch(console.error);

async function listall(client, dbname, colname){
  // const result = await client.db(dbname).collection(colname).find({}).toArray();
  // const result = await client.db(dbname).collection(colname).find({"Name":"TV"}).toArray();
  // const result = await client.db(dbname).collection(colname).findOne({});  
  
  const projection = { name: 1 , price: 1};
  const result = await client.db(dbname).collection(colname).find({}).project(projection).toArray(); 

  console.log(typeof(result));
  console.log(result);

  //  forEach loop
  // var count=0;
  // result.forEach(row => {
  //   count++;
  //   console.log(count, row['Name'], row['price']);
  // });

  console.log(typeof(JSON.stringify(result)));
  console.log(JSON.stringify(result));
};
```

```bash
node --env-file .env find.js
```

## 8. 데이터 검색(query)
query.js
```js
const {MongoClient} = require('mongodb');

async function main(){
  const uri = process.env.DB_LOCAL_URL;
  // const uri = process.env.DB_ATLAS_URL;
  // console.log(uri);
   const client = new MongoClient(uri);

   try {
      await client.connect();
      await fetchdocs(client, "mydb", "products");
   } finally {
      await client.close();
   }
};

main().catch(console.error);

async function fetchdocs(client, dbname, colname){
  const result = await client.db(dbname).collection(colname).find({"price":{$gt:10000}}).toArray();
  //  const result = await client.db(dbname).collection(colname).find({$and:[{"price":{$gt:1000}}, {"price":{$lt:10000}}]}).toArray();
  // const result = await client.db(dbname).collection(colname).find({Name:{$regex:"^P"}}).toArray();
  // const result = await client.db(dbname).collection(colname).find({Name: /Ro/}).toArray();
  // const result = await client.db(dbname).collection(colname).find({Name: /er$/}).toArray();

  console.log(JSON.stringify(result));
};
```

```bash
node --env-file .env query.js
```

## 9. 데이터 정렬해서 출력하기
sort.js
```js
const {MongoClient} = require('mongodb');

async function main(){
  const uri = process.env.DB_LOCAL_URL;
  // const uri = process.env.DB_ATLAS_URL;
  // console.log(uri);
  const client = new MongoClient(uri);
   try {
      await client.connect();
      await sortdocs(client, "mydb", "products");
   } finally {
      await client.close();
   }
};

main().catch(console.error);

async function sortdocs(client, dbname, colname){
   var mysort = { price: 1 };
  //  var mysort = { Name: -1 };
   const result = await client.db(dbname).collection(colname).find({}).sort(mysort).toArray();
   result.forEach(element => {
      console.log(element);
   });
};
```

```bash
node --env-file .env sort.js
```

## 10. 데이터 수정하기
update.js
```js
const {MongoClient} = require('mongodb');

async function main(){
  const uri = process.env.DB_LOCAL_URL;
  // const uri = process.env.DB_ATLAS_URL;
  // console.log(uri);
   const client = new MongoClient(uri);
   try {
      await client.connect();
      await sortdocs(client, "mydb", "products");
   } finally {
      await client.close();
   }
};

main().catch(console.error);

async function sortdocs(client, dbname, colname){
  //  var qry = { ProductID: 3 };
  //  var vals = { $set: { Name: "Router", price: 2750 } };
  //  const result = await client.db(dbname).collection(colname).updateOne(qry, vals);

   var qry = {Name: /er$/};
   var vals = { $inc: { price: 125 } };
   const result = await client.db(dbname).collection(colname).updateMany(qry, vals);

  console.log(result)
  console.log("Documents updated");
};
```

```bash
node --env-file .env update.js
```

## 11. limit
limit.js
```js
const {MongoClient} = require('mongodb');

async function main(){
  const uri = process.env.DB_LOCAL_URL;
  // const uri = process.env.DB_ATLAS_URL;
  // console.log(uri);
   const client = new MongoClient(uri);

   try {
      await client.connect();
      await limitdocs(client, "mydb", "orders");
   } finally {
      await client.close();
   }
};

main().catch(console.error);

async function limitdocs(client, dbname, colname){
   var myqry = {numPurchased:{$gte:10}};
   const result = await client.db(dbname).collection(colname).find({"numPurchased":{$gte:10}}).toArray();
  //  const result = await client.db(dbname).collection(colname).find({"numPurchased":{$gte:10}}).limit(1).toArray();
  // const result = await client.db(dbname).collection(colname).find({"numPurchased":{$gte:10}}).limit(1).skip(1).toArray();
   console.log(JSON.stringify(result));
};
```

```bash
node --env-file .env limit.js
```

## 12. 데이터 삭제하기
delete.js
```js
const {MongoClient} = require('mongodb');
async function main(){
  const uri = process.env.DB_LOCAL_URL;
  // const uri = process.env.DB_ATLAS_URL;
  // console.log(uri);

   const client = new MongoClient(uri);

   try {
      await client.connect();
      await deldocs(client, "mydb", "products");
   } finally {
      await client.close();
   }
};

main().catch(console.error);

async function deldocs(client, dbname, colname){
   var myqry = { Name: "TV" };
   const result = await client.db(dbname).collection(colname).deleteOne(myqry);
   console.log("Document Deleted");

  //  var myqry = {"price":{$gt:10000}};
  //  const result = await client.db(dbname).collection(colname).deleteMany(myqry);
  //  console.log("Documents Deleted");
};
```

```bash
node --env-file .env delete.js
```

## 13. 컬렉션 삭제하기
delete_collection.js
```js
const {MongoClient} = require('mongodb');

async function main(){
  const uri = process.env.DB_LOCAL_URL;
  // const uri = process.env.DB_ATLAS_URL;
  // console.log(uri);
   const client = new MongoClient(uri);

   try {
      await client.connect();
      await dropcol(client, "mydb", "products");
   } finally {
      await client.close();
   }
}
main().catch(console.error);


async function dropcol(client, dbname, colname){
  // const result = await client.db(dbname).collection(colname).drop();
  const result = await client.db(dbname).dropCollection(colname);
  console.log("Collection dropped");
}
```

```bash
node --env-file .env delete_collection.js
```