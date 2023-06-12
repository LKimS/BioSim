from biosim.island import Island

SIM_YEARS = 10

geogr = """\
           WWWWWWWWWWWWWWWWWWW
           WDDDDDDDDDDDDDDDDDW
           WDDDDDDDDDDDDDDDDDW
           WDDDDDDDDDDDDDDDDDW
           WDDDDDDDDDDDDDDDDDW
           WDDDDDDDDDDDDDDDDDW
           WDDDDDDDDDDDDDDDDDW
           WWWWWWWWWWWWWWWWWWW"""



ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(1)]}]
"""
ini_carn = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
"""
island = Island(geogr)
island.add_population(ini_herbs)
#island.add_population(ini_carn)

cell_pop_history = {}
island_pop_history = {'Herbivore': [], 'Carnivore': []}

for x in range(1, island.map_height + 1):
    for y in range(1, island.map_width + 1):
        cell_pop_history[(x, y)] = {'Herbivore': [], 'Carnivore': []}

habital_map = island.habital_map

for year in range(1, SIM_YEARS + 1):


    island.migrate_animals()

