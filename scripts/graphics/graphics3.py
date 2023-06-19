from biosim.graphics import Graphics
from biosim.island import Island
import matplotlib.pyplot as plt
import random
from time import time
random.seed(12345)

SIM_YEARS = 600

ini_herbs = [{'loc': (2,8),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]},
             {'loc': (2,9),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(0)]}]


geogr = """\
           WWWWWWWWWWWWWWWWWWWWW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHLLLLWWLLLLLLLWW
           WWHHLLLLLLLWWLLLLLLLW
           WWHHLLLLLLLWWLLLLLLLW
           WWWWWWWWHWWWWLLLLLLLW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHHHHHWWLLLLLLWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHHDDDDDWWLLLLLWWW
           WHHHHDDDDDDLLLLWWWWWW
           WWHHHHDDDDDDLWWWWWWWW
           WWHHHHDDDDDLLLWWWWWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHDDDDDDLLLLWWWWWW
           WWHHHHDDDDDLLLWWWWWWW
           WWWHHHHLLLLLLLWWWWWWW
           WWWHHHHHHWWWWWWWWWWWW
           WWWWWWWWWWWWWWWWWWWWW"""

island = Island(geogr)
island.add_population(ini_herbs)

graphics = Graphics()
graphics.setup(island.bitmap, SIM_YEARS, 5)

cell_pop_history = {'Herbivore': {} , 'Carnivore': {}}
island_pop_history = {'Herbivore': [], 'Carnivore': []}


habital_map = island.habital_map

for loc, cell in habital_map.items():
    cell_pop_history["Herbivore"][loc] = []
    cell_pop_history["Carnivore"][loc] = []

year = 0

while year < 50:
    start = time()
    sum_herbivore = 0
    sum_carnivore = 0

    migrating_animals = []

    # tile/cell work
    for loc, cell in habital_map.items():
        # Teller dyr i cellen
        cell.update_animal_count()
        sum_herbivore += cell.count_herbivore
        sum_carnivore += cell.count_carnivore
        cell_pop_history['Herbivore'][loc].append(cell.count_herbivore)
        cell_pop_history['Carnivore'][loc].append(cell.count_carnivore)

        cell.add_newborns(cell.herbivore)
        cell.add_newborns(cell.carnivore)
        cell.feed_animals()
        migrating_animals.extend(cell.moving_animals_list())
        cell.age_animals()
        cell.loss_of_weight()
        cell.animal_death()

    island_pop_history['Herbivore'].append(sum_herbivore)
    island_pop_history['Carnivore'].append(sum_carnivore)
    year += 1
    graphics.update(year= year,
                    herbivore_population= sum_herbivore,
                    carnivore_population= sum_carnivore,
                    herbivore_dict_map = cell_pop_history['Herbivore'],
                    carnivore_dict_map = cell_pop_history['Carnivore'])
    print(f"year: {year}, time: {time()-start}")
    island._move_all_animals(migrating_animals)


ini_carns = [{'loc': (2,8),
                'pop': [{'species': 'Carnivore',
                        'age': 5,
                        'weight': 20}
                        for _ in range(2)]}]
island.add_population(ini_carns)

while year < SIM_YEARS:
    sum_herbivore = 0
    sum_carnivore = 0

    migrating_animals = []

    # tile/cell work
    for loc, cell in habital_map.items():
        # Teller dyr i cellen
        #cell.update_animal_count()
        sum_herbivore += cell.count_herbivore
        sum_carnivore += cell.count_carnivore
        cell_pop_history['Herbivore'][loc].append(cell.count_herbivore)
        cell_pop_history['Carnivore'][loc].append(cell.count_carnivore)

        cell.add_newborns(cell.herbivore)
        cell.add_newborns(cell.carnivore)
        cell.feed_animals()
        migrating_animals.extend(cell.moving_animals_list())
        cell.age_animals()
        cell.loss_of_weight()
        cell.animal_death()

    island_pop_history['Herbivore'].append(sum_herbivore)
    island_pop_history['Carnivore'].append(sum_carnivore)
    year += 1
    graphics.update(year= year,
                    herbivore_population= sum_herbivore,
                    carnivore_population= sum_carnivore,
                    herbivore_dict_map = cell_pop_history['Herbivore'],
                    carnivore_dict_map = cell_pop_history['Carnivore'])
    print(f"year: {year}, time: {time()-start}")
    island._move_all_animals(migrating_animals)

plt.show()