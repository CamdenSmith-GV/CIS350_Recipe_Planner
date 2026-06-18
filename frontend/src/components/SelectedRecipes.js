/**
 * @file ./frontend/src/components/SelectedRecipes.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/18/2026
 * @brief Small column listing the recipes added to the shopping list.
 */
import "bootstrap/dist/css/bootstrap.min.css";

function SelectedRecipes({ groceryList = [], onRemoveFromGroceryList }) {
  if (groceryList.length === 0)
  {
    return (
      <div className="container-fluid mt-4 p-4 recipe-page">
        <h5 className="mb-3 recipe-title">Selected</h5>
        <p className="recipe-empty">No recipes added.</p>
      </div>
    );
  }

  return (
    <div className="container-fluid mt-4 p-4 recipe-page">
      <h5 className="mb-3 recipe-title">Selected</h5>

      <div className="list-group">
        {groceryList.map((recipe) => (
          <div
            key={recipe.id}
            className="recipe-list-item list-group-item d-flex justify-content-between align-items-center"
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
    </div>
  );
}

export default SelectedRecipes;
