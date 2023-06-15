"""
Implements the Animal class.
"""

import math
import random

class Animal:
    """Animals witch can be herbivore or carnivore with attributes and methods for both. """

    # These parameters are defined at the class level
    w_birth = None
    sigma_birth = None
    beta = None
    eta = None
    a_half = None
    phi_age = None
    w_half = None
    phi_weight = None
    mu = None
    gamma = None
    zeta = None
    xi = None
    omega = None
    F = None
    DeltaPhiMax = None

    default_parameters = {'w_birth': w_birth, 'sigma_birth': sigma_birth,
                     'beta': beta, 'eta': eta, 'a_half': a_half,
                     'phi_age': phi_age, 'w_half': w_half,
                     'phi_weight': phi_weight, 'mu': mu,
                     'gamma': gamma, 'zeta': zeta, 'xi': xi,
                     'omega': omega, 'F': F, 'DeltaPhiMax': DeltaPhiMax}

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
            if key not in ('w_birth', 'sigma_birth', 'beta', 'eta', 'a_half',
                           'phi_age', 'w_half', 'phi_weight', 'mu', 'gamma', 'zeta', 'xi',
                           'omega', 'F', 'DeltaPhiMax'):
                raise KeyError('Invalid parameter name: ' + key)

        #All parameters must be positive
        for key in new_parameters:
            if not new_parameters[key] >= 0:
                raise ValueError('All parameters must be positive')
            else:
                cls.key = new_parameters[key]

        #DeltaPhiMax must be strictly positive
        if 'DeltaPhiMax' in new_parameters:
            if not new_parameters['DeltaPhiMax'] > 0:
                raise ValueError('DeltaPhiMax must be strictly positive')
            else:
                cls.DeltaPhiMax = new_parameters['DeltaPhiMax']

        #Eta must be less than 1
        if 'eta' in new_parameters:
            if not new_parameters['eta'] >= 1:
                raise ValueError('eta must be less than 1')
            else:
                cls.eta = new_parameters['eta']

    @classmethod
    def get_parameters(cls):
        """Get parameter for the Animal.
        :return: dict
        """
        return {'w_birth': cls.w_birth, 'sigma_birth': cls.sigma_birth,
                'beta': cls.beta, 'eta': cls.eta, 'a_half': cls.a_half,
                'phi_age': cls.phi_age, 'w_half': cls.w_half,
                'phi_weight': cls.phi_weight, 'mu': cls.mu,
                'gamma': cls.gamma, 'zeta': cls.zeta, 'xi': cls.xi,
                'omega': cls.omega, 'F': cls.F, 'DeltaPhiMax': cls.DeltaPhiMax}


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
        """
        Returns a new animal if the animal procreates, None otherwise.
        Repeat given text a given number of times.

        Parameters
        ----------
        animal_in_pos : list
            Animals in the same position as the parent.

        Returns
        -------
        dict
            Dictionary with a new born animal.
        """
        self.newborn = None

        offspring_value = self.zeta * (self.w_birth + self.sigma_birth)
        if self.weight >= offspring_value:
            probility_of_procreation = min(1, self.gamma * self.fitness * animal_in_pos)
            if random.random() < probility_of_procreation:
                #'newborn log calc'
                mu = math.log(self.w_birth**2/(math.sqrt(self.w_birth**2 + self.sigma_birth**2)))
                sigma = math.sqrt(math.log(1 + (self.sigma_birth**2/self.w_birth**2)))
                newborn_weight = random.lognormvariate(mu, sigma)

                parent_loss = self.xi * newborn_weight
                if self.weight > parent_loss:
                    self.weight -= parent_loss
                    self.newborn = True
                    self.update_fitness()
                    newborn_info = {"species": self.species, "age": 0, "weight": newborn_weight}
                    return type(self)(newborn_info, self.loc)
        else:
            #'animal does not procreate'
            return None

    def calc_fitness(self):
        """Calculates the fitness of the animal."""
        if self.weight <= 0:
            return 0
        else:
            age_parameter = 1 / (1 + math.exp(
                self.phi_age * (self.age - self.a_half)))
            weight_parameter = 1 / (1 + math.exp(-self.phi_weight * (self.weight - self.w_half)))
            return age_parameter * weight_parameter

    def update_fitness(self):
        """Updates the fitness of the animal."""
        self.fitness = self.calc_fitness()

    def aging(self):
        """Animal ages by one year."""
        self.age += 1

    def loss_of_weight(self):
        """Animal loses weight by one year"""
        self.weight -= self.eta * self.weight

    def death(self):
        """Sets the animal to False if it dies, true otherwise."""
        self.update_fitness()
        probility_of_death = self.omega * (1 - self.fitness)
        if self.weight <= 0:
            self.alive = False
        elif random.random() < probility_of_death:
            self.alive = False
        else:
            # self.alive = True
            pass
    def migrate(self):
        """Returns True if the animal migrates, False otherwise."""
        probility_of_migration = self.mu * self.fitness
        if random.random() < probility_of_migration:
            return True
        else:
            return False

