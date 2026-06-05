/**
 * @file ./frontend/src/App.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/5/2026
 * @brief Top-level app shell.
 */

import { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import RecipePlanner from "./components/RecipePlanner";

function App()
{
  const [showPlanner, setShowPlanner] = useState(false);

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

  return <div className="container-fluid py-4">{content}</div>;
}

export default App;
