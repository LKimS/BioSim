"""
Compatibility check for BioSim simulations.

This script shall function with biosim packages written for
the INF200 project June 2023.
"""

__author__ = "Hans Ekkehard Plesser, NMBU"
__email__ = "hans.ekkehard.plesser@nmbu.no"

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim

if __name__ == '__main__':

    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHLLLLLLLLLLLLWWW
               WHHHHHLLLLLLLLHLLLWWW
               WHHLLLLLLLLLLLHHHHWWW
               WWHHHHLLLLLLLLHWWWWWW
               WHHHLLLLLLLLLLLLLLWWW
               WHHHHLLLLLLLLLLWWWWWW
               WWHHHHLLLLLLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]
    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]


for seed in range(100, 103):
    sim = BioSim(geogr, ini_herbs, seed=seed,
                 img_dir='results', img_base=f'mono_hc_{seed:05d}', img_years=300)

    sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
    sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
                                            'omega': 0.3, 'F': 65,
                                            'DeltaPhiMax': 9.})
    sim.set_landscape_parameters('L', {'f_max': 700})

    sim.simulate(50)
    sim.add_population(ini_carns)
    sim.simulate(251)