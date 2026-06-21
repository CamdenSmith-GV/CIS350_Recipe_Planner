import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from bson import ObjectId

# imports from the main file
from main import Ingredient, Recipe, app, ListRequest, recipe_collection

# imports from the listIngredient file
from ingredient import listIngredient

# imports from the format_ouput file
from format_output import formatOuput

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
    # Should pass when amount is not numeric
    with pytest.raises(ValidationError):
        Ingredient(
            name="Sugar",
            measurement_type="volume",
            amount="two cups",  # invalid
            unit="cup"
        )

def test_missing_required_field():
    # Should pass when required field is missing
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
    #Should pass because ingredients is required
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
    # Should pass when nested ingredient is invalid
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
    # should pass for recipe_id required and frontend forgot to send data
    with pytest.raises(ValidationError):
        ListRequest()

def test_list_request_wrong_type_should_fail():
    # should pass for recipe_ids must be a list, and sending a string instead of a list
    with pytest.raises(ValidationError):
        ListRequest(recipe_ids="not-a-list")


def test_list_request_invalid_element_type_should_fail():
    # should pass for list must contain strings only, not integers or None
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
    # should pass because cook_time is required and missing from the payload
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
    # Should pass because the nested ingredient has an invalid amount type (string instead of float/int)
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
    # should pass for MongoDB error should break at the endpount and return a 500 error to the frontend (simulates a database crash)
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
    # should pass for MongoDB error should break at the endpount and return a 500 error to the frontend (simulates a database crash)
    def raise_error(*args, **kwargs):
        raise Exception("DB connection failed")

    monkeypatch.setattr(recipe_collection, "find", raise_error)

    response = client.get("/getRecipes")

    # FastAPI will return 500
    assert response.status_code == 500

def test_get_recipes_missing_id(monkeypatch):
    # should pass for missing _id field in the database response
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
    # should pass for MongoDB error should break at the endpount and return a 500 error to the frontend (simulates a database crash)
    def crash(*args, **kwargs):
        raise Exception("DB crashed")

    monkeypatch.setattr(recipe_collection, "find", crash)

    response = client.post("/groceryList", json={"recipe_ids": ["1"]})

    assert response.status_code == 500

def test_grocery_list_missing_ingredients(monkeypatch):
    # should pass for missing ingredients field in the database response
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
    # should pass for invalid ingredient structure (missing amount/unit)
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
    # should pass for invalid request type (recipe_ids must be a list, not a string)
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


"""
listIngredient class conversion tests from ingredient.py
"""
def test_add_volume_basic():
    # should pass, basic volume addition and conversion to largest unit
    ing = listIngredient("Milk")
    ing.add(1, "L")
    result = ing.getString()
    assert "Milk" in result
    assert "1 L" in result


def test_add_mass_basic():
    # should pass, basic mass addition and conversion to largest unit
    ing = listIngredient("Flour")
    ing.add(1, "kg")
    result = ing.getString()
    assert "Flour" in result
    assert "1 kg" in result


def test_add_count_only():
    # should pass, basic count addition with no unit
    ing = listIngredient("Eggs")
    ing.add(3, "count")
    result = ing.getString()
    assert "3 count" in result

def test_add_invalid_amount_type():
    # should pass, it is using a non numeric amount
    ing = listIngredient("Sugar")

    with pytest.raises(TypeError):
        ing.add("one", "kg")

def test_add_none_amount():
    # should pass, it is using a non exsistent amount
    ing = listIngredient("Milk")

    with pytest.raises(TypeError):
        ing.add(None, "L")

def test_add_negative_float():
    # should pass it is using a negative input
    ing = listIngredient("Salt")

    with pytest.raises(ValueError):
        ing.add(-0.5, "g")

def test_add_none_unit():
    # should pass as it is using an invalid type
    ing = listIngredient("Flour")

    ing.add(1, None)
    result = ing.getString()

    # should treat as count fallback
    assert "1 count" in result

