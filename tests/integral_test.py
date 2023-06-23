from biosim.simulation import BioSim
import pytest


@pytest.mark.parametrize("species", ["Herbivore", "Carnivore"])
def test_migration_integration(species):
    """Test migration integration test.
    This forces the animals to move each year.
    The test is checking if the animals are following the chekkerboard pattern."""
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

    sim = BioSim(island_map=geography, seed=23456,
                 cmax_animals={"Herbivore": 1, 'Carnivore': 1},
                 ymax_animals=100, vis_years=1, img_dir='pp')
    sim.set_animal_parameters(species, {'mu': 100000, 'eta': 0})  # Ensures that the animals move

    ini_pop = [{'loc': (10, 10),
                'pop': [{'species': species,
                         'age': 5,
                         'weight': 20}
                        for _ in range(1000)]}]

    sim.add_population(population=ini_pop)
    map = sim.island.habital_map

    for year in range(1, 8):
        sim.simulate(num_years=1)
        for loc, cell in map.items():
            x = loc[0]
            y = loc[1]

            # Check if the animals are following the checkerboard pattern
            if year % 2 == 0:
                if x % 2 == 0:
                    if y % 2 != 0:
                        assert cell.animals == []
                elif x % 2 != 0:
                    if y % 2 == 0:
                        assert cell.animals == []
            elif year % 2 != 0:
                if x % 2 == 0:
                    if y % 2 == 0:
                        assert cell.animals == []
                elif x % 2 != 0:
                    if y % 2 != 0:
                        assert cell.animals == []
