import math
import random


class Animal:
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

    def __init__(self, row, loc):
        self.row = row
        self.loc = loc
        self.species = self.row["species"]
        self.age = self.row["age"]
        self.weight = self.row["weight"]
        self.fitness = self.calc_fitness()
        self.alive = True
        self.newborn = None

    def procreation(self, animal_in_pos=100):
        self.newborn = None

        offspring_value = self.zeta * (self.w_birth + self.sigma_birth)
        if self.weight >= offspring_value:
            probility_of_procreation = min(1, self.gamma * self.fitness * animal_in_pos)
            if random.random() < probility_of_procreation:
                'newborn log calc'
                sigma_birth_log = math.log((self.sigma_birth)**2 / math.sqrt(self.sigma_birth**2 + self.omega**2))
                omega_birth_log = math.sqrt(math.log(1 + (self.omega**2 / self.sigma_birth**2)))
                newborn_weight = math.log(random.lognormvariate(sigma_birth_log, omega_birth_log))

                parent_loss = self.xi * newborn_weight
                if self.weight > parent_loss:
                    self.weight -= parent_loss
                    self.newborn = True
                    return {"species": self.species, "age": 0, "weight": newborn_weight}
        else:
            'animal does not procreate'
            return None

    def calc_fitness(self):
        if self.w_birth <= 0:
            return 0
        if self.weight <= 0:
            return 0
        else:
            age_parameter = 1 / (1 + math.exp(
                self.phi_age * (self.age - self.a_half)))
            weight_parameter = 1 / (1 + math.exp(-self.phi_weight * (self.weight - self.w_half)))

            return age_parameter * weight_parameter

    def aging(self):
        self.age += 1

    def loss_of_weight(self):
        self.weight -= self.eta * self.weight

    def death(self):
        probility_of_death = self.omega * (1 - self.fitness)
        if self.weight <= 0:
            self.alive = False
        elif random.random() < probility_of_death:
            self.alive = False
        else:
            # self.alive = True
            pass


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

    def feeding(self, fodder=300):
        if fodder < self.F:
            amount_eaten = fodder
        else:
            amount_eaten = self.F

        self.weight += (amount_eaten*self.beta)
        return amount_eaten
    pass

class Carnivore(Animal):
    w_birth = None
    pass