---
title: 9. onChange event handler
layout: default
grand_parent: Language
parent: React
nav_order: 9
has_children: false
permalink: /language/react/react_9
---
### 9. onChange event handler

#### input tags
src/App.jsx
```jsx
import MyComponent_09 from './09/MyComponent'

export default function App() {

  return (
    <>
      <MyComponent_09/>
    </>
  )
}
```

src/09/MyComponent.jsx
```jsx
import { useState } from "react"

export default function MyComponent_09(){

  const [name,setName] = useState("Guest");
  const [quantity,setQuantity] = useState(1);
  const [comment,setComment] = useState("");
  const [payment,setPayment] = useState("Visa");
  const [shipping,setShipping] = useState("Delivery");

  function handleNameChange(event){
    setName(event.target.value);
  }
  function handleQuantityChange(event){
    setQuantity(event.target.value);
  }
  function handleCommentChange(event){
    setComment(event.target.value);
  }
  function handlePaymentChange(event){
    setPayment(event.target.value);
  }
  function handleShippingChange(event){
    setShipping(event.target.value)
  }

  return(
    <div>
      <input value={name} onChange={handleNameChange} />
      <p>Name:{name}</p>

      <input value={quantity} onChange={handleQuantityChange} />
      <p>Quantity:{quantity}</p>

      <textarea value={comment} onChange={handleCommentChange} placeholder="Enter delivery instaructions" ></textarea>
      <p>Comment: {comment}</p>
      <select value={payment} onChange={handlePaymentChange}>
        <option value="">Select an option</option>
        <option value="Visa">Visa</option>
        <option value="Mastercard">Mastercard</option>
        <option value="Giftcard">Giftcard</option>
      </select>
      <p>Payment: {payment}</p>
      <label>
        <input type="radio" value="Pick up" checked={shipping === "Pick up"} onChange={handleShippingChange} />
        Pick up
      </label><br/>
      <label >
        <input type="radio" value="Delivery" checked={shipping === "Delivery"} onChange={handleShippingChange} />
        Delivery
      </label>
      <p>Shipping: {shipping}</p>
    </div>
  )
}
```

#### color picker

src/App.jsx
```jsx
import ColorPicker from './10/ColorPicker'

export default function App() {

  return (
    <>
      <ColorPicker/>
    </>
  )
}
```

src/10/ColorPicker.jsx
```jsx{%raw%}
import { useState } from "react"
import './ColorPicker.css'

export default function ColorPicker() {
  const [color, setColor] = useState("#ffffff");

  function handleColorChange(event){
    setColor(event.target.value);
  }
  return (
    <div className="color-picker-container">
      <div className="color-picker-title">Color Picker</div>
      <div className="color-display" style={{ backgroundColor: color }}>
        <p>Selected Color: {color}</p>
      </div>
      <label htmlFor="color" className="color-picker-label">Select a Color</label>
      <input type="color" value={color} onChange={handleColorChange} id="color" className="color-picker-input" />
    </div>
  )
}{%endraw%}
```

src/10/ColorPicker.css
```css
@reference "../index.css"; 

.color-picker-container{
  @apply flex flex-col items-center;
}
.color-picker-title {
  @apply m-[50px] text-5xl;
}
.color-display{
  @apply w-[300px] h-[300px] flex justify-center items-center border-[5px] border-gray-300 rounded-[25px] mb-[25px] transition-all duration-250 ease-in-out;
}

.color-picker-label{
  @apply text-2xl font-bold mb-[10px];
}

.color-picker-input{
  @apply w-[75px] h-[50px] p-[5px] rounded-[10px] border-[3px] border-gray-300;
}

```

### 11. updater functions

src/11/App.jsx
```jsx
import MyComponent_11 from './11/MyComponent'
export default function App() {

  return (
    <>
      <MyComponent_11/>
    </>
  )
}
```

src/11/MyComponent.jsx
```jsx
import { useState } from "react";

export default function MyComponent_11(){
  const [count,setCount] = useState(0);
  const increment = () =>{
    // 1씩 증가
    setCount(count + 1)
    setCount(count + 1)

    // 2씩 증가
    // setCount(count => count + 1);
    // setCount(count => count + 1);

    // setCount(c => c + 1);
    // setCount(c => c + 1);

  }
  const decrement = () => {
    setCount(count - 1);
    setCount(count - 1);
    // setCount(count => count - 1);
  }
  const reset = () => {
    setCount(0);
  }
  return(
    <div>
      <p>{count}</p>
      <button onClick={decrement}>Decrement</button>
      <button onClick={reset}>Reset</button>
      <button onClick={increment}>Increment</button>
    </div>
  );
}
```