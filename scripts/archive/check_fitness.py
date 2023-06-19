from biosim.animals import Herbivore, Carnivore

h1_info = {'species': 'Herbivore',
                          'age': 5,
                            'weight': .5}
location = (2, 2)
h1 = Herbivore(h1_info, location)

c1_info = {'species': 'Carnivore',
                          'age': 5,
                            'weight': .9}

c1 = Carnivore(c1_info, location)



print(h1.fitness)


h1.weight = 30
h1.age = 50
h1._update_fitness()
print(h1.fitness)

print(c1.fitness)
c1.weight = 30
c1.age = 20
c1._update_fitness()
print(c1.fitness)