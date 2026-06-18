/**
 * @file ./frontend/src/components/SelectedRecipes.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/18/2026
 * @brief Small column listing the recipes added to the shopping list.
 */
import "bootstrap/dist/css/bootstrap.min.css";
import api from "../api";

function SelectedRecipes({ groceryList = [], onRemoveFromGroceryList }) {

  const handleDownload = async () => 
  {
    const ids = groceryList.map((recipe) => recipe.id);
    const response = await api.post("/groceryList", { recipe_ids: ids });

    const link = document.createElement("a");
    link.href = URL.createObjectURL(new Blob([response.data]));
    link.download = "grocery-list.txt";
    link.click();
  };

  if (groceryList.length === 0)
  {
    return (
      <div className="container-fluid mt-4 p-4 selected-panel">
        <h5 className="mb-3 recipe-title">Selected</h5>
        <p className="recipe-empty">No recipes added.</p>
      </div>
    );
  }

  return (
    <div className="container-fluid mt-4 p-4 selected-panel">
      <h5 className="mb-3 recipe-title">Selected</h5>

      <div className="list-group">
        {groceryList.map((recipe) => (
          <div
            key={recipe.id}
            className="selected-item d-flex justify-content-between align-items-center"
          >
            <span>{recipe.name}</span>
            <button
              type="button"
              className="btn-close"
              aria-label="Remove"
              onClick={() => onRemoveFromGroceryList(recipe)}
            />
          </div>
        ))}
      </div>

      <button
        type="button"
        className="btn custom-green-btn w-100 mt-3"
        onClick={handleDownload}
      >
        Download Grocery List
      </button>
    </div>
  );
}

export default SelectedRecipes;
