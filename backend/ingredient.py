# converts all of the possible selected cooking volume units into milliliters 
VOLUME_TO_ML = {
    "gallon": 3785.41,
    "L": 1000,
    "quart": 946.353,
    "pint": 473.176,
    "cup": 236.588,
    "fl oz": 29.5735,
    "tbsp": 14.7868,
    "tsp": 4.92892,
    "mL": 1,
}

# converts all of the possible selected cooking mass units into grams
MASS_TO_G = {
    "kg": 1000,
    "lbs": 453.592,
    "oz": 28.3495,
    "g": 1,
}

class listIngredient:
    """
    This class will track a single ingredient accross multiple recipes (this is called when the grocery list is being made)
    It will automatically convert all the units to a common unit the make them into the largest possible unit that was selected by the user via their recipe
    It will seperate volumes, mass, and qunaintity into different categories and will add them together to make the grocery list easier to read for the user 
    """
    def __init__(self, name):
        self.name = name

        # accumulates all of the amounts of the ingredient that are in count, volume, and mass units
        self.count = 0.0
        self.ml = 0.0
        self.g = 0.0

        # tracks the largest unit that is selected
        self.vol_largest_unit = "mL"
        self.mass_largest_unit = "g"

    def add(self, amount, unit):
        """
        This adds a new amount of the ingredient to the total amount and converts it to the smallest unit of volume or mass if needed
        volume to mL, mass to g, and quantities are just added together 
        """
        if unit in VOLUME_TO_ML:
            self.ml += amount * VOLUME_TO_ML[unit]
            
            if VOLUME_TO_ML[self.vol_largest_unit] < VOLUME_TO_ML[unit]:
                self.vol_largest_unit = unit

        elif unit in MASS_TO_G:
            self.g += amount * MASS_TO_G[unit]

            if MASS_TO_G[self.mass_largest_unit] < MASS_TO_G[unit]:
                self.mass_largest_unit = unit
       
        else:
            self.count += amount

    def getString(self):
        """
        this is what will return to the main and is added to the .txt file for the ingredient in the grocery list. 
        It will convert the total amount back into the largest unit that was selected by the user and will format it nicely for the user to read
        """
        result = self.name
        result_Q = result_V = result_M = "" 

        # formats count items
        if self.count > 0: result_Q += f"{self.count} count"

        # formats volume items
        if self.ml > 0: result_V += f"{self.ml / VOLUME_TO_ML[self.vol_largest_unit]} {self.vol_largest_unit}"

        # formats mass items
        if self.g > 0: result_M += f"{self.g / MASS_TO_G[self.mass_largest_unit]} {self.mass_largest_unit}"

        # combines the different types of units into one string with the correct formatting
        result = result + ": " + " + ".join([x for x in (result_Q, result_V, result_M) if x])
        return result