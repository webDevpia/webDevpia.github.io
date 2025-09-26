---
title: React 10
layout: default
grand_parent: Language
parent: React
nav_order: 10
has_children: false
permalink: /language/react/react_10
---
### 12. update OBJECTS in state
src/App.jsx
```jsx
import MyComponent_12 from "./12/MyComponent"
export default function App() {

  return (
    <>
      <MyComponent_12/>
    </>
  )
}
```

src/MyComponent.jsx
```jsx
import { useState } from "react";

export default function MyComponent_12(){

  const [car, setCar] = useState({
    year:2024,
    make: "Ford",
    model: "Mustang"
  });

  function handleYearChange(event){
    setCar(car => ({...car, year:event.target.value}));
  }

  function handleMakeChange(event){
    setCar(c => ({...c, make:event.target.value}));
  }

  function handleModelChange(event){
    setCar(c => ({...c, model:event.target.value}));
  }

  return(
    <div>
      <p>
        Your favorite car is : {car.year} {car.make} {car.model}
      </p>
      <input type="number" value={car.year} onChange={handleYearChange} /><br/>
      <input type="text" value={car.make} onChange={handleMakeChange} /><br/>
      <input type="text" value={car.model}  onChange={handleModelChange}/><br/>
    </div>
  );
}
```

### 13. update ARRAYS in state

src/App.jsx
```jsx
import MyComponent_13 from "./13/MyComponent"
export default function App() {
  return (
    <>
      <MyComponent_13 />
    </>
  )
}
```

src/13/MyComponent.jsx
```jsx

import { useState } from "react";

export default function MyComponent_13(){

  const [foods,setFoods] = useState(["Apple","Orange","Banana"]);

  function handleAddFood(){

    const newFood = document.getElementById("foodInput").value;
    document.getElementById("foodInput").value = "";
    setFoods(f => [...f, newFood]);
    console.log(foods)

  }

  function handleRemoveFood(index){

    setFoods(foods.filter((_,i) => i !== index))

  }

  return(
    <div>
      <h2>List of Food</h2>
      <ul>
        {foods.map((food,index) => 
          <li key={index} onClick={()=>handleRemoveFood(index)}>
            {food}
          </li>
        )}
      </ul>
      <input type="text" id="foodInput" placeholder="Enter food name" />
      <button onClick={handleAddFood}>Add Food</button>
    </div>
  );
}
```

### 14. update ARRAY of OBJECTS in state
```jsx
import { useState } from "react";

export default function MyComponent_14(){

  const [cars,setCars] = useState([]);
  const [carYear,setCarYear] = useState(new Date().getFullYear());
  const [carMake,setCarMake] = useState("");
  const [carModel,setCarModel] = useState("");

  function handleAddCar(){

    const newCar = {
      year:carYear,
      make:carMake,
      model:carModel,
    };

    setCars(c => [...c, newCar]);
    setCarYear(new Date().getFullYear());
    setCarMake("");
    setCarModel("");

  }

  function handleRemoveCar(index){
    setCars(c => c.filter((_,i) => i !== index));
  }

  function handleYearChange(event){
    setCarYear(event.target.value);
  }

  function handleMakeChange(event){
    setCarMake(event.target.value);
  }

  function handleModelChange(event){
    setCarModel(event.target.value);
  }

  return(
    <div>
      <h2>List of Car Objects</h2>
      <ul>
        {cars.map((car,index) => 
          <li key={index} onClick={()=>handleRemoveCar(index)}> 
          {car.year} {car.make} {car.model} 
          </li>
        )}
      </ul>
      <input type="number" value={carYear} onChange={handleYearChange} /><br/>
      <input type="text" value={carMake} onChange={handleMakeChange} placeholder="Enter car make" /><br/>
      <input type="text" value={carModel} onChange={handleModelChange} placeholder="Enter car model" /><br/>
      <button onClick={handleAddCar}>Add Car</button>
    </div>
  );
}
```