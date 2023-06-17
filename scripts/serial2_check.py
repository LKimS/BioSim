from biosim.simulation import BioSim


sim = BioSim().load_simulation('test.pkl')

ini_carns = [{'loc': (3, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(40)]}]
sim.add_population(population=ini_carns)
sim.simulate(100)

sim.make_movie('test.mp4')