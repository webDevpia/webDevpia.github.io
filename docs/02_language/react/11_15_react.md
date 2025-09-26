---
title: React 15
layout: default
grand_parent: Language
parent: React
nav_order: 15
has_children: false
permalink: /language/react/react_15
---
### 21. axios

#### server

프로젝트 생성
```bash
mkdir server
cd server
npm init -y
npm i express mongoose axios cors mongoose-sequence
npm i nodemon -D
```

package.json 수정
```
  "scripts":{
    "start": "nodemon index.js"
  },
```

Models/Todo.js 생성
```js
const mongoose = require('mongoose')
const AutoIncrement = require("mongoose-sequence")(mongoose);

const TodoSchema = new mongoose.Schema({
  // id 필드는 스키마에서 안만들어도 plugin()에서 설정하면 해당 필드 자동 생성
  task: {type: String},
  done: {
    type: Boolean,
    default: false
  }},{
    // mongoose를 통해서 데이터를 삽입하면 '__v' 필드가 생긴다. 
    // 의미하는 바는 버전 키라고 하는데 문서의 내부 개정판을 설명하고 기본 값은 0이다.
    // 삭제할려면 versionKey값을 false로 설정
    versionKey: false }
)
TodoSchema.plugin(AutoIncrement,{inc_field:"id"})

module.exports = mongoose.model("Todo",TodoSchema)
```

index.js 생성
```jsx
const express = require('express')
const mongoose = require('mongoose')
const cors = require('cors')
const Todo = require('./Models/Todo')

const app = express()
app.use(cors())
app.use(express.json())

// mongoose.connect('mongodb://localhost:27017/todolist')
mongoose.connect(process.env.DB_CONN)

app.get('/get',async(req,res)=>{
  const todos = await Todo.find()
  console.log('/get 호출')
  console.log(todos)
  res.json(todos)
})

app.put('/update/:id', async(req,res) => {
  const {id} = req.params
  const todo = await Todo.findById(id)
  todo.done = !todo.done
  todo.save()
  console.log('/update/:id 호출')
  console.log(todo)
  res.json(todo)
})

app.delete('/delete/:id',async(req,res)=>{
  const {id} = req.params
  const todos = await Todo.findByIdAndDelete({_id:id})
  console.log('/delete/:id 호출')
  console.log(todos)
  res.json(todos)
})

app.post('/add',async(req,res) => {
  const task = req.body.task;
  const todos = await Todo.create({task:task})
  console.log('/add 호출')
  console.log(todos)
  res.json(todos)
})

app.listen(3001,() => {
  console.log("Server is Running!")
})
```

#### server koyeb 배포하기

##### 1. github에 올리기

.gitignore 파일 작성해서 node_modules는 제외시키고 server폴더를 기준으로 git init 해서 github에 올려준다.

![](/img/react001.png)

##### 2. koyeb 배포

로그인 해서 overview에서 'Create Web Service' 클릭
![](/img/react002.png)

'GitHub' 클릭
![](/img/react003.png)

소스 올린 리파지토리 선택
![](/img/react004.png)

Run Command - npm i;npm start 설정
![](/img/react005.png)

Advanced에서 Environment variables에 몽고DB 서버 연결 URL 작성     
Port를 3001번으로 코드에 셋팅했으므로 맞게 설정.   
App name 값도 입력  
deploy 버튼 클릭  
![](/img/react007.png)

배포작업이 진행되고  
![](/img/react008.png)

로그에 서버가 Started 되는 메시지 확인  
![](/img/react009.png)


##### 3. vscode 에서 확인
![](/img/react010.png)
![](/img/react011.png)
![](/img/react012.png)
![](/img/react013.png)

##### 4. koyeb에 배포한 서비스 삭제할 경우
![](/img/react014.png)


#### client

**프로젝트 생성**

