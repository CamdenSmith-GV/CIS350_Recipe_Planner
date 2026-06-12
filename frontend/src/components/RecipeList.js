/**
 * @file ./frontend/src/components/RecipeList.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/12/2026
 * @brief Recipe selection list group.
 */
import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";

function RecipeList({ savedRecipes = [] }) {
  const [selectedId, setSelectedId] = useState(null);

  const selectRecipe = (e, id) => 
  {
    e.preventDefault();
    setSelectedId(id);
    console.log(id);
  };

  return (
    <div className="container-fluid mt-4 p-4 recipe-page">
      <h1 className="mb-3 recipe-title">Recipe Planner</h1>

      <div className="list-group">
        {savedRecipes.map((recipe) => (
          <a
            key={recipe.id}
            href="#"
            className={`list-group-item list-group-item-action ${selectedId === recipe.id ? "active" : ""}`}
            onClick={(e) => selectRecipe(e, recipe.id)}
          >
            <div className="d-flex w-100 justify-content-between">
              <h5 className="mb-1">{recipe.name}</h5>
              <small>{recipe.cookTime} min</small>
            </div>
            <p className="mb-1">Summary TBD</p>
          </a>
        ))}
      </div>
    </div>
  );
}

export default RecipeList;