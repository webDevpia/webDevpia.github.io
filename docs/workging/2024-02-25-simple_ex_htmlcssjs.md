---
layout: default
# title: 404
# permalink: /404
nav_exclude: true
search_exclude: true
---
### Age Calculator
```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Age Calculator</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>나이 계산기</h1>
        <div class="form">
            <label for="birthday">생일을 입력하세요</label>
            <input type="date" id="birthday" name="birthday">
            <button id="btn">나이계산</button>
            <p id="result">당신의 나이는 21살입니다.</p>
        </div>
    </div>
    <script src="index.js"></script>
</body>
</html>
```
```css
/* style.css */
body {
  margin: 0;
  padding: 20px;
  font-family: "Montserrat", sans-serif;
  background-color: #f7f7f7;
}

.container {
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
  border-radius: 5px;
  margin-top: 50px;
}

h1 {
  font-size: 36px;
  text-align: center;
  margin-top: 0;
  margin-bottom: 20px;
}

.form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

label {
  font-weight: bold;
  margin-bottom: 10px;
}

input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  max-width: 300px;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  margin-top: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0062cc;
}

#result {
  margin-top: 20px;
  font-size: 24px;
  font-weight: bold;
}

```
```js
// index.js
const btnEl = document.getElementById("btn");
const birthdayEl = document.getElementById("birthday");
const resultEl = document.getElementById("result");

function calculateAge() {
  const birthdayValue = birthdayEl.value;
  if (birthdayValue === "") {
    alert("생일을 입력하세요");
  } else {
    const age = getAge(birthdayValue);
    resultEl.innerText = `당신의 나이는 ${age}살입니다.`;
  }
}

function getAge(birthdayValue) {
  const currentDate = new Date();
  const birthdayDate = new Date(birthdayValue);
  let age = currentDate.getFullYear() - birthdayDate.getFullYear();
  const month = currentDate.getMonth() - birthdayDate.getMonth();

  if (
    month < 0 ||
    (month === 0 && currentDate.getDate() < birthdayDate.getDate())
  ) {
    age--;
  }

  return age;
}

btnEl.addEventListener("click", calculateAge);
```

### animated search bar
```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Animated Search Bar</title>
    <script src="https://kit.fontawesome.com/발급받은kit.js" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div class="search-bar-container active">
      <i class="fas fa-magnifying-glass magnifier"></i>
      <!-- <img
        src="https://cdn4.iconfinder.com/data/icons/evil-icons-user-interface/64/magnifier-512.png"
        alt="magnifier"
        class="magnifier"
      /> -->
      <input type="text" class="input" placeholder="Search ..." />
      <img
        src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-25-512.png"
        alt="mic-icon"
        class="mic-icon"
      />
    </div>
    <script src="index.js"></script>
  </body>
</html>
```
```css
/* style.css */
body {
  margin: 0;
  display: flex;
  justify-content: center;
  height: 100vh;
  align-items: center;
  background-color: aliceblue;
}

.search-bar-container {
  display: flex;
  align-items: center;
  background-color: aliceblue;
  padding: 5px;
  width: 300px;
  height: 50px;
  border-radius: 50px;
  box-shadow: 6px 6px 10px rgba(0, 0, 0, 0.2),
    -6px -6px 10px rgba(255, 255, 255, 0.7);
  margin: 10px;
  position: relative;
  transition: width 1.5s;
}

.magnifier {
  color:cadetblue;
  width: 25px;
  cursor: pointer;
  position: absolute;
  left: 23px;
}

.mic-icon {
  width: 30px;
  position: absolute;
  right: 10px;
  transition: width 0.4s;
  transition-delay: 1s;
}

.input {
  background-color: transparent;
  border: none;
  margin: 10px 50px;
  width: 100%;
  outline: none;
  color: rgb(100, 100, 100);
  transition: width 1s;
  transition-delay: 0.5s;
}

.active.search-bar-container {
  width: 50px;
}

.active .input {
  width: 0;
}

.active .mic-icon {
  width: 0;
}

```
```js
// index.js
const searchBarContainerEl = document.querySelector(".search-bar-container");

const magnifierEl = document.querySelector(".magnifier");

magnifierEl.addEventListener("click", () => {
  searchBarContainerEl.classList.toggle("active");
});

```
### emoji rating
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Emoji Rating</title>
    <script src="https://kit.fontawesome.com/bcd94d8463.js" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div class="feedback-container">
      <div class="emoji-container">
        <i class="far fa-angry fa-3x"></i>
        <i class="far fa-frown fa-3x"></i>
        <i class="far fa-meh fa-3x"></i>
        <i class="far fa-smile fa-3x"></i>
        <i class="far fa-laugh fa-3x"></i>
      </div>
      <div class="rating-container">
        <i class="fas fa-star fa-2x active"></i>
        <i class="fas fa-star fa-2x"></i>
        <i class="fas fa-star fa-2x"></i>
        <i class="fas fa-star fa-2x"></i>
        <i class="fas fa-star fa-2x"></i>
      </div>
    </div>
    <script src="index.js"></script>
  </body>
