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

function App()
{
  const [showPlanner, setShowPlanner] = useState(false);
  const [savedRecipes, setSavedRecipes] = useState([]);

  useEffect(() => {
    fetch("http://localhost:3001/getRecipes")
      .then((response) => response.json())
      .then((data) => setSavedRecipes(data))
      .catch((error) => console.error("Failed to load recipes:", error));
  }, []);

  console.log("Here!!!!");
  console.log(savedRecipes);

  let content;
  if (showPlanner)
  {
    content = <RecipePlanner />;
  }
  else
  {
    content = 
    (
      <button className="btn custom-orange-btn" onClick={() => setShowPlanner(true)}>
        Open Recipe Planner
      </button>
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
