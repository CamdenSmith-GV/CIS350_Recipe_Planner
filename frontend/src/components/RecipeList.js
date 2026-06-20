/**
 * @file ./frontend/src/components/RecipeList.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/12/2026
 * @brief Recipe selection list group.
 */
import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";
import { formatCookTime } from "../constants";

/**
 * @brief Shows a clickable list of saved recipes.
 *
 * Each recipe shows its name, cook time, and summary. Clicking one highlights
 * it and tells the app which recipe was picked.
 *
 * @param savedRecipes The list of recipes to show.
 * @param onSelectRecipe Called with the id of the recipe that was clicked.
 * @return The recipe list page.
 */
function RecipeList({ savedRecipes = [], onSelectRecipe }) {
  const [selectedId, setSelectedId] = useState(null);

  /**
   * @brief Marks a recipe as selected and tells the app about it.
   *
   * Saves the id so the button shows as active, then calls the parent handler.
   *
   * @param id The id of the recipe that was clicked.
   */
  const selectRecipe = (id) =>
  {
    setSelectedId(id);
    onSelectRecipe(id);
  };

  return (
    <div className="container-fluid mt-4 p-4">
      <h1 className="mb-3 recipe-title">Select Recipes:</h1>

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
              <small className="recipe-list-time">{formatCookTime(recipe.cook_time)}</small>
            </div>
            <p className="mb-1 recipe-list-summary">{recipe.summary}</p>
          </button>
        ))}
      </div>
    </div>
  );
}

export default RecipeList;