import pytest
from pytest import approx
import random
import math
import scipy.stats as stats

from biosim.animals import Herbivore, Carnivore


def std_herb():
    herb = Herbivore({"species": "Herbivore", "age": 40, "weight": 60}, (1, 2))
    return herb


def std_carn():
    carn = Carnivore({"species": "Carnivore", "age": 40, "weight": 60}, (1, 2))
    return carn


@pytest.fixture
def reset_default_params():
    """Resets the default parameters to their original values"""
    yield
    Herbivore.set_parameters({'w_birth': 8.0,
                              'sigma_birth': 1.5,
                              'beta': 0.9,
                              'eta': 0.05,
                              'a_half': 40.0,
                              'phi_age': 0.6,
                              'w_half': 10.0,
                              'phi_weight': 0.1,
                              'mu': 0.25,
                              'gamma': 0.2,
                              'zeta': 3.5,
                              'xi': 1.2,
                              'omega': 0.4,
                              'F': 10.0})

    Carnivore.set_parameters({'w_birth': 6.0,
                              'sigma_birth': 1.0,
                              'beta': 0.75,
                              'eta': 0.125,
                              'a_half': 40.0,
                              'phi_age': 0.3,
                              'w_half': 4.0,
                              'phi_weight': 0.4,
                              'mu': 0.4,
                              'gamma': 0.8,
                              'zeta': 3.5,
                              'xi': 1.1,
                              'omega': 0.8,
                              'F': 50.0,
                              'DeltaPhiMax': 10.0})


@pytest.mark.parametrize("species, change", [("Herbivore", {"w_birth": 10,
                                                            "sigma_birth": 2,
                                                            "beta": 0.8,
                                                            "eta": 0.1,
                                                            "a_half": 30,
                                                            "phi_age": 0.5,
                                                            "w_half": 15,
                                                            "phi_weight": 0.2,
                                                            "mu": 0.2,
                                                            "gamma": 0.4,
                                                            "zeta": 4,
                                                            "xi": 1.3,
                                                            "omega": 0.5,
                                                            "F": 15}),
                                             ("Carnivore", {"w_birth": 5,
                                                            "sigma_birth": 1,
                                                            "beta": 0.5,
                                                            "eta": 0.05,
                                                            "a_half": 20,
                                                            "phi_age": 0.2,
                                                            "w_half": 5,
                                                            "phi_weight": 0.3,
                                                            "mu": 0.3,
                                                            "gamma": 0.6,
                                                            "zeta": 3,
                                                            "xi": 1.2,
                                                            "omega": 0.7,
                                                            "F": 30,
                                                            "DeltaPhiMax": 5})])
def test_set_parameters(reset_default_params, species, change):
    """Test that parameters are set correctly"""
    if species == "Herbivore":
        Herbivore.set_parameters(change)
        assert Herbivore.get_parameters() == approx(change)

    elif species == "Carnivore":
        Carnivore.set_parameters(change)
        assert Carnivore.get_parameters() == approx(change)


@pytest.mark.parametrize("species, change", [("Herbivore", {"w_birth": - 1}),
                                             ("Herbivore", {"w_birth": "a"}),
                                             ("Herbivore", {"sigma_birth": - 1}),
                                             ("Herbivore", {"beta": - 1}),
                                             ("Herbivore", {"eta": - 1}),
                                             ("Herbivore", {"eta": 2}),
                                             ("Herbivore", {"a_half": - 1}),
                                             ("Herbivore", {"phi_age": - 1}),
                                             ("Herbivore", {"w_half": - 1}),
                                             ("Herbivore", {"phi_weight": - 1}),
                                             ("Herbivore", {"mu": - 1}),
                                             ("Herbivore", {"gamma": - 1}),
                                             ("Herbivore", {"zeta": - 1}),
                                             ("Herbivore", {"xi": - 1}),
                                             ("Herbivore", {"omega": - 1}),
                                             ("Herbivore", {"F": - 1}),
                                             ("Carnivore", {"w_birth": - 1}),
                                             ("Carnivore", {"w_birth": "a"}),
                                             ("Carnivore", {"sigma_birth": - 1}),
                                             ("Carnivore", {"beta": - 1}),
                                             ("Carnivore", {"eta": - 1}),
                                             ("Carnivore", {"eta": 2}),
                                             ("Carnivore", {"a_half": - 1}),
                                             ("Carnivore", {"phi_age": - 1}),
                                             ("Carnivore", {"w_half": - 1}),
                                             ("Carnivore", {"phi_weight": - 1}),
                                             ("Carnivore", {"mu": - 1}),
                                             ("Carnivore", {"gamma": - 1}),
                                             ("Carnivore", {"zeta": - 1}),
                                             ("Carnivore", {"xi": - 1}),
                                             ("Carnivore", {"omega": - 1}),
                                             ("Carnivore", {"F": - 1}),
                                             ("Carnivore", {"DeltaPhiMax": - 1}),
                                             ("Carnivore", {"DeltaPhiMax": 0}),
                                             ("Carnivore", {"DeltaPhiMa": "a"})])
