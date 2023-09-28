from biosim.simulation import BioSim


















ini_herbs = [{'loc': (1, 1),
                  'pop': [{'species': 'Herbivore',
                           'age': 5.5,
                           'weight': 20}]}]

sim = BioSim("W", ini_pop=ini_herbs, vis_years=0)