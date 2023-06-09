"""
Template for BioSim class.
"""
from biosim.island import Island
import matplotlib.pyplot as plt

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2023 Hans Ekkehard Plesser / NMBU


class BioSim:
    """
    Top-level interface to BioSim package.
    """

    def __init__(self, island_map, population, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_years=None, img_dir=None, img_base=None, img_fmt='png',
                 log_file=None):

        self.island = Island(island_map, seed)
        self.island.add_population(population)

        self.img_dir = img_dir
        self.img_base = img_base
        self.img_years = img_years
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

    def set_animal_parameters(self, species, params):
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

    def set_landscape_parameters(self, landscape, params):
        pass

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

    def plot_population_history(self):
        plt.plot(self.island_history)


    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        Parameters
        ----------
        num_years : int
            Number of years to simulate
        """

        self.cell_history = {}
        self.island_history = [] #gjøre om dict med lister under

        for x in range(1, self.island.map_height + 1):
            for y in range(1, self.island.map_width + 1):
                self.cell_history[(x, y)] = []

        for year in range(1, num_years + 1):
            sum_herbivore = 0
            for x in range(1, self.island.map_height + 1):  # Actually y axsis
                for y in range(1, self.island.map_width + 1):  # Actually x axsis
                    # tile/cell work
                    cell = self.island.map[(x, y)]
                    cell.count_animals()
                    sum_herbivore += cell.count_herbivore
                    #sum_carnivore += cell.count_carnivore
                    # teller dyr i cellen
                    self.cell_history[(x, y)].append(cell.count_herbivore)
                    #pop_animals[(x, y)].append(cell.count_carnivore)
                    # newborn in cell
                    cell.add_newborns(cell.herbivore)
                    cell.add_newborns(cell.carnivore)
                    cell.feed_animals()
                    cell.update_fitness()
                    # ceel.migration()
                    cell.age_animals()
                    cell.loss_of_weight()
                    cell.animal_death()
                    cell.reset_fodder()

            self.island_history.append(sum_herbivore)
        self.plot_population_history()


    def add_population(self, population):
        """
        Add a population to the island

        Parameters
        ----------
        population : List of dictionaries
            See BioSim Task Description, Sec 3.3.3 for details.
        """
        pass


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
