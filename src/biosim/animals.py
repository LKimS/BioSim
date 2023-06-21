"""
Implements a class for animals.
"""

import math
import random


class Animal:
    """
    A complete lifecycle to an animal on the island.
    """
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
        Set adjusted parameters from user for the animal class.

        Parameters
        ----------
        new_parameters : dict
            Legal keys

        Raises
        ------
        ValueError
            If any of the parameters are invalid.

        ValueError
            If any of the parameters are negative.

        ValueError
            If DeltaPhiMax is not strictly positive.

        ValueError
            If eta is not less than 1.


        .. note::
            Legal keys are those in the default_parameters class attribute.

            - 'w_birth'
            - 'sigma_birth'
            - 'beta'
            - 'eta'
            - 'a_half'
            - 'phi_age'
            - 'w_half'
            - 'phi_weight'
            - 'mu'
            - 'gamma'
            - 'zeta'
            - 'xi'
            - 'omega'
            - 'F'
            - 'DeltaPhiMax'



        """
        # check for invalid parameters
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
        """
        Get parameters returns the current parameters for the animal class.

        Returns
        --------
        cls.param : dict
            Dictionary with the current parameters for the animal class.
        """
        return cls.params

    def __init__(self, row, loc):
        """Create an animal with attributes from row and loc."""
        self.row = row
        self.loc = loc
        self.species = self.row["species"]
        self.age = self.row["age"]
        self.weight = self.row["weight"]
        self.fitness = self.calc_fitness()
        self.alive = True
        self.newborn = None

    def procreation(self, animal_in_pos):
        r"""
        Methods checks if the animal can give birth to a new animal.
        Bellow is the steps taken by the method:

        - If the offspring value is less than the weight of the animal, the animal can give birth.
        - If the animal can give birth, the probability of procreation is calculated.
        - If the animal procreates, the weight of the newborn is calculated.
        - Newborn weight is subtracted from the parent.
        - The fitness of the parent is updated.
        - A newborn object is added to the list of newborns.

        Parameters
        ----------
        animal_in_pos : int
            Number of animals in the same position as the animal.

        Returns
        -------
        Animal instance or None
            If the animal procreates, a newborn animal is returned. Else None is returned.


        .. note::

            - Relevant parameters are given in the table at the beginning of the
            Animal class documentation.

            The probability of procreation is given by the formula below.

            .. math::
                p_{procreation} =
                min(1, gamma \cdot fitness_{self} \cdot N_{same})

            Where :math:`N_{same}` is the number of animals in the same position as the animal.

            The weight of the newborn is calculated by a log-normal distribution from the python
            ``random.lognormvariate(mu, sigma)``.
            Below is a figure of the log-normal distribution, and formulas for
            calculating the parameters mu and sigma.

            .. math::
                mu = \ln \left( \frac{w_{birth}^2}{\sqrt{w_{birth}^2 + \sigma_{birth}^2}}\right)

                sigma = \sqrt{\ln \left(1 + \frac{\sigma_{birth}^2}{w_{birth}^2} \right)}

            .. figure:: ../docs/figures/lognormdist.png
                :width: 400
                :align: center
                :alt: lognormdist.png

                Source: https://en.wikipedia.org/wiki/Log-normal_distribution
        """
        # Initialize variables
        self.newborn = None
        zeta = self.params["zeta"]
        w_birth = self.params["w_birth"]
        sigma_birth = self.params["sigma_birth"]
        gamma = self.params["gamma"]
        xi = self.params["xi"]

        # Calculate probability of procreation
        offspring_value = zeta * (w_birth + sigma_birth)
        if self.weight >= offspring_value:
            probability_of_procreation = min(1, gamma * self.fitness * animal_in_pos)

            if random.random() < probability_of_procreation:
                # Calculate weight of newborn
                mu = math.log(w_birth ** 2 / (
                    math.sqrt(w_birth ** 2 + sigma_birth ** 2)))
                sigma = math.sqrt(math.log(1 + (sigma_birth ** 2 / w_birth ** 2)))
                newborn_weight = random.lognormvariate(mu, sigma)

                # Check if parent has enough weight to give birth
                parent_loss = xi * newborn_weight
                if self.weight > parent_loss:
                    self.weight -= parent_loss
                    self.newborn = True
                    self._update_fitness()
                    newborn_info = {"species": self.species, "age": 0, "weight": newborn_weight}
                    return type(self)(newborn_info, self.loc)

        # animal does not procreate
        return None

    def calc_fitness(self):
        r"""
        The overall condition of the animal is described by the fitness.
        This method calculates the fitness of the animal.

        Returns
        -------
        float
            The fitness of the animal.


        .. note::
            Fitness is calculated by the following formula:

            .. math::

                \Phi =
                \frac{1}{1+e^{\phi_{age} \cdot (age - a_{half})}}
                \cdot
                \frac{1}{1+e^{-\phi_{weight} \cdot (weight - w_{half})}}

            Where :math:`\phi_{age}` and :math:`\phi_{weight}` are parameters given by the user.
            :math:`a_{half}` and :math:`w_{half}` are parameters given by the user.
            :math:`age` and :math:`weight` are the age and weight of the animal.
            :math:`\phi` is the fitness of the animal.
        """
        if self.weight <= 0:
            return 0
        else:
            phi_weight = self.params["phi_weight"]
            phi_age = self.params["phi_age"]
            a_half = self.params["a_half"]
            w_half = self.params["w_half"]

            age_parameter = 1 / (1 + math.exp(phi_age * (self.age - a_half)))
            weight_parameter = 1 / (1 + math.exp(-phi_weight * (self.weight - w_half)))
            return age_parameter * weight_parameter

    def _update_fitness(self):
        """
        Updates the fitness of the animal.
        """
        self.fitness = self.calc_fitness()

    def aging(self):
        """
        Methods that ages animals by one year.
        Fitness of the animal is updated in next method loss_of_weight(). This
        makes the code more efficient.
        """
        self.age += 1

    def loss_of_weight(self):
        r"""
        Methods that makes the animal lose weight. Since animals lose weight,
        the fitness of the animal is updated.
        Animal loses an amount of weight given by the following formula:

        .. math::
            weight loss = \eta \cdot weight

        Where eta, :math:`\eta`, is a default parameter or parameter given by the user.
        """
        self.weight -= self.params["eta"] * self.weight
        self._update_fitness()

    def death(self):
        r"""
        Methods sets the animal to dead if the animals weight is below zero or
        if the animal dies by a probability of death.

        Probability of death is given by the following formula:

        .. math::
            p_{death} = \omega \cdot (1 - \phi)

        Where omega, :math:`\omega`, is a default parameter or given by the user.
        Fitness, :math:`\phi`, is the fitness of the animal.
        """
        probability_of_death = self.params["omega"] * (1 - self.fitness)
        if self.weight <= 0:
            self.alive = False
        elif random.random() < probability_of_death:
            self.alive = False
        else:
            pass

    def migrate(self):
        r"""
        Methods checks if the animal migrates or not. With a higher
        fitness the probability of migration increases.

        Probability of migration is given by the following formula:

        .. math::
            p_{migration} = \mu \cdot \phi

        Where mu, :math:`\mu`, is a default parameter or given by the user.
        Fitness, :math:`\phi`, is the fitness of the animal.

        Returns
        -------
        bool
            True if the animal migrates, False if the animal does not migrate.
        """
        probability_of_migration = self.params["mu"] * self.fitness
        if random.random() < probability_of_migration:
            return True
        else:
            return False


class Herbivore(Animal):
    """
    Herbivores depends on the amount of food available to survive and reproduce.
    """
    default_parameters = {'w_birth': 8.0, 'sigma_birth': 1.5,
                          'beta': 0.9, 'eta': 0.05, 'a_half': 40.0,
                          'phi_age': 0.6, 'w_half': 10.0,
                          'phi_weight': 0.1, 'mu': 0.25,
                          'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                          'omega': 0.4, 'F': 10.0}

    params = default_parameters.copy()

    def feeding(self, fodder):
        """
        Feeding method for planteating animals, herbivores. Herbivore eats the amount
        of fodder given, or the maximum amount of fodder it can eat. After eating the animal
        gains weight and the fitness is updated.

        Parameters
        ----------
        fodder : float
            The amount of fodder available to the animal.

        Returns
        -------
        amount_eaten : float
            The amount of fodder eaten by the animal.
        """
        if fodder < self.params["F"]:
            amount_eaten = fodder
        else:
            amount_eaten = self.params["F"]

        # Add weight and update fitness
        self.weight += (amount_eaten * self.params["beta"])
        self._update_fitness()
        return amount_eaten


class Carnivore(Animal):
    """
    Carnivores depends on the availability of prey to survive and reproduce.
    """
    default_parameters = {'w_birth': 6.0, 'sigma_birth': 1.0,
                          'beta': 0.75, 'eta': 0.125, 'a_half': 40.0,
                          'phi_age': 0.3, 'w_half': 4.0,
                          'phi_weight': 0.4, 'mu': 0.4,
                          'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
                          'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0}

    params = default_parameters.copy()

    def feeding(self, sorted_lowest_fitness_herbivore):
        """
        Feeding method for predators, carnivores.

        - Carnivore tries to kill, with a probability, the weakest herbivore until it's full.
        - After eating one animal it gains weight and the fitness is updated.
        - If an animal is killed, the object variable "alive" is set to False.
        - Carnivore continues to kill until it has tried to kill all Herbivores in the cell.


        Parameters
        ----------
        sorted_lowest_fitness_herbivore : list
            List of herbivores sorted by lowest fitness.
        """
        delta_phi_max = self.params["DeltaPhiMax"]
        amount_eaten = 0

        # loop over all herbivores in the cell and eats them if the conditions are met.
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
