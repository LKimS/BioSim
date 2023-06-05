import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# TODO: error handling and bitmap to plot map

class Island:

    geography = {
        "W": {
            "type": "Water",
            "fodder": 0,
            "herbivore": 0,
            "carnivore": 0,
            "color": (0.13, 0.00, 1.00)
        },
        "L": {
            "type": "Lowland",
            "fodder": 0,
            "herbivore": 0,
            "carnivore": 0,
            "color": (0.00, 0.62, 0.00)
        },
        "H": {
            "type": "Highland",
            "fodder": 0,
            "herbivore": 0,
            "carnivore": 0,
            "color": (0.20, 1.00, 0.42)
        },
        "D": {
            "type": "Desert",
            "fodder": 0,
            "herbivore": 0,
            "carnivore": 0,
            "color": (1.00, 1.00, 0.40)
        }
    }


    def __init__(self, input_island_map):
        self.map_processed = self.process_input_map(input_island_map)

        bool = self.check_line_length(self.map_processed)

        map = self.map_processed_to_dict(self.map_processed)

        self.bitmap = self.create_bitmap(self.map_processed)


        self.map = map

    def process_input_map(self, input_island_map):
        lines = input_island_map.split("\n")
        processed_lines = [line.strip() for line in lines]
        return processed_lines

    def map_processed_to_dict(self, map_processed):
        map = {}
        line_length = len(map_processed[0])

        for i in range(1, len(map_processed)+1):
            map[i] = {}
            for j in range(1, line_length + 1):
                map[i][j] = self.geography[map_processed[i-1][j-1]]

        map = map

        return map

    def create_bitmap(self, map_processed):

        height = len(map_processed)
        width = len(map_processed[0])

        bitmap = np.empty((height,width, 3), dtype=np.float32)

        for i in range(height):
            for j in range(width):
                bitmap[i,j] = self.geography[map_processed[i][j]]["color"]

        return bitmap

    def plot_map(self):
        plt.imshow(self.bitmap)
        #plt.legend()
        plt.show()


    def check_line_length(self, island_map_processed):
        line1 = island_map_processed[0]
        for line in island_map_processed[1:]:
            if len(line) != len(line1):

                return False

if __name__ == "__main__":
    map = """\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHLLLLLLLLLLLLWWW
               WHHHHHLLLDDLLLHLLLWWW
               WHHLLLLLDDDLLLHHHHWWW
               WWHHHHLLLDDLLLHWWWWWW
               WHHHLLLLLDDLLLLLLLWWW
               WHHHHLLLLDDLLLLWWWWWW
               WWHHHHLLLLLLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""

    A = Island(map)
    #bitmap = A.bitmap

    print(repr(A.map))
    print(A.map[1][1])