</html>
```
```css
body {
  margin: 0;
  display: flex;
  justify-content: center;
  height: 100vh;
  align-items: center;
  background-color: yellow;
}

.feedback-container {
  background-color: white;
  width: 400px;
  height: 200px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  position: relative;
}

.emoji-container {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 20%;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  overflow: hidden;
}

.far {
  margin: 1px;
  transform: translateX(0);
  transition: transform 0.2s;
}

.rating-container {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 20%;
}

.fa-star {
  color: lightgray;
  cursor: pointer;
}

.fa-star.active {
  color: gold;
}

```
```js
const starsEl = document.querySelectorAll(".fa-star");
const emojisEl = document.querySelectorAll(".far");
const colorsArray = ["red", "orange", "lightblue", "lightgreen", "green"];

updateRating(0);

starsEl.forEach((starEl, index) => {
  starEl.addEventListener("click", () => {
    updateRating(index);
  });
});

function updateRating(index) {
  starsEl.forEach((starEl, idx) => {
    if (idx < index + 1) {
      starEl.classList.add("active");
    } else {
      starEl.classList.remove("active");
    }
  });

  emojisEl.forEach((emojiEl) => {
    emojiEl.style.transform = `translateX(-${index * 50}px)`;
    emojiEl.style.color = colorsArray[index];
  });
}

```

### heart trail animation
```html
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Heart Trail Animation</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <script src="index.js"></script>
  </body>
</html>
```

```css
body {
  margin: 0;
  height: 100vh;
  background-color: black;
  overflow: hidden;
}

span {
  background: url("https://cdn4.iconfinder.com/data/icons/general-office/91/General_Office_54-512.png");
  width: 100px;
  height: 100px;
  position: absolute;
  pointer-events: none;
  background-size: cover;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  animation: animate 6s linear;
}

@keyframes animate {
  0% {
    transform: translate(-50%, -50%);
    opacity: 1;
    filter: hue-rotate(0);
  }
  100% {
    transform: translate(-50%, -5000%);
    opacity: 0;
    filter: hue-rotate(720deg);
  }
}

```

```js
const bodyEl = document.querySelector("body");

bodyEl.addEventListener("mousemove", (event) => {
  const xPos = event.offsetX;
  const yPos = event.offsetY;
  const spanEl = document.createElement("span");
  spanEl.style.left = xPos + "px";
  spanEl.style.top = yPos + "px";
  const size = Math.random() * 100;
  spanEl.style.width = size + "px";
  spanEl.style.height = size + "px";
  bodyEl.appendChild(spanEl);
  setTimeout(() => {
    spanEl.remove();
  }, 3000);
});

```

### 내용 줄여서 표현
```html
  <!DOCTYPE html>
  <html lang="ko">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>CSS Grid Layout</title>
  </head>
  <body>
    <div id="wrapper">
      <div class="items">
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet, reprehenderit.Lorem ipsum dolor, sit amet consectetur adipisicing elit.</p> 
      </div>
      <div class="items">
        <p>Lorem ipsum dolor, sit amet consectetur adipisicing elit.Lorem ipsum dolor, sit amet consectetur adipisicing elit</p>
      </div>
      <div class="items">
        <p>
          Lorem ipsum dolor sit amet.Lorem ipsum dolor, sit amet consectetur adipisicing elit</p>
        </div>
      <div class="items">
        <p>Lorem ipsum dolor sit.Lorem ipsum dolor, sit amet consectetur adipisicing elit</p>
      </div>
      <div class="items">
        <p>Lorem, ipsum dolor.</p>
      </div>
    </div>
  </body>
  </html>
