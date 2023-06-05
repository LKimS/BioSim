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
    const["Landskap"] = {"Lowland": 800, "Highland": 300}


    def __init__(self, row, loc,seed=0):
        random.seed(seed)
        self.row = row
        self.loc = loc
        self.species = self.row["species"]
        self.age = self.row["age"]
        self.weight = self.row["weight"]
        self.calc_fitness()
        self.alive = True
        self.baby = None

    def procreation(self):
        baby ={}

        self.baby = baby
        return baby

    def calc_fitness(self):
        if self.const["Herbivore"]["w_birth"] < 0:
            self.fitness = 0
        else:
            self.fitness = 1/(1+math.exp(self.const["Herbivore"]["phi_age"]*(self.age-self.const["Herbivore"]["a_half"]))) * 1/(1+math.exp(-self.const["Herbivore"]["phi_weight"]*(self.weight-self.const["Herbivore"]["w_half"])))

    def aging(self):
        self.age += 1

    def feeding(self):
        self.weight += self.const["Herbivore"]["beta"]*self.const["Landskap"]["Lowland"]

    def loss_of_weight(self):
        self.weight -= self.const["Herbivore"]["eta"]*self.weight

    def death(self):
        probility_of_death = self.const["Herbivore"]["omega"]*(1-self.fitness)
        if self.weight <= 0:
            print(f'status:"død", vekt ved død {self.weight}')
            self.alive = False
        elif random.random() <= probility_of_death:
            #print((f'Status:"død", Random(1-0): {random.random()}, Probility of death: {probility_of_death}'))
            self.alive = False
        else:
            #print((f'Status:"levende", Random(1-0): {random.random()}, Probility of death: {probility_of_death}'))
            #self.alive = True
            pass

def main(file):
    animals = []

#Start population
    for item in file:
        for row in item["pop"]:
            animals.append(Animal(row,item["loc"]))

#Annual cycle
    for year in range(1, 11):
        print(f'År: {year} Antall dyr: {len(animals)} Dyr[0]alder: {animals[0].age} Dyr[0]vekt: {animals[0].weight}, Dyr[0]fitness: {animals[0].fitness} ')
        for animal in animals:

            #animal.procreation()
            animal.feeding() #husk å sortere etter fitness før mating
            animal.calc_fitness()
            #animal.migration()
            animal.aging()
            animal.loss_of_weight()
            animal.death()


    #procreation
    #feeding
    #migration
    #aging
    #loss of weight
    #death


    return animals


if __name__ == "__main__":

    file = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(20)]}]

    animals = main(file)

#tilfeldig tall mellom 0 og 1



    '''
        
    
        def migration(self):
            pass

        def birth(self, N, w_birth, sigma_birth, gamma):
            if self.weight >= w_birth+sigma_birth:
                probility = min(1, gamma * self.fitness*N)
                #newborn
                #add to population
                #update weight
                pass
            pass

        def death(self):
            if self.weight <= 0:
                #remove from population
                pass
            else:
                #remove from population with probability
                pass
    '''