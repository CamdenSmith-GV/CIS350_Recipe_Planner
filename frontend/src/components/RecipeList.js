/**
 * @file ./frontend/src/components/RecipeList.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/12/2026
 * @brief Recipe selection list group.
 */
import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";

function RecipeList({ savedRecipes = [], onSelectRecipe }) {
  const [selectedId, setSelectedId] = useState(null);

  const selectRecipe = (id) =>
  {
    setSelectedId(id);
    onSelectRecipe(id);
  };

  return (
    <div className="container-fluid mt-4 p-4">
      <h1 className="mb-3 recipe-title">Recipe Planner</h1>

      <div className="list-group">
        {savedRecipes.map((recipe) => (
          <button
            key={recipe.id}
            type="button"
            className={`recipe-list-item list-group-item list-group-item-action ${selectedId === recipe.id ? "active" : ""}`}
            onClick={() => selectRecipe(recipe.id)}
          >
            <div className="d-flex w-100 justify-content-between">
              <h5 className="mb-1">{recipe.name}</h5>
              <small className="recipe-list-time">{recipe.cookTime} min</small>
            </div>
            <p className="mb-1 recipe-list-summary">{recipe.summary}</p>
          </button>
        ))}
      </div>
    </div>
  );
}

export default RecipeList;