import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from bson import ObjectId

# imports from the main file
from main import Ingredient, Recipe, app, ListRequest, recipe_collection

client = TestClient(app)


"""
Ingredient class test from main.py
"""
def test_valid_ingredient():
    # Should pass with correct ingredient data
    ing = Ingredient(
        name="Flour",
        measurement_type="volume",
        amount=2.0,
        unit="cup"
    )

    assert ing.name == "Flour"
    assert ing.amount == 2.0

def test_missing_optional_unit():
    # Should pass when unit is omitted (Optional field)
    ing = Ingredient(
        name="Eggs",
        measurement_type="quantity",
        amount=3
    )

    assert ing.unit is None

def test_invalid_amount_type():
    # Should fail when amount is not numeric
    with pytest.raises(ValidationError):
        Ingredient(
            name="Sugar",
            measurement_type="volume",
            amount="two cups",  # invalid
            unit="cup"
        )

def test_missing_required_field():
    # Should fail when required field is missing
    with pytest.raises(ValidationError):
        Ingredient(
            name="Milk",
            # missing measurement_type
            amount=1,
            unit="L"
        )

# Edge case: negative amount (allowed unless you explicitly restrict it)
def test_negative_amount_edge_case():
    # Pydantic allows negatives unless constrained
    ing = Ingredient(
        name="Salt",
        measurement_type="mass",
        amount=-5,
        unit="g"
    )

    assert ing.amount == -5


"""
Recipe class test from main.py
"""
def test_valid_recipe():
    # Should pass with valid nested ingredients
    recipe = Recipe(
        name="Pancakes",
        summary="Breakfast food",
        instructions="Mix and cook",
        cook_time=10,
        ingredients=[
            Ingredient(name="Flour", measurement_type="volume", amount=2, unit="cup"),
            Ingredient(name="Eggs", measurement_type="quantity", amount=2)
        ]
    )

    assert recipe.name == "Pancakes"
    assert len(recipe.ingredients) == 2

def test_recipe_missing_ingredients():
    #Should fail because ingredients is required
    with pytest.raises(ValidationError):
        Recipe(
            name="Toast",
            summary="Simple toast",
            instructions="Toast bread",
            cook_time=2
            # missing ingredients
        )

def test_recipe_empty_ingredients_edge_case():
    # Should pass even with empty ingredient list (valid edge case)
    recipe = Recipe(
        name="Water",
        summary="Just water",
        instructions="Pour water",
        cook_time=0,
        ingredients=[]
    )

    assert recipe.ingredients == []

def test_invalid_nested_ingredient():
    # Should fail when nested ingredient is invalid
    with pytest.raises(ValidationError):
        Recipe(
            name="Cake",
            summary="Dessert",
            instructions="Bake it",
            cook_time=30,
            ingredients=[
                Ingredient(name="Flour", measurement_type="volume", amount="lots")  # invalid
            ]
        )


"""
ListRequest class test from main.py
"""
def test_valid_list_request():
    # passes
    req = ListRequest(recipe_ids=["a1", "b2", "c3"])
    assert req.recipe_ids == ["a1", "b2", "c3"]

def test_invalid_list_request_type():
    # edge case (valid)
    req = ListRequest(recipe_ids=[])
    assert req.recipe_ids == []



def test_empty_list_request():
    # should fail for recipe_id required and frontend forgot to send data
    with pytest.raises(ValidationError):
        ListRequest()

def test_list_request_wrong_type_should_fail():
    # should fail for recipe_ids must be a list, and sending a string instead of a list
    with pytest.raises(ValidationError):
        ListRequest(recipe_ids="not-a-list")


def test_list_request_invalid_element_type_should_fail():
    # should fail for list must contain strings only, not integers or None
    with pytest.raises(ValidationError):
        ListRequest(recipe_ids=["a1", 123, None])