def test_bad_params(reset_default_params, species, change):
    """Test that bad parameters raise ValueError"""
    with pytest.raises(ValueError):
        if species == "Herbivore":
            Herbivore.set_parameters(change)
        elif species == "Carnivore":
            Carnivore.set_parameters(change)


@pytest.mark.parametrize("loc, species, age, weight, new_params",
                         [[(1, 2), "Herbivore", 5, 20, {"phi_age": 0.6, "phi_weight": 0.1, "a_half": 40, "w_half": 10}],
                          [(2, 1), "Herbivore", 0, 1, {"phi_age": 0.1, "phi_weight": 0.6, "a_half": 20, "w_half": 15}],
                          [(10, 3), "Herbivore", 150, 2000,
                           {"phi_age": 0.1, "phi_weight": 0.6, "a_half": 20, "w_half": 15}],
                          [(1, 2), "Carnivore", 5, 20, {"phi_age": 0.3, "phi_weight": 0.4, "a_half": 60, "w_half": 20}],
                          [(2, 1), "Carnivore", 0, 1, {"phi_age": 0.4, "phi_weight": 0.3, "a_half": 30, "w_half": 10}]])
def test_init(reset_default_params, loc, species, age, weight, new_params):
    """Test that animal is created with correct attributes"""
    stat = {'species': species,
            'age': age,
            'weight': weight}

    if species == "Herbivore":
        Herbivore.set_parameters(new_params)
        animal = Herbivore(stat, loc)
    elif species == "Carnivore":
        Carnivore.set_parameters(new_params)
        animal = Carnivore(stat, loc)

    result = {'loc': animal.loc,
              'species': animal.species,
              'age': animal.age,
              'weight': animal.weight,
              "fitness": animal.fitness,
              "alive": animal.alive,
              "newborn": animal.newborn
              }

    fitness_age_param = 1 / (1 + math.exp(new_params["phi_age"] * (age - new_params["a_half"])))
    fitness_weight_param = 1 / (1 + math.exp(-new_params["phi_weight"] * (weight - new_params["w_half"])))

    fitness = fitness_age_param * fitness_weight_param

    expected = {'loc': loc,
                'species': species,
                'age': age,
                'weight': weight,
                "fitness": fitness,
                "alive": True,
                "newborn": None
                }
    assert result == approx(expected)


@pytest.mark.parametrize("animal", [(Herbivore({"species": "Herbivore", "age": 0, "weight": 1000}, (1, 2))),
                                    (Carnivore({"species": "Carnivore", "age": 0, "weight": 1000}, (1, 2)))])
# Set high weight and low age to get high probability of procreation
def test_procreation_age(animal):
    """Test that procreation works"""
    baby = animal.procreation(10)
    assert baby.age == 0 and type(baby) == type(animal)


@pytest.mark.parametrize("animal", [std_herb(), std_carn()])
def test_procreation_prob(animal):
    num_trials = 10000
    animal_in_cell = 2
    probability_of_procreation = min(1, animal.params["gamma"] * animal.fitness * animal_in_cell)

    num_babies = 0
    for i in range(num_trials):
        baby = animal.procreation(animal_in_cell)
        animal.weight = 60
        if baby is not None:
            num_babies += 1

    assert stats.binom_test(num_babies, num_trials, probability_of_procreation) > .01


