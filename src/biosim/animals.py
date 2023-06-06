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
        self.baby = None
        self.baby1 = None

    def procreation(self):
        '''Krav til procreation:
        - vekten er tung nok
        - større sannsynling het med samme art i samme posisjon
        - Kun et barn per år
        - Moren mister vekt etter fødsel
        - Mister moren mer vekt enn hun veier, blir det ikke født noen barn
        '''
        self.baby1 = False
        if self.weight >= self.const[self.species]["zeta"]*(self.const[self.species]["w_birth"]+self.const[self.species]["sigma_birth"]):
            animal_in_pos = 1 #hvor mange dyr som er i samme posisjon
            babyweight = 5 #antatt vekt på baby
            probility_of_procreation = min(1, self.const[self.species]["gamma"]*self.fitness*(animal_in_pos)) #sannsynlighet minus dyret jeg ser på?
            #print(f'probility_of_procreation: {probility_of_procreation}')
            if random.random() < probility_of_procreation:
                #print("baby")
                self.weight -= self.const[self.species]["xi"]*babyweight
                if not self.weight <= 0:
                    self.baby = {"species": self.species, "age": 0, "weight": babyweight}
                    self.baby1 = True
        else:
            #animal does not procreate
            pass

        #self.baby = baby
        #return baby

    def calc_fitness(self):
        if self.const["Herbivore"]["w_birth"] < 0:
            self.fitness = 0
        else:
            self.fitness = 1/(1+math.exp(self.const["Herbivore"]["phi_age"]*(self.age-self.const["Herbivore"]["a_half"]))) * 1/(1+math.exp(-self.const["Herbivore"]["phi_weight"]*(self.weight-self.const["Herbivore"]["w_half"])))

    def aging(self):
        self.age += 1

    def feeding(self):
        self.weight += self.const["Herbivore"]["beta"]*self.const["Landskap"]["Lowland"] #bytte ut med celltype/geografi

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
    for year in range(1, 20):
        print(f'Basics År: {year} Antall dyr: {len(animals)}, Dyr[0]år: {animals[0].age}, Dyr[0]vekt: {animals[0].weight}, Dyr[0]fitness: {animals[0].fitness}, Dyr[0]status: {animals[0].alive}, Dyr[0]baby1: {animals[0].baby1}')
        for animal in animals:
            animal.procreation()
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
                          for _ in range(1)]}]

    animals = main(file)
