import pytest
from pytest import approx
import random
import math
from biosim.animals import Animal, Herbivore #, Carnivore


'''
Tests-structure for island-class
- animals have attributes strength | age | f
- No other letters than W, L, H, D
- Geography must be surrounded by W (water)
- Each character must represent a cell with character code
- Each cell must have character information
- No animals in water

Not implemented yet
- water, desert, highland, lowland
- no migration yet
- Coordinate system (1,1) in upper left corner
- the first coordinate enumerates rows, the second coordinate enumerates columns

Requirements violated
- raise value error
'''
#TEST ANIMAL
# create
@pytest.mark.parametrize("loc, species, age, weight", [[(1, 2), "Herbivore", 5, 20],
                                                       [(2, 1), "Herbivore", 0, 1],
                                                       [(10, 3), "Herbivore", 150, 2000]])
def test_init(loc, species, age, weight):
    """Test that animal is created with correct attributes"""
    stat = {'species': species,
            'age': age,
            'weight': weight}

    if species == "Herbivore":
        animal = Herbivore(stat, loc)
    elif species == "Carnivore":
       #animal = Carnivore(stat, loc)
        pass

    result = {'loc': animal.loc,
              'species': animal.species,
              'age': animal.age,
              'weight': animal.weight,
              "fitness": animal.fitness,
              "alive": animal.alive,
              "newborn": animal.newborn
              }

    fitness_age_param = 1/(1 + math.exp(animal.phi_age * (age - animal.a_half)))
    fitness_weight_param = 1/(1 + math.exp(-animal.phi_weight * (weight - animal.w_half)))

    fitness = fitness_age_param * fitness_weight_param



    expected = {'loc': loc,
                'species': 'Herbivore',
                'age': age,
                'weight': weight,
                "fitness": fitness,
                "alive": True,
                "newborn": None
                }
    assert result == approx(expected)


# TODO: Procreation

# Calc_fitness
@pytest.mark.parametrize("species, age, weight", [["Herbivore", 5, 20],
                                                   ["Herbivore", 0, 1],
                                                   ["Herbivore", 150, 2000]])
def test_calc_fitness(species, age, weight):
    """Test that fitness is calculated correctly"""
    loc = (1, 1)
    stat = {'species': species,
            'age': age,
            'weight': weight}

    if species == "Herbivore":
        animal = Herbivore(stat, loc)
    elif species == "Carnivore":
        #animal = Carnivore(stat, loc)
        pass

    animal.calc_fitness()

    result = animal.fitness

    fitness_age_param = 1/(1 + math.exp(animal.phi_age * (animal.age - animal.a_half)))
    fitness_weight_param = 1/(1 + math.exp(-animal.phi_weight * (animal.weight - animal.w_half)))

    expected = fitness_age_param * fitness_weight_param

    assert result == approx(expected)
# age / aging

@pytest.mark.parametrize("age", [-100,-1,0 ,1 , 2, 3, 4, 5, 6, 100, 1000])
def test_aging(age):
    """Test that age is increased by 1"""
    loc = (1, 1)
    stat = {'species': 'Herbivore',
            'age': age,
            'weight': 20}
    animal = Herbivore(stat, loc)
    animal.aging()
    assert animal.age == age + 1


# weight / loss of weight

@pytest.mark.parametrize("weight", [1 , 2, 3, 4, 5, 6, 100, 1000])
def test_loss_of_weight(weight):
    """Test that weight is decreased by 1"""
    loc = (1, 1)
    stat = {'species': 'Herbivore',
            'age': 5,
            'weight': weight}
    animal = Herbivore(stat, loc)
    animal.loss_of_weight()
    assert animal.weight == approx(weight - animal.eta * weight)





# death
@pytest.mark.parametrize("species, age, weight, seed", [("Herbivore", 5, 20, 1),
                                                        ("Herbivore", 0, 1, 2),
                                                        ("Herbivore", 2, 200, 0),
                                                        ("Herbivore", 100, 40, 1)])

def test_death(species, age, weight, seed):
    """Test that animal dies when weight is 0 or less and that it dies with the correct probability"""
    loc = (1, 1)
    stat = {'species': species,
            'age': age,
            'weight': weight}

    animal = Herbivore(stat, loc)
    random.seed(seed)
    animal.death()

    random.seed(seed)
    probability_of_death = animal.omega * (1 - animal.fitness)
    if animal.weight <= 0:
        expected = False
    elif random.random() < probability_of_death:
        expected = False
    else:
        expected = True

    assert animal.alive == expected
# Feeding Herbivore

@pytest.mark.parametrize("weight, fodder", [(20, 10),
                                            (1,1),
                                            (200, 100),
                                            (100, 1),
                                            (100, 2),
                                            (100, 3),
                                            (100, 4),
                                            (100, 5),
                                            (100, 6),
                                            (100, 7),
                                            (100, 8),
                                            (100, 9),
                                            (100, 10),
                                            (100, 11),
                                            (100, 12)])
def test_feeding_herbivore(weight, fodder):
    """Test that herbivore eats the correct amount of fodder and that weight is increased by the correct amount"""
    loc = (1, 1)
    stat = {'species': 'Herbivore',
            'age': 10,
            'weight': weight}

    animal = Herbivore(stat, loc)
    amount_eaten = animal.feeding(fodder)
    result = (animal.weight, amount_eaten)

    expected_amount_eaten = min(animal.F, fodder)
    expected_weight = weight + expected_amount_eaten * animal.beta
    expected = (expected_weight, expected_amount_eaten)

    assert result == approx(expected)


# Feeding Carnivore


# Migration


# procreate

# error handling

