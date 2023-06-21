from biosim.simulation import BioSim
import pytest
import matplotlib.pyplot as plt



"""Test migration integration test."""
geography = """\
                WWWWWWWWWWWWWWWWWWW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHLHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WHHHHHHHHHHHHHHHHHW
                WWWWWWWWWWWWWWWWWWW
                """

sim = BioSim(island_map=geography, seed=23456, cmax_animals={"Herbivore": 1})
sim.set_animal_parameters('Herbivore', {'mu': 1, 'eta': 0})

ini_pop = [{'loc': (10, 10),
            'pop': [{'species': 'Herbivore',
                     'age': 5,
                     'weight': 20}
                    for _ in range(100)]}]

sim.add_population(population=ini_pop)

for _ in range(1):
    sim.simulate(num_years=3)


#sim.simulate(num_years=9)

sim.island.plot_map()
#plt.show()



