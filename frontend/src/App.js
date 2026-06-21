/**
 * @file ./frontend/src/App.js
 * @author Camden, William, Jasper
 * @course CIS350
 * @date 6/5/2026
 * @brief Top-level app shell.
 */

import { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import RecipePlanner from "./components/RecipePlanner";
import { THEME, THEME_STYLES } from "./constants";
import api from './api';
import RecipeList from "./components/RecipeList";
import RecipeDisplay from "./components/RecipeDisplay";
import SelectedRecipes from "./components/SelectedRecipes";

/**
 * @brief The top-level app component.
 *
 * Loads the saved recipes and either shows the recipe planner or the main
 * view (recipe list, the selected recipe, and the grocery list). Keeps all
 * the shared state and passes it down to the components.
 *
 * @return The whole app.
 */
function App()
{
  /**
   * @brief Gets the saved recipes from the backend and stores them.
   */
  const fetchRecipes = async () =>
  {
    const response = await api.get("/getRecipes");
    setSavedRecipes(response.data);
  };

  const [showPlanner, setShowPlanner] = useState(false);
  const [savedRecipes, setSavedRecipes] = useState([]);
  const [groceryList, setGroceryList] = useState([]);
  const [selectedRecipe, setSelectedRecipe] = useState(null);

  /**
   * @brief Finds the clicked recipe and sets it as the selected one.
   * @param id The id of the recipe that was clicked.
   */
  const handleSelectRecipe = (id) =>
  {
    const recipe = savedRecipes.find((r) => r.id === id);
    setSelectedRecipe(recipe);
  };

  /**
   * @brief Adds a recipe to the grocery list if it isn't already there.
   * @param recipe The recipe to add.
   */
  const handleAddToGroceryList = (recipe) =>
  {
    setGroceryList((prev) =>
    {
      if (prev.some((r) => r.id === recipe.id))
      {
        return prev;
      }
      return [...prev, recipe];
    });
  };

  /**
   * @brief Removes a recipe from the grocery list.
   * @param recipe The recipe to remove.
   */
  const handleRemoveFromGroceryList = (recipe) =>
  {
    setGroceryList((prev) =>
    {
      return prev.filter((r) => r.id !== recipe.id);
    });
  };

  useEffect(() =>
  {
    fetchRecipes();
  }, []);

  /**
   * @brief Closes the recipe planner and reloads the recipes.
   *
   * Refetches so any recipe just added shows up in the list.
   */
  const handleExitPlanner = () =>
  {
    setShowPlanner(false);
    fetchRecipes();
  };

  let content;
  if (showPlanner)
  {
    content =
    (
      <>
        <button className="btn custom-red-btn mb-3" onClick={handleExitPlanner}>
          Exit Recipe Planner
        </button>
        <RecipePlanner savedRecipes={savedRecipes} />
      </>
    );
  }
  else
  {
    content =
    (
      <>
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h1 className="recipe-title mb-0">Grocery Studio</h1>
          <button className="btn custom-orange-btn" onClick={() => setShowPlanner(true)}>
            Open Recipe Planner
          </button>
        </div>

        <div className="row mt-4">
          <div className="col-md-3">
            <RecipeList savedRecipes={savedRecipes} onSelectRecipe={handleSelectRecipe} />

          </div>
          <div className="col-md-7">
            <RecipeDisplay selectedRecipe={selectedRecipe} onAddToGroceryList={handleAddToGroceryList} />
          </div>
          <div className="col-md-2">
            <SelectedRecipes groceryList={groceryList} onRemoveFromGroceryList={handleRemoveFromGroceryList} />
          </div>
        </div>
      </>
    );
  }

  return (
    <div className="container-fluid py-4" style={{ backgroundColor: THEME.cream, minHeight: "100vh" }}>
      <style>{THEME_STYLES}</style>
      {content}
    </div>
  );
}

export default App;
