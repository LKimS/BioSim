import pytest
from biosim.simulation import BioSim
from biosim.island import Island
from biosim.animals import Herbivore, Carnivore
from biosim.cell import Lowland, Highland

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
    sim.simulate(0)  # the program updated it's data only when simulate is called
    count = {'Herbivore': 200, 'Carnivore': 50}
    assert sim.num_animals_per_species == count


@pytest.mark.parametrize("num_years", [1, 10, 100])
def test_year_counter(num_years):
    """
    Test that the year counter is updated correctly
    """
    sim = BioSim(geogr, vis_years=0)
    sim.simulate(num_years)  # the program updated its data only when simulate is called

    assert sim.year == num_years


def test_population_count():
    """
    Test that the population is counted correctly
    """
    sim = BioSim(geogr, ini_herbs + ini_carns, vis_years=0)
    sim.simulate(0)  # the program updated its data only when simulate is called
    assert sim.num_animals == 250


# test inspired by "test_biosim.interface.py"

@pytest.mark.parametrize('bad_boundary',
                         ['L', 'H', 'D'])
def test_bad_boundary(bad_boundary):
    """Non-ocean boundary must raise error"""
    with pytest.raises(ValueError):
        BioSim(island_map=f"{bad_boundary}WW\nWLW\nWWW", vis_years=0)


@pytest.mark.parametrize('bad_boundary',
                         ['L', 'H', 'D'])
def test_bad_boundary2(bad_boundary):
    """Non-ocean boundary must raise error"""
    with pytest.raises(ValueError):
        BioSim(island_map=f"W{bad_boundary}W\nWLW\nWWW", vis_years=0)


@pytest.mark.parametrize('bad_boundary',
                         ['L', 'H', 'D'])
def test_bad_boundary3(bad_boundary):
    """Non-ocean boundary must raise error"""
    with pytest.raises(ValueError):
        BioSim(island_map=f"WWW\nWLW\nW{bad_boundary}W", vis_years=0)


def test_bad_landscape():
    """Invalid landscape type must raise error"""
    with pytest.raises(ValueError):
        BioSim(island_map="WWW\nWMW\nWWW", vis_years=0)


def test_inconsistent_length():
    """Inconsistent line length must raise error"""
    with pytest.raises(ValueError):
        BioSim(island_map="WWWW\nWLW\nWWW", vis_years=0)


@pytest.fixture
def reset_animal_defaults():
    """Reset animal default parameters"""

    yield
    BioSim().set_animal_parameters('Herbivore',
                                   {'w_birth': 8.,
                                    'sigma_birth': 1.5,
                                    'beta': 0.9,
                                    'eta': 0.05,
                                    'a_half': 40.,
                                    'phi_age': 0.6,
                                    'w_half': 10.,
                                    'phi_weight': 0.1,
                                    'mu': 0.25,
                                    'gamma': 0.2,
                                    'zeta': 3.5,
                                    'xi': 1.2,
                                    'omega': 0.4,
                                    'F': 10.}
                                   )
    # noinspection DuplicatedCode
    BioSim().set_animal_parameters('Carnivore',
                                   {'w_birth': 6.,
                                    'sigma_birth': 1.0,
                                    'beta': 0.75,
                                    'eta': 0.125,
                                    'a_half': 40.,
                                    'phi_age': 0.3,
                                    'w_half': 4.,
                                    'phi_weight': 0.4,
                                    'mu': 0.4,
                                    'gamma': 0.8,
                                    'zeta': 3.5,
                                    'xi': 1.1,
                                    'omega': 0.8,
                                    'F': 50.,
                                    'DeltaPhiMax': 10.})


@pytest.mark.parametrize("species, change_params", [('Herbivore', {'w_birth': 10, 'w_half': 5}),
                                                    ('Carnivore', {'w_birth': 10, 'w_half': 5})])
def test_set_animal_parameters(reset_animal_defaults, species, change_params):
    """Test that set_animal_parameters works correctly"""
    BioSim().set_animal_parameters(species, change_params)

    if species == 'Herbivore':
        new_params = {key: Herbivore.params[key] for key in change_params.keys()}
    else:
        new_params = {key: Carnivore.params[key] for key in change_params.keys()}

    assert new_params == change_params


@pytest.mark.parametrize("species, change_params", [('Herbivore', {'w_birth': -10}),
                                                    ('Carnivore', {'w_birth': -10})])
