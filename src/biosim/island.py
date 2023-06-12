import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

from biosim.animals import Animal
from .cell import Water, Lowland, Highland, Desert

# TODO: error handling and bitmap to plot map

"""
Vizualization of island map
- Plot heatmap of population density
- Animate simulation

ERROR HANDLING: 
- All lines must have same length
- No other letters than W, L, H, D
- Geography must be surrounded by W (water)
- No animals in water
"""

class Island:

    #INIT METHOD
    def __init__(self, input_island_map, random_seed=0):
        random.seed(random_seed)

        self.map_processed = self.process_input_map(input_island_map)
        self.map_height = self.get_map_height(self.map_processed)
        self.map_width = self.get_map_width(self.map_processed)

        bool = self.check_line_length(self.map_processed)

        self.map = self.map_processed_to_dict(self.map_processed)

        self.habital_map = self.get_map_with_animals()

        self.bitmap = self.create_bitmap(self.map_processed)


    #METHODS for input and processing
    def process_input_map(self, input_island_map):
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

            self.map[(x,y)].update_animal_count()

    def migrate_animals(self):
        moving_animals = []
        for old_location in self.habital_map:
            remove_animals = []
            for animal in self.habital_map[old_location].animals:
                if True:
                    new_location = self.get_random_neighboring_cell(old_location)

                    if new_location in self.habital_map:
                        moving_animals.append((animal, old_location, new_location))


                        for l in [old_location, new_location]:
                            self.habital_map[l].update_animal_count()

                    else:
                        print('no migration' + str(old_location))

        self.move_all_animals(moving_animals)






    def get_random_neighboring_cell(self, location):
        """
        Returns a random neighboring cell.
        """
        new_location = list(location)
        dim = random.choice([0, 1])
        new_location[dim] += random.choice([-1, 1])

        return tuple(new_location)

    def move_all_animals(self,list_of_moving_animals):
        """
        Moves animals from old location to new location.
        """
        for animal, old_location, new_location in list_of_moving_animals:
            self.habital_map[new_location].add_animal_object(animal)
            self.habital_map[old_location].remove_animal(animal)
            print('from', old_location, 'to', new_location)





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


