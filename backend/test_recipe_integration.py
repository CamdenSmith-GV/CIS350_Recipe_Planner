from main import create_recipe, get_recipes, recipe_collection, Recipe, Ingredient


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