```
```css

     #wrapper{
      width:600px;
      display:grid;  /* 그리드 컨테이너 지정 */
      grid-template-columns:repeat(auto-fit, 200px);  /* 너비가 같은 칼럼 3개 */
      grid-template-rows: minmax(100px, auto);  /* 줄 높이 최소 100px */
    }
    .items{
      padding:10px;
      background-color:#eee;
      /* 한줄로 줄여서 표현 */
      /* white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis; */
    }   
    p{
      /* 특정 줄수만큼 줄이기 */
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .items:nth-child(odd){
      background-color:#bbb;
    }

```

### doto list
```html
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>To Do List</title>
    <script src="https://kit.fontawesome.com/개인키.js" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <form class="form">
      <input
        type="text"
        class="input"
        placeholder="Enter your task"
        autocomplete="off"
      />
      <ul class="list">
        <!-- <li>
          Buy Milk <i class="fas fa-check"></i
          ><i class="fas fa-trash-can"></i>
        </li>
        <li class="checked">
          Call David <i class="fas fa-check"></i
          ><i class="fas fa-trash-can"></i>
        </li> -->
      </ul>
    </form>
    <script src="index.js"></script>
  </body>
</html>
```
```css
body{
    margin: 0;
    display: flex;
    justify-content: center;
    background-color: rgb(140, 195, 229);
}

.form{
    position: absolute;
    top: 30%;
    box-shadow: 0 4px 8px rgba(0,0,0,.3);
    width: 400px;
    background-color:yellow;
    border-radius: 10px;
}

.input{
    width: 100%;
    box-sizing: border-box;
    padding: 20px;
    border-radius: 10px 10px 0 0;
    border: none;
    font-size: 20px;
    font-family: cursive;
}

.input::placeholder{
    color: lightgray;
}

.list{
    padding: 0;
    margin: 0;
}

.list li{
    list-style-type: none;
    padding: 20px;
    font-family: cursive;
    border-top: dotted;
    border-color: darkgray;
    position: relative;
}

.list li .fa-trash{
    color: red;
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
}
.list li .fa-check-square{
    color: green;
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
}

.list li.checked {
    color: darkgray;
    text-decoration: line-through;
}

.list li.checked .fa-check-square{
    color: darkgray;
}
```
```js
const formEl = document.querySelector(".form");

const inputEl = document.querySelector(".input");

const ulEl = document.querySelector(".list");

let list = JSON.parse(localStorage.getItem("list"));
if (list) {
  list.forEach((task) => {
    toDoList(task);
  });
}

formEl.addEventListener("submit", (event) => {
  event.preventDefault();
  toDoList();
});

function toDoList(task) {
  let newTask = inputEl.value;
  if (task) {
    newTask = task.name;
  }

  const liEl = document.createElement("li");
  if (task && task.checked) {
    liEl.classList.add("checked");
  }
  liEl.innerText = newTask;
  ulEl.appendChild(liEl);
  inputEl.value = "";
  const checkBtnEl = document.createElement("div");
  checkBtnEl.innerHTML = `
  <i class="fas fa-check-square">
  `;
  liEl.appendChild(checkBtnEl);
  const trashBtnEl = document.createElement("div");
  trashBtnEl.innerHTML = `
  <i class="fas fa-trash"></i>
  `;
  liEl.appendChild(trashBtnEl);

  checkBtnEl.addEventListener("click", () => {
    liEl.classList.toggle("checked");
    updateLocalStorage();
  });

  trashBtnEl.addEventListener("click", () => {
    liEl.remove();
    updateLocalStorage();
  });
  updateLocalStorage();
}

function updateLocalStorage() {
  const liEls = document.querySelectorAll("li");
  list = [];
  liEls.forEach((liEl) => {
    list.push({
      name: liEl.innerText,
      checked: liEl.classList.contains("checked"),
    });
  });
  localStorage.setItem("list", JSON.stringify(list));
}

```
### video trailer popup
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Video Trailer Popup</title>
     <script src="https://kit.fontawesome.com/개인키.js" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div class="main-container">
      <img
        src="https://images.pexels.com/photos/3062545/pexels-photo-3062545.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
        alt="movie-image"
      />
      <h1>Movie Title</h1>
      <p>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Illum iste
        necessitatibus porro explicabo illo dolorum dolores cupiditate non modi
        quasi nobis, earum ab, autem esse vero sapiente minus vel! Provident?
      </p>
      <button class="btn">Watch now</button>
    </div>
    <div class="trailer-container active">
      <video src="trailer.mp4" controls="true"></video>
      <i class="fas fa-times fa-2x close-icon"></i>
    </div>
    <script src="index.js"></script>
  </body>
</html>

```
```css
body {
  margin: 0;
  box-sizing: border-box;
  font-family: sans-serif;
  display: flex;
  justify-content: center;
  height: 100vh;
  align-items: center;
  background-color: black;
}

.main-container {
  max-width: 550px;
  padding: 10px;
}

.main-container img {
  max-width: 100%;
  margin-bottom: 15px;
  border-radius: 10px;
}

.main-container h1 {
  color: white;
  font-weight: 500;
}

.main-container p {
  color: white;
  margin: 15px 0;
}

.btn {
  background-color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
}

.btn:hover {
  background-color: orange;
}

.trailer-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: black;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 1;
  transition: opacity 0.7s;
}

.active.trailer-container {
  visibility: hidden;
  opacity: 0;
}

.trailer-container video {
  position: relative;
  max-width: 900px;
  outline: none;
}

@media (max-width: 991px) {
  .trailer-container video {
    max-width: 90%;
  }
}

.close-icon {
  position: absolute;
  top: 30px;
  right: 30px;
  color: white;
  cursor: pointer;
}

```
```js
const btnEl = document.querySelector(".btn");
const closeIconEl = document.querySelector(".close-icon");
const trailerContainerEl = document.querySelector(".trailer-container");
const videoEl = document.querySelector("video");

btnEl.addEventListener("click", () => {
  trailerContainerEl.classList.remove("active");
});

closeIconEl.addEventListener("click", () => {
  trailerContainerEl.classList.add("active");
  videoEl.pause();
  videoEl.currentTime = 0;
});

```