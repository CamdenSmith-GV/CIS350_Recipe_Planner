import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Dict, Optional
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Dict, Optional
from pydantic import BaseModel

#Classes
# allows us to easily call the ingreidents from the recipe and use them in the frontend
class Ingredient(BaseModel):
    name: str
    measurement_type: str  # "volume", "mass", "quantity"
    amount: float
    unit: Optional[str] = None

# allows us to call the recipe and use it in the frontend, it also allows us to call the ingredients from the recipe and use them in the frontend
class Recipe(BaseModel):
    name: str
    summary: str
    instructions: str
    cook_time: int
    ingredients: List[Ingredient]


app = FastAPI(debug=True)

client = MongoClient(
    "mongodb+srv://calihanw_db_user:popcorn@cluster.ivrzvu1.mongodb.net/"
)

db = client["recipe_database"]
recipe_collection = db["recipes"]

origins = [
    "http://localhost:3000",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/createRecipe")
def create_recipe(recipe: Recipe):
    print(Recipe)
    recipe_collection.insert_one(
        recipe.model_dump()
    )

    return recipe

@app.get("/getRecipes")
def get_recipes():

    recipes = list(
        recipe_collection.find({})
    )

    for recipe in recipes:
        recipe["id"] = str(recipe.pop("_id"))

    return recipes


@app.get("/getGroceryList")
def get_grocery_list():

    recipes = list(
        recipe_collection.find(
            {},
            {"_id": 0}
        )
    )

    ingredient_array = []

    ingredient_quantity = 0
    ingredient_volume = 0
    ingredient_mass = 0

    largest_volume = "mL"
    largest_mass = "g"

    with open("grocery_list.txt", "w") as f:
        for recipe in recipes:
            for ingredient in recipe["ingredients"]:
                if ingredient["name"] not in ingredient_array:
                    ingredient_array.append(ingredient["name"])
                    f.write(f"{ingredient['name']}: ")
                    for recipe in recipes:
                        for ingredient in recipe["ingredients"]:
                            if ingredient["name"] == ingredient_array[-1]:
                                
                                if ingredient["measurement_type"] == "quantity":
                                    ingredient_quantity += ingredient["amount"]
                                
                                # Adding Volumes Together and Converting to the Largest Unit
                                elif ingredient["measurement_type"] == "volume":
                                    if ingredient["unit"] == "gallon":
                                        ingredient_volume += (ingredient["amount"] * 3786) # convert gallon to ml (rounded from 3785.41)
                                        largest_volume = "gallon"
                                    elif ingredient["unit"] == "L":
                                        ingredient_volume += (ingredient["amount"] * 1000) # convert l to ml
                                        if largest_volume != "gallon":
                                            largest_volume = "l"
                                    elif ingredient["unit"] == "quart":
                                        ingredient_volume += (ingredient["amount"] * 946) # convert quart to ml (rounded from 946.353)
                                        if largest_volume != "gallon" and largest_volume != "L":
                                            largest_volume = "quart"
                                    elif ingredient["unit"] == "pint":
                                        ingredient_volume += (ingredient["amount"] * 473) # convert pint to ml (rounded from 473.176)
                                        if largest_volume != "gallon" and largest_volume != "L" and largest_volume != "quart":
                                            largest_volume = "pint"
                                    elif ingredient["unit"] == "cup":
                                        ingredient_volume += (ingredient["amount"] * 237) # convert cup to ml (rounded from 236.588)
                                        if largest_volume != "gallon" and largest_volume != "L" and largest_volume != "quart" and largest_volume != "pint":
                                            largest_volume = "cup"
                                    elif ingredient["unit"] == "fl oz":
                                        ingredient_volume += (ingredient["amount"] * 30) # convert fl oz to ml (rounded from 29.5735)
                                        if largest_volume != "gallon" and largest_volume != "L" and largest_volume != "quart" and largest_volume != "pint" and largest_volume != "cup":
                                            largest_volume = "fl oz"
                                    elif ingredient["unit"] == "tbsp":
                                        ingredient_volume += (ingredient["amount"] * 15) # convert tbsp to ml (rounded from 14.7868)
                                        if largest_volume != "gallon" and largest_volume != "L" and largest_volume != "quart" and largest_volume != "pint" and largest_volume != "cup" and largest_volume != "fl oz":
                                            largest_volume = "tbsp"
                                    elif ingredient["unit"] == "tsp":
                                        ingredient_volume += (ingredient["amount"] * 5) # convert tsp to ml (rounded from 4.92892)
                                        if largest_volume != "gallon" and largest_volume != "L" and largest_volume != "quart" and largest_volume != "pint" and largest_volume != "cup" and largest_volume != "fl oz" and largest_volume != "tbsp":
                                            largest_volume = "tsp"
                                    else:
                                        ingredient_volume += ingredient["amount"]
                                
                                # Adding Masses Together and Converting to the Largest Unit       
                                elif ingredient["measurement_type"] == "mass":
                                    if ingredient["unit"] == "kg":
                                        ingredient_mass += (ingredient["amount"] * 1000) # convert kg to g
                                        largest_mass = "kg"
                                    elif ingredient["unit"] == "lbs":
                                        ingredient_mass += (ingredient["amount"] * 454) # convert lbs to g (rounded from 453.592)
                                        if largest_mass != "kg":
                                            largest_mass = "lbs"
                                    elif ingredient["unit"] == "oz":
                                        ingredient_mass += (ingredient["amount"] * 29) # convert oz to g (rounded from 28.3495)
                                        if largest_mass != "kg" and largest_mass != "lbs":
                                            largest_mass = "oz"
                                    else:
                                        ingredient_mass += ingredient["amount"]

                    if ingredient_quantity > 0:
                        f.write(f"{ingredient_quantity} count + ")
                    
                    if ingredient_volume > 0:
                        if largest_volume == "L":
                            f.write(f"{ingredient_volume / 1000} L + ")
                        elif largest_volume == "cup":
                            f.write(f"{ingredient_volume / 237} cups + ")
                        elif largest_volume == "tbsp":
                            f.write(f"{ingredient_volume / 15} tbsp + ")
                        elif largest_volume == "tsp":
                            f.write(f"{ingredient_volume / 5} tsp + ")
                        elif largest_volume == "ml":
                            f.write(f"{ingredient_volume} ml")
                    
                    if ingredient_mass > 0:
                        if largest_mass == "kg":
                            f.write(f"{ingredient_mass / 1000} kg")
                        elif largest_mass == "lbs":
                            f.write(f"{ingredient_mass / 454} lbs")
                        elif largest_mass == "oz":
                            f.write(f"{ingredient_mass / 29} oz")
                        elif largest_mass == "g":
                            f.write(f"{ingredient_mass} g")

                    f.write("\n\n")
                    
                    ingredient_quantity = 0
                    ingredient_volume = 0
                    ingredient_mass = 0

                    largest_volume = "mL"
                    largest_mass = "g"

    with open("grocery_list.txt", "r") as f:
        output = f.read()

    return Response(
        content=output,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=grocery_list.txt"},
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)