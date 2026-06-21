from main import (
    create_recipe,
    get_recipes,
    get_grocery_list,
    recipe_collection,
    Recipe,
    Ingredient,
    ListRequest,
)


def test_create_then_get_recipe():
    """
    Calls our create_recipe function to save a recipe to the
    database, then calls get_recipes to pull it back and checks the data
    matches. Cleans up the test recipe at the end so nothing is left behind.
    """
    recipe = Recipe(
        name="Test Pancakes",
        summary="Breakfast food",
        instructions="Make it or something",
        cook_time=10,
        ingredients=[
            Ingredient(name="Flour", measurement_type="volume", amount=2, unit="cup")
        ],
    )
   
    # create the recipe using our function
    create_recipe(recipe)

    # pull all recipes back using our function and find the one we made
    all_recipes = get_recipes()
    pulled = [r for r in all_recipes if r["name"] == "Test Pancakes"]

    assert len(pulled) == 1
    assert pulled[0]["name"] == "Test Pancakes"
    assert pulled[0]["summary"] == "Breakfast food"
    assert pulled[0]["instructions"] == "Make it or something"
    assert pulled[0]["cook_time"] == 10
    assert pulled[0]["ingredients"][0]["name"] == "Flour"


    # clean up so we don't leave the test recipe in the real database
    recipe_collection.delete_many({"name": "Test Pancakes"})

def test_get_grocery_list():
    """
    Creates a recipe with a few ingredients, then calls get_grocery_list with
    that recipe's id and checks the ingredients show up in the list. Cleans up
    the test recipe at the end so nothing is left behind.
    """
    recipe = Recipe(
        name="Test Pancakes",
        summary="Breakfast food",
        instructions="Make it or something",
        cook_time=10,
        ingredients=[
            Ingredient(name="Flour", measurement_type="volume", amount=2, unit="cup"),
            Ingredient(name="Flour", measurement_type="volume", amount=2, unit="tbsp"),
            Ingredient(name="Flour", measurement_type="mass", amount=500, unit="g"),
            Ingredient(name="Egg", measurement_type="quantity", amount=2, unit=None),
        ],
    )

    # create the recipe and grab its id back from the database
    create_recipe(recipe)
    all_recipes = get_recipes()
    recipe_id = [r for r in all_recipes if r["name"] == "Test Pancakes"][0]["id"]

    # make the grocery list of just the test recipe
    response = get_grocery_list(ListRequest(recipe_ids=[recipe_id]))
    output = response.body.decode()

    # Volumes are (2 cup + 2 tbsp) = 2.13 cup, and the
    # 500g should be written on the same line
    assert "Flour: 2.13 cup + 500 g" in output

    # the egg should show up as a count
    assert "Egg: 2 count" in output

    # clean up so we don't leave the test recipe in the real database
    recipe_collection.delete_many({"name": "Test Pancakes"})