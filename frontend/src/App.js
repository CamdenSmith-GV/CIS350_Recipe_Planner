/**
 * @file ./frontend/src/App.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/4/2026
 * @brief React client for displaying and creating ingredients.
 */

import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState, useEffect } from "react";
import Axios from "axios";

function App() {
  const [ingredientName, setIngredientName] = useState("");
  const [quantity, setQuantity] = useState("");
  const [ingredients, setIngredients] = useState([]);

  const addIngredient = () => 
    {
      const newIngredient = 
      {
        name: ingredientName,
        quantity: quantity,
      };

      setIngredients([...ingredients, newIngredient,]);

      setIngredientName("");
      setQuantity("");
   };
  

 return (
    <div className="container mt-4">
      <div className="card p-4 mb-4 shadow-sm">
        <h1 className="mb-3">Recipe Planner</h1>

        <input
          className="form-control mb-2"
          type="text"
          placeholder="Ingredient name..."
          value={ingredientName}
          onChange={(event) => 
            {
              setIngredientName(event.target.value);
            }}
        />

        <input
          className="form-control mb-3"
          type="text"
          placeholder="Quantity..."
          value={quantity}
          onChange={(event) => 
            {
              setQuantity(event.target.value);
            }}
        />

        <button className="btn btn-primary" onClick={addIngredient}>
          Add Ingredient
        </button>
      </div>

      <div className="card p-4 shadow-sm">
        <h2>Current Ingredients</h2>

        {ingredients.map((ingredient, index) => 
          {
            return (
              <p key={index}>
                {ingredient.quantity} {ingredient.name}
              </p>
            );
          })}
      </div>
    </div>
  );

}

export default App;
