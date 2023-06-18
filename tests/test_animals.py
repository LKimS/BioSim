import pytest
from pytest import approx
import random
import math

from biosim.animals import Herbivore, Carnivore, Animal

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
    with pytest.raises(ValueError):
        if species == "Herbivore":
            Herbivore.set_parameters(change)
        elif species == "Carnivore":
            Carnivore.set_parameters(change)

@pytest.mark.parametrize("loc, species, age, weight, new_params", [[(1, 2), "Herbivore", 5, 20, {"phi_age": 0.6, "phi_weight": 0.1, "a_half": 40, "w_half": 10}],
                                                       [(2, 1), "Herbivore", 0, 1, {"phi_age": 0.1, "phi_weight": 0.6, "a_half": 20, "w_half": 15}],
                                                       [(10, 3), "Herbivore", 150, 2000, {"phi_age": 0.1, "phi_weight": 0.6, "a_half": 20, "w_half": 15}],
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

    fitness_age_param = 1/(1 + math.exp(new_params["phi_age"] * (age - new_params["a_half"])))
    fitness_weight_param = 1/(1 + math.exp(-new_params["phi_weight"] * (weight - new_params["w_half"])))

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
    assert animal.calc_fitness() == approx(fitness)

def test_update_fitness():
    """Test that fitness is updated correctly"""
    stat = {'species': "Herbivore",
            'age': 5,
            'weight': 20}
    animal = Herbivore(stat, (1, 2))
    # change age and weight
    animal.age = 10
    animal.weight = 10
    animal.update_fitness()
    assert animal.fitness == approx(animal.calc_fitness())
