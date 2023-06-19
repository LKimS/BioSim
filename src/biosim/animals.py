"""
Implements the Animal class.
"""

import math
import random


class Animal:
    """Animals witch can be herbivore or carnivore with attributes and methods for both. """

    # These parameters are defined at the class level

    default_parameters = {'w_birth': None, 'sigma_birth': None,
                          'beta': None, 'eta': None, 'a_half': None,
                          'phi_age': None, 'w_half': None,
                          'phi_weight': None, 'mu': None,
                          'gamma': None, 'zeta': None, 'xi': None,
                          'omega': None, 'F': None, 'DeltaPhiMax': None}

    params = default_parameters.copy()

    @classmethod
    def set_parameters(cls, new_parameters):
        """
        Set class parameters.

        Parameters
        ----------
        new_parameters : dict
            Legal keys: 'w_birth', 'sigma_birth', 'beta', 'eta', 'a_half',
            'phi_age', 'w_half', 'phi_weight', 'mu', 'gamma', 'zeta', 'xi',
            'omega', 'F', 'DeltaPhiMax'.

        Raises
        ------
        ValueError, KeyError
        """

        for key in new_parameters:
            if key not in cls.default_parameters.keys():
                raise ValueError('Invalid parameter name: ' + key)

        # All parameters must be positive
        for key in new_parameters:
            if not (type(new_parameters[key]) == int or type(new_parameters[key]) == float):
                raise ValueError('All parameters must be positive numbers')
            elif not new_parameters[key] >= 0:
                raise ValueError('All parameters must be positive numbers')
            else:
                cls.params[key] = new_parameters[key]

        # DeltaPhiMax must be strictly positive
        if 'DeltaPhiMax' in new_parameters:
            if not new_parameters['DeltaPhiMax'] > 0:
                raise ValueError('DeltaPhiMax must be strictly positive')
            else:
                cls.params["DeltaPhiMax"] = new_parameters['DeltaPhiMax']

        # Eta must be less than 1
        if 'eta' in new_parameters:
            if new_parameters['eta'] >= 1:
                raise ValueError('eta must be less than 1')
            else:
                cls.params["eta"] = new_parameters['eta']

    @classmethod
    def get_parameters(cls):
        """Get parameter for the Animal.
        :return: dict
        """
        return cls.params

    def __init__(self, row, loc):
        """Create an animal with attributes from row and loc."""
        self.row = row
        self.loc = loc
        self.species = self.row["species"]
        self.age = self.row["age"]
        self.weight = self.row["weight"]
        self.fitness = self._calc_fitness()
        self.alive = True
        self.newborn = None

    def procreation(self, animal_in_pos):
        """
        Returns a new animal if the animal procreates, None otherwise.
        Repeat given text a given number of times.

        Parameters
        ----------
        animal_in_pos : int
            Animals in the same position as the parent.

        Returns
        -------
        dict
            Dictionary with a newborn animal.
        """
        self.newborn = None
        zeta = self.params["zeta"]
        w_birth = self.params["w_birth"]
        sigma_birth = self.params["sigma_birth"]
        gamma = self.params["gamma"]
        xi = self.params["xi"]

        offspring_value = zeta * (w_birth + sigma_birth)
        if self.weight >= offspring_value:
            probability_of_procreation = min(1, gamma * self.fitness * animal_in_pos)
            if random.random() < probability_of_procreation:
                # 'newborn log calc'
                mu = math.log(w_birth ** 2 / (
                    math.sqrt(w_birth ** 2 + sigma_birth ** 2)))
                sigma = math.sqrt(math.log(1 + (sigma_birth ** 2 / w_birth ** 2)))
                newborn_weight = random.lognormvariate(mu, sigma)

                parent_loss = xi * newborn_weight
                if self.weight > parent_loss:
                    self.weight -= parent_loss
                    self.newborn = True
                    self._update_fitness()
                    newborn_info = {"species": self.species, "age": 0, "weight": newborn_weight}
                    return type(self)(newborn_info, self.loc)

            # 'animal does not procreate'
        return None

    def _calc_fitness(self):
        """Calculates the fitness of the animal."""
        if self.weight <= 0:
            return 0
        else:
            phi_weight = self.params["phi_weight"]
            phi_age = self.params["phi_age"]
            a_half = self.params["a_half"]
            w_half = self.params["w_half"]

            age_parameter = 1 / (1 + math.exp(
                phi_age * (self.age - a_half)))
            weight_parameter = 1 / (1 + math.exp(-phi_weight * (self.weight - w_half)))
            return age_parameter * weight_parameter

    def _update_fitness(self):
        """Updates the fitness of the animal."""
        self.fitness = self._calc_fitness()

    def aging(self):
        """Animal ages by one year."""
        self.age += 1

    def loss_of_weight(self):
        """Animal loses weight by one year"""
        self.weight -= self.params["eta"] * self.weight
        self._update_fitness()

    def death(self):
        """Sets the animal to False if it dies, true otherwise."""

        probability_of_death = self.params["omega"] * (1 - self.fitness)
        if self.weight <= 0:
            self.alive = False
        elif random.random() < probability_of_death:
            self.alive = False
        else:
            # self.alive = True
            pass

    def migrate(self):
        """Returns True if the animal migrates, False otherwise."""
        probability_of_migration = self.params["mu"] * self.fitness
        if random.random() < probability_of_migration:
            return True
        else:
            return False


class Herbivore(Animal):
    default_parameters = {'w_birth': 8.0, 'sigma_birth': 1.5,
                          'beta': 0.9, 'eta': 0.05, 'a_half': 40.0,
                          'phi_age': 0.6, 'w_half': 10.0,
                          'phi_weight': 0.1, 'mu': 0.25,
                          'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                          'omega': 0.4, 'F': 10.0}

    params = default_parameters.copy()

    def feeding(self, fodder):
        """Herbivore eats the amount of fodder given, or the maximum amount of fodder it can eat."""
        if fodder < self.params["F"]:
            amount_eaten = fodder
        else:
            amount_eaten = self.params["F"]

        self.weight += (amount_eaten * self.params["beta"])
        self._update_fitness()
        return amount_eaten


class Carnivore(Animal):
    default_parameters = {'w_birth': 6.0, 'sigma_birth': 1.0,
                          'beta': 0.75, 'eta': 0.125, 'a_half': 40.0,
                          'phi_age': 0.3, 'w_half': 4.0,
                          'phi_weight': 0.4, 'mu': 0.4,
                          'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
                          'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0}

    params = default_parameters.copy()

    def feeding(self, sorted_lowest_fitness_herbivore):
        """
        Carnivore kills the weakest herbivore until it has eaten the amount of fodder it can eat.
        """
        delta_phi_max = self.params["DeltaPhiMax"]
        amount_eaten = 0

        for herbivore in sorted_lowest_fitness_herbivore:
            if amount_eaten >= self.params["F"]:
                break

            diff_fitness = self.fitness - herbivore.fitness
            if diff_fitness < 0:
                probability_of_killing = 0
            elif 0 < diff_fitness < delta_phi_max:
                probability_of_killing = (self.fitness - herbivore.fitness) / delta_phi_max
            else:
                probability_of_killing = 1

            if random.random() < probability_of_killing:
                desired_food = self.params["F"] - amount_eaten
                if herbivore.weight > desired_food:
                    eating = desired_food
                else:
                    eating = herbivore.weight

                self.weight += eating * self.params["beta"]
                herbivore.alive = False
                self._update_fitness()
                amount_eaten += eating
