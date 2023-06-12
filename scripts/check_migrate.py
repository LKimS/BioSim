from biosim.island import Island

SIM_YEARS = 1

geogr = """\
           WWW
           WLW
           WWW"""



ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
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

self.cell_pop_history = {}
self.island_pop_history = {'Herbivore': [], 'Carnivore': []}

for x in range(1, self.island.map_height + 1):
    for y in range(1, self.island.map_width + 1):
        self.cell_pop_history[(x, y)] = {'Herbivore': [], 'Carnivore': []}

habital_map = self.island.habital_map

for year in range(1, num_years + 1):
    sum_herbivore = 0
    sum_carnivore = 0

    # tile/cell work
    for loc, cell in habital_map.items():
        # Teller dyr i cellen
        cell.update_animal_count()
        sum_herbivore += cell.count_herbivore
        sum_carnivore += cell.count_carnivore
        self.cell_pop_history[loc]['Herbivore'].append(cell.count_herbivore)
        self.cell_pop_history[loc]['Carnivore'].append(cell.count_carnivore)

        cell.migrate_animals()

    self.island_pop_history['Herbivore'].append(sum_herbivore)
    self.island_pop_history['Carnivore'].append(sum_carnivore)
self.plot_population_history()