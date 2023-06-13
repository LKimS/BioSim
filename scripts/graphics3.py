from biosim.graphics import Graphics
from biosim.island import Island

SIM_YEARS = 300

ini_herbs = [{'loc': (2,2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(2)]}]

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
graphics.setup(SIM_YEARS, 1)

cell_pop_history = {}
island_pop_history = {'Herbivore': [], 'Carnivore': []}

for x in range(1, island.map_height + 1):
    for y in range(1, island.map_width + 1):
        cell_pop_history[(x, y)] = {'Herbivore': [], 'Carnivore': []}

habital_map = island.habital_map

year = 0

while year < SIM_YEARS:
    sum_herbivore = 0
    sum_carnivore = 0

    # tile/cell work
    for loc, cell in habital_map.items():
        # Teller dyr i cellen
        cell.update_animal_count()
        sum_herbivore += cell.count_herbivore
        sum_carnivore += cell.count_carnivore
        cell_pop_history[loc]['Herbivore'].append(cell.count_herbivore)
        cell_pop_history[loc]['Carnivore'].append(cell.count_carnivore)

        # pop_animals[(x, y)].append(cell.count_carnivore)
        # newborn in cell
        cell.add_newborns(cell.herbivore)
        cell.add_newborns(cell.carnivore)
        cell.feed_animals()
        #cell.migration()
        cell.age_animals()
        cell.loss_of_weight()
        cell.animal_death()

    island_pop_history['Herbivore'].append(sum_herbivore)
    island_pop_history['Carnivore'].append(sum_carnivore)
    year += 1
    graphics.update(year, sum_herbivore)
    print(year)



