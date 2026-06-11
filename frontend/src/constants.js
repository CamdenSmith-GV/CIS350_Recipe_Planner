/**
 * @file ./frontend/src/constants.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/5/2026
 * @brief Shared constants and helpers for ingredient entry.
 */

export const VOLUME_UNITS = ["tsp", "tbsp", "fl oz", "cup", "pint", "quart", "gallon", "mL", "L"];
export const MASS_UNITS = ["oz", "lbs", "g", "kg"];

// Colors used for the recipe planner theme
export const THEME = 
{
  white: "#FFFFFF",
  cream: "#F5EEE6",
  green: "#2F8F5B",
  orange: "#FF7218",
  brown: "#2D1708",
  taupe: "#80766B",
};

export const THEME_STYLES = `
.recipe-page
{
  background-color: ${THEME.cream};
  color: ${THEME.brown};
  min-height: 100vh;
}

.recipe-title
{
  color: ${THEME.brown};
  font-weight: bold;
}

.recipe-heading
{
  color: ${THEME.brown};
  font-weight: bold;
}

.recipe-card
{
  background-color: ${THEME.white};
  border: 1px solid ${THEME.taupe};
  border-radius: 16px;
}

.recipe-card h2
{
  color: ${THEME.brown};
  font-weight: bold;
}

.recipe-ingredient-item
{
  color: ${THEME.brown};
  border-bottom: 1px solid ${THEME.taupe};
  padding-bottom: 0.4rem;
  margin-bottom: 0.4rem;
}

.recipe-input
{
  background-color: ${THEME.white};
  border: 1px solid ${THEME.taupe};
  color: ${THEME.brown};
  border-radius: 10px;
}

.recipe-input::placeholder
{
  color: ${THEME.taupe};
}

.recipe-input:focus
{
  background-color: ${THEME.white};
  border-color: ${THEME.green};
  color: ${THEME.brown};
  box-shadow: 0 0 5px ${THEME.green};
}

.btn.custom-orange-btn
{
  background-color: ${THEME.orange};
  border-color: ${THEME.orange};
  border-radius: 30px;
  color: ${THEME.white};
  font-weight: bold;
}

.btn.custom-orange-btn:hover
{
  background-color: ${THEME.brown};
  border-color: ${THEME.brown};
  color: ${THEME.white};
}

.btn.custom-green-btn
{
  background-color: ${THEME.green};
  border-color: ${THEME.green};
  border-radius: 30px;
  color: ${THEME.white};
  font-weight: bold;
}

.btn.custom-green-btn:hover
{
  background-color: ${THEME.brown};
  border-color: ${THEME.brown};
  color: ${THEME.white};
}
`;

export const createEmptyIngredient = () =>
({
  name: "",
  measurementType: "", 
  unit: "",
  amount: "", 
});

export const createRecipe = (recipeName, ingredientList, instructions, hours, minutes) =>
({
  name: recipeName,
  ingredients: ingredientList,
  instructions: instructions,
  cookTimeMinutes: Number(hours) * 60 + Number(minutes),
});