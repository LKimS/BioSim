import pytest
from biosim.simulation import BioSim
from biosim.island import Island

geogr = """\
           WWWWWWWWWWWWWWWWWWWWW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHLLLLWWLLLLLLLWW
           WWHHLLLLLLLWWLLLLLLLW
           WWHHLLLLLLLWWLLLLLLLW
           WWWWWWWWHWWWWLLLLLLLW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHHHHHWWLLLLLLWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHHDDDDDWWLLLLLWWW
           WHHHHDDDDDDLLLLWWWWWW
           WWHHHHDDDDDDLWWWWWWWW
           WWHHHHDDDDDLLLWWWWWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHDDDDDDLLLLWWWWWW
           WWHHHHDDDDDLLLWWWWWWW
           WWWHHHHLLLLLLLWWWWWWW
           WWWHHHHHHWWWWWWWWWWWW
           WWWWWWWWWWWWWWWWWWWWW"""

ini_herbs = [{'loc': (2, 7),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(200)]}]
ini_carns = [{'loc': (2, 7),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

sim = BioSim(geogr, ini_herbs + ini_carns, seed=1,
             hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                         'age': {'max': 60.0, 'delta': 2},
                         'weight': {'max': 60, 'delta': 2}},
             cmax_animals={'Herbivore': 200, 'Carnivore': 50},
             img_dir='results',
             img_base='sample')


def test_create_object():
    """
    Test that the object is created
    """
    sim = BioSim()

def test_map():
    """
    Test that the map is created correctly
    """

    sim = BioSim(geogr)

    assert sim.island.map_processed == Island(geogr).map_processed

def test_add_population():
    """
    Test that the population is added correctly
    """
    sim = BioSim(geogr, ini_herbs + ini_carns)
    assert sim.is == len(ini_herbs + ini_carns)