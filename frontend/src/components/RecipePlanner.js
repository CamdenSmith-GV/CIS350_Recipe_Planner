/**
 * @file ./frontend/src/components/RecipePlanner.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/5/2026
 * @brief Recipe planner: enter ingredients one at a time and list them.
 */

import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";
import api from '../api';

import 
{
  VOLUME_UNITS,
  MASS_UNITS,
  createEmptyIngredient,
} from "../constants";

function RecipePlanner()
{
  const [savedRecipes, setSavedRecipes] = useState([]);
  const [ingredientList, setIngredientList] = useState([]);
  const [recipName, setName] = useState("");
  const [recipSummary, setSummary] = useState("");
  const [instructions, setInstructions] = useState("");
  const [hours, setHours] = useState("0");
  const [minutes, setMinutes] = useState("0");
  const [currentIngredient, setCurrentIngredient] = useState(createEmptyIngredient());

  const hourOptions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
  const minuteOptions = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55];

  const updateRow = (changes) =>
  {
    setCurrentIngredient((current) => ({ ...current, ...changes }));
  };

  const handleMeasurementTypeChange = (measurementType) =>
  {
    updateRow({ measurementType, unit: "", amount: "" });
  };

  const addIngredient = () =>
  {
    if (currentIngredient.name.trim() === "")
    {
      return;
    }
    if (currentIngredient.measurementType === "")
    {
      return;
    }
    if (currentIngredient.amount === "")
    {
      return;
    }
    if (currentIngredient.measurementType !== "quantity" && currentIngredient.unit === "")
    {
      return;
    }
    setIngredientList([...ingredientList, currentIngredient]);
    setCurrentIngredient(createEmptyIngredient());
  };

  let unitOptions = [];

  if (currentIngredient.measurementType === "volume")
  {
    unitOptions = VOLUME_UNITS;
  }
  else if (currentIngredient.measurementType === "mass")
  {
    unitOptions = MASS_UNITS;
  }

  const formatIngredient = (ingredient) => 
  {
    if (ingredient.measurementType === "quantity")
    {
      return `${ingredient.amount} ${ingredient.name}`;
    }
    return `${ingredient.amount} ${ingredient.unit} ${ingredient.name}`;
  };

  const addRecipe = () =>
  {
    if (ingredientList.length === 0) {
      return;
    }

  
  const recipe = 
    {
      name: recipName,
      summary: recipSummary,
      instructions: instructions,
      cook_time: Number(hours) * 60 + Number(minutes),
      ingredients: ingredientList.map((ingrediant) => ({
        name: ingrediant.name,
        measurement_type: ingrediant.measurementType,
        amount: Number(ingrediant.amount),
        unit: ingrediant.unit || "none"
      }))
    };

    const sendRecipe = async (recipe) =>
    {
      await api.post('/createRecipe', recipe);
    }

    sendRecipe(recipe);

    // recipe will be sent to the backend later
    setSavedRecipes([...savedRecipes, recipe]);

    // Reset the form for the next recipe.
    setName("");
    setSummary("")
    setIngredientList([]);
    setInstructions("");
    setHours("0");
    setMinutes("0");
    setCurrentIngredient(createEmptyIngredient());
  };

  return (
    <div className="container-fluid mt-4 p-4 recipe-page position-relative">
      <h1 className="mb-3 recipe-title">Recipe Planner</h1>

    <div className="position-absolute top-0 end-0 mt-4" style={{ width: "37%", marginRight: "8rem" }}>
        <div className="card recipe-card p-4 shadow-sm">
          <h2>Current Ingredients</h2>

          {ingredientList.map((ingredient, index) => (
            <p key={index} className="recipe-ingredient-item">{formatIngredient(ingredient)}</p>
          ))}
        </div>
      </div>

      <div className="row g-4">
        <div className="col-auto">
          <h4 className="mb-3 recipe-heading">Recipe Name:</h4>
        </div>
        <div className="col-md-2">
          <input
            className="form-control recipe-input"
            type="text"
            placeholder="Name..."
            value={recipName}
            onChange={(event) => setName(event.target.value)}
          />
        </div>
      </div>

      <div className="row g-4">
        <div className="col-auto">
          <h4 className="mb-3 recipe-heading">Summary:</h4>
        </div>
        <div className="col-md-5">
          <input
            className="form-control recipe-input"
            type="text"
            placeholder="Summary..."
            value={recipSummary}
            onChange={(event) => setSummary(event.target.value)}
            />
        </div>
      </div>
      <div className="row g-4 align-items-start">
        <div className="col-md-6">
          {/* Ingrediant enter col*/}
          <div className="row g-2 align-items-center mb-2">
            {/* Ingredient name */}
            <div className="col">
              <input
                className="form-control recipe-input"
                type="text"
                placeholder="Ingredient..."
                value={currentIngredient.name}
                onChange={(event) => updateRow({ name: event.target.value })}
              />
            </div>

            {/* Measurement type dropdown */}
            <div className="col-auto">
              <select
                className="form-select recipe-input"
                value={currentIngredient.measurementType}
                onChange={(event) =>
                  handleMeasurementTypeChange(event.target.value)
                }
              >
                <option value="">Measurement type...</option>
                <option value="quantity">Quantity</option>
                <option value="volume">Volume</option>
                <option value="mass">Mass</option>
              </select>
            </div>

            {/* Unit dropdown */}
            {unitOptions.length > 0 && (
              <div className="col-auto">
                <select
                  className="form-select recipe-input"
                  value={currentIngredient.unit}
                  onChange={(event) => updateRow({ unit: event.target.value })}
                >
                  <option value="">Unit...</option>

                  {unitOptions.map((unit) => (
                    <option value={unit} key={unit}>
                      {unit}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Amount box */}
            {currentIngredient.measurementType !== "" && (
              <div className="col-auto">
                <input
                  className="form-control recipe-input"
                  type="number"
                  placeholder="Amount..."
                  value={currentIngredient.amount}
                  onChange={(event) => updateRow({ amount: event.target.value })}
                />
              </div>
            )}
          </div>

          <button
            className="btn custom-green-btn mt-2"
            onClick={addIngredient}
          >
            Add Ingredient
          </button>
        </div>
      </div>

      <div className="row g-4 mt-1">
        {/* Enter Instructions */}
        <div className="col-md-6">
          <h4 className="recipe-heading">Instructions:</h4>
          <textarea
            className="form-control recipe-input"
            placeholder="Instructions..."
            rows="5"
            value={instructions}
            onChange={(event) => setInstructions(event.target.value)}
          />
        </div>
      </div>

      <div className="row g-4 mt-1">
        <div className="col-md-1">
          <h4 className="recipe-heading">Cook Time:</h4>
        </div>

        <div className="col-md-1">
          <select
            className="form-select recipe-input"
            value={hours}
            onChange={(event) => setHours(event.target.value)}
          >
            {hourOptions.map((hour) => (
               <option value={hour} key={hour}>
                {hour} hour{hour !== 1 && "s"}
               </option>
            ))}
          </select>
        </div>
        
        <div className="col-md-1">
          <select
          className="form-select recipe-input"
          value={minutes}
          onChange={(event) => setMinutes(event.target.value)}
          >
            {minuteOptions.map((minute) => (
              <option value={minute} key={minute}>
                {minute} minute{minute !== 1 && "s"}
              </option>
            ))}

          </select>
        </div>
      </div>

      <div className="row g-4 mt-1">
        <div className="col-md-1">
           <button
            className="btn custom-orange-btn mt-2"
            onClick={addRecipe}
          >
            Add Recipe
          </button>
        </div>
      </div>

    </div>
  );
}

export default RecipePlanner;
