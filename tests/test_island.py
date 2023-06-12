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

from biosim.island import Island

def test_init():
    """Test that the init method works as expected"""
    pass



def test_process_input_map():
    map_string = """\
                    WHLD
                    WLDH
                    WWWW
                    HHHH
                    """

    island = Island(map_string)

    expected = ["WHLD", "WLDH", "WWWW", "HHHH"]
    assert island.process_input_map(map_string) == expected

def test_add_population():
    """Test that the add_population puts animals in right cell with information"""

    map_string = """\
                    WHLD
                    WLDH
                    WWWW
                    HHHH
                    """
    number = 5
    island = Island(map_string)
    ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(number)]}]

    island.add_population(ini_herbs)

    assert len(island.map[(2,2)].herbivore) == number



"""
def test_all_lines_same_length():
    pass

def test_no_other_letters_than_W_L_H_D():
    pass

def test_geography_must_be_surrounded_by_W():
    pass

def test_each_character_must_represent_a_cell():
    pass

def test_each_cell_must_have_characteristics_information():
    pass

def test_no_animals_in_water():
    pass
"""