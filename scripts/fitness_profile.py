from biosim.simulation import BioSim
import itertools


geogr = """\
             WWW
             WLW
             WWW"""

ini_pop = [{'loc': (2, 2),
                'pop': [{'species': 'Herbivore',
                            'age': 10,
                            'weight': 20},
                        {'species': 'Herbivore',
                            'age': 10,
                            'weight': 20},
                        {'species': 'Carnivore',
                            'age': 5,
                            'weight': 20},
                        {'species': 'Carnivore',
                            'age': 5,
                            'weight': 20}]}]



sim = BioSim(geogr, ini_pop, seed=0)
sim.simulate(0)

