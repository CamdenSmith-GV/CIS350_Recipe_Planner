/**
 * @file ./frontend/src/components/SelectedRecipes.js
 * @author Camden, William, Jasper
 * @course CIS350
 * @date 6/18/2026
 * @brief Small column listing the recipes added to the shopping list.
 */
import "bootstrap/dist/css/bootstrap.min.css";
import api from "../api";

/**
 * @brief Shows the recipes added to the shopping list.
 *
 * Lists each added recipe with a remove button, and a button to download the
 * grocery list. If nothing is added it shows an empty message instead.
 *
 * @param groceryList The recipes that have been added to the list.
 * @param onRemoveFromGroceryList Called with a recipe to remove it from the list.
 * @return The selected recipes column.
 */
function SelectedRecipes({ groceryList = [], onRemoveFromGroceryList }) {

  /**
   * @brief Downloads the grocery list as a text file.
   *
   * Sends the recipe ids to the backend, then turns the response into a file
   * and clicks a link to download it.
   */
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
