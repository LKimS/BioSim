"""
Implements a complete simulation for BioSim class.
"""
from .cell import Lowland, Highland, Water, Desert
from .animals import Herbivore, Carnivore
from .island import Island

import matplotlib.pyplot as plt

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2023 Hans Ekkehard Plesser / NMBU


class BioSim:
    """
    Top-level interface to BioSim package.
    """

    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_years=None, img_dir=None, img_base=None, img_fmt='png',
                 log_file=None):

        """
        Parameters
        ----------
        island_map : str
            Multi-line string specifying island geography
        ini_pop : list
            List of dictionaries specifying initial population
        seed : int
            Integer used as random number seed
        vis_years : int
            Years between visualization updates (if 0, disable graphics)
        ymax_animals : int
            Number specifying y-axis limit for graph showing animal numbers
        cmax_animals : dict
            Color-scale limits for animal densities, see below
        hist_specs : dict
            Specifications for histograms, see below
        img_years : int
            Years between visualizations saved to files (default: `vis_years`)
        img_dir : str
            Path to directory for figures
        img_base : str
            Beginning of file name for figures
        img_fmt : str
            File type for figures, e.g. 'png' or 'pdf'
        log_file : str
            If given, write animal counts to this file

        Notes
        -----
        - If `ymax_animals` is None, the y-axis limit should be adjusted automatically.
        - If `cmax_animals` is None, sensible, fixed default values should be used.
        - `cmax_animals` is a dict mapping species names to numbers, e.g.,

          .. code:: python

             {'Herbivore': 50, 'Carnivore': 20}

        - `hist_specs` is a dictionary with one entry per property for which a histogram
          shall be shown. For each property, a dictionary providing the maximum value
          and the bin width must be given, e.g.,

          .. code:: python

             {'weight': {'max': 80, 'delta': 2},
              'fitness': {'max': 1.0, 'delta': 0.05}}

          Permitted properties are 'weight', 'age', 'fitness'.
        - If `img_dir` is None, no figures are written to file.
        - Filenames are formed as

          .. code:: python

             Path(img_dir) / f'{img_base}_{img_number:05d}.{img_fmt}'

          where `img_number` are consecutive image numbers starting from 0.

        - `img_dir` and `img_base` must either be both None or both strings.
        """
        self.island = Island(island_map, seed)
        self.island.add_population(ini_pop)

        self.img_dir = img_dir
        self.img_base = img_base
        self.img_years = img_years

    def set_animal_parameters(self, species, new_parameters):
        pass
        """
        Set parameters for animal species.

        Parameters
        ----------
        species : str
            Name of species for which parameters shall be set.
        params : dict
            New parameter values

        Raises
        ------
        ValueError
            If invalid parameter values are passed.
        """

        if species == "Herbivore":
            Herbivore.set_parameters(new_parameters)

        elif species == "Carnivore":
            Carnivore.set_parameters(new_parameters)
        else:
            raise ValueError("Invalid species. Choose between Herbivore and Carnivore")


    def set_landscape_parameters(self, landscape, new_parameters):
        """
        Set parameters for landscape type.

        Parameters
        ----------
        landscape : str
            Code letter for landscape
        params : dict
            New parameter values

        Raises
        ------
        ValueError
            If invalid parameter values are passed.
        """
        if landscape == "L":
            Lowland.set_parameters(new_parameters)
        elif landscape == "H":
            Highland.set_parameters(new_parameters)
        else:
            raise ValueError("Invalid landscape. Only L and H has fodder")


    def plot_population_history(self):
        plt.plot(self.island_pop_history['Herbivore'],'b')
        plt.plot(self.island_pop_history['Carnivore'], 'r')


    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        Parameters
        ----------
        num_years : int
            Number of years to simulate
        """

        self.cell_pop_history = {}
        self.island_pop_history = {'Herbivore': [], 'Carnivore': []}

        for x in range(1, self.island.map_height + 1):
            for y in range(1, self.island.map_width + 1):
                self.cell_pop_history[(x, y)] = {'Herbivore': [], 'Carnivore': []}

        habital_map = self.island.habital_map

        for year in range(1, num_years + 1):
            sum_herbivore = 0
            sum_carnivore = 0
            migrating_animals = []
            # tile/cell work
            for loc, cell in habital_map.items():
                # Teller dyr i cellen
                cell.update_animal_count()
                sum_herbivore += cell.count_herbivore
                sum_carnivore += cell.count_carnivore
                self.cell_pop_history[loc]['Herbivore'].append(cell.count_herbivore)
                self.cell_pop_history[loc]['Carnivore'].append(cell.count_carnivore)

                # pop_animals[(x, y)].append(cell.count_carnivore)
                # newborn in cell
                cell.add_newborns(cell.herbivore)
                cell.add_newborns(cell.carnivore)
                cell.feed_animals()
                migrating_animals.extend(cell.moving_animals_list())
                cell.age_animals()
                cell.loss_of_weight()
                cell.animal_death()
                cell.reset_fodder()

            self.island_pop_history['Herbivore'].append(sum_herbivore)
            self.island_pop_history['Carnivore'].append(sum_carnivore)

            self.island.move_all_animals(migrating_animals)
        self.plot_population_history()


    def update_animal_count(self, cell):
        """
        Update the number of animals on the island
        """
        cell.update_animal_count()



    def add_population(self, population):
        """
        Add a population to the island

        Parameters
        ----------
        population : List of dictionaries
            See BioSim Task Description, Sec 3.3.3 for details.
        """

        self.island.add_population(population)


    @property
    def year(self):
        """Last year simulated."""

    @property
    def num_animals(self):
        """Total number of animals on island."""

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
