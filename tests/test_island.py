'''
Tests-structure for island-class
- All lines must have same length
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
from biosim.cell import Water, Desert, Highland, Lowland
from biosim.island import Island
import pytest


def test_create_island():
    """Test that island is created with correct attributes"""
    map_string = """\
                    W
                    """
    Island(map_string)


@pytest.mark.parametrize("letter", ["W", "L", "H", "D"])
def test_process_input_map(letter):
    """Test that the input map is processed correctly"""
    map_string = f"""\
                    WWW
                    W{letter}W
                    WWW
                    """

    island = Island(map_string)

    expected = ["WWW", f"W{letter}W", "WWW"]
    assert island._process_input_map(map_string) == expected


@pytest.mark.parametrize("letter", ["L", "H", "D"])
def test_wrong_boundry(letter):
    """Invalid boundry in map string raises ValueError"""

    map_string = f"""\
                    {letter}WW
                    WLW
                    WWW
                    """

    with pytest.raises(ValueError):
        Island(map_string)


@pytest.mark.parametrize("letter", ["L", "H", "D"])
def test_wrong_boundry2(letter):
    """Invalid boundry in map string raises ValueError"""

    map_string = f"""\
                    WWW
                    WLW
                    WW{letter}
                    """

    with pytest.raises(ValueError):
        Island(map_string)


def test_wrong_character():
    """Invalid character in map string raises ValueError"""

    map_string = """\
                    WWW
                    WRW
                    WWW
                    """

    with pytest.raises(ValueError):
        Island(map_string)


def test_wrong_length():
    """Invalid length of map string raises ValueError"""

    map_string = """\
                    WWW
                    W
                    WWW
                    """

    with pytest.raises(ValueError):
        Island(map_string)


def test_correct_map():
    map_string = """\
                        WWWW
                        WHLW
                        WWWW"""

    island = Island(map_string)
    processed_map = island._process_input_map(map_string)

    map = island._map_processed_to_dict(processed_map)

    for loc, cell in map.items():
        assert cell.type[0] == processed_map[loc[0] - 1][loc[1] - 1]


def test_add_population():
    """Test that the add_population puts animals in right cell with information"""

    map_string = """\
                    WWWW
                    WLDW
                    WWWW
                    WWWW
                    """
    number = 5
    island = Island(map_string)
    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                          for _ in range(number)]}]

    island.add_population(ini_herbs)

    assert len(island.map[(2, 2)].fauna["Herbivore"]) == number


@pytest.mark.parametrize("letter", ["W", "L", "H", "D"])
def test_add_cell(letter):
    cells = {
        'W': Water,
        'L': Lowland,
        'H': Highland,
        'D': Desert
    }

    island = Island("WWW\nWLW\nWWW")

    assert type(island._add_cell(letter, (2, 2))) == cells[letter]


def test_move_all_animals():
    """Test that the move_all_animals moves all animals to the right cell"""
    map_string = """\
                    WWWW
                    WLDW
                    WWWW
                    WWWW
                    """
    number = 5
    island = Island(map_string)
    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                          for _ in range(number)]}]

    island.add_population(ini_herbs)

    animals = island.map[(2, 2)].animals

    moving_list = [(animal, (2, 2), (2, 3)) for animal in animals]

    island._move_all_animals(moving_list)

    assert len(island.map[(2, 3)].fauna["Herbivore"]) == number
