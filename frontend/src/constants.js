/**
 * @file ./frontend/src/constants.js
 * @author Camden Smith
 * @course CIS350
 * @date 6/5/2026
 * @brief Shared constants and helpers for ingredient entry.
 */

export const VOLUME_UNITS = ["tsp", "tbsp", "fl oz", "cup", "pint", "quart", "gallon", "mL", "L"];
export const MASS_UNITS = ["oz", "lbs", "g", "kg"];

export const emptyRow = () =>
({
  name: "",
  measurementType: "", // quantity, volume, mass
  unit: "", // unit for volume and mass
  amount: "", // the amount typed in
});
