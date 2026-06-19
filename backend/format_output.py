def formatOuput(ingredient_array):
    
    fopen = open("Grocery_List.txt", "w")

    for name in ingredient_array:
        ingredient = ingredient_array[name]
        fopen.write(f"{ingredient.getString()}\n")

    fopen.close()
    return "Grocery_List.txt"