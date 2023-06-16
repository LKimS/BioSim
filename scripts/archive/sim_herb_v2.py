from biosim.simulation import BioSim

geogr = """\
           WWW
           WLW
           WWW"""



ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

sim = BioSim(geogr, ini_herbs, seed=0)
sim.simulate(100)
sim.simulate(50)

