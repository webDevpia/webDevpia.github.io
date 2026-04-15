---
title: 11. to-do list app
layout: default
grand_parent: Language
parent: React
nav_order: 11
has_children: false
permalink: /language/react/react_11
---
### 15. to-do list app

src/App.jsx
```jsx
import ToDoList from './15/ToDoList'

export default function App() {

  return (
    <>
      <ToDoList/>
    </>
  )
}
```

src/15/ToDoList.jsx
```jsx
import { useState } from "react";

export default function ToDoList(){

  const [tasks,setTasks] = useState(["Eat Breakfast","Take a shower","walk the dog"]);
  const [newTask,setNewTask] = useState("");

  function handleInputChange(event){
    setNewTask(event.target.value);
  }

  function addTask(){
    if(newTask.trim() !== ""){
      setTasks(t => [...t, newTask]);
      setNewTask("");
    }
  }

  function deleteTask(index){
    const updatedTasks = tasks.filter((_, i) => i !== index);
    setTasks(updatedTasks);
  }

  function moveTaskUp(index){
    if(index > 0){
      const updatedTasks = [...tasks];
      [updatedTasks[index],updatedTasks[index - 1]] = 
      [updatedTasks[index - 1],updatedTasks[index]];
      setTasks(updatedTasks);
    }
  }

  function moveTaskDown(index){
    if(index < tasks.length - 1 ){
      const updatedTasks = [...tasks];
      [updatedTasks[index],updatedTasks[index + 1]] = 
      [updatedTasks[index + 1],updatedTasks[index]];
      setTasks(updatedTasks);
    }
  }

  return(
    <div className="flex flex-col items-center min-h-screen bg-slate-100 font-sans p-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-6 mt-10">
        <h1 className="text-4xl font-bold text-slate-800 text-center mb-6">To-Do-List</h1>
        
        <div className="flex gap-2 mb-6">
          <input 
            type="text" 
            placeholder="Enter a task..." 
            value={newTask} 
            onChange={handleInputChange}
            className="flex-grow p-3 border-2 border-slate-300 rounded-lg focus:outline-none focus:border-cyan-500 transition-colors"
          />
          <button 
            className="px-6 py-3 rounded-lg font-semibold hover:bg-cyan-600 transition-colors disabled:bg-slate-300" 
            onClick={addTask}
            disabled={!newTask.trim()}
          >
          Add
          </button>
        </div>

        <ol className="space-y-3">
          {tasks.map((task,index) =>
            <li key={index} className="flex items-center bg-slate-50 p-3 rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <span className="flex-grow text-slate-700 text-lg">{task}</span>
              <div className="flex gap-2 ml-4">
                <button className="text-slate-500 hover:text-slate-700 transition-colors text-xl" onClick={()=> moveTaskUp(index)}>👆</button>
                <button className="text-slate-500 hover:text-slate-700 transition-colors text-xl" onClick={()=> moveTaskDown(index)}>👇</button>
                <button className="text-red-500 hover:text-red-700 transition-colors font-bold text-xl" onClick={()=> deleteTask(index)}>🗑️</button>
              </div>
            </li>
          )}
        </ol>
      </div>
    </div>
  );
}
```