def test_add_empty_unit():
    # should fail sense there is an empty string
    ing = listIngredient("Oil")

    ing.add(2, "")
    result = ing.getString()

    assert "2 count" in result

def test_add_whitespace_unit():
    # should pass because it is checking to make sure it does not allow any whitespace
    ing = listIngredient("Sugar")

    ing.add(3, "   ")
    result = ing.getString()

    assert "3 count" in result

def test_add_unknown_unit_multiple():
    # should pass because the unit inconsistentcy should not be allowed
    ing = listIngredient("Weird")

    ing.add(2, "banana")
    ing.add(3, "apple")

    result = ing.getString()

    assert "5 count" in result

def test_add_large_values():
    # should pass as this checks how it woulds with vary large inputs
    ing = listIngredient("Rice")

    ing.add(10**9, "g")

    result = ing.getString()

    assert "Rice" in result

def test_add_dict_amount():
    # should pass as it see how it works with the incorrect object being an input
    ing = listIngredient("Milk")

    with pytest.raises(TypeError):
        ing.add({"amount": 1}, "L")


"""
listIngredient class adding multiple units tests from ingredient.py            
"""
def test_multiple_add_same_unit():
    # should pass, adding multiple amounts of the same unit should accumulate correctly
    ing = listIngredient("Milk")
    ing.add(1, "L")
    ing.add(1, "L")

    result = ing.getString()
    assert "2 L" in result


def test_multiple_different_volume_units():
    # should pass, adding different volume units should convert to smallest unit and then back to largest unit correctly
    ing = listIngredient("Milk")
    ing.add(1, "L")
    ing.add(1, "cup")

    result = ing.getString()
    assert "Milk" in result
    assert "L" in result  # largest unit should dominate


def test_multiple_mass_units():
    # should pass, adding different mass units should convert to smallest unit and then back to largest unit correctly
    ing = listIngredient("Sugar")
    ing.add(1, "kg")
    ing.add(500, "g")

    result = ing.getString()
    assert "Sugar" in result
    assert "kg" in result


def test_count_accumulates():
    # should pass, adding multiple count amounts should accumulate correctly
    ing = listIngredient("Eggs")
    ing.add(1, "count")
    ing.add(2, "count")

    assert "3 count" in ing.getString()

def test_zero_amount():
    # should pass zero values should not affect totals or break the program
    ing = listIngredient("Nothing")
    ing.add(0, "kg")

    assert ing.getString().startswith("Nothing:")

def test_negative_amount():
    # should pass as we do not want to except negative numbers
    ing = listIngredient("Buggy")

    with pytest.raises(ValueError):
        ing.add(-1, "kg")


def test_unknown_unit_treated_as_count():
    # should pass unknown units should default to count instead of causing an error
    ing = listIngredient("Weird")
    ing = listIngredient("Weird")

    ing.add(5, "banana")  # not in maps

    result = ing.getString()
    assert "5 count" in result


"""
ListIngredient class rounding for display tests from ingredient.py
"""
def test_volume_rounding():
    # should pass, volume should round to 2 decimal places in the display string
    ing = listIngredient("Milk")
    ing.add(1000, "mL")  # exactly 1 L
    result = ing.getString()
    assert "1000 mL" in result


def test_mass_rounding_two_decimals():
    # should pass, mass should round to 2 decimal places in the display string
    ing = listIngredient("Flour")
    ing.add(1, "kg")
    ing.add(250, "g")  # 1.25 kg total

    result = ing.getString()
    assert "1.25 kg" in result


def test_small_volume_precision():
    # should pass, small volume amounts should round correctly and not display too many decimals
    ing = listIngredient("Oil")
    ing.add(1, "tbsp")

    result = ing.getString()
    assert "1" in result  # 14.7868 mL converted to tbsp


