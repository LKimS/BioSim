from biosim.island import Island

geogr = """\
        WWWWWWWWWWWWWWWWWWWWW
        WWWWWWWWHWWWWLLLLLLLW
        WHHHHHLLLLWWLLLWWLLLW
        WHHHHHHLLLWWLLLWWLLLW
        WHHHHHLLLLWWLLLWWLLLW
        WHHHHHHWWWWWWLLLWWWWW
        WHHHHHHWWWWWWLLLWWWWW
        WHHHHHLLLLWWLLLWWLLLW
        WHHHHHLLLLWWLLLWWLLLW
        WHHHHHLLLLWWLLLWWLLLW
        WHHHHHHWWWWWWLLLWWWWW
        WHHHHHHWWWWWWLLLWWWWW
        WHHHHHLLLLWWLLLWWLLLW
        WHHHHHLLLLWWLLLWWLLLW
        WHHHHHLLLLWWLLLWWLLLW
        WDDDDDDDDDDDDDDDDDDDW
        WWWWWWWWWWWWWWWWWWWWW"""

I = Island(geogr)
ini_herbs = [{'loc': (1, 1),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(1)]}]
ini_carns = [{'loc': (10, 10),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(1)]}]

I.add_population(ini_herbs)