@pytest.mark.parametrize("animal", [(Herbivore({"species": "Herbivore", "age": 0, "weight": 1000}, (1, 2))),
                                    (Carnivore({"species": "Carnivore", "age": 0, "weight": 1000}, (1, 2)))])
def test_procreation_weight(animal):
    # TODO
    """This test executes procreation N times and checks that the weight of the baby is within the expected range.
        The distribution of the weight will follow the log normal distribution, and at high N will be approximated by
        the normal distribution. The test checks that the mean of the distribution is within the expected range.
    """
    pass


@pytest.mark.parametrize("species, age_change, weight", [["Herbivore", 5, 20],
                                                         ["Herbivore", 0, 1],
                                                         ["Herbivore", 150, 2000],
                                                         ["Carnivore", 5, 20],
                                                         ["Carnivore", 0, 1],
                                                         ["Carnivore", 150, 2000]])
def test_calc_fitness(species, age_change, weight):
    """Test that fitness is calculated correctly"""
    stat = {'species': species,
            'age': 5,
            'weight': weight}

    if species == "Herbivore":
        animal = Herbivore(stat, (1, 2))
    elif species == "Carnivore":
        animal = Carnivore(stat, (1, 2))

    animal.age = age_change

    fitness_age_param = 1 / (1 + math.exp(animal.params["phi_age"] * (age_change - animal.params["a_half"])))
    fitness_weight_param = 1 / (1 + math.exp(-animal.params["phi_weight"] * (weight - animal.params["w_half"])))

    fitness = fitness_age_param * fitness_weight_param
    assert animal._calc_fitness() == approx(fitness)


def test_update_fitness():
    """Test that fitness is updated correctly"""
    stat = {'species': "Herbivore",
            'age': 5,
            'weight': 20}
    animal = Herbivore(stat, (1, 2))
    # change age and weight
    animal.age = 10
    animal.weight = 10
    animal._update_fitness()
    assert animal.fitness == approx(animal._calc_fitness())


@pytest.mark.parametrize("species, age", [("Herbivore", 5),
                                          ("Herbivore", 1),
                                          ("Herbivore", 150),
                                          ("Carnivore", 5),
                                          ("Carnivore", 1),
                                          ("Carnivore", 150)])
def test_aging(species, age):
    """Test that aging works correctly"""
    stat = {'species': species,
            'age': age,
            'weight': 20}
    if species == "Herbivore":
        animal = Herbivore(stat, (1, 2))
    elif species == "Carnivore":
        animal = Carnivore(stat, (1, 2))

    animal.aging()
    assert animal.age == age + 1


@pytest.mark.parametrize("species, weight", [("Herbivore", 20),
                                             ("Herbivore", 1),
                                             ("Herbivore", 150),
                                             ("Carnivore", 20),
                                             ("Carnivore", 1),
                                             ("Carnivore", 150)])
def test_weight_loss(species, weight):
    """Test that weight loss works correctly"""
    stat = {'species': species,
            'age': 5,
            'weight': weight}
    if species == "Herbivore":
        animal = Herbivore(stat, (1, 2))
    elif species == "Carnivore":
        animal = Carnivore(stat, (1, 2))

    animal.loss_of_weight()
    assert animal.weight == approx(weight - animal.params["eta"] * weight)


@pytest.mark.parametrize("animal", [std_herb(), std_carn()])
def test_death(animal):
    """Test the statistical probability of death"""
    num_trial = 10000
    deaths = 0

    prob_of_death = animal.params["omega"] * (1 - animal.fitness)

    for i in range(num_trial):
        animal.death()
        if not animal.alive:
            deaths += 1
            animal.alive = True

    assert stats.binom_test(deaths, num_trial, prob_of_death) > .01


def test_death_weight():
    """Test that animals dies if their weight is 0"""
    animal = std_herb()

    animal.weight = 0
    animal.death()

    assert animal.alive == False


@pytest.mark.parametrize("animal", [std_herb(), std_carn()])
def test_migrate(animal):
    """Test that migration works correctly"""

    num_trial = 10000
    num_migrate = 0

    prob_migrate = animal.params["mu"] * animal.fitness

    for i in range(num_trial):
        if animal.migrate():
            num_migrate += 1

    assert stats.binom_test(num_migrate, num_trial, prob_migrate) > .01


