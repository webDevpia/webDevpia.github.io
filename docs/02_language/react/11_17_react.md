---
title: React 17
layout: default
grand_parent: Language
parent: React
nav_order: 17
has_children: false
permalink: /language/react/react_17
---
### 22. Zustand

[npm trend](https://npmtrends.com/jotai-vs-recoil-vs-zustand)
- 독일어로 '상태'라는 뜻, 상태 관리 라이브러리 중 하나  
- 한개의 중앙에 집중된 형식의 스토어 구조를 활용하면서 상태를 정의하고 사용하는 방법이 단순하다.
- Context API를 사용할 때와 달리 상태 변경 시 불필요한 리랜더링을 일으키지 않도록 제어하기 쉽다.
- 동작을 이해하기 위해 알아야 하는 코드 양이 아주 적다. 


#### 1. zustand 설치

```bash
npm i zustand
```

#### 2. store 생성
- 스토어를 생성하기 위해 create 함수를 사용
- 스토어는 상태 변수와 해당 상태를 업데이트하는 액션(함수)으로 구성할 수 있다.
  - 버튼을 선택하는 함수
  - count 를 증가시키는 함수
  - count를 리셋하는 함수 등과 같은...

src/stores/storeButton.jsx
```jsx
import {create} from "zustand";

const useButtonStore = create((set) => ({
  count: 0,
  selectedButton: null,

  setSelectedButton: (button) => set({ selectedButton: button }),
  incrementCount: () => set((state) => ({ count: state.count + 1 })),
  removeCount: () => set({ count: 0 }),
}));

export default useButtonStore;
```

#### 3. 상태 변수 및 액션 사용
- 상태 변수와 액션을 사용하려면 컴포넌트 내에서 useStore함수를 호출

src/components/FirstChild.jsx
```jsx
import React from "react";
import useButtonStore from "../stores/storeButton";

export default function FirstChild() {

  const { setSelectedButton, incrementCount, removeCount } = useButtonStore((state) => state);

  const handleClick = (button) => {
    setSelectedButton(button);
  };

  return (
    <div>
      <h1>FirstChild</h1>
      <div>
        <button onClick={() => handleClick("O")}>O</button>
        <button onClick={() => handleClick("X")}>X</button>
      </div>
      <div>
        <button onClick={incrementCount}>카운트 증가</button>
        <button onClick={removeCount}>카운트 리셋</button>
      </div>
    </div>
  );
}
```

src/components/SecondChild.jsx
```jsx
import React from "react";
import useButtonStore from "../stores/storeButton";

export default function SecondChild() {

  const { count, selectedButton } = useButtonStore((state) => state);

  return (
    <div>
      <h1>SecondChild</h1>
      <p>카운트: {count}</p>
      <p>선택한 버튼: {selectedButton}</p>
    </div>
  );
}
```

src/Test.jsx
```jsx
import FirstChild from "./components/FirstChild";
import SecondChild from "./components/SecondChild";

export default function Test() {
  return (
    <div>
      <FirstChild />
      <SecondChild />
    </div>
  );
}
```

src/App.jsx
```jsx
import Test from "./Test";

export default function App() {
  return (
    <div>
      <Test />
    </div>
  );
}
```

src/index.css
```css
:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;

  color-scheme: light dark;
  color: rgba(255, 255, 255, 0.87);
  background-color: #242424;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#root {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

a {
  font-weight: 500;
  color: #646cff;
  text-decoration: inherit;
}
a:hover {
  color: #535bf2;
}

body {
  margin: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
}

h1 {
  font-size: 3.2em;
  line-height: 1.1;
}

button {
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 0.5em 1.2em;
  margin-left: 1em;
  font-size: 0.7em;
  font-weight: 500;
  font-family: inherit;
  background-color: #1a1a1a;
  cursor: pointer;
  transition: border-color 0.25s;
}
button:hover {
  border-color: #e420f2;
}
button:focus,
button:focus-visible {
  outline: 4px auto -webkit-focus-ring-color;
}

@media (prefers-color-scheme: light) {
  :root {
    color: #213547;
    background-color: #ffffff;
  }
  a:hover {
    color: #747bff;
  }
  button {
    background-color: #f9f9f9;
  }
}

p{
  background-color: #f9f9f9;
  height: 2.5em;
  line-height : 2.5em;
}
```
#### 4. prop사용과 비교

##### prop 사용
src/components/Form.jsx
```jsx
const Form = (props) => {
  return (
    <>
      <form onSubmit={props.onSubmit}>
        <input type='text' onChange={props.onAdd} value={props.memo} />
        <button type='submit'>작성완료</button>
      </form>
    </>
  );
};

export default Form
```

src/components/Memos.jsx
```jsx
const Memos = (props) => {
  return (
    <div>
      {props.memos.map((memo,index) => {
        return <p key={index}>{memo}</p>;
      })}
    </div>
  );
};
export default Memos
```

src/Test1.jsx
```jsx
import { useState } from 'react'
import Form from './components/Form';
import Memos from './components/Memos';

export default function Test1() {
  const [memo, setMemo] = useState('');
  const [memos, setMemos] = useState([]);

  const handleWriteMemo = (e) => {
    setMemo(e.target.value);
  };

  const handleAddMemo = (e) => {
    e.preventDefault();
    setMemos((prevMemos) => [...prevMemos, memo]);
    setMemo('');
  };

  return (
    <div>
      <h1>메모 작성하기</h1>
      <Form onAdd={handleWriteMemo} onSubmit={handleAddMemo} memo={memo} />
      <Memos memos={memos} />
    </div>
  );
}
```

src/App.jsx
```jsx
import Test1 from "./Test1";

export default function App() {
  return (
    <div>
      <Test1 />
    </div>
  );
}
```

##### zustand 사용

src/stores/storeMemos.jsx
```jsx
import {create} from 'zustand';

const useMemosStore = create((set) => ({
  memo: '',
  setMemo: (text) => set({ memo: text }),
  memos: [],
  setMemos: (newMemo) =>
    set((prev) => ({
      memos: [...prev.memos, newMemo],
    })),
}));

export default useMemosStore;
```

src/components/Form1.jsx
```jsx
import useMemosStore from '../stores/storeMemos';

const Form1 = () => {
  const { memo, setMemo, setMemos } = useMemosStore();

  const handleWriteMemo = (e) => {
    setMemo(e.target.value);
  };

  const handleAddMemo = (e) => {
    e.preventDefault();
    setMemos(memo);
    setMemo('');
  };

  return (
    <>
      <form onSubmit={handleAddMemo}>
        <input type='text' onChange={handleWriteMemo} value={memo} />
        <button type='submit'>작성완료</button>
      </form>
    </>
  );
};
export default Form1
```

src/components/Memos1.jsx
```jsx
import useMemosStore from '../stores/storeMemos';

const Memos1 = () => {
  const { memos } = useMemosStore();

  return (
    <div>
      {memos.map((memo,index) => {
        return <p key={index}>{memo}</p>;
      })}
    </div>
  );
};
export default Memos1
```

src/Test2.jsx
```jsx
import Form1 from './components/Form1';
import Memos1 from './components/Memos1';

export default function Test2() {
  return (
    <div>
      <h1>메모 작성하기</h1>
      <Form1 />
      <Memos1 />
    </div>
  );
}
```

src/App.jsx
```jsx
import Test2 from "./Test2";

export default function App() {
  return (
    <div>
      <Test2 />
    </div>
  );
}
```