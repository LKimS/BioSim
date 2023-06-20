"""Implements diffrent characteristics of cells."""

from .animals import Herbivore, Carnivore

import random


class Cell:
    """
    Cell characteristics for cells without animals.
    The cell can have a type, color and if it is habitable or not.
    """
    type = None
    color = None
    _habitable = False

    def __init__(self, location):
        """
        Initializes the Cell class. A class without animals.

        Parameters
        ----------
        location : tuple
            Location of the cell
        """
        self.location = location

    def add_animal_from_dict(self, animal_info):
        """
        Raises an error if animal is added to a cell that is not habitable.

        Parameters
        ----------
        animal_info : dict
            Dictionary with information about the animal

        Raises
        -------
        ValueError
            If animal species is invalid

        """
        raise ValueError(f"Cannot add animal to {type(self)} cell at loc: {self.location}")

    @classmethod
    def set_parameters(cls, params):
        """
        Raises an error if this class has no changeable parameters.

        Parameters
        ----------
        params : dict
            Dictionary with parameters

        Raises
        -------
        ValueError
            If this class has no changeable parameters
        """
        raise ValueError(f"{type(cls)} cell has no changeable parameters")

    @property
    def is_habitable(self):
        """
        Checks if cell is habitable.

        Returns
        -------
        bool: True if habitable, False if not


        """
        return self._habitable


class Cell_with_animals(Cell):
    """
    Cell characteristics for cells with animals.
    This is a subclass of Cell.
    """
    _habitable = True

    def __init__(self, location):
        """
        Initializes the Cell_with_animals class. A class with animals.

        Parameters
        ----------
        location : tuple
            Location of the cell
        """
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

    # General methods
    def add_animal_from_dict(self, animal_info):
        """
        If the animal dictionary keys is valid, it creates an animal object and adds it to the cell.
        Raises an error if animal dictionary keys has invalid type of species, age or weight.

        Parameters
        ----------
        animal_info : dict
            Dictionary with information about the animal.

        Raises
        -------
        ValueError
            Animal species, age or weight is invalid.
        """

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
        If an animal object is valid, it is added to the cell.
        Raises an error if object has invalid species.

        Parameters
        ----------
        animal : object
            Animal object.

        Raises
        -------
        ValueError
            Invalid animal species.
        """
        new_animal_species = animal.species

        if new_animal_species not in self.fauna.keys():
            raise ValueError(f"Invalid animal species: {new_animal_species}")

        self.fauna[new_animal_species].append(animal)

    def remove_animal(self, animal):
        """
        If method is called with an animal object, it is removed from the cell.

        Parameters
        ----------
        animal : object
            Animal object.
        """
        animal_species = animal.species
        self.fauna[animal_species].remove(animal)

    def _sort_herbivore_after_fitness(self, descending=True):
        """
        Sorts herbivores after fitness
        Parameters
        ----------
        self
        descending=True

        """
        self.fauna["Herbivore"].sort(key=lambda animal: animal.fitness, reverse=descending)

    # Annual cycle methods
    def add_newborns(self):
        """
        Check if any animals will give birth, and adds newborns to the cell.
        The method sends the number of animals in the cell to the procreation method,
        and it returns a newborn object.
        """

        for species, animal_list in self.fauna.items():
            for animal in animal_list:
                newborn = animal.procreation(len(animal_list))
                if newborn is not None:
                    self.fauna[species].append(newborn)

    def feed_animals(self):
        """
        Feeding method for predators, Carnivores, in a cell. A random Carnivore eats the
        Herbivores with the lowest fitness first. Method calls the feeding method in the
        Carnivore class. And removes dead animals from the cell.
        """
        # skip if there is no herbivores in the cell
        if self.count_herbivore > 0:
            self._sort_herbivore_after_fitness(descending=False)
            random.shuffle(self.fauna["Carnivore"])
            for animal in self.fauna["Carnivore"]:
                animal.feeding(self.fauna["Herbivore"])

                # remove dead animals
                herbivores = self.fauna["Herbivore"]
                self.fauna["Herbivore"] = [animal for animal in herbivores if animal.alive]

    def moving_animals_list(self):
        """
        Method for moving animals from one cell to another.
        The method checks if any animals will migrate, and
        returns a list with the object that will move.

        Returns
        -------
        list : list of tuples
            List of tuples with animal object, old location and new location.

        """
        moving_animals = []
        for animal in self.animals:
            if animal.migrate():
                new_location = self._get_random_neighboring_cell(self.location)
                moving_animals.append((animal, self.location, new_location))

        return moving_animals

    def reset_fodder(self):
        """
        Method for resetting fodder in the cell. This class has no fodder, so the method is empty.
        """
        # this class has no fodder
        pass

    def _get_random_neighboring_cell(self, location):
        """
        Returns a random neighboring cell.

        Parameters
        ----------
        location : tuple

        Returns
        -------
        new location : tuple
            Tuple with new coordinates.
        """
        new_location = []

        # Change in direction       South, North, West, East
        direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])

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
        Reduces weight of all animals in the cell.
        Calls the loss_of_weight() method in the animal class.
        """
        for animal in self.animals:
            animal.loss_of_weight()

    def animal_death(self):
        """
        Checks if any animals will die in the cell, and removes them from the cell.
        Uses the death method in the animal class.
        """
        for species, animal_list in self.fauna.items():
            for animal in animal_list:
                animal.death()
            # Remove dead animals
            self.fauna[species] = [animal for animal in animal_list if animal.alive]

    @property
    def count_herbivore(self):
        """
        Returns the number of herbivores in the cell.

        Returns
        -------
        int
        """
        return len(self.fauna["Herbivore"])

    @property
    def count_carnivore(self):
        """
        Returns the number of carnivores in the cell.

        Returns
        -------
        int
        """
        return len(self.fauna["Carnivore"])


