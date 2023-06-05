from biosim.animals import Animal

"""
core methods:
- remove animal when dead
- sort animals by fitness
- update fodder
- feed animals
"""

class Cell:
    geography = {
        "W": {
            "type": "Water",
            "fodder": 0,
            "herbivore": 0,
            "carnivore": 0,
            "color": (0.13, 0.00, 1.00)
        },
        "L": {
            "type": "Lowland",
            "fodder": 0,
            "herbivore": 0,
            "carnivore": 0,
            "color": (0.00, 0.62, 0.00)
        },
        "H": {
            "type": "Highland",
            "fodder": 0,
            "herbivore": 0,
            "carnivore": 0,
            "color": (0.20, 1.00, 0.42)
        },
        "D": {
            "type": "Desert",
            "fodder": 0,
            "herbivore": 0,
            "carnivore": 0,
            "color": (1.00, 1.00, 0.40)
        }
    }

    def __init__(self, letter, location):
        self.location = location
        self.type = self.geography[letter]["type"]
        self.fodder = self.geography[letter]["fodder"]
        self.herbivore = []
        self.carnivore = []
        self.count_herbivore = 0
        self.count_carnivore = 0
        self.color = self.geography[letter]["color"]

    def add_animal(self, animal_info):
        if animal_info["species"] == "Herbivore":
            self.herbivore.append(Animal(animal_info, self.location))
        elif animal_info["species"] == "Carnivore":
            self.carnivore.append(Animal(animal_info, self.location))
        else:
            raise ValueError("Invalid animal species")

    def count_animals(self):
        self.count_herbivore = len(self.herbivore)
        self.count_carnivore = len(self.carnivore)