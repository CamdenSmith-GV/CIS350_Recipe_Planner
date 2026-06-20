/**
 * @file ./frontend/src/components/RecipeDisplay.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/12/2026
 * @brief Displays the details of the selected recipe.
 */
import "bootstrap/dist/css/bootstrap.min.css";
import { formatCookTime } from "../constants";

/**
 * @brief Shows the details of the selected recipe.
 *
 * Shows the name, cook time, summary, ingredients, and instructions. If no
 * recipe is picked it shows a message instead.
 *
 * @param selectedRecipe The recipe to show (or null if none is picked).
 * @param onAddToGroceryList Called to add the recipe to the shopping list.
 * @return The recipe display page.
 */
function RecipeDisplay({ selectedRecipe, onAddToGroceryList }) {
    if (!selectedRecipe) 
    {
        return (
            <div className="container-fluid mt-4 p-4">
                <h1 className="mb-3 recipe-title">Recipe Display</h1>
                <p className="recipe-empty">Select a recipe to see its details.</p>
            </div>
        );
    }

    /**
     * @brief Turns an ingredient into a readable string.
     *
     * Quantity ingredients skip the unit, everything else includes it.
     *
     * @param ingredient The ingredient to format.
     * @return A string like "2 cups flour".
     */
    const formatIngredient = (ingredient) =>
    {
        if (ingredient.measurement_type === "quantity")
        {
            return `${ingredient.amount} ${ingredient.name}`;
        }
        return `${ingredient.amount} ${ingredient.unit} ${ingredient.name}`;
    };

    /**
     * @brief Adds the selected recipe to the shopping list.
     *
     * Passes the current recipe up to the parent's handler.
     */
    const addToList = () =>
    {
        onAddToGroceryList(selectedRecipe);
    };

    return (
        <div className="container-fluid mt-4 p-4 recipe-page">
            <div className="card recipe-card p-4 shadow-sm">
                <div className="d-flex w-100 justify-content-between">
                    <h1 className="recipe-title">{selectedRecipe.name}</h1>
                    <h5 className="recipe-list-time">{formatCookTime(selectedRecipe.cook_time)}</h5>
                </div>

                <p className="recipe-list-summary">{selectedRecipe.summary}</p>

                <h4 className="recipe-heading mt-3">Ingredients</h4>
                {selectedRecipe.ingredients.map((ingredient, index) => (
                    <p key={index} className="recipe-ingredient-item">{formatIngredient(ingredient)}</p>
                ))}

                <h4 className="recipe-heading mt-3">Instructions</h4>
                <p className="recipe-instructions">{selectedRecipe.instructions}</p>
            </div>

            <button 
                className="btn custom-green-btn mt-2"
                onClick={addToList}
            >
                Add To Shopping List
            </button>
        </div>
    );
}

export default RecipeDisplay;
