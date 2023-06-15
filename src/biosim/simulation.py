"""
Implements a complete simulation.
"""
from .island import Island
from .cell import Lowland, Highland
from .animals import Herbivore, Carnivore
from .graphics import Graphics


import matplotlib.pyplot as plt

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2023 Hans Ekkehard Plesser / NMBU


class BioSim:
    """
    Top-level interface to BioSim package.
    """

    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None, live_visualization=True,
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
        live_visualization : bool
            Boolean specifying if live visualization is to be used (default: True)
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
        self.pop_history = {'Herbivore': [], 'Carnivore': []}
        self.graphics = Graphics(img_dir, img_base, img_fmt)
        self.current_year = 1


    def set_animal_parameters(self, species, new_parameters):
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

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        Parameters
        ----------
        num_years: number of simulation steps to execute
        vis_years: interval between visualization updates
        img_years: interval between visualizations saved to files (default: vis_years)

        Notes
        -----
        Image files will be numbered consecutively.
        """
        self.final_year = self.current_year + num_years

        self.vis_years = vis_years

        if img_years is None:
            img_years = vis_years

        if img_years % vis_years != 0:
            raise ValueError('img_years must be multiple of vis_steps')

        self.graphics.setup(self.island.bitmap, self.final_year)




        while self.current_year < self.final_year + 1:
            self.island.yearly_island_cycle()
            self.upate_graphics(self.current_year,
                                     herbivore_population=self.island.pop['Herbivore'],
                                     carnivore_population=self.island.pop['Carnivore'],
                                     herbivore_dict_map=self.island.pop_cell['Herbivore'],
                                     carnivore_dict_map=self.island.pop_cell['Carnivore'],
                                     herbivore_age_list=self.island.specs['Herbivore']['age'],
                                     carnivore_age_list=self.island.specs['Carnivore']['age'],
                                     herbivore_weight_list=self.island.specs['Herbivore']['weight'],
                                     carnivore_weight_list=self.island.specs['Carnivore']['weight'],
                                     herbivore_fitness_list=self.island.specs['Herbivore']['fitness'],
                                     carnivore_fitness_list=self.island.specs['Carnivore']['fitness'])

            self.current_year += 1

    def upate_graphics(self ,
                       year,
                       herbivore_population = [],
                       carnivore_population = [],
                       herbivore_dict_map = {},
                       carnivore_dict_map = {},
                       herbivore_age_list = [],
                       carnivore_age_list = [],
                       herbivore_weight_list = [],
                       carnivore_weight_list = [],
                       herbivore_fitness_list = [],
                       carnivore_fitness_list = []):
        """
        Update graphics with animal info from current year.

        Parameters
        ----------
        year
        herbivore_population
        carnivore_population
        herbivore_dict_map
        carnivore_dict_map
        herbivore_age_list
        carnivore_age_list
        herbivore_weight_list
        carnivore_weight_list
        herbivore_fitness_list
        carnivore_fitness_list

        Returns
        -------

        """


        if year % self.vis_years == 0:
            self.graphics.update(self.current_year,
                                 herbivore_population=herbivore_population,
                                 carnivore_population=carnivore_population,
                                 herbivore_dict_map=herbivore_dict_map,
                                 carnivore_dict_map=carnivore_dict_map,
                                 herbivore_age_list=herbivore_age_list,
                                 carnivore_age_list=carnivore_age_list,
                                 herbivore_weight_list=herbivore_weight_list,
                                 carnivore_weight_list=carnivore_weight_list,
                                 herbivore_fitness_list=herbivore_fitness_list,
                                 carnivore_fitness_list=carnivore_fitness_list)

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
        self.graphics.make_movie()
