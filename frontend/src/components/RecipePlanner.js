/**
 * @file ./frontend/src/components/RecipePlanner.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/5/2026
 * @brief Recipe planner: enter ingredients one at a time and list them.
 */

import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";
import { VOLUME_UNITS, MASS_UNITS, emptyRow } from "../constants";

function RecipePlanner()
{
  const [ingredients, setIngredients] = useState([]);
  const [instructions, setInstructions] = useState("");
  const [hours, setHours] = useState("0");
  const [minutes, setMinutes] = useState("0");
  const [row, setRow] = useState(emptyRow());

  const hourOptions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

  const updateRow = (changes) =>
  {
    setRow((current) => ({ ...current, ...changes }));
  };

  const handleMeasurementTypeChange = (measurementType) =>
  {
    updateRow({ measurementType, unit: "", amount: "" });
  };

  const addIngredient = () =>
  {
    if (row.name.trim() === "") {
      return;
    }
    setIngredients([...ingredients, row]);
    setRow(emptyRow());
  };

  let unitOptions = [];

  if (row.measurementType === "volume")
  {
    unitOptions = VOLUME_UNITS;
  }
  else if (row.measurementType === "mass")
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

  return (
    <div className="container-fluid mt-4">
      <h1 className="mb-3">Recipe Planner</h1>
      <div className="row g-4">
        <div className="col-md-6">
          {/* Ingrediant enter col*/}
          <div className="row g-2 align-items-center mb-2">
            {/* Ingredient name */}
            <div className="col">
              <input
                className="form-control"
                type="text"
                placeholder="Ingredient..."
                value={row.name}
                onChange={(event) => updateRow({ name: event.target.value })}
              />
            </div>

            {/* Measurement type dropdown */}
            <div className="col-auto">
              <select
                className="form-select"
                value={row.measurementType}
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
                  className="form-select"
                  value={row.unit}
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

            {/* Amount box (shown once a measurement type is chosen) */}
            {row.measurementType !== "" && (
              <div className="col-auto">
                <input
                  className="form-control"
                  type="number"
                  placeholder="Amount..."
                  value={row.amount}
                  onChange={(event) => updateRow({ amount: event.target.value })}
                />
              </div>
            )}
          </div>

          <button
            className="btn custom-orange-btn mt-2"
            onClick={addIngredient}
          >
            Add Ingredient
          </button>
        </div>

        <div className="col-md-6">
          <div className="card p-4 shadow-sm">
            <h2>Current Ingredients</h2>

            {ingredients.map((ingredient, index) => (
              <p key={index}>{formatIngredient(ingredient)}</p>
            ))}
          </div>
        </div>
      </div>

      <div className="row g-4">
        {/* Enter Instructions */}
        <div className="col-md-6">
          <h4>Instructions:</h4>
          <textarea
            className="form-control"
            placeholder="Instructions..."
            rows="5"
            value={instructions}
            onChange={(event) => setInstructions(event.target.value)}
          />
        </div>
      </div>

      <div className="row g-4">
        <div className="col-md-1">
          <select
            className="form-select"
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
      </div>
    </div>
  );
}

export default RecipePlanner;
