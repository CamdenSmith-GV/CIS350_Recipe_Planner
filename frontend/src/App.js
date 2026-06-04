/**
 * @file ./frontend/src/App.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/4/2026
 * @brief React client for displaying and creating ingredients.
 */

import "./App.css";
import { useState, useEffect } from "react";
import Axios from "axios";

function App() {
  const [listOfIngredients, setListOfIngredients] = useState([]);
  const [name, setName] = useState("");
  const [quantity, setQuantity] = useState(0);

  useEffect(() => {
    Axios.get("http://localhost:3001/getIngredients").then((response) => {
      setListOfIngredients(response.data);
    });
  }, []);

  const createIngredient = () => {
    Axios.post("http://localhost:3001/createIngredient", {
      name,
      quantity,
    }).then((response) => {
      setListOfIngredients([
        ...listOfIngredients,
        {
          name,
          quantity,
        },
      ]);
    });
  };

  return (
    <div className="App">
      <div className="ingredientDisplay">
        {listOfIngredients.map((i) => {
          return (
            <div>
              <h1>
                {i.quantity} {i.name}
              </h1>
            </div>
          );
        })}
      </div>
      <div>
        <input
          type="text"
          placeholder="Name..."
          onChange={(event) => {
            setName(event.target.value);
          }}
        />
        <input
          type="number"
          step="0.1"
          placeholder="Quantity..."
          onChange={(event) => {
            setQuantity(parseFloat(event.target.value));
          }}
        />
        <button onClick={createIngredient}> Add Ingredient </button>
      </div>
    </div>
  );
}

export default App;
