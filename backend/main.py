import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List


class Ingredient(BaseModel):
    name: str
    quantity: float


app = FastAPI(debug=True)

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

memory_db = {"ingredients": []}


@app.get("/getIngredients", response_model=List[Ingredient])
def get_ingredients():
    return memory_db["ingredients"]


@app.post("/createIngredient")
def create_ingredient(ingredient: Ingredient):
    memory_db["ingredients"].append(ingredient)
    return ingredient


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
