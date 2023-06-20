from biosim.cell import Lowland, Water, Desert
import random


cell = Lowland((1, 1))

ini_herb = {'species': 'Herbivore', 'age': 1, 'weigt': 1}

cell.add_animal_from_dict(ini_herb)