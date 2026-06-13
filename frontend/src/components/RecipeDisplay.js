/**
 * @file ./frontend/src/components/RecipeDisplay.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/12/2026
 * @brief Displays the details of the selected recipe.
 */
import "bootstrap/dist/css/bootstrap.min.css";

function RecipeDisplay({ selectedRecipe }) {
    return (
        <div className="container-fluid mt-4 p-4 recipe-page">
            <h1 className="mb-3 recipe-title">Recipe Display!!!</h1>
            {selectedRecipe && <p>{selectedRecipe.name}</p>}
        </div>
    )
}

export default RecipeDisplay;