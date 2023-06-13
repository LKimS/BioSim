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

    def procreation(self, animal_in_pos):
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
        if self.weight <= 0:
            return 0
        else:
            age_parameter = 1 / (1 + math.exp(
                self.phi_age * (self.age - self.a_half)))
            weight_parameter = 1 / (1 + math.exp(-self.phi_weight * (self.weight - self.w_half)))
            return age_parameter * weight_parameter

    def update_fitness(self):
        self.fitness = self.calc_fitness()

    def aging(self):
        self.age += 1

    def loss_of_weight(self):
        self.weight -= self.eta * self.weight

    def death(self):
        self.update_fitness()
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
    DeltaPhiMax = 15.0

    def feeding(self, sorted_lowest_fitness_herbivore):
        """Carnivore tries to kill the weakest herbivore first, then the next weakest and so on."""

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