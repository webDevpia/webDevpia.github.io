---
title: 04. Props — 데이터 전달
layout: default
parent: React (리뉴얼)
nav_order: 5
permalink: /language/react-new/props
---

{% raw %}

# 04장. Props — 컴포넌트 간 데이터 전달

> "Props = 택배 — 보내는 사람(부모)이 내용물을 결정하고, 받는 사람(자식)은 열어서 사용합니다."

택배를 생각해보세요. 보내는 사람이 상자에 물건을 넣어서 보냅니다. 받는 사람은 상자를 열어 물건을 꺼내 씁니다. 받는 사람이 상자 안 물건을 바꿀 수는 없고, 본인이 받은 것을 쓸 뿐입니다. React의 Props도 이와 같습니다.

---

## 학습 목표

- Props가 무엇인지, 왜 필요한지 이해한다
- 여러 개의 Props를 컴포넌트에 전달할 수 있다
- 구조분해 할당으로 Props를 편리하게 사용할 수 있다
- ES6 기본값으로 Props 기본값을 설정할 수 있다
- `children` Props로 컴포넌트를 감싸는 방법을 안다
- Props가 읽기 전용임을 이해한다
- React DevTools로 Props를 실시간 확인할 수 있다

---

<a id="toc"></a>
## 진행 순서
1. [Props란?](#1)
2. [여러 개의 Props 전달하기](#2)
3. [기본값 설정 (ES6 기본 매개변수)](#3)
4. [children Props](#4)
5. [Props는 읽기 전용](#5)
6. [React DevTools로 Props 확인하기](#6)
7. [실습: 학생 카드 컴포넌트](#7)
8. [정리](#summary)

---

<a id="1"></a>
## 1️⃣ Props란? [↑](#toc)

### 문제: 하드코딩된 컴포넌트

지난 장에서 만든 `ProfileCard`는 항상 "홍길동"의 정보만 보여줬습니다. 카드 10개가 필요하면 동일한 컴포넌트를 10번 복붙하고 이름을 하나씩 바꿔야 합니다.

```jsx
// 이런 식으로 하면 안 됩니다 — 코드 중복
function AliceCard() {
  return <div className="...">Alice</div>;
}

function BobCard() {
  return <div className="...">Bob</div>;
}

function CharlieCard() {
  return <div className="...">Charlie</div>;
}
```

### 고통: 디자인 변경 시 모든 컴포넌트를 수정해야 합니다

둥근 모서리 크기를 `rounded-xl`에서 `rounded-2xl`로 바꾸려면 위의 세 함수를 모두 수정해야 합니다. 30개라면 30번입니다.

### 해결: Props로 데이터를 외부에서 주입

**일반 함수의 매개변수와 똑같습니다.**

```javascript
// 일반 함수 — 매개변수로 데이터를 받습니다
function greet(name, age) {
  return `안녕하세요, ${name}님 (${age}세)!`;
}

greet("Alice", 25);
greet("Bob", 30);
```

```jsx
// React 컴포넌트 — Props로 데이터를 받습니다
function GreetCard(props) {
  return (
    <div className="p-4 border rounded-lg">
      <h2>안녕하세요, {props.name}님 ({props.age}세)!</h2>
    </div>
  );
}

// 사용할 때 — HTML 속성처럼 전달합니다
<GreetCard name="Alice" age={25} />
<GreetCard name="Bob" age={30} />
```

### Props 전달 방법

```jsx
{/* 문자열은 따옴표 */}
<Card name="홍길동" />

{/* 숫자, 불리언, 배열, 객체, 함수는 중괄호 */}
<Card age={25} />
<Card isAdmin={true} />
<Card skills={["React", "CSS"]} />
<Card user={{ name: "Alice", age: 25 }} />
<Card onClick={() => console.log("클릭!")} />

{/* 불리언 true는 속성 이름만 써도 됩니다 */}
<Card isAdmin />       {/* isAdmin={true}와 동일 */}
<Card isAdmin={false} />  {/* false는 명시해야 합니다 */}
```

### 구조분해로 더 간결하게

```jsx
// props 객체를 그대로 받는 방식
function GreetCard(props) {
  return <h2>{props.name} ({props.age}세)</h2>;
}

// 매개변수에서 바로 구조분해 — 더 간결하고 읽기 쉽습니다
function GreetCard({ name, age }) {
  return <h2>{name} ({age}세)</h2>;
}
```

이 강의에서는 구조분해 방식을 사용합니다.

---

<a id="2"></a>
## 2️⃣ 여러 개의 Props 전달하기 [↑](#toc)

### StudentCard 컴포넌트 만들기

학생 카드 컴포넌트에 이름, 나이, 학과, 사진, 성적 정보를 Props로 전달해봅시다.

```jsx
// src/components/StudentCard.jsx
function StudentCard({ name, age, department, imageUrl, gpa }) {
  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden">
      {/* 상단 이미지 영역 */}
      <div className="h-36 bg-gradient-to-br from-blue-400 to-indigo-600 flex items-end p-4">
        <img
          src={imageUrl}
          alt={name}
          className="w-16 h-16 rounded-full border-3 border-white shadow-lg object-cover"
        />
      </div>

      {/* 정보 영역 */}
      <div className="p-5">
        <h3 className="text-lg font-bold text-gray-900">{name}</h3>
        <p className="text-sm text-gray-500 mt-0.5">{department} · {age}세</p>

        {/* 성적 배지 */}
        <div className="mt-3 flex items-center gap-2">
          <span className="text-xs text-gray-500">평균 학점</span>
          <span className="bg-blue-100 text-blue-800 text-sm font-bold px-2 py-0.5 rounded-full">
            {gpa.toFixed(2)}
          </span>
        </div>
      </div>
    </div>
  );
}

export default StudentCard;
```

```jsx
// src/App.jsx — 다른 Props로 같은 컴포넌트를 재사용합니다
import StudentCard from "./components/StudentCard";

function App() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">학생 목록</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <StudentCard
          name="김민지"
          age={21}
          department="컴퓨터공학과"
          imageUrl="https://i.pravatar.cc/150?img=1"
          gpa={3.85}
        />
        <StudentCard
          name="박준호"
          age={23}
          department="경영학과"
          imageUrl="https://i.pravatar.cc/150?img=2"
          gpa={3.42}
        />
        <StudentCard
          name="이수연"
          age={22}
          department="디자인학과"
          imageUrl="https://i.pravatar.cc/150?img=3"
          gpa={4.1}
        />
      </div>
    </div>
  );
}

export default App;
```

컴포넌트 하나를 만들고, 다른 데이터로 세 번 재사용했습니다. 이제 카드 디자인을 바꾸려면 `StudentCard.jsx` 하나만 수정하면 됩니다.

---

<a id="3"></a>
## 3️⃣ 기본값 설정 (ES6 기본 매개변수) [↑](#toc)

### Props가 전달되지 않으면?

```jsx
function StudentCard({ name, age, department, gpa }) {
  return (
    <div>
      <h3>{name}</h3>
      <p>{department}</p>
    </div>
  );
}

// age와 department를 전달하지 않으면
<StudentCard name="홍길동" gpa={3.5} />
// age → undefined, department → undefined
// 화면에 아무것도 표시되지 않거나, 에러가 생길 수 있습니다
```

### ES6 기본 매개변수로 기본값 설정

```jsx
// React 19부터는 PropTypes가 제거되었습니다.
// 대신 ES6 기본 매개변수(default parameters)를 사용합니다.

function StudentCard({
  name,
  age = 20,                    // 기본값: 20
  department = "학과 미기재",  // 기본값: "학과 미기재"
  imageUrl = "https://i.pravatar.cc/150", // 기본값: 기본 이미지
  gpa = 0,                     // 기본값: 0
}) {
  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden">
      <div className="h-36 bg-gradient-to-br from-blue-400 to-indigo-600 flex items-end p-4">
        <img
          src={imageUrl}
          alt={name}
          className="w-16 h-16 rounded-full border-3 border-white shadow-lg object-cover"
        />
      </div>
      <div className="p-5">
        <h3 className="text-lg font-bold text-gray-900">{name}</h3>
        <p className="text-sm text-gray-500 mt-0.5">{department} · {age}세</p>
        <div className="mt-3 flex items-center gap-2">
          <span className="text-xs text-gray-500">평균 학점</span>
          <span className="bg-blue-100 text-blue-800 text-sm font-bold px-2 py-0.5 rounded-full">
            {gpa.toFixed(2)}
          </span>
        </div>
      </div>
    </div>
  );
}
```

이제 `age`나 `department`를 전달하지 않아도 기본값이 표시됩니다.

```jsx
{/* age, department 없이도 동작합니다 */}
<StudentCard name="홍길동" gpa={3.5} />
{/* 결과: 나이 20세, "학과 미기재" */}
```

### Props 타입에 따른 기본값 패턴

```jsx
function WeatherCard({
  city = "알 수 없음",          // 문자열 기본값
  temp = 0,                    // 숫자 기본값
  humidity = 0,
  isRaining = false,           // 불리언 기본값
  forecast = [],               // 배열 기본값
  unit = "°C",
}) {
  return (
    <div className="bg-white rounded-xl p-6 shadow-md">
      <h2 className="text-xl font-bold text-gray-800">{city}</h2>
      <p className="text-5xl font-thin text-blue-600 mt-2">
        {temp}{unit}
      </p>
      <p className="text-gray-500 mt-2">습도: {humidity}%</p>
      {isRaining && (
        <p className="text-blue-500 mt-1 flex items-center gap-1">
          🌧️ 비가 내리고 있습니다
        </p>
      )}
    </div>
  );
}
```

---

<a id="4"></a>
## 4️⃣ children Props [↑](#toc)

### children이란?

컴포넌트 태그 사이에 넣은 내용이 자동으로 `children` Props로 전달됩니다. 감싸는 레이아웃 컴포넌트를 만들 때 매우 유용합니다.

```jsx
// children을 사용하는 Card 컴포넌트
function Card({ children, className = "" }) {
  return (
    <div className={`bg-white rounded-xl shadow-md p-6 ${className}`}>
      {children}
    </div>
  );
}
```

```jsx
// 사용 방법 — 태그 사이에 원하는 내용을 넣습니다
function App() {
  return (
    <div className="p-8 grid gap-4">
      {/* 어떤 내용이든 Card 안에 넣을 수 있습니다 */}
      <Card>
        <h2 className="font-bold text-lg">날씨 정보</h2>
        <p className="text-gray-600">서울: 22°C</p>
      </Card>

      <Card className="border-l-4 border-blue-500">
        <h2 className="font-bold text-lg">공지사항</h2>
        <p className="text-gray-600">내일 강의가 있습니다.</p>
        <button className="mt-2 text-blue-600 text-sm hover:underline">
          자세히 보기
        </button>
      </Card>

      <Card>
        <img src="weather.jpg" alt="날씨" className="w-full rounded-lg" />
      </Card>
    </div>
  );
}
```

### children의 실제 타입

`children`은 React가 렌더링할 수 있는 모든 것이 될 수 있습니다.

```jsx
// 문자열
<Card>안녕하세요</Card>

// JSX 요소
<Card><h1>제목</h1></Card>

// 여러 요소
<Card>
  <h1>제목</h1>
  <p>내용</p>
</Card>

// 다른 컴포넌트
<Card>
  <StudentCard name="Alice" gpa={3.9} />
</Card>
```

### 실용적인 레이아웃 컴포넌트

```jsx
// src/components/Section.jsx
function Section({ title, children, className = "" }) {
  return (
    <section className={`py-8 ${className}`}>
      {title && (
        <h2 className="text-2xl font-bold text-gray-800 mb-6">{title}</h2>
      )}
      {children}
    </section>
  );
}

export default Section;
```

```jsx
// App.jsx에서 사용
import Section from "./components/Section";
import StudentCard from "./components/StudentCard";

function App() {
  return (
    <div className="max-w-5xl mx-auto px-4">
      <Section title="재학생 목록">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <StudentCard name="김민지" gpa={3.85} />
          <StudentCard name="박준호" gpa={3.42} />
          <StudentCard name="이수연" gpa={4.1} />
        </div>
      </Section>

      <Section title="공지사항" className="bg-yellow-50 px-6 rounded-xl">
        <p>다음 주 중간고사 일정이 확정되었습니다.</p>
      </Section>
    </div>
  );
}
```

---

<a id="5"></a>
## 5️⃣ Props는 읽기 전용 [↑](#toc)

### 규칙: 자식은 Props를 수정할 수 없습니다

택배 비유로 돌아가봅시다. 받는 사람(자식 컴포넌트)이 택배 상자를 열어 물건을 쓰는 것은 괜찮습니다. 하지만 보내는 사람(부모)의 창고에 있는 원본을 바꾸는 것은 불가능합니다.

```jsx
// ❌ 잘못된 예 — Props를 수정하려고 하면 안 됩니다
function BadCounter({ count }) {
  // 에러! Props는 읽기 전용입니다
  count = count + 1;  // 에러는 안 나지만 부모의 상태를 바꾸지 못합니다
  return <p>{count}</p>;
}

// ✅ 올바른 예 — 새 변수를 만들어서 사용합니다
function GoodCounter({ count }) {
  const displayCount = count + 1; // 새 변수에 계산 결과를 담습니다
  return <p>{displayCount}</p>;
}
```

### 왜 읽기 전용인가요?

데이터 흐름이 한 방향(부모 → 자식)으로 흘러야 앱의 상태를 예측하기 쉽습니다. 자식이 Props를 마음대로 바꿀 수 있다면 어디서 값이 바뀌었는지 추적하기 어렵습니다.

자식 컴포넌트가 부모의 데이터를 바꾸고 싶다면? → **함수를 Props로 전달**합니다.

```jsx
// 부모에서 함수를 전달합니다
function App() {
  function handleDelete(id) {
    console.log(`${id}번 항목 삭제`);
    // 실제 삭제 로직은 여기서 처리합니다
  }

  return (
    <StudentCard
      name="김민지"
      id={1}
      onDelete={handleDelete}  // 함수를 Props로 전달
    />
  );
}

// 자식에서 전달받은 함수를 호출합니다
function StudentCard({ name, id, onDelete }) {
  return (
    <div className="bg-white rounded-xl p-5 shadow-md">
      <h3 className="font-bold text-gray-900">{name}</h3>
      <button
        onClick={() => onDelete(id)}  // 부모의 함수를 호출
        className="mt-3 text-red-500 hover:text-red-700 text-sm"
      >
        삭제
      </button>
    </div>
  );
}
```

이 패턴은 이벤트 처리 장(07장)에서 더 자세히 다룹니다.

---

<a id="6"></a>
## 6️⃣ React DevTools로 Props 확인하기 [↑](#toc)

Props를 제대로 전달하고 있는지 확인하는 가장 좋은 방법은 React DevTools입니다.

### DevTools에서 Props 확인 방법

1. 브라우저에서 `F12`를 눌러 개발자 도구를 엽니다
2. **Components** 탭을 클릭합니다
3. 컴포넌트 트리에서 `StudentCard`를 클릭합니다
4. 오른쪽 패널에서 Props 섹션을 확인합니다

**확인할 수 있는 것들:**

```
Props
  name: "김민지"
  age: 21
  department: "컴퓨터공학과"
  gpa: 3.85
  imageUrl: "https://i.pravatar.cc/150?img=1"
```

### DevTools 활용 팁

**Props가 `undefined`로 보인다면?**
- 부모에서 Props 이름이 정확한지 확인합니다 (`gpa` vs `GPA`)
- 철자 오류가 있는지 확인합니다

**Props 값이 예상과 다르다면?**
- 부모 컴포넌트도 클릭해서 어떤 값을 내려보내는지 확인합니다

**트리에서 컴포넌트를 바로 선택하는 팁:**
- DevTools 상단의 "Select an element" 버튼(화살표 아이콘)을 클릭합니다
- 화면에서 원하는 컴포넌트를 클릭하면 자동으로 선택됩니다

---

<a id="7"></a>
## 7️⃣ 실습: 학생 카드 컴포넌트 [↑](#toc)

지금까지 배운 Props 개념을 종합하여 완성도 높은 학생 카드 목록을 만들어봅시다.

### 데이터 분리하기

실제 앱에서는 데이터를 별도 파일로 관리합니다.

```javascript
// src/data/students.js
const students = [
  {
    id: 1,
    name: "김민지",
    age: 21,
    department: "컴퓨터공학과",
    year: 3,
    gpa: 3.85,
    imageUrl: "https://i.pravatar.cc/150?img=1",
    skills: ["Python", "React", "SQL"],
    isHonor: true,
  },
  {
    id: 2,
    name: "박준호",
    age: 23,
    department: "경영학과",
    year: 4,
    gpa: 3.42,
    imageUrl: "https://i.pravatar.cc/150?img=2",
    skills: ["Excel", "PowerPoint", "데이터 분석"],
    isHonor: false,
  },
  {
    id: 3,
    name: "이수연",
    age: 22,
    department: "디자인학과",
    year: 2,
    gpa: 4.1,
    imageUrl: "https://i.pravatar.cc/150?img=3",
    skills: ["Figma", "Illustrator", "Photoshop"],
    isHonor: true,
  },
  {
    id: 4,
    name: "최동현",
    age: 20,
    department: "전기공학과",
    year: 1,
    gpa: 2.98,
    imageUrl: "https://i.pravatar.cc/150?img=4",
    skills: ["C언어", "회로이론"],
    isHonor: false,
  },
];

export default students;
```

### 완성된 StudentCard 컴포넌트

```jsx
// src/components/StudentCard.jsx
function StudentCard({
  name,
  age = 20,
  department = "학과 미기재",
  year = 1,
  gpa = 0,
  imageUrl = "https://i.pravatar.cc/150",
  skills = [],
  isHonor = false,
}) {
  // GPA에 따른 배지 색상
  const gpaBadgeClass =
    gpa >= 4.0 ? "bg-purple-100 text-purple-800" :
    gpa >= 3.5 ? "bg-green-100 text-green-800" :
    gpa >= 3.0 ? "bg-blue-100 text-blue-800" :
                 "bg-gray-100 text-gray-700";

  return (
    <div className="bg-white rounded-2xl shadow hover:shadow-lg transition-shadow overflow-hidden">
      {/* 상단 배너 */}
      <div className="h-24 bg-gradient-to-r from-blue-500 to-indigo-600 relative">
        {isHonor && (
          <span className="absolute top-3 right-3 bg-yellow-400 text-yellow-900 text-xs font-bold px-2 py-1 rounded-full">
            🏅 우등생
          </span>
        )}
      </div>

      {/* 아바타 */}
      <div className="px-5">
        <img
          src={imageUrl}
          alt={name}
          className="-mt-10 w-20 h-20 rounded-full border-4 border-white shadow-md object-cover"
        />
      </div>

      {/* 정보 */}
      <div className="px-5 pb-5 mt-2">
        <h3 className="text-lg font-bold text-gray-900">{name}</h3>
        <p className="text-sm text-gray-500 mt-0.5">
          {department} {year}학년 · {age}세
        </p>

        {/* GPA */}
        <div className="mt-3 flex items-center gap-2">
          <span className="text-xs text-gray-400">학점</span>
          <span className={`text-sm font-bold px-2.5 py-0.5 rounded-full ${gpaBadgeClass}`}>
            {gpa.toFixed(2)} / 4.5
          </span>
        </div>

        {/* 기술 스택 */}
        {skills.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1.5">
            {skills.map(skill => (
              <span
                key={skill}
                className="bg-gray-100 text-gray-700 text-xs px-2.5 py-1 rounded-full"
              >
                {skill}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default StudentCard;
```

### App에서 데이터를 Props로 전달하기

```jsx
// src/App.jsx
import students from "./data/students";
import StudentCard from "./components/StudentCard";

function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      {/* 헤더 */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-900">학생 관리 시스템</h1>
          <span className="text-sm text-gray-500">총 {students.length}명</span>
        </div>
      </header>

      {/* 학생 목록 */}
      <main className="max-w-5xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {students.map(student => (
            <StudentCard
              key={student.id}
              name={student.name}
              age={student.age}
              department={student.department}
              year={student.year}
              gpa={student.gpa}
              imageUrl={student.imageUrl}
              skills={student.skills}
              isHonor={student.isHonor}
            />
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
```

### 스프레드로 Props 전달 간소화

Props를 하나씩 열거하는 대신 스프레드 연산자로 한 번에 전달할 수 있습니다.

```jsx
{/* 풀어서 전달 — 반복적 */}
<StudentCard
  key={student.id}
  name={student.name}
  age={student.age}
  department={student.department}
  year={student.year}
  gpa={student.gpa}
  imageUrl={student.imageUrl}
  skills={student.skills}
  isHonor={student.isHonor}
/>

{/* 스프레드로 전달 — 간결 */}
<StudentCard key={student.id} {...student} />
```

> 주의: 스프레드 방식은 필요 없는 Props까지 전달될 수 있습니다. 꼭 필요한 Props만 있을 때 사용하세요.

---

## 🔍 React DevTools로 확인

앱을 실행하고 DevTools의 Components 탭을 열어보세요.

```
App
├── header
│   └── ...
└── main
    ├── StudentCard  ← 클릭하면 Props 확인
    │   Props
    │   ├── name: "김민지"
    │   ├── age: 21
    │   ├── gpa: 3.85
    │   ├── isHonor: true
    │   └── skills: Array(3)
    ├── StudentCard
    ├── StudentCard
    └── StudentCard
```

---

## 실습 과제

### 기본 과제

`students.js`에 자신의 정보를 추가하고 카드가 화면에 표시되는지 확인하세요.
- `id`는 기존 최댓값 + 1
- `isHonor`는 GPA 3.5 이상이면 `true`

### 도전 과제

**우등생 필터** 기능을 추가해보세요.

힌트: `students.filter(s => s.isHonor)` — 이 결과를 `map`에 전달합니다.

```jsx
// App.jsx에 아래를 추가해보세요
const honorStudents = students.filter(s => s.isHonor);

// 별도 섹션으로 표시합니다
<section>
  <h2 className="text-xl font-bold mb-4">🏅 우등생 ({honorStudents.length}명)</h2>
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
    {honorStudents.map(student => (
      <StudentCard key={student.id} {...student} />
    ))}
  </div>
</section>
```

---

<a id="summary"></a>
## 정리 [↑](#toc)

| 개념 | 설명 | 예시 |
|------|------|------|
| Props 전달 | HTML 속성처럼 | `<Card name="Alice" age={25} />` |
| Props 받기 | 구조분해 매개변수 | `function Card({ name, age })` |
| 기본값 | ES6 기본 매개변수 | `function Card({ age = 20 })` |
| children | 태그 사이 내용 | `<Card><p>내용</p></Card>` |
| 읽기 전용 | 자식은 Props 수정 불가 | 새 변수를 만들어 사용 |

**Props로 데이터를 전달했지만 아직 한 가지 문제가 남아 있습니다.** 학생이 30명이라면 30개의 `<StudentCard ... />`를 직접 써야 할까요? 그렇지 않습니다. 이미 이 장의 App.jsx 코드에서 `map`을 살짝 사용해봤습니다. 다음 장에서는 **배열과 map()을 이용한 리스트 렌더링**을 본격적으로 배웁니다. 데이터 100개가 있어도 코드 한 줄로 카드 100개를 만들 수 있습니다.

**[→ 05장: 리스트와 렌더링 (공개 예정)**

{% endraw %}
