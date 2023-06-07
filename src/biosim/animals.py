import math
import random

class Animal:
    const = {}
    const["Herbivore"] = {'w_birth': 8.0,
                          'sigma_birth': 1.5,
                          'beta': 0.9,
                          'eta': 0.05,
                          'a_half': 40.0,
                          'phi_age': 0.6,
                          'w_half': 10.0,
                          'phi_weight': 0.1,
                          'mu': 0.25,
                          'gamma': 0.2,
                          'zeta': 3.5,
                          'xi': 1.2,
                          'omega': 0.4,
                          'F': 10.0,
                          'DeltaPhiMax': None}

    const["Carnivore"] = {}
    const["Landskap"] = {"Lowland": 100, "Highland": 300}


    def __init__(self, row, loc,seed=0):
        random.seed(seed)
        self.row = row
        self.loc = loc
        self.species = self.row["species"]
        self.age = self.row["age"]
        self.weight = self.row["weight"]
        self.calc_fitness()
        self.alive = True
        self.newborn = None

    def procreation(self, animal_in_pos=100):
        self.newborn = None

        offspring_value = self.const[self.species]["zeta"] * (self.const[self.species]["w_birth"] + self.const[self.species]["sigma_birth"])
        if self.weight >= offspring_value:
            probility_of_procreation = min(1, self.const[self.species]["gamma"] * self.fitness * animal_in_pos) #sannsynlighet minus dyret jeg ser på?
            if random.random() < probility_of_procreation:
                #newborn log calc
                sigma_birth = self.const[self.species]["sigma_birth"]
                omega_birth = self.const[self.species]["omega"]
                sigma_birth_log = math.log((sigma_birth)**2 / math.sqrt(sigma_birth**2 + omega_birth**2))
                omega_birth_log = math.sqrt(math.log(1 + (omega_birth**2 / sigma_birth**2)))
                newborn_weight = math.log(random.lognormvariate(sigma_birth_log, omega_birth_log))

                parent_loss = self.const[self.species]["xi"] * newborn_weight
                if self.weight > parent_loss:
                    self.weight -= parent_loss
                    self.newborn = True
                    return {"species": self.species, "age": 0, "weight": newborn_weight}
        else:
            #animal does not procreate
            return None

    def calc_fitness(self):
        if self.const["Herbivore"]["w_birth"] <= 0:
            self.fitness = 0
        if self.weight <= 0:
            self.fitness = 0
        else:
            age_parameter = 1/(1+math.exp(self.const["Herbivore"]["phi_age"]*(self.age-self.const["Herbivore"]["a_half"])))
            weight_parameter = 1/(1+math.exp(-self.const["Herbivore"]["phi_weight"]*(self.weight-self.const["Herbivore"]["w_half"])))
            self.fitness = age_parameter * weight_parameter

    def aging(self):
        self.age += 1

    def feeding(self, fodder=300):
        if fodder < self.const["Herbivore"]["F"]:
            amount_eaten = fodder
        else:
            amount_eaten = self.const["Herbivore"]["F"] #bytte ut med celltype/geografi

        self.weight += (amount_eaten*self.const["Herbivore"]["beta"])
        return amount_eaten

    def loss_of_weight(self):
        self.weight -= self.const["Herbivore"]["eta"]*self.weight

    def death(self):
        probility_of_death = self.const["Herbivore"]["omega"]*(1-self.fitness)
        if self.weight <= 0:
            print(f'status:"død", vekt ved død {self.weight}')
            self.alive = False
        elif random.random() < probility_of_death:
            self.alive = False
        else:
            #self.alive = True
            pass

def main(file):
    animals = []

#Start population
    for item in file:
        for row in item["pop"]:
            animals.append(Animal(row,item["loc"]))

#Annual cycle
    for year in range(1, 10):
        print(f'Basics År: {year} Antall dyr: {len(animals)}, Dyr[0]år: {animals[0].age}, Dyr[0]vekt: {animals[0].weight}, Dyr[0]fitness: {animals[0].fitness}, Dyr[0]status: {animals[0].alive}, Dyr[0]baby: {animals[0].newborn}')
        for animal in animals:
            animal.procreation()
            animal.feeding() #husk å sortere etter fitness før mating
            animal.calc_fitness()
            #animal.migration()
            animal.aging()
            animal.loss_of_weight()
            animal.death()

    return animals


if __name__ == "__main__":

    file = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(1)]}]

    animals = main(file)
