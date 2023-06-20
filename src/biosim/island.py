# -*- coding: utf-8 -*-

"""
    The Island class introduce the yearly cycle of the simulation by:

    - Create a map of the island.
    - Add animals to the map.
    - Run through an early lifecycle.
    - Gather data from one year, and store it for visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
import random

from .cell import Water, Lowland, Highland, Desert


class Island:
    """

    """

    allowed_cells = ['W', 'L', 'H', 'D']

    # INIT METHOD
    def __init__(self, input_island_map, random_seed=0):
        """
        Class constructor for island.

        Parameters
        ----------
        input_island_map : str
            Multi-line string with island geography
        random_seed : int
            Integer used as random number seed.
        """
        random.seed(random_seed)

        self.map_processed = self._process_input_map(input_island_map)
        self.map_height = self._get_map_height(self.map_processed)
        self.map_width = self._get_map_width(self.map_processed)
        self.map = self._map_processed_to_dict(self.map_processed)
        self.habital_map = self._get_map_with_animals()
        self.bitmap = self.create_colormap(self.map_processed)

        self.pop_in_cell = {'Herbivore': {}, 'Carnivore': {}}
        self.pop = {'Herbivore': 0, 'Carnivore': 0}

        self.specs = {'Herbivore': {'weight': [], 'age': [], 'fitness': []},
                      'Carnivore': {'weight': [], 'age': [], 'fitness': []}}

    # METHODS for input and processing
    def _process_input_map(self, input_island_map):
        """
        Processes string with island geography

        Parameters
        ----------
        input_island_map : str
            Multi-line string with island geography

        """
        lines = input_island_map.split("\n")
        processed_lines = [line.strip() for line in lines]
        processed_lines = [line for line in processed_lines if line != '']

        self._island_compatibility_check(processed_lines)

        return processed_lines

    def _island_compatibility_check(self, processed_lines):
        """
        Checks if input_island_map is compatible with the Island class.

        Parameters
        ----------
        processed_lines: list
            List of strings with island geography

        Raises
        ------
        ValueError
            If the island is not surrounded by water.
        ValueError
            If the island contains letters other than W, L, H, D.
        ValueError
            If the island contains lines with different lengths.

        """

        line_width = len(processed_lines[0])

        for row, line in enumerate(processed_lines):
            if len(line) != line_width:
                raise ValueError("All lines must contain the same number of letters.")
            for column, letter in enumerate(line):
                if letter not in self.allowed_cells:
                    raise ValueError(f"Only letters W, L, H, D are allowed. Not {letter}.")
                if row == 0 or row == len(processed_lines) - 1:
                    if letter != 'W':
                        raise ValueError("Geography must be surrounded by water.")
                if column == 0 or column == len(line) - 1:
                    if letter != 'W':
                        raise ValueError("Geography must be surrounded by water.")

    def _get_map_height(self, map_processed):
        """
        Get the height of the map

        Parameters
        ----------
        map_processed : list

        Returns
        -------
        int : height of map
        """
        return len(map_processed)

    def _get_map_width(self, map_processed):
        """
        Get the width of the map

        Parameters
        ----------
        map_processed : list

        Returns
        -------
        int : width of map
        """
        return len(map_processed[0])

    def _map_processed_to_dict(self, map_processed):
        """
        Creates a map (dict) with coordinates as keys and cell objects as values

        Parameters
        ----------
        map_processed : list

        Returns
        -------
        dict : map with coordinates as keys and cell objects as values
        """
        map = {}

        for x in range(1, self.map_height + 1):
            for y in range(1, self.map_width + 1):
                cell_letter = map_processed[x - 1][y - 1]
                map[(x, y)] = self._add_cell(cell_letter, (x, y))

        return map

    # TODO: move into method above
    def _get_map_with_animals(self):
        """
        Creates a map(dict) with only habitable cells

        Returns
        -------
        dict: map with animals
        """
        map_with_animals = {loc: cell for loc, cell in self.map.items() if cell.is_habitable}

        return map_with_animals

    def _add_cell(self, cell_letter, loc):
        """
        Adds a cell object to the map

        Parameters
        ----------
        cell_letter : str
            Letter representing the cell type
        loc : tuple
            Coordinates of the cell

        Returns
        -------
        Cell : cell object
        """
        cells = {
            'W': Water,
            'L': Lowland,
            'H': Highland,
            'D': Desert
        }
        cell = cells[cell_letter](loc)

        return cell

    # METHODS for adding animals
    def add_population(self, population):
        """
        Adds animals to the map with a given location.

        Parameters
        ----------
        population : list
            List of dictionaries with animals location and information.

        Raises
        ------
        ValueError
            If location does not exist on island.
        """
        for item in population:
            loc = item["loc"]
            if loc not in self.map:
                raise ValueError("Location does not exist on island.")

            for animal_info in item['pop']:
                self.map[loc].add_animal_from_dict(animal_info)

    def _move_all_animals(self, list_of_moving_animals):
        """
        Moves animals from old location to new location.

        Parameters
        ----------
        list_of_moving_animals : list of tuples

        """
        for animal, old_location, new_location in list_of_moving_animals:

            if new_location in self.habital_map and animal.alive:
                self.habital_map[new_location].add_animal_object(animal)
                self.habital_map[old_location].remove_animal(animal)

    # METHODS for creating bitmap and plotting
    def create_colormap(self, map_processed):
        """
        Creates a bitmap for plotting by using the length and width of the processed map.
        Returns a color map of the island shown in visualization.

        Parameters
        ----------
        map_processed : list
            List of strings with island geography.

        Returns
        -------
        bitmap  : numpy.ndarray
            A island map with colors for visualization.

        """

        height = len(map_processed)
        width = len(map_processed[0])

        bitmap = np.empty((height, width, 3), dtype=np.float32)

        for x in range(height):
            for y in range(width):
                loc = (x + 1, y + 1)
                bitmap[x, y] = self.map[loc].color

        return bitmap

    def plot_map(self):
        """
        Plots the map using bitmap.
        """
        plt.imshow(self.bitmap)
        # plt.legend()
        plt.show()

    # METHODS for yearly cycle

    def yearly_island_cycle(self):
        """
        Method runs through each cell on the island.
        For every year the method resets the data for statistics,
        and puts in the data from the previous year.

        Yearly island cycle calling cell methods for:

        - adding newborns
        - feeding animals
        - moving animals
        - aging animals
        - loss of weight
        - animal death
        - resetting fodder
        """
        migrating_animals = []
        self.specs = {'Herbivore': {'weight': [], 'age': [], 'fitness': []},
                      'Carnivore': {'weight': [], 'age': [], 'fitness': []}}

        for loc, cell in self.habital_map.items():

            cell.add_newborns()
            cell.feed_animals()
            migrating_animals.extend(cell.moving_animals_list())
            cell.age_animals()
            cell.loss_of_weight()
            cell.animal_death()
            cell.reset_fodder()
            self.update_data(loc, cell)
        self._move_all_animals(migrating_animals)
        self.collect_data()

    def update_data(self, loc, cell):
        """
        Refreshes gathered data in each cell on the island.
        Method is counting the species in one cell,
        and gather their age, weight and fitness into lists.

        Parameters
        ----------
        loc : tuple
        cell : object

        """
        self.pop_in_cell['Herbivore'][loc] = cell.count_herbivore
        self.pop_in_cell['Carnivore'][loc] = cell.count_carnivore

        for animal in cell.animals:
            self.specs[animal.species]['age'].append(animal.age)
            self.specs[animal.species]['weight'].append(animal.weight)
            self.specs[animal.species]['fitness'].append(animal.fitness)

    def collect_data(self):
        """
        Summarizes number of animals of each species on the island.

        """
        self.pop['Herbivore'] = sum(self.pop_in_cell['Herbivore'].values())
        self.pop['Carnivore'] = sum(self.pop_in_cell['Carnivore'].values())
