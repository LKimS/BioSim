from biosim.simulation import BioSim

geogr = """\
               
               WWWWWWWWWWWWWWWWWWW
               WHHHHHHHHHLLLLLLLLW
               WHHHHHLLLLLLLLLLLLW
               WHHHHHLLLDDLLLHLLLW
               WHHLLLLLDDDLLLHHHHW
               WHHHHHLLLDDLLLHHHHW
               WWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWW"""

sim = BioSim(island_map=geogr)

sim.island.plot_map()