class Cell_with_fodder(Cell_with_animals):
    """
    Cell characteristics with fodder for vegetarian animals
    This is a subclass of Cell_with_animals.
    """
    f_max = None

    default_parameters = {'f_max': f_max}

    @classmethod
    def set_parameters(cls, new_parameters):
        """
        Set the default parameters for the cell

        Parameters
        ----------
        new_parameters : dict
            Dictionary with new parameters

        Raises
        ------
        ValueError
            If the parameter is not valid
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
        Get the actual parameters for the cell.
        Collects the parameter form the class and returns f_max.
        """
        return {'f_max': cls.f_max}

    def __init__(self, location):
        """
        Initialize the Cell_with_fodder class. A class with fodder and animals.

        Parameters
        ----------
        location : tuple
            Tuple with coordinates for the cell.
        """
        super().__init__(location)
        self.fodder = self.f_max

    def feed_animals(self):
        """
        Feed all vegetarian animals, Herbivores, in the cell.
        Animals with the highest fitness eats first.
        Methods calls the feeding method in the Herbivore class.
        """
        self._sort_herbivore_after_fitness()
        for animal in self.fauna["Herbivore"]:
            if self.fodder > 0:
                self.fodder -= animal.feeding(self.fodder)
            else:
                break

        super().feed_animals()

    def reset_fodder(self):
        """
        Reset the fodder in the cell to the maximum value.
        This method is called at the end of each year.
        """
        self.fodder = self.f_max


class Water(Cell):
    """
    Water is a subclass of Cell. And in this class there is no fodder and no animals.
    This class is not habitable.
    """
    type = "Water"
    color = (0.13, 0.00, 1.00)


class Desert(Cell_with_animals):
    """
    Dessert is a subclass of Cell_with_animals.
    In this class animals can move, and predators can eat.
    """
    type = "Desert"
    color = (1.00, 1.00, 0.40)


class Lowland(Cell_with_fodder):
    """
    Lowland is a subclass of Cell_with_fodder.
    Lowland has a large amount of fodder, and all animals will thrive.
    """
    type = "Lowland"
    f_max = 800
    color = (0.00, 0.62, 0.00)
    default_parameters = {'f_max': f_max}


class Highland(Cell_with_fodder):
    """
    Highland is a subclass of Cell_with_fodder.
    Highland has a limited amount of fodder, and Herbivores will struggle to find food.
    Predators can live on their prey until there is no Herbivores left.
    """
    type = "Highland"
    f_max = 300
    color = (0.20, 1.00, 0.42)
    default_parameters = {'f_max': f_max}
