# fast api and server imported libraries
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

# Pydantic library for data validation and settings management using Python type annotations
from pydantic import BaseModel
from typing import List, Optional

# MongoDB drivers
from pymongo import MongoClient

# file imports
from ingredient import listIngredient 
from format_output import formatOuput

# Classes
# allows us to easily call the ingreidents from the recipe and use them in the frontend
# this class represents a single ingredient in the recipe
class Ingredient(BaseModel):
    name: str
    measurement_type: str  # "volume", "mass", "quantity"
    amount: float
    unit: Optional[str] = None


# allows us to call the recipe and use it in the frontend, it also allows us to call the ingredients from the recipe and use them in the frontend
# this class with represent one entire receipe
class Recipe(BaseModel):
    name: str
    summary: str
    instructions: str
    cook_time: int
    ingredients: List[Ingredient]

class ListRequest(BaseModel):
    recipe_ids: List[str]


# this class is used to get the list of recipe ids from the frontend and use them in the backend to generate the grocery list
class ListRequest(BaseModel):
    recipe_ids: List[str]


# setup fo rthe fast api server
app = FastAPI(debug=True)


# connects to the MongoDB server cluster
client = MongoClient(
    "mongodb+srv://calihanw_db_user:popcorn@cluster.ivrzvu1.mongodb.net/"
)


# database and collection selection
db = client["recipe_database"]
recipe_collection = db["recipes"]


# CORS config (This is what allows the frontend to make a requerst to the backend API)
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


# creates and stores a brand new recipe in the MongoDB database
@app.post("/createRecipe")
def create_recipe(recipe: Recipe):
    try:
        recipe_collection.insert_one(
            recipe.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str("database error"))

    return recipe


# This will retrieve all of the recipes from MongoDB and will return them back to the frontend
@app.get("/getRecipes")
def get_recipes():
    try:     
        recipes = list(
            recipe_collection.find({})
        )

        for recipe in recipes:
            recipe["id"] = str(recipe.pop("_id"))

        return recipes
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str("database error"))


# will generate a full grocery list of what the user has selected from their recipes
@app.post("/groceryList")
def get_grocery_list(request: ListRequest):

    try:
        recipes = list(
                recipe_collection.find({})
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str("database error"))

    # converts ids
    for recipe in recipes:
        if "_id" in recipe:
            recipe["id"] = str(recipe.pop("_id"))
        else:
            recipe["id"] = None

    recipes = [recipe for recipe in recipes if recipe["id"] in request.recipe_ids]

    # Loop through recipes
    # If a new ingrediant is found make a new ingrediant object call add function
    # Add ingrediant to the list of ingrediant objects
    # If ingrediant with said name is in list only need to call add function
    
    ingredients = {}

    for recipe in recipes:
        for ingre in recipe.get("ingredients", []):
            name = ingre.get("name")
            amount = ingre.get("amount")
            unit = ingre.get("unit")

            if name is None or amount is None:
                raise HTTPException(status_code=500, detail=str("invalid ingredient structure"))

            if name not in ingredients:
                ingredients[name] = listIngredient(name)

            ingredients[name].add(amount, unit)
    
    filename = formatOuput(ingredients)

    try:
        with open(filename, "r") as f:
            output = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str("error reading grocery list file"))

    return Response(
        content=output,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=grocery_list.txt"},
    )

# this is what will run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
    """ 
    use this to run the server
    py -m uvicorn main:app --reload --port 3001
    """