```bash
npm create vite@latest
# project -> 이름: client, react, javascript 로 생성 
cd client
npm i
npm i axios
npm i tailwindcss @tailwindcss/vite
npm run dev
```

**vite.config.ts 파일 설정**  

```js{% raw %}
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
}){% endraw %}
```

**index.css에 @tailwindcss의 각 레이어에 대한 지시문을 파일에 추가**

```css
@import "tailwindcss";
```

src/App.jsx
```jsx
import Home from './Home'

export default function App() {
  return (
    <>
      <Home/>
    </>
  )
}
```

src/Home.jsx
```jsx
import { useState, useEffect, useRef } from "react"
import axios from 'axios'
import './Home.css'

export default function Home(){
  const [todos,setTodos] = useState([])
  const [task,setTask] = useState("")

  const inputRef = useRef()

  useEffect(() => {
    async function getData(){
      const result = await axios.get('http://localhost:3001/get')
      setTodos(result.data)
      inputRef.current.focus()  
    }
    getData()
  },[])

  const handleAdd = async () => {
    await axios.post('http://localhost:3001/add',{task:task})
    const result = await axios.get('http://localhost:3001/get')
    setTodos(result.data) 
    inputRef.current.value = ""
    inputRef.current.focus()
  }

  const handleEdit = async (id) => {
    await axios.put('http://localhost:3001/update/'+id)
    const result = await axios.get('http://localhost:3001/get')
    setTodos(result.data)  
  }

  const handleDelete = async (id) => {
    await axios.delete('http://localhost:3001/delete/'+id)
    const result = await axios.get('http://localhost:3001/get')
    setTodos(result.data)  
  }

  return(
    <div className="home">
      <h2>Todo List</h2>
      <div className="create_form">
      <input type="text" placeholder="Enter Task" 
            onChange={(e) => setTask(e.target.value)}
            ref={inputRef}/>
      <button onClick={handleAdd}>Add</button>
      </div>
      {
        todos.length === 0
        ?
        <div><h2>No Record</h2></div>
        :
        todos.map(todo => (
          <div className="task" key = {todo._id}>
            <input type="checkbox" 
                  onChange={ () => handleEdit(todo._id)}
                  checked={todo.done ? "checked" : ""}/>
            <p className={todo.done ? "line_through" : ""}>{todo.task}</p>
            <div>
              <button onClick={() => handleDelete(todo._id)}> Delete </button>
            </div>
          </div>
        ))
      }
    </div>
  )
}
```

src/Home.css
```css
.home{
  display: flex;
  flex-direction: column;
  align-items: center;
}
.create_form input{
  width: 300px;
  padding: 10px;
  border-bottom: 2px solid;
  outline: none;
  margin-bottom: 10px;
}
.create_form button{
  padding: 10px;
  background-color: hsl(0, 0%, 15%);
  color: rgb(209, 206, 206);
  cursor: pointer;
}
.task{
  display: flex;
  align-items: center;
  width: 360px;
  justify-content: space-between;
  background-color: hsl(0, 0%, 15%);
  color: rgb(208, 204, 204);
  height: 35px;
  padding: 2px 5px 2px 5px;
  margin-top: 2px;
}
.line_through{
  text-decoration: line-through;
}
button ,input[type="checkbox"]{
  cursor: pointer;
}
```

#### client netlify 배포

##### 1. axios쪽 접속 url은 koyeb에 배포한 url로 수정한다. 

##### 2. github 레파지토리 생성 후 client 코드 올려준다.

##### 3. import from Git 클릭
![](/img/react015.png)

##### 4. Deploy with GitHub 클릭
![](/img/react016.png)

##### 5. 레파지토리 선택
![](/img/react018.png)

##### 6. Site name 항목 입력후 중복체크 후, Deploy 사이트명 클릭
![](/img/react019.png)

##### 7. 성공메시지 창이 나타남.
![](/img/react020.png)

##### 8. 배포 내역 확인
![](/img/react021.png)
