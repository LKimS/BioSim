from .animals import Herbivore, Carnivore
import random

"""
core methods:
- remove animal when dead
- sort animals by fitness
- update fodder
- feed animals
- add baby animals
"""

class Cell:
    """
    Class for a cell in the island
    """
    type = None
    color = None
    _habitable = False


    def __init__(self, location):
        self.location = location

    def add_animal(self, animal_info):
        raise ValueError(f"Cannot add animal to {type(self)} cell")

    @classmethod
    def set_parameters(cls, params):
        raise ValueError(f"{type(self)} cell has no changeable parameters")

    @property
    def is_habitable(self):
        return self._habitable


class Cell_with_animals(Cell):

    _habitable = True

    def __init__(self, location):
        super().__init__(location)
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

    def update_animal_count(self):
        self.count_herbivore = len(self.herbivore)
        self.count_carnivore = len(self.carnivore)

    def add_newborns(self, animal_list):

        newborn_list = []

        for animal in animal_list:
            newborn = animal.procreation(len(animal_list))
            if newborn is not None:
                newborn_list.append(newborn)

        if newborn_list != []:
            species = newborn_list[0].species


            if species == "Herbivore":
                self.herbivore.extend(newborn_list)
            elif species == "Carnivore":
                self.carnivore.extend(newborn_list)


    def feed_animals(self):
        self.sort_herbivore_after_fitness(descending=False)
        random.shuffle(self.carnivore)
        for animal in self.carnivore:
            animal.feeding(self.herbivore)
            #remove dead animals
            self.herbivore = [animal for animal in self.herbivore if animal.alive]


    def update_fitness(self):
        for animal in self.herbivore:
            animal.fitness = animal.calc_fitness()

        for animal in self.carnivore:
            animal.fitness = animal.calc_fitness()

    def sort_herbivore_after_fitness(self, descending=True):
        self.herbivore.sort(key=lambda animal: animal.fitness, reverse=descending)

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




class Cell_with_fodder(Cell_with_animals):
    """
    Class for a cell in the island
    """
    f_max =None

    default_parameters = {'f_max': f_max}

    @classmethod
    def set_parameters(cls, new_parameters):
        """
        Set the default parameters for the cell
        Parameters
        ----------
        new_parameters

        """
        for key in new_parameters:
            if key not in (cls.default_parameters.keys()):
                raise ValueError("Invalid parameter: " + key)

        if 'f_max' in new_parameters:
            if new_parameters['f_max'] < 0:
                raise ValueError("Invalid parameter: f_max must be positive")
            cls.f_max = new_parameters['f_max']

    @classmethod
    def get_parameters(cls):
        """
        Get the default parameters for the cell
        :return: dict
        """
        return {'f_max': cls.f_max}
    def __init__(self, location):
        super().__init__(location)
        self.fodder = self.f_max

    def feed_animals(self):
        self.sort_herbivore_after_fitness()
        for animal in self.herbivore:
            if self.fodder > 0:
                self.fodder -= animal.feeding(self.fodder)
            else:
                break

        super().feed_animals()

        self.reset_fodder()


    def reset_fodder(self):
        self.fodder = self.f_max

class Water(Cell):
    type = "Water"
    color = (0.13, 0.00, 1.00)

class Desert(Cell_with_animals):
    type = "Desert"
    color = (1.00, 1.00, 0.40)
    
class Lowland(Cell_with_fodder):
    type = "Lowland"
    f_max = 800
    color = (0.00, 0.62, 0.00)
    
class Highland(Cell_with_fodder):
    type = "Highland"
    f_max = 300
    color = (0.20, 1.00, 0.42)
    



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