class Herbivore(Animal):
    w_birth = 8.0
    sigma_birth = 1.5
    beta = 0.9
    eta = 0.05
    a_half = 40.0
    phi_age = 0.6
    w_half = 10.0
    phi_weight = 0.1
    mu = 0.25
    gamma = 0.2
    zeta = 3.5
    xi = 1.2
    omega = 0.4
    F = 10.0
    DeltaPhiMax = None

    default_parameters = {'w_birth': w_birth, 'sigma_birth': sigma_birth,
                     'beta': beta, 'eta': eta, 'a_half': a_half,
                     'phi_age': phi_age, 'w_half': w_half,
                     'phi_weight': phi_weight, 'mu': mu,
                     'gamma': gamma, 'zeta': zeta, 'xi': xi,
                     'omega': omega, 'F': F, 'DeltaPhiMax': DeltaPhiMax}

    def feeding(self, fodder=300):
        """Herbivore eats the amount of fodder given, or the maximum amount of fodder it can eat."""
        if fodder < self.F:
            amount_eaten = fodder
        else:
            amount_eaten = self.F

        self.weight += (amount_eaten*self.beta)
        self.update_fitness()
        return amount_eaten

class Carnivore(Animal):
    w_birth = 6.0
    sigma_birth = 1.0
    beta = 0.75
    eta = 0.125
    a_half = 40.0
    phi_age = 0.3
    w_half = 4.0
    phi_weight = 0.4
    mu = 0.4
    gamma = 0.8
    zeta = 3.5
    xi = 1.1
    omega = 0.8
    F = 50.0
    DeltaPhiMax = 10.0
    default_parameters = {'w_birth': w_birth, 'sigma_birth': sigma_birth,
                     'beta': beta, 'eta': eta, 'a_half': a_half,
                     'phi_age': phi_age, 'w_half': w_half,
                     'phi_weight': phi_weight, 'mu': mu,
                     'gamma': gamma, 'zeta': zeta, 'xi': xi,
                     'omega': omega, 'F': F, 'DeltaPhiMax': DeltaPhiMax}

    def feeding(self, sorted_lowest_fitness_herbivore):
        """Carnivore kills the weakest herbivore until it has eaten the amount of fodder it can eat."""
        amount_eaten = 0
        for herbivore in sorted_lowest_fitness_herbivore:
            if amount_eaten >= self.F:
                break

            diff_fitness = self.fitness - herbivore.fitness
            if diff_fitness < 0:
                probility_of_killing = 0
            elif 0 < diff_fitness and diff_fitness < self.DeltaPhiMax:
                probility_of_killing = (self.fitness-herbivore.fitness)/self.DeltaPhiMax
            else:
                probility_of_killing = 1

            if random.random() < probility_of_killing:
                desiered_food = self.F - amount_eaten
                if herbivore.weight > desiered_food:
                    eating = desiered_food
                else:
                    eating = herbivore.weight

                self.weight += eating*self.beta
                herbivore.alive = False
                self.update_fitness()
                amount_eaten += eating