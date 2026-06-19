
from ingredient import listIngredient 
from format_output import formatOuput
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from pymongo import MongoClient
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Optional
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

class ListRequest(BaseModel):
    recipe_ids: List[str]


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


@app.post("/groceryList")
def get_grocery_list(request: ListRequest):

    recipes = list(
            recipe_collection.find({})
        )

    for recipe in recipes:
        recipe["id"] = str(recipe.pop("_id"))

    recipes = [recipe for recipe in recipes if recipe["id"] in request.recipe_ids]

    # Loop through recipes
    # If a new ingrediant is found make a new ingrediant object call add function
    # Add ingrediant to the list of ingrediant objects
    # If ingrediant with said name is in list only need to call add function
    
    ingredients = {}

    for recipe in recipes:
        for ingre in recipe["ingredients"]:
            name = ingre["name"]
            key = name.lower().rstrip()
            if len(key) > 1 and key[-1] == "s":
                key = key[:-1]
            if key not in ingredients:
                ingredients[key] = listIngredient(name)
            ingredients[key].add(ingre["amount"], ingre["unit"])
    
    filename = formatOuput(ingredients)

    with open(filename, "r") as f:
        output = f.read()

    return Response(
        content=output,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=grocery_list.txt"},
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)