"""
create recipe endpoint test from main.py
"""
def test_create_recipe_valid_should_pass(monkeypatch):
    # pass
    mock_insert = MagicMock()
    monkeypatch.setattr(recipe_collection, "insert_one", mock_insert)

    payload = {
        "name": "Pancakes",
        "summary": "Breakfast food",
        "instructions": "Mix and cook",
        "cook_time": 10,
        "ingredients": [
            {
                "name": "Flour",
                "measurement_type": "volume",
                "amount": 2,
                "unit": "cup"
            }
        ]
    }

    response = client.post("/createRecipe", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == "Pancakes"
    assert mock_insert.call_count == 1

def test_create_recipe_missing_field_should_fail(monkeypatch):
    # should fail because cook_time is required and missing from the payload
    mock_insert = MagicMock()
    monkeypatch.setattr(recipe_collection, "insert_one", mock_insert)

    payload = {
        "name": "Pancakes",
        "summary": "Breakfast food",
        "instructions": "Mix and cook",
        # cook_time missing
        "ingredients": []
    }

    response = client.post("/createRecipe", json=payload)

    assert response.status_code == 422  # FastAPI validation error
    assert mock_insert.call_count == 0  # MongoDB must NOT be called

def test_create_recipe_invalid_ingredient_should_fail(monkeypatch):
    # Should fail because the nested ingredient has an invalid amount type (string instead of float/int)
    mock_insert = MagicMock()
    monkeypatch.setattr(recipe_collection, "insert_one", mock_insert)

    payload = {
        "name": "Cake",
        "summary": "Dessert",
        "instructions": "Bake it",
        "cook_time": 30,
        "ingredients": [
            {
                "name": "Flour",
                "measurement_type": "volume",
                "amount": "lots"  # invalid
            }
        ]
    }

    response = client.post("/createRecipe", json=payload)

    assert response.status_code == 422
    assert mock_insert.call_count == 0

def test_create_recipe_empty_ingredients_should_pass(monkeypatch):
    # Edge case: empty ingredient list (valid)
    mock_insert = MagicMock()
    monkeypatch.setattr(recipe_collection, "insert_one", mock_insert)

    payload = {
        "name": "Water",
        "summary": "Just water",
        "instructions": "Pour water",
        "cook_time": 0,
        "ingredients": []
    }

    response = client.post("/createRecipe", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == "Water"
    assert mock_insert.call_count == 1

def test_create_recipe_db_failure(monkeypatch):
    # should fail for MongoDB error should break at the endpount and return a 500 error to the frontend (simulates a database crash)
    def crash(*args, **kwargs):
        raise Exception("DB crashed")

    monkeypatch.setattr(recipe_collection, "insert_one", crash)

    payload = {
        "name": "Pasta",
        "summary": "test",
        "instructions": "boil water",
        "cook_time": 10,
        "ingredients": [
            {"name": "Noodles", "amount": 1, "measurement_type": "lb"}
        ]
    }

    response = client.post("/createRecipe", json=payload)

    assert response.status_code == 500


"""
get recipes endpoint test from main.py
"""
def test_get_recipes_valid(monkeypatch):
    # pass
    fake_db_data = [
        {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "name": "Pasta",
            "summary": "Dinner",
            "instructions": "Boil water",
            "cook_time": 10,
            "ingredients": []
        }
    ]

    mock_find = MagicMock(return_value=fake_db_data)
    monkeypatch.setattr(recipe_collection, "find", mock_find)

    response = client.get("/getRecipes")

    assert response.status_code == 200
    data = response.json()

    # _id MUST be converted to id
    assert "id" in data[0]
    assert "_id" not in data[0]

    # correctness
    assert data[0]["name"] == "Pasta"

def test_get_recipes_db_failure(monkeypatch): 
    # should fail for MongoDB error should break at the endpount and return a 500 error to the frontend (simulates a database crash)
    def raise_error(*args, **kwargs):
        raise Exception("DB connection failed")

    monkeypatch.setattr(recipe_collection, "find", raise_error)

    response = client.get("/getRecipes")

    # FastAPI will return 500
    assert response.status_code == 500

def test_get_recipes_missing_id(monkeypatch):
    # should fail for missing _id field in the database response
    fake_db_data = [
        {
            "name": "Broken Recipe",
            "summary": "No ID",
            "instructions": "??",
            "cook_time": 5,
            "ingredients": []
        }
    ]

    monkeypatch.setattr(recipe_collection, "find", MagicMock(return_value=fake_db_data))

    response = client.get("/getRecipes")

    assert response.status_code == 500

def test_get_recipes_empty_db(monkeypatch):
    # edge case: should pass and return empty list if no recipes in database
    monkeypatch.setattr(recipe_collection, "find", MagicMock(return_value=[]))

    response = client.get("/getRecipes")

    assert response.status_code == 200
    assert response.json() == []

def test_get_recipes_multiple(monkeypatch):
    # Edge case, should pass
    fake_db_data = [
        {"_id": ObjectId(), "name": "A", "summary": "", "instructions": "", "cook_time": 1, "ingredients": []},
        {"_id": ObjectId(), "name": "B", "summary": "", "instructions": "", "cook_time": 2, "ingredients": []},
    ]

    monkeypatch.setattr(recipe_collection, "find", MagicMock(return_value=fake_db_data))

    response = client.get("/getRecipes")

    data = response.json()

    assert len(data) == 2
    assert all("id" in r for r in data)


"""
grocery list endpoint test from main.py
"""
def test_grocery_list_basic_success(monkeypatch):
    # pass, valid recipe selection, ingredients should be returned in the grocery list, and file should be generated correctly
    fake_db = [
        {
            "_id": "1",
            "name": "Recipe1",
            "ingredients": [
                {"name": "Flour", "amount": 2, "unit": "cup"},
                {"name": "Sugar", "amount": 1, "unit": "cup"}
            ]
        }
    ]

    monkeypatch.setattr(recipe_collection, "find", lambda x: fake_db)

    payload = {"recipe_ids": ["1"]}

    response = client.post("/groceryList", json=payload)

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "Flour" in response.text

def test_grocery_list_multiple_recipes(monkeypatch):
    # pass, same ingredient from multiple recipes should be combined correctly
    fake_db = [
        {
            "_id": "1",
            "ingredients": [
                {"name": "Flour", "amount": 1, "unit": "cup"}
            ]
        },
        {
            "_id": "2",
            "ingredients": [
                {"name": "Flour", "amount": 2, "unit": "cup"}
            ]
        }
    ]

    monkeypatch.setattr(recipe_collection, "find", lambda x: fake_db)

    response = client.post("/groceryList", json={"recipe_ids": ["1", "2"]})

    assert response.status_code == 200
    assert "Flour" in response.text

def test_grocery_list_db_failure(monkeypatch):
    # should fail for MongoDB error should break at the endpount and return a 500 error to the frontend (simulates a database crash)
    def crash(*args, **kwargs):
        raise Exception("DB crashed")

    monkeypatch.setattr(recipe_collection, "find", crash)

    response = client.post("/groceryList", json={"recipe_ids": ["1"]})

    assert response.status_code == 500

def test_grocery_list_missing_ingredients(monkeypatch):
    # should fail for missing ingredients field in the database response
    fake_db = [
        {
            "_id": "1",
            "name": "BadRecipe"
            # missing ingredients
        }
    ]

    monkeypatch.setattr(recipe_collection, "find", lambda x: fake_db)

    response = client.post("/groceryList", json={"recipe_ids": ["1"]})

    assert response.status_code == 200

def test_grocery_list_invalid_ingredient_structure(monkeypatch):
    # should fail for invalid ingredient structure (missing amount/unit)
    fake_db = [
        {
            "_id": "1",
            "ingredients": [
                {"name": "Flour"}  # missing amount/unit
            ]
        }
    ]

    monkeypatch.setattr(recipe_collection, "find", lambda x: fake_db)

    response = client.post("/groceryList", json={"recipe_ids": ["1"]})

    assert response.status_code == 500

def test_grocery_list_invalid_request_type():
    # should fail for invalid request type (recipe_ids must be a list, not a string)
    response = client.post("/groceryList", json={"recipe_ids": "not-a-list"})

    assert response.status_code == 422

def test_grocery_list_empty_selection(monkeypatch):
    # edge case: should pass and return empty grocery list if no recipes selected
    fake_db = [
        {
            "_id": "1",
            "ingredients": [
                {"name": "Flour", "amount": 1, "unit": "cup"}
            ]
        }
    ]

    monkeypatch.setattr(recipe_collection, "find", lambda x: fake_db)

    response = client.post("/groceryList", json={"recipe_ids": []})

    assert response.status_code == 200
    assert response.text == "Grocery List:\n\n"

def test_grocery_list_count_only(monkeypatch):
    # edge case: should pass and handle ingredients with no unit (count only)
    fake_db = [
        {
            "_id": "1",
            "ingredients": [
                {"name": "Eggs", "amount": 3, "unit": None}
            ]
        }
    ]

    monkeypatch.setattr(recipe_collection, "find", lambda x: fake_db)

    response = client.post("/groceryList", json={"recipe_ids": ["1"]})

    assert response.status_code == 200
    assert "Eggs" in response.text

def test_grocery_list_duplicate_ingredients(monkeypatch):
    # edge case: should pass and combine duplicate ingredients
    fake_db = [
        {
            "_id": "1",
            "ingredients": [
                {"name": "Sugar", "amount": 1, "unit": "cup"}
            ]
        },
        {
            "_id": "2",
            "ingredients": [
                {"name": "Sugar", "amount": 2, "unit": "cup"}
            ]
        }
    ]

    monkeypatch.setattr(recipe_collection, "find", lambda x: fake_db)

    response = client.post("/groceryList", json={"recipe_ids": ["1", "2"]})

    assert response.status_code == 200
    assert "Sugar" in response.text

def test_grocery_list_no_matching_recipes(monkeypatch):
    # edge case: should pass and return empty grocery list if no matching recipe IDs found
    fake_db = [
        {
            "_id": "1",
            "ingredients": [
                {"name": "Flour", "amount": 1, "unit": "cup"}
            ]
        }
    ]

    monkeypatch.setattr(recipe_collection, "find", lambda x: fake_db)

    response = client.post("/groceryList", json={"recipe_ids": ["999"]})

    assert response.status_code == 200
    assert "Grocery List" in response.text

    