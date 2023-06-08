from .animals import Herbivore, Carnivore

"""
core methods:
- remove animal when dead
- sort animals by fitness
- update fodder
- feed animals
- add baby animals
"""

class Cell:
    type = None
    max_fodder = None
    color = None

    def __init__(self, location):
        self.location = location
        self.fodder = self.max_fodder
        self.herbivore = []
        self.carnivore = []
        self.count_herbivore = 0
        self.count_carnivore = 0

    def add_animal(self, animal_info):
        if animal_info["species"] == "Herbivore":
            self.herbivore.append(Herbivore(animal_info, self.location))
        elif animal_info["species"] == "Carnivore":
            self.carnivore.append(Carnivore(animal_info, self.location))
        else:
            raise ValueError("Invalid animal species")

    def count_animals(self):
        self.count_herbivore = len(self.herbivore)
        self.count_carnivore = len(self.carnivore)

    def get_newborns(self, animal_list):
        newborns = [{
            'loc': self.location,
            'pop': []
        }]
        for animal in animal_list:
            newborn = animal.procreation(len(animal_list))
            if newborn is not None:
                newborns[0]['pop'].append(newborn)

        return newborns

    def feed_animals(self):
        self.sort_herbivore_after_fitness()
        for animal in self.herbivore:
            if self.fodder > 0:
                self.fodder -= animal.feeding(self.fodder)

            else:
                break

        for animal in self.carnivore:
            # TODO: implement feeding for carnivores
            pass

    def update_fitness(self):
        for animal in self.herbivore:
            animal.fitness = animal.calc_fitness()

        for animal in self.carnivore:
            animal.fitness = animal.calc_fitness()

    def sort_herbivore_after_fitness(self):
        self.herbivore.sort(key=lambda animal: animal.fitness, reverse=True)
    def age_animals(self):
        for animal in self.herbivore:
            animal.aging()

        for animal in self.carnivore:
            animal.aging()

    def loss_of_weight(self):
        for animal in self.herbivore:
            animal.loss_of_weight()

        for animal in self.carnivore:
            animal.loss_of_weight()

    def animal_death(self):
        for animal in self.herbivore:
            animal.death()
        self.herbivore = [animal for animal in self.herbivore if animal.alive]

        for animal in self.carnivore:
            animal.death()
        self.carnivore = [animal for animal in self.carnivore if animal.alive]

    def reset_fodder(self):
        self.fodder = self.max_fodder
    @property
    def num_herbivore(self):
        return self.count_herbivore

    @property
    def num_carnivore(self):
        return self.count_carnivore


class Water(Cell):
    type = "Water"
    max_fodder = 0
    color = (0.13, 0.00, 1.00)
    
class Lowland(Cell):
    type = "Lowland"
    max_fodder = 800
    color = (0.00, 0.62, 0.00)
    
class Highland(Cell):
    type = "Highland"
    max_fodder = 300
    color = (0.20, 1.00, 0.42)
    
class Desert(Cell):
    type = "Desert"
    max_fodder = 0
    color = (1.00, 1.00, 0.40)


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

    def get_newborns(self, animal_list):
        newborns = [{
            'loc': self.location,
            'pop': []
        }]
        for animal in animal_list:
            newborn = animal.cycle_procreation()
            newborns[0]['pop'].append(newborn)

        return newborns

    def feed_animals(self):
        pass
"""