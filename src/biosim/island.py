# -*- coding: utf-8 -*-

"""
Implements of Island class.
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

from .cell import Water, Lowland, Highland, Desert


# TODO: error handling and bitmap to plot map



class Island:

    """
    Island class. Superclass for all landscape types.
    """
#INIT METHOD
    def __init__(self, input_island_map, random_seed=0):
        """
        Class constructor for island.
        Parameters
        ----------
        self
        input_island_map
        random_seed

        Returns
        -------

        """
        random.seed(random_seed)
        self.map_processed = self.process_input_map(input_island_map)
        self.map_height = self.get_map_height(self.map_processed)
        self.map_width = self.get_map_width(self.map_processed)
        bool = self.check_line_length(self.map_processed)
        self.map = self.map_processed_to_dict(self.map_processed)
        self.habital_map = self.get_map_with_animals()
        self.bitmap = self.create_bitmap(self.map_processed)

        self.pop_cell = {'Herbivore': {}, 'Carnivore': {}}
        self.pop = {'Herbivore': 0, 'Carnivore': 0}

        self.specs = {'Herbivore': {'weight': [], 'age': [], 'fitness': []},
                      'Carnivore': {'weight': [], 'age': [], 'fitness': []}}



#METHODS for input and processing
    def process_input_map(self, input_island_map):
        """
        Processes the input island map.
        Parameters
        ----------
        self
        input_island_map

        Returns
        -------

        """
        lines = input_island_map.split("\n")
        processed_lines = [line.strip() for line in lines]
        processed_lines = [line for line in processed_lines if line != '']
        return processed_lines

    def get_map_height(self, map_processed):
        return len(map_processed)

    def get_map_width(self, map_processed):
        return len(map_processed[0])

    def map_processed_to_dict(self, map_processed):
        map = {}

        for x in range(1, self.map_height+1):
            for y in range(1, self.map_width + 1):
                cell_letter = map_processed[x-1][y-1]
                map[(x,y)] = self.add_cell(cell_letter, (x,y))

        return map

    def get_map_with_animals(self):
        map_with_animals = {}
        for x in range(1, self.map_height+1):
            for y in range(1, self.map_width + 1):
                loc = (x,y)
                if self.map[loc].is_habitable:
                    map_with_animals[(x,y)] = self.map[(x,y)]

        return map_with_animals

    def add_cell(self, cell_letter, loc):
        cells = {
            'W': Water,
            'L': Lowland,
            'H': Highland,
            'D': Desert
        }
        cell = cells[cell_letter](loc)

        return cell


#METHODS for adding animals
    def add_population(self, population):
        for item in population:
            x, y = item["loc"]
            for animal_info in item['pop']:
                self.map[(x,y)].add_animal_from_dict(animal_info)

            #self.map[(x,y)].update_animal_count()

    def migrate_animals(self):
        all_moving_animals = []
        for old_location, cell in self.habital_map.items():
            all_moving_animals.extend(cell.moving_animals_list())

        self.move_all_animals(all_moving_animals)

    def move_all_animals(self,list_of_moving_animals):
        """
        Moves animals from old location to new location.
        """
        for animal, old_location, new_location in list_of_moving_animals:

            if new_location in self.habital_map and animal.alive:
                self.habital_map[new_location].add_animal_object(animal)
                self.habital_map[old_location].remove_animal(animal)


#METHODS for creating bitmap and plotting
    def create_bitmap(self, map_processed):

        height = len(map_processed)
        width = len(map_processed[0])

        bitmap = np.empty((height,width, 3), dtype=np.float32)

        for x in range(height):
            for y in range(width):
                loc = (x+1,y+1)
                bitmap[x,y] = self.map[loc].color

        return bitmap

    def plot_map(self):
        plt.imshow(self.bitmap)
        #plt.legend()
        plt.show()

    # ERROR HANDLING
    def check_line_length(self, island_map_processed):
        line1 = island_map_processed[0]
        for line in island_map_processed[1:]:
            if len(line) != len(line1):

                return False


#METHODS for yearly cycle

    def yearly_island_cycle(self):
        migrating_animals = []

        self.specs = {'Herbivore': {'weight': [], 'age': [], 'fitness': []},
                      'Carnivore': {'weight': [], 'age': [], 'fitness': []}}

        for loc , cell in self.habital_map.items():
            self.update_data(loc, cell)
            cell.add_newborns(cell.herbivore)
            cell.add_newborns(cell.carnivore)
            cell.feed_animals()
            migrating_animals.extend(cell.moving_animals_list())
            cell.age_animals()
            cell.loss_of_weight()
            cell.animal_death()
            cell.reset_fodder()
        self.move_all_animals(migrating_animals)
        self.collect_data()

    def update_data(self, loc, cell):
        """Update data for visualization of island map."""
        self.pop_cell['Herbivore'][loc] = cell.count_herbivore
        self.pop_cell['Carnivore'][loc] = cell.count_carnivore


        for animal in cell.herbivore+cell.carnivore:
            self.specs[animal.species]['age'].append(animal.age)
            self.specs[animal.species]['weight'].append(animal.weight)
            self.specs[animal.species]['fitness'].append(animal.fitness)



    def collect_data(self):
        """Collects data from all cells on island."""
        self.pop['Herbivore'] = sum(self.pop_cell['Herbivore'].values())
        self.pop['Carnivore'] = sum(self.pop_cell['Carnivore'].values())


