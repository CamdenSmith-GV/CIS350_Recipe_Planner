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

MASS_TO_G = {
    "kg": 1000,
    "lbs": 453.592,
    "oz": 28.3495,
    "g": 1,
}


class listIngredient:
    def __init__(self, name):
        self.name = name
        self.count = 0.0
        self.ml = 0.0
        self.g = 0.0
        self.vol_largest_unit = "mL"
        self.mass_largest_unit = "g"

    
    def add(self, amount, unit):
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
        result = ""
        result_Q = result_V = result_M = "" 
        if self.count > 0: result_Q += f"{self.count} count"
        if self.ml > 0: result_V += f"{self.ml / VOLUME_TO_ML[self.vol_largest_unit]} {self.vol_largest_unit}"
        if self.g > 0: result_M += f"{self.g / MASS_TO_G[self.mass_largest_unit]} {self.mass_largest_unit}"
        result = "+".join([x for x in (result_Q, result_V, result_M) if x])
        return result