def test_set_animal_parameters_error(reset_animal_defaults, species, change_params):
    """Test that set_animal_parameters raises error for invalid species"""
    with pytest.raises(ValueError):
        BioSim().set_animal_parameters(species, change_params)


@pytest.fixture
def reset_landscape_defaults():
    """Reset landscape default parameters"""
    yield
    BioSim(island_map="W",
           ini_pop=[], seed=1, vis_years=0).set_landscape_parameters('L', {'f_max': 800.0})
    BioSim(island_map="W",
           ini_pop=[], seed=1, vis_years=0).set_landscape_parameters('H', {'f_max': 300.0})


@pytest.mark.parametrize('cell_letter, params',
                         [('L', {'f_max': 100.}),
                          ('H', {'f_max': 200.})])
def test_set_param_landscape(reset_landscape_defaults, cell_letter, params):
    """Parameters can be set on landscape classes"""

    BioSim().set_landscape_parameters(cell_letter, params)

    cell = {'L': Lowland, 'H': Highland}

    assert cell[cell_letter].f_max == params['f_max']


@pytest.mark.parametrize('cell_letter, params',
                         [('L', {'f_max': -100.}),
                          ('H', {'f_max': -200.})])
def test_set_param_landscape_error(reset_landscape_defaults, cell_letter, params):
    """Parameters can be set on landscape classes"""
    with pytest.raises(ValueError):
        BioSim().set_landscape_parameters(cell_letter, params)


@pytest.mark.parametrize('cell_letter', ("D", "R"))
def test_set_param_invalid_cell(reset_landscape_defaults, cell_letter):
    """Parameters can be set on landscape classes"""
    with pytest.raises(ValueError):
        BioSim().set_landscape_parameters(cell_letter, {'f_max': 100})


def test_yearly_cycle(mocker):
    """
    Test yearly cycle by choosing some methods in animal class and counting them manually.
    Then comparing them to how many times the program calls the methods.
    """
    # Keep count of methods called
    mocker.spy(Herbivore, 'calc_fitness')
    mocker.spy(Herbivore, 'procreation')
    mocker.spy(Herbivore, 'feeding')
    mocker.spy(Herbivore, 'migrate')
    mocker.spy(Herbivore, 'aging')
    mocker.spy(Herbivore, 'loss_of_weight')
    mocker.spy(Herbivore, 'death')

    mocker.spy(Carnivore, 'calc_fitness')
    mocker.spy(Carnivore, 'procreation')
    mocker.spy(Carnivore, 'feeding')
    mocker.spy(Carnivore, 'migrate')
    mocker.spy(Carnivore, 'aging')
    mocker.spy(Carnivore, 'loss_of_weight')
    mocker.spy(Carnivore, 'death')

    geogr = """\
                WWWWW
                WLWHW
                WWWWW"""
    sim = BioSim(island_map=geogr, vis_years=0)

    # Adding 1 herbivore
    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}]}]
    sim.add_population(ini_herbs)
    sim.simulate(1)

    # adding 1 carnivore
    ini_carns = [{'loc': (2, 4),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}]}]
    sim.add_population(ini_carns)

    sim.simulate(1)

    result = {"h_calc_fit": Herbivore.calc_fitness.call_count,
              "h_procreation": Herbivore.procreation.call_count,
              "h_feeding": Herbivore.feeding.call_count,
              "h_migrate": Herbivore.migrate.call_count,
              "h_aging": Herbivore.aging.call_count,
              "h_loss_of_weight": Herbivore.loss_of_weight.call_count,
              "h_death": Herbivore.death.call_count,
              "c_calc_fit": Carnivore.calc_fitness.call_count,
              "c_procreation": Carnivore.procreation.call_count,
              "c_feeding": Carnivore.feeding.call_count,
              "c_migrate": Carnivore.migrate.call_count,
              "c_aging": Carnivore.aging.call_count,
              "c_loss_of_weight": Carnivore.loss_of_weight.call_count,
              "c_death": Carnivore.death.call_count}

    # Manually counted method calls:
    expect = {"h_calc_fit": 5,
              "h_procreation": 2,
              "h_feeding": 2,
              "h_migrate": 2,
              "h_aging": 2,
              "h_loss_of_weight": 2,
              "h_death": 2,
              "c_calc_fit": 2,
              "c_procreation": 1,
              "c_feeding": 0,
              "c_migrate": 1,
              "c_aging": 1,
              "c_loss_of_weight": 1,
              "c_death": 1}

    assert result == expect
