from biosim.island import Island

import matplotlib.pyplot as plt

# Map of the island
geogr = """\
           WWW
           WLW
           WWW"""

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(2)]}]


pop_sims = []

sim = 10
for seed in range(10):

    lost = Island(geogr, seed)
    lost.add_population(ini_herbs)

    pop_animals = {}

    years = 200
    for x in range(1, lost.map_height+1):
        for y in range(1, lost.map_width+1):
            pop_animals[(x,y)] = []

    for year in range(1,years+1):
        for x in range(1, lost.map_height+1):
            for y in range(1, lost.map_width+1):
                # tile/cell work
                #print(lost.map[x][y].type)
                cell = lost.map[(x,y)]
                cell.count_animals()
                #teller dyr i cellen
                pop_animals[(x,y)].append(cell.count_herbivore)
                #newborn in cell
                cell.add_newborns(cell.herbivore)
                cell.add_newborns(cell.carnivore)
                cell.feed_animals()
                cell.update_fitness()
                #ceel.migration()
                cell.age_animals()
                cell.loss_of_weight()
                cell.animal_death()
                cell.reset_fodder()

    pop_sims.append(pop_animals[(2,2)])


for pop in pop_sims:
    plt.plot(pop)

plt.show()

