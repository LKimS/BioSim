"""
Implements a complete simulation for BioSim class.
"""
from .island import Island
from .cell import Lowland, Highland
from .animals import Herbivore, Carnivore
from .graphics import Graphics

import csv
import pickle


# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2023 Hans Ekkehard Plesser / NMBU


class BioSim:
    """
    BioSim class is the top-level interface to BioSim package. It implements a complete simulation
    of the ecosystem.
    Choose between multiple different parameters to adjust your simulation and preferred output.
    """
    _default_map = """\
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

    def __init__(self, island_map=None, ini_pop=None, seed=123,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_years=None, img_dir=None, img_base=None, img_fmt='png',
                 log_file=None):
        """
        Initializes the BioSim class with the following parameters:

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

        self.final_year = None
        self.current_year = 0

        if island_map is None:
            island_map = self._default_map
            print('Using default map')

        self.island = Island(island_map, seed)

        if ini_pop is not None:
            self.island.add_population(ini_pop)
        self.pop_history = {'Herbivore': {}, 'Carnivore': {}}

        if vis_years <= 0 and type(vis_years) != int:
            raise ValueError('vis_years must be a positive integer')
        self.vis_years = vis_years

        if self.vis_years != 0:
            self.graphics = Graphics(img_dir=img_dir, img_name=img_base,
                                     img_fmt=img_fmt, img_years=img_years,
                                     vis_years=vis_years, ymax_animals=ymax_animals,
                                     cmax_animals=cmax_animals, hist_specs=hist_specs)

            self.img_years = vis_years

            if self.img_years % vis_years != 0:
                raise ValueError('img_years must be multiple of vis_steps')
        else:
            print('Visualization is disabled')

        self.log_file = log_file

    def set_animal_parameters(self, species, new_parameters):
        """
        Set parameters for animal species.

        Parameters
        ----------
        species : str
            Name of species for which parameters shall be set.
        new_parameters : dict
            New parameter values

        Raises
        ------
        ValueError
            If invalid parameter values are passed.


        Example
        --------
        .. code:: python

            sim.set_animal_parameters('Carnivore', {'a_half': 70,
                                                    'phi_age': 0.5,
                                                    'omega': 0.3,
                                                    'DeltaPhiMax': 9.})

        Parameters can be used to simulate sickness and changes in the animal.

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
        new_parameters : dict
            New parameter values

        Raises
        ------
        ValueError
            If invalid parameter values are passed.


        Example
        --------

        .. code:: python

            sim.set_landscape_parameters('L', {'f_max': 700})

        Parameter 'L' is for Lowland,
        and by decreasing the f_max, the amount of fodder is decreased.

        """
        if landscape == "L":
            Lowland.set_parameters(new_parameters)
        elif landscape == "H":
            Highland.set_parameters(new_parameters)
        else:
            raise ValueError("Invalid landscape. Only L and H has fodder")

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result. Look at __init__
        for information about the parameters and features.

        :param num_years: number of simulation steps to execute

        .. note:: If image directory is given then image files will be numbered consecutively.
        """

        self.final_year = self.current_year + num_years

        if self.vis_years != 0:
            self.graphics.setup(self.island.map_processed, self.final_year)

        self.update_island_data()

        self.update_history_data()

        self.update_graphics()

        while self.current_year < self.final_year:

            self.island.yearly_island_cycle()
            self.current_year += 1
            year = self.current_year
            print(f"\rSimulating... year: {year} out of {self.final_year}", flush=True, end='')
            self.update_history_data()

            self.update_graphics()
        print()

        if self.log_file is not None:
            print(f"Saving log file to {self.log_file}")
            self.save_log_file()

    def update_graphics(self):
        if self.vis_years != 0 and self.current_year % self.vis_years == 0:
            self.graphics.update(self.current_year,
                                 herbivore_population=self.island.pop['Herbivore'],
                                 carnivore_population=self.island.pop['Carnivore'],
                                 herbivore_dict_map=self.island.pop_in_cell['Herbivore'],
                                 carnivore_dict_map=self.island.pop_in_cell['Carnivore'],
                                 herbivore_age_list=self.island.specs['Herbivore']['age'],
                                 carnivore_age_list=self.island.specs['Carnivore']['age'],
                                 herbivore_weight_list=self.island.specs['Herbivore']['weight'],
                                 carnivore_weight_list=self.island.specs['Carnivore']['weight'],
                                 herbivore_fitness_list=self.island.specs['Herbivore']['fitness'],
                                 carnivore_fitness_list=self.island.specs['Carnivore']['fitness'])

    def update_history_data(self):
        """
        Updates history data for visualization.
        """

        self.pop_history['Herbivore'][self.current_year] = self.island.pop['Herbivore']
        self.pop_history['Carnivore'][self.current_year] = self.island.pop['Carnivore']

    def update_island_data(self):
        for loc, cell in self.island.habital_map.items():
            self.island.update_data(loc, cell)
        self.island.collect_data()

    def add_population(self, population):
        """
        Adds population on a location on the Island.
        Follow examples bellow for list-format.

        Parameters
        ----------
        population : List of dictionaries
            List with dictionary. Keys 'loc' and 'pop'.


        Example
        ---------
        .. code:: python

            ini_herbs = [{'loc': (3, 2),
            'pop': [{'species': 'Herbivore',
            'age': 5, 'weight': 20} for _ in range(150)]}]

        Permitted keys within 'pop' are age, weight and species.

        """

        self.island.add_population(population)

    def save_log_file(self):
        """
        Save population history as a csv file.

        Example
        -------
        .. code:: python

            year,Herbivore,Carnivore
            0,150,50
            1,200,40
            2,300,30

        """
        if self.log_file is None:
            return

        if self.log_file[-4:] != ".csv":
            self.log_file += ".csv"

        with open(self.log_file, "w") as file:
            writer = csv.writer(file)
            header = ["year"] + list(self.pop_history.keys())
            writer.writerow(header)

            for year in range(self.current_year + 1):
                count = [self.pop_history[species][year] for species in self.pop_history.keys()]
                row = [year] + count
                writer.writerow(row)

    def _save_simulation(self, file_name):
        """
        Save the simulation to a file.

        :param file_name: name of file to save to

        This feature is not fully implemented yet.
        """
        if file_name[-4:] != ".pkl":
            file_name += ".pkl"

        with open(file_name, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def _load_simulation(file_name):
        """
        Load a simulation from a file.

        :param file_name: name of file to load from
        :return: simulation object

        This feature is not fully implemented yet.
        """
        with open(file_name, "rb") as file:
            sim = pickle.load(file)

        return sim

    @property
    def year(self):
        """
        Last year simulated.

        Return
        -------
        year : int
            Last year simulated.

        """

        return self.current_year

    @property
    def num_animals(self):
        """
        Total number of animals on island.

        Return
        -------
        num_animal : int
            Number of animals on island

        """
        num_animal = 0

        self.update_island_data()
        self.update_history_data()

        for pop_history in self.pop_history.values():
            num_animal += pop_history[self.current_year]

        return num_animal

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.

        Return
        -------
        num_animals_per_species : dict
            Number of animals per species in island, as dictionary.
        """
        # If population is None, return zero. If not None, return last population history

        self.update_island_data()
        self.update_history_data()

        year = self.current_year

        current_pop = {species: p_history[year] for species, p_history in self.pop_history.items()}
        return current_pop

    def make_movie(self, movie_fmt='mp4'):
        """
        Create MPEG4 movie from visualization images saved.

        Parameters
        ----------
        movie_fmt : mp4
            Format of movie, defaults to 'mp4'.

        """
        if self.vis_years == 0:
            return ValueError('To turn on movie making, set vis_years > 0')

        self.graphics.make_movie(movie_fmt)
