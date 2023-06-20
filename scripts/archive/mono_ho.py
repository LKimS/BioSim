"""
Simulate herbivore population in single lowland cell for several seeds.
"""

__author__ = 'Hans Ekkehard Plesser, NMBU'


import textwrap

import numpy as np

from biosim.simulation import BioSim
import matplotlib.pyplot as plt

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

y_data = []
for seed in range(100, 203):
    sim = BioSim(geogr, ini_herbs, seed=seed, ymax_animals=300, vis_years=0)
    y = sim.pop_history['Herbivore']
    sim.simulate(301)
    y_data.append(y[100:])
    plt.plot(y)

means = []
std = []
for list in y_data:
    means.append(np.mean(list))
    std.append(np.std(list))
