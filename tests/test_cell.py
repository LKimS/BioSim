"""Test the Cell-class."""
import pytest
from pytest import approx
import math
import itertools

from biosim.cell import Lowland, Highland, Desert, Water
from biosim.animals import Herbivore, Carnivore, Animal


@pytest.mark.parametrize("cell_class", [Lowland, Highland, Desert, Water])
def test_init(cell_class):
    """Test that the cell is created with correct attributes."""
    loc = (2, 2)
    cell = cell_class(loc)

    assert cell.location == loc


@pytest.mark.parametrize("cell_class, species", [(Lowland, "Herbivore"),
                                                 (Highland, "Carnivore"),
                                                 (Desert, "Carnivore")])
def test_add_animal(cell_class, species):
    """Test that the animal is added to the cell."""
    loc = (2, 2)
    cell = cell_class(loc)

    animal_info = {'species': species,
                   'age': 5,
                   'weight': 20}

    cell.add_animal_from_dict(animal_info)
    result = {"species": cell.fauna[species][0].species,
              "age": cell.fauna[species][0].age,
              "weight": cell.fauna[species][0].weight}

    assert result == approx(animal_info)


@pytest.mark.parametrize("cell_class", [Lowland, Highland, Desert, Water])
def test_add_animal_wrong_species(cell_class):
    """Test that the animal is added to the cell."""
    loc = (2, 2)
    cell = cell_class(loc)

    animal_info = {'species': 'Skilpadde',
                   'age': 5,
                   'weight': 20}

    with pytest.raises(ValueError):
        cell.add_animal_from_dict(animal_info)


@pytest.mark.parametrize("animal_info", [{'species': 'Herbivore',
                                          'age': -5,
                                          'weight': 20},
                                         {'species': 'Carnivore',
                                          'age': 5,
                                          'weight': -20},
                                         {'species': 'Carnivore',
                                          'random_number': 5,
                                          'weight': 20},
                                         {'species': 'Canivore',
                                          'age': 5,
                                          'random_number': 20}])
def test_adding_wrong_animal_params(animal_info):
    """Test error handling when adding animal with wrong parameters."""
    loc = (2, 2)
    cell = Lowland(loc)

    with pytest.raises(ValueError):
        cell.add_animal_from_dict(animal_info)


def test_add_animal_to_water():
    """
    Test that the animal is not added to the cell if the cell is water.
    """
    cell = Water((2, 2))
    animal_info = {'species': 'Herbivore',
                   'age': 5,
                   'weight': 20}

    with pytest.raises(ValueError):
        cell.add_animal_from_dict(animal_info)


@pytest.mark.parametrize("cell_class", [Lowland, Highland, Desert])
def test_add_animal_obj(cell_class):
    """Test that the animal is added to the cell."""
    animal_info = {'species': 'Herbivore',
                   'age': 5,
                   'weight': 20}

    animal = Herbivore(animal_info, (2, 2))

    cell = cell_class((2, 2))

    cell.add_animal_object(animal)

    assert cell.animals[0] == animal

def test_add_animal_obj_wrong_species():
    """Test that the animal is added to the cell."""
    animal_info = {'species': 'Herivore',
                   'age': 5,
                   'weight': 20}

    animal = Herbivore(animal_info, (2, 2))

    cell = Lowland((2, 2))

    with pytest.raises(ValueError):
        cell.add_animal_object(animal)


@pytest.fixture
def cell_with_animals():
    """Create a cell with two animals."""
    cell = Lowland((2, 2))

    animal1 = {'species': 'Herbivore',
               'age': 5,
               'weight': 20}

    animal1 = Herbivore(animal1, (2, 2))

    cell.add_animal_object(animal1)

    animal2 = {'species': 'Herbivore',
               'age': 5,
               'weight': 20}

    animal2 = Herbivore(animal2, (2, 2))
    cell.add_animal_object(animal2)

    yield cell, animal1, animal2


def test_remove_animals(cell_with_animals):
    """Test that the animals are removed from the cell."""
    cell, herb, carn = cell_with_animals

    cell.remove_animal(herb)
    cell.remove_animal(carn)

    assert len(cell.animals) == 0


def test_sort_herbs_fitness_desc():
    """Test that the animals are sorted by fitness."""
    cell = Lowland((2, 2))

    animals = [{'species': 'Herbivore',
                'age': age,
                'weight': 20} for age in range(100, 0, -5)]

    for animal in animals:
        cell.add_animal_from_dict(animal)

    cell._sort_herbivore_after_fitness()

    # list of herbivore fitness in ascending order
    fitness_list = [animal.fitness for animal in cell.fauna['Herbivore']]

    # Check if list is sorted with descending order
    is_sorted = all(a >= b for a, b in zip(fitness_list, fitness_list[1:]))

    assert is_sorted


