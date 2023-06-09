from biosim.island import Island
map = """\
WHW
LHL
WDL
HWW"""

island = Island(map)
pop = [{'loc': (1, 1),
        'pop': [{'species': 'Herbivore',
                 'age': 5,
                 'weight': 20}
                for _ in range(150)]},

       {'loc': (2, 2),
        'pop': [{'species': 'Carnivore',
                 'age': 5,
                 'weight': 20}
                for _ in range(150)]},

       ]

island.add_population(pop)
island.plot_map()
# bitmap = A.bitmap

print(repr(island.map))
print(island.map[1][1])


