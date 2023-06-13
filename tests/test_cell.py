"""Test the Cell-class."""
import pytest
from pytest import approx
import math

from biosim.cell import Cell_with_animals, Lowland, Highland, Desert, Water



def test_init():
    """Test that the cell is created with correct attributes."""
    loc = (2, 2)
    cell = Cell_with_animals(loc)

    assert cell.location == loc
    assert cell.herbivore == []
    assert cell.carnivore == []
    assert cell.count_herbivore == 0
    assert cell.count_carnivore == 0

def test_add_animal():
    """Test that the animal is added to the cell."""
    loc = (2, 2)
    cell = Cell_with_animals(loc)

    animal_info = {'species': 'Herbivore',
                   'age': 5,
                   'weight': 20}

    cell.add_animal_from_dict(animal_info)

    assert cell.herbivore[0].species == 'Herbivore'
    assert cell.herbivore[0].age == 5
    assert cell.herbivore[0].weight == 20

def test_add_animal_wrong_species():
    """Test that the animal is added to the cell."""
    loc = (2, 2)
    cell = Cell_with_animals(loc)

    animal_info = {'species': 'Skilpadde',
                   'age': 5,
                   'weight': 20}

    with pytest.raises(ValueError):
        cell.add_animal_from_dict(animal_info)

def test_count_animals():
    """Test that the number of animals in the cell is counted correctly."""
    loc = (2, 2)
    cell = Cell_with_animals(loc)

    animal_info = {'species': 'Herbivore',
                   'age': 5,
                   'weight': 20}

    cell.add_animal_from_dict(animal_info)
    cell.update_animal_count()

    assert  cell.count_herbivore == 1

def test_add_newborns():
    """Test that the newborns are added to the cell."""
    # TODO: Testen feiler når sannsynligheten for å få barn ikke slår til. Så bør utarbeides videre
    loc = (2, 2)
    cell = Cell_with_animals(loc)

    animal_info = {'species': 'Herbivore',
                   'age': 6,
                   'weight': 3000}
    cell.add_animal_from_dict(animal_info)
    cell.herbivore[0].fitness = 1
    cell.herbivore[0].gamma = 1

    animal_list = cell.herbivore
    cell.add_newborns(animal_list)

    assert cell.herbivore[1].species == 'Herbivore'
    assert cell.herbivore[1].age == 0

def test_feed_animals():
    """Test that all animals in the cell have their weight updated correctly."""
    loc = (2, 2)
    cell = Lowland(loc)

    list = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(1)]
    for animal_info in list:
        cell.add_animal_from_dict(animal_info)

    cell.feed_animals()

    assert cell.herbivore[0].weight > 20


def test_update_fitness():
    """Test that all animals in the cell have their fitness updated correctly."""
    loc = (2, 2)
    cell = Cell_with_animals(loc)

    animal_info = {'species': 'Herbivore',
                   'age': 6,
                   'weight': 3000}
    cell.add_animal_from_dict(animal_info)
    old_fitness = cell.herbivore[0].fitness

    cell.herbivore[0].weight = 20
    cell.herbivore[0].age = 10
    cell.update_fitness()

    assert cell.herbivore[0].fitness < old_fitness

def sort_animals_by_fitness():
    #TODO: Test til sortering av dyr etter fitness
    pass


def test_age_animals():
    """Test that all animals in the cell have their age updated correctly."""

    loc = (2, 2)
    cell = Cell_with_animals(loc)

    list = [{'species': 'Herbivore', 'age': 5,'weight': 20} for _ in range(3)]
    for animal_info in list:
        cell.add_animal_from_dict(animal_info)

    cell.age_animals()

    for animal in cell.herbivore:
        assert animal.age == 6



def test_loss_of_weight():
    """Test that all animals in the cell have their weight updated correctly."""

    loc = (2, 2)
    cell = Cell_with_animals(loc)
    weight = 20
    list = [{'species': 'Herbivore', 'age': 5,'weight': weight} for _ in range(3)]
    for animal_info in list:
        cell.add_animal_from_dict(animal_info)

    cell.loss_of_weight()

    for animal in cell.herbivore:
        assert animal.weight == approx(weight - weight * animal.eta)

def test_animal_death():
    """Test that the animals in the cell die correctly."""

    loc = (2, 2)
    cell = Cell_with_animals(loc)
    n_herbivore = 3
    n_dead = 2
    list = [{'species': 'Herbivore', 'age': 5,'weight': 20} for _ in range(n_herbivore)]
    for animal_info in list:
        cell.add_animal_from_dict(animal_info)

    for _ in range(n_dead):
        cell.herbivore[_].weight = 0

    cell.animal_death()
    assert len(cell.herbivore) == n_herbivore-n_dead



