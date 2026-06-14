/**
 * @file ./frontend/src/components/RecipeDisplay.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/12/2026
 * @brief Displays the details of the selected recipe.
 */
import "bootstrap/dist/css/bootstrap.min.css";

function RecipeDisplay({ selectedRecipe }) {
    if (!selectedRecipe) 
    {
        return (
            <div className="container-fluid mt-4 p-4 recipe-page">
                <h1 className="mb-3 recipe-title">Recipe Display</h1>
                <p className="recipe-empty">Select a recipe to see its details.</p>
            </div>
        );
    }

    const formatIngredient = (ingredient) => 
    {
        if (ingredient.measurement_type === "quantity")
        {
            return `${ingredient.amount} ${ingredient.name}`;
        }
        return `${ingredient.amount} ${ingredient.unit} ${ingredient.name}`;
    };

    return (
        <div className="container-fluid mt-4 p-4 recipe-page">
            <div className="card recipe-card p-4 shadow-sm">
                <div className="d-flex w-100 justify-content-between">
                    <h1 className="recipe-title">{selectedRecipe.name}</h1>
                    <h5 className="recipe-list-time">{selectedRecipe.cook_time} min</h5>
                </div>

                <p className="recipe-list-summary">{selectedRecipe.summary}</p>

                <h4 className="recipe-heading mt-3">Ingredients</h4>
                {selectedRecipe.ingredients.map((ingredient, index) => (
                    <p key={index} className="recipe-ingredient-item">{formatIngredient(ingredient)}</p>
                ))}

                <h4 className="recipe-heading mt-3">Instructions</h4>
                <p className="recipe-instructions">{selectedRecipe.instructions}</p>
            </div>
        </div>
    );
}

export default RecipeDisplay;
