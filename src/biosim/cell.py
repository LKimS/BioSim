"""Implements the Cell class."""

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

    def add_animal_from_dict(self, animal_info):
        raise ValueError(f"Cannot add animal to {type(self)} cell at loc: {self.location}")

    @classmethod
    def set_parameters(cls, params):
        raise ValueError(f"{type(cls)} cell has no changeable parameters")

    @property
    def is_habitable(self):
        return self._habitable

class Cell_with_animals(Cell):

    _habitable = True

    def __init__(self, location):
        super().__init__(location)
        self.fauna = {'Herbivore': [], 'Carnivore': []}
        self.cell_pop_history = {'Herbivore': [], 'Carnivore': []}

        self.species = {'Herbivore': Herbivore, 'Carnivore': Carnivore}

    @property
    def animals(self):
        animals = []

        for animal_list in self.fauna.values():
            animals.extend(animal_list)
        return animals

    #General methods
    def add_animal_from_dict(self, animal_info):

        valid_keys = ["species", "age", "weight"]

        for key, value in animal_info.items():
            if key not in valid_keys:
                raise ValueError(f"Invalid key: {key}. Valid keys are: {valid_keys}")
            if key == "species" and value not in ["Herbivore", "Carnivore"]:
                raise ValueError(f"Invalid species: {value}")
            if key == "age" and (value < 0 or type(value) != int):
                raise ValueError(f"Invalid age: {value}. Age must be a non negative integer")
            if key == "weight" and value <= 0:
                raise ValueError(f"Invalid weight: {value}. Weight must be a positive number")

        new_animal = self.species[animal_info["species"]](animal_info, self.location)
        self.fauna[animal_info["species"]].append(new_animal)


    def add_animal_object(self, animal):
        """
        Adds an animal object to the cell
        Parameters
        ----------
        animal
        """

        new_animal_species = animal.species

        if new_animal_species not in self.fauna.keys():
            raise ValueError(f"Invalid animal species: {new_animal_species}")

        self.fauna[new_animal_species].append(animal)

    def remove_animal(self, animal):
        """
        Removes an animal object from the cell
        """
        animal_species = animal.species
        self.fauna[animal_species].remove(animal)

    def sort_herbivore_after_fitness(self, descending=True):
        self.fauna["Herbivore"].sort(key=lambda animal: animal.fitness, reverse=descending)


    # TODO: is this used
    def update_fitness(self):

        for animal in self.animals:
            animal.fitness = animal.calc_fitness()
    #Annual cycle methods

    def add_newborns(self):
        """
        Adds newborns to the cell
        """
        for species, animal_list in self.fauna.items():
            for animal in animal_list:
                newborn = animal.procreation(len(animal_list))
                if newborn is not None:
                    self.fauna[species].append(newborn)


    def feed_animals(self):

        # skip if there is no herbivores in the cell
        if self.count_herbivore > 0:
            self.sort_herbivore_after_fitness(descending=False)
            random.shuffle(self.fauna["Carnivore"])
            for animal in self.fauna["Carnivore"]:
                animal.feeding(self.fauna["Herbivore"])

                #remove dead animals
                self.fauna["Herbivore"] = [animal for animal in self.fauna["Herbivore"] if animal.alive]

    def moving_animals_list(self):
        """
        Returns a list of animals that will move
        """
        moving_animals = []
        for animal in self.animals:
            if True:
                new_location = self.get_random_neighboring_cell(self.location)
                moving_animals.append((animal, self.location, new_location))

        return moving_animals

    def reset_fodder(self):
        #this cell has no fodder
        pass

    def get_random_neighboring_cell(self, location):
        """
        Returns a random neighboring cell.
        """
        new_location = []

        # Change in direction       South, North, West, East
        direction = random.choice([(-1,0), (1,0), (0,-1), (0,1)])

        # Calculate new coordinates
        for current, change in zip(location, direction):
            new_location.append(current + change)

        return tuple(new_location)

    def age_animals(self):
        """
        Ages all animals in the cell with one year
        """
        for animal in self.animals:
            animal.aging()

    def loss_of_weight(self):
        """
        Updates the weight of all animals in the cell
        """
        for animal in self.animals:
            animal.loss_of_weight()
    def animal_death(self):
        """
        Removes dead animals from the cell
        """
        for species, animal_list in self.fauna.items():
            for animal in animal_list:
                animal.death()

            self.fauna[species] = [animal for animal in animal_list if animal.alive]





    @property
    def count_herbivore(self):
        return len(self.fauna["Herbivore"])

    @property
    def count_carnivore(self):
        return len(self.fauna["Carnivore"])

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
        for animal in self.fauna["Herbivore"]:
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
    default_parameters = {'f_max': f_max}
    
class Highland(Cell_with_fodder):
    type = "Highland"
    f_max = 300
    color = (0.20, 1.00, 0.42)
    default_parameters = {'f_max': f_max}
