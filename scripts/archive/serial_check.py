from biosim.simulation import BioSim

ini_herbs = [{'loc': (3, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(150)]}]
ini_carns = [{'loc': (3, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(40)]}]

sim = BioSim()

sim.add_population(population=ini_herbs)
sim.simulate(100)

sim._save_simulation('test.pkl')