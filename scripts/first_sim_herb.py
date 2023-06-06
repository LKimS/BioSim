from biosim.island import Island

import matplotlib.pyplot as plt

geogr = """\
           WWW
           WLW
           WWW"""

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(10)]}]

lost = Island(geogr)
lost.add_population(ini_herbs)

pop_animals = {}

N = 10
for x in range(1, lost.map_height+1):
    for y in range(1, lost.map_width+1):
        pop_animals[(x,y)] = []

for year in range(1,N+1):
    for x in range(1, lost.map_height+1):
        for y in range(1, lost.map_width+1):
            # tile/cell work
            #print(lost.map[x][y].type)
            cell = lost.map[x][y]
            cell.count_animals()
            #teller dyr i cellen
            pop_animals[(x,y)].append(cell.count_herbivores())
            #newborn in cell
            newborn_herbivores = cell.get_newborns(cell.herbivores)
            newborn_carnivores = cell.get_newborns(cell.carnivores)
            lost.add_population(newborn_carnivores)
            lost.add_population(newborn_herbivores)
            cell.feed_animals()
            #ceel.migration()
            cell.age_animals()
            cell.loss_of_weight()
            cell.animal_death()


plt.plot(pop_animals[(2,2)])
plt.show()