/**
 * @file ./frontend/src/App.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/5/2026
 * @brief Top-level app shell.
 */

import { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import RecipePlanner from "./components/RecipePlanner";
import { THEME_STYLES } from "./constants";
import api from './api';
import RecipeList from "./components/RecipeList";
import RecipeDisplay from "./components/RecipeDisplay";

function App()
{
  const fetchRecipes = async () => 
  {
    const response = await api.get("/getRecipes");
    setSavedRecipes(response.data);
  };

  const [showPlanner, setShowPlanner] = useState(false);
  const [savedRecipes, setSavedRecipes] = useState([]);
  const [selectedRecipe, setSelectedRecipe] = useState(null);

  const handleSelectRecipe = (id) =>
  {
    const recipe = savedRecipes.find((r) => r.id === id);
    setSelectedRecipe(recipe);
  };

  useEffect(() => 
  {
    fetchRecipes();
  }, []);

  console.log("Here!!!!");

  let content;
  if (showPlanner)
  {
    content = <RecipePlanner savedRecipes={savedRecipes} />;
  }
  else
  {
    content =
    (
      <>
       
        <div className="row mt-4">
          <div className="col-md-4">
            <RecipeList savedRecipes={savedRecipes} onSelectRecipe={handleSelectRecipe} />

          </div>
          <div className="col-md-8">
            <RecipeDisplay selectedRecipe={selectedRecipe} />
          </div>
        </div>

         <button className="btn custom-orange-btn" onClick={() => setShowPlanner(true)}>
          Open Recipe Planner
        </button>
      </>
    );
  }

  return (
    <div className="container-fluid py-4">
      <style>{THEME_STYLES}</style>
      {content}
    </div>
  );
}

export default App;