@pytest.mark.parametrize("animal, fodder", [(std_herb(), 0),
                                            (std_herb(), 100),
                                            (std_herb(), 2),
                                            (std_herb(), 11)])
def test_feeding_herb(animal, fodder):
    """Test that feeding works correctly"""

    amount_eaten = animal.feeding(fodder)

    if fodder < animal.params["F"]:
        assert amount_eaten == fodder
    else:
        assert amount_eaten == animal.params["F"]


@pytest.mark.parametrize("animal, fodder", [(std_herb(), 0),
                                            (std_herb(), 100),
                                            (std_herb(), 2),
                                            (std_herb(), 11)])
def test_feeding_herb_weight(animal, fodder):
    """Test that feeding increases weight correctly"""
    old_weight = animal.weight
    amount_eaten = animal.feeding(fodder)

    if fodder < animal.params["F"]:
        assert animal.weight == approx(animal.params["beta"] * fodder + old_weight)
    else:
        assert animal.weight == approx(animal.params["beta"] * animal.params["F"] + old_weight)


def test_herb_death_eaten(reset_default_params):
    """Test that herbivore dies if eaten"""
    herb = std_herb()
    carn = std_carn()

    herb.fitness = 0.001
    carn.fitness = 1

    Carnivore.set_parameters({"DeltaPhiMax": 1})  # guaranties that carn eats herb

    carn.feeding([herb])

    assert not herb.alive


@pytest.mark.parametrize("herb_weight", [1, 10, 15, 25, 40, 50, 60])
def test_herb_death_eaten(reset_default_params, herb_weight):
    """Test that carnivore gains the right amount of weight when eating"""

    herb_stat = {'species': "Herbivore",
                 'age': 5,
                 'weight': herb_weight}
    herb = Herbivore(herb_stat, (1, 2))

    carn = std_carn()

    old_weight = carn.weight

    herb.fitness = 0.001
    carn.fitness = 1

    Carnivore.set_parameters({"DeltaPhiMax": 1})  # guaranties that carn eats herb

    carn.feeding([herb])

    assert carn.weight == approx(min(herb.weight, carn.params["F"]) * carn.params["beta"] + old_weight)


def test_carn_eat_full(reset_default_params):
    """Test that carnivore stops after eaten enough"""

    herb_weight = 7

    herb_stat = {'species': "Herbivore",
                 'age': 1000,
                 'weight': herb_weight}

    herb_list = [Herbivore(herb_stat, (1, 2)) for _ in range(60)]
    carn = std_carn()

    carn.weight = carn.params["F"]
    carn.fitness = 1

    Carnivore.set_parameters({"DeltaPhiMax": .1})  # guaranties that carn eats herb

    carn.feeding(herb_list)

    herb_alive = [herb for herb in herb_list if herb.alive]

    num_alive = len(herb_list) - math.ceil(carn.params["F"] / herb_weight)

    assert len(herb_alive) == num_alive


def test_carn_eat_prob():
    """Test that the probability of eating is correct"""
    num_trial = 10000

    carn = std_carn()
    herb = std_herb()

    diff_fitness = carn.fitness - herb.fitness

    if diff_fitness < 0:
        probability_of_killing = 0
    elif 0 < diff_fitness and diff_fitness < carn.params["DeltaPhiMax"]:
        probability_of_killing = (carn.fitness - herb.fitness) / carn.params["DeltaPhiMax"]
    else:
        probability_of_killing = 1

    num_kills = 0
    for i in range(num_trial):
        carn.feeding([herb])
        if not herb.alive:
            num_kills += 1
            herb.alive = True

    assert stats.binom_test(num_kills, num_trial, probability_of_killing) > .01


def test_carn_eat_prob_fitness():
    """Test that carnivore cannot eat if their fitness is lower than the herbivores"""
    herb = std_herb()
    carn = std_carn()

    herb.fitness = 1
    carn.fitness = 0.5

    for i in range(10000):
        carn.feeding([herb])

    assert herb.alive == True