def test_sort_herbs_fitness_asc():
    """Test that the animals are sorted by fitness."""
    cell = Lowland((2, 2))

    animals = [{'species': 'Herbivore',
                'age': age,
                'weight': 20} for age in range(100, 0, -5)]

    for animal in animals:
        cell.add_animal_from_dict(animal)

    cell._sort_herbivore_after_fitness(descending=False)

    # list of herbivore fitness in ascending order
    fitness_list = [animal.fitness for animal in cell.fauna['Herbivore']]

    # Check if list is sorted with descending order
    is_sorted = all(a <= b for a, b in zip(fitness_list, fitness_list[1:]))

    assert is_sorted


@pytest.mark.parametrize("cell_class", [Desert, Water])
def test_change_params_error(cell_class):
    """Test that the method raises error when called on wrong cell type."""
    cell = cell_class((2, 2))

    new_params = {'f_max': 100}

    with pytest.raises(ValueError):
        cell.set_parameters(new_params)


def test_add_newborns(cell_with_animals, mocker):
    """Test that the method is called the right number of times."""
    cell, herb, carn = cell_with_animals

    mocker.spy(Animal, "procreation")

    cell.add_newborns()

    assert Animal.procreation.call_count == 2

def test_feed_animals_count(cell_with_animals, mocker):
    """Test that the method is called the right number of times."""
    mocker.spy(Herbivore, "feeding")
    mocker.spy(Carnivore, "feeding")
    cell, herb, carn = cell_with_animals
    cell.feed_animals()

    assert Herbivore.feeding.call_count + Carnivore.feeding.call_count  == 2

def test_moving_animals_list(cell_with_animals):
    """Test that the new location is in the list of possible locations."""
    cell, herb, carn = cell_with_animals

    for _ in range(100):
        list = cell.moving_animals_list()

        for animal, loc , new_loc in list:
            if new_loc not in ((1,2),(2,1),(2,3),(3,2)):
                assert loc in ((1,2),(2,1),(2,3),(3,2))




@pytest.fixture
def reset_fodder():
    """Reset the fodder in the cell."""
    yield

    Lowland.set_parameters({'f_max': 800})
    Highland.set_parameters({'f_max': 300})

@pytest.mark.parametrize("cell_class", [Lowland, Highland])
def test_set_parameters(reset_fodder, cell_class):
    """Test that the parameters are set correctly."""
    loc = (2, 2)
    cell = cell_class(loc)

    new_params = {'f_max': 1000}

    cell.set_parameters(new_params)

    assert cell.get_parameters() == new_params
@pytest.mark.parametrize("cell_class", [Lowland, Highland])
def test_reset_fodder(reset_fodder, cell_class):
    cell = cell_class((2, 2))

    cell.set_parameters({'f_max': 1000})

    cell.fodder = 1
    cell.reset_fodder()
    assert cell.fodder == 1000

def test_wrong_parameters(reset_fodder):
    """Test that the method raises an error."""
    cell = Lowland((2, 2))

    new_params = {'f_max': -1000}

    with pytest.raises(ValueError):
        cell.set_parameters(new_params)

def test_wrong_param_key(reset_fodder):
    """Test that the method raises an error."""
    cell = Lowland((2, 2))

    new_params = {'f_max': 1000, 'f_min': 100}

    with pytest.raises(ValueError):
        cell.set_parameters(new_params)

def test_age_animals_count(cell_with_animals, mocker):
    """Test that the method is called the right number of times."""
    mocker.spy(Animal, "aging")
    cell, herb, carn = cell_with_animals
    cell.age_animals()

    assert Animal.aging.call_count == 2

def test_loss_of_weight_count(cell_with_animals, mocker):
    """Test that the method is called the right number of times."""
    mocker.spy(Animal, "loss_of_weight")
    cell, herb, carn = cell_with_animals
    cell.loss_of_weight()

    assert Animal.loss_of_weight.call_count == 2

def test_animal_death_count(cell_with_animals, mocker):
    """Test that the method is called the right number of times."""
    mocker.spy(Animal, "death")
    cell, herb, carn = cell_with_animals
    cell.animal_death()

    assert Animal.death.call_count == 2



