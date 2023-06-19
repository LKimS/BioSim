"""
Simulate herbivore population in single lowland cell, then add carnivore population.
Repeat for several seeds.
"""


__author__ = 'Hans Ekkehard Plesser, NMBU'

import numpy as np
import matplotlib.pyplot as plt
import textwrap
from biosim.simulation import BioSim

geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]

herb_mean = []
herb_std = []
carn_mean = []
carn_std = []
herbs = []
carns = []



for seed in range(100, 150):
    sim = BioSim(geogr, ini_herbs, seed=seed, vis_years=0)
    sim.set_animal_parameters('Carnivore', {'DeltaPhiMax': 15})
    sim.simulate(50)
    sim.add_population(ini_carns)
    sim.simulate(251)
    herbs.append(sim.pop_history['Herbivore'])
    carns.append(sim.pop_history['Carnivore'])
    herb_mean.append(np.mean(sim.pop_history['Herbivore']))
    herb_std.append(np.std(sim.pop_history['Herbivore']))
    carn_mean.append(np.mean(sim.pop_history['Carnivore']))
    carn_std.append(np.std(sim.pop_history['Carnivore']))
    plt.plot(sim.pop_history['Herbivore'], "b")
    plt.plot(sim.pop_history['Carnivore'], "r")

print("mean herbivore population: ", np.mean(herb_mean))
print("std herbivore population: ", np.mean(herb_std))
print("mean carnivore population: ", np.mean(carn_mean))
print("std carnivore population: ", np.mean(carn_std))

herb_means = []
herb_stds = []
carn_means = []
carn_stds = []
for herb, carn in zip(herbs, carns):
    if carn[-1] == 0:
        continue
    herb_means.append(np.mean(herb[175:]))
    herb_stds.append(np.std(herb[175:]))
    carn_means.append(np.mean(carn[175:]))
    carn_stds.append(np.std(carn[175:]))

print("mean herbivore population: ", np.mean(herb_means))
print("std herbivore population: ", np.mean(herb_stds))
print("mean carnivore population: ", np.mean(carn_means))
print("std carnivore population: ", np.mean(carn_stds))

