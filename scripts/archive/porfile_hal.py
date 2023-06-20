from src.biosim.simulation import BioSim
from time import perf_counter

start = perf_counter()

geogr = """\
           WWWWWWWWWWWWWWWWWWWWW
           WWWWWWWWHWWWWLLLLLLLW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHHHHHWWLLLLLLWWW
           WHHHHHLLLLLLLLLLLLWWW
           WHHHHHLLLDDLLLHLLLWWW
           WHHLLLLLDDDLLLHHHHWWW
           WWHHHHLLLDDLLLHWWWWWW
           WHHHLLLLLDDLLLLLLLWWW
           WHHHHLLLLDDLLLLWWWWWW
           WWHHHHLLLLLLLLWWWWWWW
           WWWHHHHLLLLLLLWWWWWWW
           WWWWWWWWWWWWWWWWWWWWW"""

population = [{"loc": (5, 10),
               "pop": [{"species": "Herbivore", "age": 5, "weight": 20} for _ in range(150)]},
              {"loc": (5, 10),
               "pop": [{"species": "Carnivore", "age": 5, "weight": 20} for _ in range(40)]}]

sim = BioSim(island_map=geogr, ini_pop=population, seed=123456, vis_years=1, ymax_animals=12000)

sim.simulate(3)

end = perf_counter()
print(f"Time elapsed: {end - start:0.4f} seconds")