"""
ListIngredient class largest unit stored variable held test from ingredient.py
"""
def test_volume_largest_unit_promotion():
    # shoul pass, volume values should auto-promote to the largest appropriate unit
    ing = listIngredient("Milk")
    ing.add(1000, "mL")
    ing.add(1, "L")  # should promote to L

    result = ing.getString()
    assert "L" in result


def test_mass_largest_unit_promotion():
    # should pass, mass values should auto-promote to the largest appropriate unit
    ing = listIngredient("Sugar")
    ing.add(1000, "g")
    ing.add(1, "kg")  # should promote to kg

    result = ing.getString()
    assert "kg" in result


"""
ListIngredient class string format test from ingredient.py
"""
def test_output_format_structure():
    # should pass, as this is the ocrrect format
    ing = listIngredient("Sugar")
    ing.add(1, "kg")

    result = ing.getString()

    assert ":" in result
    assert "Sugar:" in result


"""
ListIngredient class stability test from ingredient.py
"""
def test_repeated_calls_stability():
    # should pass ensures that repeated additions accumulate correctly without losing precision
    ing = listIngredient("Stable")

    for _ in range(10):
        ing.add(1, "g")

    result = ing.getString()
    assert "10 g" in result


def test_float_inputs():
    # should pass ensures that floating point inputs are handled correctly and summed accurately
    ing = listIngredient("Oil")

    ing.add(0.5, "L")
    ing.add(0.25, "L")

    result = ing.getString()
    assert "0.75" in result


"""
format output test cases from format_output.py
"""
def test_valid_volume_addition():
    # valid case: converts volume correctly and displays in largest unit
    ing = listIngredient("Milk")
    ing.add(2, "cup")

    result = ing.getString()
    assert "Milk" in result
    assert "cup" in result

def test_valid_mass_addition():
    # valid case: converts mass correctly
    ing = listIngredient("Sugar")
    ing.add(1000, "g")

    result = ing.getString()
    assert "Sugar" in result
    assert "kg" in result or "1000 g" in result

def test_valid_count_only():
    # valid case: no unit → treated as count
    ing = listIngredient("Eggs")
    ing.add(5, "count")

    result = ing.getString()
    assert "5 count" in result

def test_edge_case_zero_value():
    # edge case: zero should not break system
    ing = listIngredient("Water")
    ing.add(0, "L")

    result = ing.getString()
    assert result.startswith("Water:")

def test_edge_case_large_values():
    # edge case: system should handle large quantities without overflow
    ing = listIngredient("Flour")
    ing.add(10_000, "g")

    result = ing.getString()
    assert "Flour" in result

def test_edge_case_floating_precision():
    # edge case: ensures no floating precision corruption
    ing = listIngredient("Oil")

    ing.add(0.1, "L")
    ing.add(0.2, "L")

    result = ing.getString()
    assert "0.3" in result or "0.30" in result

def test_edge_case_mixed_units():
    # edge case: mixing different volume units
    ing = listIngredient("Milk")

    ing.add(1, "L")
    ing.add(1, "cup")

    result = ing.getString()
    assert "Milk" in result
    assert "L" in result

def test_invalid_negative_value():
    # invalid case: negative values should be rejected
    ing = listIngredient("Sugar")

    with pytest.raises(ValueError):
        ing.add(-5, "kg")

def test_invalid_none_unit():
    # invalid case: None unit should be treated safely or rejected
    ing = listIngredient("Milk")

    ing.add(3, None)

    result = ing.getString()
    assert "3 count" in result

def test_invalid_empty_unit():
    # invalid case: empty unit should default to count
    ing = listIngredient("Eggs")

    ing.add(4, "")

    result = ing.getString()
    assert "4 count" in result

def test_invalid_non_numeric_amount():
    # invalid case: amount must be numeric
    ing = listIngredient("Flour")

    with pytest.raises(TypeError):
        ing.add("two", "kg")

def test_invalid_unknown_unit():
    # invalid case: unknown unit should default to count safely
    ing = listIngredient("Mystery")

    ing.add(7, "banana_unit")

    result = ing.getString()
    assert "7 count" in result