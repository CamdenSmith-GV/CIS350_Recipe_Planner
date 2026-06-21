def formatOuput(ingredient_array):
    """
    Generates a formatted .txt grocery list from a 
    dictionary of the listIngredients objects
    """
    fopen = open("Grocery_List.txt", "w")
    fopen.write("Grocery List:\n\n")
    for name in ingredient_array:
        ingredient = ingredient_array[name]
        fopen.write(f"{ingredient.getString()}\n")

    fopen.close()
    return "Grocery_List.txt"